---
name: managing-branches
description: >
  Investigates and creates Git branches.
  Triggered when: branch status check, new branch creation, branch-related errors.
allowed-tools: Bash(git:*)
---

# Branch Investigation

```bash
git branch --show-current
git status --short
git fetch --all
git branch -vv
git rev-list --count <main-branch>..HEAD 2>/dev/null || echo "0"  # Check CLAUDE.md for main branch name
```

Report: current branch, uncommitted changes, remote sync status, commits ahead of main.

# Branch Creation

```bash
git fetch origin <base-branch>
git checkout -b <new-branch> origin/<base-branch>
```

# Error Handling

| Error | Action |
|-------|--------|
| Branch exists | Report to user, suggest alternative or confirm use existing |
| Uncommitted changes | `git stash` or commit first |
| Remote sync error | `git fetch --all` retry |
| Permission error | Report to user |

# Conflict Resolution

1. `git status` to identify conflicts
2. Resolve each file
3. `git add <resolved-file>`
4. Continue operation

Ask for guidance if resolution is complex.

# Completion Report

- Current branch name
- Branch creation result (if applicable)
- Any issues encountered
