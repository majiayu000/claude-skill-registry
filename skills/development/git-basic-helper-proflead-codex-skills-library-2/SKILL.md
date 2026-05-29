---
name: git-basic-helper
description: Provide safe git commands for common tasks. Use when a junior developer needs help with branching, commits, or resolving simple conflicts.
---

# Git Basic Helper

## Purpose
Provide safe git commands for common tasks.

## Inputs to request
- Goal (branch, commit, sync, or resolve conflict).
- Current branch and remote name.
- Any uncommitted changes or stashes.

## Workflow
1. Clarify the goal (new branch, commit, update, or simple rebase).
2. Provide minimal commands with explanations and safety notes.
3. Call out any files to inspect before pushing.

## Output
- Exact git command sequence.
- Warnings for destructive operations.

## Quality bar
- Avoid destructive commands unless explicitly requested.
- Explain when to pause and inspect state.
