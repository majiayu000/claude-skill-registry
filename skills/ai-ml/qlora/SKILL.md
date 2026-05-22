---
name: qlora
description: Memory-efficient fine-tuning with 4-bit quantization and LoRA adapters. Use when fine-tuning large models (7B+) on consumer GPUs, when VRAM is limited, or when standard LoRA still exceeds memory. Builds on the lora skill.
---

# QLoRA: Quantized Low-Rank Adaptation

QLoRA enables fine-tuning of large language models on consumer GPUs by combining 4-bit quantization with LoRA adapters. A 65B model can be fine-tuned on a single 48GB GPU while matching 16-bit fine-tuning performance.

> **Prerequisites**: This skill assumes familiarity with LoRA. See the `lora` skill for LoRA fundamentals (LoraConfig, target_modules, training patterns).

## Table of Contents

- [Core Innovations](#core-innovations)
- [BitsAndBytesConfig Deep Dive](#bitsandbytesconfig-deep-dive)
- [Memory Requirements](#memory-requirements)
- [Complete Training Example](#complete-training-example)
- [Inference and Merging](#inference-and-merging)
- [Troubleshooting](#troubleshooting)
- [Best Practices](#best-practices)

## Core Innovations

QLoRA introduces three techniques that reduce memory usage without sacrificing performance:

### 4-bit NormalFloat (NF4)

NF4 is an information-theoretically optimal quantization data type for normally distributed weights. Neural network weights are typically normally distributed, making NF4 more efficient than standard 4-bit floats.

```
Storage: 4-bit NF4 (quantized weights)
Compute: 16-bit BF16 (dequantized for forward/backward pass)
```

The key insight: weights are stored in 4-bit but dequantized to bf16 for computation. Only the frozen base model is quantized; LoRA adapters remain in full precision.

**NF4 vs FP4:**

| Quantization | Description | Use Case |
|--------------|-------------|----------|
| `nf4` | Normalized Float 4-bit, optimal for normal distributions | Default, recommended |
| `fp4` | Standard 4-bit float | Legacy, rarely needed |

### Double Quantization

Standard quantization requires storing scaling constants (typically fp32) for each quantization block. Double quantization quantizes these constants too:

```
First quantization:  weights → 4-bit + fp32 scaling constants
Double quantization: scaling constants → 8-bit + fp32 second-level constants
```

This saves approximately **0.37 bits per parameter**—significant for billion-parameter models:
- 7B model: ~325 MB savings
- 70B model: ~3.2 GB savings

### Paged Optimizers

During training, gradient checkpointing can cause memory spikes when processing long sequences. Paged optimizers use NVIDIA unified memory to automatically transfer optimizer states between GPU and CPU:

```
Normal training: OOM on memory spike
Paged optimizers: GPU ↔ CPU transfer handles spikes gracefully
```

This is handled automatically by bitsandbytes when using 4-bit training.

## BitsAndBytesConfig Deep Dive

### All Parameters Explained

```python
from transformers import BitsAndBytesConfig
import torch

bnb_config = BitsAndBytesConfig(
    # Core 4-bit settings
    load_in_4bit=True,              # Enable 4-bit quantization
    bnb_4bit_quant_type="nf4",      # "nf4" (recommended) or "fp4"

    # Double quantization
    bnb_4bit_use_double_quant=True, # Quantize the quantization constants

    # Compute precision
    bnb_4bit_compute_dtype=torch.bfloat16,  # Dequantize to this dtype for compute

    # Optional: specific storage type (usually auto-detected)
    bnb_4bit_quant_storage=torch.uint8,     # Storage dtype for quantized weights
)
```

### Compute Dtype Selection

| Dtype | Hardware | Notes |
|-------|----------|-------|
| `torch.bfloat16` | Ampere+ (RTX 30xx, A100) | Recommended, faster |
| `torch.float16` | Older GPUs (V100, RTX 20xx) | Use if bf16 not supported |
| `torch.float32` | Any | Slower, only for debugging |

Check bf16 support:
```python
import torch
print(torch.cuda.is_bf16_supported())  # True on Ampere+
```

### Comparison: Quantization Options

```python
# Recommended: NF4 + double quant + bf16
optimal_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# Maximum memory savings (slightly slower)
max_savings_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.float16,  # fp16 uses less memory than bf16
)

# 8-bit alternative (less compression, sometimes more stable)
eight_bit_config = BitsAndBytesConfig(
    load_in_8bit=True,
)
```

## Memory Requirements

| Model Size | Full Fine-tuning | LoRA (16-bit) | QLoRA (4-bit) |
|------------|------------------|---------------|---------------|
| 7B         | ~60 GB           | ~16 GB        | ~6 GB         |
| 13B        | ~104 GB          | ~28 GB        | ~10 GB        |
| 34B        | ~272 GB          | ~75 GB        | ~20 GB        |
| 70B        | ~560 GB          | ~160 GB       | ~48 GB        |

**Notes:**
- QLoRA memory includes model + optimizer states + activations
- Actual usage varies with batch size, sequence length, and gradient checkpointing
- Add ~20% buffer for safe operation

### GPU Recommendations

| GPU VRAM | Max Model Size (QLoRA) |
|----------|------------------------|
| 8 GB     | 7B (tight)             |
| 16 GB    | 7-13B                  |
| 24 GB    | 13-34B                 |
| 48 GB    | 34-70B                 |
| 80 GB    | 70B+ comfortably       |

## Complete Training Example

```python
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
)
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset
import torch

# 1. Quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_use_double_quant=True,
    bnb_4bit_compute_dtype=torch.bfloat16,
)

# 2. Load quantized model
model_name = "meta-llama/Llama-3.1-8B"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
    attn_implementation="flash_attention_2",  # Optional: faster attention
)

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right"

# 3. Prepare for k-bit training (critical step!)
model = prepare_model_for_kbit_training(model)

# 4. LoRA config (see lora skill for parameter details)
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM",
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# 5. Dataset
dataset = load_dataset("tatsu-lab/alpaca", split="train[:1000]")

def format_example(example):
    if example["input"]:
        return {"text": f"### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}"}
    return {"text": f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"}

dataset = dataset.map(format_example)

# 6. Training
sft_config = SFTConfig(
    output_dir="./qlora-output",
    max_seq_length=512,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    learning_rate=2e-4,
    bf16=True,
    logging_steps=10,
    save_steps=100,
    gradient_checkpointing=True,
    gradient_checkpointing_kwargs={"use_reentrant": False},
    optim="paged_adamw_8bit",  # Paged optimizer for memory efficiency
)

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=dataset,
    processing_class=tokenizer,
    dataset_text_field="text",
)

trainer.train()

# 7. Save adapter
model.save_pretrained("./qlora-adapter")
tokenizer.save_pretrained("./qlora-adapter")
```

## Inference and Merging

### Inference with Quantized Model

```python
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from peft import PeftModel
import torch

model_name = "meta-llama/Llama-3.1-8B"

# Load quantized base model
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16,
)

base_model = AutoModelForCausalLM.from_pretrained(
    model_name,
    quantization_config=bnb_config,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Load adapter
model = PeftModel.from_pretrained(base_model, "./qlora-adapter")
model.eval()

# Generate
inputs = tokenizer("### Instruction:\nExplain quantum computing.\n\n### Response:\n", return_tensors="pt").to(model.device)
outputs = model.generate(**inputs, max_new_tokens=256)
print(tokenizer.decode(outputs[0], skip_special_tokens=True))
```

### Merging to Full Precision

To merge QLoRA adapters into a full-precision model (for deployment without bitsandbytes):

```python
from transformers import AutoModelForCausalLM
from peft import PeftModel
import torch

# Load base model in full precision (on CPU to avoid OOM)
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.1-8B",
    torch_dtype=torch.bfloat16,
    device_map="cpu",
)

# Load adapter
model = PeftModel.from_pretrained(base_model, "./qlora-adapter")

# Merge and unload
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./merged-model")
```

**Note**: Merging requires enough RAM to hold the full-precision model. For 70B models, this means ~140GB RAM.

## Troubleshooting

### CUDA Version Issues

```bash
# Check CUDA version
nvcc --version
python -c "import torch; print(torch.version.cuda)"

# bitsandbytes requires CUDA 11.7+
# If version mismatch, reinstall:
pip uninstall bitsandbytes
pip install bitsandbytes --upgrade
```

### "cannot find libcudart" or Missing Library Errors

```bash
# Find CUDA installation
find /usr -name "libcudart*" 2>/dev/null

# Set environment variable
export LD_LIBRARY_PATH=/usr/local/cuda/lib64:$LD_LIBRARY_PATH

# Or for conda:
export LD_LIBRARY_PATH=$CONDA_PREFIX/lib:$LD_LIBRARY_PATH
```

### Slow Training

Common cause: compute dtype mismatch

```python
# Check if model is using expected dtype
for name, param in model.named_parameters():
    if param.requires_grad:
        print(f"{name}: {param.dtype}")
        break  # All LoRA params should match

# Ensure bf16 is used in training args if BitsAndBytesConfig uses bf16
# Mismatch causes constant dtype conversions
```

### Out of Memory

```python
# 1. Enable gradient checkpointing
model.gradient_checkpointing_enable()

# 2. Reduce batch size, increase accumulation
per_device_train_batch_size = 1
gradient_accumulation_steps = 16

# 3. Use paged optimizer
optim = "paged_adamw_8bit"

# 4. Reduce sequence length
max_seq_length = 256

# 5. Target fewer modules
target_modules = ["q_proj", "v_proj"]  # Minimal set
```

### Model Loads But Training Fails

```python
# Ensure prepare_model_for_kbit_training is called
from peft import prepare_model_for_kbit_training
model = prepare_model_for_kbit_training(model)  # Don't skip this!

# Enable input gradients if needed
model.enable_input_require_grads()
```

## Best Practices

1. **Always use `prepare_model_for_kbit_training`**: This enables gradient computation through the frozen quantized layers

2. **Match compute dtype with training precision**: If `bnb_4bit_compute_dtype=torch.bfloat16`, use `bf16=True` in training args

3. **Use paged optimizers for large models**: `optim="paged_adamw_8bit"` or `"paged_adamw_32bit"` handles memory spikes

4. **Start with NF4 + double quantization**: This is the recommended default; only change if debugging

5. **Gradient checkpointing is essential**: Always enable for QLoRA training to fit larger batch sizes

6. **Test inference before long training runs**: Load the model and generate a few tokens to catch configuration issues early

7. **Monitor GPU memory**: Use `nvidia-smi` or `torch.cuda.memory_summary()` to track actual usage

8. **Consider 8-bit for unstable training**: If 4-bit training shows instability, try `load_in_8bit=True` as a middle ground
