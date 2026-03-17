---
name: lora
description: Parameter-efficient fine-tuning with Low-Rank Adaptation (LoRA). Use when fine-tuning large language models with limited GPU memory, creating task-specific adapters, or when you need to train multiple specialized models from a single base.
---

# Using LoRA for Fine-tuning

LoRA (Low-Rank Adaptation) enables efficient fine-tuning by freezing pretrained weights and injecting small trainable matrices into transformer layers. This reduces trainable parameters to ~0.1% of the original model while maintaining performance.

## Table of Contents

- [Core Concepts](#core-concepts)
- [Basic Setup](#basic-setup)
- [Configuration Parameters](#configuration-parameters)
- [QLoRA (Quantized LoRA)](#qlora-quantized-lora)
- [Training Patterns](#training-patterns)
- [Saving and Loading](#saving-and-loading)
- [Merging Adapters](#merging-adapters)
- [Best Practices](#best-practices)

## Core Concepts

### How LoRA Works

Instead of updating all weights during fine-tuning, LoRA decomposes weight updates into low-rank matrices:

```
W' = W + BA
```

Where:
- `W` is the frozen pretrained weight matrix (d × k)
- `B` is a trainable matrix (d × r)
- `A` is a trainable matrix (r × k)
- `r` is the rank, much smaller than d and k

The key insight: weight updates during fine-tuning have low intrinsic rank, so we can represent them efficiently with smaller matrices.

### Why Use LoRA

| Aspect | Full Fine-tuning | LoRA |
|--------|------------------|------|
| Trainable params | 100% | ~0.1-1% |
| Memory usage | High | Low |
| Adapter size | Full model | ~3-100 MB |
| Training speed | Slower | Faster |
| Multiple tasks | Separate models | Swap adapters |

## Basic Setup

### Installation

```bash
pip install peft transformers accelerate
```

### Minimal Example

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from peft import LoraConfig, get_peft_model, TaskType
import torch

# Load base model
model_name = "meta-llama/Llama-3.2-1B"
model = AutoModelForCausalLM.from_pretrained(
    model_name,
    torch_dtype=torch.bfloat16,
    device_map="auto",
)
tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

# Configure LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

# Apply LoRA
model = get_peft_model(model, lora_config)
model.print_trainable_parameters()
# trainable params: 3,407,872 || all params: 1,238,300,672 || trainable%: 0.28%
```

## Configuration Parameters

### LoraConfig Options

```python
from peft import LoraConfig, TaskType

config = LoraConfig(
    # Core parameters
    r=16,                          # Rank of update matrices
    lora_alpha=32,                 # Scaling factor (alpha/r applied to updates)
    target_modules=["q_proj", "v_proj"],  # Layers to adapt

    # Regularization
    lora_dropout=0.05,             # Dropout on LoRA layers
    bias="none",                   # "none", "all", or "lora_only"

    # Task configuration
    task_type=TaskType.CAUSAL_LM,  # CAUSAL_LM, SEQ_CLS, SEQ_2_SEQ_LM, TOKEN_CLS

    # Advanced
    modules_to_save=None,          # Additional modules to train (e.g., ["lm_head"])
    layers_to_transform=None,      # Specific layer indices to adapt
    use_rslora=False,              # Rank-stabilized LoRA scaling
    use_dora=False,                # Weight-Decomposed LoRA
)
```

### Target Modules by Architecture

```python
# Llama, Mistral, Qwen
target_modules = ["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]

# GPT-2, GPT-J
target_modules = ["c_attn", "c_proj", "c_fc"]

# BERT, RoBERTa
target_modules = ["query", "key", "value", "dense"]

# Falcon
target_modules = ["query_key_value", "dense", "dense_h_to_4h", "dense_4h_to_h"]

# Phi
target_modules = ["q_proj", "k_proj", "v_proj", "dense", "fc1", "fc2"]
```

### Finding Target Modules

```python
# Print all linear layer names
from peft.utils import get_peft_model_state_dict

def find_target_modules(model):
    linear_modules = set()
    for name, module in model.named_modules():
        if isinstance(module, torch.nn.Linear):
            # Get the last part of the name (e.g., "q_proj" from "model.layers.0.self_attn.q_proj")
            layer_name = name.split(".")[-1]
            linear_modules.add(layer_name)
    return list(linear_modules)

print(find_target_modules(model))
```

## QLoRA (Quantized LoRA)

QLoRA combines 4-bit quantization with LoRA, enabling fine-tuning of large models on consumer GPUs.

### Setup

```python
from transformers import AutoModelForCausalLM, BitsAndBytesConfig
from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
import torch

# 4-bit quantization config
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # Normalized float 4-bit
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,       # Nested quantization
)

# Load quantized model
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-3B",
    quantization_config=bnb_config,
    device_map="auto",
)

# Prepare for k-bit training
model = prepare_model_for_kbit_training(model)

# Apply LoRA
lora_config = LoraConfig(
    r=16,
    lora_alpha=32,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"],
    lora_dropout=0.05,
    bias="none",
    task_type=TaskType.CAUSAL_LM,
)

model = get_peft_model(model, lora_config)
```

### Memory Requirements

| Model Size | Full FT (16-bit) | LoRA (16-bit) | QLoRA (4-bit) |
|------------|------------------|---------------|---------------|
| 7B         | ~60 GB           | ~16 GB        | ~6 GB         |
| 13B        | ~104 GB          | ~28 GB        | ~10 GB        |
| 70B        | ~560 GB          | ~160 GB       | ~48 GB        |

## Training Patterns

### With Hugging Face Trainer

```python
from transformers import TrainingArguments, Trainer, DataCollatorForLanguageModeling
from datasets import load_dataset

# Prepare dataset
dataset = load_dataset("tatsu-lab/alpaca", split="train")

def format_prompt(example):
    if example["input"]:
        text = f"### Instruction:\n{example['instruction']}\n\n### Input:\n{example['input']}\n\n### Response:\n{example['output']}"
    else:
        text = f"### Instruction:\n{example['instruction']}\n\n### Response:\n{example['output']}"
    return {"text": text}

dataset = dataset.map(format_prompt)

def tokenize(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        max_length=512,
        padding=False,
    )

tokenized = dataset.map(tokenize, batched=True, remove_columns=dataset.column_names)

# Training arguments (note higher learning rate)
training_args = TrainingArguments(
    output_dir="./lora-output",
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    learning_rate=2e-4,              # Higher than full fine-tuning
    bf16=True,
    logging_steps=10,
    save_steps=500,
    warmup_ratio=0.03,
    gradient_checkpointing=True,
    optim="adamw_torch_fused",
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized,
    data_collator=DataCollatorForLanguageModeling(tokenizer, mlm=False),
)

trainer.train()
```

### With SFTTrainer (TRL)

```python
from trl import SFTTrainer, SFTConfig

sft_config = SFTConfig(
    output_dir="./sft-lora",
    max_seq_length=1024,
    per_device_train_batch_size=4,
    gradient_accumulation_steps=4,
    num_train_epochs=1,
    learning_rate=2e-4,
    bf16=True,
    logging_steps=10,
    gradient_checkpointing=True,
)

trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=dataset,
    tokenizer=tokenizer,
    peft_config=lora_config,      # Pass config directly, SFTTrainer applies it
    dataset_text_field="text",
)

trainer.train()
```

### Classification Task

```python
from transformers import AutoModelForSequenceClassification
from peft import LoraConfig, get_peft_model, TaskType

model = AutoModelForSequenceClassification.from_pretrained(
    "bert-base-uncased",
    num_labels=2,
)

lora_config = LoraConfig(
    r=8,
    lora_alpha=16,
    target_modules=["query", "value"],
    lora_dropout=0.1,
    bias="none",
    task_type=TaskType.SEQ_CLS,
    modules_to_save=["classifier"],  # Train classification head fully
)

model = get_peft_model(model, lora_config)
```

## Saving and Loading

### Save Adapter

```python
# Save only LoRA weights (small file)
model.save_pretrained("./my-lora-adapter")
tokenizer.save_pretrained("./my-lora-adapter")

# Push to Hub
model.push_to_hub("username/my-lora-adapter")
```

### Load Adapter

```python
from peft import PeftModel
from transformers import AutoModelForCausalLM

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1B",
    torch_dtype=torch.bfloat16,
    device_map="auto",
)

# Load adapter
model = PeftModel.from_pretrained(base_model, "./my-lora-adapter")

# For inference
model.eval()
```

### Switch Between Adapters

```python
# Load multiple adapters
model.load_adapter("./adapter-1", adapter_name="task1")
model.load_adapter("./adapter-2", adapter_name="task2")

# Switch active adapter
model.set_adapter("task1")
output = model.generate(**inputs)

model.set_adapter("task2")
output = model.generate(**inputs)

# Disable adapter (use base model)
with model.disable_adapter():
    output = model.generate(**inputs)
```

## Merging Adapters

Merge LoRA weights into the base model for deployment without adapter overhead.

```python
from peft import PeftModel

# Load base model
base_model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Llama-3.2-1B",
    torch_dtype=torch.bfloat16,
    device_map="cpu",  # Merge on CPU to avoid memory issues
)

# Load adapter
model = PeftModel.from_pretrained(base_model, "./my-lora-adapter")

# Merge and unload
merged_model = model.merge_and_unload()

# Save merged model
merged_model.save_pretrained("./merged-model")
tokenizer.save_pretrained("./merged-model")

# Push merged model to Hub
merged_model.push_to_hub("username/my-merged-model")
```

## Best Practices

1. **Start with r=16**: Scale up to 32 or 64 if the model underfits, down to 8 if overfitting or memory-constrained

2. **Set lora_alpha = 2 × r**: This is a common heuristic; the effective scaling is `alpha/r`

3. **Target all attention and MLP layers**: For best results on LLMs, include gate/up/down projections:
   ```python
   target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"]
   ```

4. **Use higher learning rate**: 2e-4 is typical for LoRA vs 2e-5 for full fine-tuning

5. **Enable gradient checkpointing**: Reduces memory at cost of ~20% slower training:
   ```python
   model.gradient_checkpointing_enable()
   ```

6. **Use QLoRA for large models**: Essential for fine-tuning 7B+ models on consumer GPUs

7. **Keep dropout low**: 0.05 is usually sufficient; higher values may hurt performance

8. **Save checkpoints frequently**: LoRA adapters are small, so save often

9. **Evaluate on base model too**: Ensure adapter doesn't degrade base capabilities

10. **Consider modules_to_save for task heads**: For classification, train the classifier fully:
    ```python
    modules_to_save=["classifier", "score"]
    ```

## References

See `reference/` for detailed documentation:
- `advanced-techniques.md` - DoRA, rsLoRA, adapter composition, and debugging
