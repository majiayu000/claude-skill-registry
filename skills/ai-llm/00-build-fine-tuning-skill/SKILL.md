---
sidebar_position: 0
title: "Build Your Fine-Tuning Skill"
description: "Create your llmops-fine-tuner skill from Unsloth documentation before learning fine-tuning theory"
chapter: 64
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill-First Learning Application"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can create a skill from official documentation using the Skill-First pattern"

  - name: "Documentation-Grounded Skill Creation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can fetch and synthesize official library documentation into a structured skill"

  - name: "LLMOps Skill Architecture"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can explain the structure and purpose of an LLMOps fine-tuning skill"

learning_objectives:
  - objective: "Create an llmops-fine-tuner skill from Unsloth documentation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill file creation with correct structure and grounded content"

  - objective: "Apply the Skill-First Learning Pattern to LLMOps"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "LEARNING-SPEC.md creation with clear success criteria"

  - objective: "Understand the structure of fine-tuning skills"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Explanation of skill components and their purposes"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (Skill-First pattern, LEARNING-SPEC, documentation grounding, LLMOps skill structure) within B1 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Add evaluation criteria and hyperparameter tuning decision trees to the skill"
  remedial_for_struggling: "Focus on the basic skill structure; defer advanced sections to later lessons"
---

# Build Your Fine-Tuning Skill

You are about to learn supervised fine-tuning. But here is the pattern that separates effective AI-native developers from those who struggle: **build your skill first, then learn the technology**.

In traditional learning, you study a topic, maybe take notes, and hope you remember it later. In Skill-First learning, you create a reusable intelligence asset before you even understand the technology deeply. This asset grows with you as you learn, and by the end of the chapter, you own a production-ready skill you can sell or deploy.

This lesson follows the same pattern you used in Part 6 and Part 7. Clone a fresh skills-lab, fetch official documentation, and build your `llmops-fine-tuner` skill from authoritative sources rather than memory.

## Why Skill-First for Fine-Tuning?

Fine-tuning has dozens of hyperparameters, multiple training strategies, and evolving best practices. Trying to memorize all of this is futile. But encoding it into a skill that you can invoke, test, and improve makes this knowledge permanently accessible and actionable.

| Traditional Approach | Skill-First Approach |
|---------------------|---------------------|
| Read tutorials, forget details | Build skill, query anytime |
| Notes scattered across files | Single authoritative source |
| Knowledge decays over time | Skill improves with use |
| Cannot delegate to AI | AI executes your skill |

By the end of this chapter, your `llmops-fine-tuner` skill will guide you through:
- Dataset preparation and validation
- Model and adapter configuration
- Training loop setup and monitoring
- Checkpoint management and export

## Step 1: Clone a Fresh Skills-Lab

Start with a clean environment. This prevents state from previous experiments from affecting your work.

```bash
# Clone the skills-lab repository
git clone https://github.com/panaversity/skills-lab.git ~/skills-lab-ch64

# Navigate to the directory
cd ~/skills-lab-ch64

# Create the skill directory structure
mkdir -p .claude/skills/llmops-fine-tuner
```

**Output:**
```
Cloning into '/Users/you/skills-lab-ch64'...
```

## Step 2: Write Your LEARNING-SPEC.md

Before creating the skill, define what you are trying to accomplish. This specification guides both your learning and the skill you create.

```markdown
# LEARNING-SPEC.md

## What I Want to Learn
Supervised fine-tuning of large language models using LoRA/QLoRA with Unsloth
on Colab Free Tier (T4 GPU, 15GB VRAM).

## Why This Matters
I want to create proprietary models that encode my domain expertise,
enabling Digital FTEs that are differentiated from generic foundation models.

## Success Criteria
1. I can explain why LoRA reduces 99% of trainable parameters
2. I can configure hyperparameters (rank, alpha, learning rate) with reasoning
3. I can run a training loop on Colab T4 without OOM errors
4. I can export a fine-tuned model to GGUF for Ollama deployment
5. My skill accurately reflects official Unsloth documentation

## Constraints
- Must work on Colab Free Tier (T4, 15GB VRAM, 12GB RAM)
- Must use Unsloth for 2x speed and 60% memory reduction
- Must produce GGUF output for local deployment

## Running Example
Fine-tune a model to become a Task API Assistant (from Chapter 40)
that understands task management domain language.
```

Save this file:

```bash
# Create the learning spec
cat > LEARNING-SPEC.md << 'EOF'
# LEARNING-SPEC.md

## What I Want to Learn
Supervised fine-tuning of large language models using LoRA/QLoRA with Unsloth
on Colab Free Tier (T4 GPU, 15GB VRAM).

## Why This Matters
I want to create proprietary models that encode my domain expertise,
enabling Digital FTEs that are differentiated from generic foundation models.

## Success Criteria
1. I can explain why LoRA reduces 99% of trainable parameters
2. I can configure hyperparameters (rank, alpha, learning rate) with reasoning
3. I can run a training loop on Colab T4 without OOM errors
4. I can export a fine-tuned model to GGUF for Ollama deployment
5. My skill accurately reflects official Unsloth documentation

## Constraints
- Must work on Colab Free Tier (T4, 15GB VRAM, 12GB RAM)
- Must use Unsloth for 2x speed and 60% memory reduction
- Must produce GGUF output for local deployment

## Running Example
Fine-tune a model to become a Task API Assistant (from Chapter 40)
that understands task management domain language.
EOF
```

## Step 3: Fetch Official Documentation

The skill must be grounded in official documentation, not AI memory which may be outdated or hallucinated.

Use Claude Code or your AI assistant:

```
/fetching-library-docs unsloth fine-tuning

Fetch the official Unsloth documentation covering:
1. LoRA hyperparameters (rank, alpha, learning rate)
2. QLoRA 4-bit configuration
3. SFTTrainer setup
4. Model saving and export options
```

Key sources to reference:
- [Unsloth LoRA Hyperparameters Guide](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide/lora-hyperparameters-guide)
- [Unsloth Fine-tuning LLMs Guide](https://docs.unsloth.ai/get-started/fine-tuning-llms-guide)
- [Unsloth GitHub Repository](https://github.com/unslothai/unsloth)

## Step 4: Create Your llmops-fine-tuner Skill

Based on the documentation, create your skill file:

```bash
cat > .claude/skills/llmops-fine-tuner/SKILL.md << 'EOF'
---
name: llmops-fine-tuner
description: This skill should be used when fine-tuning language models with LoRA/QLoRA using Unsloth. Use when preparing datasets, configuring training, running SFT, and exporting models.
---

# LLMOps Fine-Tuner Skill

## Purpose

Guide supervised fine-tuning of LLMs using Parameter-Efficient Fine-Tuning (PEFT)
with LoRA/QLoRA and Unsloth optimization on consumer GPUs.

## When to Use This Skill

Invoke this skill when:
- Preparing datasets for supervised fine-tuning
- Selecting base models appropriate for task and hardware
- Configuring LoRA/QLoRA hyperparameters
- Running training loops with SFTTrainer
- Monitoring training progress and detecting issues
- Exporting models (adapter, merged, GGUF)

## Prerequisite Knowledge

- Understanding of transformers architecture (attention layers, MLP)
- Familiarity with Hugging Face ecosystem (transformers, datasets, PEFT)
- Python proficiency for debugging training issues

## Hardware Context

**Colab Free Tier (T4 GPU):**
- 15GB VRAM
- 12GB RAM
- Use QLoRA (4-bit) for models up to 8B parameters
- Gradient accumulation required for effective batch sizes

## LoRA Configuration Guide

### Core Parameters

| Parameter | Recommended | Range | Purpose |
|-----------|-------------|-------|---------|
| `r` (rank) | 16 | 8-64 | Controls adapter capacity |
| `lora_alpha` | 16 (= r) | r to 2*r | Scaling factor for updates |
| `lora_dropout` | 0 | 0-0.1 | Regularization (0 for most cases) |
| `target_modules` | All attention + MLP | Varies | Which layers to adapt |

### Target Modules (Recommended)

```python
target_modules = [
    "q_proj", "k_proj", "v_proj", "o_proj",  # Attention
    "gate_proj", "up_proj", "down_proj",      # MLP
]
```

### Rank Selection Framework

| Use Case | Recommended Rank | Rationale |
|----------|-----------------|-----------|
| Simple style transfer | 8 | Few new patterns needed |
| Domain adaptation | 16 | Moderate new knowledge |
| Complex tasks | 32-64 | Significant new capabilities |
| If unsure | 16 | Safe default, adjust based on results |

## QLoRA Configuration

```python
from transformers import BitsAndBytesConfig

bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4",           # NormalFloat4 (optimal)
    bnb_4bit_compute_dtype=torch.bfloat16,
    bnb_4bit_use_double_quant=True,       # Reduces memory further
)
```

**Why NF4?** The NormalFloat4 data type is information-theoretically optimal
for normally distributed weights, which matches how LLM weights are initialized.

## Training Arguments Guide

### Starting Configuration

```python
from transformers import TrainingArguments

training_args = TrainingArguments(
    output_dir="./outputs",
    per_device_train_batch_size=4,       # Limited by VRAM
    gradient_accumulation_steps=4,        # Effective batch = 16
    num_train_epochs=3,                   # Start small
    learning_rate=2e-4,                   # Higher for LoRA
    warmup_ratio=0.03,                    # 3% warmup
    weight_decay=0.01,                    # Light regularization
    fp16=True,                            # Mixed precision
    logging_steps=10,
    save_strategy="epoch",
    optim="adamw_8bit",                   # Memory efficient
)
```

### Learning Rate Guidelines

| Scenario | Learning Rate | Reasoning |
|----------|--------------|-----------|
| Standard SFT | 2e-4 | Default for LoRA fine-tuning |
| Continued pre-training | 5e-5 | Gentler for knowledge preservation |
| Small datasets (&lt;1K) | 1e-4 | Avoid overfitting |
| Large datasets (>10K) | 2e-4 to 5e-4 | Can be more aggressive |

## Unsloth Optimization

### Why Unsloth?

- **2x faster training** through optimized kernels
- **60% less VRAM** via memory-efficient attention
- **No accuracy loss** compared to standard training

### Setup Pattern

```python
from unsloth import FastLanguageModel

model, tokenizer = FastLanguageModel.from_pretrained(
    model_name="unsloth/Llama-3.2-3B-Instruct",
    max_seq_length=2048,
    load_in_4bit=True,           # QLoRA mode
    dtype=None,                   # Auto-detect
)

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

## Export Options

| Method | Size | Use Case |
|--------|------|----------|
| Adapter only | ~30MB | When base model available |
| Merged (FP16) | ~16GB | Cloud deployment with full precision |
| GGUF q4_k_m | ~4GB | Local Ollama deployment |

### GGUF Export

```python
# Save as GGUF for Ollama
model.save_pretrained_gguf(
    "model-gguf",
    tokenizer,
    quantization_method="q4_k_m",
)
```

## Troubleshooting Decision Tree

### Out of Memory (OOM)

1. Reduce `per_device_train_batch_size` (try 2, then 1)
2. Increase `gradient_accumulation_steps` proportionally
3. Reduce `max_seq_length`
4. Enable `use_gradient_checkpointing="unsloth"`
5. If still OOM: use smaller base model

### Training Loss Not Decreasing

1. Check learning rate (try 2e-4 first)
2. Verify data format matches expected template
3. Ensure tokenizer has proper chat template
4. Check for data quality issues

### Overfitting (Val loss increases while train loss decreases)

1. Reduce epochs (try 1-2)
2. Increase weight_decay
3. Add more training data
4. Reduce rank if dataset is small

## Validation Checks

Before declaring training complete:

- [ ] Training loss decreased consistently
- [ ] No OOM errors during training
- [ ] Model generates coherent responses
- [ ] Response format matches training data
- [ ] Export completed without errors
EOF
```

## Step 5: Verify Your Skill

Test that your skill was created correctly:

```bash
# Check the skill exists
ls -la .claude/skills/llmops-fine-tuner/

# View the skill content
head -50 .claude/skills/llmops-fine-tuner/SKILL.md
```

**Output:**
```
total 8
drwxr-xr-x  3 you  staff   96 Jan  1 10:00 .
drwxr-xr-x  3 you  staff   96 Jan  1 10:00 ..
-rw-r--r--  1 you  staff  4521 Jan  1 10:00 SKILL.md
```

## What Happens Next

You now have an `llmops-fine-tuner` skill that is grounded in official documentation. As you progress through this chapter:

| Lesson | How Your Skill Improves |
|--------|------------------------|
| L01: SFT Fundamentals | Add mental model explanations |
| L02: PEFT and LoRA | Refine rank/alpha selection logic |
| L03: QLoRA | Add quantization troubleshooting |
| L04: Unsloth | Add platform-specific optimizations |
| L05+: Training workflow | Add monitoring patterns |
| Capstone | Validate skill produces working model |

Each lesson will include a "Reflect on Your Skill" section where you update and improve this skill based on what you learned.

## Try With AI

Use your AI companion (Claude, ChatGPT, Gemini, or similar).

### Prompt 1: Verify Skill Structure

```
I just created my llmops-fine-tuner skill. Review the structure and tell me:
1. Does it follow the SKILL.md format correctly?
2. Is the content grounded in documentation (not hallucinated)?
3. What sections should I add as I learn more about fine-tuning?

Here is my skill:
[paste your SKILL.md content]
```

**What you are learning**: Critical evaluation of your own skill structure. Your AI partner helps identify gaps before you invest time in an incomplete skill.

### Prompt 2: Connect to Your Domain

```
I want to fine-tune a model for [your domain: legal documents, medical records,
customer support, code review, etc.]. Looking at my llmops-fine-tuner skill,
what domain-specific sections should I add? What unique challenges does my
domain present for fine-tuning?
```

**What you are learning**: Domain adaptation. Fine-tuning is not one-size-fits-all. Your AI partner helps you anticipate domain-specific challenges.

### Prompt 3: Validate Against Official Docs

```
Compare my skill's LoRA configuration recommendations against the official
Unsloth documentation. Are there any discrepancies? Any best practices
I should add?

Specifically check:
1. Recommended rank values
2. Target modules list
3. Learning rate guidance
```

**What you are learning**: Documentation verification. You are building the habit of validating AI-generated content against authoritative sources.

### Safety Note

As you create skills from documentation, remember that AI tools may not have the most current information. Always verify critical configuration values against the official source. The Unsloth documentation is updated regularly as best practices evolve.
