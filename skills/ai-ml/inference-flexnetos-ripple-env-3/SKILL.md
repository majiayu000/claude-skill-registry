---
name: AI Inference & Model Serving
description: "AI model inference and serving. Activate when: (1) Setting up LocalAI or vLLM, (2) Configuring model serving, (3) Working with GGUF/GGML models, (4) Implementing inference pipelines, or (5) Optimizing model performance."
---

# AI Inference & Model Serving

## Overview

This skill covers local AI inference using LocalAI, vLLM, and other model serving frameworks for running LLMs and other AI models.

## LocalAI

### Installation

```bash
# Docker (recommended)
docker run -p 8080:8080 \
  -v $PWD/models:/models \
  localai/localai:latest-cpu

# With GPU support
docker run --gpus all -p 8080:8080 \
  -v $PWD/models:/models \
  localai/localai:latest-gpu-nvidia-cuda-12
```

### Model Configuration

```yaml
# models/llama.yaml
name: llama
backend: llama-cpp
parameters:
  model: /models/llama-2-7b-chat.Q4_K_M.gguf
  temperature: 0.7
  top_p: 0.9
  top_k: 40
  context_size: 4096
  threads: 4
  gpu_layers: 35  # Offload layers to GPU

# Template for chat
template:
  chat: |
    {{.System}}
    {{range .Messages}}
    {{if eq .Role "user"}}User: {{.Content}}
    {{else if eq .Role "assistant"}}Assistant: {{.Content}}
    {{end}}
    {{end}}
    Assistant:
```

### API Usage

```bash
# Chat completion (OpenAI-compatible)
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama",
    "messages": [
      {"role": "system", "content": "You are a helpful assistant."},
      {"role": "user", "content": "Hello!"}
    ]
  }'

# Text completion
curl http://localhost:8080/v1/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "llama",
    "prompt": "Once upon a time",
    "max_tokens": 100
  }'

# Embeddings
curl http://localhost:8080/v1/embeddings \
  -H "Content-Type: application/json" \
  -d '{
    "model": "text-embedding-ada-002",
    "input": "Hello world"
  }'
```

### Python Client

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="not-needed"  # LocalAI doesn't require API key
)

response = client.chat.completions.create(
    model="llama",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Explain quantum computing."}
    ],
    temperature=0.7,
    max_tokens=500
)

print(response.choices[0].message.content)
```

## vLLM

### Installation

```bash
pip install vllm

# Or with specific CUDA version
pip install vllm --extra-index-url https://download.pytorch.org/whl/cu121
```

### Server Mode

```bash
# Start server
python -m vllm.entrypoints.openai.api_server \
  --model meta-llama/Llama-2-7b-chat-hf \
  --port 8000 \
  --tensor-parallel-size 1

# With quantization
python -m vllm.entrypoints.openai.api_server \
  --model TheBloke/Llama-2-7B-Chat-AWQ \
  --quantization awq
```

### Python API

```python
from vllm import LLM, SamplingParams

# Initialize model
llm = LLM(
    model="meta-llama/Llama-2-7b-chat-hf",
    tensor_parallel_size=1,
    gpu_memory_utilization=0.9
)

# Sampling parameters
sampling_params = SamplingParams(
    temperature=0.7,
    top_p=0.9,
    max_tokens=256
)

# Generate
prompts = ["Hello, my name is", "The capital of France is"]
outputs = llm.generate(prompts, sampling_params)

for output in outputs:
    print(f"Prompt: {output.prompt}")
    print(f"Generated: {output.outputs[0].text}")
```

## GGUF/GGML Models

### Model Formats

| Format | Description |
|--------|-------------|
| GGUF | New format, recommended |
| GGML | Legacy format |
| Q4_K_M | 4-bit quantization, medium quality |
| Q5_K_M | 5-bit quantization, better quality |
| Q8_0 | 8-bit quantization, near FP16 |
| F16 | Full 16-bit floating point |

### Quantization with llama.cpp

```bash
# Clone llama.cpp
git clone https://github.com/ggerganov/llama.cpp
cd llama.cpp && make

# Convert to GGUF
python convert.py /path/to/hf-model --outfile model.gguf

# Quantize
./quantize model.gguf model-q4_k_m.gguf Q4_K_M

# Run inference
./main -m model-q4_k_m.gguf \
  -p "Hello, how are you?" \
  -n 256 \
  --temp 0.7
```

## Model Optimization

### GPU Memory Management

```python
# vLLM memory management
llm = LLM(
    model="model-name",
    gpu_memory_utilization=0.9,  # Use 90% of GPU memory
    max_model_len=4096,          # Max context length
    enforce_eager=False          # Use CUDA graphs
)
```

### Batching Strategies

```python
# Continuous batching (vLLM default)
# Dynamically batch requests for better throughput

# Static batching
sampling_params = SamplingParams(max_tokens=256)
outputs = llm.generate(
    prompts,  # List of prompts
    sampling_params,
    use_tqdm=True
)
```

### Speculative Decoding

```python
# Use draft model for faster inference
llm = LLM(
    model="meta-llama/Llama-2-70b-chat-hf",
    speculative_model="meta-llama/Llama-2-7b-chat-hf",
    num_speculative_tokens=5
)
```

## Monitoring & Metrics

### Prometheus Metrics

```yaml
# LocalAI exposes /metrics endpoint
# docker-compose.yaml
services:
  localai:
    image: localai/localai:latest
    ports:
      - "8080:8080"
    environment:
      - METRICS=true

  prometheus:
    image: prom/prometheus
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml
```

### Key Metrics

| Metric | Description |
|--------|-------------|
| `request_latency` | Time to generate response |
| `tokens_per_second` | Generation speed |
| `queue_depth` | Pending requests |
| `gpu_memory_used` | GPU memory usage |
| `batch_size` | Current batch size |

## Feature Flags (A/B Testing)

```toml
# pixi.toml feature flags
[feature.inference-localai]
[feature.inference-localai.dependencies]
# LocalAI specific deps

[feature.inference-vllm]
[feature.inference-vllm.dependencies]
vllm = ">=0.3.0"
torch = ">=2.0"

[environments]
default = { features = ["inference-localai"] }
vllm = { features = ["inference-vllm"] }
```

## External Links

- [LocalAI Documentation](https://localai.io/docs/)
- [vLLM Documentation](https://docs.vllm.ai/)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)
- [GGUF Specification](https://github.com/ggerganov/ggml/blob/master/docs/gguf.md)
- [Hugging Face Model Hub](https://huggingface.co/models)
