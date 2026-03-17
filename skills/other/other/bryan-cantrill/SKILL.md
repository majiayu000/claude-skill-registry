---
name: bryan-cantrill
description: >-
  Evidence-first engineering. Written design before implementation, risk-ordered
  execution, observability as a requirement, scope discipline through explicit
  non-goals. Use when: (1) starting non-trivial implementation work, (2) planning
  task order, (3) reviewing whether a feature is complete, (4) enforcing merge
  and review discipline.
category: principles
---

# Bryan Cantrill

Write it down. Reduce uncertainty first. Instrument reality. Do not merge unreviewed thinking.

## Core Principles

1. No non-trivial implementation without a written design artifact.
2. Reduce risk first, not what is easiest first.
3. Every feature must define its observability contract.
4. Every plan must declare explicit non-goals.
5. No solo merge of architectural shifts.
6. Measure reality. Opinion is not evidence.

## 1. Planning Discipline

No non-trivial implementation begins without a written design artifact. Rough is acceptable. Missing thinking is not.

Written design must include:

| Field | Purpose |
|-------|---------|
| Problem statement | What is broken or missing |
| Determination | What we are doing about it |
| Alternatives considered | What we rejected and why |
| Non-goals | What we deliberately will not solve |
| Operational implications | What changes in production |

The point is not polish. The point is intellectual rigor.

### Planning Template

```
State: [ideation | discussion | published | committed]
Goal:
Non-goals:
Alternatives considered:
Primary risk:
What invalidates this approach:
Observability plan:
Minimal end-to-end slice:
What we explicitly defer:
```

If this cannot be filled concisely, the work is not understood.

## 2. Risk-Ordered Execution

Task ordering is not "what is easiest first." It is "what reduces uncertainty first."

Execution order:

1. Lock interfaces
2. Add observability scaffolding
3. Attack highest-risk unknown
4. Deliver minimal end-to-end slice
5. Harden
6. Expand features

If you are building features before understanding behavior, you are accumulating debt.

### Ordering Questions

Before sequencing work, answer:

- What reduces uncertainty first?
- What invalidates the plan fastest?
- What assumptions are most dangerous?

## 3. Observability Contract

Systems must be debuggable in production. Every feature must define:

1. What signal proves it works?
2. What signal proves it fails?
3. What signal distinguishes failure modes?

If you cannot answer those three questions, the feature is incomplete. Observability is not a later sprint.

## 4. Scope Discipline

Every plan must explicitly state:

- Non-goals
- What we are deliberately not solving
- What will not be refactored
- What adjacent systems are out-of-bounds

When new work appears during implementation:

- Either create a new design artifact
- Or remove something of equal weight

No silent expansion.

## 5. Merge Discipline

Designs must be reviewed before implementation begins. Significant changes must be reviewed before merge. No solo merge of architectural shifts.

If nobody reads your design, you must explicitly ask. Unreviewed thinking becomes institutional debt.

## 6. State Awareness

Every plan must declare its maturity:

| State | Meaning |
|-------|---------|
| ideation | Rough exploration, not a commitment |
| discussion | Under review, open to change |
| published | Agreed direction |
| committed | Implemented |

Never pretend ideation is commitment. This prevents accidental convergence on half-formed ideas.

## Agent Operating Mode

### Before Coding

- Where is the written determination?
- What are the non-goals?
- What invalidates this plan?

### During Implementation

- Observability hooks exist?
- Interfaces are explicit?
- Risk is being reduced, not hidden?

### Before Merge

- Review occurred?
- Scope did not silently expand?
- Rollback strategy exists?

If these checks fail, block progress.

## Rationalizations (All Rejected)

| Excuse | Why It's Wrong | Required Action |
|--------|----------------|-----------------|
| "We'll instrument later" | Later never comes | Define observability now |
| "The design is in my head" | Unwritten design is unreviewed design | Write it down |
| "This is too small to plan" | Small changes compound into architectural drift | Fill the template |
| "We'll refactor adjacent code while we're here" | Silent scope expansion | Create a separate artifact |
| "Nobody needs to review this" | Unreviewed thinking becomes institutional debt | Ask for review explicitly |
| "I know this assumption is safe" | Unmeasured assumptions are the most dangerous | Instrument it |

## Chaining

- **rick-rubin**: Complementary scope discipline. Bryan-cantrill focuses on written design and observability. Rick-rubin focuses on diff-level scope defense.
- **fresh-eyes**: Use fresh-eyes Planning mode to audit the written design artifact before implementation.
- **tdd**: Risk-ordered execution pairs naturally with TDD. Attack the highest-risk unknown with a failing test first.
