"""
Evaluation script that starts the coding agent server in background,
reads examples, sends questions to the server, and tests returned code.
"""
import asyncio
import json
import subprocess
import time
import base64
from pathlib import Path
from typing import Dict, Any, List, Optional

import httpx
from sandbox_fusion import RunCodeRequest, run_code


def test_solution(solution: str, test: str):
    base64_content = base64.b64encode(solution.encode("utf-8")).decode("utf-8")
    request = RunCodeRequest(
        language="pytest",
        code=test,
        files={"solution.py": base64_content},
    )
    return run_code(request)


class AgentEvaluator:
    """
    Evaluator that manages server lifecycle and runs evaluations on examples.
    """

    def __init__(self, model: str, max_cost: float):
        self.model = model
        self.max_cost = max_cost
        self.base_url = f"http://localhost:8888"
        self.examples_dir = Path("examples")
        self.server_process: Optional[subprocess.Popen] = None
        self.log_file = f'eval_log_{time.strftime("%m-%d-%H-%M")}.txt'
        self.log_fd = None

    def start_server(self):
        """Start the FastAPI server in a background subprocess."""
        # Start server using uvicorn command
        # log to self.log_file
        self.log_fd = open(self.log_file, 'w')
        self.server_process = subprocess.Popen(
            ["uv", "run", "uvicorn", "coding_agent.server:app",
             "--host", "localhost", "--port", "8888"],
            text=True,
            stdout=self.log_fd,
            stderr=self.log_fd
        )
        print(f"Server started in background (PID: {self.server_process.pid})")

        # Wait for server to be ready
        self._wait_for_server()

    def _wait_for_server(self, timeout: int = 30):
        """Wait for server to be ready to accept connections."""
        start_time = time.time()
        while time.time() - start_time < timeout:
            try:
                response = httpx.get(f"{self.base_url}/docs", timeout=1.0)
                if response.status_code == 200:
                    print("Server is ready!")
                    return
            except (httpx.ConnectError, httpx.TimeoutException):
                time.sleep(0.5)

        raise TimeoutError("Server failed to start within timeout period")

    def stop_server(self):
        """Stop the background server process."""
        # Close log file if open
        if self.log_fd:
            self.log_fd.close()
            self.log_fd = None
        if self.server_process and self.server_process.poll() is None:
            self.server_process.terminate()
            try:
                self.server_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.server_process.kill()
                self.server_process.wait()
            print("Server stopped")

    def _load_examples(self) -> List[Dict[str, Any]]:
        """Read all examples from the examples directory."""
        examples = []

        if not self.examples_dir.exists():
            print(f"Examples directory not found: {self.examples_dir}")
            return examples

        for example_path in sorted(self.examples_dir.iterdir()):
            if example_path.is_dir():
                question_file = example_path / "question.txt"
                test_file = example_path / "test.py"
                metadata_file = example_path / "metadata.json"

                if question_file.exists() and test_file.exists():
                    with open(question_file, 'r') as f:
                        question = f.read()
                    with open(test_file, 'r') as f:
                        test = f.read()

                    metadata = {}
                    if metadata_file.exists():
                        with open(metadata_file, 'r') as f:
                            metadata = json.load(f)

                    examples.append({
                        'name': example_path.name,
                        'path': example_path,
                        'question': question,
                        'test': test,
                        'metadata': metadata
                    })

        return examples

    async def send_question(self, question: str) -> Dict[str, Any]:
        """Send a question to the server and get the generated code."""
        async with httpx.AsyncClient(timeout=300.0) as client:
            try:
                response = await client.post(
                    f"{self.base_url}/run_agent",
                    json={
                        "question": question,
                        "model": self.model,
                        "max_cost": self.max_cost
                    }
                )
                response.raise_for_status()
                print(response)
                return response.json()
            except httpx.HTTPStatusError as e:
                print(f"Server returned error: {e.response.status_code}")
                print(f"Response body: {e.response.text}")
                raise

    async def run_instance(self, example: Dict[str, Any]) -> Dict[str, Any]:
        """Evaluate a single example."""
        response = await self.send_question(example['question'])
        code = response["code"]
        test = example['test']
        result = test_solution(code, test)
        passed = result.run_result.return_code == 0
        return {
            'name': example['name'],
            'passed': passed,
            'details': result,
            'logs': response['logs']
        }

    async def run_evaluation(self):
        """Run evaluation on all examples."""
        examples = self._load_examples()
        results = []
        for example in examples:
            result = await self.run_instance(example)
            results.append(result)

        # Print summary
        print(f"\n{'='*60}")
        print("EVALUATION SUMMARY")
        print(f"{'='*60}")
        passed = sum(1 for r in results if r.get('passed', False))
        total = len(results)
        print(f"Passed: {passed}/{total} ({100*passed/total:.1f}%)")
        print(f"\nDetailed Results:")
        for result in results:
            status = "✓" if result.get('passed', False) else "✗"
            print(f"  {status} {result['name']}")
        print(f"For more details, see log file: {self.log_file} and evaluation_results.json")
        print(f"To see examples, check the 'examples' directory.")
        return results


async def main():
    """Main entry point for evaluation."""
    import argparse
    argparser = argparse.ArgumentParser(description="Evaluate Coding Agent")
    argparser.add_argument(
        "--model",
        help="Model name to use for evaluation",
        type=str,
        default="gemini/gemini-2.5-pro"
    )
    argparser.add_argument(
        '--max-cost',
        help='Maximum cost allowed per example',
        type=float,
        default=1.0
    )

    args = argparser.parse_args()
    evaluator = AgentEvaluator(model=args.model, max_cost=args.max_cost)

    try:
        # Start server in background
        evaluator.start_server()

        # Run evaluations
        results = await evaluator.run_evaluation()

        # Save results to file
        output_file = Path("evaluation_results.json")
        with open(output_file, 'w') as f:
            json.dump(results, f, indent=2)
        print(f"\nResults saved to {output_file}")
    finally:
        # Stop server
        evaluator.stop_server()


if __name__ == "__main__":
    asyncio.run(main())
