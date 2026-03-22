---
name: pydanticai-docs
description: Use this skill whenever the user is working with the Pydantic AI framework — including building AI agents, defining structured outputs with Pydantic models, wiring up tools/function calling, configuring model providers (OpenAI, Anthropic, Gemini, etc.), managing dependencies via agent context, handling streaming responses, or debugging agent runs. Trigger this skill even for adjacent tasks like "how do I make my agent return JSON", "set up a multi-step agent", "add a tool to my agent", or "validate LLM output with Pydantic" — any time Pydantic AI is mentioned or implied as the target framework.
license: Apache-2.0
metadata:
  author: Douglas Trajano
  version: "1.0"
---

# Pydantic AI Documentation Skill

## What is Pydantic AI?

Pydantic AI is a production-grade Python agent framework for building type-safe, dependency-injected Generative AI applications. It supports multiple LLM providers, structured outputs via Pydantic models, and composable multi-agent patterns.

Doc: <https://ai.pydantic.dev/index.md>

---

## Core Concepts

### 1. Agent Instantiation

```python
from pydantic_ai import Agent

agent = Agent(
    'openai:gpt-4o',          # model string: provider:model-name
    system_prompt='Be helpful.',
)
result = agent.run_sync('What is the capital of France?')
print(result.output)
```

For full constructor parameters, run methods, and streaming: load `references/AGENT.md`.

### 2. Function Tools (`@agent.tool`)

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o', deps_type=str)

@agent.tool
def get_user_name(ctx: RunContext[str]) -> str:
    """Return the current user's name."""
    return ctx.deps

result = agent.run_sync('What is my name?', deps='Alice')
```

Use `@agent.tool_plain` when you don't need `RunContext`. For tool registration, return types, and retries: load `references/FUNCTION_TOOLS.md`.

### 3. Dependency Injection (`RunContext`)

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    api_key: str
    user_id: int

agent = Agent('openai:gpt-4o', deps_type=MyDeps)

@agent.tool
async def fetch_data(ctx: RunContext[MyDeps]) -> str:
    return f'User {ctx.deps.user_id}'
```

For `RunContext` fields, injection into system prompts and output validators: load `references/DEPENDENCIES.md`.

### 4. Structured Output

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class CityInfo(BaseModel):
    city: str
    country: str

agent = Agent('openai:gpt-4o', output_type=CityInfo)
result = agent.run_sync('Where were the 2012 Olympics held?')
print(result.output)  # CityInfo(city='London', country='United Kingdom')
```

For union types, plain scalars, `output_validator`, and partial validation: load `references/OUTPUT.md`.

---

## Additional Topics

> For these topics, load the named reference file or follow the doc link — no implementation code is provided here.

| Topic | Reference file | Doc link |
|---|---|---|
| Message history / multi-turn conversations | `references/MESSAGES.md` | <https://ai.pydantic.dev/message-history/index.md> |
| Model / provider setup (all providers) | `references/MODELS.md` | <https://ai.pydantic.dev/models/overview/index.md> |
| Toolsets (`FunctionToolset`, composition) | `references/TOOLS_AND_TOOLSETS.md` | <https://ai.pydantic.dev/toolsets/index.md> |
| MCP server integration | `references/MCP.md` | <https://ai.pydantic.dev/mcp/client/index.md> |
| Multi-agent applications | doc link only | <https://ai.pydantic.dev/multi-agent-applications/index.md> |
| Graphs (pydantic-graph) | doc link only | <https://ai.pydantic.dev/graph/index.md> |
| Evals (pydantic-evals) | doc link only | <https://ai.pydantic.dev/evals/index.md> |
| Durable execution | doc link only | <https://ai.pydantic.dev/durable_execution/overview/index.md> |
| Retries | doc link only | <https://ai.pydantic.dev/retries/index.md> |
| Testing (`TestModel`, `override`) | doc link only | <https://ai.pydantic.dev/testing/index.md> |
| Logfire integration | doc link only | <https://ai.pydantic.dev/logfire/index.md> |
| Builtin tools | doc link only | <https://ai.pydantic.dev/builtin-tools/index.md> |
| Streaming | doc link only | <https://ai.pydantic.dev/agent/index.md> |

---

## Agent Behavior Rules

1. **Default to this file** — answer from core concepts first; load only the specific `references/<CONCEPT>.md` relevant to the user's question when more depth is needed.
2. **Never fabricate API details** — always end with "For details, see: \<URL\>" using a link from the official index above.
3. **No implementation code for non-core topics** — return a doc link only for topics listed in the Additional Topics table.
4. **Prefer specificity** — route to the most specific page (e.g., `models/anthropic/index.md`) when the user's question targets a specific provider, not the overview.
5. **Out of scope** — do not debug user code passively, do not generate full production agent implementations, do not answer questions unrelated to the Pydantic AI ecosystem.
