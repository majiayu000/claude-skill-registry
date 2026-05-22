---
name: rloo
description: |
  Reinforcement Learning with Leave-One-Out estimation for policy optimization.
  Covers RLOOTrainer, reward function integration, baseline estimation, and
  variance reduction techniques for stable RL training. Includes thinking-aware patterns.
---

# Reinforcement Learning with Leave-One-Out (RLOO)

## Overview

RLOO is a reinforcement learning method that uses leave-one-out baseline estimation for variance reduction. Like GRPO, it generates multiple completions per prompt but uses a different baseline computation that can provide more stable gradients. This skill includes patterns for training thinking/reasoning models.

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `RLOOTrainer` | RL trainer with RLOO baseline |
| `RLOOConfig` | Training hyperparameters |
| `reward_funcs` | Reward function(s) for scoring |
| `completion_ids` | Token IDs passed to reward functions (no re-tokenization) |
| `num_generations` | Completions per prompt (4 typical) |
| `kl_coef` | KL penalty coefficient (0.05, lower than GRPO) |
| `learning_rate` | 1e-5 (same as GRPO) |
| Token ID 151668 | `</think>` boundary for Qwen3-Thinking models |

## Critical Environment Setup

```python
import os
from dotenv import load_dotenv
load_dotenv()

# Force text-based progress in Jupyter
os.environ["TQDM_NOTEBOOK"] = "false"

# CRITICAL: Set BEFORE importing unsloth/TRL
os.environ['ACCELERATE_MIXED_PRECISION'] = 'bf16'
```

## Critical Import Order

```python
# CRITICAL: Import unsloth FIRST for proper TRL patching
import unsloth
from unsloth import FastLanguageModel, is_bf16_supported

# Then TRL imports
from trl import RLOOConfig, RLOOTrainer
from datasets import Dataset
import torch
```

## RLOO Concepts

### How RLOO Works

1. Generate K completions for each prompt
2. Score all completions with reward function
3. For each completion, compute baseline as mean of other K-1 rewards
4. Advantage = reward - leave-one-out baseline
5. Update policy using advantages

### Leave-One-Out Baseline

```
For completion i:
  baseline_i = mean(rewards except reward_i)
  advantage_i = reward_i - baseline_i

This reduces variance compared to:
  - Single-sample estimates (high variance)
  - Fixed baselines (may be inaccurate)
```

### Comparison with GRPO

| Aspect | RLOO | GRPO |
|--------|------|------|
| Baseline | Leave-one-out mean | Group mean |
| Variance | Lower | Higher |
| Compute | Similar | Similar |
| Stability | Often better | Good |

## Dataset Format

```python
# RLOO requires prompts only (completions generated during training)
dataset = Dataset.from_dict({
    "prompt": [
        tokenizer.apply_chat_template(
            [{"role": "user", "content": "Explain recursion."}],
            tokenize=False, add_generation_prompt=True
        ),
        # ... more prompts
    ]
})
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

# Setup pad token (required for RLOO)
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

## RLOOTrainer Configuration

### Basic Configuration

```python
from trl import RLOOConfig

rloo_config = RLOOConfig(
    output_dir="./rloo_output",
    per_device_train_batch_size=1,
    gradient_accumulation_steps=4,
    max_steps=100,
    learning_rate=1e-5,
    fp16=not is_bf16_supported(),
    bf16=is_bf16_supported(),
    optim="adamw_8bit",
    num_generations=4,
    max_completion_length=128,
    kl_coef=0.05,
)
```

### Key Parameters

| Parameter | Typical Values | Effect |
|-----------|----------------|--------|
| `num_generations` | 4-8 | Completions per prompt |
| `kl_coef` | 0.01-0.1 | KL penalty strength |
| `learning_rate` | 1e-6 to 1e-5 | Lower than SFT |
| `max_completion_length` | 64-256 | Generation length |

## Reward Functions

### Simple Reward Function

```python
def length_reward(completions, prompts=None):
    """Reward based on response quality heuristics."""
    rewards = []
    for completion in completions:
        length = len(completion.split())
        score = 0.0

        # Prefer medium length
        if 10 <= length <= 50:
            score += 1.0
        elif length < 10:
            score -= 0.5

        # Prefer complete sentences
        if completion.strip().endswith("."):
            score += 0.5

        rewards.append(score)
    return rewards
```

### Using Trained Reward Model

```python
def trained_reward(completions, prompts):
    """Use trained reward model."""
    return reward_model.get_rewards(prompts, completions)
```

### Thinking-Aware Reward Function (Token-Based)

Use `completion_ids` parameter from TRL for efficient token-based parsing (same pattern as GRPO):

```python
THINK_END_TOKEN_ID = 151668  # </think> token for Qwen3-Thinking models

def thinking_reward_fn(completions, prompts=None, completion_ids=None, **kwargs):
    """
    Token-based reward function using completion_ids provided by TRL.

    Benefits over string matching:
    - No re-tokenization overhead (faster training)
    - Exact token boundaries (no regex edge cases)
    - Consistent with inference code pattern

    Scoring:
    - No </think> token: -1.0 (strongly penalized)
    - Short thinking (<10 tokens): 0.3
    - Medium thinking (10-30 tokens): 0.7
    - Long thinking (>30 tokens): 1.0
    - Bonus +0.1 for self-questioning (contains '?')
    """
    rewards = []

    for completion, comp_ids in zip(completions, completion_ids):
        # Token-based detection using </think> token ID
        if THINK_END_TOKEN_ID in comp_ids:
            end_idx = comp_ids.index(THINK_END_TOKEN_ID)
            thinking_length = end_idx  # Token count before </think>

            # String-based content analysis for question detection
            thinking_content = completion.split('</think>')[0]
            has_self_questions = '?' in thinking_content

            # Score based on thinking token count
            if thinking_length < 10:
                reward = 0.3  # Minimal thinking
            elif thinking_length < 30:
                reward = 0.7 + (0.1 if has_self_questions else 0)
            else:
                reward = 1.0 + (0.1 if has_self_questions else 0)
        else:
            reward = -1.0  # No </think> token found

        rewards.append(reward)

    return rewards
```

**Key insight**: TRL passes `completion_ids` directly to reward functions, eliminating re-tokenization overhead.

## Training

### Basic Training

```python
from trl import RLOOTrainer

trainer = RLOOTrainer(
    model=model,
    args=rloo_config,
    train_dataset=dataset,
    processing_class=tokenizer,
    reward_model=length_reward,
)

trainer.train()
```

### With Reward Model Instance

```python
trainer = RLOOTrainer(
    model=model,
    args=rloo_config,
    train_dataset=dataset,
    processing_class=tokenizer,
    reward_model=trained_reward_model,
)
```

## num_generations Selection

| K | Use Case |
|---|----------|
| 2 | Minimum (limited variance reduction) |
| 4 | Standard (recommended) |
| 8 | Better baseline estimation (more compute) |
| 16+ | Diminishing returns |

**Trade-off:** Higher K = better baseline but more memory/compute

## Troubleshooting

### High Variance

**Symptom:** Unstable training, jumpy rewards

**Fix:**
- Increase `num_generations` to 6-8
- Lower `learning_rate`
- Increase `kl_coef`

### KL Divergence Explosion

**Symptom:** Model output degrades quickly

**Fix:**
- Increase `kl_coef` to 0.1
- Reduce `learning_rate`
- More frequent evaluation

### Reward Collapse

**Symptom:** All generations get similar rewards

**Fix:**
- Check reward function diversity
- Increase `temperature` during generation
- More diverse prompts

### Memory Issues

**Symptom:** OOM with multiple generations

**Fix:**
- Reduce `num_generations` to 2-4
- Reduce `max_completion_length`
- Use gradient checkpointing

## Kernel Shutdown (Jupyter)

RLOO training uses significant GPU memory. Shutdown kernel to release memory:

```python
import IPython
print("Shutting down kernel to release GPU memory...")
app = IPython.Application.instance()
app.kernel.do_shutdown(restart=False)
```

**Important**: Always run this at the end of training notebooks before switching to different models.

## When to Use This Skill

Use when:

- Want lower variance than GRPO
- Have compute for multiple generations
- Building RLHF pipelines
- Need stable RL training
- Policy optimization from rewards

## RLOO vs GRPO Comparison

| Aspect | RLOO | GRPO |
|--------|------|------|
| Baseline | Leave-one-out mean | Group mean |
| Variance | Lower | Higher |
| KL penalty (beta) | 0.05 | 0.1 |
| num_generations | 4 | 2 |
| batch_size | 4 | 2 |
| Stability | Often better | Good |
| Use when | Need stable training | Faster iteration |

## Cross-References

- `bazzite-ai-jupyter:sft` - Pre-training before RLOO
- `bazzite-ai-jupyter:grpo` - Alternative RL method (higher variance)
- `bazzite-ai-jupyter:reward` - Training reward models for RLOO
- `bazzite-ai-jupyter:dpo` - Simpler alternative (no RL)
- `bazzite-ai-jupyter:peft` - LoRA for efficient training
- `bazzite-ai-jupyter:inference` - Fast inference with vLLM
