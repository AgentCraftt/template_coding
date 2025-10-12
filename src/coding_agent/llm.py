import os
import asyncio
from litellm import acompletion
from typing import Optional, Dict, Any

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
        Returns the model's reply or '<finish>' if cost limit exceeded.
        """
        async with self._lock:
            if self.total_cost >= self.max_cost:
                return "<finish>"

        try:
            print(self.model)
            print(messages)
            response = await acompletion(
                model=self.model,
                messages=messages,
                **kwargs
            )
            print(response)
            # LiteLLM attaches cost info if known
            cost = getattr(response, "_hidden_params", {}).get("response_cost", 0.0) or 0.0

            if await self._update_cost(cost):
                return "<finish>"

            # Handle different response formats
            if hasattr(response, 'choices') and response.choices:
                return response.choices[0].message.content
            elif hasattr(response, 'content'):
                return response.content
            else:
                return str(response)

        except Exception as e:
            return f"<error: {e}>"

    async def reset_cost(self):
        """Reset the cost counter."""
        async with self._lock:
            self.total_cost = 0.0