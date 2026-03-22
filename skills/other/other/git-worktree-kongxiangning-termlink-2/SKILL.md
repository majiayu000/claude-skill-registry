---
name: git-worktree
description: Create, inspect, and clean up Git worktrees for parallel TermLink branch development. Use when starting isolated feature or bugfix work in a separate directory, checking which branches already have attached worktrees, removing stale worktrees after merge, or pruning orphaned worktree metadata.
---

# Git Worktree

## Overview

Use this skill to run multiple TermLink tasks in parallel without stashing or mixing local changes in one checkout.

Run commands from repository root:
`E:\coding\TermLink`

## Quick Checks

1. List active worktrees before creating or removing anything:
```powershell
git worktree list
```

2. Confirm whether a branch already exists:
```powershell
git branch --list feat/my-topic
```

## Create A Worktree

Preferred helper for a new branch worktree:

```powershell
powershell -ExecutionPolicy Bypass -File .\skills\git-worktree\scripts\new-worktree.ps1 -Branch feat/my-topic -Base main
```

Behavior:

1. Resolve the current repository root.
2. Create a sibling directory such as `E:\coding\TermLink-feat-my-topic`.
3. Run `git worktree add -b <branch> <path> <base>`.
4. Print the created path for follow-up work.

Optional variants:

```powershell
# Reuse an existing branch instead of creating a new one
powershell -ExecutionPolicy Bypass -File .\skills\git-worktree\scripts\new-worktree.ps1 -Branch feat/my-topic -CheckoutExisting

# Override the default path
powershell -ExecutionPolicy Bypass -File .\skills\git-worktree\scripts\new-worktree.ps1 -Branch feat/my-topic -Base main -Path E:\coding\TermLink-wt\feat-my-topic
```

## Remove And Prune

Remove a worktree after merge or abandonment:

```powershell
git worktree remove E:\coding\TermLink-feat-my-topic
git worktree prune
```

Use force only when the user explicitly wants to discard uncommitted changes:

```powershell
git worktree remove --force E:\coding\TermLink-feat-my-topic
git worktree prune
```

## Rules

1. Check `git worktree list` before creating a new worktree to avoid path or branch collisions.
2. Prefer an explicit base branch such as `main` for new feature worktrees.
3. Keep worktrees outside the repository root as sibling directories; do not create nested worktrees inside tracked folders.
4. Do not remove a worktree with uncommitted changes unless the user explicitly asks to discard them.
5. Run `git worktree prune` after removal so stale metadata does not block later reuse.
