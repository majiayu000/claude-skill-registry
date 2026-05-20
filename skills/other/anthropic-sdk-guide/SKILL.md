---
name: anthropic-sdk-guide
description: >
  Guide for Anthropic Python/TypeScript SDK usage including messages API, streaming,
  prompt caching, batches, token counting, and error handling. Use when the user is
  building with the Anthropic API, setting up Claude SDK, calling messages endpoints,
  implementing streaming, or troubleshooting API errors.
---

# Anthropic SDK Guide

Comprehensive reference for building with the Anthropic Python and TypeScript SDKs.
Covers initialization, messages API, streaming, prompt caching, batches, and error handling.

## When to Use
- User is setting up Anthropic SDK (Python or TypeScript)
- User is calling the Messages API or needs streaming responses
- User wants prompt caching, batch processing, or token counting
- User is debugging API errors or rate limits
- User asks about Claude model IDs or API configuration

## Core Patterns

### SDK Installation and Setup

```bash
# Python
pip install anthropic

# TypeScript
npm install @anthropic-ai/sdk
```

```python
# Python - client initialization
import anthropic

client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var
# Or explicit: anthropic.Anthropic(api_key="sk-ant-...")
```

```typescript
// TypeScript - client initialization
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();  // Uses ANTHROPIC_API_KEY env var
```

### Messages API - Basic Usage

```python
# Python - simple message
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    system="You are a helpful coding assistant.",
    messages=[
        {"role": "user", "content": "Explain async/await in Python."}
    ]
)
print(message.content[0].text)
```

```typescript
// TypeScript - simple message
const message = await client.messages.create({
  model: "claude-sonnet-4-6-20250514",
  max_tokens: 1024,
  system: "You are a helpful coding assistant.",
  messages: [
    { role: "user", content: "Explain async/await in Python." }
  ],
});
console.log(message.content[0].text);
```

### Streaming Responses

```python
# Python - streaming with context manager
with client.messages.stream(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a short story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)

# Access final message after stream completes
final_message = stream.get_final_message()
```

```typescript
// TypeScript - streaming
const stream = client.messages.stream({
  model: "claude-sonnet-4-6-20250514",
  max_tokens: 1024,
  messages: [{ role: "user", content: "Write a short story." }],
});

stream.on("text", (text) => process.stdout.write(text));

const finalMessage = await stream.finalMessage();
```

### Prompt Caching

Use cache_control to cache large system prompts, tool definitions, or conversation prefixes.
Cached content costs 90% less on cache hits.

```python
# Python - prompt caching with large system prompt
message = client.messages.create(
    model="claude-sonnet-4-6-20250514",
    max_tokens=1024,
    system=[
        {
            "type": "text",
            "text": "You are an expert on this large codebase..." + large_context,
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[{"role": "user", "content": "What does the auth module do?"}]
)
# Check cache performance
print(f"Cache read: {message.usage.cache_read_input_tokens}")
print(f"Cache creation: {message.usage.cache_creation_input_tokens}")
```

### Batch Processing

Process up to 10,000 requests at 50% cost with 24-hour turnaround.

```python
# Python - create a batch
batch = client.messages.batches.create(
    requests=[
        {
            "custom_id": f"request-{i}",
            "params": {
                "model": "claude-sonnet-4-6-20250514",
                "max_tokens": 1024,
                "messages": [{"role": "user", "content": prompt}]
            }
        }
        for i, prompt in enumerate(prompts)
    ]
)

# Poll for completion
import time
while True:
    status = client.messages.batches.retrieve(batch.id)
    if status.processing_status == "ended":
        break
    time.sleep(60)

# Stream results
for result in client.messages.batches.results(batch.id):
    if result.result.type == "succeeded":
        print(result.custom_id, result.result.message.content[0].text)
```

### Token Counting

```python
# Python - count tokens before sending
count = client.messages.count_tokens(
    model="claude-sonnet-4-6-20250514",
    system="You are a helpful assistant.",
    messages=[{"role": "user", "content": long_document}]
)
print(f"Input tokens: {count.input_tokens}")
```

### Error Handling

```python
import anthropic

try:
    message = client.messages.create(
        model="claude-sonnet-4-6-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except anthropic.RateLimitError:
    # Back off and retry - SDK has built-in retries (2 by default)
    print("Rate limited. The SDK will auto-retry.")
except anthropic.APIStatusError as e:
    print(f"API error {e.status_code}: {e.message}")
except anthropic.APIConnectionError:
    print("Network connection failed.")
```

## Anti-Patterns
- Hardcoding API keys instead of using environment variables
- Not setting max_tokens (it is required, not optional)
- Ignoring the stop_reason field (could be "end_turn", "max_tokens", or "tool_use")
- Polling batch status too frequently (use 60-second intervals minimum)
- Not using streaming for user-facing applications (causes perceived latency)
- Setting temperature > 0 for deterministic tasks like classification or extraction

## Quick Reference

| Model ID | Best For |
|-----------|----------|
| claude-opus-4-6-20250514 | Deep reasoning, complex tasks |
| claude-sonnet-4-6-20250514 | Best balance of speed and capability |
| claude-haiku-4-5-20251001 | Fast, lightweight tasks |

| Feature | Endpoint / Method |
|---------|-------------------|
| Messages | `client.messages.create()` |
| Streaming | `client.messages.stream()` |
| Batches | `client.messages.batches.create()` |
| Token count | `client.messages.count_tokens()` |
| Prompt caching | `cache_control: {"type": "ephemeral"}` |

Default retries: 2 (configurable via `max_retries` on client).
