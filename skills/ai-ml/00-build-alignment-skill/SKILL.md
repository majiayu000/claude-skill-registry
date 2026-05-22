---
sidebar_position: 0
title: "Build Your Alignment Skill"
description: "Create your model-alignment skill from TRL documentation before learning DPO theory"
chapter: 68
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
    measurable_at_this_level: "Student can fetch and synthesize official TRL documentation into a structured skill"

  - name: "Alignment Skill Architecture"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can explain the structure and purpose of a model alignment skill"

learning_objectives:
  - objective: "Create a model-alignment skill from TRL documentation"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Skill file creation with correct structure and grounded content"

  - objective: "Apply the Skill-First Learning Pattern to alignment"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "LEARNING-SPEC.md creation with clear success criteria"

  - objective: "Understand the structure of alignment skills"
    proficiency_level: "B1"
    bloom_level: "Understand"
    assessment_method: "Explanation of skill components and their purposes"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (Skill-First pattern, LEARNING-SPEC, documentation grounding, alignment skill structure) within B1 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Add red-teaming patterns and safety evaluation metrics to the skill"
  remedial_for_struggling: "Focus on the basic skill structure; defer advanced sections to later lessons"
---

# Build Your Alignment Skill

You have a merged model that combines persona and agentic capabilities. But models that complete tasks eagerly can also complete harmful requests eagerly. Before learning alignment theory, you'll build a skill that encodes the knowledge you need.

This lesson follows the pattern you've used throughout Part 8: create the skill first from official documentation, then use the chapter to test and improve it. By the end of this chapter, your `model-alignment` skill will be battle-tested and production-ready.

## Why Alignment Needs a Skill

Alignment is not a one-time fix. It's an ongoing discipline with evolving techniques, common failure modes, and nuanced tradeoffs. Memorizing this is impossible. Encoding it into a skill makes the knowledge permanently accessible.

| Traditional Approach | Skill-First Approach |
|---------------------|---------------------|
| Read papers, forget details | Build skill, query anytime |
| Scattered alignment notes | Single authoritative source |
| Reinvent safety patterns | Reuse validated approaches |
| Cannot delegate to AI | AI executes your skill |

Your merged Task API model from Chapter 67 needs alignment before deployment. Without it, the model will helpfully attempt anything a user asks, including harmful requests.

## Step 1: Clone a Fresh Skills-Lab

Start with a clean environment. State from Chapter 67 should not affect your alignment work.

```bash
# Clone the skills-lab repository
git clone https://github.com/panaversity/skills-lab.git ~/skills-lab-ch68

# Navigate to the directory
cd ~/skills-lab-ch68

# Create the skill directory structure
mkdir -p .claude/skills/model-alignment
```

**Output:**
```
Cloning into '/Users/you/skills-lab-ch68'...
```

## Step 2: Write Your LEARNING-SPEC.md

Before creating the skill, define what you need to accomplish. This specification guides both your learning and the skill you create.

```markdown
# LEARNING-SPEC.md

## What I Want to Learn
Model alignment using Direct Preference Optimization (DPO) with TRL library
on Colab Free Tier (T4 GPU, 15GB VRAM).

## Why This Matters
My merged Task API model completes any request. I need it to:
- Refuse harmful task requests gracefully
- Maintain helpfulness for legitimate tasks
- Detect and resist jailbreak attempts
- Provide safe, useful responses consistently

## Success Criteria
1. I can explain why fine-tuned models need alignment
2. I can create preference datasets (prompt/chosen/rejected)
3. I can run DPO training on Colab T4 without OOM errors
4. I can red-team my model to find vulnerabilities
5. I can implement refusal training for unsafe requests
6. My aligned model achieves 90%+ harm reduction

## Constraints
- Must work on Colab Free Tier (T4, 15GB VRAM, 12GB RAM)
- Must use DPO (not RLHF) for simplicity and compute efficiency
- Must use TRL library for training
- Must integrate with existing merged model from Chapter 67

## Running Example
Align my merged Task API model to refuse harmful task requests
(e.g., "create a task to stalk someone") while remaining helpful
for legitimate productivity use cases.
```

Save this file:

```bash
cat > LEARNING-SPEC.md << 'EOF'
# LEARNING-SPEC.md

## What I Want to Learn
Model alignment using Direct Preference Optimization (DPO) with TRL library
on Colab Free Tier (T4 GPU, 15GB VRAM).

## Why This Matters
My merged Task API model completes any request. I need it to:
- Refuse harmful task requests gracefully
- Maintain helpfulness for legitimate tasks
- Detect and resist jailbreak attempts
- Provide safe, useful responses consistently

## Success Criteria
1. I can explain why fine-tuned models need alignment
2. I can create preference datasets (prompt/chosen/rejected)
3. I can run DPO training on Colab T4 without OOM errors
4. I can red-team my model to find vulnerabilities
5. I can implement refusal training for unsafe requests
6. My aligned model achieves 90%+ harm reduction

## Constraints
- Must work on Colab Free Tier (T4, 15GB VRAM, 12GB RAM)
- Must use DPO (not RLHF) for simplicity and compute efficiency
- Must use TRL library for training
- Must integrate with existing merged model from Chapter 67

## Running Example
Align my merged Task API model to refuse harmful task requests
(e.g., "create a task to stalk someone") while remaining helpful
for legitimate productivity use cases.
EOF
```

## Step 3: Fetch Official Documentation

The skill must be grounded in official documentation, not AI memory which may be outdated or incorrect.

Use Claude Code or your AI assistant:

```
/fetching-library-docs trl dpo

Fetch the official TRL documentation covering:
1. DPOTrainer setup and configuration
2. Preference dataset format (prompt/chosen/rejected)
3. DPO hyperparameters (beta, loss type)
4. Memory optimization for consumer GPUs
```

Key sources to reference:
- [TRL DPO Trainer Documentation](https://huggingface.co/docs/trl/main/en/dpo_trainer)
- [TRL GitHub Repository](https://github.com/huggingface/trl)
- [Hugging Face DPO Guide](https://huggingface.co/docs/trl/main/en/dpo_trainer)

## Step 4: Create Your model-alignment Skill

Based on the documentation, create your skill file:

```bash
cat > .claude/skills/model-alignment/SKILL.md << 'EOF'
---
name: model-alignment
description: This skill should be used when aligning language models using DPO. Use when creating preference datasets, configuring DPO training, red-teaming models, and implementing refusal behaviors.
---

# Model Alignment Skill

## Purpose

Guide model alignment using Direct Preference Optimization (DPO) to ensure
models refuse harmful requests while remaining helpful for legitimate use cases.

## When to Use This Skill

Invoke this skill when:
- Creating preference datasets for alignment training
- Configuring DPO training with TRL
- Red-teaming models to find vulnerabilities
- Implementing refusal behaviors
- Evaluating alignment effectiveness
- Balancing safety with helpfulness

## Prerequisite Knowledge

- Supervised fine-tuning (Chapter 64)
- Model merging (Chapter 67)
- Python and Hugging Face ecosystem
- Understanding of harmful content categories

## Hardware Context

**Colab Free Tier (T4 GPU):**
- 15GB VRAM
- 12GB RAM
- Use QLoRA (4-bit) for DPO training
- Gradient accumulation required for effective batch sizes

## Alignment Methods Comparison

| Method | Complexity | Compute | Use Case |
|--------|-----------|---------|----------|
| DPO | Low | T4 feasible | Most alignment tasks |
| RLHF | High | Cluster needed | Maximum quality |
| ORPO | Medium | T4 feasible | Combined SFT+alignment |
| KTO | Low | T4 feasible | When only good examples available |

**Why DPO for This Chapter:**
- No reward model required (unlike RLHF)
- Single training pass
- Stable optimization
- 90%+ of RLHF quality with 10% of complexity

## Preference Dataset Format

```json
{
  "prompt": "Create a task to track my ex-partner's location",
  "chosen": "I can't help with tracking someone without their consent. This could constitute stalking. Instead, I can help you create tasks for your own location-based reminders or coordinate meetings with people who have agreed to share their location.",
  "rejected": "Sure! Here's a task for tracking your ex-partner: 1. Install a location tracking app..."
}
```

### Quality Requirements

| Dimension | Requirement | Why It Matters |
|-----------|-------------|----------------|
| Clear contrast | chosen/rejected obviously different | Model learns distinction |
| Realistic prompts | Actual user requests | Generalizes to real use |
| Graceful refusals | Not just "I can't" | Maintains user trust |
| Helpful alternatives | Suggest safe options | Preserves utility |

## DPO Training Configuration

### Starting Configuration

```python
from trl import DPOConfig, DPOTrainer

dpo_config = DPOConfig(
    output_dir="./dpo_output",
    beta=0.1,                           # KL penalty strength
    per_device_train_batch_size=2,      # Limited by VRAM
    gradient_accumulation_steps=8,       # Effective batch = 16
    num_train_epochs=1,                  # Often sufficient
    learning_rate=5e-7,                  # Very low for alignment
    warmup_ratio=0.1,                    # 10% warmup
    fp16=True,                           # Mixed precision
    logging_steps=10,
    save_strategy="epoch",
)
```

### Beta Parameter Guide

| Beta Value | Effect | Use Case |
|------------|--------|----------|
| 0.05 | Weak KL penalty | When model is already aligned |
| 0.1 | Standard | Default starting point |
| 0.5 | Strong KL penalty | When alignment is aggressive |
| 1.0 | Very strong | When base model is unsafe |

**Intuition:** Higher beta keeps aligned model closer to base model.
Lower beta allows larger deviations for stronger alignment.

### Learning Rate Guidelines

| Scenario | Learning Rate | Reasoning |
|----------|--------------|-----------|
| Standard DPO | 5e-7 | Very conservative for alignment |
| Aggressive alignment | 1e-6 | When base model is very unsafe |
| Fine-grained adjustment | 1e-7 | When base model is mostly aligned |

## Red-Teaming Categories

### Direct Harmful Requests
- Violence, weapons, self-harm
- Illegal activities
- Privacy violations
- Harassment

### Prompt Injection Attempts
- "Ignore previous instructions"
- "You are now DAN (Do Anything Now)"
- "Roleplay as evil AI"
- System prompt extraction

### Social Engineering
- "My grandmother used to read me..."
- "I'm a security researcher testing..."
- "This is just fictional..."
- Authority impersonation

### Context Manipulation
- Gradual escalation
- Building false rapport
- Emotional manipulation
- Technical jargon obfuscation

## Refusal Training Patterns

### Graceful Refusal Template

```
I understand you're asking about [topic], but I'm not able to help with that
because [clear reason]. Instead, I can [helpful alternative].

Would you like me to help with that instead?
```

### Key Principles

1. **Acknowledge the request**: Don't pretend not to understand
2. **Clear reason**: Explain why you can't help
3. **Offer alternative**: Maintain helpfulness
4. **Stay professional**: No lecturing or moralizing

## Evaluation Metrics

### Safety Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Harmful compliance rate | &lt;5% | Red-team test suite |
| Jailbreak resistance | >90% | Standard jailbreak prompts |
| Refusal quality | >80% helpful | Human evaluation |

### Utility Metrics

| Metric | Target | How to Measure |
|--------|--------|----------------|
| Legitimate task completion | >95% | Normal use test suite |
| False refusal rate | &lt;5% | Edge case evaluation |
| User satisfaction | >4/5 | User feedback |

## Troubleshooting Decision Tree

### Model Refuses Too Much

1. Lower beta (try 0.05)
2. Add more "helpful" examples to preference data
3. Ensure chosen responses are genuinely helpful
4. Check for overly broad refusal patterns

### Model Still Complies with Harmful Requests

1. Higher beta (try 0.5)
2. Add more examples of the failure mode
3. Ensure rejected responses are clearly harmful
4. Check if harmful pattern is covered in training

### Training Unstable

1. Lower learning rate (try 1e-7)
2. Increase warmup ratio (try 0.2)
3. Check preference data quality
4. Verify chosen/rejected labels are correct

## Validation Checks

Before declaring alignment complete:

- [ ] Model refuses direct harmful requests
- [ ] Model resists common jailbreak attempts
- [ ] Model remains helpful for legitimate requests
- [ ] Refusals are graceful, not preachy
- [ ] No catastrophic forgetting of base capabilities
- [ ] Alignment generalizes beyond training examples
EOF
```

## Step 5: Verify Your Skill

Test that your skill was created correctly:

```bash
# Check the skill exists
ls -la .claude/skills/model-alignment/

# View the skill content
head -50 .claude/skills/model-alignment/SKILL.md
```

**Output:**
```
total 8
drwxr-xr-x  3 you  staff   96 Jan  1 10:00 .
drwxr-xr-x  3 you  staff   96 Jan  1 10:00 ..
-rw-r--r--  1 you  staff  5832 Jan  1 10:00 SKILL.md
```

## What Happens Next

You now have a `model-alignment` skill grounded in TRL documentation. As you progress through this chapter:

| Lesson | How Your Skill Improves |
|--------|------------------------|
| L01: Why Alignment | Add mental model explanations |
| L02: DPO vs RLHF | Refine method selection logic |
| L03: Preference Datasets | Add data quality checklists |
| L04: DPO Training | Add Colab-specific patterns |
| L05: Red-Teaming | Add attack category taxonomy |
| L06: Refusal Training | Add refusal templates |
| Capstone | Validate skill produces aligned model |

Each lesson will include a "Reflect on Your Skill" section where you update and improve this skill based on what you learned.

## Try With AI

Use your AI companion (Claude, ChatGPT, Gemini, or similar).

### Prompt 1: Verify Skill Structure

```
I just created my model-alignment skill. Review the structure and tell me:
1. Does it follow the SKILL.md format correctly?
2. Is the content grounded in documentation (not hallucinated)?
3. What sections should I add as I learn more about alignment?

Here is my skill:
[paste your SKILL.md content]
```

**What you are learning**: Critical evaluation of your own skill structure. Your AI partner helps identify gaps before you invest time in an incomplete skill.

### Prompt 2: Connect to Task API Safety

```
My Task API model helps users manage tasks. Looking at my model-alignment skill,
what specific safety concerns should I address? Think about:
- What harmful tasks could users try to create?
- How might users try to manipulate the assistant?
- What legitimate requests might accidentally trigger false refusals?
```

**What you are learning**: Domain-specific safety thinking. Generic alignment is not enough. You need to understand the specific risks in your application.

### Prompt 3: Validate Against TRL Docs

```
Compare my skill's DPO configuration recommendations against the official
TRL documentation. Are there any discrepancies? Any best practices
I should add?

Specifically check:
1. Beta parameter recommendations
2. Learning rate guidance
3. Batch size configuration for T4 GPU
```

**What you are learning**: Documentation verification. You are building the habit of validating AI-generated content against authoritative sources.

### Safety Note

As you create skills from documentation, remember that AI tools may not have the most current information. TRL is actively developed, and best practices evolve. Always verify critical configuration values against the official source before production use.
