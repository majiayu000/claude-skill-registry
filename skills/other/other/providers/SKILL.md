---
name: providers
description: Use when switching between LLM providers, accessing provider-specific features (Anthropic caching, OpenAI logprobs), or using raw SDK clients - covers multi-provider patterns and direct SDK access for OpenAI, Anthropic, Google, and Ollama
---

# Multi-Provider Patterns and Raw SDK Access

## Installation

```bash
# With uv (recommended)
uv add llmring

# With pip
pip install llmring
```

**Provider SDKs (install what you need):**
```bash
uv add openai>=1.0      # OpenAI
uv add anthropic>=0.67   # Anthropic
uv add google-genai      # Google Gemini
uv add ollama>=0.4       # Ollama
```

## API Overview

This skill covers:
- `get_provider()` method for raw SDK access
- Provider initialization and configuration
- Provider-specific features (caching, extra parameters)
- Multi-provider patterns and switching
- Fallback behavior

## Quick Start

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Get raw provider client
    openai_client = service.get_provider("openai").client
    anthropic_client = service.get_provider("anthropic").client

    # Use provider SDK directly
    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        logprobs=True  # Provider-specific feature
    )
```

## Complete API Documentation

### LLMRing.get_provider()

Get raw provider client for direct SDK access.

**Signature:**
```python
def get_provider(provider_type: str) -> BaseLLMProvider
```

**Parameters:**
- `provider_type` (str): Provider name - "openai", "anthropic", "google", or "ollama"

**Returns:**
- `BaseLLMProvider`: Provider wrapper with `.client` attribute for raw SDK

**Raises:**
- `ProviderNotFoundError`: If provider not configured or API key missing

**Example:**
```python
from llmring import LLMRing

async with LLMRing() as service:
    # Get providers
    openai_provider = service.get_provider("openai")
    anthropic_provider = service.get_provider("anthropic")

    # Access raw clients
    openai_client = openai_provider.client      # openai.AsyncOpenAI
    anthropic_client = anthropic_provider.client # anthropic.AsyncAnthropic
```

### Provider Clients

Each provider exposes its native SDK client:

**OpenAI:**
```python
provider = service.get_provider("openai")
client = provider.client  # openai.AsyncOpenAI instance
```

**Anthropic:**
```python
provider = service.get_provider("anthropic")
client = provider.client  # anthropic.AsyncAnthropic instance
```

**Google:**
```python
provider = service.get_provider("google")
client = provider.client  # google.genai.Client instance
```

**Ollama:**
```python
provider = service.get_provider("ollama")
client = provider.client  # ollama.AsyncClient instance
```

## Provider Initialization

Providers are automatically initialized based on environment variables:

**Environment Variables:**
```bash
# OpenAI
OPENAI_API_KEY=sk-...

# Anthropic
ANTHROPIC_API_KEY=sk-ant-...

# Google (any of these)
GOOGLE_GEMINI_API_KEY=AIza...
GEMINI_API_KEY=AIza...
GOOGLE_API_KEY=AIza...

# Ollama (optional, default shown)
OLLAMA_BASE_URL=http://localhost:11434
```

**What gets initialized:**
- OpenAI: If `OPENAI_API_KEY` is set
- Anthropic: If `ANTHROPIC_API_KEY` is set
- Google: If any Google API key is set
- Ollama: Always (local, no key needed)

## Provider-Specific Features

### OpenAI: Logprobs and Advanced Parameters

```python
from llmring import LLMRing

async with LLMRing() as service:
    openai_client = service.get_provider("openai").client

    # Use OpenAI-specific features
    response = await openai_client.chat.completions.create(
        model="gpt-4o",
        messages=[{"role": "user", "content": "Hello"}],
        logprobs=True,           # Token probabilities
        top_logprobs=5,          # Top 5 alternatives
        seed=12345,              # Deterministic sampling
        presence_penalty=0.1,    # Reduce repetition
        frequency_penalty=0.2,   # Reduce frequency
        parallel_tool_calls=False  # Sequential tools
    )

    # Access logprobs
    if response.choices[0].logprobs:
        for token_info in response.choices[0].logprobs.content:
            print(f"Token: {token_info.token}, prob: {token_info.logprob}")
```

### OpenAI: Reasoning Models (o1 series)

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Using unified API
    request = LLMRequest(
        model="openai:o1",
        messages=[Message(role="user", content="Complex reasoning task")],
        reasoning_tokens=10000  # Budget for internal reasoning
    )

    response = await service.chat(request)

    # Or use raw SDK
    openai_client = service.get_provider("openai").client
    response = await openai_client.chat.completions.create(
        model="o1",
        messages=[{"role": "user", "content": "Reasoning task"}],
        max_completion_tokens=5000  # Includes reasoning + output tokens
    )
```

### Anthropic: Prompt Caching

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Using unified API
    request = LLMRequest(
        model="anthropic:claude-sonnet-4-5-20250929",
        messages=[
            Message(
                role="system",
                content="Very long system prompt with 1024+ tokens...",
                metadata={"cache_control": {"type": "ephemeral"}}
            ),
            Message(role="user", content="Hello")
        ]
    )

    response = await service.chat(request)

    # Or use raw SDK
    anthropic_client = service.get_provider("anthropic").client
    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=100,
        system=[{
            "type": "text",
            "text": "Long system prompt...",
            "cache_control": {"type": "ephemeral"}
        }],
        messages=[{"role": "user", "content": "Hello"}]
    )

    # Check cache usage
    print(f"Cache read tokens: {response.usage.cache_read_input_tokens}")
    print(f"Cache creation tokens: {response.usage.cache_creation_input_tokens}")
```

### Anthropic: Extended Thinking

Extended thinking can be enabled via `extra_params`:

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Using unified API with extra_params
    request = LLMRequest(
        model="anthropic:claude-sonnet-4-5-20250929",
        messages=[Message(role="user", content="Complex reasoning problem...")],
        max_tokens=16000,
        extra_params={
            "thinking": {
                "type": "enabled",
                "budget_tokens": 10000
            }
        }
    )

    response = await service.chat(request)

    # Response may contain thinking content (check response structure)

# Or use raw SDK for full control
async with LLMRing() as service:
    anthropic_client = service.get_provider("anthropic").client

    response = await anthropic_client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=16000,
        thinking={
            "type": "enabled",
            "budget_tokens": 10000
        },
        messages=[{
            "role": "user",
            "content": "Complex reasoning problem..."
        }]
    )

    # Access thinking content
    for block in response.content:
        if block.type == "thinking":
            print(f"Thinking: {block.thinking}")
        elif block.type == "text":
            print(f"Response: {block.text}")
```

**Note:** The unified API's `reasoning_tokens` parameter is for OpenAI reasoning models (o1, o3). For Anthropic extended thinking, use `extra_params` as shown above.

### Google: Large Context and Multimodal

```python
from llmring import LLMRing

async with LLMRing() as service:
    google_client = service.get_provider("google").client

    # Use 2M+ token context
    response = google_client.models.generate_content(
        model="gemini-2.5-pro",
        contents="Very long document with millions of tokens...",
        generation_config={
            "temperature": 0.7,
            "top_p": 0.8,
            "top_k": 40,
            "candidate_count": 1,
            "max_output_tokens": 8192
        }
    )

    # Multimodal (vision)
    from PIL import Image
    img = Image.open("image.jpg")

    response = google_client.models.generate_content(
        model="gemini-2.5-flash",
        contents=["What's in this image?", img]
    )
```

### Ollama: Local Models and Custom Options

```python
from llmring import LLMRing

async with LLMRing() as service:
    ollama_client = service.get_provider("ollama").client

    # Use local model with custom options
    response = await ollama_client.chat(
        model="llama3",
        messages=[{"role": "user", "content": "Hello"}],
        options={
            "temperature": 0.8,
            "top_k": 40,
            "top_p": 0.9,
            "num_predict": 256,
            "num_ctx": 4096,
            "repeat_penalty": 1.1
        }
    )

    # List available local models
    models = await ollama_client.list()
    for model in models["models"]:
        print(f"Model: {model['name']}, Size: {model['size']}")
```

## Using extra_params

For provider-specific parameters via unified API:

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Pass provider-specific params
    request = LLMRequest(
        model="openai:gpt-4o",
        messages=[Message(role="user", content="Hello")],
        extra_params={
            "logprobs": True,
            "top_logprobs": 5,
            "seed": 12345,
            "presence_penalty": 0.1
        }
    )

    response = await service.chat(request)
```

## Multi-Provider Patterns

### Provider Switching

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Same request, different providers
    messages = [Message(role="user", content="Hello")]

    # OpenAI
    response = await service.chat(
        LLMRequest(model="openai:gpt-4o", messages=messages)
    )

    # Anthropic
    response = await service.chat(
        LLMRequest(model="anthropic:claude-sonnet-4-5-20250929", messages=messages)
    )

    # Google
    response = await service.chat(
        LLMRequest(model="google:gemini-2.5-pro", messages=messages)
    )

    # Ollama
    response = await service.chat(
        LLMRequest(model="ollama:llama3", messages=messages)
    )
```

### Automatic Fallback

Use lockfile for automatic provider failover:

```toml
# llmring.lock
[[profiles.default.bindings]]
alias = "reliable"
models = [
    "anthropic:claude-sonnet-4-5-20250929",  # Try first
    "openai:gpt-4o",                 # If rate limited
    "google:gemini-2.5-pro",         # If both fail
    "ollama:llama3"                  # Local fallback
]
```

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    # Automatically tries fallbacks on failure
    request = LLMRequest(
        model="reliable",  # Uses fallback chain
        messages=[Message(role="user", content="Hello")]
    )

    response = await service.chat(request)
    print(f"Used model: {response.model}")
```

### Cost Optimization: Try Cheaper First

```python
from llmring import LLMRing, LLMRequest, Message

async with LLMRing() as service:
    messages = [Message(role="user", content="Simple task")]

    # Try cheap model first
    try:
        response = await service.chat(
            LLMRequest(model="openai:gpt-4o-mini", messages=messages)
        )
    except Exception as e:
        # Fall back to more capable model
        response = await service.chat(
            LLMRequest(model="anthropic:claude-sonnet-4-5-20250929", messages=messages)
        )
```

### Provider-Specific Error Handling

```python
from llmring import LLMRing, LLMRequest, Message
from llmring.exceptions import (
    ProviderRateLimitError,
    ProviderAuthenticationError,
    ModelNotFoundError
)

async with LLMRing() as service:
    try:
        request = LLMRequest(
            model="anthropic:claude-sonnet-4-5-20250929",
            messages=[Message(role="user", content="Hello")]
        )
        response = await service.chat(request)

    except ProviderRateLimitError as e:
        print(f"Rate limited, retry after {e.retry_after}s")
        # Try different provider
        request.model = "openai:gpt-4o"
        response = await service.chat(request)

    except ProviderAuthenticationError:
        print("Invalid API key")

    except ModelNotFoundError:
        print("Model not available")
```

## Provider Comparison

| Provider | Strengths | Limitations | Best For |
|----------|-----------|-------------|----------|
| **OpenAI** | Fast, reliable, reasoning models (o1) | Rate limits, cost | General purpose, reasoning |
| **Anthropic** | Large context, prompt caching, extended thinking | Availability varies by region | Complex tasks, large docs |
| **Google** | 2M+ context, multimodal, fast | Newer, less documentation | Large context, vision |
| **Ollama** | Local, free, privacy | Requires local setup, slower | Development, privacy |

## When to Use Raw SDK Access

**Use unified LLMRing API when:**
- Switching between providers
- Using aliases and profiles
- Standard chat/streaming/tools
- Want provider abstraction

**Use raw SDK access when:**
- Need provider-specific features not in unified API
- Performance-critical applications
- Complex provider-specific configurations
- Vendor-specific optimizations

## Common Mistakes

### Wrong: Not Checking Provider Availability

```python
# DON'T DO THIS - provider may not be configured
provider = service.get_provider("anthropic")
client = provider.client  # May error if no API key!
```

**Right: Check Provider Availability**

```python
# DO THIS - handle missing providers
from llmring.exceptions import ProviderNotFoundError

try:
    provider = service.get_provider("anthropic")
    client = provider.client
except ProviderNotFoundError:
    print("Anthropic not configured - check ANTHROPIC_API_KEY")
```

### Wrong: Hardcoding Provider

```python
# DON'T DO THIS - locked to one provider
request = LLMRequest(
    model="openai:gpt-4o",
    messages=[...]
)
```

**Right: Use Alias for Flexibility**

```python
# DO THIS - easy to switch providers
request = LLMRequest(
    model="assistant",  # Your semantic alias defined in lockfile
    messages=[...]
)
```

### Wrong: Ignoring Provider-Specific Errors

```python
# DON'T DO THIS - generic error handling
try:
    response = await service.chat(request)
except Exception as e:
    print(f"Error: {e}")
```

**Right: Handle Provider-Specific Errors**

```python
# DO THIS - specific error types
from llmring.exceptions import (
    ProviderRateLimitError,
    ProviderTimeoutError
)

try:
    response = await service.chat(request)
except ProviderRateLimitError as e:
    # Try different provider
    request.model = "google:gemini-2.5-pro"
    response = await service.chat(request)
except ProviderTimeoutError:
    # Retry or use different provider
    pass
```

## Best Practices

1. **Use aliases for flexibility:** Don't hardcode provider:model references
2. **Configure fallbacks:** Multiple providers in lockfile for high availability
3. **Check provider availability:** Handle `ProviderNotFoundError`
4. **Use unified API when possible:** Only drop to raw SDK when needed
5. **Handle provider-specific errors:** Different providers have different failure modes
6. **Test with multiple providers:** Ensure your code works across providers
7. **Document provider choices:** Explain why you chose specific providers

## Checking Available Providers

```python
from llmring import LLMRing

async with LLMRing() as service:
    # Check which providers are configured
    providers = []
    for provider_name in ["openai", "anthropic", "google", "ollama"]:
        try:
            service.get_provider(provider_name)
            providers.append(provider_name)
        except:
            pass

    print(f"Available providers: {', '.join(providers)}")
```

## Related Skills

- `llmring-chat` - Basic chat with unified API
- `llmring-streaming` - Streaming across providers
- `llmring-tools` - Tools with different providers
- `llmring-structured` - Structured output across providers
- `llmring-lockfile` - Configure provider aliases and fallbacks

## Summary

**Multi-provider patterns enable:**
- High availability (automatic failover)
- Cost optimization (try cheaper first)
- Provider diversity (avoid vendor lock-in)
- Feature access (use best provider for each task)

**Raw SDK access provides:**
- Provider-specific features (logprobs, caching, etc.)
- Performance optimizations
- Advanced configurations
- Direct vendor SDK control

**Recommendation:** Use unified API with aliases for most work. Drop to raw SDK only when you need provider-specific features.
