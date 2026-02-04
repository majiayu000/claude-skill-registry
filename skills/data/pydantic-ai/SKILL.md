---
name: pydantic-ai
description: Build AI agents with PydanticAI. Type-safe agent framework with structured outputs, tools, and dependency injection. Use for production AI agents, type-safe LLM applications, and Python AI development.
---

# PydanticAI

Expert guidance for building type-safe AI agents with Pydantic.

## Installation

```bash
pip install pydantic-ai
```

## Quick Start

```python
from pydantic_ai import Agent

# Simple agent
agent = Agent('openai:gpt-4o')

result = agent.run_sync('What is the capital of France?')
print(result.data)  # Paris
```

## Agents with Structure

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class CityInfo(BaseModel):
    name: str
    country: str
    population: int
    notable_landmarks: list[str]

agent = Agent(
    'openai:gpt-4o',
    result_type=CityInfo,
    system_prompt='You are a geography expert. Provide accurate city information.'
)

result = agent.run_sync('Tell me about Paris')
city = result.data
print(f"{city.name}, {city.country}: pop {city.population:,}")
```

## Tools

### Basic Tools

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o')

@agent.tool
def get_weather(ctx: RunContext[None], city: str) -> str:
    """Get current weather for a city."""
    # In real app, call weather API
    return f"Weather in {city}: 72°F, sunny"

@agent.tool
def calculate(ctx: RunContext[None], expression: str) -> float:
    """Calculate a mathematical expression."""
    return eval(expression)

result = agent.run_sync('What is the weather in NYC and what is 25 * 4?')
```

### Tools with Dependencies

```python
from dataclasses import dataclass
from pydantic_ai import Agent, RunContext

@dataclass
class Dependencies:
    api_key: str
    user_id: str

agent = Agent('openai:gpt-4o', deps_type=Dependencies)

@agent.tool
def fetch_user_data(ctx: RunContext[Dependencies], field: str) -> str:
    """Fetch user data from database."""
    # Access dependencies
    user_id = ctx.deps.user_id
    return f"User {user_id}'s {field}: ..."

result = agent.run_sync(
    'Get my email address',
    deps=Dependencies(api_key='key123', user_id='user456')
)
```

### Dynamic Tools

```python
from pydantic_ai import Agent, RunContext
from pydantic_ai.tools import Tool

def create_search_tool(index_name: str) -> Tool:
    async def search(ctx: RunContext[None], query: str) -> list[str]:
        """Search the index."""
        return [f"Result from {index_name}: {query}"]

    return Tool(search, name=f"search_{index_name}")

agent = Agent('openai:gpt-4o')
agent.tools.append(create_search_tool('documents'))
agent.tools.append(create_search_tool('emails'))
```

## System Prompts

### Static System Prompt

```python
agent = Agent(
    'openai:gpt-4o',
    system_prompt="""You are a helpful coding assistant.
    Always provide code examples in Python.
    Explain your reasoning step by step."""
)
```

### Dynamic System Prompt

```python
from pydantic_ai import Agent, RunContext

@dataclass
class UserContext:
    name: str
    expertise_level: str

agent = Agent('openai:gpt-4o', deps_type=UserContext)

@agent.system_prompt
def get_system_prompt(ctx: RunContext[UserContext]) -> str:
    return f"""You are helping {ctx.deps.name}.
    Their expertise level is: {ctx.deps.expertise_level}.
    Adjust your explanations accordingly."""

result = agent.run_sync(
    'Explain recursion',
    deps=UserContext(name='Alice', expertise_level='beginner')
)
```

## Streaming

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

async def stream_response():
    async with agent.run_stream('Tell me a story') as response:
        async for text in response.stream():
            print(text, end='', flush=True)

# Or sync
with agent.run_stream_sync('Tell me a story') as response:
    for text in response.stream():
        print(text, end='', flush=True)
```

## Structured Streaming

```python
from pydantic import BaseModel
from pydantic_ai import Agent

class Story(BaseModel):
    title: str
    chapters: list[str]
    moral: str

agent = Agent('openai:gpt-4o', result_type=Story)

async def stream_structured():
    async with agent.run_stream('Write a short fable') as response:
        async for partial in response.stream_structured():
            print(partial)  # Partial Story object
```

## Conversation History

```python
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o')

# First message
result1 = agent.run_sync('My name is Alice')

# Continue conversation
result2 = agent.run_sync(
    'What is my name?',
    message_history=result1.all_messages()
)
```

## Multiple Models

```python
from pydantic_ai import Agent

# OpenAI
agent_openai = Agent('openai:gpt-4o')

# Anthropic
agent_claude = Agent('anthropic:claude-3-5-sonnet-20241022')

# Ollama (local)
agent_local = Agent('ollama:llama3.1')

# Azure OpenAI
agent_azure = Agent(
    'azure:gpt-4o',
    api_key='your-key',
    azure_endpoint='https://your-resource.openai.azure.com'
)
```

## Retries and Validation

```python
from pydantic import BaseModel, field_validator
from pydantic_ai import Agent

class ValidatedOutput(BaseModel):
    score: int
    explanation: str

    @field_validator('score')
    @classmethod
    def validate_score(cls, v):
        if not 1 <= v <= 10:
            raise ValueError('Score must be between 1 and 10')
        return v

agent = Agent(
    'openai:gpt-4o',
    result_type=ValidatedOutput,
    retries=3  # Retry on validation failure
)

result = agent.run_sync('Rate this: "Hello World" on scale 1-10')
```

## Result Validators

```python
from pydantic_ai import Agent, RunContext

agent = Agent('openai:gpt-4o', result_type=str)

@agent.result_validator
def validate_result(ctx: RunContext[None], result: str) -> str:
    if len(result) < 10:
        raise ValueError('Response too short')
    return result.strip()
```

## Logfire Integration

```python
import logfire
from pydantic_ai import Agent

logfire.configure()

agent = Agent('openai:gpt-4o')

# All agent calls are automatically traced
result = agent.run_sync('Hello!')
```

## Testing

```python
from pydantic_ai import Agent
from pydantic_ai.models.test import TestModel

# Use test model
agent = Agent(TestModel())

# Mock responses
test_model = TestModel()
test_model.seed_response('Paris is the capital of France')

agent = Agent(test_model)
result = agent.run_sync('What is the capital of France?')
```

## Resources

- [PydanticAI Documentation](https://ai.pydantic.dev/)
- [PydanticAI GitHub](https://github.com/pydantic/pydantic-ai)
- [Examples](https://ai.pydantic.dev/examples/)
