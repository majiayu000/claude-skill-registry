---
name: faion-claude-api-skill
user-invocable: false
description: ""
---

# Claude API Mastery

**Complete Guide to Anthropic Claude API (2025-2026)**

---

## Quick Reference

| API | Endpoint | Best Model | Use Case |
|-----|----------|------------|----------|
| **Messages** | `/v1/messages` | claude-sonnet-4 | Text generation, conversation |
| **Tool Use** | `/v1/messages` | claude-sonnet-4 | Function calling, structured output |
| **Vision** | `/v1/messages` | claude-sonnet-4 | Image/PDF understanding |
| **Extended Thinking** | `/v1/messages` | claude-opus-4-5 | Complex reasoning |
| **Computer Use** | `/v1/messages` | claude-sonnet-4 | Browser/desktop automation |
| **Batch** | `/v1/messages/batches` | All models | 50% cost savings |
| **Prompt Caching** | `/v1/messages` | All models | 90% cached input savings |
| **Token Counting** | `/v1/messages/count_tokens` | All models | Pre-flight token estimation |

---

## Authentication

### Setup

```bash
# Environment variable (recommended)
export ANTHROPIC_API_KEY="sk-ant-..."

# Or load from file
source ~/.secrets/anthropic  # Loads ANTHROPIC_API_KEY
```

### Headers

```bash
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json"
```

### Required Headers

| Header | Value | Purpose |
|--------|-------|---------|
| `x-api-key` | `sk-ant-...` | Authentication |
| `anthropic-version` | `2023-06-01` | API version |
| `content-type` | `application/json` | Request format |

### Optional Headers

| Header | Purpose |
|--------|---------|
| `anthropic-beta` | Enable beta features (e.g., `prompt-caching-2024-07-31`) |

---

## Models

### Available Models (2025-2026)

| Model | ID | Context | Input $/M | Output $/M | Best For |
|-------|-----|---------|-----------|------------|----------|
| **Claude Opus 4.5** | `claude-opus-4-5-20251101` | 200K | $15.00 | $75.00 | Complex reasoning, research |
| **Claude Sonnet 4** | `claude-sonnet-4-20250514` | 200K | $3.00 | $15.00 | Balanced (recommended) |
| **Claude Haiku 3.5** | `claude-3-5-haiku-20241022` | 200K | $0.80 | $4.00 | Fast, cost-effective |

### Model Selection Guide

| Task | Recommended Model | Why |
|------|-------------------|-----|
| General chat | claude-sonnet-4 | Best balance |
| Complex reasoning | claude-opus-4-5 | Highest capability |
| Code generation | claude-sonnet-4 | Fast, excellent coding |
| Quick classification | claude-3-5-haiku | Fastest, cheapest |
| Long documents | claude-sonnet-4 | Good 200K context |
| Extended thinking | claude-opus-4-5 | Deep reasoning |

### Legacy Models (Deprecated)

| Model | Status |
|-------|--------|
| claude-3-opus-20240229 | Replaced by Opus 4.5 |
| claude-3-sonnet-20240229 | Replaced by Sonnet 4 |
| claude-3-5-sonnet-20240620 | Replaced by Sonnet 4 |
| claude-3-haiku-20240307 | Replaced by Haiku 3.5 |

---

## Messages API

### Basic Request

```python
import anthropic

client = anthropic.Anthropic()  # Uses ANTHROPIC_API_KEY env var

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {"role": "user", "content": "Explain SDD methodology in 3 sentences."}
    ]
)

print(message.content[0].text)
```

### With System Prompt

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    system="You are an expert on Specification-Driven Development. Be concise and practical.",
    messages=[
        {"role": "user", "content": "What are the key phases of SDD?"}
    ]
)
```

### Multi-turn Conversation

```python
messages = [
    {"role": "user", "content": "What is SDD?"},
    {"role": "assistant", "content": "SDD (Specification-Driven Development) is a methodology..."},
    {"role": "user", "content": "How does it compare to TDD?"}
]

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=messages
)
```

### Parameters

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,           # Required: max response tokens
    messages=[...],

    # Optional
    system="System prompt",    # Set behavior
    temperature=1.0,           # 0-1, higher = more creative
    top_p=0.9,                 # Nucleus sampling (alternative to temp)
    top_k=40,                  # Top-k sampling
    stop_sequences=["END"],    # Stop generation at these
    metadata={"user_id": "123"}  # Track requests
)
```

### Response Structure

```python
message = client.messages.create(...)

# Response object
print(message.id)              # "msg_01XFDUDYJgAACzvnptvVoYEL"
print(message.type)            # "message"
print(message.role)            # "assistant"
print(message.content)         # [ContentBlock(type="text", text="...")]
print(message.model)           # "claude-sonnet-4-20250514"
print(message.stop_reason)     # "end_turn" | "max_tokens" | "stop_sequence" | "tool_use"
print(message.stop_sequence)   # The stop sequence that triggered (if any)
print(message.usage)           # Usage(input_tokens=X, output_tokens=Y)
```

### Content Blocks

```python
for block in message.content:
    if block.type == "text":
        print(block.text)
    elif block.type == "tool_use":
        print(f"Tool: {block.name}")
        print(f"Input: {block.input}")
```

---

## Tool Use / Function Calling

### Define Tools

```python
tools = [
    {
        "name": "get_weather",
        "description": "Get current weather for a location. Call this when user asks about weather.",
        "input_schema": {
            "type": "object",
            "properties": {
                "location": {
                    "type": "string",
                    "description": "City name, e.g., 'Kyiv, Ukraine'"
                },
                "unit": {
                    "type": "string",
                    "enum": ["celsius", "fahrenheit"],
                    "description": "Temperature unit"
                }
            },
            "required": ["location"]
        }
    }
]
```

### Request with Tools

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather in Kyiv?"}
    ]
)

# Check stop reason
if message.stop_reason == "tool_use":
    for block in message.content:
        if block.type == "tool_use":
            print(f"Tool: {block.name}")
            print(f"ID: {block.id}")
            print(f"Input: {block.input}")
```

### Complete Tool Loop

```python
import json

def get_weather(location: str, unit: str = "celsius") -> dict:
    # Your implementation
    return {"temperature": 15, "condition": "cloudy", "unit": unit}

# Initial request
messages = [{"role": "user", "content": "What's the weather in Kyiv?"}]

response = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=messages
)

# Process tool calls
while response.stop_reason == "tool_use":
    # Add assistant message with tool use
    messages.append({"role": "assistant", "content": response.content})

    # Process each tool use
    tool_results = []
    for block in response.content:
        if block.type == "tool_use":
            # Execute tool
            result = get_weather(**block.input)

            tool_results.append({
                "type": "tool_result",
                "tool_use_id": block.id,
                "content": json.dumps(result)
            })

    # Add tool results
    messages.append({"role": "user", "content": tool_results})

    # Continue conversation
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        tools=tools,
        messages=messages
    )

# Final response
print(response.content[0].text)
```

### Tool Choice

```python
# Auto (default) - model decides
tool_choice = {"type": "auto"}

# Required - must use a tool
tool_choice = {"type": "any"}

# Force specific tool
tool_choice = {"type": "tool", "name": "get_weather"}

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    tool_choice=tool_choice,
    messages=[...]
)
```

### Tool Result with Error

```python
# Success
tool_result = {
    "type": "tool_result",
    "tool_use_id": "toolu_01...",
    "content": json.dumps({"temperature": 15})
}

# Error
tool_result = {
    "type": "tool_result",
    "tool_use_id": "toolu_01...",
    "is_error": True,
    "content": "Error: Location not found"
}
```

### Parallel Tool Calls

Claude can request multiple tools simultaneously:

```python
# Response with multiple tool uses
for block in response.content:
    if block.type == "tool_use":
        print(f"Tool: {block.name}, ID: {block.id}")
        # Execute each tool and collect results

# Return all results in single message
tool_results = [
    {"type": "tool_result", "tool_use_id": "toolu_01...", "content": "..."},
    {"type": "tool_result", "tool_use_id": "toolu_02...", "content": "..."}
]
messages.append({"role": "user", "content": tool_results})
```

### Structured Output with Tools

```python
# Force JSON output via tool
json_tool = {
    "name": "output_json",
    "description": "Output the result as structured JSON",
    "input_schema": {
        "type": "object",
        "properties": {
            "name": {"type": "string"},
            "age": {"type": "integer"},
            "email": {"type": "string", "format": "email"}
        },
        "required": ["name", "age"]
    }
}

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=[json_tool],
    tool_choice={"type": "tool", "name": "output_json"},
    messages=[
        {"role": "user", "content": "Extract: John Doe, 30, john@example.com"}
    ]
)

# Get structured data
tool_use = next(b for b in message.content if b.type == "tool_use")
data = tool_use.input  # {"name": "John Doe", "age": 30, "email": "john@example.com"}
```

---

## Vision (Images and PDFs)

### Image from Base64

```python
import base64

def encode_image(path: str) -> str:
    with open(path, "rb") as f:
        return base64.standard_b64encode(f.read()).decode("utf-8")

image_data = encode_image("screenshot.png")

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "base64",
                        "media_type": "image/png",
                        "data": image_data
                    }
                },
                {
                    "type": "text",
                    "text": "Describe this screenshot"
                }
            ]
        }
    ]
)
```

### Image from URL

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "image",
                    "source": {
                        "type": "url",
                        "url": "https://example.com/image.jpg"
                    }
                },
                {
                    "type": "text",
                    "text": "What's in this image?"
                }
            ]
        }
    ]
)
```

### Multiple Images

```python
message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Compare these two designs:"},
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": image1_b64}
                },
                {
                    "type": "image",
                    "source": {"type": "base64", "media_type": "image/png", "data": image2_b64}
                }
            ]
        }
    ]
)
```

### PDF Support

```python
# PDFs are sent as documents (up to 100 pages)
pdf_data = encode_image("document.pdf")  # Same base64 encoding

message = client.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    messages=[
        {
            "role": "user",
            "content": [
                {
                    "type": "document",
                    "source": {
                        "type": "base64",
                        "media_type": "application/pdf",
                        "data": pdf_data
                    }
                },
                {
                    "type": "text",
                    "text": "Summarize this document"
                }
            ]
        }
    ]
)
```

### Supported Formats

| Format | Media Type | Max Size |
|--------|------------|----------|
| JPEG | `image/jpeg` | 20MB |
| PNG | `image/png` | 20MB |
| GIF | `image/gif` | 20MB |
| WebP | `image/webp` | 20MB |
| PDF | `application/pdf` | 32MB / 100 pages |

### Vision Best Practices

1. **Place images before text** for better understanding
2. **Use high resolution** for text extraction (OCR)
3. **Describe what you need** specifically
4. **Combine multiple images** for comparisons

---

## Extended Thinking

Extended thinking enables Claude to show its reasoning process for complex problems.

### Enable Extended Thinking

```python
message = client.messages.create(
    model="claude-opus-4-5-20251101",  # Works best with Opus
    max_tokens=16000,
    thinking={
        "type": "enabled",
        "budget_tokens": 10000  # Max tokens for thinking
    },
    messages=[
        {"role": "user", "content": "Solve this step by step: If a train leaves..."}
    ]
)
```

### Access Thinking

```python
for block in message.content:
    if block.type == "thinking":
        print("Thinking:", block.thinking)
    elif block.type == "text":
        print("Answer:", block.text)
```

### Use Cases

| Use Case | Benefit |
|----------|---------|
| **Math problems** | Step-by-step reasoning |
| **Logic puzzles** | Explicit deduction |
| **Code debugging** | Trace through logic |
| **Research synthesis** | Structured analysis |
| **Strategic planning** | Consider alternatives |

### Thinking Pricing

Extended thinking tokens are charged at output rate:
- Claude Opus 4.5: $75/M tokens for thinking
- Budget wisely based on complexity

### Best Practices

1. **Use appropriate budget** - 5K-10K for most problems
2. **Ask for step-by-step** - triggers deeper thinking
3. **Complex problems only** - overkill for simple tasks
4. **Review thinking** - validate reasoning quality

---

## Computer Use

Computer use allows Claude to control a computer via screenshots and actions.

### Available Tools

| Tool | Purpose |
|------|---------|
| `computer` | Screen interaction (screenshot, click, type) |
| `text_editor` | File editing |
| `bash` | Shell commands |

### Computer Tool

```python
computer_tool = {
    "type": "computer_20241022",
    "name": "computer",
    "display_width_px": 1920,
    "display_height_px": 1080,
    "display_number": 1
}

message = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=4096,
    tools=[computer_tool],
    betas=["computer-use-2024-10-22"],
    messages=[
        {"role": "user", "content": "Open Chrome and search for SDD methodology"}
    ]
)
```

### Handle Computer Actions

```python
for block in message.content:
    if block.type == "tool_use" and block.name == "computer":
        action = block.input["action"]

        if action == "screenshot":
            # Take screenshot, return as base64
            screenshot = take_screenshot()
            tool_result = {"type": "tool_result", "tool_use_id": block.id, "content": [...]}

        elif action == "mouse_move":
            x, y = block.input["coordinate"]
            move_mouse(x, y)

        elif action == "left_click":
            click()

        elif action == "type":
            text = block.input["text"]
            type_text(text)

        elif action == "key":
            key = block.input["key"]  # e.g., "Return", "ctrl+c"
            press_key(key)
```

### Text Editor Tool

```python
text_editor_tool = {
    "type": "text_editor_20241022",
    "name": "str_replace_editor"
}

# Claude can view, create, and edit files
# Actions: view, create, str_replace, insert, undo_edit
```

### Bash Tool

```python
bash_tool = {
    "type": "bash_20241022",
    "name": "bash"
}

# Claude can execute bash commands
# Returns stdout, stderr
```

### Safety Considerations

1. **Sandbox environment** - Use VMs or containers
2. **Limited permissions** - No sudo, restricted paths
3. **Network isolation** - Block external access if needed
4. **Human oversight** - Review actions before execution
5. **Timeout limits** - Prevent infinite loops

---

## Prompt Caching

Reduce costs by 90% on cached input tokens.

### Enable Caching

```python
message = client.beta.messages.create(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    betas=["prompt-caching-2024-07-31"],
    system=[
        {
            "type": "text",
            "text": "You are an expert on Faion Network and SDD methodology. [Long system prompt...]",
            "cache_control": {"type": "ephemeral"}
        }
    ],
    messages=[
        {"role": "user", "content": "What is SDD?"}
    ]
)

# Check cache usage
print(f"Cache creation: {message.usage.cache_creation_input_tokens}")
print(f"Cache read: {message.usage.cache_read_input_tokens}")
```

### Cacheable Content

```python
# System prompt
system = [
    {"type": "text", "text": "Long instructions...", "cache_control": {"type": "ephemeral"}}
]

# Messages with context
messages = [
    {
        "role": "user",
        "content": [
            {
                "type": "text",
                "text": "Here is a long document: [10K tokens...]",
                "cache_control": {"type": "ephemeral"}
            }
        ]
    }
]

# Tool definitions
tools = [
    {
        "name": "complex_tool",
        "description": "...",
        "input_schema": {...},
        "cache_control": {"type": "ephemeral"}
    }
]
```

### Cache Pricing

| Model | Cache Write | Cache Read | Savings |
|-------|-------------|------------|---------|
| Claude Opus 4.5 | $18.75/M | $1.50/M | 90% on read |
| Claude Sonnet 4 | $3.75/M | $0.30/M | 90% on read |
| Claude Haiku 3.5 | $1.00/M | $0.08/M | 90% on read |

### Cache Behavior

- **TTL:** 5 minutes from last use (extends on each use)
- **Minimum:** 1024 tokens to cache
- **Prefix matching:** Content must be at the start
- **Organization-scoped:** Cache shared within org

### Best Practices

1. **Cache system prompts** - Most reused content
2. **Cache long documents** - For multi-turn analysis
3. **Order matters** - Cached content must be prefix
4. **Monitor usage** - Track cache hit rate

---

## Batch API

50% cost reduction for non-time-sensitive workloads.

### Create Batch

```python
import json

# Prepare requests
requests = [
    {
        "custom_id": "req-001",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "Hello!"}]
        }
    },
    {
        "custom_id": "req-002",
        "params": {
            "model": "claude-sonnet-4-20250514",
            "max_tokens": 1024,
            "messages": [{"role": "user", "content": "World!"}]
        }
    }
]

# Create batch
batch = client.beta.messages.batches.create(
    requests=requests
)

print(f"Batch ID: {batch.id}")
print(f"Status: {batch.processing_status}")
```

### Check Status

```python
batch = client.beta.messages.batches.retrieve(batch.id)

print(f"Status: {batch.processing_status}")  # in_progress | ended
print(f"Total: {batch.request_counts.processing + batch.request_counts.succeeded + batch.request_counts.errored}")
print(f"Succeeded: {batch.request_counts.succeeded}")
print(f"Errored: {batch.request_counts.errored}")
```

### Get Results

```python
# When batch is complete
if batch.processing_status == "ended":
    for result in client.beta.messages.batches.results(batch.id):
        print(f"ID: {result.custom_id}")
        print(f"Type: {result.result.type}")  # succeeded | errored

        if result.result.type == "succeeded":
            print(f"Response: {result.result.message.content[0].text}")
        else:
            print(f"Error: {result.result.error}")
```

### Batch Pricing

| Model | Regular | Batch (50% off) |
|-------|---------|-----------------|
| Claude Opus 4.5 | $15/$75 | $7.50/$37.50 |
| Claude Sonnet 4 | $3/$15 | $1.50/$7.50 |
| Claude Haiku 3.5 | $0.80/$4 | $0.40/$2 |

### Use Cases

- **Content generation** - Blog posts, translations
- **Data processing** - Classification, extraction
- **Analysis** - Document review, summarization
- **Testing** - Prompt evaluation, benchmarks

---

## Streaming

### Basic Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Write a poem about AI"}]
) as stream:
    for text in stream.text_stream:
        print(text, end="", flush=True)
```

### Event-Based Streaming

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            print(f"Block started: {event.content_block.type}")
        elif event.type == "content_block_delta":
            if event.delta.type == "text_delta":
                print(event.delta.text, end="", flush=True)
        elif event.type == "message_stop":
            print("\n[Complete]")
```

### Stream with Tools

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    tools=tools,
    messages=[{"role": "user", "content": "What's the weather in Kyiv?"}]
) as stream:
    for event in stream:
        if event.type == "content_block_start":
            if event.content_block.type == "tool_use":
                print(f"Tool: {event.content_block.name}")
        elif event.type == "content_block_delta":
            if event.delta.type == "input_json_delta":
                print(event.delta.partial_json, end="")
```

### Collect Full Response

```python
with client.messages.stream(
    model="claude-sonnet-4-20250514",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Hello"}]
) as stream:
    response = stream.get_final_message()
    print(response.content[0].text)
```

### Async Streaming

```python
import asyncio

async def stream_response():
    async with client.messages.stream(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    ) as stream:
        async for text in stream.text_stream:
            print(text, end="", flush=True)

asyncio.run(stream_response())
```

### Server-Sent Events Format

Raw SSE format for custom implementations:

```
event: message_start
data: {"type":"message_start","message":{...}}

event: content_block_start
data: {"type":"content_block_start","index":0,"content_block":{...}}

event: content_block_delta
data: {"type":"content_block_delta","index":0,"delta":{"type":"text_delta","text":"Hello"}}

event: content_block_stop
data: {"type":"content_block_stop","index":0}

event: message_stop
data: {"type":"message_stop"}
```

---

## MCP (Model Context Protocol)

MCP allows Claude to connect to external tools and data sources.

### MCP Overview

```
Claude <-> MCP Server <-> Tools/Resources/Prompts
```

### MCP in Claude Desktop

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/files"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "..."
      }
    }
  }
}
```

### Available MCP Servers

| Server | Purpose |
|--------|---------|
| **filesystem** | Read/write local files |
| **github** | GitHub API access |
| **postgres** | PostgreSQL queries |
| **sqlite** | SQLite database |
| **puppeteer** | Browser automation |
| **google-drive** | Google Drive access |
| **slack** | Slack integration |

### MCP with API

```python
# MCP is primarily for Claude Desktop
# For API, use tool use pattern instead

# Tools provide similar functionality:
# - filesystem -> custom file tools
# - github -> GitHub API tools
# - database -> SQL execution tools
```

---

## Rate Limiting

### Limits

| Tier | Requests/min | Tokens/min | Tokens/day |
|------|--------------|------------|------------|
| **Tier 1** | 50 | 40,000 | 1,000,000 |
| **Tier 2** | 1,000 | 80,000 | 2,500,000 |
| **Tier 3** | 2,000 | 160,000 | 5,000,000 |
| **Tier 4** | 4,000 | 400,000 | 10,000,000 |

### Rate Limit Headers

```python
# Check headers in response
response = client.messages.with_raw_response.create(...)

print(response.headers.get("x-ratelimit-limit-requests"))
print(response.headers.get("x-ratelimit-remaining-requests"))
print(response.headers.get("x-ratelimit-reset-requests"))
print(response.headers.get("x-ratelimit-limit-tokens"))
print(response.headers.get("x-ratelimit-remaining-tokens"))
print(response.headers.get("x-ratelimit-reset-tokens"))
```

### Retry with Backoff

```python
import time
from anthropic import RateLimitError, APIError

def call_with_retry(func, max_retries=5, base_delay=1):
    for attempt in range(max_retries):
        try:
            return func()
        except RateLimitError as e:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            print(f"Rate limited. Retrying in {delay}s...")
            time.sleep(delay)
        except APIError as e:
            if e.status_code >= 500:
                if attempt == max_retries - 1:
                    raise
                delay = base_delay * (2 ** attempt)
                print(f"Server error. Retrying in {delay}s...")
                time.sleep(delay)
            else:
                raise

# Usage
response = call_with_retry(
    lambda: client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
)
```

### Using tenacity

```python
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from anthropic import RateLimitError, APIError

@retry(
    retry=retry_if_exception_type((RateLimitError, APIError)),
    wait=wait_exponential(multiplier=1, min=1, max=60),
    stop=stop_after_attempt(5)
)
def make_request():
    return client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
```

---

## Error Handling

### Common Errors

| Error | HTTP Code | Cause | Solution |
|-------|-----------|-------|----------|
| `invalid_api_key` | 401 | Bad API key | Check ANTHROPIC_API_KEY |
| `rate_limit_error` | 429 | Too many requests | Implement backoff |
| `overloaded_error` | 529 | API overloaded | Retry with backoff |
| `invalid_request_error` | 400 | Bad parameters | Check request format |
| `not_found_error` | 404 | Invalid model | Check model name |
| `api_error` | 500 | Server issue | Retry with backoff |

### Error Response Structure

```python
try:
    response = client.messages.create(...)
except anthropic.BadRequestError as e:
    print(f"Status: {e.status_code}")
    print(f"Message: {e.message}")
    print(f"Type: {e.body.get('error', {}).get('type')}")
```

### Handle Specific Errors

```python
import anthropic

try:
    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1024,
        messages=[{"role": "user", "content": "Hello"}]
    )
except anthropic.AuthenticationError:
    print("Invalid API key")
except anthropic.RateLimitError:
    print("Rate limited - wait and retry")
except anthropic.BadRequestError as e:
    print(f"Bad request: {e.message}")
except anthropic.APIStatusError as e:
    print(f"API error: {e.status_code}")
```

---

## Token Counting

### Pre-count Tokens

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    messages=[
        {"role": "user", "content": "Hello, how are you?"}
    ]
)

print(f"Input tokens: {count.input_tokens}")
```

### With System and Tools

```python
count = client.messages.count_tokens(
    model="claude-sonnet-4-20250514",
    system="You are a helpful assistant.",
    tools=tools,
    messages=[
        {"role": "user", "content": "What's the weather?"}
    ]
)

print(f"Input tokens: {count.input_tokens}")
```

### Usage from Response

```python
response = client.messages.create(...)

print(f"Input: {response.usage.input_tokens}")
print(f"Output: {response.usage.output_tokens}")
print(f"Cache creation: {getattr(response.usage, 'cache_creation_input_tokens', 0)}")
print(f"Cache read: {getattr(response.usage, 'cache_read_input_tokens', 0)}")
```

---

## Cost Tracking

### Calculate Costs

```python
class ClaudeCostTracker:
    PRICES = {
        "claude-opus-4-5-20251101": {"input": 15.00, "output": 75.00},
        "claude-sonnet-4-20250514": {"input": 3.00, "output": 15.00},
        "claude-3-5-haiku-20241022": {"input": 0.80, "output": 4.00},
    }

    CACHE_PRICES = {
        "claude-opus-4-5-20251101": {"write": 18.75, "read": 1.50},
        "claude-sonnet-4-20250514": {"write": 3.75, "read": 0.30},
        "claude-3-5-haiku-20241022": {"write": 1.00, "read": 0.08},
    }

    def __init__(self):
        self.total_cost = 0.0
        self.calls = []

    def track(self, model: str, usage) -> float:
        prices = self.PRICES.get(model, {"input": 0, "output": 0})
        cache_prices = self.CACHE_PRICES.get(model, {"write": 0, "read": 0})

        input_cost = usage.input_tokens * prices["input"] / 1_000_000
        output_cost = usage.output_tokens * prices["output"] / 1_000_000

        # Cache costs (if applicable)
        cache_write = getattr(usage, 'cache_creation_input_tokens', 0)
        cache_read = getattr(usage, 'cache_read_input_tokens', 0)
        cache_cost = (cache_write * cache_prices["write"] + cache_read * cache_prices["read"]) / 1_000_000

        total = input_cost + output_cost + cache_cost
        self.total_cost += total
        self.calls.append({"model": model, "cost": total})
        return total

    def report(self):
        print(f"Total cost: ${self.total_cost:.4f}")
        print(f"Total calls: {len(self.calls)}")

tracker = ClaudeCostTracker()

# Usage
response = client.messages.create(...)
cost = tracker.track(response.model, response.usage)
print(f"This call: ${cost:.4f}")
```

### Batch Cost Savings

```python
# Regular pricing
regular_cost = (input_tokens * 3.00 + output_tokens * 15.00) / 1_000_000

# Batch pricing (50% off)
batch_cost = regular_cost * 0.5

print(f"Saved: ${regular_cost - batch_cost:.4f}")
```

---

## Best Practices

### 1. Model Selection

| Task | Model | Reasoning |
|------|-------|-----------|
| Chat/general | Sonnet 4 | Best balance |
| Complex analysis | Opus 4.5 | Maximum capability |
| High volume | Haiku 3.5 | Cost-effective |
| Code generation | Sonnet 4 | Fast, accurate |

### 2. Prompt Engineering

```python
# Bad - vague
messages = [{"role": "user", "content": "Write something about AI"}]

# Good - specific
messages = [
    {
        "role": "user",
        "content": """Write a 200-word introduction about AI for developers.

Requirements:
- Focus on practical applications
- Include one Python code example
- Use technical but accessible language

Format: Markdown with code block"""
    }
]
```

### 3. System Prompts

```python
# Effective system prompt structure
system = """You are an expert SDD consultant.

Role: Help developers implement Specification-Driven Development

Behavior:
- Be concise and practical
- Use examples from real projects
- Provide actionable advice

Format:
- Use markdown for structure
- Include code examples when relevant
- Add links to resources when helpful"""
```

### 4. Tool Design

```python
# Good tool definition
{
    "name": "search_docs",
    "description": "Search Faion Network documentation. Use when user asks about SDD, agents, or skills.",
    "input_schema": {
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (2-5 keywords)"
            },
            "category": {
                "type": "string",
                "enum": ["sdd", "agents", "skills", "methodology"],
                "description": "Documentation category"
            }
        },
        "required": ["query"]
    }
}
```

### 5. Cost Optimization

1. **Use caching** for repeated context
2. **Choose appropriate model** for task
3. **Use Batch API** for non-urgent work
4. **Set max_tokens** appropriately
5. **Pre-count tokens** for large inputs

---

## Quick Commands

### curl Examples

```bash
# Basic message
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# With system prompt
curl https://api.anthropic.com/v1/messages \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "max_tokens": 1024,
    "system": "You are a helpful assistant.",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'

# Count tokens
curl https://api.anthropic.com/v1/messages/count_tokens \
  -H "x-api-key: $ANTHROPIC_API_KEY" \
  -H "anthropic-version: 2023-06-01" \
  -H "content-type: application/json" \
  -d '{
    "model": "claude-sonnet-4-20250514",
    "messages": [{"role": "user", "content": "Hello!"}]
  }'
```

### Python SDK Install

```bash
pip install anthropic
```

### Node.js SDK Install

```bash
npm install @anthropic-ai/sdk
```

### TypeScript Example

```typescript
import Anthropic from "@anthropic-ai/sdk";

const client = new Anthropic();

const message = await client.messages.create({
  model: "claude-sonnet-4-20250514",
  max_tokens: 1024,
  messages: [
    { role: "user", content: "Hello!" }
  ]
});

console.log(message.content[0].text);
```

---

## Related Skills

- **faion-openai-api-skill** - OpenAI API (alternative LLM)
- **faion-gemini-api-skill** - Gemini API (alternative LLM)
- **faion-langchain-skill** - LLM orchestration
- **faion-embeddings-skill** - Vector embeddings (use OpenAI)
- **faion-image-gen-skill** - Image generation (DALL-E, FLUX)
- **faion-finetuning-skill** - Model customization

---

## Sources

- [Anthropic API Documentation](https://docs.anthropic.com/)
- [Anthropic API Reference](https://docs.anthropic.com/en/api)
- [Claude Code Documentation](https://docs.anthropic.com/en/docs/claude-code)
- [Anthropic Pricing](https://www.anthropic.com/pricing)
- [Prompt Engineering Guide](https://docs.anthropic.com/en/docs/build-with-claude/prompt-engineering)
- [MCP Documentation](https://modelcontextprotocol.io/)
