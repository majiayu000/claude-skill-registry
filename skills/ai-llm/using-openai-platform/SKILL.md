---
name: using-openai-platform
description: OpenAI SDK development with GPT-5 family, Chat Completions, Responses API, embeddings, and tool calling. Use for AI-powered applications, chatbots, agents, and semantic search.
---

# OpenAI SDK Development Skill

## Quick Reference

OpenAI SDK development with Python and TypeScript/JavaScript clients. Covers GPT-5 family models, Chat Completions API, Responses API, embeddings, tool calling, and streaming.

**Progressive Disclosure**: This file provides quick reference patterns. See [REFERENCE.md](./REFERENCE.md) for comprehensive API coverage, advanced patterns, and deep dives.

---

## Table of Contents

1. [When to Use](#when-to-use)
2. [GPT-5 Model Family](#gpt-5-model-family)
3. [Quick Start](#quick-start)
4. [Chat Completions API](#chat-completions-api)
5. [Responses API (Next Gen)](#responses-api-next-gen)
6. [Tool Calling](#tool-calling)
7. [Embeddings](#embeddings)
8. [Error Handling](#error-handling)
9. [Platform Differentiators](#platform-differentiators)
10. [Further Reading](#further-reading)
11. [Context7 Integration](#context7-integration)

---

## When to Use

This skill is loaded by `backend-developer` when:
- `openai` package in `requirements.txt` or `pyproject.toml`
- `openai` in `package.json` dependencies
- Environment variables `OPENAI_API_KEY` present
- User mentions "OpenAI", "GPT", or "ChatGPT" in task

---

## GPT-5 Model Family

### Model Selection Guide

| Model | Context | Best For | Cost |
|-------|---------|----------|------|
| `gpt-5.2` | 400K | Flagship - coding, agentic, multimodal | $1.75/$14 |
| `gpt-5.2-pro` | 400K | Maximum reasoning (xhigh effort) | $21/$168 |
| `gpt-5.1` | 256K | Stable, previous generation | $1.50/$12 |
| `gpt-5.1-codex` | 256K | Long-running coding tasks | $1.50/$12 |
| `gpt-5` | 128K | General purpose | $1.25/$10 |
| `gpt-4o` | 128K | Fast, cost-effective | $2.50/$10 |
| `gpt-4o-mini` | 128K | Cheapest, simple tasks | $0.15/$0.60 |

*Costs per 1M tokens (input/output). Cached input: 50-90% discount.*

### Quick Selection

```
Simple chat/Q&A           -> gpt-4o-mini
Standard tasks            -> gpt-4o or gpt-5
Complex reasoning         -> gpt-5.1 with reasoning_effort="high"
Coding/agentic           -> gpt-5.2 or gpt-5.1-codex
Maximum intelligence      -> gpt-5.2-pro with reasoning_effort="xhigh"
```

### Reasoning Effort (GPT-5.1+)

```python
reasoning_effort = "none"    # Fast, no reasoning
reasoning_effort = "low"     # Light reasoning
reasoning_effort = "medium"  # Default
reasoning_effort = "high"    # Extended reasoning
reasoning_effort = "xhigh"   # Maximum (GPT-5.2 Pro only)
```

---

## Quick Start

### Python Setup

```python
from openai import OpenAI

# Client auto-uses OPENAI_API_KEY env var
client = OpenAI()

response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello!"}
    ]
)

print(response.choices[0].message.content)
```

### TypeScript Setup

```typescript
import OpenAI from 'openai';

const openai = new OpenAI();

const response = await openai.chat.completions.create({
  model: 'gpt-5',
  messages: [
    { role: 'system', content: 'You are a helpful assistant.' },
    { role: 'user', content: 'Hello!' }
  ]
});

console.log(response.choices[0].message.content);
```

### Async Python

```python
import asyncio
from openai import AsyncOpenAI

async def main():
    client = AsyncOpenAI()
    response = await client.chat.completions.create(
        model="gpt-5",
        messages=[{"role": "user", "content": "Hello!"}]
    )
    print(response.choices[0].message.content)

asyncio.run(main())
```

---

## Chat Completions API

### Basic Completion

```python
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"}
    ],
    temperature=0.7,
    max_tokens=1000
)

answer = response.choices[0].message.content
usage = response.usage  # tokens used
```

### Message Roles

| Role | Description |
|------|-------------|
| `system` | Sets behavior/context (first message) |
| `user` | Human input |
| `assistant` | Model responses |
| `tool` | Tool/function results |

### Common Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `model` | string | Model ID (e.g., "gpt-5") |
| `messages` | array | Conversation messages |
| `temperature` | 0-2 | Randomness (0=deterministic) |
| `max_tokens` | int | Max response tokens |
| `stream` | boolean | Enable streaming |
| `response_format` | object | JSON mode |
| `tools` | array | Tool definitions |
| `reasoning_effort` | string | Reasoning level (GPT-5.1+) |

### JSON Mode

```python
response = client.chat.completions.create(
    model="gpt-5",
    messages=[
        {"role": "system", "content": "Return JSON only."},
        {"role": "user", "content": "List 3 programming languages."}
    ],
    response_format={"type": "json_object"}
)

data = json.loads(response.choices[0].message.content)
```

### Streaming

```python
stream = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "Tell me a story."}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

---

## Responses API (Next Gen)

The Responses API provides built-in tools, conversation continuity, and chain-of-thought passing between turns.

### When to Use

| Use Case | API |
|----------|-----|
| Simple chat/completion | Chat Completions |
| Built-in web search | Responses API |
| Built-in code interpreter | Responses API |
| Conversation continuity (CoT) | Responses API |

### Basic Usage

```python
response = client.responses.create(
    model="gpt-5",
    input="Explain quantum computing simply."
)

print(response.output_text)
```

### Built-in Tools

```python
# Web search
response = client.responses.create(
    model="gpt-5",
    input="What are the latest AI news today?",
    tools=[{"type": "web_search"}]
)

# Code interpreter
response = client.responses.create(
    model="gpt-5",
    input="Calculate factorial of 20 and plot it",
    tools=[{"type": "code_interpreter"}]
)
```

### Conversation Continuity

```python
# First turn
response1 = client.responses.create(
    model="gpt-5",
    input="My name is Alice and I'm a software engineer."
)

# Continue - CoT passes between turns
response2 = client.responses.create(
    model="gpt-5",
    input="What do I do for work?",
    previous_response_id=response1.id
)
```

---

## Tool Calling

### Quick Tool Definition

```python
tools = [{
    "type": "function",
    "function": {
        "name": "get_weather",
        "description": "Get weather for a location",
        "parameters": {
            "type": "object",
            "properties": {
                "location": {"type": "string", "description": "City, country"},
                "unit": {"type": "string", "enum": ["celsius", "fahrenheit"]}
            },
            "required": ["location"],
            "additionalProperties": False
        },
        "strict": True
    }
}]
```

### Basic Tool Loop

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    return {"temperature": 22, "conditions": "sunny", "unit": unit}

# Initial request
response = client.chat.completions.create(
    model="gpt-5",
    messages=[{"role": "user", "content": "What's the weather in Tokyo?"}],
    tools=tools
)

message = response.choices[0].message

# Process tool calls if present
if message.tool_calls:
    messages = [{"role": "user", "content": "What's the weather in Tokyo?"}]
    messages.append(message)

    for tool_call in message.tool_calls:
        args = json.loads(tool_call.function.arguments)
        result = get_weather(**args)

        messages.append({
            "role": "tool",
            "tool_call_id": tool_call.id,
            "content": json.dumps(result)
        })

    # Get final response
    final = client.chat.completions.create(
        model="gpt-5",
        messages=messages
    )
    print(final.choices[0].message.content)
```

### Tool Choice Options

```python
tool_choice = "auto"      # Model decides
tool_choice = "none"      # No tools
tool_choice = "required"  # Must use at least one
tool_choice = {"type": "function", "function": {"name": "get_weather"}}  # Force specific
```

---

## Embeddings

### Generate Embeddings

```python
response = client.embeddings.create(
    model="text-embedding-3-large",
    input="The quick brown fox",
    dimensions=1024  # Optional: reduce dimensions
)

vector = response.data[0].embedding
```

### Embedding Models

| Model | Dimensions | Use Case |
|-------|------------|----------|
| `text-embedding-3-large` | 3072 (default) | Highest quality |
| `text-embedding-3-small` | 1536 (default) | Cost-effective |

### Batch Embeddings

```python
texts = ["Hello world", "How are you?", "Goodbye"]

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=texts
)

embeddings = [d.embedding for d in response.data]
```

---

## Error Handling

### Common Errors

| Error | Cause | Solution |
|-------|-------|----------|
| `AuthenticationError` | Invalid API key | Check OPENAI_API_KEY |
| `RateLimitError` | Too many requests | Implement backoff |
| `InvalidRequestError` | Bad parameters | Validate inputs |
| `APIConnectionError` | Network issues | Retry with backoff |

### Retry Pattern

```python
from openai import OpenAI, RateLimitError, APIError
import time

def call_with_retry(func, max_retries=3):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError:
            wait = 2 ** attempt
            time.sleep(wait)
        except APIError as e:
            if attempt == max_retries - 1:
                raise
            time.sleep(1)
    raise Exception("Max retries exceeded")
```

---

## Platform Differentiators

| Feature | OpenAI |
|---------|--------|
| Reasoning Effort | Budget-controlled reasoning (none->xhigh) |
| Responses API | Next-gen API with CoT passing |
| Built-in Tools | web_search, code_interpreter, file_search |
| 400K Context | GPT-5.2 largest context window |
| Agents SDK | Persistent threads with tool integration |
| ChatKit | Official React chat components |
| Batch API | 50% cost savings for async processing |

---

## Further Reading

For comprehensive coverage, see [REFERENCE.md](./REFERENCE.md):

- **Installation & Configuration**: Detailed setup, Azure OpenAI, proxies
- **Chat Completions**: Complete parameter reference, multi-turn patterns
- **Responses API**: Full tool integration, streaming events
- **Streaming**: SSE patterns, tool call streaming
- **Tool Calling**: Complete loop implementation, Pydantic helpers
- **Structured Outputs**: JSON Schema mode, Pydantic integration
- **Embeddings**: Similarity search, vector DB patterns
- **Vision & Audio**: Multimodal inputs, Whisper, TTS
- **Agents SDK**: Thread management, multi-agent orchestration
- **Batch API**: Async processing, cost optimization
- **Realtime API**: WebSocket audio/video
- **ChatKit**: React components for chat UIs
- **Error Handling**: Comprehensive retry patterns
- **Rate Limits**: Quotas, tier management
- **Security**: Best practices, API key management

---

## Context7 Integration

For up-to-date documentation beyond this skill:

```python
# Python SDK latest
mcp__context7__resolve-library-id(libraryName="openai")
mcp__context7__query-docs(libraryId="/openai/openai-python", query="streaming")

# Node SDK latest
mcp__context7__query-docs(libraryId="/openai/openai-node", query="tool calling")
```
