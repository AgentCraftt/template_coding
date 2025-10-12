import litellm
from typing import List

class LLM:
    def __init__(self, model: str, budget: str, api_key: str, api_base: str = None):
        self.model = model
        self.budget = budget
        self.api_key = api_key
        self.api_base = api_base
        self.cost = 0

    async def completion(self, messages: List = [], *args, **kwargs) -> str:
        if "model" in kwargs:
            kwargs.pop("model")
        if self.cost >= self.budget:
            raise Exception("Budget exceeded")
        response = await litellm.acompletion(
            model=self.model,
            messages=messages,
            api_key=self.api_key,
            api_base=self.api_base,
            *args,
            **kwargs
        )
        completion_cost = litellm.completion_cost(completion_response=response)
        self.cost += completion_cost
        return response