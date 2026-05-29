---
name: phase-task-verification
description: Shared branch creation and verification logic for sequential and parallel task execution - handles git operations, HEAD verification, and MODE-specific behavior
---

# Phase Task Verification

## When to Use

Invoked by `sequential-phase-task` and `parallel-phase-task` after task implementation to create and verify git-spice branch.

## Parameters

- **RUN_ID**: 6-char run ID (e.g., "8c8505")
- **TASK_ID**: Phase-task (e.g., "1-1")
- **TASK_NAME**: Short name (e.g., "create-verification-skill")
- **COMMIT_MESSAGE**: Full commit message
- **MODE**: "sequential" or "parallel"

## The Process

**Step 1: Stage and create branch**
```bash
git add .
gs branch create {RUN_ID}-task-{TASK_ID}-{TASK_NAME} -m "{COMMIT_MESSAGE}"
```

**Step 2: Verify based on MODE**

**MODE: sequential** - Verify HEAD points to expected branch:
```bash
CURRENT=$(git rev-parse --abbrev-ref HEAD)
EXPECTED="{RUN_ID}-task-{TASK_ID}-{TASK_NAME}"
[ "$CURRENT" = "$EXPECTED" ] || { echo "ERROR: HEAD=$CURRENT, expected $EXPECTED"; exit 1; }
```

**MODE: parallel** - Detach HEAD (makes branch accessible in parent repo):
```bash
git switch --detach
CURRENT=$(git rev-parse --abbrev-ref HEAD)
[ "$CURRENT" = "HEAD" ] || { echo "ERROR: HEAD not detached ($CURRENT)"; exit 1; }
```

## Rationalization Table

| Rationalization | Why It's Wrong |
|----------------|----------------|
| "Verification is optional" | Silent failures lose work |
| "Skip detach in parallel mode" | Breaks worktree cleanup |
| "Branch create errors are obvious" | Silent failures aren't detected until cleanup fails |
| "Detach can happen later" | Cleanup runs in parent repo - branch must be accessible |
| "HEAD verification adds overhead" | <100ms cost prevents hours of lost work debugging |

## Error Handling

**git add fails:**
- **No changes to stage**: Error is expected - task implementation failed or incomplete
  - Check if task was actually implemented
  - Verify files were modified in expected locations
  - Do NOT continue with branch creation
- **Permission issues**: Git repository permissions corrupted
  - Check file ownership: `ls -la .git`
  - Verify worktree is accessible
  - Escalate to orchestrator

**gs branch create fails:**
- **Duplicate branch name**: Branch already exists
  - Check existing branches: `git branch | grep {RUN_ID}-task-{TASK_ID}`
  - Verify task wasn't already completed
  - May indicate resume scenario - escalate to orchestrator
- **Git-spice errors**: Repository state issues
  - Run `gs repo sync` to fix state
  - Verify git-spice initialized: `gs ls`
  - Check for uncommitted changes blocking operation
- **Invalid branch name**: Name contains invalid characters
  - Verify RUN_ID is 6-char alphanumeric
  - Verify TASK_NAME contains only alphanumeric + hyphens
  - Do NOT sanitize - escalate to orchestrator (indicates data corruption)

**HEAD verification fails (sequential mode):**
- **Expected**: `gs branch create` should checkout new branch automatically
- **Actual**: Still on previous branch or detached HEAD
  - Indicates git-spice behavior change or bug
  - Do NOT continue - task is not properly staged
  - Escalate to orchestrator with exact HEAD state

**HEAD verification fails (parallel mode):**
- **Expected**: `git switch --detach` should detach HEAD
- **Actual**: Still on branch after detach command
  - Indicates git version issue or repository corruption
  - Do NOT continue - cleanup will fail to access branch
  - Escalate to orchestrator with git version: `git --version`
