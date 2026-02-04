---
name: finish-task
description: Finish current task. Use when user says "dokonči task", "task hotový", "mergni do main", or runs /finish-task.
allowed-tools: Bash, Read, AskUserQuestion
---

# Finish Task

Complete the current task. Behavior depends on detected mode (MAIN, FEATURE_BRANCH, WORKTREE).

## Usage

```
/finish-task              # Complete current task (auto-detects mode)
/finish-task --no-test    # Complete without running tests
```

## Current State

Current branch:
!git branch --show-current

Uncommitted changes:
!git status --porcelain

Is worktree:
!test -f "$(git rev-parse --show-toplevel)/.git" && echo "YES - WORKTREE" || echo "NO - main repo"

## Process

### Step 1: Detect Mode

```bash
BRANCH=$(git branch --show-current)
IS_WORKTREE=false
if [[ -f "$(git rev-parse --show-toplevel)/.git" ]]; then
  IS_WORKTREE=true
fi

if [[ "$IS_WORKTREE" == "true" ]]; then
  MODE="WORKTREE"
elif [[ "$BRANCH" != "main" && "$BRANCH" != "master" ]]; then
  MODE="FEATURE_BRANCH"
else
  MODE="MAIN"
fi
```

### Step 2: Detect Current Task

**MAIN mode:** Find task from in_progress status in task files
**FEATURE_BRANCH/WORKTREE:** Extract from branch name `phase-XX/task-YY-description`

### Step 3: Check Prerequisites

Before finishing:
1. No uncommitted changes (or use `--force` to override)
2. Task file exists and is readable

### Step 4: Run Tests (optional)

Unless `--no-test` is specified:

```bash
dotnet test EShopDemo.sln --filter "Category!=Integration"
```

If tests fail, the script stops and reports the error.

### Step 5: Check Code Formatting

```bash
dotnet csharpier check .
```

If formatting check fails, suggest running `dotnet csharpier format .` to fix.

### Step 6: Mode-Specific Actions

#### MAIN Mode
Just update task status - no merge needed:
```bash
# Update task file: 🔵 in_progress → ✅ completed
# Commit the status change
git add <task-file>
git commit -m "[XX-YY] docs: mark task as completed"
```

#### FEATURE_BRANCH Mode
Squash merge all commits to main:
```bash
# Switch to main
git checkout main

# Squash merge (combines all branch commits into one)
git merge --squash <feature-branch>

# Commit with task prefix
git commit -m "[XX-YY] feat: <summary of all changes>"

# Delete feature branch
git branch -d <feature-branch>
```

#### WORKTREE Mode
Squash merge to main in the main repository:
```bash
# Get main repo path
MAIN_REPO=$(cat "$(git rev-parse --show-toplevel)/.git" | sed 's/gitdir: //' | xargs dirname | xargs dirname)

# In main repo: squash merge
cd "$MAIN_REPO"
git merge --squash <worktree-branch>
git commit -m "[XX-YY] feat: <summary of all changes>"

# Offer to remove worktree
# Ask user: "Remove worktree directory?"
```

## Arguments

- `--no-test` - Skip running tests
- `--force` - Continue even with uncommitted changes

## Output

On success (MAIN mode):
```
Finishing task: task-02 - Shared Kernel
Mode: MAIN

Running unit tests... ✓
Checking code formatting... ✓
Task status updated to ✅ completed

Task task-02 completed successfully!
```

On success (FEATURE_BRANCH mode):
```
Finishing task: task-02 - Shared Kernel
Mode: FEATURE_BRANCH
Branch: phase-01/task-02-shared-kernel

Running unit tests... ✓
Checking code formatting... ✓
Squash merging to main...
Committed: [01-02] feat: implement shared kernel with Entity and ValueObject base classes
Deleted branch: phase-01/task-02-shared-kernel

Task task-02 completed successfully!
```

On success (WORKTREE mode):
```
Finishing task: task-02 - Shared Kernel
Mode: WORKTREE
Branch: phase-01/task-02-shared-kernel

Running unit tests... ✓
Checking code formatting... ✓
Squash merging to main (in main repo)...
Committed: [01-02] feat: implement shared kernel with Entity and ValueObject base classes

Remove worktree directory? [y/N]
```

On failure:
```
Error: Unit tests failed
Fix the failing tests before completing the task.
```

## Safety Rules

1. NEVER merge with uncommitted changes (unless --force)
2. ALWAYS run tests before marking complete (unless --no-test)
3. ALWAYS check formatting before merge
4. For squash merge, generate meaningful commit message summarizing all changes
5. ALWAYS ask before removing worktree directory

## Integration

This skill is part of the task lifecycle:
1. `/task-status` - see what's available
2. `/start-task XX` - begin working
3. `/commit` - commit changes
4. `/finish-task` - complete (behavior depends on mode)
