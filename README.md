# Template Coding Agent

This package contains a small-but-extensible layout for experimenting with
ReAct-style agents under strict Python-only tooling.  The goal is to make it
easy to plug in additional benchmarks (e.g. HumanEval) while keeping the
environment setup isolated through [SandboxFusion](https://bytedance.github.io/SandboxFusion/).

## Project structure

```
template_coding/
├── main.py                  # CLI entry point
├── agents/
│   └── react.py             # ReAct implementation (exported via agents.__init__)
├── tools/
│   └── python.py            # SandboxFusion-backed Python interpreter
├── config/
│   └── env.py               # Provider + sandbox configuration helpers
└── README.md
```

Keeping the code organised this way makes it straightforward to add new
agents or tools.  For example, a future benchmark can live under
`template_coding/benchmarks/` and import the `react` agent or swap in another
`tools/*` module.

## Environment setup

Install dependencies (using [uv](https://github.com/astral-sh/uv) in this
example):

```bash
uv sync
```

### Launch a local SandboxFusion server

If you want model-generated Python to execute in an isolated container,
run the official SandboxFusion server image.  The following example mirrors
the configuration from the documentation:

```bash
docker run -it -p 8080:8080 \
  -e MEMORY_LIMIT_MB=1024 \
  -e MAX_CONCURRENT=10 \
  -e DEFAULT_TIMEOUT=30 \
  -e SANDBOX_API_KEY=local-secret \
  volcengine/sandbox-fusion:server-20250609
```

After the container is running, configure the SDK to talk to it:

```bash
export SANDBOX_FUSION_API_KEY="local-secret"
export SANDBOX_FUSION_ENDPOINT="http://localhost:8080"
# optionally export SANDBOX_FUSION_TEMPLATE / PROJECT / REGION
```

If the SandboxFusion credentials are missing the agent will surface a
clear error and skip execution.

### LiteLLM providers

`template_coding.config.env.configure_litellm_provider` wires up
LiteLLM for OpenAI by default.  To use
[ChatAnywhere Midpoint](https://www.chatanywhere.com/) configure:

```bash
export CHATANYWHERE_API_KEY="your-key"
export CHATANYWHERE_API_BASE="https://api.chatanywhere.tech/v1"  # adjust if needed
```

and pass `--provider chatanywhere` on the CLI.  The helper mirrors the
values into `OPENAI_API_KEY` / `OPENAI_API_BASE` so OpenAI-compatible
clients continue to work.

## Running the ReAct agent

```bash
uv run template_coding/main.py "2+3=?" \
  --provider chatanywhere \
  --model gpt-5-mini
```

The CLI prints the final answer and the full LiteLLM message history so you
can inspect observations or debugging information from the sandbox.

## Towards benchmark support

- **HumanEval**: SandboxFusion provides first-class dataset helpers.  Follow
  the instructions at
  <https://bytedance.github.io/SandboxFusion/docs/docs/how-to/use-dataset/humaneval>
  to spin up evaluation jobs.  With the current structure you can add a
  `template_coding/benchmarks/humaneval.py` module that imports
  `template_coding.agents.react.react` and feeds each prompt to the agent
  before sending the generated code to SandboxFusion’s evaluator.
- Additional tools can live under `template_coding/tools/`, while new
  agent strategies fit naturally in `template_coding/agents/`.

Document any benchmark-specific configuration in this README so that the
baseline remains easy to reproduce.

