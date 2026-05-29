---
sidebar_position: 0
title: "Build Your Evaluation Skill"
description: "Create a reusable skill for evaluating fine-tuned models, benchmarking performance, and detecting quality regressions"
chapter: 69
lesson: 0
duration_minutes: 25

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill Creation from Documentation"
    proficiency_level: "B1"
    category: "Technical"
    bloom_level: "Apply"
    digcomp_area: "Digital Content Creation"
    measurable_at_this_level: "Student can create a functional skill from official library documentation using Context7"

  - name: "Evaluation Framework Understanding"
    proficiency_level: "B1"
    category: "Conceptual"
    bloom_level: "Understand"
    digcomp_area: "Information Literacy"
    measurable_at_this_level: "Student can explain the purpose of lm-evaluation-harness and its role in model quality assurance"

  - name: "Learning Specification Writing"
    proficiency_level: "B1"
    category: "Applied"
    bloom_level: "Apply"
    digcomp_area: "Problem-Solving"
    measurable_at_this_level: "Student can write a LEARNING-SPEC.md that captures what they want to learn and success criteria"

learning_objectives:
  - objective: "Create a fresh skills-lab environment for evaluation work"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Successful execution of clone and setup commands"

  - objective: "Write a LEARNING-SPEC.md defining evaluation learning goals"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Specification includes clear intent, constraints, and success criteria"

  - objective: "Fetch official lm-evaluation-harness documentation using Context7"
    proficiency_level: "B1"
    bloom_level: "Apply"
    assessment_method: "Documentation retrieved and core concepts identified"

  - objective: "Create an initial llmops-evaluator skill from fetched documentation"
    proficiency_level: "B1"
    bloom_level: "Create"
    assessment_method: "Skill file exists with evaluation decision frameworks"

cognitive_load:
  new_concepts: 5
  assessment: "5 concepts (skill-first pattern, LEARNING-SPEC, Context7 workflow, lm-eval-harness, evaluation metrics) within B1 limit (7-10 concepts)"

differentiation:
  extension_for_advanced: "Explore additional benchmarks like MMLU, HellaSwag, or custom task creation"
  remedial_for_struggling: "Focus on setting up the skill file; defer benchmark details to later lessons"
---

# Build Your Evaluation Skill

Before learning about model evaluation, you will build the skill that captures that knowledge. This skill-first approach means every concept you learn gets encoded into a reusable asset that becomes part of your Digital FTE toolkit.

When you fine-tune a model, how do you know it actually improved? A model might generate fluent text that completely misses the point. Evaluation frameworks provide systematic methods to measure what matters: accuracy, format compliance, reasoning quality, and safety. By the end of this chapter, you will have a skill that guides evaluation decisions for any fine-tuned model.

## Step 1: Clone Skills Lab Fresh

Every chapter starts with a clean environment. This prevents state pollution from previous work and ensures reproducible results.

```bash
# Navigate to your workspace
cd ~/workspace

# Clone fresh skills-lab (or reset if exists)
if [ -d "skills-lab-llmops" ]; then
    rm -rf skills-lab-llmops
fi

git clone https://github.com/panaversity/skills-lab.git skills-lab-llmops
cd skills-lab-llmops

# Create chapter directory
mkdir -p llmops-evaluation
cd llmops-evaluation
```

**Output:**
```
Cloning into 'skills-lab-llmops'...
remote: Enumerating objects: 156, done.
remote: Counting objects: 100% (156/156), done.
Receiving objects: 100% (156/156), 45.23 KiB | 2.26 MiB/s, done.
```

## Step 2: Write Your LEARNING-SPEC.md

Before fetching documentation, articulate what you want to learn. This specification drives focused learning.

Create `LEARNING-SPEC.md`:

```markdown
# Learning Specification: LLM Evaluation & Quality Gates

## Intent

Learn to systematically evaluate fine-tuned models to ensure they meet quality standards before deployment.

## What I Want to Learn

1. **Evaluation Taxonomy**: What metrics matter for different use cases?
2. **LLM-as-Judge**: How to use GPT-4 as an evaluator for subjective quality
3. **Benchmark Design**: How to create task-specific benchmarks for the Task API
4. **Regression Testing**: How to detect when model quality degrades
5. **Quality Gates**: How to define pass/fail thresholds for deployment

## Success Criteria

- [ ] I can select appropriate evaluation metrics for a given task
- [ ] I can implement LLM-as-Judge with structured rubrics
- [ ] I can create a custom benchmark for JSON output validation
- [ ] I can detect quality regression between model versions
- [ ] I can define quality gates that block bad deployments

## Constraints

- Must work on Colab Free Tier (T4, 15GB VRAM)
- Focus on practical evaluation, not research benchmarks
- Use lm-evaluation-harness as the primary tool
- Integrate with Task API from Chapter 40

## Prior Knowledge

- Chapter 64: SFT fundamentals
- Chapter 65-68: Various fine-tuning approaches
- Chapter 40: Task API structure

## Time Budget

- This lesson: 25 minutes (skill creation)
- Full chapter: ~4 hours (all evaluation concepts)
```

## Step 3: Fetch Official Documentation

Use Context7 to retrieve the authoritative lm-evaluation-harness documentation. This ensures your skill is grounded in official patterns, not hallucinated best practices.

```
/fetching-library-docs lm-evaluation-harness
```

**Key concepts to extract from documentation:**

| Concept | What It Means |
|---------|---------------|
| **Task** | A specific evaluation benchmark (e.g., "hellaswag", "mmlu") |
| **Model** | The model being evaluated (supports HuggingFace, OpenAI, local) |
| **Metric** | What gets measured (accuracy, perplexity, exact match) |
| **Few-shot** | Number of examples provided in prompt before evaluation |
| **Log-likelihood** | Probability the model assigns to correct answer |

## Step 4: Create Your Initial Skill

Create `llmops-evaluator/SKILL.md`:

```markdown
---
name: llmops-evaluator
description: "This skill should be used when evaluating fine-tuned LLM quality. Use when selecting metrics, designing benchmarks, running evaluations, or setting quality gates for model deployment."
---

# LLMOps Evaluator Skill

## When to Use This Skill

Invoke this skill when you need to:
- Evaluate a fine-tuned model before deployment
- Compare model versions for regression
- Design custom benchmarks for your use case
- Set pass/fail thresholds for CI/CD pipelines
- Debug why a model is underperforming

## Evaluation Decision Framework

### Step 1: Identify Evaluation Type

| Use Case | Evaluation Type | Primary Metrics |
|----------|----------------|-----------------|
| Classification | Accuracy-based | Accuracy, F1, Precision, Recall |
| Generation | Quality-based | Perplexity, BLEU, ROUGE |
| Instruction-following | LLM-as-Judge | Rubric scores (1-5) |
| JSON output | Format validation | Schema compliance rate |
| Safety | Red-teaming | Harmful response rate |

### Step 2: Select Benchmarks

**Standard Benchmarks** (for general capability):
- **MMLU**: General knowledge across domains
- **HellaSwag**: Common-sense reasoning
- **ARC**: Science reasoning
- **TruthfulQA**: Factual accuracy

**Task-Specific Benchmarks** (for your domain):
- Create custom evaluation sets matching your use case
- Minimum: 100 examples for reliable measurement
- Include edge cases and failure modes

### Step 3: Run Evaluation

```bash
# Basic evaluation with lm-eval-harness
lm_eval --model hf \
    --model_args pretrained=my-fine-tuned-model \
    --tasks hellaswag,arc_easy \
    --batch_size 8 \
    --output_path ./results
```

### Step 4: Define Quality Gates

**Deployment Thresholds**:
- Accuracy: > 85% on task-specific benchmark
- Harmful response rate: < 5%
- Schema compliance: > 95% for JSON output
- Regression: New model >= Previous model - 2%

## Common Patterns

### Pattern 1: A/B Model Comparison

```python
def compare_models(model_a_results, model_b_results, threshold=0.02):
    """Compare two models and determine if B is a regression from A."""
    delta = model_b_results['accuracy'] - model_a_results['accuracy']
    if delta &lt; -threshold:
        return "REGRESSION", f"Model B is {abs(delta):.2%} worse"
    elif delta > threshold:
        return "IMPROVEMENT", f"Model B is {delta:.2%} better"
    else:
        return "EQUIVALENT", f"Within {threshold:.2%} threshold"
```

### Pattern 2: LLM-as-Judge Template

```python
JUDGE_PROMPT = """
Evaluate the assistant's response on a scale of 1-5:

User Request: {input}
Assistant Response: {output}
Expected Behavior: {expected}

Criteria:
- Accuracy: Does the response correctly address the request?
- Format: Does the response follow the expected format?
- Helpfulness: Is the response useful and complete?

Score (1-5):
Reasoning:
"""
```

## Quality Gate Checklist

Before deploying a fine-tuned model, verify:

- [ ] Task-specific accuracy > threshold
- [ ] No regression from previous version
- [ ] Format compliance verified
- [ ] Safety evaluation passed
- [ ] Cost/latency within budget
```

## Step 5: Verify Skill Works

Test that your skill provides useful guidance:

```bash
# Verify skill file exists and is valid
cat llmops-evaluator/SKILL.md | head -20
```

**Output:**
```
---
name: llmops-evaluator
description: "This skill should be used when evaluating fine-tuned LLM quality..."
---

# LLMOps Evaluator Skill
...
```

Your skill now exists as a starting point. As you progress through this chapter, you will add:
- Detailed evaluation taxonomy (L01)
- LLM-as-Judge implementation patterns (L02)
- Task-specific benchmark design (L03)
- Regression testing workflows (L04)
- Quality gate configurations (L05)

## Skill Evolution Map

Track how your skill grows through this chapter:

| Lesson | What Gets Added |
|--------|----------------|
| L00 (now) | Initial framework, basic decision tree |
| L01 | Evaluation taxonomy, metric selection guide |
| L02 | LLM-as-Judge prompts and rubrics |
| L03 | Custom benchmark creation patterns |
| L04 | A/B testing, regression detection |
| L05 | CI/CD gate configurations |
| L06 | Complete pipeline integration |

## Try With AI

### Prompt 1: Review Your LEARNING-SPEC

```
I wrote this LEARNING-SPEC.md for learning LLM evaluation:

[paste your LEARNING-SPEC.md]

1. Are my success criteria specific and measurable?
2. What am I missing that would be important for production evaluation?
3. Do my constraints match real-world limitations?
```

**What you are learning**: Specification refinement. Your AI partner helps identify gaps in your learning goals before you invest time in the wrong direction.

### Prompt 2: Expand the Skill Framework

```
I'm building an llmops-evaluator skill. Review my initial framework:

[paste your SKILL.md]

Suggest 3 additional decision frameworks I should include for:
1. Choosing between automated metrics vs human evaluation
2. Determining sample size for reliable benchmarks
3. Handling evaluation of creative/open-ended outputs
```

**What you are learning**: Skill architecture. Evaluation has many dimensions. Your AI partner helps identify frameworks you might not have considered.

### Prompt 3: Connect to Task API

```
My fine-tuned model outputs JSON for a Task API with this schema:

{
  "action": "create|complete|list|delete",
  "title": "string",
  "priority": "low|medium|high",
  "due_date": "string|null"
}

Design 5 evaluation test cases that would catch common failure modes:
- Invalid JSON
- Missing required fields
- Wrong action selection
- Inappropriate priority assignment
- Format consistency issues
```

**What you are learning**: Domain-specific evaluation design. Generic benchmarks miss your specific requirements. Your AI partner helps design tests that match your actual use case.

### Safety Note

As you build evaluation frameworks, remember that evaluation can give false confidence. A model passing benchmarks does not guarantee safety in deployment. Always include human review for novel situations and maintain logging for post-deployment monitoring.
