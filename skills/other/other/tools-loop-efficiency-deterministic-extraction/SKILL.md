---
name: tools-loop-efficiency-deterministic-extraction
description: Scout new skill-efficiency opportunities, register them in docs/plans/startup-loop-token-efficiency-v2/deterministic-extraction-analysis.md, recompute true ROI/payback, and auto-implement every item in Implement now and Backlog via an execution queue.
---

# /tools-loop-efficiency-deterministic-extraction

End-to-end opportunity automation for the startup-loop efficiency analysis.

## Invocation

```bash
/tools-loop-efficiency-deterministic-extraction
/tools-loop-efficiency-deterministic-extraction --analysis <path>
/tools-loop-efficiency-deterministic-extraction --audit <path>
/tools-loop-efficiency-deterministic-extraction --model-cost <usd-per-mtok> --engineer-rate <usd-per-hour>
/tools-loop-efficiency-deterministic-extraction --evidence-quality <proxy|observed|measured>
/tools-loop-efficiency-deterministic-extraction --realization-prob <0-1>
/tools-loop-efficiency-deterministic-extraction --dry-run
```

Default analysis path:
`docs/plans/startup-loop-token-efficiency-v2/deterministic-extraction-analysis.md`

## Operating Mode

**SCOUT + SCORE + BUILD**

- Scout fresh opportunities from latest `skill-efficiency-audit-*.md`
- Register new opportunities directly in analysis markdown
- Recompute payback ROI, Expected ROI, and decision categories using the payback formula
- Build and execute queue for `Implement now` and `Backlog` items (in that order)

## Workflow

1. Read [modules/scout-and-register.md](modules/scout-and-register.md) and run it first.
2. Read [modules/auto-implement.md](modules/auto-implement.md) and execute queue items.
3. Keep iterating queue rows until all `Implement now` and `Backlog` rows are either `Done` or `Blocked` with explicit reasons.

## Required Scripts

- `scripts/refresh-analysis-and-scout.mjs`
- `scripts/build-execution-queue.mjs`

Run both scripts from repo root.

## Safety + Quality Gates

- Never skip validation for implementation changes.
- Keep queue status updated after each row.
- For rows marked `Blocked`, continue with the next row.
- Never run destructive git commands.

## Completion Condition

Complete only when all queue rows in categories `Implement now` and `Backlog` are no longer `Pending`.

## References

- [references/payback-model.md](references/payback-model.md)
