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


class RunRequest(BaseModel):
    question: str
    model: str
    max_cost: str


@app.post("/run_agent")
async def post_run_agent(req: RunRequest) -> Dict[str, Any]:
    """
    Single endpoint where we will run the agent with a model name and question.
    """
    try:
        llm = LLM(req.model)
        answer = await run_agent(llm, req.question, req.max_cost)
        return answer, llm._requests
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
