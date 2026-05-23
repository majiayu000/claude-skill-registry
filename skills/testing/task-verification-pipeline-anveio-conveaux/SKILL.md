---
name: task-verification-pipeline
description: Run and debug a repo verification pipeline (`./verify.sh --ui=false` or equivalent), including stage selection and opt-in E2E tiers.
---

# Verification Pipeline

## When to use

Use this when the task mentions:

- `./verify.sh`, “verification pipeline”, “format/lint/typecheck/test/build”
- CI failures or “why does verify fail”
- Enabling E2E (`--e2e=smoke|standard|full`)

## Default workflow

1. Establish baseline (headless): `./verify.sh --ui=false`
2. If it fails, fix the failing stage and rerun until green.
3. Only run E2E when needed: `./verify.sh --ui=false --e2e=standard`

## Key facts

- E2E is opt-in; default verify skips it unless `--e2e` is set.
- Prefer root scripts (`npm run lint`, `npm run typecheck`, `npm run test`, `npm run build`) for targeted iteration.

## Slash Commands

Use these for accelerated workflows:

| Command | Purpose |
|---------|---------|
| `/verify` | Run full pipeline or specific stage (`/verify lint`) |
| `/verify-lint [package]` | Quick lint check with optional scope |
| `/lint-and-learn` | Auto-fix lint + extract lessons + create PR |

## Canonical repo docs

- Your repo’s verification runner docs (commonly `apps/dev-tooling/README.md` or similar).
- Your repo’s verification entrypoint (commonly `verify.sh` or a `npm run verify` script).
