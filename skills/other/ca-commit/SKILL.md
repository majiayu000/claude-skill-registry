---
name: ca-commit
description: Run the full commit gate — the only sanctioned path to a git commit.
argument-hint: (none)
---

# /ca-commit — commit gate

The only path to a commit. The orchestrator issues no `git commit` without the `commit-gate` skill
clearing first. "It looks good" is not authorization. No arguments — the skill reads current git
state (staged files, diff, test results) and decides whether every gate is green.

## Routes to

The `commit-gate` skill (`<plugin-root>/routines/commit-gate/SKILL.md`) — all phases. The skill
is canonical for its phases, gates, and output format.

## When NOT to use

- Before writing code → `/ca-feature` or `/ca-fix` first.
- To check PR readiness → `/ca-pr` (dispatches additional BLOCK-level reviewers).
- To run tests without committing → run the test command from `tech-stack.md` directly.

## Hard gate

MUST NOT commit without `commit-gate` clearing. MUST NOT commit if the project test suite is not
green.
