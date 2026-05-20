---
name: f-thread
description: |
  Fusion/Comparison Thread for architecture decisions. Use when:
  - User says "compare approaches", "which is better"
  - User asks to "evaluate options", "architecture decision"
  - User needs "technology selection", "trade-off analysis"
  - Multiple valid approaches exist and a structured comparison is needed
context: fork
---

# Fusion Thread: Architecture Decision Comparison

Structured approach to comparing multiple solutions using parallel evaluation, weighted scoring, and ADR output.

## When to Use

- Choosing between technologies (e.g., Zustand vs Jotai vs Redux)
- Evaluating architecture patterns (e.g., monorepo vs polyrepo)
- Comparing implementation approaches for a feature
- Any decision with 2+ viable options and meaningful trade-offs

## When NOT to Use

- One option is clearly superior (just recommend it)
- Trivial decisions (formatting, naming)
- Already decided by team convention

## Workflow

### 1. Define Criteria

Establish evaluation criteria with weights (must sum to 100):

```
| Criterion        | Weight | Description                        |
|------------------|--------|------------------------------------|
| Performance      | 25     | Runtime speed, bundle size         |
| DX               | 20     | Developer experience, API quality  |
| Maintainability  | 20     | Long-term code health              |
| Ecosystem        | 15     | Community, plugins, docs           |
| Migration Cost   | 10     | Effort to adopt                    |
| Type Safety      | 10     | TypeScript integration quality     |
```

**Preset Criteria Sets:**

- **Frontend**: Performance (25), DX (20), Bundle Size (20), Accessibility (15), Ecosystem (10), Type Safety (10)
- **Backend**: Performance (25), Scalability (20), Maintainability (20), Security (15), Ops Complexity (10), Cost (10)
- **Infrastructure**: Reliability (25), Cost (20), Scalability (20), Ops Complexity (15), Vendor Lock-in (10), Migration (10)

### 2. Spawn Parallel Evaluators

Spawn one oracle agent per approach in a SINGLE message:

```
Task(oracle, "Evaluate [Approach A] against criteria: [criteria list with weights]. Score 1-10 per criterion. Include concrete examples, code samples, and evidence.")
Task(oracle, "Evaluate [Approach B] against criteria: [criteria list with weights]. Score 1-10 per criterion. Include concrete examples, code samples, and evidence.")
Task(oracle, "Evaluate [Approach C] against criteria: [criteria list with weights]. Score 1-10 per criterion. Include concrete examples, code samples, and evidence.")
```

Each evaluator must return:
- Score (1-10) per criterion with justification
- Concrete code example
- Key risks and mitigations
- Best-case and worst-case scenarios

### 3. Collect and Score

Build the comparison matrix from evaluator responses.

### 4. Synthesize Recommendation

Produce the final output in ADR format.

## Output Format

### Comparison Matrix

```
## Comparison: [Decision Title]

| Criterion (Weight)      | Option A | Option B | Option C |
|-------------------------|----------|----------|----------|
| Performance (25)        | 8 (200)  | 6 (150)  | 7 (175)  |
| DX (20)                 | 9 (180)  | 7 (140)  | 6 (120)  |
| Maintainability (20)    | 7 (140)  | 8 (160)  | 5 (100)  |
| Ecosystem (15)          | 8 (120)  | 9 (135)  | 4 (60)   |
| Migration Cost (10)     | 6 (60)   | 8 (80)   | 3 (30)   |
| Type Safety (10)        | 9 (90)   | 7 (70)   | 8 (80)   |
| **TOTAL**               | **790**  | **735**  | **565**  |

Score format: raw (weighted) where weighted = raw * weight
```

> This extends the base ADR template from `agents/planner.md` with scoring matrix and detailed risk sections.

### ADR Template

```markdown
# ADR-NNN: [Decision Title]

## Status
Proposed

## Context
[Why this decision is needed. What problem we're solving.]

## Options Considered
1. **Option A** - [one-line summary]
2. **Option B** - [one-line summary]
3. **Option C** - [one-line summary]

## Decision
We will use **Option A** because [primary reasons].

## Scoring Summary
[Comparison matrix from above]

## Consequences

### Positive
- [benefit 1]
- [benefit 2]

### Negative
- [trade-off 1]
- [trade-off 2]

### Risks
- [risk 1] → Mitigation: [approach]

## References
- [relevant links, docs, benchmarks]
```

## Examples

### Example: State Management Selection

```
User: "Which state management should we use for this Next.js app?"

→ Define criteria (Frontend preset)
→ Task(oracle, "Evaluate Zustand against frontend criteria...")
  + Task(oracle, "Evaluate Jotai against frontend criteria...")
  + Task(oracle, "Evaluate Redux Toolkit against frontend criteria...")
→ Build comparison matrix
→ Output ADR recommendation
```

### Example: Monorepo Tooling

```
User: "Compare Turborepo vs Nx for our monorepo"

→ Define criteria (Infrastructure preset)
→ Task(oracle, "Evaluate Turborepo...") + Task(oracle, "Evaluate Nx...")
→ Build comparison matrix
→ Output ADR recommendation
```
