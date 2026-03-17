---
name: nean-unit-test
description: Run NEAN unit tests, report results, and optionally fix failures.
argument-hint: "[--scope api|web|libs|all] [--no-fix]"
allowed-tools: Bash, Read, Glob, Grep, Write
---

## Purpose

Run unit tests, report failures with enough detail to debug, then (with approval) fix issues and re-run to confirm.

## Arguments

- `--scope <target>` — Limit to `api`, `web`, `libs`, or `all` (default: all)
- `--no-fix` — Report only, don't offer to fix

## Workflow

### 1. Run tests

```bash
# All tests
npm run test

# With coverage
npm run test -- --coverage

# Scoped (using Nx)
npx nx test api
npx nx test web
npx nx run-many --target=test --projects=shared-*

# Affected only (CI optimization)
npx nx affected --target=test
```

### 2. Report results

Include:

- Pass/fail/skip counts
- Coverage summary (if available)
- Each failing test: file, test name, assertion diff or error
- If coverage not configured, note this and offer to set it up

### 3–4. Approval gate, fix and confirm

See `/shared-review-workflow` for approval gate protocol, fix constraints, and severity definitions.

## Test file conventions

```
# NestJS
apps/api/src/modules/<feature>/__tests__/<feature>.service.spec.ts
apps/api/src/modules/<feature>/__tests__/<feature>.controller.spec.ts

# Angular
apps/web/src/app/<feature>/<feature>.component.spec.ts

# Libraries
libs/<scope>/<name>/src/**/*.spec.ts
```

## Coverage thresholds

Default targets (configure in jest.config.ts):
- Libs: 80% statements, 80% branches
- Apps: 60% statements, 50% branches

## Reference

For coverage setup and common fix patterns, see `reference/nean-unit-test-reference.md`
