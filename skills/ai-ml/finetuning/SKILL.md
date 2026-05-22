---
name: finetuning
description: |
  Model fine-tuning with PyTorch and HuggingFace Trainer. Covers dataset
  preparation, tokenization, training loops, TrainingArguments, SFTTrainer
  for instruction tuning, evaluation, and checkpoint management. Includes Unsloth recommendations.
---

# Model Fine-Tuning

## Overview

Fine-tuning adapts a pre-trained LLM to specific tasks by training on task-specific data. This skill covers both manual PyTorch training and HuggingFace's high-level Trainer API.

**Recommended**: For 2x faster training with less memory, use **Unsloth** (see `bazzite-ai-jupyter:sft`).

## Quick Reference

| Approach | Use Case | Speed |
|----------|----------|-------|
| **Unsloth + SFTTrainer** | **Recommended default** | **2x faster** |
| PyTorch Manual | Full control, custom training | Baseline |
| HuggingFace Trainer | Standard training, less code | Fast |
| SFTTrainer | Instruction/chat fine-tuning | Fast |

## Method Comparison

| Method | Learning Rate | Use Case |
|--------|---------------|----------|
| SFT | 2e-4 | Instruction tuning (first step) |
| GRPO | 1e-5 | RL with rewards |
| DPO | 5e-6 | Preference learning |
| RLOO | 1e-5 | RL with lower variance |
| Reward | 1e-5 | Reward model training |

## Unsloth Quickstart (Recommended)

```python
# CRITICAL: Import unsloth FIRST
import unsloth
from unsloth import FastLanguageModel, is_bf16_supported
from trl import SFTTrainer, SFTConfig

# Load model with Unsloth optimizations
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit",
    max_seq_length=1024,
    load_in_4bit=True,
)

# Apply LoRA
model = FastLanguageModel.get_peft_model(
    model, r=16, lora_alpha=16,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    use_gradient_checkpointing="unsloth",
)

# Train
trainer = SFTTrainer(
    model=model, tokenizer=tokenizer, train_dataset=dataset,
    args=SFTConfig(
        output_dir="./output",
        max_steps=100,
        learning_rate=2e-4,
        bf16=is_bf16_supported(),
        optim="adamw_8bit",
    ),
)
trainer.train()
```

See `bazzite-ai-jupyter:sft` for complete Unsloth patterns.

## Dataset Preparation

### Load from HuggingFace Hub

```python
from datasets import load_dataset

dataset = load_dataset("timdettmers/openassistant-guanaco")

train_data = dataset["train"]
val_data = dataset["test"]

print(f"Training samples: {len(train_data)}")
print(f"Validation samples: {len(val_data)}")
```

### Data Format

```python
# Example conversation format
example = train_data[0]
print(example["text"])

# Output:
# ### Human: What is Python?
# ### Assistant: Python is a programming language...
```

### Create Prompt Template

```python
def build_prompt(instruction, response=None):
    prompt = f"### Human: {instruction}\n### Assistant:"
    if response:
        prompt += f" {response}"
    return prompt

# For training
train_prompt = build_prompt("What is AI?", "AI is artificial intelligence.")

# For inference
inference_prompt = build_prompt("What is AI?")
```

## Tokenization

### Setup Tokenizer

```python
from transformers import AutoTokenizer

model_name = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
tokenizer = AutoTokenizer.from_pretrained(model_name)

# Ensure pad token exists
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
```

### Tokenize Dataset

```python
def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        padding="max_length",
        truncation=True,
        max_length=512,
        return_tensors="pt"
    )

tokenized_train = train_data.map(
    tokenize_function,
    batched=True,
    remove_columns=train_data.column_names
)

tokenized_train.set_format("torch")
```

## PyTorch Training (Manual)

### Setup Model

```python
import torch
from transformers import AutoModelForCausalLM

model = AutoModelForCausalLM.from_pretrained(
    model_name,
    device_map="auto",
    torch_dtype=torch.float16
)
```

### Training Configuration

```python
from dataclasses import dataclass

@dataclass
class TrainConfig:
    batch_size: int = 4
    learning_rate: float = 2e-5
    num_epochs: int = 3
    max_length: int = 512
    warmup_steps: int = 100
    weight_decay: float = 0.01
    output_dir: str = "./checkpoints"

cfg = TrainConfig()
```

### DataLoader

```python
from torch.utils.data import DataLoader

train_loader = DataLoader(
    tokenized_train,
    batch_size=cfg.batch_size,
    shuffle=True
)
```

### Optimizer and Scheduler

```python
from transformers import get_linear_schedule_with_warmup

optimizer = torch.optim.AdamW(
    model.parameters(),
    lr=cfg.learning_rate,
    weight_decay=cfg.weight_decay
)

total_steps = len(train_loader) * cfg.num_epochs

scheduler = get_linear_schedule_with_warmup(
    optimizer,
    num_warmup_steps=cfg.warmup_steps,
    num_training_steps=total_steps
)
```

### Training Loop

```python
from tqdm.auto import tqdm

model.train()
device = next(model.parameters()).device

for epoch in range(cfg.num_epochs):
    total_loss = 0
    progress = tqdm(train_loader, desc=f"Epoch {epoch+1}")

    for batch in progress:
        input_ids = batch["input_ids"].to(device)
        attention_mask = batch["attention_mask"].to(device)
        labels = input_ids.clone()

        optimizer.zero_grad()

        outputs = model(
            input_ids=input_ids,
            attention_mask=attention_mask,
            labels=labels
        )

        loss = outputs.loss
        loss.backward()

        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)

        optimizer.step()
        scheduler.step()

        total_loss += loss.item()
        progress.set_postfix({"loss": loss.item()})

    avg_loss = total_loss / len(train_loader)
    print(f"Epoch {epoch+1} - Average Loss: {avg_loss:.4f}")

    # Save checkpoint
    model.save_pretrained(f"{cfg.output_dir}/epoch_{epoch+1}")
```

## HuggingFace Trainer

### TrainingArguments

```python
from transformers import TrainingArguments, Trainer

training_args = TrainingArguments(
    output_dir="./checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    learning_rate=2e-5,
    weight_decay=0.01,
    warmup_steps=100,
    logging_steps=10,
    save_steps=500,
    evaluation_strategy="steps",
    eval_steps=500,
    load_best_model_at_end=True,
    fp16=True,  # Mixed precision
)
```

### Create Trainer

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
    eval_dataset=tokenized_val,
    tokenizer=tokenizer,
)
```

### Train and Evaluate

```python
# Train
train_result = trainer.train()

# Save
trainer.save_model("./final_model")
tokenizer.save_pretrained("./final_model")

# Evaluate
metrics = trainer.evaluate()
print(metrics)
```

## SFTTrainer (Instruction Tuning)

### Setup

```python
from trl import SFTTrainer, SFTConfig

sft_config = SFTConfig(
    output_dir="./sft_checkpoints",
    num_train_epochs=3,
    per_device_train_batch_size=4,
    learning_rate=2e-5,
    logging_steps=10,
    save_steps=500,
    max_seq_length=512,
    packing=False,  # Don't pack multiple samples
)
```

### Train with SFTTrainer

```python
trainer = SFTTrainer(
    model=model,
    args=sft_config,
    train_dataset=train_data,
    tokenizer=tokenizer,
    dataset_text_field="text",  # Column with training text
)

trainer.train()
trainer.save_model("./sft_model")
```

## Evaluation

### Evaluation Function

```python
def evaluate(model, dataloader):
    model.eval()
    total_loss = 0

    with torch.no_grad():
        for batch in dataloader:
            input_ids = batch["input_ids"].to(device)
            attention_mask = batch["attention_mask"].to(device)
            labels = input_ids.clone()

            outputs = model(
                input_ids=input_ids,
                attention_mask=attention_mask,
                labels=labels
            )

            total_loss += outputs.loss.item()

    return total_loss / len(dataloader)
```

### Perplexity

```python
import math

eval_loss = evaluate(model, val_loader)
perplexity = math.exp(eval_loss)
print(f"Perplexity: {perplexity:.2f}")
```

## Inference with Fine-Tuned Model

```python
def generate_response(model, tokenizer, prompt, max_new_tokens=128):
    model.eval()
    device = next(model.parameters()).device

    inputs = tokenizer(prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        outputs = model.generate(
            **inputs,
            max_new_tokens=max_new_tokens,
            do_sample=True,
            temperature=0.7,
            top_p=0.9,
            pad_token_id=tokenizer.pad_token_id
        )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Test
prompt = build_prompt("What is machine learning?")
response = generate_response(model, tokenizer, prompt)
print(response)
```

## Checkpointing

### Save Checkpoint

```python
# Save model and tokenizer
model.save_pretrained("./checkpoint")
tokenizer.save_pretrained("./checkpoint")
```

### Load Checkpoint

```python
from transformers import AutoModelForCausalLM, AutoTokenizer

model = AutoModelForCausalLM.from_pretrained("./checkpoint")
tokenizer = AutoTokenizer.from_pretrained("./checkpoint")
```

### Resume Training

```python
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_train,
)

trainer.train(resume_from_checkpoint="./checkpoint")
```

## Hyperparameters Guide

| Parameter | Typical Values | Notes |
|-----------|----------------|-------|
| `learning_rate` | 1e-5 to 5e-5 | Lower for larger models |
| `batch_size` | 4, 8, 16 | Limited by GPU memory |
| `epochs` | 1-5 | More for smaller datasets |
| `warmup_steps` | 5-10% of total | Stabilizes early training |
| `weight_decay` | 0.01-0.1 | Regularization |
| `max_length` | 512, 1024, 2048 | Context window |

## When to Use This Skill

Use when:

- Adapting LLM to specific domain/task
- Improving model performance on your data
- Creating instruction-following models
- Need full control over training process

## Cross-References

- `bazzite-ai-jupyter:sft` - Unsloth-optimized SFT (recommended)
- `bazzite-ai-jupyter:grpo` - RL with reward functions
- `bazzite-ai-jupyter:dpo` - Preference learning
- `bazzite-ai-jupyter:rloo` - RL with lower variance
- `bazzite-ai-jupyter:quantization` - Memory-efficient training
- `bazzite-ai-jupyter:peft` - Parameter-efficient fine-tuning
- `bazzite-ai-jupyter:qlora` - Advanced QLoRA experiments
- `bazzite-ai-jupyter:inference` - Fast inference patterns
- `bazzite-ai-jupyter:transformers` - Architecture understanding
