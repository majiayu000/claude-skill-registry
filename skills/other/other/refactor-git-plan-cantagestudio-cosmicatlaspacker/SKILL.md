---
name: refactor-git-plan
description: "[Code Quality] Plans Git commit strategy for refactoring: branch naming, commit granularity, commit messages, and safe merge approach. Use to structure version control for reversible, reviewable changes."
---

# Refactor: Git Plan

Structure version control for safe, reviewable refactoring.

## Branch Strategy

### Naming Convention
```
refactor/<scope>-<action>
Examples: refactor/auth-extract-service
```

## Commit Granularity

### One Commit Per
- Single rename across files
- One method extraction
- One file move
- One pattern application

### Commit Message Format
```
refactor(<scope>): <action>

<what changed and why>

Risk: low|medium|high
Tests: passing|added|updated
```

## Safety Practices

### Before Starting
- Ensure clean state (git status)
- Create branch
- Verify tests pass

### During Refactoring
- Commit frequently
- Run tests after each commit

### If Something Breaks
- git reset --soft HEAD~1 (undo, keep changes)
- git checkout -- . (discard changes)
- git revert <commit-hash> (revert specific)