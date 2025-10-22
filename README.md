# Coding Agent Assignment

This is a programming assignment designed to help students learn about building AI agents. Students will implement an agent that can solve coding problems by interacting with a language model (LLM).

## Overview

In this assignment, you will build a coding agent that:
1. Receives coding problems as natural language questions
2. Utilizes LLM and tools to generate Python code solutions
3. Returns valid Python code that passes test cases

The agent is exposed through a FastAPI server with a standardized interface for online judge evaluation.

## Project Structure
```
coding/
├── src/
│   └── coding_agent/
│       ├── agent.py          # YOUR TASK: Implement the agent logic here
│       ├── llm.py            # LLM wrapper with cost tracking
│       ├── server.py         # DO NOT MODIFY: FastAPI server for evaluation
│       └── tools/
│           └── code_executor.py  # Tool for executing code in sandbox
│
├── examples/                 # Test examples with questions and tests
│   ├── Algorithm_20713_I/
│   │   ├── question.txt      # Problem description
│   │   ├── test.py           # Test cases
│   │   ├── solution.py       # Reference solution
│   │   └── metadata.json     # Example metadata
│   └── ...                   # (More example folders)
│
├── evaluate.py               # Evaluation script
└── pyproject.toml            # Project dependencies
```

### What You Need to Do

- **Implement the `run_agent` function in `src/coding_agent/agent.py`**
- Feel free to add file/classes/functions as needed within the `coding_agent` package.
- Feel free to add any dependencies use `uv`.
- Feel free to add tools in `coding_agent/tools/` if needed.
- Use the provided LLM interface and code execution tool to build your agent.

### What You Cannot Modify

**DO NOT modify `src/coding_agent/server.py`**

The online judge system expects a specific API interface:
- Endpoint: `POST /run_agent`
- Request body: `{"question": str, "model": str, "max_cost": float}`
- Response: `{"code": str, "logs": list}`

Any changes to `server.py` will cause evaluation to fail.

### Available Resources

You have access to:

1. **LLM Interface** (`coding_agent.llm.LLM`):
   ```python
   llm = LLM(model="openai/gpt-5-mini", max_cost=1.0)
   response = await llm.acompletion(messages=[
       {"role": "system", "content": "You are a Python expert"},
       {"role": "user", "content": "Write a function to add two numbers"}
   ])
   ```

2. **Code Executor** (`coding_agent.tools.code_executor.execute_code`):
   ```python
   from coding_agent.tools.code_executor import execute_code

   result = await execute_code(
       code="print('hello')",
       language="python",
       timeout=60
   )
   print(result.run_result.stdout)  # "hello"
   print(result.run_result.return_code)  # 0 for success
   ```

3. **Cost Tracking**: The LLM automatically tracks costs and raises `CostExceeded` when the budget is exhausted

## Testing Your Agent

You can test individual examples manually:
```bash
# Send a request to your local server
curl -X POST http://localhost:8888/run_agent \
  -H "Content-Type: application/json" \
  -d '{
    "question": "Write a function that adds two numbers",
    "model": "openai/gpt-4o-mini",
    "max_cost": 0.5
  }'
```

## Evaluation with Public Examples

### Running the Evaluation Script

The `evaluate.py` script will:
1. Start the server in the background
2. Load all examples from the `examples/` directory
3. Send each question to your agent
4. Test the returned code against test cases
5. Generate a summary report

Run evaluation:
```bash
uv run python evaluate.py
```

## Grading Criteria

Your agent will be evaluated on:
1. **Correctness**: Percentage of test cases passed (primary metric)
2. **Cost Efficiency**: Ability to solve problems within budget constraints
3. **Code Quality**: Clean, maintainable implementation in `agent.py`
4. **Error Handling**: Graceful handling of edge cases and failures

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/) - For LLM integration
- [FastAPI Documentation](https://fastapi.tiangolo.com/) - For understanding the server
- [Sandbox Fusion](https://github.com/your-org/sandbox-fusion) - For code execution