---
name: github-conflicts
description: Resolve merge conflicts safely
---

# GitHub Conflicts Skill

Safely resolve merge and rebase conflicts with user guidance.

> **See also**: [Shared Conventions](../shared/CONVENTIONS.md) | [Safety Guidelines](../shared/SAFETY.md)

## Purpose

Handle merge conflicts methodically without guessing at resolutions.

## Commands

```bash
git status
git diff
git merge <branch>
git rebase <branch>
git cherry-pick <commit>
git mergetool
git add <file>
git rebase --continue
git merge --abort
git rebase --abort
```

## Conflict Resolution Protocol

**Do not guess at resolutions.** Follow this process:

### 1. Stop and Enumerate

List all conflicting files:
```bash
git status
```

### 2. Analyze Each Conflict

For each conflicting file, show:
- The conflicting sections
- **Ours** (current branch version)
- **Theirs** (incoming version)

```bash
git diff --name-only --diff-filter=U
```

### 3. Present Options

For each conflict, propose:
1. **Accept ours** - keep current branch version
2. **Accept theirs** - take incoming version
3. **Manual merge** - combine both with specific proposal

### 4. Apply Resolution

Only after user confirms:
```bash
# Edit file to resolve
git add <resolved-file>
git rebase --continue  # or git merge --continue
```

## Workflow: Rebase Conflicts

```bash
# Start rebase
git fetch origin
git rebase origin/main

# If conflicts occur:
# 1. List conflicts
git status

# 2. Show conflict details (present to user)

# 3. After user decision, resolve and continue
git add <file>
git rebase --continue
```

## Workflow: Merge Conflicts

```bash
# Start merge
git merge feature-branch

# If conflicts occur:
# 1. List conflicts
git status

# 2. Show conflict details (present to user)

# 3. After user decision, resolve and commit
git add <file>
git commit
```

## Abort Options

If resolution becomes too complex:
```bash
git merge --abort
git rebase --abort
git cherry-pick --abort
```

## Policies

- **Never auto-resolve** conflicts without user confirmation
- Always show both versions before proposing resolution
- Offer abort as an option for complex conflicts
- Verify successful resolution with `git status`
- Run tests after resolving if applicable
