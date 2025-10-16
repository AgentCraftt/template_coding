import os
import asyncio
from litellm import acompletion, ModelResponse, completion_cost
from typing import Dict, Any


class CostExceeded(Exception):
    pass


class LLM:
    def __init__(self, model: str = "openai/gpt-4o-mini", max_cost: float = 1):
        self.model = model
        self.max_cost = max_cost
        self.cost = 0.0
        self._requests = []
        self._lock = asyncio.Lock()

    async def _update(self, messages: list[Dict[str, str]], response: float) -> bool:
        """Safely update cumulative cost; return True if exceeds limit."""
        async with self._lock:
            cost = completion_cost(self.model, response)
            self.cost += cost
            self._requests.append(
                dict(
                    model=self.model,
                    messages=messages,
                    response=response,
                    cost=cost,
                )
            )

    async def _exceeds_limit(self) -> bool:
        async with self._lock:
            return self.cost >= self.max_cost

    async def acompletion(self, messages: list[Dict[str, str]], **kwargs: Any) -> str:
        """
        Send an async chat request.
        Returns the model's reply or '<finish>' if cost limit exceeded.
        """
        if await self._exceeds_limit():
            raise CostExceeded("Cost limit exceeded")

        try:
            response = await acompletion(model=self.model, messages=messages, **kwargs)
            # LiteLLM attaches cost info if known
            await self._update(messages, response)
            return response
        except Exception as e:
            raise e

    async def reset_cost(self):
        """Reset the cost counter."""
        async with self._lock:
            self.cost = 0.0
