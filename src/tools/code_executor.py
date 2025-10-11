"""Container-friendly Python executor wrapper.

This replaces the SandboxFusion-based executor with a simple in-process
interpreter suitable for running inside an isolated container.
"""

from __future__ import annotations

import io
from contextlib import redirect_stdout, redirect_stderr
from typing import Tuple


def sandbox_fusion_execute(code: str, timeout: int = 30) -> Tuple[str, bool]: