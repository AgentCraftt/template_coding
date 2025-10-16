import os
import asyncio
from litellm import acompletion
from typing import Optional, Dict, Any

class CostExceeded(Exception):
    """Raised when the cost limit is exceeded."""
    def __init__(self, message, current_cost=None, max_cost=None):
        super().__init__(message)
        self.current_cost = current_cost
        self.max_cost = max_cost

    def __str__(self):
        base = super().__str__()
        return f"{base} (current: {self.current_cost}, limit: {self.max_cost})"

class LLM:
    def __init__(self, model: str = "openai/gpt-4o-mini"):
        self.model = model
        self.max_cost = float(os.getenv("MAX_COST", "0.5"))
        self.total_cost = 0.0
        self._lock = asyncio.Lock()

    async def _update_cost(self, cost: float) -> bool:
        """Safely update cumulative cost; return True if exceeds limit."""
        async with self._lock:
            self.total_cost += cost
            return self.total_cost > self.max_cost

    async def acompletion(
        self,
        messages: list[Dict[str, str]],
        **kwargs: Any
    ) -> str:
        """
        Send an async chat request.
        Returns the model's reply or raise Error if cost limit exceeded.
        """
        if self.total_cost >= self.max_cost:
            raise CostExceeded("Cost limit exceeded", current_cost=self.total_cost, max_cost=self.max_cost)

        try:
            response = await acompletion(
                model=self.model,
                messages=messages,
                **kwargs
            )

            # LiteLLM attaches cost info if known
            cost = getattr(response, "_hidden_params", {}).get("response_cost", 0.0) or 0.0

            if await self._update_cost(cost):
                raise CostExceeded("Cost limit exceeded", current_cost=self.total_cost, max_cost=self.max_cost)

            # Handle different response formats
            if hasattr(response, 'choices') and response.choices:
                return response.choices[0].message.content
            elif hasattr(response, 'content'):
                return response.content
            else:
                return response

        except Exception as e:
            raise e

    async def reset_cost(self):
        """Reset the cost counter."""
        async with self._lock:
            self.total_cost = 0.0