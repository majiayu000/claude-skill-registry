---
name: using-git-worktrees
description: Use when developing multiple features in parallel. Isolated workspaces prevent conflicts and enable concurrent branches.
---

# SKILL: Using Git Worktrees

> **Purpose**: Parallel development using isolated workspaces for concurrent feature branches
> **Target**: Developers working on multiple features simultaneously

---

## Quick Start

### When to Use This Skill
- Developing multiple features concurrently
- Running long-running tests on one branch while working on another
- Isolating experimental changes without stash/commit dance
- Hotfix production while continuing feature work

### Quick Reference
```bash
# Create new worktree
git worktree add ../project-feature-1 feature-1
git worktree add ../project-feature-2 feature-2

# List worktrees
git worktree list

# Remove worktree after merge
git worktree remove ../project-feature-1
```

---

## Core Concepts

### Worktree Creation

**Basic Syntax**:
```bash
git worktree add <path> <branch> [<start-point>]
```

**Examples**:
```bash
# Create worktree for existing branch
git worktree add ../myproject-feature feature-x

# Create worktree for new branch
git worktree add ../myproject-experiment -b experiment-branch

# Create worktree at specific commit
git worktree add ../myproject-v1.0 -b v1.0-fixes a1b2c3d
```

### Worktree Management

**List worktrees**:
```bash
git worktree list
# Output:
# /path/to/main              abc1234 [main]
# /path/to/feature-1         def5678 [feature-1]
# /path/to/hotfix            ghi9012 [hotfix/security-fix]
```

**Remove worktree**:
```bash
# Prune after deleting directory manually
rm -rf ../myproject-feature
git worktree prune

# Remove directly
git worktree remove ../myproject-feature
```

**Lock worktree** (prevent cleanup):
```bash
git worktree lock ../myproject-critical
git worktree unlock ../myproject-critical
```

### Workflow Integration

**Parallel Development Pattern**:
```bash
# Main workspace: feature work
cd ~/project-main
git checkout -b feature-auth

# Worktree 1: Hotfix
git worktree add ../project-hotfix -b hotfix-login
cd ../project-hotfix
# Fix hotfix, test, commit, push

# Worktree 2: Experiment
git worktree add ../project-experiment -b experiment-ui
cd ../project-experiment
# Try new UI approach, discard if fails

# Return to main workspace
cd ~/project-main
# Continue feature work, merge hotfix when ready
```

---

## Cleanup

### After Feature Merge

```bash
# 1. Merge feature branch to main
git checkout main
git merge feature-1

# 2. Remove worktree
git worktree remove ../project-feature-1

# 3. Delete branch (optional)
git branch -d feature-1

# 4. Prune stale worktrees
git worktree prune
```

### Automated Cleanup

```bash
# Remove all worktrees for merged branches
git worktree list | while read path commit branch; do
  if git merge-base --is-ancestor "${branch:0:-1}" main 2>/dev/null; then
    git worktree remove "$path"
  fi
done
```

---

## Verification

### Test Worktree Operations
```bash
# Create test worktree
git worktree add /tmp/test-worktree -b test-worktree-branch

# Verify it exists
git worktree list | grep test-worktree-branch

# Verify isolation
cd /tmp/test-worktree
git status  # Should show test-worktree-branch, not main

# Cleanup
git worktree remove /tmp/test-worktree
```

---

## Troubleshooting

### Worktree Already Registered

**Error**: `working tree '.claude' already exists`

**Solution**: Remove existing worktree first
```bash
git worktree list  # Find the worktree
git worktree remove <path>  # Remove it
```

### Detached HEAD in Worktree

**Issue**: Worktree showing commit hash instead of branch

**Fix**: Create local branch
```bash
cd ../project-worktree
git checkout -b local-branch-name
```

---

## Related Skills

- **git-operations**: Push/pull/merge operations across worktrees
- **parallel-subagents**: Coordinate work across multiple worktrees
- **git-master**: Git workflow mastery including worktrees

---

**Version**: claude-pilot 4.3.0
