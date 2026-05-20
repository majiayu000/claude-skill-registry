---
name: llm-fine-tuning
description: "Fine-tune large language models efficiently using LoRA, QLoRA, and PEFT methods. Use for domain adaptation, instruction tuning, task-specific optimization, and parameter-efficient training of LLMs."
---

# LLM Fine-Tuning

Fine-tune large language models efficiently using parameter-efficient methods.

## Overview

LLM fine-tuning adapts pre-trained models to specific tasks or domains. This skill covers efficient techniques like LoRA, QLoRA, and full fine-tuning strategies.

## Quick Reference

| Scenario | Recommended Approach | Reference File |
|----------|---------------------|----------------|
| Efficient fine-tuning with limited resources | LoRA, QLoRA, PEFT methods | `/references/peft-methods.md` |
| Full model fine-tuning | Supervised fine-tuning, instruction tuning | `/references/full-finetuning.md` |
| Alignment and safety | RLHF, DPO, preference optimization | `/references/alignment.md` |

## Core Principles

1. **Parameter Efficiency** - Update small subset of parameters
2. **Task Adaptation** - Specialize model for specific use case
3. **Data Quality** - High-quality training data is critical
4. **Evaluation** - Rigorous testing on held-out data
5. **Monitoring** - Track metrics to prevent degradation

## Fine-Tuning Methods

### LoRA (Low-Rank Adaptation)
Inject trainable low-rank matrices into model layers.

**Advantages:**
- 0.1-1% of parameters trainable
- Fast training
- Multiple adapters for one base model
- No inference latency

**Hyperparameters:**
- Rank (r): 4-64 typical
- Alpha: Scaling factor
- Target modules: Which layers to adapt

### QLoRA (Quantized LoRA)
LoRA with 4-bit quantized base model.

**Benefits:**
- Fine-tune 65B model on single GPU
- Minimal performance loss
- Extreme memory efficiency

**Requirements:**
- bitsandbytes library
- NVIDIA GPU with compute capability ≥ 7.0

### Full Fine-Tuning
Update all model parameters.

**When to Use:**
- Abundant compute resources
- Significant domain shift
- Maximum performance needed

**Challenges:**
- High memory requirements
- Risk of catastrophic forgetting
- Expensive

## Training Process

### 1. Data Preparation
- Collect high-quality examples
- Format as instruction-response pairs
- Split into train/validation/test
- Typical size: 1K-100K examples

### 2. Model Selection
- Choose base model (Llama, Mistral, GPT)
- Consider size vs performance trade-off
- Check license for commercial use

### 3. Training
- Set hyperparameters (LR, batch size, epochs)
- Monitor training and validation loss
- Use gradient accumulation for large batches
- Apply early stopping

### 4. Evaluation
- Test on held-out data
- Human evaluation for quality
- Compare to base model
- Check for regressions

## Using the Reference Files

**`/references/peft-methods.md`** — LoRA, QLoRA, Prefix Tuning, Adapter layers, implementation with Hugging Face PEFT library.

**`/references/full-finetuning.md`** — Supervised fine-tuning, instruction tuning, data preparation, training strategies, and hyperparameter tuning.

**`/references/alignment.md`** — RLHF (Reinforcement Learning from Human Feedback), DPO (Direct Preference Optimization), safety considerations.

## Best Practices

- Start with LoRA/QLoRA for efficiency
- Use high-quality, diverse training data
- Monitor validation loss to prevent overfitting
- Use learning rate warm-up
- Apply gradient clipping
- Save checkpoints regularly
- Evaluate thoroughly before deployment
- Document training process

## Common Pitfalls to Avoid

- Insufficient or low-quality training data
- Overfitting to small datasets
- Learning rate too high (catastrophic forgetting)
- Not using validation set
- Ignoring base model capabilities
- Training too many epochs
- Not testing on diverse inputs
- Deploying without human evaluation

