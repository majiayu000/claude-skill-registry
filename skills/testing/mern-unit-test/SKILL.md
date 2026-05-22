---
name: mern-unit-test
description: Run MERN unit tests, report results, and optionally fix failures.
argument-hint: "[--scope apps/web|packages/shared|all] [--no-fix]"
allowed-tools: Bash, Read, Glob, Grep, Write
---

## Purpose

Run unit tests, report failures with enough detail to debug, then (with approval) fix issues and re-run to confirm.

## Arguments

- `--scope <target>` — Limit to `apps/web`, `packages/shared`, or `all` (default: all)
- `--no-fix` — Report only, don't offer to fix

## Workflow

### 1. Run tests

```bash
# All tests
pnpm test

# With coverage (if configured)
pnpm test -- --coverage

# Scoped
pnpm -C apps/web test
pnpm -C packages/shared test
```

### 2. Report results

Include:

- Pass/fail/skip counts
- Coverage summary (if available)
- Each failing test: file, test name, assertion diff or error
- If coverage not configured, note this and offer to set it up

### 3–4. Approval gate, fix and confirm

See `/shared-review-workflow` for approval gate protocol, fix constraints, and severity definitions.

## Reference

For coverage setup and common fix patterns, see `reference/mern-unit-test-reference.md`
