---
name: localai
description: Run local AI models with LocalAI. Deploy OpenAI-compatible API for LLMs, embeddings, audio, and images. Use for self-hosted AI, offline inference, and privacy-focused AI deployments.
---

# LocalAI

Expert guidance for self-hosted OpenAI-compatible AI API.

## Triggers

Use this skill when:
- Running self-hosted AI models locally
- Deploying OpenAI-compatible APIs without cloud dependencies
- Setting up privacy-focused AI deployments
- Working with LocalAI for LLMs, embeddings, audio, or images
- Building offline AI inference systems
- Keywords: localai, self-hosted, openai compatible, local ai, offline, privacy, llm server

## Installation

### Docker

```bash
# Basic (CPU)
docker run -p 8080:8080 localai/localai:latest

# With GPU (CUDA)
docker run --gpus all -p 8080:8080 localai/localai:latest-gpu-nvidia-cuda-12

# With models directory
docker run -p 8080:8080 \
  -v /path/to/models:/models \
  localai/localai:latest
```

### Docker Compose

```yaml
services:
  localai:
    image: localai/localai:latest-gpu-nvidia-cuda-12
    ports:
      - "8080:8080"
    volumes:
      - ./models:/models
    environment:
      - THREADS=8
      - CONTEXT_SIZE=4096
      - DEBUG=true
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## Model Configuration

### YAML Model Definition

```yaml
# models/llama3.yaml
name: llama3
backend: llama-cpp
parameters:
  model: /models/llama-3-8b-instruct.gguf
  temperature: 0.7
  top_p: 0.9
  top_k: 40
  context_size: 4096
  threads: 8
  f16: true
  mmap: true
template:
  chat_message: |
    <|start_header_id|>{{.RoleName}}<|end_header_id|>

    {{.Content}}<|eot_id|>
  chat: |
    {{.Input}}
    <|start_header_id|>assistant<|end_header_id|>
```

### Embedding Model

```yaml
# models/embeddings.yaml
name: text-embedding
backend: bert-embeddings
parameters:
  model: /models/all-MiniLM-L6-v2
embeddings: true
```

### Whisper (Audio)

```yaml
# models/whisper.yaml
name: whisper-1
backend: whisper
parameters:
  model: /models/whisper-base.bin
  language: en
```

### Stable Diffusion

```yaml
# models/stablediffusion.yaml
name: stablediffusion
backend: stablediffusion
parameters:
  model: /models/sd-v1-5
step: 25
```

## API Usage

### OpenAI Python Client

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # LocalAI doesn't require API key
)

# Chat completion
response = client.chat.completions.create(
    model="llama3",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What is machine learning?"}
    ],
    temperature=0.7,
    max_tokens=500
)
print(response.choices[0].message.content)

# Streaming
stream = client.chat.completions.create(
    model="llama3",
    messages=[{"role": "user", "content": "Tell me a story"}],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="")
```

### Embeddings

```python
response = client.embeddings.create(
    model="text-embedding",
    input=["Hello world", "How are you?"]
)

embeddings = [e.embedding for e in response.data]
```

### Image Generation

```python
response = client.images.generate(
    model="stablediffusion",
    prompt="A beautiful sunset over mountains",
    n=1,
    size="512x512"
)

image_url = response.data[0].url
```

### Audio Transcription

```python
with open("audio.mp3", "rb") as f:
    response = client.audio.transcriptions.create(
        model="whisper-1",
        file=f
    )
print(response.text)
```

## Gallery Models

```bash
# List available models
curl http://localhost:8080/models/available

# Install from gallery
curl http://localhost:8080/models/apply -d '{
  "id": "huggingface://TheBloke/Llama-2-7B-Chat-GGUF/llama-2-7b-chat.Q4_K_M.gguf"
}'

# Or via config
curl http://localhost:8080/models/apply -d '{
  "url": "github:go-skynet/model-gallery/gpt4all-j.yaml"
}'
```

## Function Calling

```yaml
# models/llama3-functions.yaml
name: llama3-functions
backend: llama-cpp
parameters:
  model: /models/llama-3-8b-instruct.gguf
function:
  disable_no_action: false
  grammar_prefix: |
    <|start_header_id|>assistant<|end_header_id|>
```

```python
response = client.chat.completions.create(
    model="llama3-functions",
    messages=[{"role": "user", "content": "What's the weather in Paris?"}],
    tools=[{
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get weather for a city",
            "parameters": {
                "type": "object",
                "properties": {
                    "city": {"type": "string"}
                },
                "required": ["city"]
            }
        }
    }],
    tool_choice="auto"
)
```

## Performance Tuning

```yaml
# Environment variables
THREADS=8                    # Number of CPU threads
CONTEXT_SIZE=4096           # Context window size
F16=true                    # Use FP16
MMAP=true                   # Memory map models
GPU_LAYERS=35               # Layers to offload to GPU
TENSOR_SPLIT=0.5,0.5        # Multi-GPU split
```

### GPU Offloading

```yaml
# models/llama3-gpu.yaml
name: llama3
backend: llama-cpp
parameters:
  model: /models/llama-3-8b-instruct.gguf
  gpu_layers: 35
  main_gpu: 0
  tensor_split: ""
```

## Kubernetes Deployment

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: localai
spec:
  replicas: 1
  selector:
    matchLabels:
      app: localai
  template:
    metadata:
      labels:
        app: localai
    spec:
      containers:
        - name: localai
          image: localai/localai:latest-gpu-nvidia-cuda-12
          ports:
            - containerPort: 8080
          resources:
            limits:
              nvidia.com/gpu: 1
          volumeMounts:
            - name: models
              mountPath: /models
          env:
            - name: THREADS
              value: "8"
      volumes:
        - name: models
          persistentVolumeClaim:
            claimName: models-pvc
```

## Resources

- [LocalAI Documentation](https://localai.io/docs/)
- [LocalAI GitHub](https://github.com/mudler/LocalAI)
- [Model Gallery](https://localai.io/models/)
