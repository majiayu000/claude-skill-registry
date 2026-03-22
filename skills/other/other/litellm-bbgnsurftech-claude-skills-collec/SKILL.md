---
name: litellm
description: When calling LLM APIs from Python code. When connecting to llamafile or local LLM servers. When switching between OpenAI/Anthropic/local providers. When implementing retry/fallback logic for LLM calls. When code imports litellm or uses completion() patterns.
---

# LiteLLM

Unified Python interface for calling 100+ LLM APIs using consistent OpenAI format. Provides standardized exception handling, retry/fallback logic, and cost tracking across multiple providers.

## When to Use This Skill

Use this skill when:

- Integrating with multiple LLM providers through a single interface
- Routing requests to local llamafile servers using OpenAI-compatible endpoints
- Implementing retry and fallback logic for LLM calls
- Building applications requiring consistent error handling across providers
- Tracking LLM usage costs across different providers
- Converting between provider-specific APIs and OpenAI format
- Deploying LLM proxy servers with unified configuration
- Testing applications against both cloud and local LLM endpoints

## Core Capabilities

### Provider Support

LiteLLM supports 100+ providers through consistent OpenAI-style API:

- **Cloud Providers**: OpenAI, Anthropic, Google, Azure, AWS Bedrock
- **Local Servers**: llamafile, Ollama, LocalAI, vLLM
- **Unified Format**: All requests use OpenAI message format
- **Exception Mapping**: All provider errors map to OpenAI exception types

### Key Features

1. **Unified API**: Single `completion()` function for all providers
2. **Exception Handling**: All exceptions inherit from OpenAI types
3. **Retry Logic**: Built-in retry with configurable attempts
4. **Streaming Support**: Sync and async streaming for all providers
5. **Cost Tracking**: Automatic usage and cost calculation
6. **Proxy Mode**: Deploy centralized LLM gateway

## Installation

```bash
# Using pip
pip install litellm

# Using uv
uv add litellm
```

## Llamafile Integration

### Provider Configuration

All llamafile models MUST use the `llamafile/` prefix for routing:

```python
model = "llamafile/mistralai/mistral-7b-instruct-v0.2"
model = "llamafile/gemma-3-3b"
```

### API Base URL

The `api_base` MUST point to llamafile's OpenAI-compatible endpoint:

```python
api_base = "http://localhost:8080/v1"
```

**Critical Requirements**:

- Include `/v1` suffix
- Do NOT add endpoint paths like `/chat/completions` (LiteLLM adds these automatically)
- Default llamafile port is 8080

### Environment Variable Configuration

```python
import os

os.environ["LLAMAFILE_API_BASE"] = "http://localhost:8080/v1"
```

## Basic Usage Patterns

### Synchronous Completion

```python
import litellm

response = litellm.completion(
    model="llamafile/mistralai/mistral-7b-instruct-v0.2",
    messages=[{"role": "user", "content": "Summarize this diff"}],
    api_base="http://localhost:8080/v1",
    temperature=0.2,
    max_tokens=80,
)

print(response.choices[0].message.content)
```

### Asynchronous Completion

```python
from litellm import acompletion
import asyncio

async def generate_message():
    response = await acompletion(
        model="llamafile/gemma-3-3b",
        messages=[{"role": "user", "content": "Write a commit message"}],
        api_base="http://localhost:8080/v1",
        temperature=0.3,
        max_tokens=200,
    )
    return response.choices[0].message.content

result = asyncio.run(generate_message())
print(result)
```

### Async Streaming

```python
from litellm import acompletion
import asyncio

async def stream_response():
    response = await acompletion(
        model="llamafile/gemma-3-3b",
        messages=[{"role": "user", "content": "Hello, how are you?"}],
        api_base="http://localhost:8080/v1",
        stream=True,
    )

    async for chunk in response:
        if chunk.choices[0].delta.content:
            print(chunk.choices[0].delta.content, end="", flush=True)
    print()

asyncio.run(stream_response())
```

### Embeddings

```python
from litellm import embedding
import os

os.environ["LLAMAFILE_API_BASE"] = "http://localhost:8080/v1"

response = embedding(
    model="llamafile/sentence-transformers/all-MiniLM-L6-v2",
    input=["Hello world"],
)

print(response)
```

## Exception Handling

### Import Pattern

All exceptions can be imported directly from `litellm`:

```python
from litellm import (
    BadRequestError,           # 400 errors
    AuthenticationError,       # 401 errors
    NotFoundError,             # 404 errors
    Timeout,                   # 408 errors (alias: openai.APITimeoutError)
    RateLimitError,            # 429 errors
    APIConnectionError,        # 500 errors / connection issues (default)
    ServiceUnavailableError,   # 503 errors
)
```

### Exception Types Reference

| Status Code | Exception Type                | Inherits from                | Description                 |
| ----------- | ----------------------------- | ---------------------------- | --------------------------- |
| 400         | `BadRequestError`             | openai.BadRequestError       | Invalid request             |
| 400         | `ContextWindowExceededError`  | litellm.BadRequestError      | Token limit exceeded        |
| 400         | `ContentPolicyViolationError` | litellm.BadRequestError      | Content policy violation    |
| 401         | `AuthenticationError`         | openai.AuthenticationError   | Auth failure                |
| 403         | `PermissionDeniedError`       | openai.PermissionDeniedError | Permission denied           |
| 404         | `NotFoundError`               | openai.NotFoundError         | Invalid model/endpoint      |
| 408         | `Timeout`                     | openai.APITimeoutError       | Request timeout             |
| 429         | `RateLimitError`              | openai.RateLimitError        | Rate limited                |
| 500         | `APIConnectionError`          | openai.APIConnectionError    | Default for unmapped errors |
| 500         | `APIError`                    | openai.APIError              | Generic 500 error           |
| 503         | `ServiceUnavailableError`     | openai.APIStatusError        | Service unavailable         |
| >=500       | `InternalServerError`         | openai.InternalServerError   | Unmapped 500+ errors        |

### Exception Attributes

All LiteLLM exceptions include:

- `status_code`: HTTP status code
- `message`: Error message
- `llm_provider`: Provider that raised the exception

### Exception Handling Example

```python
import litellm
import openai

try:
    response = litellm.completion(
        model="llamafile/gemma-3-3b",
        messages=[{"role": "user", "content": "Hello"}],
        api_base="http://localhost:8080/v1",
        timeout=30.0,
    )
except openai.APITimeoutError as e:
    # LiteLLM exceptions inherit from OpenAI types
    print(f"Timeout: {e}")
except litellm.APIConnectionError as e:
    print(f"Connection failed: {e.message}")
    print(f"Provider: {e.llm_provider}")
```

### Alternative Import from litellm.exceptions

```python
from litellm.exceptions import BadRequestError, AuthenticationError, APIError

try:
    response = litellm.completion(
        model="llamafile/gemma-3-3b",
        messages=[{"role": "user", "content": "Hello"}],
        api_base="http://localhost:8080/v1",
    )
except AuthenticationError as e:
    print(f"Authentication failed: {e}")
except BadRequestError as e:
    print(f"Bad request: {e}")
except APIError as e:
    print(f"API error: {e}")
```

### Checking If Exception Should Retry

```python
import litellm

try:
    response = litellm.completion(
        model="llamafile/gemma-3-3b",
        messages=[{"role": "user", "content": "Hello"}],
        api_base="http://localhost:8080/v1",
    )
except Exception as e:
    if hasattr(e, 'status_code'):
        should_retry = litellm._should_retry(e.status_code)
        print(f"Should retry: {should_retry}")
```

## Retry and Fallback Configuration

```python
from litellm import completion

response = completion(
    model="llamafile/gemma-3-3b",
    messages=[{"role": "user", "content": "Hello"}],
    api_base="http://localhost:8080/v1",
    num_retries=3,      # Retry 3 times on failure
    timeout=30.0,       # 30 second timeout
)
```

## Proxy Server Configuration

For proxy deployments, use `config.yaml`:

```yaml
model_list:
  - model_name: commit-polish-model
    litellm_params:
      model: llamafile/gemma-3-3b          # add llamafile/ prefix
      api_base: http://localhost:8080/v1   # add api base for OpenAI compatible provider
```

## Application Integration Patterns

### Connection Verification Pattern

```python
import litellm
from litellm import APIConnectionError

def verify_llamafile_connection(api_base: str = "http://localhost:8080/v1") -> bool:
    """Check if llamafile server is running."""
    try:
        litellm.completion(
            model="llamafile/test",
            messages=[{"role": "user", "content": "test"}],
            api_base=api_base,
            max_tokens=1,
        )
        return True
    except APIConnectionError:
        return False
```

### Async Service Pattern

```python
import litellm
from litellm import acompletion, APIConnectionError
import asyncio

class AIService:
    """LiteLLM wrapper with llamafile routing."""

    def __init__(self, model: str, api_base: str, temperature: float = 0.3, max_tokens: int = 200):
        self.model = model
        self.api_base = api_base
        self.temperature = temperature
        self.max_tokens = max_tokens

    async def generate_commit_message(self, diff: str, system_prompt: str) -> str:
        """Generate a commit message using the LLM."""
        try:
            response = await acompletion(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": f"Generate a commit message for this diff:\n\n{diff}"},
                ],
                api_base=self.api_base,
                temperature=self.temperature,
                max_tokens=self.max_tokens,
            )
            return response.choices[0].message.content.strip()
        except APIConnectionError as e:
            raise RuntimeError(f"Failed to connect to llamafile server at {self.api_base}: {e.message}")
```

## Common Pitfalls to Avoid

1. **Missing `llamafile/` prefix**: Without prefix, LiteLLM won't route to OpenAI-compatible endpoint
2. **Wrong port**: Llamafile uses 8080 by default, not 8000
3. **Missing `/v1` suffix**: API base must end with `/v1`
4. **Adding extra path segments**: Do NOT use `http://localhost:8080/v1/chat/completions` - LiteLLM adds the endpoint path automatically
5. **API key requirement**: No API key needed for local llamafile (use empty string or any value if required by validation)

## Configuration Examples

### TOML Configuration

```toml
# ~/.config/commit-polish/config.toml
[ai]
model = "llamafile/gemma-3-3b"  # MUST have llamafile/ prefix
temperature = 0.3
max_tokens = 200
```

### Environment Variables

```bash
export LLAMAFILE_API_BASE="http://localhost:8080/v1"
export LITELLM_LOG="INFO"  # Enable LiteLLM debug logging
```

## Related Skills

For comprehensive documentation on related tools:

- **llamafile**: Activate the llamafile skill using `Skill(command: "llamafile")` for llamafile server setup, model management, and local LLM deployment patterns
- **uv**: Activate the uv skill using `Skill(command: "uv")` for Python project management, dependency handling, and virtual environment workflows

## References

### Official Documentation

- [LiteLLM Documentation](https://docs.litellm.ai/) - Main documentation portal
- [Llamafile Provider Docs](https://docs.litellm.ai/docs/providers/llamafile) - Llamafile-specific configuration
- [Exception Mapping](https://docs.litellm.ai/docs/exception_mapping) - Complete exception reference
- [GitHub Repository](https://github.com/BerriAI/litellm) - Source code and examples

### Provider-Specific Documentation

- [Llamafile API Endpoints](https://github.com/Mozilla-Ocho/llamafile/blob/main/llama.cpp/server/README.md#api-endpoints) - Llamafile OpenAI-compatible API reference
- [Completion Streaming](https://docs.litellm.ai/docs/completion/stream) - Streaming implementation guide

### Version Information

- Documentation verified against: LiteLLM GitHub repository (main branch, accessed 2025-01-15)
- Python: 3.11+
- Llamafile: 0.9.3+
