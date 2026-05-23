---
name = "ralplan"
description = "Create a strict, quality-first execution plan with explicit gates and rollback-ready sequencing."
---

## Purpose

Use this skill when planning must prioritize correctness and risk control over speed.

## Trigger

- High-risk refactors or migrations
- Security or reliability-sensitive changes
- User asks for strict planning before coding

## Workflow

1. Define objective, constraints, and non-goals.
2. Build a stage-gated plan (`plan -> prd -> exec -> verify -> fix`).
3. Define hard pass/fail criteria per stage.
4. Include rollback points and stop conditions.
5. Add validation gates before release readiness.

## Output Template

```markdown
## Goal
- ...

## Stage Gates
| Stage | Entry Criteria | Exit Criteria | Owner |
| --- | --- | --- | --- |

## Risk Controls
- ...

## Rollback Plan
- ...
```
