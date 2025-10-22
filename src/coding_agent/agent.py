import re
from coding_agent.llm import LLM


async def run_agent(llm: LLM, question: str) -> str:
    """
    Run the coding agent to generate a solution for the given question.

    Args:
        llm: LLM instance to use for generation with cost control, if exceeded raises CostExceeded
        question: The coding problem description

    Returns:
        Generated response with thoughts and Python code in markdown format
    """
    # Create a prompt for code generation with thinking
    system_prompt = """You are an expert Python programmer.
Given a coding problem, you will:
1. First, share your thoughts and approach to solving the problem
2. Then, provide the Python code wrapped in ```python...``` code blocks

Your response should follow this format:
<thoughts>
Your analysis and approach to solving the problem
</thoughts>

```python
# Your Python code here
```

Make sure your code passes all the tests described in the problem."""

    user_prompt = f"""Please solve the following coding problem:

{question}

Remember to:
1. Share your thoughts in <thoughts>...</thoughts> tags
2. Wrap your code in ```python...``` code blocks"""

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # Call the LLM
    response = await llm.acompletion(messages)
    output = response.choices[0].message.content
    code_pattern = r"```python(.*?)```"
    # get code
    code = re.search(code_pattern, output, re.DOTALL)
    if code:
        return code.group(1).strip()
    else:
        raise ""
