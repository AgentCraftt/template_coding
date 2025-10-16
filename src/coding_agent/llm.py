import os
import asyncio
from litellm import acompletion
from typing import Dict, Any


class CostExeeeded(Exception):
    pass


class LLM:
    def __init__(self, model: str = "openai/gpt-4o-mini", max_cost: float = 1):
        self.model = model
        self.max_cost = max_cost
        self.cost = 0.0
        self._lock = asyncio.Lock()

    async def _update_cost(self, cost: float) -> bool:
        """Safely update cumulative cost; return True if exceeds limit."""
        async with self._lock:
            self.cost += cost

    async def _exceeds_limit(self) -> bool:
        async with self._lock:
            return self.cost >= self.max_cost

    async def acompletion(self, messages: list[Dict[str, str]], **kwargs: Any) -> str:
        """
        Send an async chat request.
        Returns the model's reply or '<finish>' if cost limit exceeded.
        """
        if await self._exceeds_limit():
            raise CostExeeeded("Cost limit exceeded")

        try:
            response = await acompletion(model=self.model, messages=messages, **kwargs)
            # LiteLLM attaches cost info if known
            cost = (
                getattr(response, "_hidden_params", {}).get("response_cost", 0.0) or 0.0
            )
            await self._update_cost(cost)
            return response
        except Exception as e:
            raise e

    async def reset_cost(self):
        """Reset the cost counter."""
        async with self._lock:
            self.cost = 0.0
