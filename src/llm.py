"""Minimal LiteLLM wrapper with a single completion entrypoint.

This module centralizes all LLM calls behind ``completion()`` so the rest of
the codebase does not depend on provider specifics. Configure once via
``configure()`` with an ``LLMConfig`` and then call ``completion(messages=...)``.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional
import litellm


from dotenv import load_dotenv


@dataclass(frozen=True)
class LLMConfig:
    provider: str = "openai"
    model: str = "gpt-4o-mini"
    temperature: float = 0.0
    max_tokens: Optional[int] = None
    api_base: Optional[str] = None
    api_key: Optional[str] = None
    extra: Dict[str, Any] = field(default_factory=dict)


_CONFIG: Optional[LLMConfig] = None


def configure(config: LLMConfig) -> LLMConfig:
    """Configure the global LLM settings used by ``completion``.

    Applies user-supplied credentials first so provider setup can succeed
    without requiring pre-set environment variables.
    """

    provider_key = (config.provider or "openai").strip().lower()

    # Seed env with provided credentials BEFORE provider checks so that
    # `_configure_provider` does not fail when env is missing.
    if provider_key == "chatanywhere":
        if config.api_key:
            os.environ["CHATANYWHERE_API_KEY"] = config.api_key
        if config.api_base:
            os.environ["CHATANYWHERE_API_BASE"] = config.api_base
    else:  # default: openai
        if config.api_key:
            os.environ["OPENAI_API_KEY"] = config.api_key
        if config.api_base:
            os.environ["OPENAI_API_BASE"] = config.api_base

    # Perform provider-specific setup (also mirrors to OPENAI_* for compat)
    _configure_provider(provider_key)

    # Allow explicit overrides in config to take precedence over env.
    if config.api_key:
        litellm.api_key = config.api_key
    if config.api_base:
        litellm.api_base = config.api_base

    global _CONFIG
    _CONFIG = config
    return config


def _ensure_config() -> LLMConfig:
    global _CONFIG
    if _CONFIG is None:
        _CONFIG = LLMConfig()
        configure(_CONFIG)
    return _CONFIG


def _maybe_load_dotenv() -> None:
    if load_dotenv is not None:
        try:
            load_dotenv()  # load default .env if present
        except Exception:
            pass


def _configure_provider(provider: str) -> str:
    """Configure LiteLLM for the requested provider.

    Mirrors env vars for compatibility with OpenAI-compatible SDKs.
    """

    provider_key = (provider or "openai").strip().lower()
    _maybe_load_dotenv()

    if provider_key == "chatanywhere":
        api_key = os.getenv("CHATANYWHERE_API_KEY")
        if not api_key:
            raise RuntimeError(
                "CHATANYWHERE_API_KEY is not set. Add it to your environment or .env file."
            )
        api_base = os.getenv("CHATANYWHERE_API_BASE", "https://api.chatanywhere.tech/v1")

        litellm.api_key = api_key
        litellm.api_base = api_base

        os.environ["OPENAI_API_KEY"] = api_key
        os.environ["OPENAI_API_BASE"] = api_base
        return "chatanywhere"

    # Default: OpenAI
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise RuntimeError(
            "OPENAI_API_KEY is not set. Create a .env or export the key."
        )
    litellm.api_key = api_key

    api_base = os.getenv("OPENAI_API_BASE")
    if api_base:
        litellm.api_base = api_base
        os.environ["OPENAI_API_BASE"] = api_base

    os.environ["OPENAI_API_KEY"] = api_key
    return "openai"


def completion(*, messages: List[dict], **kwargs: Any):
    """Call the underlying provider via LiteLLM.

    Parameters
    ----------
    messages: List[dict]
        Chat messages in OpenAI format.
    **kwargs: Any
        Optional overrides passed directly to ``litellm.completion``.
    """

    cfg = _ensure_config()

    call_kwargs: Dict[str, Any] = {
        "model": cfg.model,
        "messages": messages,
        "temperature": cfg.temperature,
    }
    if cfg.max_tokens is not None:
        call_kwargs["max_tokens"] = cfg.max_tokens

    # Merge any static extras from config and dynamic kwargs from the caller.
    call_kwargs.update(cfg.extra or {})
    call_kwargs.update(kwargs)

    return litellm.completion(**call_kwargs)


__all__ = [
    "LLMConfig",
    "configure",
    "completion",
]
