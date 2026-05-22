---
name: git-worktrees
description: Master Git worktrees for parallel development, PR reviews, and experiments. Create isolated working directories for multiple branches simultaneously. Use when working on multiple branches at once, reviewing PRs, or running experiments without affecting main work. Triggers on worktree, parallel development, multiple branches, PR review isolation, experiment branch, feature isolation.
---

# Git Worktrees

Work on multiple branches simultaneously without stashing or switching.

## Quick Reference

### Core Commands

| Action | Command |
|--------|---------|
| List worktrees | `git worktree list` |
| Add worktree | `git worktree add ../path branch` |
| Add new branch | `git worktree add -b new-branch ../path` |
| Remove worktree | `git worktree remove ../path` |
| Prune stale | `git worktree prune` |
| Lock worktree | `git worktree lock ../path` |

## Key Concepts

### What is a Worktree?

```
main-repo/                    # Main worktree (default)
+-- .git/                     # Shared Git database
+-- src/
+-- ...

../main-repo-feature-auth/    # Linked worktree
+-- .git --> main-repo/.git   # Points to main .git
+-- src/                      # Independent working files
+-- ...
```

### Benefits

| Benefit | Description |
|---------|-------------|
| **No stashing** | Keep uncommitted work while switching context |
| **Parallel work** | Work on multiple features simultaneously |
| **Clean reviews** | Review PRs in isolated directories |
| **Experiments** | Try things without affecting main work |
| **Fast switching** | Just `cd` to another directory |

## Common Workflows

### 1. Parallel Feature Development

```bash
# You're working on feature A
cd ~/repos/my-project
git checkout feature-a
# ... making changes ...

# Urgent: Need to work on feature B
git worktree add ../my-project-feature-b feature-b

# Work on feature B in the new directory
cd ../my-project-feature-b
# ... make changes, commit ...

# Go back to feature A - your work is still there!
cd ../my-project
```

### 2. PR Review in Isolation

```bash
# Fetch the PR
git fetch origin pull/123/head:pr-123

# Create worktree for review
git worktree add ../project-pr-123 pr-123

# Review in the isolated worktree
cd ../project-pr-123
npm install && npm test

# Back to your work
cd ../project

# Clean up after review
git worktree remove ../project-pr-123
git branch -d pr-123
```

### 3. Long-running Experiments

```bash
# Create experiment worktree
git worktree add -b experiment/new-architecture ../project-experiment

# Work on experiment over days/weeks
cd ../project-experiment

# Lock it to prevent accidental deletion
git worktree lock ../project-experiment

# Continue normal work in main repo
cd ../project
```

### 4. Hotfix While Mid-Feature

```bash
# Mid-feature, need to hotfix
git worktree add ../project-hotfix main

cd ../project-hotfix
git checkout -b hotfix/critical-bug

# Fix, test, push
git add . && git commit -m "fix: critical bug"
git push origin hotfix/critical-bug

# Clean up and return
cd ../project
git worktree remove ../project-hotfix
```

## Naming Convention

Recommended worktree directory naming:

```
{repo-name}-{purpose}/
```

Examples:
- `my-app-feature-auth/` - Feature work
- `my-app-pr-123/` - PR review
- `my-app-experiment-v2/` - Experimental work
- `my-app-hotfix/` - Hotfix branch

## Best Practices

### DO
- Use descriptive directory names
- Clean up worktrees after use
- Lock long-running worktrees
- Run `git worktree prune` periodically
- Keep worktrees in sibling directories

### DON'T
- Create worktrees inside the main repo
- Delete worktree directories manually (use `git worktree remove`)
- Forget to install dependencies in each worktree
- Have too many worktrees (they take disk space)
- Share node_modules between worktrees

## IDE Integration

### VS Code

Open each worktree as a separate window:
```bash
cd ../project-feature-b
code .
```

Or use Multi-root Workspaces to see all worktrees.

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "branch already checked out" | That branch is in another worktree |
| "not a git repository" | Worktree was moved/deleted incorrectly |
| Stale worktree entries | Run `git worktree prune` |
| Can't delete worktree | `git worktree unlock` first if locked |
| Missing dependencies | Run install in each worktree |

## When to Use This Skill

- Working on multiple features simultaneously
- Reviewing pull requests without disrupting work
- Running long-term experiments
- Handling urgent hotfixes mid-feature
- Testing different branches side by side
- Comparing code across branches
