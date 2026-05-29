---
name: troubleshooting-execute
description: Use when execute command encounters errors - diagnostic guide for phase failures, parallel agent failures, merge conflicts, worktree issues, and recovery strategies
---

# Troubleshooting Execute Command

## Overview

**Reference guide for diagnosing and recovering from execute command failures.**

This skill provides recovery strategies for common execute command errors. Use it when execution fails or produces unexpected results.

## When to Use

Use this skill when:
- Phase execution fails (sequential or parallel)
- Parallel agent fails or doesn't complete
- Merge conflicts occur during stacking
- Worktree creation fails
- Main worktree not found
- Need to resume execution after fixing an issue

**This is a reference skill** - consult when errors occur, not part of normal execution flow.

## Error Categories

### 1. Sequential Phase Execution Failure

**Symptoms:**
- Task agent fails mid-execution
- Quality checks fail (test, lint, build)
- Branch not created after task completes

**Error message format:**
```markdown
❌ Phase {id} Execution Failed

**Task**: {task-id}
**Error**: {error-message}
```

**Resolution steps:**

1. **Review the error output** - Understand what failed (test? build? implementation?)

2. **Check current state:**
   ```bash
   cd .worktrees/{runid}-main
   git status
   git log --oneline -5
   ```

3. **Fix manually if needed:**
   ```bash
   # Current branch already has completed work from previous tasks
   # Fix the issue in the working directory

   # Run quality checks
   bash <<'EOF'
   npm test
   if [ $? -ne 0 ]; then
     echo "❌ Tests failed"
     exit 1
   fi

   npm run lint
   if [ $? -ne 0 ]; then
     echo "❌ Lint failed"
     exit 1
   fi

   npm run build
   if [ $? -ne 0 ]; then
     echo "❌ Build failed"
     exit 1
   fi
   EOF

   # Create branch if task completed but branch wasn't created
   gs branch create {runid}-task-{phase}-{task}-{name} -m "[Task {phase}.{task}] {description}"
   ```

4. **Resume execution:**
   - If fixed manually: Continue to next task
   - If need fresh attempt: Reset branch and re-run task
   - If plan was wrong: Update plan and re-execute from this phase

### 2. Parallel Phase - Agent Failure

**Symptoms:**
- One or more parallel agents fail
- Some task branches created, others missing
- Error during concurrent execution

**Error message format:**
```markdown
❌ Parallel Phase {id} - Agent Failure

**Failed Task**: {task-id}
**Branch**: {task-branch}
**Error**: {error-message}

**Successful Tasks**: {list}
```

**Resolution options:**

#### Option A: Fix in Existing Branch

Use when fix is small and task mostly completed:

```bash
# Navigate to task's worktree
cd .worktrees/{runid}-task-{phase}-{task}

# Debug and fix issue
# Edit files, fix code

# Run quality checks
bash <<'EOF'
npm test
if [ $? -ne 0 ]; then
  echo "❌ Tests failed"
  exit 1
fi

npm run lint
if [ $? -ne 0 ]; then
  echo "❌ Lint failed"
  exit 1
fi

npm run build
if [ $? -ne 0 ]; then
  echo "❌ Build failed"
  exit 1
fi
EOF

# Commit fix on existing branch
git add --all
git commit -m "[Task {phase}.{task}] Fix: {description}"

# Return to main repo
cd "$REPO_ROOT"

# Proceed with stacking (failed branch now exists)
```

#### Option B: Create Stacked Fix Branch

Use when fix is significant or logically separate:

```bash
# Navigate to task's worktree
cd .worktrees/{runid}-task-{phase}-{task}

# Ensure original work is committed
git status  # Should be clean

# Create stacked fix branch
gs branch create {runid}-task-{phase}-{task}-fix-{issue} -m "[Task {phase}.{task}] Fix: {issue}"

# Implement fix
# Edit files

# Commit fix
git add --all
git commit -m "[Task {phase}.{task}] Fix: {description}"

# Return to main repo
cd "$REPO_ROOT"
```

#### Option C: Restart Failed Agent

Use when task implementation is fundamentally wrong:

```bash
# Navigate to main repo
cd "$REPO_ROOT"

# Remove task worktree
git worktree remove .worktrees/{runid}-task-{phase}-{task}

# Delete failed branch if it exists
git branch -D {runid}-task-{phase}-{task}-{name}

# Recreate worktree from base
BASE_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
git worktree add .worktrees/{runid}-task-{phase}-{task} --detach "$BASE_BRANCH"

# Install dependencies
cd .worktrees/{runid}-task-{phase}-{task}
{install-command}
{postinstall-command}

# Spawn fresh agent for this task only
# [Use Task tool with task prompt]
```

#### Option D: Continue Without Failed Task

Use when task is non-critical or can be addressed later:

1. Stack successful task branches
2. Mark failed task as follow-up work
3. Continue to next phase
4. Address failed task in separate branch later

### 3. Merge Conflicts During Stacking

**Symptoms:**
- Stacking parallel branches causes conflicts
- `gs upstack onto` fails with merge conflict
- Git reports conflicting changes in same files

**Error message format:**
```markdown
❌ Merge Conflict - Tasks Modified Same Files

**Conflict**: {file-path}
**Branches**: {branch-1}, {branch-2}

This should not happen if task independence was verified correctly.
```

**Root cause:** Tasks were marked parallel but have file dependencies.

**Resolution steps:**

1. **Verify task independence:**
   ```bash
   # Check which files each task modified
   git diff {base-branch}..{task-1-branch} --name-only
   git diff {base-branch}..{task-2-branch} --name-only
   # Should have no overlap for parallel tasks
   ```

2. **Resolve conflict manually:**
   ```bash
   cd .worktrees/{runid}-main

   # Checkout first task branch
   git checkout {task-1-branch}

   # Attempt merge with second task
   git merge {task-2-branch}
   # Conflict will occur

   # Resolve in editor
   # Edit conflicted files

   # Complete merge
   git add {conflicted-files}
   git commit -m "Merge {task-2-branch} into {task-1-branch}"

   # Continue stacking remaining branches
   ```

3. **Update plan for future:**
   - Mark tasks as sequential, not parallel
   - File dependencies mean tasks aren't independent
   - Prevents conflict in future executions

### 4. Worktree Not Found

**Symptoms:**
- Execute command can't find `{runid}-main` worktree
- Error: `.worktrees/{runid}-main does not exist`

**Error message format:**
```markdown
❌ Worktree Not Found

**Error**: .worktrees/{run-id}-main does not exist

This means `/spectacular:spec` was not run, or the worktree was removed.
```

**Root cause:** Spec command not run, or worktree manually deleted.

**Resolution:**

Run the spec command first to create workspace:

```bash
/spectacular:spec {feature-name}
```

**This will:**
1. Create `.worktrees/{runid}-main/` directory
2. Generate `specs/{runid}-{feature-slug}/spec.md`
3. Create base branch `{runid}-main`

**Then:**
1. Run `/spectacular:plan` to generate execution plan
2. Run `/spectacular:execute` to execute the plan

**Never skip spec** - execute depends on worktree structure created by spec.

### 5. Parallel Task Worktree Creation Failure

**Symptoms:**
- `git worktree add` fails for parallel tasks
- Error: "path already exists"
- Error: "working tree contains modified files"

**Error message format:**
```markdown
❌ Parallel Task Worktree Creation Failed

**Error**: {error-message}
```

**Common causes and fixes:**

#### Cause 1: Path Already Exists

```bash
# Clean existing path
rm -rf .worktrees/{runid}-task-{phase}-{task}

# Prune stale worktree entries
git worktree prune

# Retry worktree creation
git worktree add .worktrees/{runid}-task-{phase}-{task} --detach {base-branch}
```

#### Cause 2: Uncommitted Changes on Current Branch

```bash
# Stash changes
git stash

# Or commit changes
git add --all
git commit -m "WIP: Save progress before parallel phase"

# Retry worktree creation
```

#### Cause 3: Working Directory Not Clean

```bash
# Check status
git status

# Either commit or stash changes
git add --all
git commit -m "[Task {X}.{Y}] Complete task"

# Or stash if work is incomplete
git stash

# Retry worktree creation
```

#### Cause 4: Running from Wrong Directory

```bash
# Verify not in worktree
REPO_ROOT=$(git rev-parse --show-toplevel)
if [[ "$REPO_ROOT" =~ \.worktrees ]]; then
  echo "Error: In worktree, navigate to main repo"
  cd "$(dirname "$(dirname "$REPO_ROOT")")"
fi

# Navigate to main repo root
MAIN_REPO=$(git rev-parse --show-toplevel | sed 's/\.worktrees.*//')
cd "$MAIN_REPO"

# Retry worktree creation
```

## Diagnostic Commands

**Check execution state:**

```bash
# List all worktrees
git worktree list

# View current branches
git branch | grep "{runid}-"

# View stack structure
cd .worktrees/{runid}-main
gs log short

# Check main worktree state
cd .worktrees/{runid}-main
git status
git branch --show-current
```

**Verify phase readiness:**

```bash
# Before parallel phase
cd .worktrees/{runid}-main
BASE_BRANCH=$(git branch --show-current)
echo "Parallel phase will build from: $BASE_BRANCH"

# Before sequential phase
cd .worktrees/{runid}-main
CURRENT_BRANCH=$(git branch --show-current)
echo "Sequential phase starting from: $CURRENT_BRANCH"
```

**Check task completion:**

```bash
# Verify all task branches exist
TASK_BRANCHES=({runid}-task-{phase}-1-{name} {runid}-task-{phase}-2-{name})
for BRANCH in "${TASK_BRANCHES[@]}"; do
  if git rev-parse --verify "$BRANCH" >/dev/null 2>&1; then
    echo "✅ $BRANCH exists"
  else
    echo "❌ $BRANCH missing"
  fi
done
```

## Recovery Strategies

### Resume After Manual Fix

If you fixed an issue manually:

1. Verify state is clean:
   ```bash
   cd .worktrees/{runid}-main
   git status  # Should be clean
   git log --oneline -3  # Verify commits exist
   ```

2. Continue to next task/phase:
   - Sequential: Next task creates branch from current HEAD
   - Parallel: Remaining tasks execute in parallel

### Reset Phase and Retry

If phase is fundamentally broken:

1. **Reset main worktree to pre-phase state:**
   ```bash
   cd .worktrees/{runid}-main
   git reset --hard {base-branch}
   ```

2. **Remove failed task branches:**
   ```bash
   git branch -D {failed-task-branches}
   ```

3. **Re-run phase:**
   - Fix plan if needed
   - Re-execute phase from execute command

### Abandon Feature and Clean Up

If feature implementation should be abandoned:

1. **Remove all worktrees:**
   ```bash
   git worktree remove .worktrees/{runid}-main
   git worktree remove .worktrees/{runid}-task-*
   git worktree prune
   ```

2. **Delete all feature branches:**
   ```bash
   git branch | grep "^  {runid}-" | xargs git branch -D
   ```

3. **Clean spec directory:**
   ```bash
   rm -rf specs/{runid}-{feature-slug}
   ```

## Prevention

**Prevent failures before they occur:**

1. **Validate plan before execution:**
   - Check task independence for parallel phases
   - Verify file paths are explicit, not wildcards
   - Ensure no circular dependencies

2. **Run setup validation:**
   - Use `validating-setup-commands` skill
   - Verify CLAUDE.md has install/postinstall commands
   - Test quality check commands exist

3. **Use skills correctly:**
   - `executing-parallel-phase` for ALL parallel phases
   - `executing-sequential-phase` for ALL sequential phases
   - `understanding-cross-phase-stacking` for phase boundaries

4. **Verify before proceeding:**
   - Check branches exist after each phase
   - Verify stack structure with `gs log short`
   - Run quality checks manually if agents skip them

## Quick Reference

**Common error patterns:**

| Error | Quick Fix |
|-------|-----------|
| Phase execution failed | Check error, fix manually, resume or retry |
| Parallel agent failed | Fix in branch, restart agent, or continue without |
| Merge conflict | Resolve manually, update plan to sequential |
| Worktree not found | Run `/spectacular:spec` first |
| Worktree creation failed | Clean path, stash changes, prune worktrees |

**Diagnostic sequence:**

1. Read error message carefully
2. Check execution state (worktrees, branches, commits)
3. Identify root cause (plan issue? implementation? environment?)
4. Choose recovery strategy (fix, retry, or continue)
5. Verify state is clean before proceeding

## The Bottom Line

**Most failures are recoverable.** Understand the error, verify state, fix the issue, and resume execution.

The execute command is designed to be resilient - you can fix issues manually and continue from any phase.
