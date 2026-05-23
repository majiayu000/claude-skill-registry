---
name: ollama
description: Run local LLMs with Ollama. Deploy, manage, and interact with open-source models locally. Use for private AI, offline inference, and local development without API costs.
---

# Ollama

Expert guidance for running local LLMs with Ollama.

## Triggers

Use this skill when:
- Running LLMs locally for privacy or cost savings
- Setting up offline AI inference
- Managing local model deployments
- Working with open-source models (Llama, Mistral, etc.)
- Developing AI applications without cloud API costs
- Keywords: ollama, local llm, offline, self-hosted, llama, mistral, local model

## Installation

```bash
# macOS
brew install ollama

# Linux
curl -fsSL https://ollama.com/install.sh | sh

# Windows
# Download from https://ollama.com/download
```

## Start Server

```bash
# Start Ollama service
ollama serve

# Runs on http://localhost:11434
```

## Model Management

```bash
# Pull models
ollama pull llama3.1
ollama pull llama3.1:70b
ollama pull mistral
ollama pull codellama
ollama pull phi3
ollama pull gemma2

# List models
ollama list

# Show model info
ollama show llama3.1

# Remove model
ollama rm llama3.1

# Copy model
ollama cp llama3.1 my-llama

# Run model interactively
ollama run llama3.1
```

## API Usage

### Python

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1",
        "prompt": "What is Python?",
        "stream": False
    }
)
print(response.json()["response"])
```

### Python with OpenAI SDK

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Required but unused
)

response = client.chat.completions.create(
    model="llama3.1",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is Python?"}
    ]
)
print(response.choices[0].message.content)
```

### Streaming

```python
import requests

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1",
        "prompt": "Write a poem",
        "stream": True
    },
    stream=True
)

for line in response.iter_lines():
    if line:
        import json
        data = json.loads(line)
        print(data.get("response", ""), end="", flush=True)
```

### Chat API

```python
import requests

response = requests.post(
    "http://localhost:11434/api/chat",
    json={
        "model": "llama3.1",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello!"}
        ]
    }
)
print(response.json()["message"]["content"])
```

### Embeddings

```python
response = requests.post(
    "http://localhost:11434/api/embeddings",
    json={
        "model": "llama3.1",
        "prompt": "Hello world"
    }
)
embedding = response.json()["embedding"]
```

## Custom Models (Modelfile)

### Create Custom Model

```dockerfile
# Modelfile
FROM llama3.1

# Set parameters
PARAMETER temperature 0.7
PARAMETER top_p 0.9
PARAMETER num_ctx 4096

# Set system prompt
SYSTEM """You are a helpful coding assistant specializing in Python.
Always provide code examples and explain your reasoning."""

# Set template (optional)
TEMPLATE """{{ if .System }}<|system|>
{{ .System }}<|end|>
{{ end }}{{ if .Prompt }}<|user|>
{{ .Prompt }}<|end|>
{{ end }}<|assistant|>
{{ .Response }}<|end|>"""
```

```bash
# Create model
ollama create my-coder -f Modelfile

# Run custom model
ollama run my-coder
```

### Import GGUF Models

```dockerfile
# Modelfile
FROM ./mistral-7b-instruct-v0.2.Q4_K_M.gguf

PARAMETER temperature 0.7
PARAMETER num_ctx 8192

TEMPLATE """[INST] {{ .Prompt }} [/INST]
{{ .Response }}"""
```

## Generation Parameters

```python
response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llama3.1",
        "prompt": "Hello",
        "options": {
            "temperature": 0.7,
            "top_p": 0.9,
            "top_k": 40,
            "num_predict": 256,
            "num_ctx": 4096,
            "repeat_penalty": 1.1,
            "seed": 42
        }
    }
)
```

## Vision Models

```python
import base64

# Encode image
with open("image.jpg", "rb") as f:
    image_data = base64.b64encode(f.read()).decode()

response = requests.post(
    "http://localhost:11434/api/generate",
    json={
        "model": "llava",
        "prompt": "What's in this image?",
        "images": [image_data]
    }
)
```

## LangChain Integration

```python
from langchain_community.llms import Ollama
from langchain_community.chat_models import ChatOllama

# LLM
llm = Ollama(model="llama3.1")
response = llm.invoke("What is Python?")

# Chat model
chat = ChatOllama(model="llama3.1")
response = chat.invoke([
    ("system", "You are helpful."),
    ("human", "Hello!")
])
```

## LlamaIndex Integration

```python
from llama_index.llms.ollama import Ollama
from llama_index.embeddings.ollama import OllamaEmbedding
from llama_index.core import Settings

Settings.llm = Ollama(model="llama3.1", request_timeout=120.0)
Settings.embed_model = OllamaEmbedding(model_name="llama3.1")
```

## Docker Deployment

```yaml
# docker-compose.yml
services:
  ollama:
    image: ollama/ollama:latest
    ports:
      - "11434:11434"
    volumes:
      - ollama_data:/root/.ollama
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]

volumes:
  ollama_data:
```

```bash
# Pull model in container
docker exec -it ollama ollama pull llama3.1
```

## Environment Variables

```bash
# Model storage location
OLLAMA_MODELS=/path/to/models

# Server host/port
OLLAMA_HOST=0.0.0.0:11434

# GPU settings
OLLAMA_NUM_GPU=1
CUDA_VISIBLE_DEVICES=0

# Memory settings
OLLAMA_MAX_LOADED_MODELS=2
```

## Popular Models

| Model | Size | Use Case |
|-------|------|----------|
| `llama3.1` | 8B | General purpose |
| `llama3.1:70b` | 70B | Complex reasoning |
| `mistral` | 7B | Fast, efficient |
| `codellama` | 7B-34B | Code generation |
| `phi3` | 3.8B | Small but capable |
| `gemma2` | 9B | Google's model |
| `llava` | 7B | Vision + language |
| `nomic-embed-text` | - | Embeddings |

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama/blob/main/README.md)
- [Ollama Model Library](https://ollama.com/library)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
