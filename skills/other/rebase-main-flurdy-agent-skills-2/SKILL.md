---
name: rebase-main
description: Rebase the current branch onto an updated main branch. Use when main has been updated and you need to incorporate those changes into your feature branch.
---

# Rebase onto Main

Rebase the current feature branch onto the latest main branch.

## Usage

```
/rebase-main
```

## Instructions

### 1. Check Current State

```bash
# Get current branch
git branch --show-current

# Check for uncommitted changes
git status --porcelain
```

If there are uncommitted changes, ask the user whether to:
- Stash them before rebasing
- Commit them first
- Abort the rebase

### 2. Fetch Latest Main

```bash
git fetch origin main
```

### 3. Check if Rebase is Needed

```bash
# See how many commits main is ahead
git rev-list --count HEAD..origin/main
```

If main is not ahead, inform the user the branch is already up to date.

### 4. Perform Rebase

```bash
git rebase origin/main
```

### 5. Handle Conflicts

If conflicts occur:

1. List the conflicting files:
   ```bash
   git diff --name-only --diff-filter=U
   ```

2. For each conflicting file:
   - Read the file to understand the conflict
   - Resolve the conflict appropriately
   - Stage the resolved file: `git add {file}`

3. Continue the rebase:
   ```bash
   git rebase --continue
   ```

4. If conflicts are too complex, offer to abort:
   ```bash
   git rebase --abort
   ```

### 6. Force Push (if branch was already pushed)

```bash
# Check if branch has upstream
git rev-parse --abbrev-ref @{upstream} 2>/dev/null

# If it does, force push with lease for safety
git push --force-with-lease
```

### 7. Report Result

Tell the user:
- How many commits were rebased
- Whether force push was needed
- Any conflicts that were resolved
