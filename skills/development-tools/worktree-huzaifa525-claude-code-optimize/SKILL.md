---
name: worktree
description: Use when the user wants to work in an isolated branch, start a safe development environment, or avoid polluting the main branch.
disable-model-invocation: true
allowed-tools: Bash, Read, Grep, Glob
argument-hint: "[branch-name or feature description]"
---

Create an isolated git worktree for safe development on: **$ARGUMENTS**

## Iron Law

> **All new feature work happens in a worktree. The main branch stays clean.**

If you think "this change is small enough to do on main" — you are wrong. Worktrees cost 5 seconds. Debugging a polluted main branch costs hours.

## Steps

### 1. Verify Clean Baseline

Before creating the worktree:

```bash
# Ensure we're in a git repo
git rev-parse --is-inside-work-tree

# Check for uncommitted changes
git status --porcelain
```

If there are uncommitted changes, ask the user whether to stash or commit them first. Do NOT proceed with dirty state.

### 2. Create the Worktree

Sanitize the branch name from the user's description:
- Lowercase everything
- Replace spaces and special characters with hyphens
- Remove consecutive hyphens
- Example: "User Notifications!" → `feature/user-notifications`

```bash
# Create worktree on a new branch
git worktree add "../$(basename $PWD)-feature-$BRANCH_NAME" -b "feature/$BRANCH_NAME"
```

### 3. Verify Test Baseline

Run the project's test suite in the new worktree BEFORE making any changes:

```bash
cd "../$(basename $PWD)-$BRANCH_NAME"
# Run tests (detect test command from package.json, Makefile, etc.)
```

If tests fail BEFORE any changes, the baseline is broken. Stop and report.

### 4. Work in the Worktree

- Make all changes in the worktree directory
- Commit frequently with descriptive messages
- Run tests after each meaningful change

### 5. Finish

When work is complete, present options:

| Option | Command | When |
|--------|---------|------|
| **Merge** | `git checkout main && git merge $BRANCH_NAME` | Feature is complete and tested |
| **PR** | `gh pr create` from the worktree branch | Needs review before merge |
| **Keep** | Leave worktree as-is | Work in progress, will continue later |
| **Discard** | `git worktree remove ../worktree-dir` | Experiment failed, throw it away |

## Red Flags

- "Let me just make this quick fix on main" — NO. Use a worktree.
- "The tests were already failing" — Then fix the baseline FIRST.
- "I'll clean up the branch later" — You won't. Clean it now.

<!-- Skill by Huzefa Nalkheda Wala | github.com/huzaifa525 | claude-code-optimizer -->
