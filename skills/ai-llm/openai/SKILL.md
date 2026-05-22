---
name: openai
description: |
  OpenAI compatibility layer for Ollama. Use the official OpenAI Python
  library to interact with Ollama, enabling easy migration from OpenAI
  and compatibility with LangChain, LlamaIndex, and other OpenAI-based tools.
---

# Ollama OpenAI Compatibility

## Overview

Ollama provides an OpenAI-compatible API at `/v1/*` endpoints. This allows using the official `openai` Python library with Ollama, enabling:

- **Migration** - Drop-in replacement for OpenAI API
- **Tool ecosystem** - Works with LangChain, LlamaIndex, etc.
- **Familiar interface** - Standard OpenAI patterns

## Quick Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/v1/models` | GET | List models |
| `/v1/completions` | POST | Text generation |
| `/v1/chat/completions` | POST | Chat completion |
| `/v1/embeddings` | POST | Generate embeddings |

### Limitations

The OpenAI compatibility layer does **not** support:

- Show model details (`/api/show`)
- List running models (`/api/ps`)
- Copy model (`/api/copy`)
- Delete model (`/api/delete`)

Use `bazzite-ai-jupyter:chat` or `bazzite-ai-jupyter:ollama` for these operations.

## Setup

```python
import os
from openai import OpenAI

OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

client = OpenAI(
    base_url=f"{OLLAMA_HOST}/v1",
    api_key="ollama"  # Required by library but ignored by Ollama
)
```

## List Models

```python
models = client.models.list()

for model in models.data:
    print(f"  - {model.id}")
```

## Text Completions

```python
response = client.completions.create(
    model="llama3.2:latest",
    prompt="Why is the sky blue? Answer in one sentence.",
    max_tokens=100
)

print(response.choices[0].text)
print(f"Tokens used: {response.usage.completion_tokens}")
```

## Chat Completion

### Single Turn

```python
response = client.chat.completions.create(
    model="llama3.2:latest",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain machine learning in one sentence."}
    ],
    temperature=0.7,
    max_tokens=100
)

print(response.choices[0].message.content)
print(f"Tokens used: {response.usage.total_tokens}")
```

### Multi-Turn Conversation

```python
messages = [
    {"role": "system", "content": "You are a helpful math tutor."}
]

# Turn 1
messages.append({"role": "user", "content": "What is 2 + 2?"})
response = client.chat.completions.create(
    model="llama3.2:latest",
    messages=messages,
    max_tokens=50
)
assistant_msg = response.choices[0].message.content
messages.append({"role": "assistant", "content": assistant_msg})
print(f"User: What is 2 + 2?")
print(f"Assistant: {assistant_msg}")

# Turn 2
messages.append({"role": "user", "content": "And what is that multiplied by 3?"})
response = client.chat.completions.create(
    model="llama3.2:latest",
    messages=messages,
    max_tokens=50
)
print(f"User: And what is that multiplied by 3?")
print(f"Assistant: {response.choices[0].message.content}")
```

## Streaming

```python
stream = client.chat.completions.create(
    model="llama3.2:latest",
    messages=[{"role": "user", "content": "Count from 1 to 5."}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Generate Embeddings

```python
response = client.embeddings.create(
    model="llama3.2:latest",
    input="Ollama makes running LLMs locally easy."
)

embedding = response.data[0].embedding
print(f"Dimensions: {len(embedding)}")
print(f"First 5 values: {embedding[:5]}")
```

## Error Handling

```python
try:
    response = client.chat.completions.create(
        model="invalid-model",
        messages=[{"role": "user", "content": "Hello"}]
    )
except Exception as e:
    print(f"Error: {type(e).__name__}")
```

## Migration from OpenAI

### Before (OpenAI)

```python
from openai import OpenAI

client = OpenAI()  # Uses OPENAI_API_KEY

response = client.chat.completions.create(
    model="gpt-4",
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### After (Ollama)

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)

response = client.chat.completions.create(
    model="llama3.2:latest",  # Change model name
    messages=[{"role": "user", "content": "Hello!"}]
)
```

## LangChain Integration

```python
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
    model="llama3.2:latest"
)

response = llm.invoke("What is Python?")
print(response.content)
```

## LlamaIndex Integration

```python
from llama_index.llms.openai import OpenAI

llm = OpenAI(
    api_base="http://localhost:11434/v1",
    api_key="ollama",
    model="llama3.2:latest"
)

response = llm.complete("What is Python?")
print(response.text)
```

## Connection Health Check

```python
import requests

def check_ollama_health(model="llama3.2:latest"):
    """Check if Ollama server is running and model is available."""
    OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")
    try:
        response = requests.get(f"{OLLAMA_HOST}/api/tags", timeout=5)
        if response.status_code == 200:
            models = response.json()
            model_names = [m.get("name", "") for m in models.get("models", [])]
            return True, model in model_names
        return False, False
    except requests.exceptions.RequestException:
        return False, False

server_ok, model_ok = check_ollama_health()
```

## When to Use This Skill

Use when:

- Migrating from OpenAI to local LLMs
- Using LangChain, LlamaIndex, or other OpenAI-based tools
- You prefer the OpenAI client interface
- Building applications that may switch between OpenAI and Ollama

## Cross-References

- `bazzite-ai-jupyter:ollama` - Native Ollama library (more features)
- `bazzite-ai-jupyter:chat` - Direct REST API access
