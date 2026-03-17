---
name: text-generation-inference
description: Deploy LLMs with Hugging Face Text Generation Inference. Configure quantization, continuous batching, and tensor parallelism. Use for production LLM serving, high-throughput inference, and model deployment.
---

# Text Generation Inference (TGI)

Expert guidance for Hugging Face's production LLM inference server.

## Installation

### Docker

```bash
# Basic GPU deployment
docker run --gpus all -p 8080:80 \
  -v /path/to/models:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct

# With quantization
docker run --gpus all -p 8080:80 \
  -v /path/to/models:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-8B-Instruct \
  --quantize bitsandbytes-nf4

# Multi-GPU
docker run --gpus all -p 8080:80 \
  -v /path/to/models:/data \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-70B-Instruct \
  --num-shard 4
```

### Docker Compose

```yaml
services:
  tgi:
    image: ghcr.io/huggingface/text-generation-inference:latest
    ports:
      - "8080:80"
    volumes:
      - ./models:/data
    environment:
      - HUGGING_FACE_HUB_TOKEN=${HF_TOKEN}
    command: >
      --model-id meta-llama/Llama-3.1-8B-Instruct
      --max-input-length 4096
      --max-total-tokens 8192
      --max-batch-prefill-tokens 4096
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: all
              capabilities: [gpu]
```

## Server Options

```bash
text-generation-launcher \
  --model-id meta-llama/Llama-3.1-8B-Instruct \
  --port 8080 \
  --max-input-length 4096 \
  --max-total-tokens 8192 \
  --max-batch-prefill-tokens 4096 \
  --max-batch-total-tokens 32768 \
  --max-concurrent-requests 128 \
  --waiting-served-ratio 0.3 \
  --dtype float16 \
  --trust-remote-code
```

## Quantization Options

```bash
# BitsAndBytes 4-bit
--quantize bitsandbytes-nf4
--quantize bitsandbytes-fp4

# GPTQ
--quantize gptq

# AWQ
--quantize awq

# EETQ (efficient 8-bit)
--quantize eetq

# FP8
--quantize fp8
```

## API Usage

### Python Client

```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="http://localhost:8080")

# Generate text
response = client.text_generation(
    "What is machine learning?",
    max_new_tokens=256,
    temperature=0.7,
    top_p=0.9,
    stop_sequences=["</s>"]
)
print(response)

# Chat
messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What is Python?"}
]
response = client.chat_completion(messages, max_tokens=500)
print(response.choices[0].message.content)

# Streaming
for token in client.text_generation(
    "Once upon a time",
    max_new_tokens=100,
    stream=True
):
    print(token, end="")
```

### OpenAI-Compatible

```python
from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:8080/v1",
    api_key="-"
)

response = client.chat.completions.create(
    model="tgi",
    messages=[
        {"role": "user", "content": "Hello!"}
    ],
    max_tokens=100,
    temperature=0.7
)
print(response.choices[0].message.content)
```

### REST API

```bash
# Generate
curl http://localhost:8080/generate \
  -H "Content-Type: application/json" \
  -d '{
    "inputs": "What is AI?",
    "parameters": {
      "max_new_tokens": 100,
      "temperature": 0.7,
      "top_p": 0.9
    }
  }'

# Chat
curl http://localhost:8080/v1/chat/completions \
  -H "Content-Type: application/json" \
  -d '{
    "model": "tgi",
    "messages": [{"role": "user", "content": "Hello"}],
    "max_tokens": 100
  }'

# Health check
curl http://localhost:8080/health
curl http://localhost:8080/info
```

## Embedding Support

```python
from huggingface_hub import InferenceClient

client = InferenceClient(model="http://localhost:8080")

# Single embedding
embedding = client.feature_extraction("Hello world")

# Batch embeddings
embeddings = client.feature_extraction([
    "First sentence",
    "Second sentence"
])
```

## Speculative Decoding

```bash
# Use draft model for faster generation
docker run --gpus all -p 8080:80 \
  ghcr.io/huggingface/text-generation-inference:latest \
  --model-id meta-llama/Llama-3.1-70B-Instruct \
  --speculative-model meta-llama/Llama-3.1-8B-Instruct \
  --num-speculative-tokens 4
```

## Performance Tuning

```bash
# Memory optimization
--max-batch-prefill-tokens 4096
--max-batch-total-tokens 32768
--max-concurrent-requests 64

# Latency optimization
--max-batch-size 1
--max-waiting-tokens 1

# Throughput optimization
--max-batch-size 32
--waiting-served-ratio 0.3
```

## Kubernetes Deployment

```yaml
apikind: Deployment
metadata:
  name: tgi
spec:
  replicas: 1
  selector:
    matchLabels:
      app: tgi
  template:
    metadata:
      labels:
        app: tgi
    spec:
      containers:
        - name: tgi
          image: ghcr.io/huggingface/text-generation-inference:latest
          ports:
            - containerPort: 80
          args:
            - --model-id
            - meta-llama/Llama-3.1-8B-Instruct
            - --max-input-length
            - "4096"
          resources:
            limits:
              nvidia.com/gpu: 1
              memory: 32Gi
          env:
            - name: HUGGING_FACE_HUB_TOKEN
              valueFrom:
                secretKeyRef:
                  name: hf-token
                  key: token
          volumeMounts:
            - name: model-cache
              mountPath: /data
      volumes:
        - name: model-cache
          persistentVolumeClaim:
            claimName: model-cache-pvc
```

## Monitoring

```bash
# Prometheus metrics
curl http://localhost:8080/metrics

# Key metrics:
# tgi_request_duration_seconds
# tgi_request_count
# tgi_queue_size
# tgi_batch_size
```

## Resources

- [TGI Documentation](https://huggingface.co/docs/text-generation-inference)
- [TGI GitHub](https://github.com/huggingface/text-generation-inference)
- [Supported Models](https://huggingface.co/docs/text-generation-inference/supported_models)
