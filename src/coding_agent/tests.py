import pytest
from fastapi import HTTPException
from coding_agent.server import AgentInput, post_run_agent


@pytest.mark.asyncio
async def test_server_connects_to_agent_interface(monkeypatch):
    """
    Verify the endpoint function calls the agent interface and returns its output.
    Uses monkeypatch to avoid real LLM/sandbox calls.
    """

    async def fake_run_agent(llm, question: str, max_cost: str):
        assert llm.model == "dummy-model"
        assert question == "What is 2+2?"
        return "4"

    monkeypatch.setattr("coding_agent.server.run_agent", fake_run_agent, raising=True)

    req = AgentInput(model="dummy-model", question="What is 2+2?", max_cost="1.0")
    result = await post_run_agent(req)
    assert result[0] == "4"
    assert isinstance(result[1], list)


@pytest.mark.asyncio
async def test_server_propagates_agent_errors(monkeypatch):
    """
    If the agent raises, the endpoint should raise HTTPException 500 with detail.
    """

    async def failing_run_agent(llm, question: str, max_cost: str):
        raise RuntimeError("agent failed")

    monkeypatch.setattr(
        "coding_agent.server.run_agent", failing_run_agent, raising=True
    )

    req = AgentInput(model="dummy-model", question="Anything", max_cost="1.0")
    with pytest.raises(HTTPException) as ei:
        await post_run_agent(req)
    assert ei.value.status_code == 500
    assert "agent failed" in str(ei.value.detail)
