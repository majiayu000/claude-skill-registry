---
name: 'llm-integration'
description: 'Guide for using LLM utilities in speedy_utils, including memoized OpenAI clients and chat format transformations.'
---

# LLM Integration Guide

This skill provides comprehensive guidance for using the LLM utilities in `speedy_utils`.

## When to Use This Skill

Use this skill when you need to:
- Make OpenAI API calls with automatic caching (memoization) to save costs and time.
- Transform chat messages between different formats (ChatML, ShareGPT, Text).
- Prepare prompts for local LLM inference.

## Prerequisites

- `speedy_utils` installed.
- `openai` package installed for API clients.

## Core Capabilities

### Memoized OpenAI Clients (`MOpenAI`, `MAsyncOpenAI`)
- Drop-in replacements for `OpenAI` and `AsyncOpenAI`.
- Automatically caches `post` (chat completion) requests.
- Uses `speedy_utils` caching backend (disk/memory).
- Configurable per-instance caching.

### Chat Format Transformation (`transform_messages`)
- Converts between:
    - `chatml`: List of `{"role": "...", "content": "..."}` dicts.
    - `sharegpt`: Dict with `{"conversations": [{"from": "...", "value": "..."}]}`.
    - `text`: String with `<|im_start|>` tokens.
    - `simulated_chat`: Human/AI transcript format.
- Supports applying tokenizer templates.

## Usage Examples

### Example 1: Memoized OpenAI Call
Make repeated calls without hitting the API twice.

```python
from llm_utils.lm.openai_memoize import MOpenAI

# Initialize just like OpenAI client
client = MOpenAI(api_key="sk-...")

# First call hits the API
response1 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)

# Second call returns cached result instantly
response2 = client.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[{"role": "user", "content": "Hello"}]
)
```

### Example 2: Async Memoized Call
Same as above but for async workflows.

```python
from llm_utils.lm.openai_memoize import MAsyncOpenAI
import asyncio

async def main():
    client = MAsyncOpenAI(api_key="sk-...")
    response = await client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": "Hi"}]
    )
```

### Example 3: Transforming Chat Formats
Convert ShareGPT format to ChatML.

```python
from llm_utils.chat_format.transform import transform_messages

sharegpt_data = {
    "conversations": [
        {"from": "human", "value": "Hi"},
        {"from": "gpt", "value": "Hello there"}
    ]
}

# Convert to ChatML list
chatml_data = transform_messages(sharegpt_data, frm="sharegpt", to="chatml")
# Result: [{'role': 'user', 'content': 'Hi'}, {'role': 'assistant', 'content': 'Hello there'}]

# Convert to Text string
text_data = transform_messages(chatml_data, frm="chatml", to="text")
# Result: "<|im_start|>user\nHi<|im_end|>\n<|im_start|>assistant\nHello there<|im_end|>\n<|im_start|>assistant\n"
```

## Guidelines

1.  **Caching Behavior**:
    - The cache key is generated from the arguments passed to `create`.
    - If you change any parameter (e.g., `temperature`, `model`), it counts as a new request.
    - Cache is persistent if configured (default behavior of `memoize`).

2.  **Format Detection**:
    - `transform_messages` tries to auto-detect input format, but it's safer to specify `frm` explicitly.

3.  **Tokenizer Support**:
    - You can pass a HuggingFace `tokenizer` to `transform_messages` to use its specific chat template.

## Limitations

- **Streaming**: Memoization does NOT work with streaming responses (`stream=True`).
- **Side Effects**: If your LLM calls rely on randomness (high temperature) and you want different results each time, disable caching or change the seed/input.
