---
name: git-workflow
description: Quick reference for common Git commands and workflows. Use when working with version control, committing changes, managing branches, or resolving Git issues. Covers daily Git operations, branching strategies, and troubleshooting.
---

# Git Workflow

## Overview

A concise reference for common Git commands and workflows used in daily development. This skill provides quick access to frequently-used Git operations without searching documentation.

## Daily Workflow

### Check Status and Changes

```bash
# View current status
git status

# View changes in working directory
git diff

# View staged changes
git diff --cached

# View commit history
git log --oneline --graph --all
```

### Staging and Committing

```bash
# Stage specific files
git add <file1> <file2>

# Stage all changes
git add .

# Stage only modified files (not new files)
git add -u

# Commit staged changes
git commit -m "Commit message"

# Add and commit in one step
git commit -am "Commit message"

# Amend last commit
git commit --amend
```

### Syncing with Remote

```bash
# Fetch changes from remote
git fetch origin

# Pull changes (fetch + merge)
git pull origin main

# Push commits to remote
git push origin main

# Push new branch to remote
git push -u origin <branch-name>
```

## Branching

### Creating and Switching Branches

```bash
# Create new branch
git branch <branch-name>

# Switch to branch
git checkout <branch-name>

# Create and switch in one step
git checkout -b <branch-name>

# Switch to previous branch
git checkout -

# List all branches
git branch -a
```

### Merging and Rebasing

```bash
# Merge branch into current branch
git merge <branch-name>

# Rebase current branch onto main
git rebase main

# Interactive rebase (squash, reorder commits)
git rebase -i HEAD~3

# Abort merge/rebase
git merge --abort
git rebase --abort
```

### Deleting Branches

```bash
# Delete local branch
git branch -d <branch-name>

# Force delete local branch
git branch -D <branch-name>

# Delete remote branch
git push origin --delete <branch-name>
```

## Undoing Changes

### Unstage and Discard

```bash
# Unstage file (keep changes)
git restore --staged <file>

# Discard changes in working directory
git restore <file>

# Discard all local changes
git restore .
```

### Reverting Commits

```bash
# Revert specific commit (creates new commit)
git revert <commit-hash>

# Reset to previous commit (soft - keep changes)
git reset --soft HEAD~1

# Reset to previous commit (hard - discard changes)
git reset --hard HEAD~1

# Reset to specific commit
git reset --hard <commit-hash>
```

### Stashing

```bash
# Stash current changes
git stash

# Stash with message
git stash save "Work in progress"

# List stashes
git stash list

# Apply most recent stash
git stash apply

# Apply and remove stash
git stash pop

# Apply specific stash
git stash apply stash@{2}

# Delete stash
git stash drop stash@{0}

# Clear all stashes
git stash clear
```

## Repository Setup

### Initializing and Cloning

```bash
# Initialize new repository
git init

# Clone repository
git clone <url>

# Clone to specific directory
git clone <url> <directory>

# Clone specific branch
git clone -b <branch-name> <url>
```

### Remote Management

```bash
# Add remote
git remote add origin <url>

# View remotes
git remote -v

# Change remote URL
git remote set-url origin <new-url>

# Remove remote
git remote remove origin
```

## Troubleshooting

### Conflict Resolution

```bash
# View files with conflicts
git status

# After resolving conflicts manually
git add <resolved-file>
git commit

# Abort merge and start over
git merge --abort
```

### Finding and Inspecting

```bash
# Search for text in commits
git log -S "search term"

# View specific commit
git show <commit-hash>

# View file at specific commit
git show <commit-hash>:<file-path>

# Find who changed a line
git blame <file>

# View reflog (history of HEAD)
git reflog
```

### Cleaning Up

```bash
# Remove untracked files (dry run)
git clean -n

# Remove untracked files
git clean -f

# Remove untracked files and directories
git clean -fd
```

## Best Practices

### Commit Messages

```bash
# Good commit message format:
# <type>: <subject>
#
# <body>

# Examples:
git commit -m "feat: Add user authentication"
git commit -m "fix: Resolve login redirect bug"
git commit -m "docs: Update API documentation"
git commit -m "refactor: Simplify validation logic"
```

### Branch Naming

```
feature/<feature-name>    # New features
bugfix/<bug-name>         # Bug fixes
hotfix/<issue>            # Urgent fixes
release/<version>         # Release preparation
```

### Common Workflows

**Feature Branch Workflow:**
```bash
# 1. Create feature branch
git checkout -b feature/new-feature

# 2. Work and commit
git add .
git commit -m "feat: Implement new feature"

# 3. Push to remote
git push -u origin feature/new-feature

# 4. After review, merge to main
git checkout main
git pull origin main
git merge feature/new-feature
git push origin main

# 5. Delete feature branch
git branch -d feature/new-feature
git push origin --delete feature/new-feature
```

## Quick Tips

- **Undo last commit but keep changes:** `git reset --soft HEAD~1`
- **View graphical log:** `git log --oneline --graph --all --decorate`
- **Cherry-pick specific commit:** `git cherry-pick <commit-hash>`
- **Create tag:** `git tag -a v1.0.0 -m "Version 1.0.0"`
- **View diff between branches:** `git diff branch1..branch2`
- **Update last commit message:** `git commit --amend -m "New message"`
- **List files in commit:** `git show --name-only <commit-hash>`
