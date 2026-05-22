---
name: fine-tuning-customization
description: LLM fine-tuning with LoRA, QLoRA, DPO alignment, and synthetic data generation. Efficient training, preference learning, data creation. Use when customizing models for specific domains.
version: 1.0.0
tags: [fine-tuning, lora, qlora, dpo, synthetic-data, rlhf, 2026]
context: fork
agent: llm-integrator
author: SkillForge
user-invocable: false
---

# Fine-Tuning & Customization

Customize LLMs for specific domains using parameter-efficient fine-tuning and alignment techniques.

> **Unsloth 2026**: 7x longer context RL, FP8 RL on consumer GPUs, rsLoRA support. **TRL**: OpenEnv integration, vLLM server mode, transformers 5.0.0+ compatible.

## Decision Framework: Fine-Tune or Not?

| Approach | Try First | When It Works |
|----------|-----------|---------------|
| Prompt Engineering | Always | Simple tasks, clear instructions |
| RAG | External knowledge needed | Knowledge-intensive tasks |
| Fine-Tuning | Last resort | Deep specialization, format control |

**Fine-tune ONLY when:**
1. Prompt engineering tried and insufficient
2. RAG doesn't capture domain nuances
3. Specific output format consistently required
4. Persona/style must be deeply embedded
5. You have ~1000+ high-quality examples

## LoRA vs QLoRA (Unsloth 2026)

| Criteria | LoRA | QLoRA |
|----------|------|-------|
| Model fits in VRAM | Use LoRA | |
| Memory constrained | | Use QLoRA |
| Training speed | 39% faster | |
| Memory savings | | 75%+ (dynamic 4-bit quants) |
| Quality | Baseline | ~Same (Unsloth recovered accuracy loss) |
| 70B LLaMA | | <48GB VRAM with QLoRA |

## Quick Reference: LoRA Training

```python
from unsloth import FastLanguageModel
from trl import SFTTrainer

# Load with 4-bit quantization (QLoRA)
model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Meta-Llama-3.1-8B",
    max_seq_length=2048,
    load_in_4bit=True,
)

# Add LoRA adapters
model = FastLanguageModel.get_peft_model(
    model,
    r=16,              # Rank (16-64 typical)
    lora_alpha=32,     # Scaling (2x r)
    lora_dropout=0.05,
    target_modules=[
        "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
        "gate_proj", "up_proj", "down_proj",      # MLP (QLoRA paper)
    ],
)

# Train
trainer = SFTTrainer(
    model=model,
    tokenizer=tokenizer,
    train_dataset=dataset,
    max_seq_length=2048,
)
trainer.train()
```

## DPO Alignment

```python
from trl import DPOTrainer, DPOConfig

config = DPOConfig(
    learning_rate=5e-6,  # Lower for alignment
    beta=0.1,            # KL penalty coefficient
    per_device_train_batch_size=4,
    num_train_epochs=1,
)

# Preference dataset: {prompt, chosen, rejected}
trainer = DPOTrainer(
    model=model,
    ref_model=ref_model,  # Frozen reference
    args=config,
    train_dataset=preference_dataset,
    tokenizer=tokenizer,
)
trainer.train()
```

## Synthetic Data Generation

```python
async def generate_synthetic(topic: str, n: int = 100) -> list[dict]:
    """Generate training examples using teacher model."""
    examples = []
    for _ in range(n):
        response = await client.chat.completions.create(
            model="gpt-4o",  # Teacher
            messages=[{
                "role": "system",
                "content": f"Generate a training example about {topic}. "
                          "Include instruction and response."
            }],
            response_format={"type": "json_object"}
        )
        examples.append(json.loads(response.choices[0].message.content))
    return examples
```

## Key Hyperparameters

| Parameter | Recommended | Notes |
|-----------|-------------|-------|
| Learning rate | 2e-4 | LoRA/QLoRA standard |
| Epochs | 1-3 | More risks overfitting |
| LoRA r | 16-64 | Higher = more capacity |
| LoRA alpha | 2x r | Scaling factor |
| Batch size | 4-8 | Per device |
| Warmup | 3% | Ratio of steps |

## Anti-Patterns (FORBIDDEN)

```python
# NEVER fine-tune without trying alternatives first
model.fine_tune(data)  # Try prompt engineering & RAG first!

# NEVER use low-quality training data
data = scrape_random_web()  # Garbage in, garbage out

# NEVER skip evaluation
trainer.train()
deploy(model)  # Always evaluate before deploy!

# ALWAYS use separate eval set
train, eval = split(data, test_size=0.1)
trainer = SFTTrainer(..., eval_dataset=eval)
```

## Detailed Documentation

| Resource | Description |
|----------|-------------|
| [references/lora-qlora.md](references/lora-qlora.md) | Parameter-efficient fine-tuning |
| [references/dpo-alignment.md](references/dpo-alignment.md) | Direct Preference Optimization |
| [references/synthetic-data.md](references/synthetic-data.md) | Training data generation |
| [references/when-to-finetune.md](references/when-to-finetune.md) | Decision framework |

## Related Skills

- `llm-evaluation` - Evaluate fine-tuned models
- `embeddings` - When to use embeddings instead
- `rag-retrieval` - When RAG is better than fine-tuning
- `langfuse-observability` - Track training experiments

## Capability Details

### lora-qlora
**Keywords:** LoRA, QLoRA, PEFT, parameter efficient, adapter, low-rank
**Solves:**
- Fine-tune large models on consumer hardware
- Configure LoRA hyperparameters
- Choose target modules for adapters

### dpo-alignment
**Keywords:** DPO, RLHF, preference, alignment, human feedback, preference data
**Solves:**
- Align models to human preferences
- Create preference datasets
- Configure DPO training

### synthetic-data
**Keywords:** synthetic data, data generation, teacher model, distillation
**Solves:**
- Generate training data with LLMs
- Implement teacher-student training
- Scale training data quality

### when-to-finetune
**Keywords:** should I fine-tune, fine-tune decision, customize model
**Solves:**
- Decide when fine-tuning is appropriate
- Evaluate alternatives to fine-tuning
- Assess data requirements
