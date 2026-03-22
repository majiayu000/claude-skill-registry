---
name: cleanup
description: >
  Clean up the development environment: remove git worktrees, stale branches,
  merged remote branches (with no open PR), git stashes, stale remote-tracking refs,
  coverage/test artifacts, node_modules cache, and Claude temp files.
  Use when the repo feels cluttered or before a fresh start.
allowed-tools: Bash, Read, Grep, Glob
---

# Environment Cleanup

Run the cleanup script to remove stale branches, worktrees, caches, and artifacts.

## Usage

Invoke from the repo root:

```bash
# Preview what will be cleaned (no deletions)
bash .claude/skills/cleanup/cleanup.sh --dry-run

# Actually clean everything
bash .claude/skills/cleanup/cleanup.sh
```

## What it cleans

1. **Git worktrees** under `.claude/worktrees/`
2. **Stale local branches** (anything not `main`)
3. **Remote branches** with no open PR — merged or abandoned (uses `gh` CLI)
4. **Git stashes** (drops all)
5. **Stale remote-tracking refs** (`git remote prune origin`)
6. **Coverage/test artifacts** (`coverage*`, `playwright-report`, `test-results`)
7. **node_modules/.cache**
8. **Claude temp files** in `/tmp`

## Flags

| Flag | Description |
|------|-------------|
| `--dry-run` | Preview actions without making changes |

## Notes

- Always skips `main` branch
- Always skips branches with open PRs on GitHub
- Idempotent: safe to run multiple times
- Requires `gh` CLI to be authenticated for remote branch cleanup
