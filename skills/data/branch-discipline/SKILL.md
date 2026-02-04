---
name: branch-discipline
description: Use before any code changes - hard gate ensuring work never happens on main branch, with proper feature branch creation from correct base
---

# Branch Discipline

## Overview

Never work on main. Create feature branches for all work.

**Core principle:** The main branch is sacred. All work happens in feature branches.

**This is a HARD GATE.** Do not proceed with code changes if on main.

## The Gate

```
┌─────────────────────────────────────┐
│         CODE CHANGE NEEDED          │
└─────────────────┬───────────────────┘
                  │
                  ▼
        ┌─────────────────┐
        │ Current branch? │
        └────────┬────────┘
                 │
       ┌─────────┴─────────┐
       │                   │
     main              feature/*
       │                   │
       ▼                   ▼
  ┌─────────┐         ┌─────────┐
  │  STOP   │         │ PROCEED │
  │ Create  │         │  with   │
  │ branch  │         │  work   │
  └─────────┘         └─────────┘
```

## Check Current Branch

```bash
# Show current branch
git branch --show-current

# If output is "main" or "master" → STOP
# If output is feature/* or fix/* → PROCEED
```

## Branch Naming Convention

### Format

```
[type]/issue-[number]-[short-description]
```

### Types

| Type | Use For |
|------|---------|
| `feature` | New functionality |
| `fix` | Bug fixes |
| `chore` | Maintenance, dependencies |
| `docs` | Documentation only |
| `refactor` | Code restructuring |
| `test` | Test additions/fixes |

### Examples

```
feature/issue-123-user-authentication
fix/issue-456-login-redirect-loop
chore/issue-789-update-dependencies
docs/issue-101-api-documentation
refactor/issue-202-extract-validation
test/issue-303-add-integration-tests
```

## Creating a Feature Branch

### From Main (Default)

```bash
# Ensure main is up to date
git checkout main
git pull origin main

# Create and checkout new branch
git checkout -b feature/issue-[NUMBER]-[description]

# Push branch to remote (establishes tracking)
git push -u origin feature/issue-[NUMBER]-[description]
```

### From Existing Feature Branch

When building on in-progress work:

```bash
# Checkout the base branch
git checkout feature/issue-100-base-feature

# Ensure it's up to date
git pull origin feature/issue-100-base-feature

# Create new branch from it
git checkout -b feature/issue-101-dependent-feature
```

**Document the dependency** in the issue.

## Branch Lifecycle

```
Create → Work → Push → PR → Merge → Delete
```

### After Merge

```bash
# Switch to main
git checkout main

# Pull the merge
git pull origin main

# Delete local branch
git branch -d feature/issue-123-completed-feature

# Delete remote branch (usually done via PR UI)
git push origin --delete feature/issue-123-completed-feature
```

## Handling Stale Branches

If main has moved ahead:

```bash
# Option 1: Rebase (preferred for clean history)
git checkout feature/issue-123-my-feature
git fetch origin
git rebase origin/main

# Option 2: Merge (if conflicts are complex)
git checkout feature/issue-123-my-feature
git fetch origin
git merge origin/main
```

## Protected Branches

Main should be protected. Never:

- Push directly to main
- Force push to main
- Delete main

If you accidentally commit to main:

```bash
# If not yet pushed - move commits to new branch
git branch feature/issue-123-accidental-main
git reset --hard origin/main

# If already pushed - DO NOT force push
# Instead, revert and recreate in proper branch
```

## Multiple Issues, Same Branch?

**Generally NO.** Each issue gets its own branch.

**Exception:** Tightly coupled sub-issues from `issue-decomposition` MAY share a branch if:
- They are sequential dependencies
- They will be merged together
- They are part of the same PR

Document this in the issues if doing so.

## Verification

Before making any code change:

```bash
# Check current branch
BRANCH=$(git branch --show-current)

# Verify not on main
if [ "$BRANCH" = "main" ] || [ "$BRANCH" = "master" ]; then
    echo "ERROR: On protected branch. Create feature branch first."
    exit 1
fi

# Verify branch follows naming convention
if ! echo "$BRANCH" | grep -qE '^(feature|fix|chore|docs|refactor|test)/issue-[0-9]+-'; then
    echo "WARNING: Branch name doesn't follow convention"
fi
```

## Common Mistakes

| Mistake | Prevention |
|---------|------------|
| Committing to main | Check branch before every commit |
| Pushing to main | Branch protection rules |
| Wrong base branch | Verify before creating branch |
| Outdated branch | Rebase/merge before PR |
| Branch name typos | Use consistent naming |

## Checklist

Before writing any code:

- [ ] Current branch is NOT main
- [ ] Branch name follows convention
- [ ] Branch is from correct base
- [ ] Branch is pushed to remote
- [ ] Issue number is in branch name

## Integration

This skill is called by:
- `issue-driven-development` - Step 6

This skill enables:
- Clean separation of work
- Easy PR creation
- Safe experimentation
