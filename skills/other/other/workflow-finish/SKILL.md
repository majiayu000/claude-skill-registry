---
name: workflow-finish
description: "Cleanup branch after PR is merged. Use when user says /workflow finish or /workflow-finish."
user-invocable: true
allowed-tools:
  - Bash
  - Glob
  - Read
  - Write
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill workflow-finish"
---

# CI E2E Runner Workflow Finish

## Purpose

Cleanup git branches after a PR is merged. Removes local branch, remote branch, and workflow context files.

## Quick Reference

- **Deletes**: Local branch, remote branch, workflow context
- **Requires**: Branch name or current branch
- **Safe**: Verifies PR is merged before deleting

## Usage

```
/workflow-finish                              # Current branch
/workflow-finish feat/add-retry-logic         # Specify branch name
```

## Procedure

### Step 1: Resolve Target Branch

| Input | Resolution |
|-------|------------|
| No argument | Use current branch (`git branch --show-current`) |
| Branch name | Use directly |

### Step 2: Verify PR is Merged

```bash
gh pr list --head <branch-name> --state all --json number,state,mergedAt
```

| State | Action |
|-------|--------|
| `MERGED` | Proceed to cleanup |
| `OPEN` | Warn: "PR not merged. Force finish anyway?" |
| `CLOSED` | Warn: "PR closed without merge. Force finish anyway?" |
| Not found | Warn: "No PR found. Force finish anyway?" |

### Step 3: Switch to Main (if on target branch)

```bash
CURRENT=$(git branch --show-current)
if [ "$CURRENT" = "<target-branch>" ]; then
  git checkout main
  git pull origin main
fi
```

### Step 4: Cleanup

```bash
# Delete remote branch
git push origin --delete <branch-name> 2>/dev/null || echo "Remote branch already deleted"

# Delete local branch
git branch -D <branch-name> 2>/dev/null || echo "Local branch already deleted"

# Remove workflow context directory
rm -rf .claude/workflow/<branch-name>/ 2>/dev/null || true
```

### Step 5: Report

```
Workflow finished for `<branch-name>`

| Item | Status |
|------|--------|
| PR #<number> | Merged |
| Remote branch | Deleted / Already deleted |
| Local branch | Deleted |
| Workflow context | Cleaned |
```

## Safety Rules

1. **Always verify PR is merged** before deleting branches
2. **Never force-finish without user confirmation** if PR is not merged
3. **Switch to main first** if currently on the branch being deleted
4. **Ignore errors** for already-deleted resources (idempotent)

## Examples

### Finish current branch
```
/workflow-finish
```
Uses current branch name.

### Finish by branch name
```
/workflow-finish feat/add-retry-logic-to-e2e-pipeline
```

## Automation

See `skill.yaml` for patterns.
See `sharp-edges.yaml` for common pitfalls.
