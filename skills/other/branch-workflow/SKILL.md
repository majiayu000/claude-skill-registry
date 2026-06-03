---
name: branch-workflow
description: Git branch workflow for autonomous work. Apply when implementing features, fixes, or any code changes.
---

# Branch Workflow - Safe Autonomous Coding

All work happens on branches. Main stays clean. Tako reviews before merge.

## Branch Naming

```
feat/TASK-ID-short-description    # New features
fix/TASK-ID-short-description     # Bug fixes
docs/TASK-ID-short-description    # Documentation
research/TASK-ID-description      # Exploration
refactor/TASK-ID-description      # Code improvements
```

**Examples:**
- `feat/TSC-001-plugin-supervisor`
- `fix/MSC-023-dashboard-crash`
- `docs/TORIS-005-case-study`

## Commit Format

```
TASK-ID: Brief description of change

- Detail 1
- Detail 2

Co-Authored-By: Claude <co-author>
```

**Good commits:**
- Atomic (one logical change)
- Buildable (tests pass at each commit)
- Descriptive (explains what, not how)

## Workflow

### Starting Work
```bash
git checkout main
git pull origin main
git checkout -b feat/TASK-ID-description
```

### During Work
```bash
# Commit often
git add -A
git commit -m "TASK-ID: Implement X"

# Push periodically
git push -u origin feat/TASK-ID-description
```

### Finishing Work
```bash
# Ensure tests pass
cargo test  # or npm test, pytest, etc.

# Push final state
git push

# Log completion (megg or BACKLOG.md)
```

## Rules

### NEVER Do
- Push directly to main
- Force push (`git push --force`)
- Merge your own branches
- Delete branches without Tako approval
- Commit secrets or credentials

### ALWAYS Do
- Create branch before changing code
- Run tests before pushing
- Commit with clear messages
- Push branches for review
- Document decisions

## When Blocked

1. Push current work to branch
2. Document blocker in `.megg/blocked.md` or commit message
3. Move to next task
4. Tako will review on return

## Review Workflow

Tako reviews branches by:
```bash
# See all work
git branch -a

# Review specific branch
git log main..feat/BRANCH-NAME
git diff main..feat/BRANCH-NAME

# Merge if good
git checkout main
git merge feat/BRANCH-NAME
```

## Integration with OpenSpec

For OpenSpec changes:
- Branch name matches change ID: `feat/add-plugin-system`
- One branch per OpenSpec change
- Archive OpenSpec change only after merge

## Emergency Fixes

For critical bugs in production:
1. Create `hotfix/description` branch
2. Minimal fix only
3. Tests must pass
4. Document urgency in commit
5. Flag for immediate Tako review
