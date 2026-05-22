---

name: pydantic-ai
description: "Build production AI agents with Pydantic AI: type-safe tools, structured output, embeddings, MCP, 30+ model providers, evals, graphs, and observability."
version: "1.51.0"
release_date: "2026-01-30"

# Pydantic AI

Python agent framework for building production-grade GenAI applications with the "FastAPI feeling".

## Quick Navigation

| Topic        | Reference                                     |
| ------------ | --------------------------------------------- |
| Agents       | [agents.md](references/agents.md)             |
| Tools        | [tools.md](references/tools.md)               |
| Models       | [models.md](references/models.md)             |
| Embeddings   | [embeddings.md](references/embeddings.md)     |
| Evals        | [evals.md](references/evals.md)               |
| Integrations | [integrations.md](references/integrations.md) |
| Graphs       | [graphs.md](references/graphs.md)             |
| UI Streams   | [ui.md](references/ui.md)                     |

## When to Use

- Building AI agents with structured output
- Need type-safe, IDE-friendly agent development
- Require dependency injection for tools
- Multi-model support (OpenAI, Anthropic, Gemini, etc.)
- Production observability with Logfire
- Complex workflows with graphs

## Installation

**Requires Python 3.10+**

```bash
# Full install (all model dependencies)
pip install pydantic-ai

# With examples
pip install "pydantic-ai[examples]"
```

### Slim Install

Use `pydantic-ai-slim` for minimal dependencies:

```bash
# Single model
pip install "pydantic-ai-slim[openai]"

# Multiple models
pip install "pydantic-ai-slim[openai,anthropic,logfire]"
```

**Optional Groups:**

| Group                   | Dependency                 |
| ----------------------- | -------------------------- |
| `openai`                | OpenAI models & embeddings |
| `anthropic`             | Anthropic Claude           |
| `google`                | Google Gemini & embeddings |
| `xai`                   | xAI Grok (native SDK)      |
| `groq`                  | Groq models                |
| `mistral`               | Mistral models             |
| `bedrock`               | AWS Bedrock                |
| `vertexai`              | Google Vertex AI           |
| `cohere`                | Cohere models & embeddings |
| `huggingface`           | Hugging Face Inference     |
| `voyageai`              | VoyageAI embeddings        |
| `sentence-transformers` | Local embeddings           |
| `logfire`               | Pydantic Logfire           |
| `evals`                 | Pydantic Evals             |
| `mcp`                   | MCP protocol               |
| `fastmcp`               | FastMCP                    |
| `a2a`                   | Agent-to-Agent             |
| `tavily`                | Tavily search              |
| `duckduckgo`            | DuckDuckGo search          |
| `exa`                   | Exa neural search          |
| `cli`                   | CLI tools                  |
| `dbos`                  | DBOS durable execution     |
| `prefect`               | Prefect durable execution  |

## Quick Start

### Basic Agent

```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-4o',
    instructions='Be concise, reply with one sentence.'
)

result = agent.run_sync('Where does "hello world" come from?')
print(result.output)
```

### With Structured Output

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class CityInfo(BaseModel):
    name: str
    country: str
    population: int

agent = Agent('openai:gpt-4o', output_type=CityInfo)
result = agent.run_sync('Tell me about Paris')
print(result.output)  # CityInfo(name='Paris', country='France', population=2161000)
```

### With Tools and Dependencies

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class Deps:
    user_id: int

agent = Agent('openai:gpt-4o', deps_type=Deps)

@agent.tool
async def get_user_name(ctx: RunContext[Deps]) -> str:
    """Get the current user's name."""
    return f"User #{ctx.deps.user_id}"

result = agent.run_sync('What is my name?', deps=Deps(user_id=123))
```

## Key Features

| Feature              | Description                     |
| -------------------- | ------------------------------- |
| Type-safe            | Full IDE support, type checking |
| Model-agnostic       | 30+ providers supported         |
| Dependency Injection | Pass context to tools           |
| Structured Output    | Pydantic model validation       |
| Embeddings           | Multi-provider vector support   |
| Logfire Integration  | Built-in observability          |
| MCP Support          | External tools and data         |
| Evals                | Systematic testing              |
| Graphs               | Complex workflow support        |

## Supported Models

| Provider  | Models                   |
| --------- | ------------------------ |
| OpenAI    | GPT-4o, GPT-4, o1, o3    |
| Anthropic | Claude 4, Claude 3.5     |
| Google    | Gemini 2.0, Gemini 1.5   |
| xAI       | Grok-4 (native SDK)      |
| Groq      | Llama, Mixtral           |
| Mistral   | Mistral Large, Codestral |
| Azure     | Azure OpenAI             |
| Bedrock   | AWS Bedrock + Nova 2.0   |
| SambaNova | SambaNova models         |
| Ollama    | Local models             |

## Best Practices

1. **Use type hints** — enables IDE support and validation
2. **Define output types** — guarantees structured responses
3. **Use dependencies** — inject context into tools
4. **Add tool docstrings** — LLM uses them as descriptions
5. **Enable Logfire** — for production observability
6. **Use `run_sync` for simple cases** — `run` for async
7. **Override deps for testing** — `agent.override(deps=...)`
8. **Set usage limits** — prevent infinite loops with `UsageLimits`

## Prohibitions

- Do not expose API keys in code
- Do not skip output validation in production
- Do not ignore tool errors
- Do not use `run_stream` without handling partial outputs
- Do not forget to close MCP connections (`async with agent`)

## Common Patterns

### Streaming Response

```python
async with agent.run_stream('Query') as response:
    async for text in response.stream_text():
        print(text, end='')
```

### Fallback Models

```python
from pydantic_ai.models.fallback import FallbackModel

fallback = FallbackModel(openai_model, anthropic_model)
agent = Agent(fallback)
```

### MCP Integration

```python
from pydantic_ai.mcp import MCPServerStdio

server = MCPServerStdio('python', args=['mcp_server.py'])
agent = Agent('openai:gpt-4o', toolsets=[server])
```

### Testing with TestModel

```python
from pydantic_ai.models.test import TestModel

agent = Agent(model=TestModel())
result = agent.run_sync('test')  # Deterministic output
```

### Embeddings

```python
from pydantic_ai import Embedder

embedder = Embedder('openai:text-embedding-3-small')

# Embed search query
result = await embedder.embed_query('What is ML?')

# Embed documents for indexing
docs = ['Doc 1', 'Doc 2', 'Doc 3']
result = await embedder.embed_documents(docs)
```

See [embeddings.md](references/embeddings.md) for providers and settings.

### xAI Provider

```python
from pydantic_ai import Agent

agent = Agent('xai:grok-4-1-fast-non-reasoning')
```

See [models.md](references/models.md#xai-grok) for configuration details.

### Exa Neural Search

```python
import os
from pydantic_ai import Agent
from pydantic_ai.common_tools.exa import ExaToolset

api_key = os.getenv('EXA_API_KEY')
toolset = ExaToolset(api_key, num_results=5, include_search=True)
agent = Agent('openai:gpt-4o', toolsets=[toolset])
```

See [tools.md](references/tools.md#exa-neural-search) for all Exa tools.

## Links

- [Documentation](https://ai.pydantic.dev/)
- [Releases](https://github.com/pydantic/pydantic-ai/releases)
- [GitHub](https://github.com/pydantic/pydantic-ai)
- [PyPI](https://pypi.org/project/pydantic-ai/)
