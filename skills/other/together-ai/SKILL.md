---
name: together-ai
description: |
  Cloud platform for running open-source AI models. Provides inference APIs for LLMs,
  image models, and embedding models. Supports fine-tuning on custom data, OpenAI-compatible
  API format, and competitive pricing for open-source model hosting.
license: Apache-2.0
compatibility: 'python 3.8+, typescript/node 18+, any OpenAI-compatible client'
metadata:
  author: terminal-skills
  version: 1.0.0
  category: data-ai
  tags:
    - llm-hosting
    - open-source-models
    - fine-tuning
    - embeddings
    - inference-api
---

# Together AI

## Installation

```bash
# Install Together Python client
pip install together

# Set API key
export TOGETHER_API_KEY="xxxxxxxxxxxx"
```

## Chat Completions (OpenAI-Compatible)

```python
# chat_completions.py — Use Together AI with the OpenAI SDK
from openai import OpenAI

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key="your-together-api-key",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-70B-Instruct-Turbo",
    messages=[
        {"role": "system", "content": "You are a helpful coding assistant."},
        {"role": "user", "content": "Write a Python function to merge two sorted lists."},
    ],
    max_tokens=500,
    temperature=0.7,
)
print(response.choices[0].message.content)
```

## Together Python SDK

```python
# together_sdk.py — Use the native Together SDK for additional features
import together

client = together.Together()

# Chat completion
response = client.chat.completions.create(
    model="mistralai/Mixtral-8x7B-Instruct-v0.1",
    messages=[{"role": "user", "content": "Explain transformers architecture."}],
    max_tokens=300,
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="meta-llama/Llama-3.1-8B-Instruct-Turbo",
    messages=[{"role": "user", "content": "Write a haiku about coding"}],
    stream=True,
)
for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
```

## Embeddings

```python
# embeddings.py — Generate embeddings for semantic search and RAG
from openai import OpenAI

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key="your-together-api-key",
)

response = client.embeddings.create(
    model="togethercomputer/m2-bert-80M-8k-retrieval",
    input=["What is machine learning?", "How does deep learning work?"],
)

for i, emb in enumerate(response.data):
    print(f"Text {i}: {len(emb.embedding)} dimensions")
```

## Image Generation

```python
# image_gen.py — Generate images with open-source models
import together
import base64

client = together.Together()

response = client.images.generate(
    model="stabilityai/stable-diffusion-xl-base-1.0",
    prompt="A serene Japanese garden at sunset, watercolor style",
    width=1024,
    height=1024,
    steps=30,
    n=1,
)

# Save the image
image_data = base64.b64decode(response.data[0].b64_json)
with open("garden.png", "wb") as f:
    f.write(image_data)
```

## Fine-Tuning

```python
# fine_tune.py — Fine-tune an open-source model on custom data
import together

client = together.Together()

# Upload training data (JSONL format)
file = client.files.upload(file="training_data.jsonl")
print(f"File ID: {file.id}")

# Start fine-tuning job
ft_job = client.fine_tuning.create(
    training_file=file.id,
    model="meta-llama/Llama-3.1-8B-Instruct-Reference",
    n_epochs=3,
    learning_rate=1e-5,
    batch_size=4,
    suffix="my-custom-model",
)
print(f"Job ID: {ft_job.id}")

# Check status
status = client.fine_tuning.retrieve(ft_job.id)
print(f"Status: {status.status}")
```

```jsonl
# training_data.jsonl — Training data format for fine-tuning
{"messages": [{"role": "system", "content": "You are a support agent."}, {"role": "user", "content": "How do I reset my password?"}, {"role": "assistant", "content": "Go to Settings > Security > Reset Password."}]}
{"messages": [{"role": "user", "content": "What are your hours?"}, {"role": "assistant", "content": "We're available 24/7 via chat and email."}]}
```

## JSON Mode

```python
# json_mode.py — Force structured JSON output from models
from openai import OpenAI

client = OpenAI(
    base_url="https://api.together.xyz/v1",
    api_key="your-together-api-key",
)

response = client.chat.completions.create(
    model="meta-llama/Llama-3.1-70B-Instruct-Turbo",
    messages=[{"role": "user", "content": "List 3 programming languages with their year of creation as JSON."}],
    response_format={"type": "json_object"},
)
print(response.choices[0].message.content)
```

## Key Concepts

- **OpenAI-compatible**: Use the OpenAI SDK by changing `base_url` — minimal migration effort
- **Open-source focus**: Hosts Llama, Mistral, Mixtral, DBRX, and other open models
- **Turbo models**: Together-optimized versions with faster inference and lower latency
- **Fine-tuning**: LoRA and full fine-tuning on hosted models with simple JSONL data format
- **Embeddings**: Dedicated embedding models for RAG and semantic search use cases
- **Pricing**: Per-token pricing, typically cheaper than proprietary model APIs
