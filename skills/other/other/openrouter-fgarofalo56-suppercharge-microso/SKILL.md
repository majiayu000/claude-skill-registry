---
name: openrouter
description: Access 100+ AI models via OpenRouter. Route between providers, manage costs, and use fallbacks. Use for multi-model AI applications, cost optimization, and LLM provider abstraction.
---

# OpenRouter

Expert guidance for multi-provider AI model access.

## Installation

```bash
pip install openai  # Uses OpenAI-compatible API
```

## Quick Start

```python
from openai import OpenAI

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key="your-openrouter-key"
)

response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Hello!"}]
)

print(response.choices[0].message.content)
```

## Available Models

```python
# Anthropic
model = "anthropic/claude-3.5-sonnet"
model = "anthropic/claude-3-opus"
model = "anthropic/claude-3-haiku"

# OpenAI
model = "openai/gpt-4o"
model = "openai/gpt-4-turbo"
model = "openai/gpt-3.5-turbo"

# Google
model = "google/gemini-pro-1.5"
model = "google/gemini-flash-1.5"

# Meta
model = "meta-llama/llama-3.1-405b-instruct"
model = "meta-llama/llama-3.1-70b-instruct"

# Mistral
model = "mistralai/mistral-large"
model = "mistralai/mixtral-8x7b-instruct"

# Free models (rate limited)
model = "meta-llama/llama-3.1-8b-instruct:free"
```

## Request Headers

```python
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Hello!"}],
    extra_headers={
        "HTTP-Referer": "https://your-app.com",  # For rankings
        "X-Title": "Your App Name"  # For identification
    }
)
```

## Streaming

```python
stream = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Function Calling

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a city",
        "parameters": {
            "type": "object",
            "properties": {
                "city": {"type": "string"}
            },
            "required": ["city"]
        }
    }
}]

response = client.chat.completions.create(
    model="openai/gpt-4o",
    messages=[{"role": "user", "content": "Weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

if response.choices[0].message.tool_calls:
    for call in response.choices[0].message.tool_calls:
        print(f"Function: {call.function.name}")
        print(f"Args: {call.function.arguments}")
```

## Provider Routing

```python
# Route to specific provider
response = client.chat.completions.create(
    model="openai/gpt-4o",  # Explicit provider
    messages=[{"role": "user", "content": "Hello"}]
)

# Let OpenRouter choose best provider
response = client.chat.completions.create(
    model="gpt-4o",  # OpenRouter routes automatically
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "provider": {
            "order": ["Azure", "OpenAI"],  # Preferred order
            "allow_fallbacks": True
        }
    }
)
```

## Cost Control

```python
# Set spending limit per request
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "max_price": {
            "prompt": 0.01,      # Max $/1K prompt tokens
            "completion": 0.03   # Max $/1K completion tokens
        }
    }
)

# Check usage
print(f"Prompt tokens: {response.usage.prompt_tokens}")
print(f"Completion tokens: {response.usage.completion_tokens}")
```

## Fallbacks

```python
# Define fallback models
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "route": "fallback",
        "models": [
            "anthropic/claude-3.5-sonnet",
            "openai/gpt-4o",
            "google/gemini-pro-1.5"
        ]
    }
)
```

## Transforms

```python
# Enable prompt transforms for better compatibility
response = client.chat.completions.create(
    model="anthropic/claude-3.5-sonnet",
    messages=[{"role": "user", "content": "Hello"}],
    extra_body={
        "transforms": ["middle-out"]  # Compress long prompts
    }
)
```

## Get Model Info

```python
import requests

# List all models
response = requests.get(
    "https://openrouter.ai/api/v1/models",
    headers={"Authorization": f"Bearer {api_key}"}
)

models = response.json()["data"]
for model in models[:5]:
    print(f"{model['id']}: ${model['pricing']['prompt']}/1K tokens")
```

## Check Credits

```python
import requests

response = requests.get(
    "https://openrouter.ai/api/v1/auth/key",
    headers={"Authorization": f"Bearer {api_key}"}
)

info = response.json()
print(f"Credits remaining: ${info['data']['limit'] - info['data']['usage']}")
```

## Async Usage

```python
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key="your-key"
    )

    response = await client.chat.completions.create(
        model="anthropic/claude-3.5-sonnet",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## LangChain Integration

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    model="anthropic/claude-3.5-sonnet",
    openai_api_base="https://openrouter.ai/api/v1",
    openai_api_key="your-openrouter-key",
    model_kwargs={
        "extra_headers": {
            "HTTP-Referer": "https://your-app.com"
        }
    }
)

response = llm.invoke("Hello!")
```

## Resources

- [OpenRouter Documentation](https://openrouter.ai/docs)
- [Model List](https://openrouter.ai/models)
- [API Reference](https://openrouter.ai/docs/api-reference)
