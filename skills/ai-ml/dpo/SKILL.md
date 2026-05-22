---
name: dpo
description: |
  Direct Preference Optimization for learning from preference pairs. Covers DPOTrainer,
  preference dataset preparation, implicit reward modeling, and beta tuning for
  stable preference learning without explicit reward models. Includes thinking quality patterns.
---

# Direct Preference Optimization (DPO)

## Overview

DPO learns from preference pairs (chosen vs rejected responses) without training an explicit reward model. It directly optimizes the policy using the Bradley-Terry preference model, making it simpler than RLHF while achieving comparable results. This skill includes patterns for training thinking/reasoning models.

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `DPOTrainer` | Trainer for preference optimization |
| `DPOConfig` | Training hyperparameters |
| `beta` | Temperature for implicit reward (0.1 typical) |
| `learning_rate` | 5e-6 (most conservative of RL methods) |
| `ref_model` | Reference model for KL constraint |
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

# Then TRL imports
from trl import DPOConfig, DPOTrainer
from datasets import Dataset
import torch
```

## DPO Concepts

### How DPO Works

1. Given prompt + chosen response + rejected response
2. Compute log-probabilities under policy and reference
3. Optimize policy to increase P(chosen) / P(rejected) ratio
4. Beta controls how strongly to enforce preference

### Key Differences from RLHF

| Aspect | DPO | RLHF |
|--------|-----|------|
| Reward Model | Implicit | Explicit |
| Training | Single stage | Multi-stage |
| Complexity | Simpler | More complex |
| Compute | Lower | Higher |

## Dataset Format

### Required Fields

```python
dataset = [
    {
        "prompt": "What is recursion?",
        "chosen": "Recursion is when a function calls itself with a simpler version of the problem, including a base case to stop.",
        "rejected": "Recursion is loops."
    },
    # ... more preference pairs
]
```

### From Comparison Data

```python
def format_preferences(sample):
    return {
        "prompt": tokenizer.apply_chat_template(
            [{"role": "user", "content": sample["question"]}],
            tokenize=False, add_generation_prompt=True
        ),
        "chosen": sample["better_response"],
        "rejected": sample["worse_response"],
    }

dataset = raw_dataset.map(format_preferences)
```

### Thinking Quality Preference Pairs

For thinking models, create preference pairs based on reasoning quality:

```python
# Chosen = Good thinking, Rejected = Poor/no thinking
thinking_preference_data = [
    {
        "prompt": "Explain recursion in programming.",
        "chosen": """<think>
What is recursion exactly? It's when a function calls itself.
Why would we use this? To break down problems into smaller, similar pieces.
What's a good example? Factorial: 5! = 5 * 4!
What's needed for it to work? A base case to stop the recursion.
</think>

Recursion is a programming technique where a function calls itself to solve a problem by breaking it into smaller, similar subproblems. For example, calculating factorial: n! = n * (n-1)!. Every recursive solution needs a base case to prevent infinite loops.""",
        "rejected": "Recursion is just loops."
    },
    {
        "prompt": "What is 15 + 27?",
        "chosen": """<think>
I need to add 15 and 27.
Let me break it down: 15 + 27 = 15 + 20 + 7 = 35 + 7 = 42.
I can verify: 42 - 15 = 27. Correct!
</think>

15 + 27 = 42""",
        "rejected": "42"
    },
    {
        "prompt": "Explain the difference between TCP and UDP.",
        "chosen": """<think>
What are TCP and UDP? They're network transport protocols.
What's the key difference? TCP is connection-oriented, UDP is connectionless.
What does that mean practically?
- TCP: Reliable, ordered delivery with acknowledgments
- UDP: Fast, no guarantees, better for streaming
When would you use each?
- TCP: File transfer, web browsing, email
- UDP: Video streaming, gaming, DNS
</think>

TCP is a connection-oriented protocol that guarantees reliable, ordered delivery through acknowledgments and retransmission. UDP is connectionless, offering faster but unreliable delivery without guarantees. Use TCP for reliability (file transfers, web), UDP for speed (streaming, gaming).""",
        "rejected": "TCP is reliable, UDP is not."
    },
]

dataset = Dataset.from_list(thinking_preference_data)

def format_thinking_preferences(sample):
    return {
        "prompt": tokenizer.apply_chat_template(
            [{"role": "user", "content": sample["prompt"]}],
            tokenize=False, add_generation_prompt=True
        ),
        "chosen": sample["chosen"],
        "rejected": sample["rejected"],
    }

dataset = dataset.map(format_thinking_preferences)
```

## Setup

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

# Setup pad token (required for DPO)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.pad_token_id = tokenizer.eos_token_id
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

## DPOTrainer Configuration

### Basic Configuration

```python
from trl import DPOConfig

dpo_config = DPOConfig(
    output_dir="./dpo_output",
    per_device_train_batch_size=2,
    gradient_accumulation_steps=4,
    max_steps=100,
    learning_rate=5e-6,
    fp16=not is_bf16_supported(),
    bf16=is_bf16_supported(),
    optim="adamw_8bit",
    beta=0.1,
    max_length=512,
    max_prompt_length=256,
)
```

### Key Parameters

| Parameter | Typical Values | Effect |
|-----------|----------------|--------|
| `beta` | 0.1-0.5 | Implicit reward temperature |
| `learning_rate` | 1e-6 to 5e-6 | Lower than SFT |
| `max_length` | 512-1024 | Max combined length |
| `max_prompt_length` | 256-512 | Max prompt length |

## Training

### Basic Training

```python
from trl import DPOTrainer

trainer = DPOTrainer(
    model=model,
    args=dpo_config,
    train_dataset=dataset,
    processing_class=tokenizer,
)

trainer.train()
```

### With Reference Model

```python
# For stronger KL constraint
ref_model, _ = FastLanguageModel.from_pretrained(
    "unsloth/Qwen3-4B-unsloth-bnb-4bit",
    max_seq_length=512,
    load_in_4bit=True,
)

trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,
    args=dpo_config,
    train_dataset=dataset,
    processing_class=tokenizer,
)
```

## Beta Selection Guide

| Beta | Use Case |
|------|----------|
| 0.01 | Weak preference signal |
| 0.1 | Standard (recommended) |
| 0.3 | Strong preference enforcement |
| 0.5+ | Very strong (may overfit) |

## Troubleshooting

### Chosen/Rejected Scores Similar

**Symptom:** Model doesn't distinguish preferences

**Fix:**
- Increase `beta` for stronger signal
- Train longer
- Check data quality (clear preference differences)

### Overfitting to Preferences

**Symptom:** Model only outputs chosen-style responses

**Fix:**
- Lower `beta`
- Use reference model
- Add regularization

### Low Accuracy

**Symptom:** DPO accuracy metric stays low

**Fix:**
- Ensure chosen is genuinely better than rejected
- Increase training steps
- Check prompt formatting

### Memory Issues

**Symptom:** OOM during training

**Fix:**
- Set `ref_model=None` (uses implicit reference)
- Reduce `max_length`
- Use gradient checkpointing

## Kernel Shutdown (Jupyter)

DPO training uses significant GPU memory. Shutdown kernel to release memory:

```python
import IPython
print("Shutting down kernel to release GPU memory...")
app = IPython.Application.instance()
app.kernel.do_shutdown(restart=False)
```

**Important**: Always run this at the end of training notebooks before switching to different models.

## When to Use This Skill

Use when:

- You have preference data (chosen vs rejected)
- Simpler pipeline than RLHF desired
- No reward model available
- Post-SFT alignment
- Human preference learning

## Cross-References

- `bazzite-ai-jupyter:sft` - Pre-training before DPO
- `bazzite-ai-jupyter:grpo` - Alternative with explicit rewards
- `bazzite-ai-jupyter:rloo` - Alternative RL with lower variance
- `bazzite-ai-jupyter:reward` - Training reward models (alternative to DPO)
- `bazzite-ai-jupyter:peft` - LoRA for efficient training
- `bazzite-ai-jupyter:inference` - Fast inference with vLLM
