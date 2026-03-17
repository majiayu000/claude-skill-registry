---
name: commit-conventions
description: Commit message style and structure for this repository.
---

# Commit Message Conventions

## Format

Use the following format:

`<type>(<optional scope>): <short summary>`

Examples:
- `feat(kql): add materialized views for sales KPIs`
- `fix(datagen): handle null payloads in streaming`
- `chore(notebooks): update Silver to Gold transforms`

## Types

- `feat` – new user-facing feature
- `fix` – bug fix
- `refactor` – structural code changes without behavior change
- `chore` – tooling, CI, non-runtime code
- `docs` – documentation-only changes
- `perf` – performance improvements
- `test` – adding or adjusting tests

## Body

- Use when additional explanation is necessary.
- Include:
  - Motivation for the change
  - Notable design decisions
  - Links to tickets or issues

## Footer

- Include breaking change notes:
  - `BREAKING CHANGE: [description]`
- Include issue references:
  - `Fixes #1234`
