---
name: thinking-model-combination
description: Combine multiple mental models for richer analysis. Use for complex problems requiring multiple lenses, high-stakes decisions, or when single models leave blind spots.
---

# Model Combination

## Overview

Real-world problems rarely fit neatly into a single mental model. Model combination uses multiple frameworks together—sequentially, in parallel, or nested—to achieve deeper understanding than any single model provides. The skill is knowing how to combine models productively without creating confusion or analysis paralysis.

**Core Principle:** Multiple lenses reveal what single lenses miss. But combination requires discipline, not just accumulation.

## When to Use

- Complex problems spanning multiple domains
- High-stakes decisions where blind spots are costly
- When single models leave important questions unanswered
- Validating conclusions through different frameworks
- Teaching comprehensive analysis
- Building robust decision processes

Decision flow:

```
Analyzing a problem?
  → Does one model fully address it? → yes → Use single model
  → Are there important blind spots? → yes → ADD COMPLEMENTARY MODEL
  → Are stakes high enough to justify deeper analysis? → yes → USE MULTIPLE MODELS
```

## Combination Patterns

### Pattern 1: Sequential (Pipeline)

Use one model's output as another's input:

```markdown
## Sequential Combination

Model A → Model B → Model C

Example: Product Decision
1. Jobs to be Done → Identify the real user need
2. First Principles → Design solution from fundamentals
3. Pre-mortem → Identify what could go wrong
4. Reversibility → Assess if we can course-correct

Flow:
[JTBD identifies need] → [First Principles designs solution] →
[Pre-mortem finds risks] → [Reversibility determines commitment level]

Each model builds on previous insights.
```

### Pattern 2: Parallel (Multiple Lenses)

Apply models independently, compare results:

```markdown
## Parallel Combination

     ┌→ Model A → Result A ─┐
Problem → Model B → Result B → Synthesis
     └→ Model C → Result C ─┘

Example: Strategic Decision
Apply independently:
- Red Team: "How could this fail?"
- Opportunity Cost: "What are we giving up?"
- Second-Order Thinking: "What happens next?"

Synthesis:
| Model | Conclusion | Unique Insight |
|-------|------------|----------------|
| Red Team | [Finding] | [What only this revealed] |
| Opportunity Cost | [Finding] | [What only this revealed] |
| Second-Order | [Finding] | [What only this revealed] |

Combined conclusion: [Synthesis of all three]
```

### Pattern 3: Nested (Zoom Levels)

Use different models at different scales:

```markdown
## Nested Combination

Macro level: Model A
  └→ Meso level: Model B
       └→ Micro level: Model C

Example: System Optimization
- Macro (System): Theory of Constraints → Find the bottleneck
- Meso (Process): Scientific Method → Diagnose bottleneck cause
- Micro (Action): OODA Loop → Rapid iteration on fixes

The macro model identifies WHERE to focus.
The meso model identifies WHAT is happening.
The micro model guides HOW to respond.
```

### Pattern 4: Adversarial (Thesis-Antithesis)

Use models that challenge each other:

```markdown
## Adversarial Combination

Model A argues FOR → ← Model B argues AGAINST

Example: Investment Decision
- Optimistic lens (First Principles): "Here's why this could work"
- Pessimistic lens (Pre-mortem): "Here's why this will fail"
- Neutral lens (Bayesian): "Here's the actual probability"

Structure:
| Aspect | First Principles | Pre-mortem | Bayesian Estimate |
|--------|------------------|------------|-------------------|
| Market | [Optimistic case] | [Failure mode] | [P(success)] |
| Technology | [Optimistic case] | [Failure mode] | [P(success)] |
| Team | [Optimistic case] | [Failure mode] | [P(success)] |

Resolution: Adjust probabilities based on adversarial insights
```

### Pattern 5: Temporal (Time-Based)

Different models for different time horizons:

```markdown
## Temporal Combination

Past: Model A (understand history)
Present: Model B (assess current state)
Future: Model C (project outcomes)

Example: Career Decision
- Past (5 Whys): "Why am I in this situation?"
- Present (Circle of Competence): "What are my current advantages?"
- Future (Regret Minimization): "What will 80-year-old me think?"

Timeline:
Past analysis → Present assessment → Future projection → Decision
```

## Combination Recipes

### Recipe 1: High-Stakes Decision

```markdown
## High-Stakes Decision Recipe

Combine: Reversibility + Pre-mortem + Opportunity Cost + Second-Order

Step 1 - Reversibility Check:
Is this Type 1 or Type 2?
[Assessment]

Step 2 - Pre-mortem:
Assume failure, explain why
[Failure modes]

Step 3 - Opportunity Cost:
What's the best alternative?
[Alternatives foregone]

Step 4 - Second-Order:
What happens after the immediate effect?
[Cascading consequences]

Synthesis:
Given [reversibility], with risks of [pre-mortem findings],
giving up [opportunity cost], leading to [second-order effects],
the decision is: [Conclusion]
```

### Recipe 2: System Diagnosis

```markdown
## System Diagnosis Recipe

Combine: Cynefin + Theory of Constraints + Feedback Loops + Leverage Points

Step 1 - Cynefin:
What domain is this? [Clear/Complicated/Complex/Chaotic]
Appropriate approach: [Sense-Categorize-Respond / Sense-Analyze-Respond / etc.]

Step 2 - Theory of Constraints:
Where's the bottleneck?
[Constraint identification]

Step 3 - Feedback Loops:
What reinforcing/balancing loops exist?
[Loop mapping]

Step 4 - Leverage Points:
Where can small changes have big effects?
[Intervention points]

Synthesis:
This is a [domain] problem. The constraint is [X].
The key feedback loop is [Y]. The highest leverage point is [Z].
```

### Recipe 3: Innovation Challenge

```markdown
## Innovation Recipe

Combine: First Principles + TRIZ + Effectuation + Via Negativa

Step 1 - First Principles:
What are the fundamental truths?
[Core elements]

Step 2 - TRIZ:
What contradictions exist? What inventive principles apply?
[Contradiction resolution]

Step 3 - Effectuation:
What means do we have? What's affordable loss?
[Means inventory and constraints]

Step 4 - Via Negativa:
What should we remove or avoid?
[Subtractions]

Synthesis:
Starting from [first principles], resolving [contradiction] via [TRIZ principle],
using [available means], and removing [via negativa items],
the innovation path is: [Approach]
```

### Recipe 4: Argument Evaluation

```markdown
## Argument Evaluation Recipe

Combine: Steel-manning + Bayesian + Debiasing

Step 1 - Steel-manning:
What's the strongest version of this argument?
[Strengthened argument]

Step 2 - Bayesian:
What's my prior? What evidence would update it?
Prior: [X%]
Evidence that would increase: [List]
Evidence that would decrease: [List]

Step 3 - Debiasing:
What biases might affect my evaluation?
[Bias checklist]

Synthesis:
The steel-manned argument is [X]. Given [evidence] and controlling for [biases],
my updated probability is [Y%]. Conclusion: [Assessment]
```

## Combination Anti-Patterns

### Too Many Models

```markdown
## Anti-Pattern: Model Soup

Problem: Using 5+ models without clear purpose
Result: Confusion, analysis paralysis, contradictory conclusions

Symptoms:
- Can't synthesize findings
- Each model says something different
- Analysis takes forever
- No clear recommendation emerges

Fix: Maximum 3-4 models with clear roles
     Define how models relate BEFORE applying
     Designate a "tiebreaker" model for conflicts
```

### Incompatible Models

```markdown
## Anti-Pattern: Forced Marriage

Problem: Combining models with conflicting assumptions
Example: Effectuation (embrace uncertainty) + Detailed planning (predict future)

Symptoms:
- Models contradict each other fundamentally
- Can't reconcile conclusions
- Feels like arguing with yourself

Fix: Use models in sequence for different phases
     Or use as adversarial pair intentionally
     Don't try to blend incompatible worldviews
```

### Model Without Purpose

```markdown
## Anti-Pattern: Checkbox Combination

Problem: Adding models to seem thorough, not for insight
Result: Wasted effort, no additional value

Symptoms:
- Model confirms what you already knew
- No new insights from additional model
- Adding models "just in case"

Fix: Add model only if it addresses a specific blind spot
     Ask: "What question does this model answer that others don't?"
```

## Model Combination Template

```markdown
# Model Combination Analysis: [Problem]

## Problem Characterization
[Describe the problem and why combination is needed]

## Combination Pattern
Pattern: [Sequential/Parallel/Nested/Adversarial/Temporal]
Rationale: [Why this pattern]

## Models Selected
| Model | Role | What It Addresses |
|-------|------|-------------------|
| | | |

## Analysis

### Model 1: [Name]
[Analysis using this model]
Key insight: [What this uniquely revealed]

### Model 2: [Name]
[Analysis using this model]
Key insight: [What this uniquely revealed]

### Model 3: [Name]
[Analysis using this model]
Key insight: [What this uniquely revealed]

## Synthesis

### Convergence
Where models agree: [Common conclusions]

### Divergence
Where models differ: [Conflicting conclusions]
Resolution: [How to resolve conflicts]

### Unique Contributions
| Model | Unique Insight |
|-------|----------------|
| | |

## Combined Conclusion
[Synthesis that incorporates all models]

## Confidence Assessment
Confidence in conclusion: [High/Medium/Low]
What would change my mind: [Key uncertainties]
```

## Verification Checklist

- [ ] Each model has a clear, distinct role
- [ ] Combination pattern is explicit
- [ ] Models are compatible or deliberately adversarial
- [ ] Synthesis addresses convergence and divergence
- [ ] Not using more models than necessary
- [ ] Clear combined conclusion emerges

## Key Questions

- "What does each model contribute that others don't?"
- "How do these models relate to each other?"
- "Where do the models agree? Disagree?"
- "Am I adding models for insight or just thoroughness?"
- "What's the simplest combination that addresses the problem?"
- "How do I synthesize if models conflict?"

## Munger's Wisdom (Extended)

"I've long believed that a certain system—which almost any intelligent person can learn—works way better than the systems most people use. What you need is a latticework of mental models in your head."

"You may have noticed students who just try to remember and pound back what is remembered. Well, they fail in school and in life. You've got to hang experience on a latticework of models in your head."

The latticework isn't just having models—it's the connections between them. Combination is how you weave the lattice. Individual models are threads; combination creates the fabric that catches reality's complexity.
