"""
Exposes a single POST endpoint `/post_run_agent` that accepts a JSON payload:
{
  "model_name": "openai/gpt-4o-mini",
  "question": "Write a function that calculate the sum of a and b in python"
}
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from coding_agent.agent import run_agent
from coding_agent.llm import LLM

app = FastAPI(title="Agent Server")


class AgentInput(BaseModel):
    question: str
    model: str
    max_cost: float


class AgentResponse(BaseModel):
    code: str
    logs: list[Dict[str, Any]]


@app.post("/run_agent")
async def post_run_agent(req: AgentInput) -> AgentResponse:
    """
    Single endpoint where we will run the agent with a model name and question.
    """
    try:
        llm = LLM(req.model, max_cost=req.max_cost)
        code = await run_agent(llm, req.question)
        return AgentResponse(code=code, logs=llm._logs)
    except Exception as e:
        import traceback

        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))
