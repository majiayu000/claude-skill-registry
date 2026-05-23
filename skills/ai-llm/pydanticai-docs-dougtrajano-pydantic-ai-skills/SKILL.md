---
name: pydanticai-docs
description: Use this skill for requests related to Pydantic AI framework - building agents, tools, dependencies, structured outputs, and model integrations.
---

# Pydantic AI Documentation Skill

## Overview

This skill provides guidance for using **Pydantic AI** - a Python agent framework for building production-grade Generative AI applications. Pydantic AI emphasizes type safety, dependency injection, and structured outputs.

## Key Concepts

### Agents

Agents are the primary interface for interacting with LLMs. They contain:

- **Instructions**: System prompts for the LLM
- **Tools**: Functions the LLM can call
- **Output Type**: Structured datatype the LLM must return
- **Dependencies**: Data/services injected into tools and prompts

### Models

Pydantic AI supports multiple LLM providers via model identifiers.

All models that supports tool-calling can be used with pydantic-ai-skills.

### Tools

Two types of tools:

- `@agent.tool`: Receives `RunContext` with dependencies
- `@agent.tool_plain`: Plain function without context

### Toolsets

Collections of tools that can be registered with agents:

- `FunctionToolset`: Group multiple tools
- `MCPServerTool`: Model Context Protocol servers
- Third-party toolsets (ACI.dev, etc.)

## Instructions

### 1. Fetch Full Documentation

For comprehensive information, fetch the complete Pydantic AI documentation: <https://ai.pydantic.dev/llms.txt>

This contains complete documentation including agents, tools, dependencies, models, and API reference.

### 2. Quick Reference

#### Basic Agent Creation

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2')
result = agent.run_sync('What is the capital of France?')
print(result.output)
```

#### Agent with Tools

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-5.2', deps_type=str)

@agent.tool
def get_user_name(ctx: RunContext[str]) -> str:
    """Get the current user's name."""
    return ctx.deps

result = agent.run_sync('What is my name?', deps='Alice')
```

#### Structured Output

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class CityInfo(BaseModel):
    name: str
    country: str
    population: int

agent = Agent('openai:gpt-5.2', output_type=CityInfo)
result = agent.run_sync('Tell me about Paris')
print(result.output)  # CityInfo(name='Paris', country='France', population=...)
```

#### Dependencies

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class MyDeps:
    api_key: str
    user_id: int

agent = Agent('openai:gpt-5.2', deps_type=MyDeps)

@agent.tool
async def fetch_data(ctx: RunContext[MyDeps]) -> str:
    # Access dependencies via ctx.deps
    return f"User {ctx.deps.user_id}"
```

#### Using Toolsets

```python
from pydantic_ai import Agent
from pydantic_ai.toolsets import FunctionToolset

toolset = FunctionToolset()

@toolset.tool
def search(query: str) -> str:
    """Search for information."""
    return f"Results for: {query}"

agent = Agent('openai:gpt-5.2', toolsets=[toolset])
```

#### Async Execution

```python
import asyncio
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2')

async def main():
    result = await agent.run('Hello!')
    print(result.output)

asyncio.run(main())
```

#### Streaming

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-5.2')

async with agent.run_stream('Tell me a story') as response:
    async for text in response.stream():
        print(text, end='', flush=True)
```

### 3. Common Patterns

#### Dynamic Instructions

```python
@agent.instructions
async def add_context(ctx: RunContext[MyDeps]) -> str:
    return f"Current user ID: {ctx.deps.user_id}"
```

#### System Prompts

```python
@agent.system_prompt
def add_system_info() -> str:
    return "You are a helpful assistant."
```

#### Tool with Retries

```python
@agent.tool(retries=3)
def unreliable_api(query: str) -> str:
    """Call an unreliable API."""
    ...
```

#### Testing with Override

```python
from pydantic_ai.models.test import TestModel

with agent.override(model=TestModel()):
    result = agent.run_sync('Test prompt')
```

### 4. Installation

```bash
# Full installation
pip install pydantic-ai

# Slim installation (specific model)
pip install "pydantic-ai-slim[openai]"
```

### 5. Best Practices

1. **Type Safety**: Always define `deps_type` and `output_type` for better IDE support
2. **Dependency Injection**: Use deps for database connections, API clients, etc.
3. **Structured Outputs**: Use Pydantic models for validated, typed responses
4. **Error Handling**: Use `retries` parameter for unreliable tools
5. **Testing**: Use `TestModel` or `override()` for unit tests
