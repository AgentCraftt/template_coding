"""ReAct agent implementation constrained to a Python execution tool."""

from __future__ import annotations
import re
from coding_agent.llm import LLM
from coding_agent.tools.code_executor import execute_code
from typing import Optional, List, Tuple
import textwrap


THOUGHT_REGEX = re.compile(r"<thought>\s*(.*?)\s*</thought>", re.DOTALL | re.IGNORECASE)
EXEC_REGEX = re.compile(r"<execute>\s*(.*?)\s*</execute>", re.DOTALL | re.IGNORECASE)
FINISH_REGEX = re.compile(r"<answer>\s*(.*?)\s*</answer>", re.DOTALL | re.IGNORECASE)

SYSTEM_PROMPT = (
    "You are a ReAct-style assistant. You run in a loop of Thought, Action, PAUSE, Observation.\n"
    "At the end of the loop you output your final answer enclosed in the <answer> tags\n"
    "Use <thought> tags to enclose your reasoning about the question you have been asked.\n"
    "Use Action to run one of the actions available to you - then return PAUSE.\n"
    "Observation will be the result of running those actions."
    "Your available action is:\n"
    "<execute> python_code (with no backticks) </execute>\n\n"
    "Always verify your code by <execute> tool if you have the opportunity to do so.\n\n"
    "Example session:\n\n"
    "Problem:\nWrite a program that sums a + b\n"
    "<thought> I should design a function that takes two inputs a and b that returns their sum.\n"
    "I also need to test the function before returning it.\n"
    "<execute> def sum(a, b):\n    return a + b\n\nif __name__ == '__main__':\n    assert sum(3, 4) == 7\n</execute>"
    "PAUSE\n"    
    "You will be called again with this:\n\n"
    "Observation: {'status': 'success', 'stdout': '', 'stderr': ''}"
    "You then output:"
    "<thought> The assertion error did not arise. The function sum(a, b) is correct. I can now return it.\n"
    "<answer> def sum(a, b):\n    return a + b </answer>\n"
)
class CodingAgent:
    def __init__(self, model: LLM):
        self.model = model

    @staticmethod
    def _extract_tag_content(pattern: re.Pattern, text: str) -> Optional[str]:
        match = pattern.search(text)
        if match:
            content = match.group(1).strip()
            return textwrap.dedent(content).strip() if content else None
        return None

    def _extract_code(self, text: str) -> Optional[str]:
        """Extract Python code from <execute> tags or legacy formats."""
        code = CodingAgent._extract_tag_content(EXEC_REGEX, text)
        if code:
            return code
        
    def _extract_answer(self, text: str) -> Optional[str]:
        """Extract final <finish> or <finish> answer."""
        return (
            CodingAgent._extract_tag_content(FINISH_REGEX, text)
        )

    async def run(self, question: str) -> Tuple[str, List[dict]]:
        messages: List[dict] = [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": f"# Problem:\n{question}"}
        ]

        while True:
            # LLM call
            response = await self.model.acompletion(messages=messages)
            messages.append({"role": "assistant", "content": response})

            # extract <execute> code
            code = self._extract_code(response)
            # check for <finish> / <finish>
            answer = self._extract_answer(response)
            if code:
                # 3️⃣ execute safely in sandbox
                sandbox_output = await execute_code(code)
                obs = sandbox_output.run_result
                messages.append({"role": "user", "content": f"Observation: {obs}"})
                continue
            
            if answer:
                return answer, messages

            if not code:
                observation = "Invalid action: please use <execute>...</execute> if you want to verify your solution. Otherwise return with <answer> ... </answer>"
                messages.append({"role": "user", "content": f"Observation: {observation}"})

        return "Cost Exceeded", messages
        
async def run_agent(model: str, question: str) -> Tuple[str, List[dict]]:
    return await CodingAgent(model).run(question)