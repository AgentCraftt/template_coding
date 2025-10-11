"""Container-friendly Python executor wrapper.

This replaces the SandboxFusion-based executor with a simple in-process
interpreter suitable for running inside an isolated container.
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Tuple


def sandbox_fusion_execute(code: str, timeout: int = 30) -> Tuple[str, bool]:
    """Execute ``code`` in-process and capture stdout/stderr.

    Parameters
    ----------
    code: str
        Python code to execute. Any prints will be captured as output.
    timeout: int
        Ignored in this simplified implementation.
    """

    stdout = io.StringIO()
    stderr = io.StringIO()
    local_ns: dict = {}
    global_ns: dict = {"__name__": "__main__"}

    try:
        with redirect_stdout(stdout), redirect_stderr(stderr):
            exec(compile(code, filename="<agent>", mode="exec"), global_ns, local_ns)
        out = "\n".join(filter(None, [stdout.getvalue().strip(), stderr.getvalue().strip()]))
        return (out or "Python succeeded with no output.", True)
    except Exception as exc:  # surface runtime errors back to the agent
        err = stderr.getvalue().strip()
        out = stdout.getvalue().strip()
        msg_parts = [part for part in [out, err, f"Exception: {exc}"] if part]
        return ("\n".join(msg_parts) or f"Exception: {exc}", False)
