---
name: pydantic-ai-model-integration
description: Configure LLM providers, use fallback models, handle streaming, and manage model settings in PydanticAI. Use when selecting models, implementing resilience, or optimizing API calls.
---

# PydanticAI Model Integration

## Provider Model Strings

Format: `provider:model-name`

```python
from pydantic_ai import Agent

# OpenAI
Agent('openai:gpt-4o')
Agent('openai:gpt-4o-mini')
Agent('openai:o1-preview')

# Anthropic
Agent('anthropic:claude-sonnet-4-5')
Agent('anthropic:claude-haiku-4-5')

# Google (API Key)
Agent('google-gla:gemini-2.0-flash')
Agent('google-gla:gemini-2.0-pro')

# Google (Vertex AI)
Agent('google-vertex:gemini-2.0-flash')

# Groq
Agent('groq:llama-3.3-70b-versatile')
Agent('groq:mixtral-8x7b-32768')

# Mistral
Agent('mistral:mistral-large-latest')

# Other providers
Agent('cohere:command-r-plus')
Agent('bedrock:anthropic.claude-3-sonnet')
```

## Model Settings

```python
from pydantic_ai import Agent
from pydantic_ai.settings import ModelSettings

agent = Agent(
    'openai:gpt-4o',
    model_settings=ModelSettings(
        temperature=0.7,
        max_tokens=1000,
        top_p=0.9,
        timeout=30.0,  # Request timeout
    )
)

# Override per-run
result = await agent.run(
    'Generate creative text',
    model_settings=ModelSettings(temperature=1.0)
)
```

## Fallback Models

Chain models for resilience:

```python
from pydantic_ai.models.fallback import FallbackModel

# Try models in order until one succeeds
fallback = FallbackModel(
    'openai:gpt-4o',
    'anthropic:claude-sonnet-4-5',
    'google-gla:gemini-2.0-flash'
)

agent = Agent(fallback)
result = await agent.run('Hello')

# Custom fallback conditions
from pydantic_ai.exceptions import ModelAPIError

def should_fallback(error: Exception) -> bool:
    """Only fallback on rate limits or server errors."""
    if isinstance(error, ModelAPIError):
        return error.status_code in (429, 500, 502, 503)
    return False

fallback = FallbackModel(
    'openai:gpt-4o',
    'anthropic:claude-sonnet-4-5',
    fallback_on=should_fallback
)
```

## Streaming Responses

```python
async def stream_response():
    async with agent.run_stream('Tell me a story') as response:
        # Stream text output
        async for chunk in response.stream_output():
            print(chunk, end='', flush=True)

    # Access final result after streaming
    print(f"\nTokens used: {response.usage().total_tokens}")
```

### Streaming with Structured Output

```python
from pydantic import BaseModel

class Story(BaseModel):
    title: str
    content: str
    moral: str

agent = Agent('openai:gpt-4o', output_type=Story)

async with agent.run_stream('Write a fable') as response:
    # For structured output, stream_output yields partial JSON
    async for partial in response.stream_output():
        print(partial)  # Partial Story object as parsed

    # Final validated result
    story = response.output
```

## Dynamic Model Selection

```python
import os

# Environment-based selection
model = os.getenv('PYDANTIC_AI_MODEL', 'openai:gpt-4o')
agent = Agent(model)

# Runtime model override
result = await agent.run(
    'Hello',
    model='anthropic:claude-sonnet-4-5'  # Override default
)

# Context manager override
with agent.override(model='google-gla:gemini-2.0-flash'):
    result = agent.run_sync('Hello')
```

## Deferred Model Checking

Delay model validation for testing:

```python
# Default: Validates model immediately (checks env vars)
agent = Agent('openai:gpt-4o')

# Deferred: Validates only on first run
agent = Agent('openai:gpt-4o', defer_model_check=True)

# Useful for testing with override
with agent.override(model=TestModel()):
    result = agent.run_sync('Test')  # No OpenAI key needed
```

## Usage Tracking

```python
result = await agent.run('Hello')

# Request usage (last request)
usage = result.usage()
print(f"Input tokens: {usage.input_tokens}")
print(f"Output tokens: {usage.output_tokens}")
print(f"Total tokens: {usage.total_tokens}")

# Full run usage (all requests in run)
run_usage = result.run_usage()
print(f"Total requests: {run_usage.requests}")
```

## Usage Limits

```python
from pydantic_ai.usage import UsageLimits

# Limit token usage
result = await agent.run(
    'Generate content',
    usage_limits=UsageLimits(
        total_tokens=1000,
        request_tokens=500,
        response_tokens=500,
    )
)
```

## Provider-Specific Features

### OpenAI

```python
from pydantic_ai.models.openai import OpenAIModel

model = OpenAIModel(
    'gpt-4o',
    api_key='your-key',  # Or use OPENAI_API_KEY env var
    base_url='https://custom-endpoint.com'  # For Azure, proxies
)
```

### Anthropic

```python
from pydantic_ai.models.anthropic import AnthropicModel

model = AnthropicModel(
    'claude-sonnet-4-5',
    api_key='your-key'  # Or ANTHROPIC_API_KEY
)
```

## Common Model Patterns

| Use Case | Recommendation |
|----------|---------------|
| General purpose | `openai:gpt-4o` or `anthropic:claude-sonnet-4-5` |
| Fast/cheap | `openai:gpt-4o-mini` or `anthropic:claude-haiku-4-5` |
| Long context | `anthropic:claude-sonnet-4-5` (200k) or `google-gla:gemini-2.0-flash` |
| Reasoning | `openai:o1-preview` |
| Cost-sensitive prod | `FallbackModel` with fast model first |
