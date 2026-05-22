---
name: sft
description: |
  Supervised Fine-Tuning with SFTTrainer and Unsloth. Covers dataset preparation,
  chat template formatting, training configuration, and Unsloth optimizations
  for 2x faster instruction tuning. Includes thinking model patterns.
---

# Supervised Fine-Tuning (SFT)

## Overview

SFT adapts a pre-trained LLM to follow instructions by training on instruction-response pairs. Unsloth provides an optimized SFTTrainer for 2x faster training with reduced memory usage. This skill includes patterns for training thinking/reasoning models.

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `FastLanguageModel` | Load model with Unsloth optimizations |
| `SFTTrainer` | Trainer for instruction tuning |
| `SFTConfig` | Training hyperparameters |
| `dataset_text_field` | Column containing formatted text |
| Token ID 151668 | `</think>` boundary for Qwen3-Thinking models |

## Critical Environment Setup

```python
import os
from dotenv import load_dotenv
load_dotenv()

# Force text-based progress in Jupyter
os.environ["TQDM_NOTEBOOK"] = "false"
```

## Critical Import Order

```python
# CRITICAL: Import unsloth FIRST for proper TRL patching
import unsloth
from unsloth import FastLanguageModel, is_bf16_supported

# Then other imports
from trl import SFTTrainer, SFTConfig
from datasets import Dataset
import torch
```

**Warning**: Importing TRL before Unsloth will disable optimizations and may cause errors.

## Dataset Formats

### Instruction-Response Format

```python
dataset = [
    {"instruction": "What is Python?", "response": "A programming language."},
    {"instruction": "Explain ML.", "response": "Machine learning is..."},
]
```

### Chat/Conversation Format

```python
dataset = [
    {"messages": [
        {"role": "user", "content": "What is Python?"},
        {"role": "assistant", "content": "A programming language."}
    ]},
]
```

### Using Chat Templates

```python
def format_conversation(sample):
    messages = [
        {"role": "user", "content": sample["instruction"]},
        {"role": "assistant", "content": sample["response"]}
    ]
    return {"text": tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )}

dataset = dataset.map(format_conversation)
```

### Thinking Model Format

For models like Qwen3-Thinking, include `<think>` tags in the assistant response. Use **self-questioning internal dialogue** style:

```python
def format_thinking_conversation(sample):
    """Format with thinking/reasoning tags."""
    # Combine thinking and response with tags
    assistant_content = f"<think>\n{sample['thinking']}\n</think>\n\n{sample['response']}"

    messages = [
        {"role": "user", "content": sample["instruction"]},
        {"role": "assistant", "content": assistant_content}
    ]
    return {"text": tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=False
    )}

# Sample dataset with self-questioning thinking style
thinking_data = [
    {
        "instruction": "What is machine learning?",
        "thinking": "What is the user asking here? They want to understand machine learning. What are the key concepts I should cover? It's a subset of AI... and it involves learning from data. How should I keep this accessible? Short and clear definition.",
        "response": "Machine learning is a subset of artificial intelligence where computers learn patterns from data."
    },
    {
        "instruction": "Explain Python in one sentence.",
        "thinking": "One sentence only - what's most important about Python? Its readability and versatility are the defining features. How do I capture both in one sentence?",
        "response": "Python is a high-level programming language known for its readability and versatility."
    },
    {
        "instruction": "What is a neural network?",
        "thinking": "How do I explain neural networks simply? What's the core concept? They're inspired by biological neurons... they process information in layers. Should I mention deep learning? Maybe keep it basic for now.",
        "response": "A neural network is a computational model inspired by biological neurons that processes information through connected layers."
    },
]

dataset = Dataset.from_list(thinking_data)
dataset = dataset.map(format_thinking_conversation, remove_columns=["instruction", "thinking", "response"])
```

**Thinking Style Patterns:**
- "What is the user asking here?"
- "Let me think about the key concepts..."
- "How should I structure this explanation?"
- "What's most important about X?"

## Unsloth SFT Setup

### Load Model

```python
from unsloth import FastLanguageModel

# Standard model
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-unsloth-bnb-4bit",
    max_seq_length=512,
    load_in_4bit=True,
)

# Thinking model (for reasoning tasks)
model, tokenizer = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-Thinking-2507-unsloth-bnb-4bit",
    max_seq_length=1024,  # Increased for thinking content
    load_in_4bit=True,
)
```

### Apply LoRA

```python
model = FastLanguageModel.get_peft_model(
    model,
    r=16,
    lora_alpha=16,
    lora_dropout=0,
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj",
                    "gate_proj", "up_proj", "down_proj"],
    use_gradient_checkpointing="unsloth",
)
```

### Training Configuration

```python
from trl import SFTConfig

sft_config = SFTConfig(
    output_dir="./sft_output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    max_steps=100,
    learning_rate=2e-4,
    fp16=not is_bf16_supported(),
    bf16=is_bf16_supported(),
    optim="adamw_8bit",
    max_seq_length=512,
)
```

## SFTTrainer Usage

### Basic Training

```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    dataset_text_field="text",
    args=sft_config,
)

trainer.train()
```

### With Custom Formatting

```python
def formatting_func(examples):
    texts = []
    for instruction, response in zip(examples["instruction"], examples["response"]):
        text = f"### Instruction:\n{instruction}\n\n### Response:\n{response}"
        texts.append(text)
    return texts

trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    formatting_func=formatting_func,
    args=sft_config,
)
```

## Key Parameters

| Parameter | Typical Values | Effect |
|-----------|----------------|--------|
| `learning_rate` | 2e-4 to 2e-5 | Training speed vs stability |
| `per_device_train_batch_size` | 1-4 | Memory usage |
| `gradient_accumulation_steps` | 2-8 | Effective batch size |
| `max_seq_length` | 512-2048 | Context window |
| `optim` | "adamw_8bit" | Memory-efficient optimizer |

## Save and Load

### Save Model

```python
# Save LoRA adapters only (small)
model.save_pretrained("./sft_lora")

# Save merged model (full size)
model.save_pretrained_merged("./sft_merged", tokenizer)
```

### Load for Inference

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained("./sft_lora")
FastLanguageModel.for_inference(model)
```

### Thinking Model Inference

Parse thinking content from model output using token IDs:

```python
THINK_END_TOKEN_ID = 151668  # </think> token for Qwen3-Thinking

def generate_with_thinking(model, tokenizer, prompt):
    """Generate and parse thinking model output."""
    messages = [{"role": "user", "content": prompt}]
    inputs = tokenizer.apply_chat_template(
        messages, tokenize=True, add_generation_prompt=True, return_tensors="pt"
    ).to(model.device)

    # Setup pad token if needed
    if tokenizer.pad_token_id is None:
        tokenizer.pad_token_id = tokenizer.eos_token_id

    outputs = model.generate(
        input_ids=inputs,
        max_new_tokens=1024,
        temperature=0.6,
        top_p=0.95,
        do_sample=True,
        pad_token_id=tokenizer.pad_token_id,
    )

    # Extract only generated tokens
    input_length = inputs.shape[1]
    generated_ids = outputs[0][input_length:].tolist()

    # Parse thinking and response
    if THINK_END_TOKEN_ID in generated_ids:
        end_idx = generated_ids.index(THINK_END_TOKEN_ID)
        thinking = tokenizer.decode(generated_ids[:end_idx], skip_special_tokens=True)
        response = tokenizer.decode(generated_ids[end_idx + 1:], skip_special_tokens=True)
    else:
        thinking = tokenizer.decode(generated_ids, skip_special_tokens=True)
        response = "(incomplete - increase max_new_tokens)"

    return thinking.strip(), response.strip()

# Usage
FastLanguageModel.for_inference(model)
thinking, response = generate_with_thinking(model, tokenizer, "What is 15 + 27?")
print(f"Thinking: {thinking}")
print(f"Response: {response}")
```

## Ollama Integration

### Export to GGUF

```python
# Export to GGUF for Ollama
model.save_pretrained_gguf(
    "model",
    tokenizer,
    quantization_method="q4_k_m"
)
```

### Deploy to Ollama

```bash
ollama create mymodel -f Modelfile
ollama run mymodel
```

## Troubleshooting

### Out of Memory

**Symptom:** CUDA out of memory error

**Fix:**
- Use `gradient_checkpointing="unsloth"`
- Reduce `per_device_train_batch_size` to 1
- Use 4-bit quantization (`load_in_4bit=True`)

### NaN Loss

**Symptom:** Loss becomes NaN during training

**Fix:**
- Lower `learning_rate` to 1e-5
- Check data quality (no empty samples)
- Use gradient clipping

### Slow Training

**Symptom:** Training slower than expected

**Fix:**
- Ensure Unsloth is imported FIRST (before TRL)
- Use `bf16=True` if supported
- Enable `use_gradient_checkpointing="unsloth"`

## Kernel Shutdown (Jupyter)

SFT training uses significant GPU memory. Shutdown kernel to release memory:

```python
import IPython
print("Shutting down kernel to release GPU memory...")
app = IPython.Application.instance()
app.kernel.do_shutdown(restart=False)
```

**Important**: Always run this at the end of training notebooks before switching to different models.

## When to Use This Skill

Use when:

- Creating instruction-following models
- Fine-tuning for chat/conversation
- Adapting to domain-specific tasks
- Building custom assistants
- First step before preference optimization (DPO/GRPO)

## Cross-References

- `bazzite-ai-jupyter:peft` - LoRA configuration details
- `bazzite-ai-jupyter:qlora` - Advanced QLoRA experiments (alpha, rank, modules)
- `bazzite-ai-jupyter:finetuning` - General fine-tuning concepts
- `bazzite-ai-jupyter:dpo` - Direct Preference Optimization after SFT
- `bazzite-ai-jupyter:grpo` - GRPO reinforcement learning after SFT
- `bazzite-ai-jupyter:inference` - Fast inference with vLLM
- `bazzite-ai-jupyter:vision` - Vision model fine-tuning
- `bazzite-ai-ollama:api` - Ollama deployment
