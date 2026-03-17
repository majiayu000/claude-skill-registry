---
name: mern-code-review
description: Review MERN code for compliance with standards, NFRs, and security policy.
argument-hint: "[--paths <glob>] [--no-fix]"
allowed-tools: Bash, Read, Glob, Grep, Write
---

## Purpose

Review code against mern-std, mern-nfr, and mern-sec policies. Report issues, then (with approval) fix and run tests to confirm.

## Arguments

- `--paths <glob>` — Limit review scope (default: whole repo)
- `--no-fix` — Report only, don't offer to fix

## Workflow

### 1. Automated gates

```bash
pnpm lint
pnpm format --check
pnpm typecheck  # if available
```

### 2. Policy review

Review against:

- **mern-std** — coding standards, project structure, conventions
- **mern-nfr** — performance, reliability, observability, accessibility
- **mern-sec** — input validation, injection prevention, auth, error handling

For each issue, note:

- Category: `std` | `nfr` | `sec`
- Severity: `must-fix` | `should-fix` | `nice-to-have`
- File and location
- What's wrong and how to fix it

### 3. Report results

Summary of automated gate results + policy findings grouped by severity.

### 4–5. Approval gate, fix and confirm

See `/shared-review-workflow` for severity definitions, approval gate protocol, and fix constraints. Run `/mern-unit-test` to confirm no regressions after fixes.

## Reference

For review checklists and common issues, see `reference/mern-code-review-reference.md`
