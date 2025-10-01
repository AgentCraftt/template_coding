"""ReAct agent implementation constrained to the Python interpreter tool."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple

import re
import textwrap

import litellm

if __package__ in (None, ""):
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent.parent))

from template_coding.tools.python import sandbox_fusion_execute


SYSTEM_PROMPT = """
You are a ReAct-style assistant. Each response must contain both a Thought and an Action. The only valid action is `python(<code>)`. Only when you get the <answer> from python(<code>), emit `Action: Finish(<answer>)` in a separate response turn. In order to get the <answer>, please remember to print the result whenever necessary in the <code>.
""".strip()


@dataclass
class AgentConfig:
    model: str = "gpt-4o-mini"
    max_steps: int = 4


THOUGHT_REGEX = re.compile(r"Thought:\s*(.*?)(?=\n[A-Za-z]+:|\Z)", re.DOTALL)
ACTION_REGEX = re.compile(r"Action:\s*(.*?)(?=\n[A-Za-z]+:|\Z)", re.DOTALL)


def _parse_thought_action(message: str) -> Tuple[str | None, str | None]:
    thought_match = THOUGHT_REGEX.search(message)
    action_match = ACTION_REGEX.search(message)

    thought = thought_match.group(1).strip() if thought_match else None
    action = action_match.group(1).strip() if action_match else None
    print("ACTION:")
    print(action)
    return thought, action


def _extract_python_code(action: str) -> str | None:
    match = re.match(r"^python\s*\((.*)\)\s*$", action, re.DOTALL)
    if not match:
        return None
    code = match.group(1).strip()
    print("code:")
    print(code)
    if not code:
        return None

    # if code.startswith('"""') and code.endswith('"""'):
    #     code = code[3:-3]
    # elif code.startswith("'''") and code.endswith("'''"):
    #     code = code[3:-3]
    # elif code[0] == code[-1] and code[0] in {'"', "'"}:
    #     code = code[1:-1]

    code = textwrap.dedent(code).strip()
    return code or None


def react(question: str, config: AgentConfig | None = None) -> Tuple[str, List[dict]]:
    cfg = config or AgentConfig()

    messages: List[dict] = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": question},
    ]

    for _ in range(cfg.max_steps):
        response = litellm.completion(model=cfg.model, messages=messages)
        assistant_message = response.choices[0].message.content or ""
        messages.append({"role": "assistant", "content": assistant_message})

        thought, action = _parse_thought_action(assistant_message)

        if not action:
            return ("Agent failed: missing action.", list(messages))

        if action.lower().startswith("finish"):
            return (thought or assistant_message or "Finished.", list(messages))

        code = _extract_python_code(action)
        if code is None:
            observation = "Invalid action. Only python(<code>) is allowed."
            messages.append({"role": "user", "content": f"Observation: {observation}"})
            return ("Agent stopped: invalid action.", list(messages))

        sandbox_output, success = sandbox_fusion_execute(code)
        observation = sandbox_output if success else f"Error: {sandbox_output}"
        messages.append({"role": "user", "content": f"Observation: {observation}"})

    return ("Agent stopped: maximum steps exceeded.", list(messages))
