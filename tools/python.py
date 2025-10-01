"""SandboxFusion-powered Python interpreter wrapper."""

from __future__ import annotations

import os
from typing import Tuple

try:  # pragma: no cover - optional dependency, required for real isolation
    from sandbox_fusion import run_code, RunCodeRequest, set_sandbox_endpoint  # type: ignore
    from sandbox_fusion.models import CommandRunStatus, RunStatus  # type: ignore
except Exception as exc:  # pragma: no cover - provide informative error later
    raise RuntimeError(
        "Failed to import sandbox_fusion SDK. Install `sandbox-fusion` in the current environment."
    ) from exc

from template_coding.config.env import load_sandbox_fusion_config


def _format_run_output(response) -> Tuple[str, bool]:
    if response.run_result is None and response.compile_result is None:
        return (response.message or "Sandbox returned no output.", response.status == RunStatus.Success)

    parts = []
    success = response.status == RunStatus.Success

    if response.compile_result is not None:
        compile_result = response.compile_result
        if compile_result.stdout:
            parts.append(compile_result.stdout.strip())
        if compile_result.stderr:
            parts.append(compile_result.stderr.strip())
        if compile_result.return_code not in (None, 0):
            success = False

    if response.run_result is not None:
        run_result = response.run_result
        if run_result.stdout:
            parts.append(run_result.stdout.strip())
        if run_result.stderr:
            parts.append(run_result.stderr.strip())
        if run_result.return_code not in (None, 0):
            success = False
        if run_result.status == CommandRunStatus.TimeLimitExceeded:
            success = False

    output = "\n".join(filter(None, parts)) or response.message or "Python succeeded with no output."
    return (output, success)


def sandbox_fusion_execute(code: str, timeout: int = 30) -> Tuple[str, bool]:
    """Execute ``code`` using the SandboxFusion Python SDK."""

    try:
        config = load_sandbox_fusion_config()
    except RuntimeError as exc:
        return (str(exc), False)

    if config.endpoint:
        set_sandbox_endpoint(config.endpoint)

    if config.api_key:
        os.environ.setdefault("SANDBOX_API_KEY", config.api_key)

    try:
        response = run_code(
            RunCodeRequest(
                code=code,
                language="python",
                run_timeout=float(timeout),
                compile_timeout=float(min(timeout, 10)),
            )
        )
        if response.status == RunStatus.Failed:
            return (response.message or "Sandbox run failed.", False)
    except Exception as exc:  # pragma: no cover - surface sandbox errors
        return (f"SandboxFusion exception: {exc}", False)

    return _format_run_output(response)
