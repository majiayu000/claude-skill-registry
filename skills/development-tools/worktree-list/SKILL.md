---
name: worktree-list
description: List all active feature worktrees with their status. Shows branch name, commits ahead of main, and whether there are uncommitted changes. Use to get an overview when working with multiple parallel features.
disable-model-invocation: true
allowed-tools:
  - Bash
---

# Worktree List

Shows a status summary of all active feature worktrees in `.worktrees/`.

## What it shows

For each active worktree:
- Feature name and branch
- Commits ahead of `main`
- Dirty status (uncommitted files count)
- Last commit message and time

## Usage

```
/worktree-list
```

## How to execute

**Run from the original project directory.**

```bash
bash .claude/skills/worktree-list/scripts/worktree-list.sh
```

## Important

- Only lists worktrees managed by `worktree-start` (in `.worktrees/`)
- If no worktrees are active, suggests running `/worktree-start`
