import pytest
from fastapi import HTTPException
from coding_agent.server import RunRequest, post_run_agent


@pytest.mark.asyncio
async def test_server_connects_to_agent_interface(monkeypatch):
    """
    Verify the endpoint function calls the agent interface and returns its output.
    Uses monkeypatch to avoid real LLM/sandbox calls.
    """

    async def fake_run_agent(model_name: str, question: str):
        assert model_name == "dummy-model"
        assert question == "What is 2+2?"
        return "4", [{"role": "assistant", "content": "<solution>4</solution>"}]

    monkeypatch.setattr("coding_agent.server.run_agent", fake_run_agent, raising=True)

    req = RunRequest(model_name="dummy-model", question="What is 2+2?")
    body = await post_run_agent(req)
    assert body["answer"] == "4"
    assert isinstance(body["history"], list)


@pytest.mark.asyncio
async def test_server_propagates_agent_errors(monkeypatch):
    """
    If the agent raises, the endpoint should raise HTTPException 500 with detail.
    """

    async def failing_run_agent(model_name: str, question: str):
        raise RuntimeError("agent failed")

    monkeypatch.setattr(
        "coding_agent.server.run_agent", failing_run_agent, raising=True
    )

    req = RunRequest(model_name="dummy-model", question="Anything")
    with pytest.raises(HTTPException) as ei:
        await post_run_agent(req)
    assert ei.value.status_code == 500
    assert "agent failed" in str(ei.value.detail)
