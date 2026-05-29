---
title: "Build Your LLMOps Decision Skill"
sidebar_position: 7
chapter: 61
lesson: 7
duration_minutes: 45

# HIDDEN SKILLS METADATA
skills:
  - name: "Skill Creation"
    proficiency_level: "B2"
    category: "Applied"
    bloom_level: "Create"
    digcomp_area: "AI and Machine Learning"
    measurable_at_this_level: "Student creates functional skill file following correct structure"

  - name: "LLMOps Decision Framework"
    proficiency_level: "B2"
    category: "Applied"
    bloom_level: "Evaluate"
    digcomp_area: "AI and Machine Learning"
    measurable_at_this_level: "Student applies decision framework to evaluate fine-tuning suitability"

  - name: "Knowledge Encoding"
    proficiency_level: "B2"
    category: "Conceptual"
    bloom_level: "Analyze"
    digcomp_area: "AI and Machine Learning"
    measurable_at_this_level: "Student extracts reusable patterns from chapter learnings"

learning_objectives:
  - objective: "Create a reusable LLMOps decision skill from chapter learnings"
    proficiency_level: "B2"
    bloom_level: "Create"
    assessment_method: "Skill file validates against schema and produces correct guidance"

  - objective: "Encode decision frameworks as structured prompts and criteria"
    proficiency_level: "B2"
    bloom_level: "Synthesize"
    assessment_method: "Skill includes complete decision tree with criteria"

  - objective: "Test and iterate skill quality through practical application"
    proficiency_level: "B2"
    bloom_level: "Evaluate"
    assessment_method: "Student identifies skill gaps and implements improvements"

cognitive_load:
  new_concepts: 4
  assessment: "Skill structure, persona definition, decision encoding, skill testing - moderate load as synthesizing prior knowledge"

differentiation:
  extension_for_advanced: "Add multiple decision trees for different stages; include cost calculators"
  remedial_for_struggling: "Start with provided template; focus on filling in content rather than structure"

generated_by: "content-implementer"
created: "2026-01-01"
---

# Build Your LLMOps Decision Skill

You've spent this chapter building mental models: the LLMOps lifecycle, training taxonomy, economic analysis, use case specification. All valuable knowledge—but knowledge fades. Six months from now, you won't remember the exact criteria for choosing DPO over RLHF.

That's why we encode knowledge into skills.

This lesson transforms your chapter learnings into a reusable **llmops-decision-framework** skill. Every future LLMOps project starts with this skill providing structured guidance. The knowledge compounds instead of disappearing.

## What Makes a Good Decision Skill?

Decision skills differ from procedural skills. You're not encoding "how to train a model" (that's procedural). You're encoding "how to decide WHAT training approach fits this situation."

Effective decision skills include:

1. **Clear activation criteria** — When should this skill be invoked?
2. **Structured questions** — What must I analyze before deciding?
3. **Decision frameworks** — Given inputs, how do I select the right approach?
4. **Trade-off analysis** — What am I gaining and losing with each choice?
5. **Red flags** — What signals indicate I'm on the wrong path?

## The Skill Structure

Skills live in `.claude/skills/` as directories containing `SKILL.md`. The file has two parts:

**YAML Frontmatter**: Metadata for tool integration
**Markdown Body**: The actual skill content

Here's the target structure for your LLMOps decision skill:

```
.claude/skills/
└── llmops-decision-framework/
    └── SKILL.md
```

## Building Your Skill

Let's construct this skill by extracting knowledge from each lesson.

### Step 1: Define the Activation Criteria

When should this skill be invoked? Write the opening that tells AI when to use it:

```markdown
---
name: llmops-decision-framework
description: "This skill should be used when evaluating whether fine-tuning is appropriate for an LLMOps project. Use when analyzing domain use cases, comparing training methods, calculating ROI, or deciding between API-based and self-hosted solutions."
---

# LLMOps Decision Framework

## When to Use This Skill

Invoke this skill when you need to:
- Decide whether to fine-tune a model for a specific use case
- Choose between training approaches (SFT, DPO, RLHF)
- Calculate ROI for an LLMOps investment
- Compare API-based vs self-hosted inference
- Scope a fine-tuning project

**Do not use this skill for**:
- Actual training implementation (see training-specific skills)
- Data preparation procedures
- Model deployment configuration
```

### Step 2: Encode the Decision Criteria

Extract the key decision points from Lesson 3 (When to Fine-Tune):

```markdown
## Fine-Tuning Decision Framework

### Primary Question: Should You Fine-Tune?

**Evaluate each criterion (all must be YES to proceed)**:

| Criterion | Question | Red Flag if NO |
|-----------|----------|----------------|
| Capability Gap | Does your task require something current models can't do well? | If prompt engineering works, fine-tuning is overkill |
| Data Availability | Do you have (or can create) 500+ quality examples? | Without data, fine-tuning is impossible |
| Stability | Is the target behavior stable for 6+ months? | Frequent changes waste training investment |
| Measurability | Can you objectively evaluate model quality? | Without metrics, you can't know if it worked |
| Resource Commitment | Can you invest 40+ hours in the project? | Rushed projects fail |

### Decision Tree

```
Is there a genuine capability gap?
├── NO → Improve prompting first
└── YES → Do you have or can create 500+ examples?
    ├── NO → Build data pipeline first
    └── YES → Is the target stable for 6+ months?
        ├── NO → Consider RAG or in-context learning
        └── YES → PROCEED TO TRAINING METHOD SELECTION
```
```

### Step 3: Add the Training Method Selection

From Lesson 4 (Training Taxonomy):

```markdown
## Training Method Selection

### Method Decision Tree

```
What do you need?
├── New capabilities the model lacks
│   └── → SFT with domain-specific examples
├── Better output quality on existing tasks
│   └── → SFT with high-quality examples
├── Different response style or persona
│   └── → SFT (dramatic changes) or DPO (refinement)
└── Safer or more aligned outputs
    └── → DPO (simpler) or RLHF (more powerful)
```

### Hardware Constraints Decision

```
What GPU do you have access to?
├── Consumer GPU (8-16 GB VRAM)
│   └── → QLoRA is your only option for 7B+ models
├── Professional GPU (24-48 GB VRAM)
│   └── → LoRA or full fine-tuning possible
└── Cloud cluster (80+ GB VRAM)
    └── → Any method viable; optimize for quality
```

### Method Comparison Matrix

| Need | SFT | DPO | RLHF | QLoRA |
|------|-----|-----|------|-------|
| Domain expertise | Primary | - | - | Enabler |
| Output format | Primary | - | - | Enabler |
| Persona/style | Good | Better | - | Enabler |
| Safety alignment | - | Primary | Most powerful | Enabler |
| Consumer hardware | - | - | - | Required |
```

### Step 4: Include Economic Analysis Framework

From Lesson 5 (Economics):

```markdown
## Economic Analysis Framework

### Quick ROI Assessment

**Calculate these four numbers**:

1. **Current Cost** = (Hours per task) × (Hourly rate) × (Tasks/month)
2. **Future Cost** = Infrastructure + Maintenance + Human oversight
3. **Monthly Savings** = Current Cost - Future Cost
4. **Investment** = Development + Training + Setup

**Decision rules**:
- Payback < 3 months → Strong project
- Payback 3-12 months → Good project (verify assumptions)
- Payback > 12 months → Reconsider (unless strategic value)

### Break-Even Analysis

**API vs Self-Hosted break-even**:
```
Break-Even Queries = Fixed Costs / (API Cost per Query - Self-Host Cost per Query)
```

**Rule of thumb**:
- < 100K queries/month → API usually cheaper
- 100K-1M queries/month → Calculate carefully
- > 1M queries/month → Self-hosting usually wins

### Hidden Cost Checklist

Before finalizing budget, verify you've included:
- [ ] Data preparation (40-100 hours typical)
- [ ] Evaluation development (20-40 hours typical)
- [ ] Infrastructure setup (5-20 hours)
- [ ] Iteration multiplier (3-10x base estimates)
- [ ] Ongoing maintenance (5-10 hours/month)
```

### Step 5: Add Use Case Specification Template

From Lesson 6 (Use Case Analysis):

```markdown
## Use Case Specification Template

When scoping an LLMOps project, document:

### 1. Executive Summary
- One paragraph: What are you building and why?

### 2. Capability Requirements
| Capability | Description | Priority | Measurable Target |
|------------|-------------|----------|-------------------|
| | | | |

### 3. Gap Analysis
- Current state: [What exists today]
- Current performance: [Metrics]
- Target performance: [Metrics]

### 4. Training Data Strategy
- Total examples: [MVP] scaling to [Target]
- Distribution by category:
  - [Category 1]: [%]
  - [Category 2]: [%]
- Data sources: [List]

### 5. Success Criteria
| Metric | Target | Measurement Method |
|--------|--------|-------------------|
| | | |

### 6. Risks and Mitigations
| Risk | Impact | Mitigation |
|------|--------|------------|
| | | |

### 7. Go/No-Go Criteria
- Proceed if: [Conditions]
- Revisit if: [Conditions]
```

### Step 6: Add Red Flags and Anti-Patterns

From your accumulated learning:

```markdown
## Red Flags and Anti-Patterns

### Signs Fine-Tuning Is Wrong for This Project

- **"We want the model to know everything about X"** — Fine-tuning adds patterns, not encyclopedic knowledge. Use RAG for knowledge retrieval.

- **"Our requirements change frequently"** — Each requirement change needs retraining. Consider prompt engineering or RAG.

- **"We don't have time to create examples"** — No examples = no fine-tuning. There are no shortcuts.

- **"Training will fix our prompt quality issues"** — If prompts are bad, training data will be bad. Fix prompts first.

- **"We need 100% accuracy"** — Models are probabilistic. Plan for validation layers, not perfection.

### Signs You Should Proceed

- **Consistent capability gap** — Prompt engineering demonstrably insufficient
- **Clear success metrics** — You know what "better" means and can measure it
- **Stable requirements** — Target behavior won't change for months
- **Available data** — You have or can create sufficient examples
- **Resource commitment** — Team can dedicate focused time
```

## The Complete Skill

Assemble all sections into your final `SKILL.md`:

```markdown
---
name: llmops-decision-framework
description: "This skill should be used when evaluating whether fine-tuning is appropriate for an LLMOps project. Use when analyzing domain use cases, comparing training methods, calculating ROI, or deciding between API-based and self-hosted solutions."
---

# LLMOps Decision Framework

## When to Use This Skill

Invoke this skill when you need to:
- Decide whether to fine-tune a model for a specific use case
- Choose between training approaches (SFT, DPO, RLHF)
- Calculate ROI for an LLMOps investment
- Compare API-based vs self-hosted inference
- Scope a fine-tuning project

**Do not use this skill for**:
- Actual training implementation (see training-specific skills)
- Data preparation procedures
- Model deployment configuration

---

## Fine-Tuning Decision Framework

### Primary Question: Should You Fine-Tune?

**All criteria must be YES to proceed**:

| Criterion | Question | Red Flag if NO |
|-----------|----------|----------------|
| Capability Gap | Does your task require something current models can't do well? | If prompt engineering works, fine-tuning is overkill |
| Data Availability | Do you have (or can create) 500+ quality examples? | Without data, fine-tuning is impossible |
| Stability | Is the target behavior stable for 6+ months? | Frequent changes waste training investment |
| Measurability | Can you objectively evaluate model quality? | Without metrics, you can't know if it worked |
| Resource Commitment | Can you invest 40+ hours in the project? | Rushed projects fail |

### Decision Flow

1. Evaluate all five criteria
2. If any criterion is NO → Address that gap first
3. If all criteria are YES → Proceed to training method selection

---

## Training Method Selection

### What training method fits your need?

| Need | Primary Method | Notes |
|------|---------------|-------|
| New domain expertise | SFT | Train on domain-specific input/output pairs |
| Consistent output format | SFT | Train on correctly formatted examples |
| Persona or style change | SFT or DPO | SFT for major changes, DPO for refinement |
| Safety alignment | DPO or RLHF | DPO is simpler; RLHF for complex alignment |
| Behavior refinement | DPO | Train on preference pairs |

### Hardware constraints

| Available VRAM | Recommended Method | Max Model Size |
|---------------|-------------------|----------------|
| 8-16 GB | QLoRA | 7-13B |
| 24-48 GB | LoRA or Full FT | 13-70B with LoRA |
| 80+ GB | Any method | Any size |

---

## Economic Analysis

### Quick ROI Check

1. **Current monthly cost** = Manual hours × Hourly rate × Volume
2. **Future monthly cost** = Infrastructure + Maintenance + Oversight
3. **Monthly savings** = Current - Future
4. **Total investment** = Development + Training + Setup
5. **Payback period** = Investment / Monthly savings

**Decision guide**:
- Payback < 3 months → Strong project, proceed
- Payback 3-12 months → Good project, verify assumptions
- Payback > 12 months → Reconsider unless strategic

### API vs Self-Hosting

**Rule of thumb by query volume**:
- < 100K/month → API typically cheaper (no infrastructure)
- 100K-1M/month → Calculate break-even carefully
- > 1M/month → Self-hosting typically wins

### Hidden Costs Checklist

Verify budget includes:
- [ ] Data preparation: 40-100 hours
- [ ] Evaluation development: 20-40 hours
- [ ] Infrastructure setup: 5-20 hours
- [ ] Iteration cycles: 3-10x training runs
- [ ] Ongoing maintenance: 5-10 hours/month

---

## Use Case Specification Template

### Required Sections

1. **Executive Summary** — One paragraph: what and why
2. **Capability Requirements** — Table with measurable targets
3. **Gap Analysis** — Current vs target state
4. **Training Data Strategy** — Volume, distribution, sources
5. **Success Criteria** — Metrics and measurement methods
6. **Risks and Mitigations** — Known risks with plans
7. **Go/No-Go Criteria** — Decision boundaries

---

## Red Flags

Stop and reconsider if you hear:

- "We want the model to know everything about X" → Use RAG for knowledge
- "Requirements change frequently" → Use prompt engineering
- "We don't have time for examples" → Can't fine-tune without data
- "Training will fix our prompts" → Bad prompts = bad training data
- "We need 100% accuracy" → Models are probabilistic

## Green Lights

Proceed confidently if:

- Consistent capability gap demonstrated
- Clear, measurable success criteria defined
- Stable requirements for 6+ months
- 500+ examples available or creatable
- Team can dedicate focused effort
```

## Testing Your Skill

A skill without testing is untested code. Validate that your skill provides useful guidance.

### Test Case 1: Clear Fine-Tuning Candidate

**Scenario**: E-commerce company wants consistent product description formatting

**Use your skill**:
1. Apply the five criteria
2. Select training method
3. Estimate data requirements
4. Run ROI analysis

**Expected result**: Skill should recommend SFT with QLoRA, estimate 1,000-2,000 examples, provide positive ROI assessment

### Test Case 2: Fine-Tuning Is Wrong

**Scenario**: Startup wants model to "know everything about our product"

**Use your skill**:
1. Apply the five criteria
2. Check for red flags

**Expected result**: Skill should identify "know everything" as a red flag, recommend RAG instead

### Test Case 3: Edge Case

**Scenario**: Medical company needs consistent diagnosis formatting with regulatory constraints

**Use your skill**:
1. Evaluate criteria
2. Note special considerations (safety-critical domain)
3. Provide recommendation

**Expected result**: Skill should recommend SFT + DPO for safety alignment, emphasize evaluation rigor

## Improving Your Skill

After initial creation, iterate based on usage:

### Identify Gaps

When using the skill, note:
- Questions it doesn't answer
- Situations where guidance is unclear
- Missing decision criteria

### Add Specificity

Generic guidance ("consider your requirements") is useless. Replace with specific criteria ("if query volume exceeds 100K/month, calculate break-even").

### Include Examples

Abstract frameworks become concrete with examples. Add real scenarios that illustrate each decision path.

## Try With AI

Complete your skill through these exercises.

**Part 1: Create the Skill File**

```text
Based on the skill structure in this lesson, help me create my complete llmops-decision-framework SKILL.md file.

I want to include:
1. Clear activation criteria
2. The five-criterion decision framework from Lesson 3
3. Training method selection from Lesson 4
4. Economic analysis framework from Lesson 5
5. Use case template from Lesson 6
6. Red flags and green lights

Format it properly with YAML frontmatter and markdown sections.
```

**What you're practicing:** Synthesizing chapter knowledge into a structured, reusable artifact. The skill becomes a durable encoding of your learning.

**Part 2: Test Against Your Use Case**

Take the use case specification you created in Lesson 6 and run it through your skill:

```text
Using my llmops-decision-framework skill, evaluate this use case:

[Paste your use case specification from Lesson 6]

Apply:
1. The five criteria checklist
2. Training method selection
3. Economic analysis
4. Red flag check

Give me a go/no-go recommendation with reasoning.
```

**What you're practicing:** Validating that your skill produces actionable guidance. If the output is vague or wrong, you've identified improvement areas.

**Part 3: Refine Based on Gaps**

```text
After testing my skill, I noticed these gaps:
- [Gap 1: What the skill didn't answer]
- [Gap 2: Where guidance was unclear]

Help me add sections to address these gaps. Each section should include:
1. Clear criteria or decision rules
2. Specific guidance (not generic advice)
3. An example that illustrates the concept
```

**What you're practicing:** Iterative skill improvement. First versions are never complete—real usage reveals what's missing.

Save your skill file to `.claude/skills/llmops-decision-framework/SKILL.md`. You've now created reusable intelligence that compounds across all future LLMOps projects.
