---
name: thinking-model-selection
description: Choose the right mental model for the problem at hand. Use when facing new problems, when current approaches fail, or when you need to match tool to context.
---

# Model Selection

## Overview

Every mental model has a domain where it excels and domains where it fails. Model selection is the meta-skill of recognizing which model fits which problem. The expert doesn't just know many models—they know when to apply each one. Using the wrong model is often worse than using no model at all.

**Core Principle:** The map is not the territory. Choose the map that best serves your journey.

## When to Use

- Facing a new problem type
- Current approach isn't working
- Multiple stakeholders suggest different frameworks
- Deciding how to structure analysis
- Teaching others which tools to use
- Building decision-making processes

Decision flow:

```
Facing a problem?
  → Have you identified the problem type? → no → CLASSIFY THE PROBLEM FIRST
  → Does your usual model fit? → no → CONSIDER ALTERNATIVES
  → Are you using a model by habit? → yes → QUESTION THE FIT
```

## Problem-Model Matching

### Step 1: Classify the Problem

```markdown
## Problem Classification

Problem: [Describe the problem]

Problem dimensions:
| Dimension | Assessment |
|-----------|------------|
| Predictability | Can outcomes be predicted? [High/Medium/Low] |
| Complexity | How many interacting parts? [Simple/Complicated/Complex] |
| Time horizon | When do consequences matter? [Immediate/Short/Long] |
| Reversibility | Can decisions be undone? [Easily/With difficulty/Not at all] |
| Information | How much do you know? [Complete/Partial/Minimal] |
| Stakeholders | Who's affected? [Individual/Team/Organization/Society] |
```

### Step 2: Match to Model Categories

```markdown
## Model Category Matching

Based on classification, which category fits?

| Problem Type | Model Category | Examples |
|--------------|----------------|----------|
| Root cause unknown | Diagnostic models | 5 Whys, Scientific Method, Kepner-Tregoe |
| Decision under uncertainty | Probabilistic models | Bayesian, Expected Value, Regret Minimization |
| System behavior | Systems models | Feedback Loops, Leverage Points, Archetypes |
| Cognitive bias risk | Debiasing models | Pre-mortem, Red Team, Steel-manning |
| Resource allocation | Constraint models | Theory of Constraints, Opportunity Cost |
| Innovation/exploration | Generative models | First Principles, TRIZ, Effectuation |
| Domain classification | Meta models | Cynefin, Circle of Competence |
```

### Step 3: Select Specific Model

```markdown
## Model Selection

Category: [From Step 2]

Candidate models:
| Model | Fit Score | Strengths for This Problem | Weaknesses |
|-------|-----------|---------------------------|------------|
| [Model 1] | [1-5] | [Why it fits] | [Limitations] |
| [Model 2] | [1-5] | [Why it fits] | [Limitations] |
| [Model 3] | [1-5] | [Why it fits] | [Limitations] |

Selected model: [Choice]
Rationale: [Why this model for this problem]
```

## Model Selection Matrix

### By Problem Type

```
DIAGNOSTIC PROBLEMS (What's causing this?)
├── Known categories exist → Kepner-Tregoe (systematic analysis)
├── Need quick root cause → 5 Whys Plus (iterative drilling)
├── Hypothesis-driven → Scientific Method (test and falsify)
└── System-wide issue → Feedback Loops (find reinforcing patterns)

DECISION PROBLEMS (What should we do?)
├── High stakes, irreversible → Regret Minimization, Pre-mortem
├── Under uncertainty → Bayesian, Probabilistic Thinking
├── Resource constrained → Opportunity Cost, Theory of Constraints
├── Multiple options → Kepner-Tregoe (decision analysis)
└── Type 1 vs Type 2 → Reversibility Framework

UNDERSTANDING PROBLEMS (How does this work?)
├── Complex system → Systems Thinking, Feedback Loops
├── Human behavior → Jobs to be Done, Incentive Analysis
├── Organizational → Archetypes, Leverage Points
└── Competitive → Red Team, Game Theory

CREATIVE PROBLEMS (How might we...?)
├── Break assumptions → First Principles, TRIZ
├── Limited resources → Effectuation, Via Negativa
├── Technical contradiction → TRIZ
└── Unknown territory → Thought Experiments, Cynefin (probe)

EVALUATION PROBLEMS (Is this good?)
├── Arguments/proposals → Steel-manning, Red Team
├── Predictions → Probabilistic, Calibration
├── Longevity → Lindy Effect
├── Safety → Margin of Safety, Pre-mortem
└── Expertise fit → Circle of Competence
```

### By Domain

```markdown
## Domain-Model Mapping

| Domain | Primary Models | Why |
|--------|---------------|-----|
| Debugging | Scientific Method, 5 Whys | Hypothesis testing, root cause |
| Architecture | Systems Thinking, Leverage Points | Interconnections, intervention |
| Product | Jobs to be Done, Cynefin | User needs, complexity |
| Strategy | Red Team, Pre-mortem | Adversarial, risk |
| Performance | Theory of Constraints, Fermi | Bottlenecks, estimation |
| Decisions | Reversibility, Regret Minimization | Stakes assessment |
| Innovation | First Principles, TRIZ | Breakthrough thinking |
| Risk | Margin of Safety, Probabilistic | Uncertainty handling |
```

## Model Failure Modes

### Using the Wrong Model

```markdown
## Model Mismatch Indicators

Signs you're using the wrong model:
- Analysis feels forced or awkward
- Key aspects don't fit the framework
- You're ignoring important factors
- Results don't match intuition consistently
- Stakeholders don't recognize the framing

Common mismatches:
| Situation | Wrong Model | Right Model |
|-----------|-------------|-------------|
| Complex adaptive system | Root cause analysis | Systems thinking |
| Simple process problem | Systems thinking | Checklist/SOP |
| Uncertain future | Detailed planning | Effectuation |
| Known domain | First principles | Best practices |
| Political problem | Technical analysis | Stakeholder mapping |
```

### Model Overuse

```markdown
## Model Overuse Patterns

"When you have a hammer, everything looks like a nail"

Signs of overuse:
- You use the same model for every problem
- You haven't learned new models recently
- Problems that don't fit are "forced" into the model
- You dismiss problems that don't fit your model

Fix: Deliberately practice with unfamiliar models
     Ask: "What model would someone else use?"
     Rotate models intentionally
```

## Model Selection Process

### Quick Selection (< 2 minutes)

```markdown
## Quick Model Selection

1. What type of problem? [Diagnostic/Decision/Understanding/Creative/Evaluation]
2. What's the constraint? [Time/Information/Stakes/Complexity]
3. What's the default model for this type?
4. Any reason NOT to use the default?
5. Proceed or reconsider

Default models by type:
- Diagnostic → 5 Whys Plus
- Decision → Reversibility check first
- Understanding → Systems Thinking
- Creative → First Principles
- Evaluation → Steel-manning
```

### Deliberate Selection (> 5 minutes)

```markdown
## Deliberate Model Selection

1. Characterize the problem fully
2. Identify 3-5 candidate models
3. Score each on fit
4. Consider combining models
5. Select and document rationale
6. Plan to reassess if model doesn't illuminate

Selection criteria:
| Criterion | Weight | Model A | Model B | Model C |
|-----------|--------|---------|---------|---------|
| Problem fit | 30% | | | |
| Available info | 20% | | | |
| Time to apply | 15% | | | |
| Stakeholder acceptance | 15% | | | |
| My competence with model | 20% | | | |
```

## Model Selection Template

```markdown
# Model Selection: [Problem]

## Problem Characterization
Type: [Diagnostic/Decision/Understanding/Creative/Evaluation]
Complexity: [Simple/Complicated/Complex/Chaotic]
Stakes: [Low/Medium/High]
Reversibility: [High/Medium/Low]
Information: [Complete/Partial/Minimal]

## Candidate Models
| Model | Fit | Strengths | Weaknesses |
|-------|-----|-----------|------------|
| | | | |

## Selected Model
Model: [Choice]
Rationale: [Why this model]

## Fallback
If selected model doesn't work: [Alternative]
Signs to switch: [Indicators]

## Application Plan
How I'll use this model:
1. [Step]
2. [Step]
```

## Meta-Model Guidelines

### When to Use Multiple Models

```markdown
## Model Combination Triggers

Use multiple models when:
- Problem spans multiple types
- Single model leaves blind spots
- Stakes are very high
- Time allows deeper analysis

Combination patterns:
- Sequential: Use A to narrow, then B to decide
- Parallel: Use A and B independently, compare results
- Nested: Use A at macro level, B at micro level
```

### When to Abandon a Model

```markdown
## Model Exit Criteria

Stop using a model when:
- 15+ minutes with no insight
- Key facts don't fit the framework
- You're forcing the analysis
- Someone suggests a better fit

Don't stop just because:
- The answer is uncomfortable
- It requires more work
- Results disagree with intuition (investigate why)
```

## Verification Checklist

- [ ] Classified the problem type
- [ ] Considered multiple candidate models
- [ ] Checked for model-problem fit
- [ ] Avoided using model out of habit
- [ ] Have a fallback if model doesn't work
- [ ] Can articulate why this model fits

## Key Questions

- "What type of problem is this really?"
- "What model would an expert in this domain use?"
- "Am I using this model because it fits, or because I know it?"
- "What aspects of the problem does this model ignore?"
- "What model would give a different answer?"
- "When should I switch to a different model?"

## Munger's Wisdom

"You've got to have models in your head. And you've got to array your experience—both vicarious and direct—on this latticework of models."

"You must know the big ideas in the big disciplines, and use them routinely—all of them, not just a few."

The power isn't in any single model—it's in having many models and knowing when each applies. A tool is only useful when matched to the task. The meta-skill of model selection multiplies the value of every model you know.
