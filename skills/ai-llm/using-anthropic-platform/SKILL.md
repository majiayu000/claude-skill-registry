---
name: using-anthropic-platform
description: Claude SDK development with Messages API, Tool Use, Extended Thinking, streaming, and prompt caching
---

# Anthropic Claude SDK - Quick Reference

## When to Use

Load this skill when:
- `anthropic` package in `requirements.txt` or `pyproject.toml`
- `@anthropic-ai/sdk` in `package.json` dependencies
- `ANTHROPIC_API_KEY` environment variable present
- User mentions "Anthropic", "Claude", or Claude models

**For detailed patterns**: See [REFERENCE.md](./REFERENCE.md)

---

## Table of Contents

1. [Claude Models](#claude-models-january-2026)
2. [Quick Start](#quick-start)
3. [Messages API Essentials](#messages-api-essentials)
4. [Streaming](#streaming)
5. [Tool Use (Function Calling)](#tool-use-function-calling)
6. [Extended Thinking](#extended-thinking)
7. [Vision](#vision)
8. [Prompt Caching](#prompt-caching)
9. [Error Handling](#error-handling)
10. [Platform Features](#platform-features)
11. [Further Reading](#further-reading)

---

## Claude Models (January 2026)

| Model | Context | Max Output | Thinking | Best For |
|-------|---------|------------|----------|----------|
| `claude-opus-4-5-20251101` | 200K | 32K | Yes | Maximum intelligence |
| `claude-sonnet-4-20250514` | 200K | 64K | Yes | Complex reasoning, coding |
| `claude-3-5-sonnet-20241022` | 200K | 8K | No | Standard tasks |
| `claude-3-5-haiku-20241022` | 200K | 8K | No | Simple chat, Q&A (cheapest) |

### Model Selection

```
Simple chat/Q&A           -> claude-3-5-haiku (cheapest)
Standard tasks            -> claude-3-5-sonnet
Complex reasoning/coding  -> claude-sonnet-4 or claude-opus-4-5
Extended thinking needed  -> claude-sonnet-4 or claude-opus-4-5
Batch processing          -> Any model (50% cost savings)
```

### Pricing (per 1M tokens)

| Model | Input | Output | Cache Read |
|-------|-------|--------|------------|
| claude-opus-4-5 | $15.00 | $75.00 | $1.50 |
| claude-sonnet-4 | $3.00 | $15.00 | $0.30 |
| claude-3-5-sonnet | $3.00 | $15.00 | $0.30 |
| claude-3-5-haiku | $0.80 | $4.00 | $0.08 |

---

## Quick Start

### Python

```python
from anthropic import Anthropic

client = Anthropic()  # Uses ANTHROPIC_API_KEY env var

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello, Claude!"}]
)
print(message.content[0].text)
```

### TypeScript

```typescript
import Anthropic from '@anthropic-ai/sdk';

const client = new Anthropic();

const message = await client.messages.create({
  model: 'claude-sonnet-4-20250514',
  max_tokens: 1024,
  messages: [{ role: 'user', content: 'Hello, Claude!' }]
});
console.log(message.content[0].text);
```

### Async Python

```python
import asyncio
from anthropic import AsyncAnthropic

async def main():
    client = AsyncAnthropic()
    message = await client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(message.content[0].text)

asyncio.run(main())
```

---

## Messages API Essentials

### With System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are a helpful coding assistant. Be concise.",
    messages=[{"role": "user", "content": "Explain async/await."}]
)
```

### Multi-Turn Conversation

```python
messages = [
    {"role": "user", "content": "What is Python?"},
    {"role": "assistant", "content": "Python is a programming language..."},
    {"role": "user", "content": "How do I install it?"}
]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)
```

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (required) |
| `max_tokens` | int | Max response tokens (required) |
| `messages` | array | Conversation messages (required) |
| `system` | string | System prompt |
| `temperature` | float (0-1) | Randomness |
| `tools` | array | Tool definitions |
| `stream` | boolean | Enable streaming |

---

## Streaming

### Basic Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a story."}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Async Streaming

```python
async with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": prompt}]
) as stream:
    async for text in stream.text_stream:
        print(text, end="", flush=True)
```

---

## Tool Use (Function Calling)

### Define Tools

```python
tools = [{
    "name": "get_weather",
    "description": "Get weather for a location",
    "input_schema": {
        "type": "object",
        "properties": {
            "location": {"type": "string", "description": "City, e.g., San Francisco"}
        },
        "required": ["location"]
    }
}]
```

### Tool Use Loop

```python
def process_with_tools(user_message: str) -> str:
    messages = [{"role": "user", "content": user_message}]

    while True:
        response = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=1024,
            tools=tools,
            messages=messages
        )

        if response.stop_reason == "end_turn":
            return response.content[0].text

        # Process tool calls
        tool_results = []
        for block in response.content:
            if block.type == "tool_use":
                result = execute_tool(block.name, block.input)
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result)
                })

        messages.append({"role": "assistant", "content": response.content})
        messages.append({"role": "user", "content": tool_results})
```

---

## Extended Thinking

For complex reasoning tasks (Claude 4 models only):

```python
response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Tokens allocated for thinking
    },
    messages=[{"role": "user", "content": "Solve this complex problem..."}]
)

for block in response.content:
    if block.type == "thinking":
        print("Thinking:", block.thinking)
    elif block.type == "text":
        print("Response:", block.text)
```

### Budget Guidelines

| Task Complexity | Budget |
|-----------------|--------|
| Simple reasoning | 2,000 - 5,000 |
| Moderate | 5,000 - 10,000 |
| Complex | 10,000 - 20,000 |

---

## Vision

### Image from Base64

```python
import base64

with open("image.jpg", "rb") as f:
    image_data = base64.standard_b64encode(f.read()).decode()

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{
        "role": "user",
        "content": [
            {"type": "image", "source": {
                "type": "base64",
                "media_type": "image/jpeg",
                "data": image_data
            }},
            {"type": "text", "text": "Describe this image."}
        ]
    }]
)
```

### Supported Types

- Images: `image/jpeg`, `image/png`, `image/gif`, `image/webp`
- Documents: `application/pdf`

---

## Prompt Caching

90% cost savings for repeated content (>1024 tokens):

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system=[{
        "type": "text",
        "text": long_system_prompt,
        "cache_control": {"type": "ephemeral"}
    }],
    messages=[{"role": "user", "content": "Question"}]
)

# Check cache usage
print(f"Cache read: {message.usage.cache_read_input_tokens}")
```

---

## Error Handling

```python
from anthropic import (
    Anthropic, RateLimitError, AuthenticationError, APIConnectionError
)
import time

def safe_message(messages, max_retries=3):
    for attempt in range(max_retries):
        try:
            return client.messages.create(
                model="claude-sonnet-4-20250514",
                max_tokens=1024,
                messages=messages
            )
        except AuthenticationError:
            raise  # Don't retry auth errors
        except RateLimitError:
            if attempt < max_retries - 1:
                time.sleep(2 ** attempt)
        except APIConnectionError:
            if attempt < max_retries - 1:
                time.sleep(1)
    return None
```

---

## Platform Features

| Feature | Description |
|---------|-------------|
| Extended Thinking | Budget-controlled deep reasoning |
| Agent SDK | Build agents with Task, Read, Write, Edit, Bash |
| Message Batches | 50% cost savings for async processing |
| Computer Use | Browser/desktop automation (beta) |
| MCP | Model Context Protocol for extensions |
| Citations | Grounded responses with sources |
| Prompt Caching | 90% cost savings on repeated content |

---

## Further Reading

- **[REFERENCE.md](./REFERENCE.md)**: Full API reference, advanced patterns
- **[templates/](./templates/)**: Code generation templates
- **[examples/](./examples/)**: Production-ready examples
- **Official Docs**: https://docs.anthropic.com/
