---
name: commit-conventions
description: Create conventional commit messages and plan commits. Use when a user asks to commit changes, write commit messages, or organize commits. Enforce repo-specific git/commit rules from AGENTS.md and split multiple logical changes into separate, digestible commits.
---

# Commit Conventions

## Overview

Plan and execute commits that follow Conventional Commits plus any repository rules in AGENTS.md. Default to multiple commits when changes span more than one logical unit.

## Workflow

1. Read AGENTS.md (repo root or nearest) and apply any git/commit rules.
2. Inspect the working tree: `git status -sb`, `git diff --stat`, and focused `git diff` as needed.
3. Group changes by logical unit (feature, fix, refactor, docs, build/CI, etc.).
4. If more than one logical unit exists, create multiple commits. Propose a brief commit plan before committing.
5. Message heuristic: if draft subject wants `and`, list separators, or >1 scope/target, split before committing.
6. Stage per group (`git add -p` or specific paths), then commit with a Conventional Commit message.
7. If the user asks for a single commit but changes are multiple logical units, warn and ask for confirmation before combining.

## Hook Rewrite Recovery

- If `git commit` fails because pre-commit hooks rewrote files (formatter/linter), do not change the commit plan.
- Re-stage only hook-modified files, confirm staged set (`git diff --cached --name-only`), and re-run the same commit message.
- If hooks keep rewriting on every attempt, run the project formatter command once, stage result, then commit.

## Git Lock Recovery

- If commit/stash fails with `.git/index.lock`, first confirm no active git process is still running.
- If no git process is active, remove only `.git/index.lock`, keep staged set unchanged, and retry the same command.
- Never use reset/checkout cleanup as lock recovery; lock errors are process-state issues, not content-state issues.

## Conventional Commit Format

- Default format: `<type>: <subject>`
- Use scope only for monorepos with multiple targets, and scope to the target: `<type>(<target>): <subject>`.
- Otherwise do not use scope.
- Subject is imperative, lowercase, and has no trailing period.

## Type Selection

- Prefer repo-specific types from AGENTS.md.
- Otherwise use standard types: `feat`, `fix`, `refactor`, `perf`, `docs`, `test`, `build`, `ci`, `chore`, `revert`.
- `style` is intentionally excluded here: use it only for code style or formatting-only changes, not for UI, design-system, visual, UX, or theming work.
- UI or visual behavior changes usually map to `fix`, `feat`, or `refactor` based on intent.

## File Hygiene

- Exclude unrelated changes or generated artifacts unless explicitly required.
- If untracked files appear, confirm they are intended before staging.
- Avoid mixing unrelated existing changes into the same commit.

## Examples

- `fix: use macos match certificates for signing`
- `build: split plugin signing into notarized release artifacts`
- `feat(ios-app): add waveform preview in editor` (monorepo multi-target only)
