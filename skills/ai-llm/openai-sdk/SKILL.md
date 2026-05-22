---
name: openai-sdk
description: |
  OpenAI official SDK usage (Python, Node.js). Use when: writing code that calls OpenAI API,
  implementing chat/embeddings/images/audio features, handling streaming responses,
  async patterns, error handling with SDK. For raw HTTP/REST calls, see `openai-api` skill.
---

# OpenAI SDK

Official SDKs for Python and Node.js. Handles auth, retries, types automatically.

## Quick Start

### Python

```bash
pip install openai
```

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY env var

response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hello!"}]
)
print(response.choices[0].message.content)
```

### Node.js

```bash
npm install openai
```

```typescript
import OpenAI from "openai";

const client = new OpenAI();  // Uses OPENAI_API_KEY env var

const response = await client.chat.completions.create({
  model: "gpt-4o",
  messages: [{ role: "user", content: "Hello!" }],
});
console.log(response.choices[0].message.content);
```

## Environment Variables

```bash
export OPENAI_API_KEY="sk-..."
export OPENAI_ORG_ID="org-..."      # Optional
export OPENAI_PROJECT_ID="proj-..." # Optional
```

## Key Features

| Feature | Python | Node.js |
|---------|--------|---------|
| Sync client | `OpenAI()` | `new OpenAI()` |
| Async client | `AsyncOpenAI()` | Same (async/await) |
| Streaming | `stream=True` | `stream: true` |
| Auto-retry | Built-in | Built-in |
| Timeout | `timeout=60` | `timeout: 60000` |
| Types | Full typing | TypeScript |

## Common Operations

### Chat Completion
```python
response = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hi"}]
)
```

### Streaming
```python
stream = client.chat.completions.create(
    model="gpt-4o",
    messages=[{"role": "user", "content": "Hi"}],
    stream=True
)
for chunk in stream:
    print(chunk.choices[0].delta.content or "", end="")
```

### Embeddings
```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input="Hello world"
)
vector = response.data[0].embedding
```

### Image Generation
```python
response = client.images.generate(
    model="dall-e-3",
    prompt="A sunset over mountains",
    size="1024x1024"
)
url = response.data[0].url
```

### Audio Transcription
```python
with open("audio.mp3", "rb") as f:
    transcript = client.audio.transcriptions.create(
        model="whisper-1",
        file=f
    )
print(transcript.text)
```

## Error Handling

```python
from openai import OpenAI, APIError, RateLimitError

client = OpenAI()

try:
    response = client.chat.completions.create(...)
except RateLimitError:
    # Retry with backoff
except APIError as e:
    print(f"API error: {e.status_code}")
```

## References

- **[python.md](references/python.md)** — Full Python SDK guide
- **[nodejs.md](references/nodejs.md)** — Full Node.js SDK guide
- **[streaming.md](references/streaming.md)** — Streaming patterns for both

## Related

- `openai-api` skill — Raw REST API without SDK
