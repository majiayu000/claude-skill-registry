---
name: litellm
description: Unified LLM API with LiteLLM. Call 100+ LLM providers with one interface. Use for multi-provider AI, cost optimization, fallbacks, and LLM gateway deployment.
---

# LiteLLM

Expert guidance for unified LLM API access across providers.

## Installation

```bash
pip install litellm
```

## Quick Start

```python
from litellm import completion

# OpenAI
response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Anthropic
response = completion(
    model="claude-3-5-sonnet-20241022",
    messages=[{"role": "user", "content": "Hello!"}]
)

# Azure OpenAI
response = completion(
    model="azure/gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="https://my-resource.openai.azure.com",
    api_key="your-key",
    api_version="2024-02-01"
)

# Ollama
response = completion(
    model="ollama/llama3.1",
    messages=[{"role": "user", "content": "Hello!"}],
    api_base="http://localhost:11434"
)
```

## Streaming

```python
from litellm import completion

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in response:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

## Async

```python
import asyncio
from litellm import acompletion

async def main():
    response = await acompletion(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

## Embeddings

```python
from litellm import embedding

# OpenAI
response = embedding(
    model="text-embedding-3-small",
    input=["Hello world"]
)

# Cohere
response = embedding(
    model="cohere/embed-english-v3.0",
    input=["Hello world"]
)

embeddings = response.data[0].embedding
```

## Function Calling

```python
from litellm import completion

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

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=tools,
    tool_choice="auto"
)

if response.choices[0].message.tool_calls:
    for tool_call in response.choices[0].message.tool_calls:
        print(f"Function: {tool_call.function.name}")
        print(f"Arguments: {tool_call.function.arguments}")
```

## Fallbacks & Retries

```python
from litellm import completion
import litellm

# Enable fallbacks
litellm.set_verbose = True

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}],
    fallbacks=["claude-3-5-sonnet-20241022", "gpt-3.5-turbo"],
    num_retries=3
)
```

## Router (Load Balancing)

```python
from litellm import Router

router = Router(
    model_list=[
        {
            "model_name": "gpt-4",
            "litellm_params": {
                "model": "azure/gpt-4-deployment",
                "api_base": "https://us-east.openai.azure.com",
                "api_key": "key1"
            }
        },
        {
            "model_name": "gpt-4",
            "litellm_params": {
                "model": "azure/gpt-4-deployment",
                "api_base": "https://us-west.openai.azure.com",
                "api_key": "key2"
            }
        }
    ],
    routing_strategy="least-busy"  # or "simple-shuffle", "latency-based-routing"
)

response = router.completion(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Proxy Server

### Configuration (config.yaml)

```yaml
model_list:
  - model_name: gpt-4
    litellm_params:
      model: azure/gpt-4
      api_base: https://my-resource.openai.azure.com
      api_key: os.environ/AZURE_API_KEY
      api_
  - model_name: claude
    litellm_params:
      model: claude-3-5-sonnet-20241022
      api_key: os.environ/ANTHROPIC_API_KEY

litellm_settings:
  drop_params: true
  set_verbose: false

general_settings:
  master_key: sk-1234
  database_url: postgresql://user:pass@localhost/litellm
```

### Run Proxy

```bash
# Start server
litellm --config config.yaml --port 4000

# Or with Docker
docker run -p 4000:4000 \
  -v $(pwd)/config.yaml:/app/config.yaml \
  ghcr.io/berriai/litellm:main-latest \
  --config /app/config.yaml
```

### Use Proxy

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:4000",
    api_key="sk-1234"
)

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Cost Tracking

```python
from litellm import completion
import litellm

litellm.success_callback = ["langfuse"]  # or "langsmith", "helicone"

response = completion(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello"}]
)

# Access cost
print(f"Cost: ${response._hidden_params['response_cost']}")
```

## Budget Management

```python
from litellm import BudgetManager

budget = BudgetManager(project_name="my-project")

# Set budget
budget.create_budget(
    total_budget=100,  # $100
    user="user-123",
    duration="monthly"
)

# Check before request
if budget.get_current_cost("user-123") < budget.get_total_budget("user-123"):
    response = completion(model="gpt-4o", messages=[...])
    budget.update_cost(response._hidden_params['response_cost'], "user-123")
```

## Model Aliases

```python
import litellm

litellm.model_alias_map = {
    "fast": "gpt-3.5-turbo",
    "smart": "gpt-4o",
    "cheap": "claude-3-haiku-20240307"
}

response = completion(
    model="smart",  # Uses gpt-4o
    messages=[{"role": "user", "content": "Hello"}]
)
```

## Resources

- [LiteLLM Documentation](https://docs.litellm.ai/)
- [LiteLLM GitHub](https://github.com/BerriAI/litellm)
- [Supported Providers](https://docs.litellm.ai/docs/providers)
