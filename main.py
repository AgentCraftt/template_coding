from __future__ import annotations

import argparse
from typing import List

if __package__ in (None, ""):
    # Support running the module directly via `python template_coding/main.py`
    import sys
    from pathlib import Path

    sys.path.append(str(Path(__file__).resolve().parent.parent))

from template_coding.config.env import configure_litellm_provider
from template_coding.agents import AgentConfig, react


def _format_history(history: List[dict]) -> str:
    lines = []
    for message in history:
        role = message.get("role", "?")
        content = message.get("content", "")
        lines.append(f"[{role}] {content}")
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the sandboxed ReAct agent.")
    parser.add_argument("question", nargs="*", help="Question to send to the agent")
    parser.add_argument("--model", default="gpt-4o-mini", help="Model name to use with LiteLLM")
    parser.add_argument(
        "--provider",
        default="openai",
        help="LiteLLM provider to use (openai or chatanywhere).",
    )
    parser.add_argument("--max-steps", type=int, default=4, help="Maximum reasoning steps")
    args = parser.parse_args()

    question = " ".join(args.question).strip() or "What is the sum of squares from 1 to 5?"

    provider = configure_litellm_provider(args.provider)

    answer, history = react(question, AgentConfig(model=args.model, max_steps=args.max_steps))

    print("=== Answer ===")
    print(answer)
    print("\n=== History ===")
    print(_format_history(history))


if __name__ == "__main__":
    main()
