---
name: code
description: Use when implementing an approved task or plan in the current session and you are ready to make code changes.
---

task = $ARGUMENTS

Implement the plan. CLAUDE.md standards and quality gates apply throughout.

## Incremental Execution

Commit after each meaningful step — a failing change on top of 5 uncommitted steps is much harder to debug than one on top of a clean commit.

## Completion Check

Before declaring done, verify:
- No TODOs, FIXMEs, stubs, or incomplete implementations remain
- No silent fallbacks — default/fallback values inserted to make type errors disappear instead of fixing the actual type or data issue. Models reflexively add these; catch yourself.

## Error Recovery

When something breaks, try a different approach — not the same fix again. On second failure, revert to last working state and try a fundamentally different strategy. On third failure, **stop and tell the user** — report what you tried, what failed, and what context you're missing.

Repeated failure usually means missing context or a wrong assumption, not insufficient effort.

**Hard stops** (don't retry, just ask):
- Same file fails to compile/typecheck/lint 3 times
- Same test fails 3 times after different fixes
- You notice yourself repeating the same action

## Deviations from Plan

- **Minor** (naming, internal structure): document the reason and continue
- **Major** (different approach, new dependencies, scope change): stop and present options with trade-offs — the plan was approved, departing significantly needs explicit buy-in

## Quality Gates

After completing implementation, run quality gates (format, lint, typecheck, tests, build). Report PASS or FAIL with specific errors.
