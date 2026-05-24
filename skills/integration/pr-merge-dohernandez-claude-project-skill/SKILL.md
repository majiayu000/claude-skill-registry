---
name: pr-merge
description: Merge GitHub pull requests with strict CI validation. Never bypasses failed checks. Use when merging PRs or when user says /pr-merge.
user-invocable: true
allowed-tools: [Bash, Read]
hooks:
  Stop:
    - type: command
      command: "task claude:validate-skill -- --skill pr-merge"
---

# PR Merge

## Purpose
Merge GitHub pull requests with strict CI validation and merge state checking.
Enforces the rule: **NEVER bypass failed CI checks**. Only offers bypass for missing reviews when all checks pass.

## Quick Reference
- Merges: GitHub PR via `gh pr merge --squash`
- Requires: GitHub CLI installed and authenticated, PR exists for branch

## Critical Rule

**NEVER offer to bypass failed CI checks.**

Failed checks mean broken code. The only acceptable bypass is for missing review when ALL checks pass.

```
All checks pass + CLEAN        -> Auto-merge
All checks pass + BEHIND       -> Update branch, re-check
All checks pass + BLOCKED      -> Ask: "Bypass review?"
Any check FAILED               -> STOP. Investigate failure.
Conflicts (DIRTY)              -> Cannot auto-merge
Checks still running           -> Wait and re-check
```

## Merge Flow

### Step 1: Get PR

```bash
# If PR number provided, use it
gh pr view 123 --json state,mergeable,mergeStateStatus,statusCheckRollup

# Otherwise, find PR for current branch
gh pr list --head $(git branch --show-current) --json number,state
```

### Step 2: Check PR State

| State | Action |
|-------|--------|
| `MERGED` | "PR already merged" - done |
| `CLOSED` | "PR is closed" - stop |
| `OPEN` | Continue to CI check |

### Step 3: Check CI Status

For each check in `statusCheckRollup`:

| Status | Action |
|--------|--------|
| `IN_PROGRESS` | Wait 30s, retry (max 5 retries) |
| `FAILURE` | **STOP. Display failed check name. Investigate.** |
| `SUCCESS` | Continue |

**CRITICAL**: On FAILURE, do NOT offer to bypass. Say:
> "CI check '<name>' failed. Please investigate before merging."

### Step 4: Check Merge State

| mergeStateStatus | Action |
|------------------|--------|
| `CLEAN` | Proceed to merge |
| `BEHIND` | Update branch, re-check CI |
| `BLOCKED` | If all checks pass -> ask "Bypass review?" |
| `DIRTY` | "Conflicts detected. Resolve before merging." |

### Step 5: Execute Merge

```bash
gh pr merge <number> --squash
```

## Update Behind Branch

When `mergeStateStatus` is `BEHIND`:

```bash
git fetch origin main
git merge origin/main --no-edit
git push
# Then re-check from Step 3
```

## Automation
See `skill.yaml` for the full procedure and patterns.
See `sharp-edges.yaml` for common failure modes.
