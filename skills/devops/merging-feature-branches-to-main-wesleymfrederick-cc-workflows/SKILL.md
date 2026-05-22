---
name: merging-feature-branches-to-main
description: Use when feature branch is complete and reviewed, ready to merge to main - squashes multiple commits into single clean commit in main using git merge --squash
---

# Merging Feature Branches to Main

## Overview

Merge a completed and reviewed feature branch into main using `git merge --squash` to create a single clean commit in main's history.

**Core principle:** Main branch shows feature-level history (one commit per user story), not development-level history (many TDD commits).

**Workflow context:**
1. Worktree implementation → feature branch (via `finishing-a-development-branch`)
2. Human review on feature branch
3. Feature branch → main (THIS SKILL - squash merge)

## When to Use

Use this skill when:
- Feature branch has all implementation work merged in (from worktrees)
- Human has reviewed the feature branch
- Ready to integrate feature branch into main
- Want single clean commit in main (not 10+ granular commits)
- Using TDD workflow that created many commits during implementation

Do NOT use when:
- Still working in worktree (use `finishing-a-development-branch` first)
- Feature hasn't been reviewed yet
- Tests are failing on feature branch
- Working directly on main branch
- Want to preserve all individual commits in main history

## Background

We use TDD which creates many commits during development (test, implementation, refactor cycles). These granular commits are valuable during development but should be squashed to one commit when merging to main.

## Prerequisites Checklist

Before starting, verify:

```bash
# 1. Check current branch (should be on feature branch)
git branch --show-current

# 2. Verify working directory is clean
git status
# Should show "working tree clean"

# 3. Ensure all work is committed
git log --oneline -5
# Review recent commits to confirm work is saved

# 4. Verify main branch exists
git branch -a | grep main
```

**If any check fails, STOP and resolve before proceeding.**

## Step-by-Step Workflow

### Step 1: Switch to Main Branch

```bash
git checkout main
```

If you have a remote, update main:

```bash
git pull origin main
```

### Step 2: Perform Squash Merge

```bash
git merge --squash <feature-branch-name>
```

This stages all changes from feature branch WITHOUT creating a commit yet.

Verify changes are staged:

```bash
git status
# Should show "Changes to be committed"
```

### Step 3: Create Commit with create-git-commit Skill

**REQUIRED SUB-SKILL:** Use `create-git-commit` skill to craft the commit message.

Do NOT write commit message manually. The create-git-commit skill ensures proper format, scope, and message quality.

```bash
# The create-git-commit skill will guide you through:
# - Analyzing the staged changes
# - Following repository commit message conventions
# - Creating a well-formatted commit message
```

After create-git-commit skill creates the commit, verify:

```bash
git log --oneline -1
# Should show your new squashed commit
```

### Step 4: Delete Feature Branch

After successful merge, clean up the feature branch:

```bash
# Force delete (required since squash doesn't create merge commit)
git branch -D <feature-branch-name>
```

**Why -D:** The `-D` flag force-deletes because `--squash` doesn't create a merge commit, so git doesn't recognize the branch as "merged" with `-d`.

### Step 5: Push to Remote (if applicable)

```bash
git push origin main
```

### Step 6: Verification

Confirm main branch has clean history:

```bash
# View recent commits
git log --oneline -5

# Verify one commit for the feature (not 10+)
# Verify commit message follows conventions
```

Run tests on main to ensure everything works:

```bash
npm test
# Or your test command
```

## Error Handling

| Problem | Solution |
|---------|----------|
| Uncommitted changes on feature branch | Commit or stash changes before switching |
| Merge conflicts after squash | Resolve conflicts, `git add` files, then create commit |
| Feature branch not found | Verify branch name with `git branch -a` |
| Already on main branch | Checkout feature branch first, or specify branch name differently |
| Branch deletion fails | Use `-D` flag for force delete (squash merges don't mark as "merged") |

## Quick Reference

```bash
# Complete workflow
git checkout main
git pull origin main                      # If using remote
git merge --squash <feature-branch>
# Use create-git-commit skill here
git branch -D <feature-branch>
git push origin main                      # If using remote
git log --oneline -5                      # Verify
```

## Common Mistakes

### ❌ Writing commit message manually

```bash
git commit -m "Add feature"  # WRONG
```

### ✅ Using create-git-commit skill
- Ensures proper format and conventions
- Analyzes all changes in the squash
- Creates comprehensive feature-level message

### ❌ Using -d flag for deletion

```bash
git branch -d feature-x  # FAILS
# Error: not fully merged
```

### ✅ Using -D flag

```bash
git branch -D feature-x  # WORKS
# Squash merges require force delete
```

### ❌ Forgetting to delete branch
- Leaves stale branches cluttering repository
- Makes it unclear which branches are active

### ✅ Always delete after successful merge
- Keeps repository clean
- Makes active work visible
