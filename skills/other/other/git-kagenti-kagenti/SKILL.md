---
name: git
description: Git operations including worktrees, branching, and repository management
---

# Git Skills

Git operations for development workflows.

## Sub-Skills

| Skill | Description |
|-------|-------------|
| `git:commit` | Create properly formatted commits |
| `git:rebase` | Rebase branches onto upstream main |
| `git:status` | Show worktrees with PR status and TODO files overview |
| `git:worktree` | Manage git worktrees for parallel development |

## When to Use

- Committing code with proper format (`git:commit`)
- Rebasing branches onto upstream (`git:rebase`)
- Creating worktrees for parallel development (`git:worktree`)
- Managing branches across worktrees
- Setting up isolated development environments

## Quick Commands

```bash
# List worktrees
git worktree list

# Create worktree
git worktree add .worktrees/<name> -b <branch> main

# Remove worktree
git worktree remove .worktrees/<name>

# Prune stale references
git worktree prune
```

## Why Worktrees?

- **Parallel development**: Work on multiple features simultaneously
- **No context switching**: Each worktree has its own working directory
- **CI-like testing**: Test different branches in isolation
- **Code review**: Check out PRs without affecting your work
