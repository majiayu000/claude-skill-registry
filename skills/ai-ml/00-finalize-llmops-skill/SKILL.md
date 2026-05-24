---
sidebar_position: 0
title: "Finalize Your LLMOps Skill"
description: "Consolidate all Part 8 skills into a production-ready llmops-fine-tuner skill"
keywords: [llmops, skill consolidation, digital fte, fine-tuning, production]
chapter: 72
lesson: 0
duration_minutes: 30

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill Consolidation Architecture"
    proficiency_level: "B2"
    category: "Technical"
    bloom_level: "Create"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student designs a unified skill that composes 6+ specialized skills into cohesive intelligence"

  - name: "Intelligence Integration Patterns"
    proficiency_level: "B2"
    category: "Applied"
    bloom_level: "Evaluate"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student evaluates which skill components belong in unified skill vs remain separate"

  - name: "Production Skill Validation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Safety"
    measurable_at_this_level: "Student applies verification workflow to ensure consolidated skill produces consistent results"

learning_objectives:
  - objective: "Consolidate 6+ specialized LLMOps skills into one production-ready skill"
    proficiency_level: "B2"
    bloom_level: "Create"
    assessment_method: "Review consolidated skill structure, verify all capabilities preserved"

  - objective: "Evaluate skill composition decisions using cohesion principles"
    proficiency_level: "B2"
    bloom_level: "Evaluate"
    assessment_method: "Justify which components merged vs separated based on cohesion analysis"

  - objective: "Validate consolidated skill through comprehensive testing"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Execute skill on test scenarios, verify outputs match specialized skill quality"

cognitive_load:
  new_concepts: 4
  assessment: "4 concepts (skill consolidation, cohesion analysis, capability preservation, production validation) within B1-B2 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Design skill versioning strategy and backwards compatibility approach"
  remedial_for_struggling: "Focus on consolidating just 3 skills (data, training, deployment) before adding remaining"
---

# Finalize Your LLMOps Skill

Throughout Part 8, you built specialized skills for each LLMOps capability:

| Chapter | Skill | Capability |
|---------|-------|------------|
| 61 | `llmops-decision-framework` | When to fine-tune |
| 62 | `llmops-compute-planner` | VRAM budgeting |
| 63 | `llmops-data-engineer` | Dataset creation |
| 64 | `llmops-fine-tuner` | Training workflows |
| 67 | `model-merging` | Adapter combination |
| 68 | `model-alignment` | DPO safety |
| 69 | `model-evaluation` | Quality gates |
| 70 | `model-serving` | Deployment |
| 71 | `agent-integration` | Framework connection |

Now you will consolidate these into one production-ready `llmops-fine-tuner` skill that composes all capabilities. This is Layer 3 work: transforming specialized knowledge into reusable intelligence.

## Why Consolidation Matters

**The Problem with 9 Separate Skills:**

When you need to fine-tune a model for production, you currently must:

1. Invoke `llmops-decision-framework` to determine if fine-tuning is appropriate
2. Invoke `llmops-compute-planner` to budget VRAM
3. Invoke `llmops-data-engineer` to create datasets
4. Invoke `llmops-fine-tuner` for training
5. Invoke `model-evaluation` for quality gates
6. Invoke `model-serving` for deployment
7. Invoke `agent-integration` for framework connection

That is 7 separate skill invocations with manual handoffs between each. Errors compound. Context is lost.

**The Solution: Unified Orchestration**

A consolidated skill:

- Accepts a single specification
- Orchestrates all pipeline stages internally
- Maintains context across stages
- Produces a deployable Digital FTE

This transforms your skills from **components** into a **product**.

## Skill Consolidation Architecture

### The Composition Pattern

Your consolidated skill follows this architecture:

```
llmops-fine-tuner (Unified)
├── Decision Layer
│   └── When to fine-tune? (from Ch.61)
│
├── Planning Layer
│   └── Compute requirements (from Ch.62)
│
├── Data Layer
│   └── Dataset creation (from Ch.63)
│
├── Training Layer
│   ├── Fine-tuning (from Ch.64)
│   ├── Merging (from Ch.67)
│   └── Alignment (from Ch.68)
│
├── Validation Layer
│   └── Quality gates (from Ch.69)
│
└── Deployment Layer
    ├── Serving (from Ch.70)
    └── Integration (from Ch.71)
```

### Cohesion Analysis

Not all skills should merge. Ask:

| Question | Keep Separate If... | Merge If... |
|----------|---------------------|-------------|
| **Usage frequency** | Used independently often | Always used together |
| **Domain coupling** | Different expertise needed | Same expertise |
| **Execution context** | Different environments | Same environment |
| **Failure isolation** | Need to retry independently | Fail together, succeed together |

**Analysis for LLMOps Skills:**

| Skill | Verdict | Reasoning |
|-------|---------|-----------|
| `llmops-decision-framework` | **Merge** | Always first step, gates everything |
| `llmops-compute-planner` | **Merge** | Informs all training decisions |
| `llmops-data-engineer` | **Merge** | Pipeline stage, not standalone |
| `llmops-fine-tuner` | **Core** | Central skill, others compose around it |
| `model-merging` | **Merge** | Optional but integrated |
| `model-alignment` | **Merge** | Optional but integrated |
| `model-evaluation` | **Merge** | Always required, gates deployment |
| `model-serving` | **Merge** | Pipeline terminus |
| `agent-integration` | **Merge** | Final step, produces Digital FTE |

**Result:** All skills merge into unified `llmops-fine-tuner`.

## Creating Your Consolidated Skill

### Step 1: Define the Unified SKILL.md

Create your consolidated skill:

```bash
mkdir -p .claude/skills/llmops-fine-tuner
```

**SKILL.md Structure:**

```markdown
---
name: llmops-fine-tuner
description: "End-to-end LLMOps pipeline for fine-tuning, evaluating, and deploying custom models as Digital FTEs. Use when building production model deployments."
---

# LLMOps Fine-Tuner Skill

## Purpose

Complete pipeline from specification to deployed Digital FTE.

## When to Use

- Building custom models for specific domains
- Creating proprietary AI products
- Deploying fine-tuned models to production

## Pipeline Stages

### Stage 1: Decision (from Ch.61)
Evaluate whether fine-tuning is appropriate for this use case.

[Include decision framework here]

### Stage 2: Planning (from Ch.62)
Calculate VRAM budget and hardware requirements.

[Include compute planning here]

### Stage 3: Data (from Ch.63)
Create and validate training dataset.

[Include data engineering here]

### Stage 4: Training (from Ch.64, 67, 68)
Execute fine-tuning with optional merging and alignment.

[Include training workflows here]

### Stage 5: Evaluation (from Ch.69)
Run quality gates before deployment.

[Include evaluation criteria here]

### Stage 6: Deployment (from Ch.70, 71)
Deploy model and integrate with agent frameworks.

[Include deployment and integration here]

## Specification Template

When invoking this skill, provide:

- **Domain**: What expertise is this model encoding?
- **Base Model**: Which model to fine-tune
- **Dataset Source**: Where does training data come from
- **Quality Target**: What accuracy threshold for deployment
- **Deployment Target**: Where model will run (Ollama, API, etc.)

## Constraints

- Colab Free Tier compatible (T4 GPU)
- Total cost < $1
- Completion time < 4 hours
```

### Step 2: Merge Skill Content

For each specialized skill, extract the core patterns and integrate:

**From `llmops-decision-framework`:**
```python
# Decision criteria
def should_fine_tune(use_case):
    """
    Returns True if fine-tuning is appropriate.

    Fine-tune when:
    - Prompting consistently fails (>30% error rate)
    - Domain requires specialized vocabulary
    - Latency requirements mandate smaller model
    - Cost optimization requires local deployment

    Don't fine-tune when:
    - Prompting achieves 90%+ accuracy
    - Task is one-off or experimental
    - No clear evaluation criteria exist
    """
    pass
```

**From `llmops-compute-planner`:**
```python
# VRAM budget calculation
def calculate_vram_budget(model_size_b, batch_size=1, lora_rank=16):
    """
    Estimate VRAM requirements for training.

    Formula: VRAM = model_params * 4 bytes + optimizer_state * 8 bytes + activations
    With LoRA: Reduce by ~80% (only training adapter weights)

    T4 GPU (16GB):
    - 1B params: Works with batch_size=4
    - 3B params: Works with batch_size=2
    - 7B params: Works with batch_size=1, gradient_checkpointing
    - 8B params: Works with 4-bit quantization
    """
    pass
```

**From `llmops-data-engineer`:**
```python
# Dataset creation patterns
def create_training_dataset(examples, format="chat"):
    """
    Create JSONL dataset for fine-tuning.

    Format options:
    - chat: {"messages": [{"role": "user", "content": ...}, ...]}
    - instruct: {"instruction": ..., "input": ..., "output": ...}
    - completion: {"text": "Input: ... Output: ..."}
    """
    pass
```

### Step 3: Define Handoff Protocols

Each stage produces artifacts consumed by the next:

```
Stage 1 (Decision) → decision_report.json
    └── Inputs: use_case_description
    └── Outputs: should_proceed, reasoning, constraints

Stage 2 (Planning) → compute_plan.json
    └── Inputs: decision_report, model_choice
    └── Outputs: vram_budget, batch_size, hardware_requirements

Stage 3 (Data) → dataset.jsonl + data_report.json
    └── Inputs: raw_examples, format_spec
    └── Outputs: training_data, validation_data, quality_metrics

Stage 4 (Training) → adapter_weights/ + training_report.json
    └── Inputs: base_model, dataset, compute_plan
    └── Outputs: trained_adapter, loss_curves, checkpoint_path

Stage 5 (Evaluation) → eval_report.json
    └── Inputs: trained_model, test_dataset, quality_thresholds
    └── Outputs: accuracy, pass_fail, regression_analysis

Stage 6 (Deployment) → deployed_model + integration_config.json
    └── Inputs: trained_model, deployment_target
    └── Outputs: model_endpoint, ollama_modelfile, agent_config
```

### Step 4: Validate Consolidation

Test your consolidated skill end-to-end:

```bash
# Test with minimal example
claude --skill llmops-fine-tuner "
Create a Task API model:
- Domain: Task management tool-calling
- Base: Qwen 2.5 3B Instruct
- Data: 200 synthetic examples
- Target: 90% tool-calling accuracy
- Deploy: Local Ollama
"
```

**Expected Output:**
```
Stage 1: Decision PASS - Fine-tuning appropriate for tool-calling specialization
Stage 2: Planning COMPLETE - T4 compatible, batch_size=2, LoRA rank=16
Stage 3: Data COMPLETE - 200 examples generated, 80/20 train/val split
Stage 4: Training COMPLETE - Loss converged: 0.12, Epoch 3/3
Stage 5: Evaluation PASS - Tool accuracy: 94%, threshold: 90%
Stage 6: Deployment COMPLETE - Ollama model registered: task-api-qwen3b

Digital FTE Ready: task-api-qwen3b
```

## Capability Preservation Checklist

Verify your consolidated skill preserves all original capabilities:

| Original Skill | Key Capability | Preserved? | Test |
|----------------|---------------|------------|------|
| `llmops-decision-framework` | Decision tree logic | [ ] | "Should I fine-tune for X?" |
| `llmops-compute-planner` | VRAM calculation | [ ] | "What hardware for 8B model?" |
| `llmops-data-engineer` | JSONL generation | [ ] | "Create dataset from examples" |
| `llmops-fine-tuner` | Training workflow | [ ] | "Fine-tune with these params" |
| `model-merging` | Adapter combination | [ ] | "Merge these LoRA adapters" |
| `model-alignment` | DPO training | [ ] | "Align model for safety" |
| `model-evaluation` | Quality gates | [ ] | "Evaluate against benchmarks" |
| `model-serving` | Deployment | [ ] | "Deploy to Ollama" |
| `agent-integration` | Framework connection | [ ] | "Connect to OpenAI SDK" |

## Production Readiness Criteria

Your consolidated skill is production-ready when:

1. **Single Invocation**: Full pipeline from one specification
2. **Stage Visibility**: Clear progress reporting for each stage
3. **Error Recovery**: Graceful handling with stage-specific retry
4. **Artifact Persistence**: All intermediate outputs saved for debugging
5. **Constraint Compliance**: Stays within Colab Free Tier limits
6. **Consistent Quality**: Produces equivalent results to individual skills

## What You Built

Your consolidated `llmops-fine-tuner` skill:

| Capability | Source | Integration |
|------------|--------|-------------|
| Decision logic | Ch.61 | Stage 1 gate |
| VRAM budgeting | Ch.62 | Planning layer |
| Data creation | Ch.63 | Automatic dataset prep |
| Training workflows | Ch.64, 67, 68 | Core execution |
| Quality gates | Ch.69 | Pre-deployment validation |
| Deployment | Ch.70, 71 | Final stage automation |

This is **intelligence accumulation**: 11 chapters of knowledge compressed into one reusable skill.

## Try With AI

### Prompt 1: Design Your Skill Structure

```
I'm consolidating these LLMOps skills into one unified skill:
- Decision framework (when to fine-tune)
- Compute planning (VRAM budgeting)
- Data engineering (dataset creation)
- Training (fine-tuning, merging, alignment)
- Evaluation (quality gates)
- Deployment (serving, integration)

Help me design the SKILL.md structure. What sections should it have?
How should stages hand off to each other? What specification template
should users provide when invoking this skill?
```

**What you're learning**: Skill architecture design—how to structure reusable intelligence for production use.

### Prompt 2: Test Capability Preservation

```
I've consolidated my LLMOps skills. Help me create a test plan to verify
all capabilities are preserved. For each original skill, give me:
1. A test prompt that exercises that capability
2. Expected output that proves it works
3. A failure mode to watch for
```

**What you're learning**: Validation methodology—ensuring consolidation doesn't lose specialized capabilities.

### Prompt 3: Connect to Your Domain

```
I'm building a consolidated LLMOps skill for [your domain: legal, medical,
finance, etc.]. My original skills handle [list your specialized skills].
Help me analyze: Which skills should merge? Which should stay separate?
Ask me questions about how I use each skill to determine the right
composition.
```

**What you're learning**: Cohesion analysis—understanding when to merge vs. separate based on usage patterns.

### Safety Note

When consolidating skills, preserve all safety mechanisms from individual skills. A unified skill must maintain the same guardrails as its components—never optimize away safety checks for convenience.
