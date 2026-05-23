---
name = "plan"
description = "Create a phased implementation plan with risks, dependencies, and validation checkpoints."
---

## Purpose

Use this skill when the request is non-trivial and should be planned before editing code.

## Trigger

- User asks for strategy, roadmap, or migration plan
- Scope touches multiple files or subsystems
- Work needs sequencing or parallelization decisions

## Workflow

1. Restate goals, constraints, and acceptance criteria.
2. Inspect only the repository areas required for planning.
3. Break work into phases and atomic tasks.
4. Mark dependencies and parallelizable tasks.
5. Add validation checkpoints and rollback notes.

## Output Template

```markdown
## Goal
- ...

## Phase Plan
1. Phase 1 - ...
2. Phase 2 - ...

## Task Breakdown
1. ...
2. ...

## Risks
- ...

## Validation
- ...
```

## Notes

- Delegate architecture tradeoffs to `omg-architect` when needed.
- Keep plans executable and testable, not abstract.
