---
name = "execute"
description = "Implement a scoped task quickly and safely, then validate and summarize changes."
---

## Purpose

Use this skill when the task is implementation-ready and requires code changes now.

## Trigger

- User asks to implement, refactor, or fix code directly
- A plan already exists and a specific phase is selected

## Workflow

1. Confirm exact scope and acceptance criteria.
2. Load only relevant files and preserve existing conventions.
3. Implement the smallest viable diff.
4. Run the most relevant checks/tests.
5. Summarize changed files, validation, and remaining work.

## Output Template

```markdown
## Scope
- ...

## Files Changed
- ...

## Validation
- ...

## Follow-ups
- ...
```

## Notes

- Escalate to `omg-reviewer` for high-risk or cross-cutting changes.
- Use `omg-debugger` immediately when checks fail.
