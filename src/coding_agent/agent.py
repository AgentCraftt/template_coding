"""ReAct agent implementation constrained to a Python execution tool."""

from __future__ import annotations
import re
from coding_agent.llm import LLM
from coding_agent.tools.code_executor import execute_code
from typing import Optional, List, Tuple
import textwrap


THOUGHT_REGEX = re.compile(r"<thought>\s*(.*?)\s*</thought>", re.DOTALL | re.IGNORECASE)
EXEC_REGEX = re.compile(r"<execute>\s*(.*?)\s*</execute>", re.DOTALL | re.IGNORECASE)
SOLUTION_REGEX = re.compile(r"<solution>\s*(.*?)\s*</solution>", re.DOTALL | re.IGNORECASE)
FINISH_REGEX = re.compile(r"<finish>\s*(.*?)\s*</finish>", re.DOTALL | re.IGNORECASE)

SYSTEM_PROMPT = (
    "You are a ReAct-style assistant. Each response must contain both a "
    "<thought> and an <execute> (or <solution>) section.\n"
    "The only valid executable action is to place raw Python code inside "
    "<execute>...</execute> tags, exactly as shown below.\n"
    "You can verify your answer for the question through using tools. After you verify the answer, "
    "you can respond with `<solution> answer </solution>` in a separate turn.\n"
    "Always print any intermediate results that are needed to derive the final answer.\n\n"
    "Format:\n"
    "<thought> your reasoning </thought>\n"
    "<execute>\n"
    "# python code (no backticks)\n"
    "</execute>\n"
    "... then, when finished ...\n"
    "<thought> reasoning </thought>\n"
    "<solution> final_answer </solution>\n"
)

class CodingAgent:
    def __init__(self, model_name: str = "gpt-4o-mini"):
        self.model = LLM(model_name)

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
        """Extract final <solution> or <finish> answer."""
        return (
            CodingAgent._extract_tag_content(FINISH_REGEX, text)
            or CodingAgent._extract_tag_content(SOLUTION_REGEX, text)
        )

    async def run(self, question: str) -> Tuple[str, List[dict]]:
        prompt = (
            SYSTEM_PROMPT
            + "\n\n----\n\n# Problem:\n"
            + str(question)
        )

        messages: List[dict] = [{"role": "system", "content": prompt}]

        while True:
            # LLM call
            response = await self.model.acompletion(messages=messages)
            messages.append({"role": "assistant", "content": response})

            # 1️⃣ check for <solution> / <finish>
            answer = self._extract_answer(response)
            if answer:
                return answer, messages

            # 2️⃣ extract <execute> code
            code = self._extract_code(response)
            if not code:
                observation = "Invalid action: please use <execute>...</execute> with Python code."
                messages.append({"role": "user", "content": f"Observation: {observation}"})
                return "Agent failed: missing action.", messages

            # 3️⃣ execute safely in sandbox
            sandbox_output = await execute_code(code)
            obs = sandbox_output.run_result.stdout if sandbox_output.status.name == "Success" else f"Error: {sandbox_output.run_result.stderr}"
            messages.append({"role": "user", "content": f"Observation: {obs}"})

        
async def run_agent(model_name: str, question: str) -> Tuple[str, List[dict]]:
    return await CodingAgent(model_name).run(question)