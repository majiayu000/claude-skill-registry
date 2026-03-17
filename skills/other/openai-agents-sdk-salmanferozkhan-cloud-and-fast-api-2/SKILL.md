---
name: openai-agents-sdk
description: Expert guidance for building multi-agent AI applications using the OpenAI Agents SDK for Python. Use when (1) creating agents with handoffs, tools, guardrails, or sessions, (2) implementing structured outputs with Pydantic models, (3) building agentic workflows, (4) debugging and tracing agent execution, (5) working with provider-agnostic LLM applications (OpenAI, Anthropic, LiteLLM), or (6) implementing customer support, legal research, financial analysis, or autonomous task completion systems.
---

# OpenAI Agents SDK

A lightweight, powerful framework for building multi-agent AI workflows in Python.

## Installation

```bash
pip install openai-agents

# With LiteLLM for multi-provider support
pip install openai-agents[litellm]
```

Set your API key:
```bash
export OPENAI_API_KEY=your-key
```

## Quick Start

```python
from agents import Agent, Runner

agent = Agent(
    name="Assistant",
    instructions="You are a helpful assistant",
)

result = Runner.run_sync(agent, "Hello!")
print(result.final_output)
```

## Core Primitives

| Primitive | Purpose |
|-----------|---------|
| **Agent** | LLM with instructions and tools |
| **Tools** | Python functions agents can call |
| **Handoffs** | Delegate to specialized agents |
| **Guardrails** | Validate inputs/outputs |
| **Sessions** | Maintain conversation history |
| **Runner** | Execute agent workflows |

## Agent with Tools

```python
from agents import Agent, Runner, function_tool

@function_tool
def get_weather(city: str) -> str:
    """Get weather for a city."""
    return f"Weather in {city}: Sunny, 72F"

agent = Agent(
    name="Weather Bot",
    instructions="Help with weather questions",
    tools=[get_weather],
)

result = Runner.run_sync(agent, "What's the weather in NYC?")
```

## Structured Output

```python
from pydantic import BaseModel
from agents import Agent, Runner

class WeatherReport(BaseModel):
    city: str
    temperature: float
    conditions: str

agent = Agent(
    name="Weather Reporter",
    instructions="Extract weather data",
    output_type=WeatherReport,
)

result = Runner.run_sync(agent, "NYC is sunny and 72 degrees")
report: WeatherReport = result.final_output
```

## Multi-Agent Handoffs

```python
from agents import Agent

billing = Agent(name="Billing", instructions="Handle billing issues")
technical = Agent(name="Technical", instructions="Handle tech issues")

triage = Agent(
    name="Triage",
    instructions="Route to billing or technical support",
    handoffs=[billing, technical],
)
```

## Sessions (Conversation Memory)

```python
from agents import Agent, Runner
from agents.extensions.session import SQLiteSession

session = SQLiteSession("user_123", "chats.db")
agent = Agent(name="Assistant", instructions="Be helpful")

# Remembers across calls
result = await Runner.run(agent, "My name is Alice", session=session)
result = await Runner.run(agent, "What's my name?", session=session)
```

## Custom OpenAI-Compatible Providers

Use `OpenAIChatCompletionsModel` for custom OpenAI-compatible APIs (Google Gemini, local models, etc.):

```python
import os
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel, set_tracing_disabled

# Disable tracing if not needed
set_tracing_disabled(True)

# Configure client for Google's Generative Language API
client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)

# Create model with custom client
llm_model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",
    openai_client=client,
)

# Use in agent
agent = Agent(
    name="Gemini Agent",
    instructions="You are a helpful assistant",
    model=llm_model,
    tools=[...],
)
```

## Multi-Provider (LiteLLM)

Alternative approach using LiteLLM for multi-provider support:

```python
from agents import Agent

# Anthropic Claude
claude = Agent(
    name="Claude",
    instructions="Be helpful",
    model="litellm/anthropic/claude-sonnet-4-20250514",
)

# Google Gemini via LiteLLM
gemini = Agent(
    name="Gemini",
    instructions="Be helpful",
    model="litellm/gemini/gemini-2.5-flash",
)
```

## Fallback Model Pattern

Create a custom model that falls back to a secondary provider when the primary API is exhausted:

```python
import os
from collections.abc import AsyncIterator

from openai import AsyncOpenAI, RateLimitError, APIStatusError
from agents import Agent, OpenAIChatCompletionsModel, ModelSettings
from agents.models.interface import Model, ModelTracing
from agents.agent_output import AgentOutputSchemaBase
from agents.handoffs import Handoff
from agents.items import ModelResponse, TResponseInputItem, TResponseStreamEvent
from agents.tool import Tool


class FallbackModel(Model):
    """Model wrapper that falls back to secondary provider on rate limit errors."""

    def __init__(self, primary_model: Model, fallback_model: Model):
        self.primary_model = primary_model
        self.fallback_model = fallback_model
        self._use_fallback = False

    async def get_response(
        self,
        system_instructions: str | None,
        input: str | list[TResponseInputItem],
        model_settings: ModelSettings,
        tools: list[Tool],
        output_schema: AgentOutputSchemaBase | None,
        handoffs: list[Handoff],
        tracing: ModelTracing,
        *,
        previous_response_id: str | None,
        conversation_id: str | None,
        prompt=None,
    ) -> ModelResponse:
        if self._use_fallback and self.fallback_model:
            return await self.fallback_model.get_response(
                system_instructions, input, model_settings, tools,
                output_schema, handoffs, tracing,
                previous_response_id=previous_response_id,
                conversation_id=conversation_id,
                prompt=prompt,
            )

        try:
            return await self.primary_model.get_response(
                system_instructions, input, model_settings, tools,
                output_schema, handoffs, tracing,
                previous_response_id=previous_response_id,
                conversation_id=conversation_id,
                prompt=prompt,
            )
        except (RateLimitError, APIStatusError) as e:
            is_quota_error = (
                isinstance(e, RateLimitError) or
                (isinstance(e, APIStatusError) and e.status_code in (429, 503)) or
                "quota" in str(e).lower()
            )
            if is_quota_error and self.fallback_model:
                print(f"[Fallback] Primary API exhausted, switching to fallback")
                self._use_fallback = True
                return await self.fallback_model.get_response(
                    system_instructions, input, model_settings, tools,
                    output_schema, handoffs, tracing,
                    previous_response_id=previous_response_id,
                    conversation_id=conversation_id,
                    prompt=prompt,
                )
            raise

    def stream_response(self, *args, **kwargs) -> AsyncIterator[TResponseStreamEvent]:
        # Implement similar fallback logic for streaming
        pass


# Usage: Gemini primary, DeepSeek fallback
gemini_client = AsyncOpenAI(
    api_key=os.getenv("GEMINI_API_KEY"),
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
)
deepseek_client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

gemini_model = OpenAIChatCompletionsModel(model="gemini-2.5-flash", openai_client=gemini_client)
deepseek_model = OpenAIChatCompletionsModel(model="deepseek-chat", openai_client=deepseek_client)

fallback_model = FallbackModel(gemini_model, deepseek_model)

agent = Agent(
    name="MyAgent",
    instructions="You are a helpful assistant",
    model=fallback_model,
    tools=[...],
)
```

## DeepSeek Integration

DeepSeek offers two main models via OpenAI-compatible API:

| Model | Use Case | Tool Support |
|-------|----------|--------------|
| `deepseek-chat` | General chat, tool calling | Yes |
| `deepseek-reasoner` | Complex reasoning (requires `reasoning_content` field) | Limited |

**Important**: Use `deepseek-chat` for agents with tools. The `deepseek-reasoner` model requires special handling for tool calls.

```python
from openai import AsyncOpenAI
from agents import Agent, OpenAIChatCompletionsModel

deepseek_client = AsyncOpenAI(
    api_key=os.getenv("DEEPSEEK_API_KEY"),
    base_url="https://api.deepseek.com",
)

# Use deepseek-chat for tool-calling agents
model = OpenAIChatCompletionsModel(
    model="deepseek-chat",  # NOT deepseek-reasoner for tool calls
    openai_client=deepseek_client,
)

agent = Agent(
    name="DeepSeek Agent",
    instructions="You are helpful",
    model=model,
    tools=[my_tool],
)
```

## Reference Documentation

For detailed guidance on specific topics:

- **[agents.md](references/agents.md)** - Agent creation, dynamic instructions, context injection, lifecycle hooks
- **[tools.md](references/tools.md)** - Function tools, hosted tools, Pydantic validation, error handling
- **[handoffs.md](references/handoffs.md)** - Multi-agent delegation, input filters, conditional handoffs
- **[guardrails.md](references/guardrails.md)** - Input/output validation, tripwires, execution modes
- **[sessions.md](references/sessions.md)** - SQLite, SQLAlchemy, encrypted sessions, memory operations
- **[running.md](references/running.md)** - Runner class, streaming, configuration, exception handling
- **[models.md](references/models.md)** - Model settings, LiteLLM integration, multi-provider workflows
- **[patterns.md](references/patterns.md)** - Customer support, research assistant, RAG, human-in-the-loop

## Common Patterns

### Customer Support

```python
from agents import Agent
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX

triage = Agent(
    name="Triage",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX}
Route customers to billing, technical, or sales.""",
    handoffs=[billing_agent, tech_agent, sales_agent],
)
```

### Input Validation

```python
from agents import Agent, input_guardrail, GuardrailFunctionOutput

@input_guardrail
async def block_harmful(ctx, agent, input_text):
    is_harmful = check_content(input_text)
    return GuardrailFunctionOutput(
        output_info={"harmful": is_harmful},
        tripwire_triggered=is_harmful,
    )

agent = Agent(
    name="Safe Agent",
    instructions="Be helpful",
    input_guardrails=[block_harmful],
)
```

### Streaming Responses

```python
from agents import Agent, Runner

async def stream():
    result = await Runner.run_streamed(agent, "Write a story")
    async for event in result.stream_events():
        if event.type == "text_delta":
            print(event.delta, end="")
```

## Key Classes

| Class | Import | Purpose |
|-------|--------|---------|
| `Agent` | `from agents import Agent` | Create agents |
| `Runner` | `from agents import Runner` | Execute agents |
| `function_tool` | `from agents import function_tool` | Decorator for tools |
| `handoff` | `from agents import handoff` | Custom handoff config |
| `input_guardrail` | `from agents import input_guardrail` | Input validation |
| `output_guardrail` | `from agents import output_guardrail` | Output validation |
| `SQLiteSession` | `from agents.extensions.session import SQLiteSession` | Conversation memory |
| `RunConfig` | `from agents import RunConfig` | Execution settings |
| `OpenAIChatCompletionsModel` | `from agents import OpenAIChatCompletionsModel` | Custom OpenAI-compatible models |
| `set_tracing_disabled` | `from agents import set_tracing_disabled` | Disable tracing |
| `Model` | `from agents.models.interface import Model` | Base class for custom models |
| `ModelTracing` | `from agents.models.interface import ModelTracing` | Tracing configuration enum |
| `ModelResponse` | `from agents.items import ModelResponse` | Model response type |
| `TResponseInputItem` | `from agents.items import TResponseInputItem` | Input item type |
| `TResponseStreamEvent` | `from agents.items import TResponseStreamEvent` | Stream event type |
