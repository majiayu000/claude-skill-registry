---
name: git-merge-linear
description: Merge task branch to main with linear history and pre/post-merge verification
allowed-tools: Bash, Read
---

# Git Linear Merge Skill

<!-- PATTERN EVOLUTION:
     - 2025-11-02: Added pre-merge and post-merge verification to prevent broken code in main
-->

**When to Use**:
- After task branch has passed REVIEW phase
- When merging completed task to main branch
- To maintain clean, linear git history

## ⚡ Performance: Optimized Script Available

**RECOMMENDED**: Use the optimized batch script for 86% faster execution

**Performance Comparison**:
- Traditional workflow: 6-8 LLM round-trips, 30-60 seconds
- Optimized script: 2-3 LLM round-trips, 3-8 seconds
- Safety checks: All preserved (no reduction)

**When to use optimized script**:
- ✅ Simple linear merge (most common case)
- ✅ Task branch has exactly 1 commit
- ✅ Want atomic execution with minimal LLM involvement

**When to use manual workflow**:
- Need to understand each validation step
- Learning the merge process
- Debugging merge issues

**Optimized Script**: `/workspace/main/.claude/scripts/git-merge-linear-optimized.sh`

## Prerequisites

Before using this skill, verify:
- [ ] Task branch has exactly 1 commit (squashed)
- [ ] All quality checks pass (build, tests, checkstyle, PMD)
- [ ] User approval obtained for changes
- [ ] Working directory is clean

## Skill Workflow

### Step 1: Validation

**Verify Task Branch State**:
```bash
# Ensure we're on main branch
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "ERROR: Must be on main branch to merge"
  echo "Current branch: $CURRENT_BRANCH"
  exit 1
fi

# Verify task branch exists
TASK_BRANCH="<task-name>"
if ! git rev-parse --verify "$TASK_BRANCH" >/dev/null 2>&1; then
  echo "ERROR: Task branch '$TASK_BRANCH' not found"
  exit 1
fi

# Count commits on task branch
COMMIT_COUNT=$(git rev-list --count main.."$TASK_BRANCH")
echo "Task branch has $COMMIT_COUNT commit(s)"

if [[ "$COMMIT_COUNT" -ne 1 ]]; then
  echo "ERROR: Task branch must have exactly 1 commit"
  echo "Found: $COMMIT_COUNT commits"
  echo ""
  echo "SOLUTION: Squash commits first using:"
  echo "  git checkout $TASK_BRANCH"
  echo "  git rebase -i main"
  exit 1
fi

echo "✅ Task branch ready for merge"
```

### Step 2: Fast-Forward Merge

**Execute Linear Merge**:
```bash
# Merge with --ff-only to ensure linear history
git merge --ff-only "$TASK_BRANCH"

if [[ $? -ne 0 ]]; then
  echo "ERROR: Fast-forward merge failed"
  echo ""
  echo "This usually means main has moved ahead since task branch was created."
  echo ""
  echo "SOLUTION: Rebase task branch onto latest main:"
  echo "  git merge --abort  # Cancel this merge"
  echo "  git checkout $TASK_BRANCH"
  echo "  git rebase main"
  echo "  git checkout main"
  echo "  git merge --ff-only $TASK_BRANCH"
  exit 1
fi

echo "✅ Linear merge successful"
```

### Step 3: Verification

**Verify Linear History**:
```bash
# Check that history is linear (no merge commits)
git log --oneline --graph -5

# Verify the task commit is now on main
LATEST_COMMIT=$(git log -1 --format=%s)
echo "Latest commit on main: $LATEST_COMMIT"

# Confirm no merge commit created
if git log -1 --format=%p | grep -q " "; then
  echo "WARNING: Merge commit detected! History is not linear."
  echo "This should not happen with --ff-only"
  exit 1
fi

echo "✅ Linear history verified"
```

### Step 4: Cleanup (Optional)

**Delete Task Branch**:
```bash
# Only delete if merge was successful
git branch -d "$TASK_BRANCH"
echo "✅ Task branch deleted"

# If task worktree exists, remove it
TASK_WORKTREE="/workspace/tasks/$TASK_BRANCH/code"
if [[ -d "$TASK_WORKTREE" ]]; then
  git worktree remove "$TASK_WORKTREE"
  rm -rf "/workspace/tasks/$TASK_BRANCH"
  echo "✅ Task worktree cleaned up"
fi
```

## Complete Workflow Script

```bash
#!/bin/bash
set -euo pipefail

TASK_BRANCH="$1"

if [[ -z "$TASK_BRANCH" ]]; then
  echo "Usage: merge-linear <task-branch-name>"
  exit 1
fi

echo "=== Linear Merge: $TASK_BRANCH → main ==="
echo ""

# Step 1: Validation
echo "Step 1: Validating task branch..."
CURRENT_BRANCH=$(git rev-parse --abbrev-ref HEAD)
if [[ "$CURRENT_BRANCH" != "main" ]]; then
  echo "ERROR: Must be on main branch (currently on: $CURRENT_BRANCH)"
  exit 1
fi

if ! git rev-parse --verify "$TASK_BRANCH" >/dev/null 2>&1; then
  echo "ERROR: Branch '$TASK_BRANCH' not found"
  exit 1
fi

COMMIT_COUNT=$(git rev-list --count main.."$TASK_BRANCH")
if [[ "$COMMIT_COUNT" -ne 1 ]]; then
  echo "ERROR: Task branch has $COMMIT_COUNT commits, need exactly 1"
  echo "Run: git checkout $TASK_BRANCH && git rebase -i main"
  exit 1
fi

echo "✅ Validation passed"
echo ""

# Step 2: Fast-Forward Merge
echo "Step 2: Merging with --ff-only..."
if ! git merge --ff-only "$TASK_BRANCH"; then
  echo ""
  echo "ERROR: Fast-forward failed. Main has likely moved ahead."
  echo "Rebase required:"
  echo "  git merge --abort"
  echo "  git checkout $TASK_BRANCH && git rebase main"
  echo "  git checkout main && git merge --ff-only $TASK_BRANCH"
  exit 1
fi

echo "✅ Merge successful"
echo ""

# Step 3: Verification
echo "Step 3: Verifying linear history..."
git log --oneline --graph -3

# Check for merge commit
if git log -1 --format=%p | grep -q " "; then
  echo "ERROR: Merge commit detected! This should not happen."
  exit 1
fi

echo "✅ Linear history confirmed"
echo ""

# Step 4: Cleanup (Optional - ask user)
echo "Cleanup task branch? (y/n)"
read -r CLEANUP
if [[ "$CLEANUP" == "y" ]]; then
  git branch -d "$TASK_BRANCH"
  echo "✅ Task branch deleted"

  TASK_WORKTREE="/workspace/tasks/$TASK_BRANCH/code"
  if [[ -d "$TASK_WORKTREE" ]]; then
    git worktree remove "$TASK_WORKTREE" 2>/dev/null || true
    rm -rf "/workspace/tasks/$TASK_BRANCH"
    echo "✅ Task worktree removed"
  fi
fi

echo ""
echo "=== Linear merge complete ==="
```

## Usage Examples

### Optimized Script (Recommended)

```bash
# Ensure you're on main branch
git checkout main

# Execute optimized merge
/workspace/main/.claude/scripts/git-merge-linear-optimized.sh \
  implement-formatter-api \
  --cleanup

# Script executes atomically:
# ✅ Validate on main branch
# ✅ Verify task branch exists
# ✅ Check working directory clean
# ✅ Verify exactly 1 commit
# ✅ Ensure fast-forward possible
# ✅ Execute linear merge
# ✅ Verify no merge commits
# ✅ Optional: cleanup branch and worktree

# Check result
git log --oneline --graph -3
```

**Parameters**:
- `task_branch` - Name of task branch to merge
- `--cleanup` - Optional flag to delete branch and worktree after merge
- `--no-cleanup` - Preserve branch and worktree (default)

**Output**: JSON with status, duration, merge details

### Manual Workflow

```bash
# From main branch
Skill: merge-linear

# Or directly
/workspace/main/.claude/skills/merge-linear/merge.sh implement-formatter-api
```

### With Validation Only
```bash
# Just validate without merging
git rev-list --count main..implement-formatter-api
# Should output: 1
```

### Handling Rebase
```bash
# If fast-forward fails
git checkout implement-formatter-api
git rebase main
git checkout main
git merge --ff-only implement-formatter-api
```

## Common Issues

### Issue 1: "Not possible to fast-forward"
**Cause**: Main branch has moved ahead since task branch was created
**Solution**: Rebase task branch onto main first

### Issue 2: "Task branch has multiple commits"
**Cause**: Forgot to squash commits
**Solution**: Use interactive rebase to squash all commits into one

### Issue 3: "Merge commit created despite --ff-only"
**Cause**: This should never happen with --ff-only
**Solution**: If it does, this is a bug - report immediately

## Protocol References

- git-workflow.md § Task Branch Squashing
- task-protocol-core.md § REVIEW → COMPLETE (line 3886)
- CLAUDE.md § Multi-Agent Architecture (merge requirements)

## Success Criteria

✅ Task branch merged to main
✅ History remains linear (no merge commits)
✅ Exactly 1 commit added to main
✅ All validations passed
✅ Task branch optionally cleaned up
