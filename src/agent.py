"""ReAct agent implementation constrained to a Python execution tool."""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Tuple, Optional

import re
import textwrap

from . import llm
from .tools.code_executor import sandbox_fusion_execute


class CodingAgent: