"""Environment helpers and LiteLLM provider configuration."""

from __future__ import annotations

import os
from dataclasses import dataclass
from typing import Optional

try:  # pragma: no cover - optional dependency
    from dotenv import load_dotenv
except ImportError:  # pragma: no cover - fallback when python-dotenv not installed
    load_dotenv = None  # type: ignore[assignment]

import litellm


def _maybe_load_dotenv() -> None:
    if load_dotenv is not None:
        load_dotenv()


def load_openai_api_key(env_var: str = "OPENAI_API_KEY") -> str:
    """Load an API key from the environment (optionally via ``.env``)."""

    _maybe_load_dotenv()
    api_key: Optional[str] = os.getenv(env_var)
    if not api_key:
        raise RuntimeError(
            f"Environment variable '{env_var}' is not set. "
            "Create a .env file or export the key before running the agent."
        )
    return api_key


def configure_litellm_provider(provider: str) -> str:
    """Configure LiteLLM globals for the requested provider."""

    provider_key = (provider or "openai").strip().lower()

    if provider_key == "chatanywhere":
        _maybe_load_dotenv()
        api_key: Optional[str] = os.getenv("CHATANYWHERE_API_KEY")
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

    api_key = load_openai_api_key()
    litellm.api_key = api_key

    api_base = os.getenv("OPENAI_API_BASE")
    if api_base:
        litellm.api_base = api_base
        os.environ["OPENAI_API_BASE"] = api_base

    os.environ["OPENAI_API_KEY"] = api_key

    return "openai"


@dataclass(frozen=True)
class SandboxFusionConfig:
    api_key: str
    template: Optional[str] = None
    endpoint: Optional[str] = None
    project: Optional[str] = None
    region: Optional[str] = None


def load_sandbox_fusion_config() -> SandboxFusionConfig:
    """Load SandboxFusion credentials from the environment or ``.env``."""

    _maybe_load_dotenv()
    endpoint = os.getenv("SANDBOX_FUSION_ENDPOINT")

    if not endpoint:
        raise RuntimeError(
            "SANDBOX_FUSION_ENDPOINT is not set. Please supply credentials for SandboxFusion."
        )
    api_key = os.getenv("SANDBOX_FUSION_API_KEY")
    template = os.getenv("SANDBOX_FUSION_TEMPLATE")
    project = os.getenv("SANDBOX_FUSION_PROJECT")
    region = os.getenv("SANDBOX_FUSION_REGION")

    return SandboxFusionConfig(
        api_key=api_key,
        template=template,
        endpoint=endpoint,
        project=project,
        region=region,
    )

