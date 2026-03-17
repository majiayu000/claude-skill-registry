---
name: git-automator
description: Automates git workflow - sync, branch management, conflict resolution, smart commits, and PRs. Integrates with feature development cycle.
globs: ["*"]
---

# Git Automator (Feature Development Integration)

Automates the entire git workflow integrated with the feature development cycle.

## Prerequisites
- `git` and `gh` (GitHub CLI) installed

## Integration with Feature Cycle

### Phase 4: BRANCH
```bash
# Check current branch
git branch --show-current

# If on main/master, create feature branch
git checkout main
git pull origin main
git checkout -b feature/XXX-name
```

### Phase 5: IMPLEMENT (Commit Workflow)

**For each completed task:**

```bash
# 1. Check status
git status

# 2. Stage changes
git add [specific files for this task]

# 3. Commit with feature prefix
git commit -m "FEAT-XXX: Complete Task N - description"

# 4. Every 30 min or 3 tasks: push
git push origin feature/XXX-name
```

### Phase 6: PR Creation

```bash
# Push final changes
git push -u origin HEAD

# Create PR
gh pr create \
  --title "FEAT-XXX: Feature Name" \
  --body "## Summary..." \
  --base main
```

## Conflict Resolution Protocol

**IF CONFLICTS OCCUR:**

1. **Identify conflicts:**
   ```bash
   git status
   ```

2. **Inform user:**
   "Conflicts detected in: [list files]"

3. **Offer assistance:**
   "Do you want me to read these files and help you choose which version to keep?"

4. **WAIT for user instruction** on each file

5. **Resolve and continue:**
   ```bash
   git add [resolved_file]
   git rebase --continue
   ```

## Smart Commit Messages

### Format
```
FEAT-XXX: [Action] [Component] - [Brief description]
```

### Examples
```
FEAT-001: Add User model with validation
FEAT-001: Create auth service with JWT support
FEAT-001: Add login endpoint and tests
FEAT-002: Fix dashboard layout on mobile
```

### Rules
- Keep under 72 characters
- Start with feature ID
- Use present tense ("Add" not "Added")
- NO emojis unless user requests
- NO automatic co-author tags

## Quick Reference

```bash
# Start feature
git checkout -b feature/XXX-name

# During implementation
git add [files]
git commit -m "FEAT-XXX: description"
git push origin feature/XXX-name

# Create PR
gh pr create --fill --base main

# After merge
git checkout main
git pull
git branch -d feature/XXX-name
```
