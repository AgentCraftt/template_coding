"""ReAct agent implementation constrained to a Python execution tool."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional

import re
import textwrap

try:
    from . import llm
    from .tools.python_exec import sandbox_fusion_execute
except Exception:  # flat layout fallback
    import llm
    from tools.python_exec import sandbox_fusion_execute


# ----------------------------------------------------------------------
# Prompt definitions
# ----------------------------------------------------------------------

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

IN_CONTEXT_EXAMPLE = (
    "Task:\n"
    "Complete the following code:\n\n"
    "from typing import Tuple\n"
    "def similar_elements(test_tup1: Tuple[int], test_tup2: Tuple[int]) -> Tuple[int]:\n"
    "    \"\"\"\n"
    "    Write a function to find the similar elements from the given two tuple lists.\n"
    "    assert similar_elements((3, 4, 5, 6),(5, 7, 4, 10)) == (4, 5)\n"
    "    \"\"\"\n\n"
    "Assistant:\n"
    "<thought> The similar elements are those appearing in both tuples. Let's test a draft. </thought>\n"
    "<execute>\n"
    "from typing import Tuple\n"
    "def similar_elements(test_tup1: Tuple[int], test_tup2: Tuple[int]) -> Tuple[int]:\n"
    "    return tuple(set(test_tup1) | set(test_tup2))\n"
    "res = similar_elements((3, 4, 5, 6), (5, 7, 4, 10))\n"
    "assert res == (4, 5), f'Expected (4,5) but got {res}'\n"
    "</execute>\n\n"
    "Observation:\n"
    "AssertionError: Expected (4,5) but got (3, 4, 5, 6, 7, 10)\n\n"
    "Assistant:\n"
    "<thought> I should take the intersection, not the union. </thought>\n"
    "<execute>\n"
    "def similar_elements(test_tup1: Tuple[int], test_tup2: Tuple[int]) -> Tuple[int]:\n"
    "    return tuple(set(test_tup1) & set(test_tup2))\n"
    "res = similar_elements((3, 4, 5, 6), (5, 7, 4, 10))\n"
    "assert res == (4, 5)\n"
    "</execute>\n\n"
    "Observation:\n"
    "[Executed Successfully with No Output]\n\n"
    "Assistant:\n"
    "<thought> No AssertionError — correct! </thought>\n"
    "<solution>\n"
    "def similar_elements(test_tup1: Tuple[int], test_tup2: Tuple[int]) -> Tuple[int]:\n"
    "    return tuple(set(test_tup1) & set(test_tup2))\n"
    "</solution>\n"
)


# ----------------------------------------------------------------------
# Configuration
# ----------------------------------------------------------------------

@dataclass
class AgentConfig:
    model: str = "gpt-4o-mini"
    max_steps: int = 4


# ----------------------------------------------------------------------
# Regex helpers
# ----------------------------------------------------------------------

THOUGHT_REGEX = re.compile(r"<thought>\s*(.*?)\s*</thought>", re.DOTALL | re.IGNORECASE)
EXEC_REGEX = re.compile(r"<execute>\s*(.*?)\s*</execute>", re.DOTALL | re.IGNORECASE)
SOLUTION_REGEX = re.compile(r"<solution>\s*(.*?)\s*</solution>", re.DOTALL | re.IGNORECASE)
FINISH_REGEX = re.compile(r"<finish>\s*(.*?)\s*</finish>", re.DOTALL | re.IGNORECASE)


# ----------------------------------------------------------------------
# ReAct Agent
# ----------------------------------------------------------------------

class ReActAgent:
    def __init__(self, model: str = "gpt-4o-mini", max_steps: int = 4):
        self.config = AgentConfig(model=model, max_steps=max_steps)

    # -- Extraction helpers ---------------------------------------------------

    @staticmethod
    def _extract_tag_content(pattern: re.Pattern, text: str) -> Optional[str]:
        match = pattern.search(text)
        if match:
            content = match.group(1).strip()
            return textwrap.dedent(content).strip() if content else None
        return None

    def _extract_code(self, text: str) -> Optional[str]:
        """Extract Python code from <execute> tags or legacy formats."""
        code = self._extract_tag_content(EXEC_REGEX, text)
        if code:
            return code

        # legacy: python(code)
        legacy = re.match(r"^python\s*\((.*)\)\s*$", text, re.DOTALL)
        if legacy:
            code = legacy.group(1).strip()
            return textwrap.dedent(code).strip() if code else None
        return None

    def _extract_answer(self, text: str) -> Optional[str]:
        """Extract final <solution> or <finish> answer."""
        return (
            self._extract_tag_content(FINISH_REGEX, text)
            or self._extract_tag_content(SOLUTION_REGEX, text)
        )

    # -- Main loop ------------------------------------------------------------

    def run(self, question: str) -> Tuple[str, List[dict]]:
        cfg = self.config
        prompt = (
            SYSTEM_PROMPT
            + "\n\n----\n\n"
            + IN_CONTEXT_EXAMPLE
            + "\n\n----\n\n# Problem:\n"
            + str(question)
        )

        messages: List[dict] = [{"role": "system", "content": prompt}]

        for _ in range(cfg.max_steps):
            # LLM call
            response = llm.completion(messages=messages)
            assistant_msg = getattr(response.choices[0].message, "content", "") or ""
            messages.append({"role": "assistant", "content": assistant_msg})

            # 1️⃣ check for <solution> / <finish>
            answer = self._extract_answer(assistant_msg)
            if answer:
                return answer, messages

            # 2️⃣ extract <execute> code
            code = self._extract_code(assistant_msg)
            if not code:
                observation = "Invalid action: please use <execute>...</execute> with Python code."
                messages.append({"role": "user", "content": f"Observation: {observation}"})
                return "Agent failed: missing action.", messages

            # 3️⃣ execute safely in sandbox
            sandbox_output, success = sandbox_fusion_execute(code)
            obs = sandbox_output if success else f"Error: {sandbox_output}"
            messages.append({"role": "user", "content": f"Observation: {obs}"})

        return "Agent stopped: maximum steps exceeded.", messages


__all__ = ["ReActAgent", "AgentConfig"]
