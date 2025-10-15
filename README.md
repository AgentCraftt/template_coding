# ReAct Baseline (Server + Container)

Minimal ReAct-style coding agent with a FastAPI server. The same source files can run either as a Python package (`react_baseline.*`) or flattened under `/workspace` inside a container.

## Layout

```
template_coding/
├── react_baseline/
   ├── agent.py           # ReAct loop (Python-only tool)
   ├── server.py          # FastAPI server (uvicorn entry: server:app or react_baseline.server:app)
   ├── llm.py             # LiteLLM wrapper (OpenAI/ChatAnywhere)
   └── tools/
       └── python_exec.py # In-process Python executor
```

## Build container for Volcano Engine

Build with the specified base image and place source files directly under `/workspace`:

```
docker build -f template_coding/Dockerfile.volc -t <REGISTRY>/<NAMESPACE>/react-baseline:<TAG> .
# If on Apple Silicon and base is amd64:
docker build --platform=linux/amd64 -f template_coding/Dockerfile.volc -t <REGISTRY>/<NAMESPACE>/react-baseline:<TAG> .
```

Run locally:

```
docker run --rm -it -p 7777:7777 <REGISTRY>/<NAMESPACE>/react-baseline:<TAG>
# On Apple Silicon if built for amd64:
docker run --rm -it --platform=linux/amd64 -p 7777:7777 <REGISTRY>/<NAMESPACE>/react-baseline:<TAG>
```

The container exposes `POST /run` on port 7777 and accepts the same JSON as above.

Here is an example of trying whether it works or not:
```
curl -X POST http://localhost:7777/run   -H "Content-Type: application/json"   -d @- <<'EOF'
{
  "model": "gpt-4o-mini",
  "question": "Complete the following code, and return the complete code:\nfrom typing import List\n\ndef has_close_elements(numbers: List[float], threshold: float) -> bool:\n\"\"\" Check if in given list of numbers, are any two numbers closer to each other than\ngiven threshold.\n>>> has_close_elements([1.0, 2.0, 3.0], 0.5)\nFalse\n>>> has_close_elements([1.0, 2.8, 3.0, 4.0, 5.0, 2.0], 0.3)\nTrue\n\"\"\"\n"
}
EOF
```
