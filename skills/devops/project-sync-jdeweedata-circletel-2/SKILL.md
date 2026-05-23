---
name: Project Sync Checker
description: Check alignment between local project and git remote. Analyzes uncommitted changes, unpushed commits, unpulled updates, branch status, and divergence to ensure local and remote are synchronized.
version: 1.0.0
dependencies: git
---

# Project Sync Checker

A skill for ensuring local project state is aligned with the git remote repository. Analyzes the full synchronization status including uncommitted changes, staged files, unpushed commits, unpulled commits, branch tracking, and divergence states.

## When This Skill Activates

This skill automatically activates when you:
- Need to check if local and remote are synchronized
- Want to verify project state before starting work
- Debug sync issues between local and remote
- Need to understand divergence between branches
- Check what commits need to be pushed or pulled
- Start a new session and need project context
- Want a full project status overview

**Keywords**: sync status, project sync, git status, local vs remote, check alignment, push status, pull status, unpushed commits, uncommitted changes, divergence, branch status, remote status, project context

## Core Concepts

### Sync States

| State | Meaning | Action Required |
|-------|---------|-----------------|
| **Fully Synced** | Local matches remote exactly | None - ready to work |
| **Uncommitted Changes** | Modified files not committed | Commit or stash |
| **Unpushed Commits** | Local ahead of remote | Push to sync |
| **Unpulled Commits** | Remote ahead of local | Pull to sync |
| **Diverged** | Both local and remote have new commits | Pull, merge/rebase, push |
| **Untracked Branch** | Local branch has no upstream | Set upstream or push |

### Status Indicators

```
[SYNCED]     - Fully synchronized
[AHEAD]      - Local has unpushed commits
[BEHIND]     - Remote has unpulled commits
[DIVERGED]   - Both have new commits
[DIRTY]      - Uncommitted local changes
[UNTRACKED]  - New files not in git
[CONFLICT]   - Merge conflicts present
```

## Quick Check Methods

### Method 1: Using PowerShell Script (Recommended)

```powershell
# Full sync check
powershell -File .claude/skills/project-sync/check-sync.ps1

# Check specific branch
powershell -File .claude/skills/project-sync/check-sync.ps1 -Branch "feature/my-branch"

# Include remote comparison (fetches latest)
powershell -File .claude/skills/project-sync/check-sync.ps1 -FetchRemote

# Quick status only (no details)
powershell -File .claude/skills/project-sync/check-sync.ps1 -Quick
```

### Method 2: Git Commands (Manual)

```bash
# Comprehensive status check
git fetch origin --prune

# Branch status
git status -sb

# Check ahead/behind
git rev-list --left-right --count origin/main...HEAD

# View uncommitted changes
git diff --stat

# View staged changes
git diff --cached --stat

# View unpushed commits
git log origin/main..HEAD --oneline

# View unpulled commits
git log HEAD..origin/main --oneline

# Check for divergence
git log --oneline --left-right origin/main...HEAD
```

### Method 3: Comprehensive Analysis (Claude Code)

When you need detailed sync analysis, provide these outputs:

```
1. Current branch: git branch --show-current
2. Remote tracking: git for-each-ref --format='%(upstream:short)' refs/heads/$(git branch --show-current)
3. Status: git status --porcelain
4. Ahead/behind: git rev-list --left-right --count @{u}...HEAD
5. Unpushed: git log @{u}..HEAD --oneline
6. Unpulled: git log HEAD..@{u} --oneline
7. Last remote sync: git show -s --format=%ci @{u}
8. Stash list: git stash list
```

## Sync Status Report Template

When reporting sync status, use this format:

```markdown
## Project Sync Status Report

**Project**: [project name]
**Branch**: [current branch] → [remote/branch]
**Status**: [SYNCED/AHEAD/BEHIND/DIVERGED/DIRTY]
**Generated**: [timestamp]

### Local State
- **Uncommitted Changes**: [count] files
- **Staged for Commit**: [count] files
- **Untracked Files**: [count] files
- **Stashed Changes**: [count] stashes

### Remote Comparison
- **Commits Ahead**: [count] (need to push)
- **Commits Behind**: [count] (need to pull)
- **Last Remote Sync**: [date/time]
- **Remote Last Commit**: [short hash] - [message]

### Recommendations
1. [Action 1]
2. [Action 2]
```

## Common Sync Scenarios

### Scenario 1: Start of Work Session

Before starting work, always check sync status:

```powershell
# Fetch and show full status
powershell -File .claude/skills/project-sync/check-sync.ps1 -FetchRemote
```

**Expected Actions**:
- If BEHIND: `git pull origin main`
- If AHEAD: Consider pushing before starting new work
- If DIRTY: Commit, stash, or discard changes

### Scenario 2: Before Creating a PR

Ensure branch is ready for PR:

```bash
# Switch to your feature branch
git checkout feature/my-feature

# Fetch latest
git fetch origin

# Check if main has new commits
git log HEAD..origin/main --oneline

# If behind main, rebase
git rebase origin/main

# Push with force if rebased
git push --force-with-lease
```

### Scenario 3: Resolving Divergence

When local and remote have diverged:

```bash
# Option A: Rebase (cleaner history)
git fetch origin
git rebase origin/main
# Resolve conflicts if any
git push --force-with-lease

# Option B: Merge (preserves history)
git fetch origin
git merge origin/main
# Resolve conflicts if any
git push
```

### Scenario 4: Multiple Developers / CI Conflicts

When commits appear on remote during your work:

```bash
# Stash current work
git stash

# Pull latest
git pull origin main

# Reapply your work
git stash pop

# Handle any conflicts, then commit
```

## Detailed Analysis Functions

### Check Uncommitted Changes

```bash
# Summary
git status --short

# Detailed diff
git diff

# Only show file names
git diff --name-only

# Show stats
git diff --stat
```

### Check Staged Changes

```bash
# What's ready to commit
git diff --cached

# File list only
git diff --cached --name-only
```

### Check Unpushed Commits

```bash
# List unpushed commits
git log @{u}..HEAD --oneline

# Show full details
git log @{u}..HEAD

# Count only
git rev-list @{u}..HEAD --count
```

### Check Unpulled Commits

```bash
# Fetch first
git fetch origin

# List unpulled commits
git log HEAD..@{u} --oneline

# Show what files will change
git diff --stat HEAD..@{u}
```

### Check Branch Tracking

```bash
# All branches with tracking info
git branch -vv

# Current branch upstream
git rev-parse --abbrev-ref @{u}

# Is tracking configured?
git config branch.$(git branch --show-current).remote
```

## Alignment Remediation Actions

### Action: Sync with Remote (Pull)

```bash
# Standard pull
git pull origin main

# Pull with rebase (preferred)
git pull --rebase origin main

# If conflicts occur
git status                    # See conflicted files
# Edit files to resolve
git add <resolved-files>
git rebase --continue        # If rebasing
git commit                   # If merging
```

### Action: Push Local Commits

```bash
# Standard push
git push origin main

# Set upstream and push
git push -u origin feature/my-branch

# Force push (after rebase) - use carefully!
git push --force-with-lease origin main
```

### Action: Stash Changes Temporarily

```bash
# Stash with message
git stash push -m "WIP: description"

# List stashes
git stash list

# Apply latest stash
git stash pop

# Apply specific stash
git stash apply stash@{2}
```

### Action: Discard Local Changes

```bash
# Discard unstaged changes (CAREFUL!)
git checkout -- .

# Reset to remote state (CAREFUL!)
git fetch origin
git reset --hard origin/main

# Remove untracked files (CAREFUL!)
git clean -fd
```

## Integration with CircleTel Workflow

### Pre-Deploy Check

Before deploying to staging or production:

```powershell
# Full sync check
powershell -File .claude/skills/project-sync/check-sync.ps1 -FetchRemote

# Expected output:
# - Branch: main
# - Status: SYNCED
# - Uncommitted: 0
# - Ahead: 0
# - Behind: 0
```

### Feature Branch Workflow

```bash
# 1. Start feature from synced main
git checkout main
powershell -File .claude/skills/project-sync/check-sync.ps1 -FetchRemote
git checkout -b feature/new-feature

# 2. Work on feature...

# 3. Before PR - sync with main
git fetch origin
git rebase origin/main

# 4. Push feature
git push -u origin feature/new-feature
```

### Staging Branch Pattern

```bash
# Push to staging for testing
git push origin feature/my-feature:staging

# Check staging status
git fetch origin
git log staging..origin/staging --oneline
```

## Environment Variables

No environment variables required. Uses local git configuration.

## Related Files

| File | Purpose |
|------|---------|
| `.git/config` | Local repository configuration |
| `.git/refs/remotes/origin/` | Remote tracking references |
| `.gitignore` | Ignored file patterns |
| `.claude/skills/project-sync/check-sync.ps1` | Quick check script |

## Troubleshooting

### Issue: "No upstream branch"

```bash
# Set upstream
git branch --set-upstream-to=origin/main main

# Or push with -u
git push -u origin main
```

### Issue: "Diverged branches"

```bash
# See divergence
git log --oneline --left-right origin/main...HEAD

# Rebase to align
git rebase origin/main
git push --force-with-lease
```

### Issue: "Cannot pull - uncommitted changes"

```bash
# Option 1: Stash
git stash
git pull
git stash pop

# Option 2: Commit first
git add .
git commit -m "WIP"
git pull --rebase
```

### Issue: "Remote rejected (non-fast-forward)"

```bash
# Someone pushed while you were working
git fetch origin
git rebase origin/main
git push
```

## Best Practices

1. **Always fetch before checking status** - Local tracking info may be stale
2. **Check sync at session start** - Avoid merge conflicts later
3. **Commit frequently** - Smaller commits are easier to sync
4. **Use feature branches** - Keep main clean and synced
5. **Pull before push** - Avoid non-fast-forward rejections
6. **Prefer rebase over merge** - Cleaner history for feature branches
7. **Use --force-with-lease** - Safer than --force when needed
8. **Stash before switching branches** - Don't carry uncommitted changes

## Quick Reference Card

```
┌─────────────────────────────────────────────────────────┐
│              PROJECT SYNC QUICK REFERENCE               │
├─────────────────────────────────────────────────────────┤
│ CHECK STATUS                                            │
│   Full check: check-sync.ps1 -FetchRemote              │
│   Quick:      git status -sb                           │
│   Ahead:      git log @{u}..HEAD --oneline             │
│   Behind:     git log HEAD..@{u} --oneline             │
├─────────────────────────────────────────────────────────┤
│ FIX SYNC ISSUES                                         │
│   Behind:     git pull --rebase origin main            │
│   Ahead:      git push origin main                     │
│   Diverged:   git pull --rebase && git push            │
│   Dirty:      git stash or git commit                  │
├─────────────────────────────────────────────────────────┤
│ DANGER ZONE (use carefully!)                            │
│   Reset to remote:  git reset --hard origin/main       │
│   Force push:       git push --force-with-lease        │
│   Discard changes:  git checkout -- .                  │
└─────────────────────────────────────────────────────────┘
```

---

**Version**: 1.0.0
**Last Updated**: 2025-01-08
**Maintained By**: CircleTel Development Team
**Reference**: https://git-scm.com/docs
