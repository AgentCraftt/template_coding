"""
Coding Agent Template Implementation that is equiped with Python execution tool.
This can be extended to equip with other tools.
"""

from __future__ import annotations
import re
from coding_agent.llm import LLM
from coding_agent.tools.code_executor import execute_code
from typing import Optional, List, Tuple
import textwrap

SYSTEM_PROMPT = (
    "<WRITE YOUR SYSTEM PROMPT HERE THAT DESCRIBE THAT THE TOOLS THAT THE AGENT CAN USE HERE>"
)
EXEC_REGEX = re.compile(r"<execute>\s*(.*?)\s*</execute>", re.DOTALL | re.IGNORECASE)


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

    async def run(self, question: str) -> Tuple[str, List[dict]]:
        """
        Implement the main logic of this Coding Agent Template to solve the given question.    
        
        1. You should call the LLM by `self.model.acompletion` method to get the response from the LLM.
        2. You can implement any additional tools that the agent can use to solve the question, the details of the tools should be implemented in the tool/ directory.
        3. Implement any additional logic to orchestrate the agent's workflow.
        
        Args:
            question (str): A natural langauge question that describes the problem to be solved.

        Returns:
            Tuple[str, List[dict]]: (
                The first element is the final answer to the question.
                The second element is a list of dictionaries that contains the intermediate results that are needed to derive the final answer.
            )
        """
        # your code here
        
async def run_agent(model_name: str, question: str) -> Tuple[str, List[dict]]:
    return await CodingAgent(model_name).run(question)