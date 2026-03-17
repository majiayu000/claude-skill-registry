---
name: write-product-brief
description: Produce a concise product brief artifact that is decision-ready, scoped, and measurable.
---

# Write Product Brief

Create a product brief that drives execution decisions, not narrative fluff.

## When to Use

Use this skill when a task deliverable is a product brief (new initiative, experiment brief, launch brief, or scope decision brief).

## Operating Mode

**BRIEF AUTHORING ONLY**

**Allowed:** synthesize evidence, define scope, write measurable outcomes, record risks.

**Not allowed:** implementation execution, speculative claims without evidence, unresolved ambiguous scope.

## Inputs

- Problem/opportunity statement
- Audience/user segment
- Business objective and metric target
- Constraints (time, budget, channel, legal, platform)
- Known dependencies and risks

## Output

Create/update:

`docs/briefs/<slug>-product-brief.md`

Required sections:

```markdown
# <Title> Product Brief

## Objective
## Target User / Segment
## Problem Statement
## Proposed Solution
## Scope
### In Scope
### Out of Scope
## Success Metrics
## Risks & Mitigations
## Dependencies
## Decision Needed
```

## Workflow

1. Convert raw request into explicit objective and decision question.
2. Define user, problem, and scope boundaries.
3. Translate desired outcome into measurable metrics.
4. Document risks/dependencies with owners or assumptions.
5. Final pass: remove ambiguity and tighten actionability.

## Quality Gate

- [ ] Objective and metric are explicit.
- [ ] Scope boundaries are unambiguous.
- [ ] Risks and dependencies are actionable.
- [ ] Brief can directly feed `/plan-feature`.

## Completion Message

> "Product brief ready: `docs/briefs/<slug>-product-brief.md`. Scope, metrics, risks, and decision point are explicit."
