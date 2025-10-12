import pytest
import pathlib
from coding_agent.agent import run_agent


examples_root = pathlib.Path(__file__).parent.parent / "examples"

@pytest.mark.asyncio
async def test_examples(question: str):
    code = await run_agent("", "")
    ...