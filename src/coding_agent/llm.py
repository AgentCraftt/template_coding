import asyncio
import tenacity
from litellm import acompletion, ModelResponse, completion_cost
from typing import Dict, Any


class CostExceeded(Exception):
    pass


@tenacity.retry(
    wait=tenacity.wait_exponential(multiplier=1, min=4, max=10),
    stop=tenacity.stop_after_attempt(5),
    retry=tenacity.retry_if_exception_type(CostExceeded),
)
async def acompletion_with_retry(
    model: str, messages: list[Dict[str, str]], **kwargs: Any
) -> ModelResponse:
    """
    Call the LLM asynchronously with retry on CostExceeded.

    Args:
        model: The model name to use.
        messages: List of message dicts with 'role' and 'content'.
        **kwargs: Additional keyword arguments for acompletion.

    Returns:
        ModelResponse: The response from the LLM.
    """
    response = await acompletion(model=model, messages=messages, **kwargs)
    return response


class LLM:
    def __init__(self, model: str = "openai/gpt-4o-mini", max_cost: float = 1):
        self.model = model
        self.max_cost = max_cost
        self.cost = 0.0
        self._logs = []
        self._lock = asyncio.Lock()

    async def _update(
        self, messages: list[Dict[str, str]], response: ModelResponse
    ) -> bool:
        """Safely update cumulative cost."""
        async with self._lock:
            cost = completion_cost(response, messages=messages)
            self.cost += cost
            self._logs.append(
                dict(
                    model=self.model,
                    messages=messages,
                    response=response.to_dict(),
                    response_cost=cost,
                    total_cost=self.cost,
                )
            )

    async def _exceeds_limit(self) -> bool:
        """Return True if cumulative cost exceeds max_cost."""
        async with self._lock:
            return self.cost >= self.max_cost

    async def acompletion(
        self, messages: list[Dict[str, str]], **kwargs: Any
    ) -> ModelResponse:
        """
        Send an async chat request.
        Args:
            messages: List of message dicts with 'role' and 'content'.
            **kwargs: Additional keyword arguments for acompletion, same with litellm.acompletion.
        Returns:
            ModelResponse: The response from the LLM.
        """
        if await self._exceeds_limit():
            raise CostExceeded("Cost limit exceeded")

        response = await acompletion_with_retry(
            model=self.model, messages=messages, **kwargs
        )
        await self._update(messages, response)
        return response

    async def reset_cost(self):
        """Reset the cost counter."""
        async with self._lock:
            self.cost = 0.0
