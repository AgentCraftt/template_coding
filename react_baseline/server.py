"""Server entrypoint for running the agent in a container or locally.

Provides both a programmatic ``run()`` and an HTTP server (FastAPI) when
executed as a script. The HTTP server listens on port 7777 by default.
"""

from __future__ import annotations

from typing import Any, Dict

# Support both package and flat imports so this file can be used
# inside the `react_baseline` package or copied to a flat workspace.
try:  # package-relative
    from .llm import LLMConfig as _LLMConfig
    from . import llm
    from .agent import ReActAgent
except Exception:  # flat layout fallback
    from llm import LLMConfig as _LLMConfig
    import llm
    from agent import ReActAgent
# HTTP server support (FastAPI)
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

LLMConfig = _LLMConfig


def run(llm_config: LLMConfig, question: str, **kwargs) -> Dict[str, Any]:
    """Run the agent with the given config and question.

    Parameters
    ----------
    llm_config: LLMConfig
        Provider + model configuration for LiteLLM. ``provider`` and ``model``
        must be specified; optional params like ``temperature``, ``top_p``,
        ``top_k`` can be provided via the config ``extra`` or as keyword args.
    question: str
        The question to ask. Required.
    **kwargs
        Optional overrides: ``max_steps``, ``temperature``, ``top_p``, ``top_k``,
        ``max_tokens``. These will be forwarded to the LLM call.

    Returns
    -------
    Dict[str, Any]
        A dict with ``answer`` and ``history`` keys.
    """

    if not (llm_config and getattr(llm_config, "provider", None)):
        raise ValueError("llm_config.provider is required")
    if not getattr(llm_config, "model", None):
        raise ValueError("llm_config.model is required")
    if not question or not isinstance(question, str):
        raise ValueError("question is required and must be a non-empty string")

    # Merge selected overrides into config extras to flow to llm.completion
    extras = dict(llm_config.extra or {})
    for key in ("temperature", "top_p", "top_k", "max_tokens"):
        if key in kwargs and kwargs[key] is not None:
            extras[key] = kwargs[key]

    merged = LLMConfig(
        provider=llm_config.provider,
        model=llm_config.model,
        temperature=extras.pop("temperature", llm_config.temperature),
        max_tokens=extras.pop("max_tokens", llm_config.max_tokens),
        api_base=llm_config.api_base,
        api_key=llm_config.api_key,
        extra={**(llm_config.extra or {}), **extras},
    )

    llm.configure(merged)

    max_steps = int(kwargs.get("max_steps", 4))
    agent = ReActAgent(model=merged.model, max_steps=max_steps)
    answer, history = agent.run(question)
    return {"answer": answer, "history": history}


if FastAPI is not None:
    class LLMConfigModel(BaseModel):
        provider: str
        model: str
        temperature: float | None = None
        max_tokens: int | None = None
        api_base: str | None = None
        api_key: str | None = None
        top_p: float | None = None
        top_k: int | None = None
        extra: dict | None = None

    class RunRequest(BaseModel):
        llm: LLMConfigModel
        question: str
        max_steps: int = 4

    app = FastAPI(title="ReAct Baseline Server")

    @app.post("/run")
    def run_endpoint(req: RunRequest):
        try:
            cfg = LLMConfig(
                provider=req.llm.provider,
                model=req.llm.model,
                temperature=req.llm.temperature or 0.0,
                max_tokens=req.llm.max_tokens,
                api_base=req.llm.api_base,
                api_key=req.llm.api_key,
                extra={**(req.llm.extra or {}), **{k: v for k, v in {
                    "top_p": req.llm.top_p,
                    "top_k": req.llm.top_k,
                }.items() if v is not None}},
            )
            result = run(cfg, question=req.question, max_steps=req.max_steps)
            return result
        except Exception as exc:
            raise HTTPException(status_code=400, detail=str(exc))


__all__ = ["run", "LLMConfig"]
