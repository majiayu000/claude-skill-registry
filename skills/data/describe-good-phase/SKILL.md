---
name: describe-good-phase
description: Phase sizing, scope boundaries, and anti-patterns. Load when evaluating whether a phase is well-formed or needs splitting.
user-invocable: false
---

## What Makes a Good Phase

A Phase is:
- Small enough to complete in one tight iteration loop
- Large enough to produce visible, testable progress
- Reviewable against explicit acceptance criteria
- Internally coherent, with one primary intent

A Phase is NOT:
- An open-ended milestone
- A roadmap
- A grab-bag of unrelated tasks
- A substitute for architecture decisions

If a requested Phase is too large, split it into multiple sequential Phases.
