"""
Minimal FastAPI server for running the agent.

Exposes a single POST endpoint `/post_run_agent`
that accepts a JSON payload:
{
  "model_name": "gpt-4o-mini",
  "question": "Explain quantum entanglement"
}
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
from coding_agent.agent import run_agent

app = FastAPI(title="Agent Server")

class RunRequest(BaseModel):
    model_name: str
    question: str


@app.post("/run_agent")
async def post_run_agent(req: RunRequest) -> Dict[str, Any]:
    """
    Single endpoint to run the agent with a model name and question.
    """
    try:
        answer, history = await run_agent(req.model_name, req.question)
        return {"answer": answer, "history": history}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))