---
name: mlx
description: Running and fine-tuning LLMs on Apple Silicon with MLX. Use when working with models locally on Mac, converting Hugging Face models to MLX format, fine-tuning with LoRA/QLoRA on Apple Silicon, or serving models via HTTP API.
---

# Using MLX for LLMs on Apple Silicon

MLX-LM is a Python package for running large language models on Apple Silicon, leveraging the MLX framework for optimized performance with unified memory architecture.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Installation](#installation)
- [Text Generation](#text-generation)
- [Interactive Chat](#interactive-chat)
- [Model Conversion](#model-conversion)
- [Quantization](#quantization)
- [Fine-tuning with LoRA](#fine-tuning-with-lora)
- [Serving Models](#serving-models)
- [Best Practices](#best-practices)
- [References](#references)

## Core Concepts

### Why MLX

| Aspect | PyTorch on Mac | MLX |
|--------|----------------|-----|
| Memory | Separate CPU/GPU copies | Unified memory, no copies |
| Optimization | Generic Metal backend | Apple Silicon native |
| Model loading | Slower, more memory | Lazy loading, efficient |
| Quantization | Limited support | Built-in 4/8-bit |

MLX arrays live in shared memory, accessible by both CPU and GPU without data transfer overhead.

### Supported Models

MLX-LM supports most popular architectures: Llama, Mistral, Qwen, Phi, Gemma, Cohere, and many more. Check the [mlx-community](https://huggingface.co/mlx-community) on Hugging Face for pre-converted models.

## Installation

```bash
pip install mlx-lm
```

Requires macOS 13.5+ and Apple Silicon (M1/M2/M3/M4).

## Text Generation

### Python API

```python
from mlx_lm import load, generate

# Load model (from HF hub or local path)
model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

# Generate text
response = generate(
    model,
    tokenizer,
    prompt="Explain quantum computing in simple terms:",
    max_tokens=256,
    temp=0.7,
)
print(response)
```

### Streaming Generation

```python
from mlx_lm import load, stream_generate

model, tokenizer = load("mlx-community/Mistral-7B-Instruct-v0.3-4bit")

prompt = "Write a haiku about programming:"
for response in stream_generate(model, tokenizer, prompt, max_tokens=100):
    print(response.text, end="", flush=True)
print()
```

### Batch Generation

```python
from mlx_lm import load, batch_generate

model, tokenizer = load("mlx-community/Qwen2.5-7B-Instruct-4bit")

prompts = [
    "What is machine learning?",
    "Explain neural networks:",
    "Define deep learning:",
]

responses = batch_generate(
    model,
    tokenizer,
    prompts,
    max_tokens=100,
)

for prompt, response in zip(prompts, responses):
    print(f"Q: {prompt}\nA: {response}\n")
```

### CLI Generation

```bash
# Basic generation
mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit \
    --prompt "Explain recursion:" \
    --max-tokens 256

# With sampling parameters
mlx_lm.generate --model mlx-community/Mistral-7B-Instruct-v0.3-4bit \
    --prompt "Write a poem about AI:" \
    --temp 0.8 \
    --top-p 0.95
```

## Interactive Chat

### CLI Chat

```bash
# Start chat REPL (context preserved between turns)
mlx_lm.chat --model mlx-community/Llama-3.2-3B-Instruct-4bit
```

### Python Chat

```python
from mlx_lm import load, generate

model, tokenizer = load("mlx-community/Llama-3.2-3B-Instruct-4bit")

messages = [
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "What's the capital of France?"},
]

prompt = tokenizer.apply_chat_template(
    messages,
    tokenize=False,
    add_generation_prompt=True
)

response = generate(model, tokenizer, prompt=prompt, max_tokens=256)
print(response)
```

## Model Conversion

Convert Hugging Face models to MLX format:

### CLI Conversion

```bash
# Convert with 4-bit quantization
mlx_lm.convert --hf-path meta-llama/Llama-3.2-3B-Instruct \
    -q  # Quantize to 4-bit

# With specific quantization
mlx_lm.convert --hf-path mistralai/Mistral-7B-Instruct-v0.3 \
    -q \
    --q-bits 8 \
    --q-group-size 64

# Upload to Hugging Face Hub
mlx_lm.convert --hf-path meta-llama/Llama-3.2-1B-Instruct \
    -q \
    --upload-repo your-username/Llama-3.2-1B-Instruct-4bit-mlx
```

### Python Conversion

```python
from mlx_lm import convert

convert(
    hf_path="meta-llama/Llama-3.2-3B-Instruct",
    mlx_path="./llama-3.2-3b-mlx",
    quantize=True,
    q_bits=4,
    q_group_size=64,
)
```

### Conversion Options

| Option | Default | Description |
|--------|---------|-------------|
| `--q-bits` | 4 | Quantization bits (4 or 8) |
| `--q-group-size` | 64 | Group size for quantization |
| `--dtype` | float16 | Data type for non-quantized weights |

## Quantization

MLX supports multiple quantization methods for different use cases:

| Method | Best For | Command |
|--------|----------|---------|
| Basic | Quick conversion | `mlx_lm.convert -q` |
| DWQ | Quality-preserving | `mlx_lm.dwq` |
| AWQ | Activation-aware | `mlx_lm.awq` |
| Dynamic | Per-layer precision | `mlx_lm.dynamic_quant` |
| GPTQ | Established method | `mlx_lm.gptq` |

### Quick Quantization

```bash
# 4-bit quantization during conversion
mlx_lm.convert --hf-path mistralai/Mistral-7B-v0.3 -q

# 8-bit for higher quality
mlx_lm.convert --hf-path mistralai/Mistral-7B-v0.3 -q --q-bits 8
```

For detailed coverage of each method, see `reference/quantization.md`.

## Fine-tuning with LoRA

MLX supports LoRA and QLoRA fine-tuning for efficient adaptation on Apple Silicon.

### Quick Start

```bash
# Prepare training data (JSONL format)
# {"text": "Your training text here"}
# or
# {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "..."}]}

# Fine-tune with LoRA
mlx_lm.lora --model mlx-community/Llama-3.2-3B-Instruct-4bit \
    --train \
    --data ./data \
    --iters 1000

# Generate with adapter
mlx_lm.generate --model mlx-community/Llama-3.2-3B-Instruct-4bit \
    --adapter-path ./adapters \
    --prompt "Your prompt here"
```

### Fuse Adapter into Model

```bash
# Merge LoRA weights into base model
mlx_lm.fuse --model mlx-community/Llama-3.2-3B-Instruct-4bit \
    --adapter-path ./adapters \
    --save-path ./fused-model

# Or export to GGUF
mlx_lm.fuse --model mlx-community/Llama-3.2-3B-Instruct-4bit \
    --adapter-path ./adapters \
    --export-gguf
```

For detailed LoRA configuration and training patterns, see `reference/fine-tuning.md`.

## Serving Models

### OpenAI-Compatible Server

```bash
# Start server
mlx_lm.server --model mlx-community/Llama-3.2-3B-Instruct-4bit --port 8080

# Use with OpenAI client
curl http://localhost:8080/v1/chat/completions \
    -H "Content-Type: application/json" \
    -d '{
        "model": "default",
        "messages": [{"role": "user", "content": "Hello!"}],
        "max_tokens": 256
    }'
```

### Python Client

```python
from openai import OpenAI

client = OpenAI(base_url="http://localhost:8080/v1", api_key="not-needed")

response = client.chat.completions.create(
    model="default",
    messages=[{"role": "user", "content": "Explain MLX in one sentence."}],
    max_tokens=100,
)
print(response.choices[0].message.content)
```

## Best Practices

1. **Use pre-quantized models**: Download from `mlx-community` on Hugging Face for immediate use

2. **Match quantization to your hardware**: M1/M2 with 8GB: use 4-bit; M2/M3 Pro/Max: 8-bit for quality

3. **Leverage unified memory**: Unlike CUDA, MLX models can exceed "GPU memory" by using swap (slower but works)

4. **Use streaming for UX**: `stream_generate` provides responsive output for interactive applications

5. **Cache prompt prefixes**: Use `mlx_lm.cache_prompt` for repeated prompts with varying suffixes

6. **Batch similar requests**: `batch_generate` is more efficient than sequential generation

7. **Start with 4-bit quantization**: Good quality/size tradeoff; upgrade to 8-bit if quality issues

8. **Fuse adapters for deployment**: After fine-tuning, fuse adapters for faster inference without loading separately

9. **Monitor memory with Activity Monitor**: Watch memory pressure to avoid swap thrashing

10. **Use chat templates**: Always apply `tokenizer.apply_chat_template()` for instruction-tuned models

## References

See `reference/` for detailed documentation:
- `quantization.md` - Detailed quantization methods and when to use each
- `fine-tuning.md` - Complete LoRA/QLoRA training guide with data formats and configuration
