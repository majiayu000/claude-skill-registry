---
name: pydantic-ai-agent-creation
description: Create PydanticAI agents with type-safe dependencies, structured outputs, and proper configuration. Use when building AI agents, creating chat systems, or integrating LLMs with Pydantic validation.
---

# Creating PydanticAI Agents

## Quick Start

```python
from pydantic_ai import Agent

# Minimal agent (text output)
agent = Agent('openai:gpt-4o')
result = agent.run_sync('Hello!')
print(result.output)  # str
```

## Model Selection

Model strings follow `provider:model-name` format:

```python
# OpenAI
agent = Agent('openai:gpt-4o')
agent = Agent('openai:gpt-4o-mini')

# Anthropic
agent = Agent('anthropic:claude-sonnet-4-5')
agent = Agent('anthropic:claude-haiku-4-5')

# Google
agent = Agent('google-gla:gemini-2.0-flash')
agent = Agent('google-vertex:gemini-2.0-flash')

# Others: groq:, mistral:, cohere:, bedrock:, etc.
```

## Structured Outputs

Use Pydantic models for validated, typed responses:

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class CityInfo(BaseModel):
    city: str
    country: str
    population: int

agent = Agent('openai:gpt-4o', output_type=CityInfo)
result = agent.run_sync('Tell me about Paris')
print(result.output.city)  # "Paris"
print(result.output.population)  # int, validated
```

## Agent Configuration

```python
agent = Agent(
    'openai:gpt-4o',
    output_type=MyOutput,           # Structured output type
    deps_type=MyDeps,               # Dependency injection type
    instructions='You are helpful.',  # Static instructions
    retries=2,                      # Retry attempts for validation
    name='my-agent',                # For logging/tracing
    model_settings=ModelSettings(   # Provider settings
        temperature=0.7,
        max_tokens=1000
    ),
    end_strategy='early',           # How to handle tool calls with results
)
```

## Running Agents

Three execution methods:

```python
# Async (preferred)
result = await agent.run('prompt', deps=my_deps)

# Sync (convenience)
result = agent.run_sync('prompt', deps=my_deps)

# Streaming
async with agent.run_stream('prompt') as response:
    async for chunk in response.stream_output():
        print(chunk, end='')
```

## Instructions vs System Prompts

```python
# Instructions: Concatenated, for agent behavior
agent = Agent(
    'openai:gpt-4o',
    instructions='You are a helpful assistant. Be concise.'
)

# Dynamic instructions via decorator
@agent.instructions
def add_context(ctx: RunContext[MyDeps]) -> str:
    return f"User ID: {ctx.deps.user_id}"

# System prompts: Static, for model context
agent = Agent(
    'openai:gpt-4o',
    system_prompt=['You are an expert.', 'Always cite sources.']
)
```

## Common Patterns

### Parameterized Agent (Type-Safe)

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class Deps:
    api_key: str
    user_id: int

agent: Agent[Deps, str] = Agent(
    'openai:gpt-4o',
    deps_type=Deps,
)

# deps is now required and type-checked
result = agent.run_sync('Hello', deps=Deps(api_key='...', user_id=123))
```

### No Dependencies (Satisfy Type Checker)

```python
# Option 1: Explicit type annotation
agent: Agent[None, str] = Agent('openai:gpt-4o')

# Option 2: Pass deps=None
result = agent.run_sync('Hello', deps=None)
```

## Decision Framework

| Scenario | Configuration |
|----------|--------------|
| Simple text responses | `Agent(model)` |
| Structured data extraction | `Agent(model, output_type=MyModel)` |
| Need external services | Add `deps_type=MyDeps` |
| Validation retries needed | Increase `retries=3` |
| Debugging/monitoring | Set `instrument=True` |
