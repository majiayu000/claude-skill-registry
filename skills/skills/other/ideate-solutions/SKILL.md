---
name: ideate-solutions
description: Use after opportunities are defined to generate and evaluate multiple product solution concepts before validating assumptions. Triggers when you need a set of distinct solution options tied to outcomes and opportunities.
---

# Ideate Solutions

Generate multiple product solution concepts grounded in outcomes and opportunities before validating assumptions.

## Position in Workflow

Step 3 of product strategy workflow:
1. `/discover-outcomes` - Define outcomes
2. `/discover-opportunities` - Identify opportunities
3. `/ideate-solutions` - Explore solution concepts (THIS)
4. `/discover-assumptions` - Validate with experiments

## Core Principle

**Diverge before you converge.** Create several distinct solutions, then evaluate them against outcomes and constraints.

## Input

**Default:** Use outcomes and opportunities from the current conversation.

**If argument provided:**
- File path: Read the file for context
- Notion/Doc URL: Summarize relevant outcomes and opportunities

## Workflow

### 1. Gather Context

- Restate the target outcomes and top opportunities.
- List constraints (time, budget, compliance, positioning).
- Clarify what is in scope vs out of scope.

### 2. Ask Clarifying Questions

Ask what improves ideation quality:
- Which outcomes matter most right now?
- What constraints are non-negotiable?
- What segments or use cases are priority?
- What current alternatives must be beaten?

### 3. Ideate Multiple Solutions

Generate 3-5 distinct solution concepts. Vary across:

| Dimension | Examples |
|-----------|----------|
| **Approach** | Self-serve tool, concierge, marketplace, automation |
| **Value prop** | Speed, cost reduction, risk reduction, delight |
| **Delivery model** | Feature, workflow, service, integration |
| **Adoption path** | Low-friction trial, assisted onboarding, pilots |

Avoid anchoring on the first idea. Make the options meaningfully different.

### 4. Evaluate Trade-offs

For each solution, assess:
- **Pros:** How it advances outcomes
- **Cons:** Risks or limitations
- **Evidence fit:** What assumptions it relies on
- **Feasibility:** Rough effort and dependencies
- **Differentiation:** Why it wins vs alternatives

### 5. Pick a Leading Concept

Rank the options and select a leading concept to validate next.

## Output Format

```
## Solution Ideation

### Context Summary
[Target outcomes + top opportunities]

### Clarifying Questions
[Questions about priorities or constraints - if any]

---

### Concepts

#### Concept 1: [Name] - Leading
[Description]

**Pros:**
- ...

**Cons:**
- ...

**Evidence fit:** [Key assumptions this relies on]
**Feasibility:** [Low/Medium/High]
**Differentiation:** [Why this wins vs alternatives]

#### Concept 2: [Name]
[Same structure]

#### Concept 3: [Name]
[Same structure]

---

### Recommendation
[Why the leading concept wins, and when you'd choose differently]

### Open Questions
[Assumptions or unknowns to validate]

### Next Step
Validate assumptions. Run `/discover-assumptions`.
```

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Jumping to one idea | Generate 3-5 concepts first |
| Concepts too similar | Force meaningful variation |
| Ignoring constraints | State non-negotiables early |
| No link to outcomes | Tie each concept to outcomes |

## What NOT to Do

- Do NOT define experiments yet
- Do NOT commit to a solution without assumptions
- Do NOT skip trade-off analysis
