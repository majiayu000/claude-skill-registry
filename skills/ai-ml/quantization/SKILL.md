---
name: quantization
description: |
  Model quantization for efficient inference and training. Covers precision
  types (FP32, FP16, BF16, INT8, INT4), BitsAndBytes configuration, memory
  estimation, and performance tradeoffs.
---

# Model Quantization

## Overview

Quantization reduces model precision to save memory and speed up inference. A 7B model at FP32 requires ~28GB, but at 4-bit only ~4GB.

## Quick Reference

| Precision | Bits | Memory | Quality | Speed |
|-----------|------|--------|---------|-------|
| FP32 | 32 | 4x | Best | Slowest |
| FP16 | 16 | 2x | Excellent | Fast |
| BF16 | 16 | 2x | Excellent | Fast |
| INT8 | 8 | 1x | Good | Faster |
| INT4 | 4 | 0.5x | Acceptable | Fastest |

## Memory Estimation

```python
def estimate_memory(params_billions, precision_bits):
    """Estimate model memory in GB."""
    bytes_per_param = precision_bits / 8
    return params_billions * bytes_per_param

# Example: 7B model
model_size = 7  # billion parameters

print(f"FP32: {estimate_memory(7, 32):.1f} GB")  # 28 GB
print(f"FP16: {estimate_memory(7, 16):.1f} GB")  # 14 GB
print(f"INT8: {estimate_memory(7, 8):.1f} GB")   # 7 GB
print(f"INT4: {estimate_memory(7, 4):.1f} GB")   # 3.5 GB
```

## Measure Model Size

```python
def get_model_size(model):
    """Get model size in GB including buffers."""
    param_size = sum(p.numel() * p.element_size() for p in model.parameters())
    buffer_size = sum(b.numel() * b.element_size() for b in model.buffers())
    total = (param_size + buffer_size) / 1024**3
    return total

print(f"Model size: {get_model_size(model):.2f} GB")
```

## Load Model at Different Precisions

### FP32 (Default)

```python
from transformers import AutoModelForCausalLM

model_32bit = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    device_map="auto"
)

print(f"FP32 size: {get_model_size(model_32bit):.2f} GB")
```

### FP16 / BF16

```python
import torch

model_16bit = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    torch_dtype=torch.float16,  # or torch.bfloat16
    device_map="auto"
)

print(f"FP16 size: {get_model_size(model_16bit):.2f} GB")
```

### 8-bit Quantization

```python
from transformers import BitsAndBytesConfig

quantization_config = BitsAndBytesConfig(
    load_in_8bit=True
)

model_8bit = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    quantization_config=quantization_config,
    device_map="auto"
)

print(f"8-bit size: {get_model_size(model_8bit):.2f} GB")
```

### 4-bit Quantization (Recommended)

```python
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",  # NormalFloat4
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True  # Nested quantization
)

model_4bit = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    quantization_config=quantization_config,
    device_map="auto"
)

print(f"4-bit size: {get_model_size(model_4bit):.2f} GB")
```

## BitsAndBytesConfig Options

### 4-bit Configuration

```python
from transformers import BitsAndBytesConfig
import torch

config = BitsAndBytesConfig(
    load_in_4bit=True,

    # Quantization type
    bnb_4bit_quant_type="nf4",  # "nf4" or "fp4"

    # Compute dtype for dequantized weights
    bnb_4bit_compute_dtype=torch.bfloat16,

    # Double quantization (saves more memory)
    bnb_4bit_use_double_quant=True,
)
```

### Options Explained

| Option | Values | Effect |
|--------|--------|--------|
| `load_in_4bit` | True/False | Enable 4-bit |
| `bnb_4bit_quant_type` | "nf4", "fp4" | nf4 better for LLMs |
| `bnb_4bit_compute_dtype` | float16, bfloat16 | Computation precision |
| `bnb_4bit_use_double_quant` | True/False | Quantize quantization constants |

## Compare Precision Performance

```python
from transformers import pipeline
import time

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"

# Test message
messages = [{"role": "user", "content": "Explain quantum computing."}]

def benchmark(model, tokenizer, name):
    pipe = pipeline("text-generation", model=model, tokenizer=tokenizer)

    start = time.time()
    output = pipe(messages, max_new_tokens=100, return_full_text=False)
    elapsed = time.time() - start

    print(f"{name}:")
    print(f"  Time: {elapsed:.2f}s")
    print(f"  Size: {get_model_size(model):.2f} GB")
    print(f"  Output: {output[0]['generated_text'][:50]}...")
    print()

# Benchmark each precision
benchmark(model_32bit, tokenizer, "FP32")
benchmark(model_16bit, tokenizer, "FP16")
benchmark(model_8bit, tokenizer, "8-bit")
benchmark(model_4bit, tokenizer, "4-bit")
```

## Quantization for Training

### QLoRA Setup

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

# 4-bit base model
quantization_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True
)

model = AutoModelForCausalLM.from_pretrained(
    "TinyLlama/TinyLlama-1.1B-Chat-v1.0",
    quantization_config=quantization_config,
    device_map="auto"
)

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)

# Add LoRA adapters
lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["q_proj", "v_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
```

## Precision Comparison

| Precision | Memory | Quality | Training | Best For |
|-----------|--------|---------|----------|----------|
| FP32 | 4x | Perfect | Yes | Research, baselines |
| FP16 | 2x | Excellent | Yes | Standard training |
| BF16 | 2x | Excellent | Yes | Large models |
| INT8 | 1x | Good | Limited | Inference |
| INT4 | 0.5x | Acceptable | QLoRA | Memory-constrained |

## FP16 vs BF16

| Aspect | FP16 | BF16 |
|--------|------|------|
| Range | Smaller | Larger (like FP32) |
| Precision | Higher | Lower |
| Overflow risk | Higher | Lower |
| Hardware | All GPUs | Ampere+ |
| Best for | Inference | Training |

## 4-bit NF4 vs BF16 Comparison (Tested)

Based on experiments with Qwen3-4B-Thinking models:

### Comparison Results

| Method | Peak Memory | Final Loss | Quality |
|--------|-------------|------------|---------|
| 4-bit NF4 | ~5.7GB | 3.0742 | Excellent |
| BF16 | ~6.5GB | 3.0742 | Reference |

**Key Finding**: 4-bit NF4 achieves **identical final loss** with 11-15% memory savings.

### Pre-Quantized Models (Recommended)

Use pre-quantized models for faster loading:

```python
from unsloth import FastLanguageModel

# Pre-quantized (fast loading)
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit",  # -bnb-4bit suffix
    max_seq_length=1024,
    load_in_4bit=True,
)

# vs. On-demand quantization (slower)
model, tokenizer = FastLanguageModel.from_pretrained(
    "Qwen/Qwen3-4B-Thinking-2507",  # Full precision
    max_seq_length=1024,
    load_in_4bit=True,  # Quantize during load
)
```

### GPU Memory Recommendations

| GPU VRAM | Recommended | Notes |
|----------|-------------|-------|
| <12GB | 4-bit NF4 | Required for training |
| 12-16GB | 4-bit NF4 | Allows larger batches |
| >16GB | BF16 or 4-bit | Choose based on batch needs |

### Quality Preservation

4-bit NF4 preserves:
- Training convergence (identical final loss)
- Thinking tag structure (`<think>...</think>`)
- Response quality and coherence
- Model reasoning capabilities

## Troubleshooting

### Out of Memory

**Symptom:** CUDA OOM error

**Fix:**

```python
# Use 4-bit quantization
config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True
)
```

### Quality Degradation

**Symptom:** Poor model outputs after quantization

**Fix:**

- Use nf4 instead of fp4
- Try 8-bit instead of 4-bit
- Increase LoRA rank if fine-tuning

### Slow Loading

**Symptom:** Model takes long to load

**Fix:**

- Quantization happens at load time
- Use `device_map="auto"` for multi-GPU

## When to Use This Skill

Use when:

- Model doesn't fit in GPU memory
- Need faster inference
- Training with limited resources (QLoRA)
- Deploying to edge devices

## Cross-References

- `bazzite-ai-jupyter:qlora` - Advanced QLoRA experiments
- `bazzite-ai-jupyter:peft` - LoRA with quantization (QLoRA)
- `bazzite-ai-jupyter:finetuning` - Full fine-tuning
- `bazzite-ai-jupyter:sft` - SFT training with quantization
- `bazzite-ai-jupyter:inference` - Fast inference patterns
- `bazzite-ai-jupyter:transformers` - Model architecture
