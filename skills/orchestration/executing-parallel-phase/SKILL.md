---
name: executing-parallel-phase
description: Use when orchestrating parallel phases in plan execution - creates isolated worktrees for concurrent task execution, installs dependencies, spawns parallel subagents, verifies completion, stacks branches linearly, and cleans up (mandatory for ALL parallel phases including N=1)
---

# Executing Parallel Phase

## Overview

**Parallel phases enable TRUE concurrent execution via isolated git worktrees**, not just logical independence.

**Critical distinction:** Worktrees are not an optimization to prevent file conflicts. They're the ARCHITECTURE that enables multiple subagents to work simultaneously.

## When to Use

Use this skill when `execute` command encounters a phase marked "Parallel" in plan.md:
- ✅ Always use for N≥2 tasks
- ✅ **Always use for N=1** (maintains architecture consistency)
- ✅ Even when files don't overlap
- ✅ Even under time pressure
- ✅ Even with disk space pressure

**Never skip worktrees for parallel phases.** No exceptions.

## The Iron Law

```
PARALLEL PHASE = WORKTREES + SUBAGENTS
```

**Violations of this law:**
- ❌ Execute in main worktree ("files don't overlap")
- ❌ Skip worktrees for N=1 ("basically sequential")
- ❌ Use sequential strategy ("simpler")

**All of these destroy the parallel execution architecture.**

## Multi-Repo Support

### Receiving Multi-Repo Context

The orchestrator passes this context for multi-repo execution:
- `WORKSPACE_MODE`: "multi-repo" or "single-repo"
- `WORKSPACE_ROOT`: Absolute path to workspace
- Per-task `TASK_REPO` from plan

### Multi-Repo Worktree Creation

In multi-repo mode, create worktrees INSIDE each task's repo:

**Single-repo (current):**
```bash
git worktree add .worktrees/${RUN_ID}-task-${PHASE}-${TASK} ...
```

**Multi-repo (new):**
```bash
# Worktree goes inside the task's repo
cd ${TASK_REPO}
git worktree add .worktrees/${RUN_ID}-task-${PHASE}-${TASK} ...
cd ${WORKSPACE_ROOT}
```

### Per-Repo Setup Commands

In multi-repo mode, read setup commands from each task's repo:

```bash
# Single-repo: Read from project root CLAUDE.md
INSTALL_CMD=$(grep -A1 "**install**:" CLAUDE.md | tail -1)

# Multi-repo: Read from task's repo CLAUDE.md
INSTALL_CMD=$(grep -A1 "**install**:" ${TASK_REPO}/CLAUDE.md | tail -1)
```

### Per-Repo Constitution

Pass the correct constitution path to subagents:

```bash
# Single-repo
CONSTITUTION="@docs/constitutions/current/"

# Multi-repo
CONSTITUTION="@${TASK_REPO}/docs/constitutions/current/"
```

## Rationalization Table

**Predictable shortcuts you WILL be tempted to make. DO NOT make them.**

| Temptation | Why It's Wrong | What To Do |
|------------|----------------|------------|
| "The spec is too long, I'll just read the task description" | Task = WHAT files + verification. Spec = WHY architecture + requirements. Missing spec → drift. | Read the full spec. It's 2-5 minutes that prevents hours of rework. |
| "I already read the constitution, that's enough context" | Constitution = HOW to code. Spec = WHAT to build. Both needed for anchored implementation. | Read constitution AND spec, every time. |
| "The acceptance criteria are clear, I don't need the spec" | Acceptance criteria = tests pass, files exist. Spec = user flow, business logic, edge cases. | Acceptance criteria verify implementation. Spec defines requirements. |
| "I'm a subagent in a parallel phase, other tasks probably read the spec" | Each parallel subagent has isolated context. Other tasks' spec reading doesn't transfer. | Every subagent reads spec independently. No assumptions. |
| "The spec doesn't exist / I can't find it" | If spec missing, STOP and report error. Never proceed without spec. | Check `specs/{run-id}-{feature-slug}/spec.md`. If missing, fail loudly. |
| "I'll implement first, then check spec to verify" | Spec informs design decisions. Checking after implementation means rework. | Read spec BEFORE writing any code. |

**If you find yourself thinking "I can skip the spec because..." - STOP. You're rationalizing. Read the spec.**

## The Process

**Announce:** "I'm using executing-parallel-phase to orchestrate {N} concurrent tasks in Phase {phase-id}."

### Step 1: Pre-Conditions Verification (MANDATORY)

**Before ANY worktree creation, verify the environment is correct:**

**Multi-repo pre-conditions:**

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  # Verify each task's repo exists
  for TASK_REPO in ${TASK_REPOS}; do
    if [ ! -d "${WORKSPACE_ROOT}/${TASK_REPO}/.git" ]; then
      echo "❌ Error: Repo not found: ${TASK_REPO}"
      exit 1
    fi
    echo "✅ Verified repo: ${TASK_REPO}"
  done

  # No main worktree to verify in multi-repo mode
  echo "✅ Multi-repo mode: Worktrees created per-task in each repo"

  # Verify workspace root
  if [ ! -d "${WORKSPACE_ROOT}" ]; then
    echo "❌ Error: Workspace root not found: ${WORKSPACE_ROOT}"
    exit 1
  fi
  echo "✅ Workspace root verified: ${WORKSPACE_ROOT}"
fi
```

**Single-repo mode:** Continue with existing pre-condition checks:

```bash
if [ "$WORKSPACE_MODE" != "multi-repo" ]; then
  # Get main repo root
  REPO_ROOT=$(git rev-parse --show-toplevel)
  CURRENT=$(pwd)

  # Check 1: Verify orchestrator is in main repo root
  if [ "$CURRENT" != "$REPO_ROOT" ]; then
    echo "❌ Error: Orchestrator must run from main repo root"
    echo "Current: $CURRENT"
    echo "Expected: $REPO_ROOT"
    echo ""
    echo "Return to main repo: cd $REPO_ROOT"
    exit 1
  fi

  echo "✅ Orchestrator location verified: Main repo root"

  # Check 2: Verify main worktree exists
  if [ ! -d .worktrees/{runid}-main ]; then
    echo "❌ Error: Main worktree not found at .worktrees/{runid}-main"
    echo "Run /spectacular:spec first to create the workspace."
    exit 1
  fi

  # Check 3: Verify main branch exists
  if ! git rev-parse --verify {runid}-main >/dev/null 2>&1; then
    echo "❌ Error: Branch {runid}-main does not exist"
    echo "Spec must be created before executing parallel phase."
    exit 1
  fi

  # Check 4: Verify we're on correct base branch for this phase
  CURRENT_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
  EXPECTED_BASE="{expected-base-branch}"  # From plan: previous phase's last task, or {runid}-main for Phase 1

  if [ "$CURRENT_BRANCH" != "$EXPECTED_BASE" ]; then
    echo "❌ Error: Phase {phase-id} starting from unexpected branch"
    echo "   Current: $CURRENT_BRANCH"
    echo "   Expected: $EXPECTED_BASE"
    echo ""
    echo "Parallel phases must start from the correct base branch."
    echo "All parallel tasks will stack onto: $CURRENT_BRANCH"
    echo ""
    echo "If $CURRENT_BRANCH is wrong, the entire phase will be misplaced in the stack."
    echo ""
    echo "To fix:"
    echo "1. Verify previous phase completed: git log --oneline $EXPECTED_BASE"
    echo "2. Switch to correct base: cd .worktrees/{runid}-main && git checkout $EXPECTED_BASE"
    echo "3. Re-run /spectacular:execute"
    exit 1
  fi

  echo "✅ Phase {phase-id} starting from correct base: $CURRENT_BRANCH"
  echo "✅ Pre-conditions verified - safe to create task worktrees"
fi
```

**Why mandatory:**
- Prevents nested worktrees from wrong location (9f92a8 regression)
- Catches upstream drift (execute.md or other skill left orchestrator in wrong place)
- Catches missing prerequisites before wasting time on worktree creation
- Provides clear error messages for common setup issues

**Red flag:** "Skip verification to save time" - NO. 20ms verification saves hours of debugging.

### Step 1.5: Check for Existing Work (Resume Support)

**Before creating worktrees, check if tasks are already complete:**

**Multi-repo resume check:**

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  COMPLETED_TASKS=()
  PENDING_TASKS=()

  for TASK_ID in ${TASK_IDS}; do
    TASK_REPO="${TASK_REPOS[$TASK_ID]}"
    cd ${WORKSPACE_ROOT}/${TASK_REPO}

    # Use pattern matching to find branch (short-name varies)
    BRANCH_PATTERN="${RUN_ID}-task-${TASK_ID}-"
    BRANCH_NAME=$(git branch | grep "^  ${BRANCH_PATTERN}" | sed 's/^  //' | head -n1)

    if [ -n "$BRANCH_NAME" ]; then
      echo "✓ Task ${TASK_ID} (${TASK_REPO}) already complete: $BRANCH_NAME"
      COMPLETED_TASKS+=("$TASK_ID")
    else
      PENDING_TASKS+=("$TASK_ID")
    fi

    cd ${WORKSPACE_ROOT}
  done

  if [ ${#PENDING_TASKS[@]} -eq 0 ]; then
    echo "✅ All tasks already complete, skipping to stacking"
    # Jump to Step 6 (Stacking)
  else
    echo "📋 Resuming: ${#COMPLETED_TASKS[@]} complete, ${#PENDING_TASKS[@]} pending"
    echo "Will execute tasks: ${PENDING_TASKS[*]}"
  fi
fi
```

**Single-repo resume check:**

```bash
if [ "$WORKSPACE_MODE" != "multi-repo" ]; then
  COMPLETED_TASKS=()
  PENDING_TASKS=()

  for TASK_ID in {task-ids}; do
    # Use pattern matching to find branch (short-name varies)
    BRANCH_PATTERN="{runid}-task-{phase-id}-${TASK_ID}-"
    BRANCH_NAME=$(git branch | grep "^  ${BRANCH_PATTERN}" | sed 's/^  //' | head -n1)

    if [ -n "$BRANCH_NAME" ]; then
      echo "✓ Task ${TASK_ID} already complete: $BRANCH_NAME"
      COMPLETED_TASKS+=("$TASK_ID")
    else
      PENDING_TASKS+=("$TASK_ID")
    fi
  done

  if [ ${#PENDING_TASKS[@]} -eq 0 ]; then
    echo "✅ All tasks already complete, skipping to stacking"
    # Jump to Step 6 (Stacking)
  else
    echo "📋 Resuming: ${#COMPLETED_TASKS[@]} complete, ${#PENDING_TASKS[@]} pending"
    echo "Will execute tasks: ${PENDING_TASKS[*]}"
  fi
fi
```

**Why check:** Enables resume after fixing failed tasks. Avoids re-executing successful tasks, which wastes time and can cause conflicts.

**Red flags:**
- "Always create all worktrees" - NO. Wastes resources on already-completed work.
- "Trust orchestrator state" - NO. Branches are source of truth.

### Step 2: Create Worktrees (BEFORE Subagents)

**Create isolated worktree for EACH PENDING task (skip completed tasks):**

**Multi-repo worktree creation:**

For each task, create worktree in the task's repo:

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  for TASK_ID in "${PENDING_TASKS[@]}"; do
    # Get task's repo from plan
    TASK_REPO="${TASK_REPOS[$TASK_ID]}"  # e.g., "backend"

    # Get base branch for this repo (each repo may have different base)
    cd ${WORKSPACE_ROOT}/${TASK_REPO}
    BASE_BRANCH=$(git branch --show-current)

    # Create worktree inside task's repo
    git worktree add ".worktrees/${RUN_ID}-task-${TASK_ID}" --detach "$BASE_BRANCH"
    echo "✅ Created ${TASK_REPO}/.worktrees/${RUN_ID}-task-${TASK_ID} (detached HEAD)"

    cd ${WORKSPACE_ROOT}
  done

  # Verify all worktrees created across repos
  for TASK_ID in "${PENDING_TASKS[@]}"; do
    TASK_REPO="${TASK_REPOS[$TASK_ID]}"
    if [ ! -d "${WORKSPACE_ROOT}/${TASK_REPO}/.worktrees/${RUN_ID}-task-${TASK_ID}" ]; then
      echo "❌ Error: Worktree not found: ${TASK_REPO}/.worktrees/${RUN_ID}-task-${TASK_ID}"
      exit 1
    fi
  done
  echo "✅ Created ${#PENDING_TASKS[@]} worktrees across repos for parallel execution"
fi
```

**Parallel tasks across repos:**
Tasks in DIFFERENT repos can truly execute simultaneously:
- Task 2.1 (backend) creates `.worktrees/` in backend/
- Task 2.2 (frontend) creates `.worktrees/` in frontend/
- No git conflicts - completely independent repos

**Single-repo worktree creation:**

```bash
if [ "$WORKSPACE_MODE" != "multi-repo" ]; then
  # Get base branch from main worktree
  BASE_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)

  # Create worktrees only for pending tasks (from Step 1.5)
  for TASK_ID in "${PENDING_TASKS[@]}"; do
    git worktree add ".worktrees/{runid}-task-${TASK_ID}" --detach "$BASE_BRANCH"
    echo "✅ Created .worktrees/{runid}-task-${TASK_ID} (detached HEAD)"
  done

  # Verify all worktrees created
  git worktree list | grep "{runid}-task-"

  CREATED_COUNT=$(git worktree list | grep -c "{runid}-task-")
  EXPECTED_COUNT=${#PENDING_TASKS[@]}

  if [ $CREATED_COUNT -ne $EXPECTED_COUNT ]; then
    echo "❌ Error: Expected $EXPECTED_COUNT worktrees, found $CREATED_COUNT"
    exit 1
  fi

  echo "✅ Created $CREATED_COUNT worktrees for parallel execution"
fi
```

**Why --detach:** Git doesn't allow same branch in multiple worktrees. Detached HEAD enables parallel worktrees.

**Red flags:**
- "Only 1 task, skip worktrees" - NO. N=1 still uses architecture.
- "Files don't overlap, skip isolation" - NO. Isolation enables parallelism, not prevents conflicts.

### Step 3: Install Dependencies Per Worktree

**Each PENDING worktree needs its own dependencies (skip completed tasks):**

**Multi-repo dependency installation:**

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  for TASK_ID in "${PENDING_TASKS[@]}"; do
    TASK_REPO="${TASK_REPOS[$TASK_ID]}"
    WORKTREE_PATH="${WORKSPACE_ROOT}/${TASK_REPO}/.worktrees/${RUN_ID}-task-${TASK_ID}"

    # Read setup commands from task's repo CLAUDE.md
    REPO_CLAUDE_MD="${WORKSPACE_ROOT}/${TASK_REPO}/CLAUDE.md"
    INSTALL_CMD=$(grep -A1 "**install**:" ${REPO_CLAUDE_MD} | tail -1 | sed 's/^- //')
    POSTINSTALL_CMD=$(grep -A1 "**postinstall**:" ${REPO_CLAUDE_MD} | tail -1 | sed 's/^- //')

    # Check for dependency marker (varies by ecosystem)
    if [ ! -d ${WORKTREE_PATH}/node_modules ] && [ ! -d ${WORKTREE_PATH}/venv ] && [ ! -d ${WORKTREE_PATH}/vendor ]; then
      echo "📦 Installing dependencies in ${TASK_REPO} worktree for Task ${TASK_ID}..."
      bash -c "cd ${WORKTREE_PATH} && ${INSTALL_CMD}"
      if [ -n "${POSTINSTALL_CMD}" ]; then
        bash -c "cd ${WORKTREE_PATH} && ${POSTINSTALL_CMD}"
      fi
    fi
  done
fi
```

**Single-repo dependency installation:**

```bash
if [ "$WORKSPACE_MODE" != "multi-repo" ]; then
  for TASK_ID in "${PENDING_TASKS[@]}"; do
    if [ ! -d .worktrees/{runid}-task-${TASK_ID}/node_modules ]; then
      bash -c "cd .worktrees/{runid}-task-${TASK_ID} && {install-command} && {postinstall-command}"
    fi
  done
fi
```

**Why per-worktree:** Isolated worktrees can't share node_modules.

**Why bash -c:** Orchestrator stays in main repo. Subshell navigates to worktree and exits after commands complete.

**Why per-repo CLAUDE.md:** In multi-repo mode, each repo may have different package managers, languages, or setup requirements. The frontend repo might use `pnpm install` while the backend uses `pip install -r requirements.txt`.

**Red flag:** "Share node_modules for efficiency" - Breaks isolation and causes race conditions.

### Step 3.5: Extract Phase Context (Before Dispatching)

**Before spawning subagents, extract phase boundaries from plan:**

The orchestrator already parsed the plan in execute.md Step 1. Extract:
- Current phase number and name
- Tasks in THIS phase (what TO implement)
- Tasks in LATER phases (what NOT to implement)

**Format for subagent context:**
```
PHASE CONTEXT:
- Phase {current-phase-id}/{total-phases}: {phase-name}
- This phase includes: Task {task-ids-in-this-phase}

LATER PHASES (DO NOT IMPLEMENT):
- Phase {next-phase}: {phase-name} - {task-summary}
- Phase {next+1}: {phase-name} - {task-summary}
...

If implementing work beyond this phase's tasks, STOP and report scope violation.
```

**Why critical:** Spec describes WHAT to build (entire feature). Plan describes HOW/WHEN (phase breakdown). Subagents need both to avoid scope creep.

### Step 4: Dispatch Parallel Tasks

**CRITICAL: Single message with multiple Task tool calls (true parallelism):**

**Only dispatch for PENDING tasks** (from Step 1.5). Completed tasks already have branches and should not be re-executed.

**Multi-repo subagent context:**

When dispatching subagents in multi-repo mode, include per-task repo context:

```
WORKSPACE_MODE: multi-repo
WORKSPACE_ROOT: /home/user/workspace
TASK_REPO: backend
WORKTREE_PATH: backend/.worktrees/${RUN_ID}-task-2-1
CONSTITUTION: @backend/docs/constitutions/current/
SETUP_COMMANDS: (from backend/CLAUDE.md)
```

The subagent works entirely within its repo's worktree.

For each pending task, spawn subagent with embedded instructions (dispatch ALL in single message):
```
Task(Implement Task {task-id}: {task-name})

ROLE: Implement Task {task-id} in isolated worktree (parallel phase)

WORKSPACE MODE: {workspace-mode}  # "multi-repo" or "single-repo"
WORKSPACE ROOT: {workspace-root}  # Only in multi-repo mode
TASK REPO: {task-repo}            # Only in multi-repo mode (e.g., "backend")
WORKTREE: {worktree-path}         # Multi-repo: {task-repo}/.worktrees/{run-id}-task-{task-id}
                                  # Single-repo: .worktrees/{run-id}-task-{task-id}

TASK: {task-name}
FILES: {files-list}
ACCEPTANCE CRITERIA: {criteria}

PHASE BOUNDARIES:
===== PHASE BOUNDARIES - CRITICAL =====

Phase {current-phase-id}/{total-phases}: {phase-name}
This phase includes ONLY: Task {task-ids-in-this-phase}

DO NOT CREATE ANY FILES from later phases.

Later phases (DO NOT CREATE):
- Phase {next-phase}: {phase-name} - {task-summary}
  ❌ NO implementation files
  ❌ NO stub functions (even with TODOs)
  ❌ NO type definitions or interfaces
  ❌ NO test scaffolding or temporary code

If tempted to create ANY file from later phases, STOP.
"Not fully implemented" = violation.
"Just types/stubs/tests" = violation.
"Temporary/for testing" = violation.

==========================================

CONTEXT REFERENCES:
- Spec: specs/{run-id}-{feature-slug}/spec.md
- Constitution (multi-repo): {task-repo}/docs/constitutions/current/
- Constitution (single-repo): docs/constitutions/current/
- Plan: specs/{run-id}-{feature-slug}/plan.md
- Worktree: {worktree-path}

INSTRUCTIONS:

1. Navigate to isolated worktree:
   # Multi-repo mode:
   cd {workspace-root}/{task-repo}/.worktrees/{run-id}-task-{task-id}
   # Single-repo mode:
   cd .worktrees/{run-id}-task-{task-id}

2. Read constitution (if exists):
   # Multi-repo: {task-repo}/docs/constitutions/current/
   # Single-repo: docs/constitutions/current/

3. Read feature specification: specs/{run-id}-{feature-slug}/spec.md

   This provides:
   - WHAT to build (requirements, user flows)
   - WHY decisions were made (architecture rationale)
   - HOW features integrate (system boundaries)

   The spec is your source of truth for architectural decisions.
   Constitution tells you HOW to code. Spec tells you WHAT to build.

4. VERIFY PHASE SCOPE before implementing:
   - Read the PHASE BOUNDARIES section above
   - Confirm this task belongs to Phase {current-phase-id}
   - If tempted to implement later phase work, STOP
   - The plan exists for a reason - respect phase boundaries

5. Implement task following spec + constitution + phase boundaries

6. Run quality checks with exit code validation:

   **CRITICAL**: Use heredoc to prevent bash parsing errors:

   # Quality commands come from the task's repo CLAUDE.md in multi-repo mode
   bash <<'EOF'
   {test-command}   # e.g., npm test, pytest, go test
   if [ $? -ne 0 ]; then
     echo "❌ Tests failed"
     exit 1
   fi

   {lint-command}   # e.g., npm run lint, ruff check, golangci-lint
   if [ $? -ne 0 ]; then
     echo "❌ Lint failed"
     exit 1
   fi

   {build-command}  # e.g., npm run build, python -m build, go build
   if [ $? -ne 0 ]; then
     echo "❌ Build failed"
     exit 1
   fi
   EOF

   **Why heredoc**: Prevents parsing errors when commands are wrapped by orchestrator.

7. Create branch and detach HEAD using verification skill:

   Skill: phase-task-verification

   Parameters:
   - RUN_ID: {run-id}
   - TASK_ID: {phase}-{task}
   - TASK_NAME: {short-name}
   - COMMIT_MESSAGE: "[Task {phase}.{task}] {task-name}"
   - MODE: parallel

   The verification skill will:
   a) Stage changes with git add .
   b) Create branch with gs branch create
   c) Detach HEAD with git switch --detach
   d) Verify HEAD is detached (makes branch accessible in parent repo)

8. Report completion

CRITICAL:
- Work in {worktree-path}, NOT main repo or workspace root
- Do NOT stay on branch - verification skill detaches HEAD
- Do NOT create additional worktrees
- Do NOT implement work from later phases (check PHASE BOUNDARIES above)
- In multi-repo mode, branches are created in task's repo, not workspace root
```

**Parallel dispatch:** All pending tasks dispatched in single message (true concurrency).

**Red flags:**
- "I'll just do it myself" - NO. Subagents provide fresh context.
- "Execute sequentially in main worktree" - NO. Destroys parallelism.
- "Spec mentions feature X, I'll implement it now" - NO. Check phase boundaries first.
- "I'll run git add myself" - NO. Let subagent use phase-task-verification skill.

### Step 5: Verify Completion (BEFORE Stacking)

**Check ALL task branches exist AND have commits (includes both previously completed and newly created):**

**Multi-repo verification:**

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  COMPLETED_TASKS=()
  FAILED_TASKS=()

  for TASK_ID in ${TASK_IDS}; do
    TASK_REPO="${TASK_REPOS[$TASK_ID]}"
    cd ${WORKSPACE_ROOT}/${TASK_REPO}

    # Get base branch for this repo
    BASE_BRANCH=$(git branch --show-current)
    BASE_SHA=$(git rev-parse "$BASE_BRANCH")

    # Use pattern matching to find branch
    BRANCH_PATTERN="${RUN_ID}-task-${TASK_ID}-"
    BRANCH_NAME=$(git branch | grep "^  ${BRANCH_PATTERN}" | sed 's/^  //' | head -n1)

    if [ -z "$BRANCH_NAME" ]; then
      FAILED_TASKS+=("Task ${TASK_ID} (${TASK_REPO}): Branch not found")
      cd ${WORKSPACE_ROOT}
      continue
    fi

    # Verify branch has commits beyond base
    BRANCH_SHA=$(git rev-parse "$BRANCH_NAME")
    if [ "$BRANCH_SHA" = "$BASE_SHA" ]; then
      FAILED_TASKS+=("Task ${TASK_ID} (${TASK_REPO}): Branch '$BRANCH_NAME' has no commits")
      cd ${WORKSPACE_ROOT}
      continue
    fi

    COMPLETED_TASKS+=("Task ${TASK_ID} (${TASK_REPO}): $BRANCH_NAME @ $BRANCH_SHA")
    cd ${WORKSPACE_ROOT}
  done

  if [ ${#FAILED_TASKS[@]} -gt 0 ]; then
    echo "❌ Phase {phase-id} execution failed"
    echo ""
    echo "Completed tasks:"
    for task in "${COMPLETED_TASKS[@]}"; do
      echo "  ✅ $task"
    done
    echo ""
    echo "Failed tasks:"
    for task in "${FAILED_TASKS[@]}"; do
      echo "  ❌ $task"
    done
    echo ""
    echo "To resume:"
    echo "1. Review subagent output above for failure details"
    echo "2. Fix failed task(s) in {task-repo}/.worktrees/${RUN_ID}-task-{task-id}"
    echo "3. Re-run /spectacular:execute to complete phase"
    exit 1
  fi

  echo "✅ All tasks completed with valid commits across repos"
fi
```

**Single-repo verification:**

```bash
if [ "$WORKSPACE_MODE" != "multi-repo" ]; then
  COMPLETED_TASKS=()
  FAILED_TASKS=()

  # Get base commit to verify branches have new work
  BASE_BRANCH=$(git -C .worktrees/{runid}-main branch --show-current)
  BASE_SHA=$(git rev-parse "$BASE_BRANCH")

  # Check ALL task IDs, not just pending - need to verify complete set exists
  for TASK_ID in {task-ids}; do
    # Use pattern matching to find branch (short-name varies)
    BRANCH_PATTERN="{runid}-task-{phase-id}-${TASK_ID}-"
    BRANCH_NAME=$(git branch | grep "^  ${BRANCH_PATTERN}" | sed 's/^  //' | head -n1)

    if [ -z "$BRANCH_NAME" ]; then
      FAILED_TASKS+=("Task ${TASK_ID}: Branch not found")
      continue
    fi

    # Verify branch has commits beyond base
    BRANCH_SHA=$(git rev-parse "$BRANCH_NAME")
    if [ "$BRANCH_SHA" = "$BASE_SHA" ]; then
      FAILED_TASKS+=("Task ${TASK_ID}: Branch '$BRANCH_NAME' has no commits (still at base $BASE_SHA)")
      continue
    fi

    COMPLETED_TASKS+=("Task ${TASK_ID}: $BRANCH_NAME @ $BRANCH_SHA")
  done

  if [ ${#FAILED_TASKS[@]} -gt 0 ]; then
    echo "❌ Phase {phase-id} execution failed"
    echo ""
    echo "Completed tasks:"
    for task in "${COMPLETED_TASKS[@]}"; do
      echo "  ✅ $task"
    done
    echo ""
    echo "Failed tasks:"
    for task in "${FAILED_TASKS[@]}"; do
      echo "  ❌ $task"
    done
    echo ""
    echo "Common causes:"
    echo "- Subagent failed to implement task (check output above)"
    echo "- Quality checks blocked commit (test/lint/build failures)"
    echo "- git add . found no changes (implementation missing)"
    echo "- gs branch create failed (check git-spice errors)"
    echo ""
    echo "To resume:"
    echo "1. Review subagent output above for failure details"
    echo "2. Fix failed task(s) in .worktrees/{runid}-task-{task-id}"
    echo "3. Run quality checks manually to verify fixes"
    echo "4. Create branch manually: gs branch create {runid}-task-{phase-id}-{task-id}-{name} -m 'message'"
    echo "5. Re-run /spectacular:execute to complete phase"
    exit 1
  fi

  echo "✅ All {task-count} tasks completed with valid commits"
fi
```

**Why verify:** Agents can fail. Quality checks can block commits. Verify branches exist before stacking.

**Red flags:**
- "Agents said success, skip check" - NO. Agent reports ≠ branch existence.
- "Trust but don't verify" - NO. Verify preconditions.

### Step 6: Stack Branches Linearly (BEFORE Cleanup)

**Multi-repo stacking:**

Each repo has its own stack. After parallel phase:

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  # Group tasks by repo
  declare -A REPO_TASKS
  for TASK_ID in ${TASK_IDS}; do
    TASK_REPO="${TASK_REPOS[$TASK_ID]}"
    REPO_TASKS[$TASK_REPO]+="${TASK_ID} "
  done

  # Stack branches within each repo
  for REPO in "${!REPO_TASKS[@]}"; do
    echo "📋 Stacking branches in ${REPO}..."
    cd ${WORKSPACE_ROOT}/${REPO}

    # Get tasks for this repo
    TASKS=(${REPO_TASKS[$REPO]})

    # Get base branch for this repo
    BASE_BRANCH=$(git branch --show-current)

    # Ensure base branch is tracked
    if ! gs branch track --show "$BASE_BRANCH" >/dev/null 2>&1; then
      echo "⏺ Base branch not tracked yet, tracking now: $BASE_BRANCH"
      git checkout "$BASE_BRANCH"
      gs branch track
    fi

    # Stack this repo's task branches
    for i in "${!TASKS[@]}"; do
      TASK_ID="${TASKS[$i]}"
      BRANCH="${RUN_ID}-task-${TASK_ID}"

      if [ $i -eq 0 ]; then
        git checkout "$BRANCH"
        gs branch track
        gs upstack onto "$BASE_BRANCH"
      else
        PREV_TASK="${TASKS[$((i-1))]}"
        PREV_BRANCH="${RUN_ID}-task-${PREV_TASK}"
        git checkout "$BRANCH"
        gs branch track
        gs upstack onto "$PREV_BRANCH"
      fi
    done

    echo "✅ ${REPO} stack complete:"
    gs log short
    echo ""

    cd ${WORKSPACE_ROOT}
  done

  echo "✅ All repo stacks complete"
fi
```

Note: Cannot stack across repos (git-spice limitation). Each repo maintains its own linear stack.

**Single-repo stacking:**

Use loop-based algorithm for any N (orchestrator stays in main repo):

```bash
if [ "$WORKSPACE_MODE" != "multi-repo" ]; then
  # Stack branches in main worktree using heredoc (orchestrator doesn't cd)
  bash <<'EOF'
  cd .worktrees/{runid}-main

  # Get base branch (what parallel tasks should stack onto)
  BASE_BRANCH=$(git branch --show-current)

  # Ensure base branch is tracked before stacking onto it
  # (Sequential phases may have created branches without tracking)
  if ! gs branch track --show "$BASE_BRANCH" >/dev/null 2>&1; then
    echo "⏺ Base branch not tracked yet, tracking now: $BASE_BRANCH"
    git checkout "$BASE_BRANCH"
    gs branch track
  fi

  TASK_BRANCHES=( {array-of-branch-names} )
  TASK_COUNT=${#TASK_BRANCHES[@]}

  # Handle N=1 edge case
  if [ $TASK_COUNT -eq 1 ]; then
    git checkout "${TASK_BRANCHES[0]}"
    gs branch track
    gs upstack onto "$BASE_BRANCH"  # Explicitly set base for single parallel task
  else
    # Handle N≥2
    for i in "${!TASK_BRANCHES[@]}"; do
      BRANCH="${TASK_BRANCHES[$i]}"

      if [ $i -eq 0 ]; then
        # First task: track + upstack onto base branch (from previous phase)
        git checkout "$BRANCH"
        gs branch track
        gs upstack onto "$BASE_BRANCH"  # Connect to previous phase's work
      else
        # Subsequent: track + upstack onto previous
        PREV_BRANCH="${TASK_BRANCHES[$((i-1))]}"
        git checkout "$BRANCH"
        gs branch track
        gs upstack onto "$PREV_BRANCH"
      fi
    done
  fi

  # Leave main worktree on last branch for next phase continuity
  # Sequential phases will naturally stack on this branch

  # Display stack
  echo "📋 Stack after parallel phase:"
  gs log short
  echo ""

  # Verify stack correctness (catch duplicate commits)
  echo "🔍 Verifying stack integrity..."
  STACK_VALID=1
  declare -A SEEN_COMMITS

  for BRANCH in "${TASK_BRANCHES[@]}"; do
    BRANCH_SHA=$(git rev-parse "$BRANCH")

    # Check if this commit SHA was already seen
    if [ -n "${SEEN_COMMITS[$BRANCH_SHA]}" ]; then
      echo "❌ ERROR: Stack integrity violation"
      echo "   Branch '$BRANCH' points to commit $BRANCH_SHA"
      echo "   But '${SEEN_COMMITS[$BRANCH_SHA]}' already points to that commit"
      echo ""
      echo "This means one of these branches has no unique commits."
      echo "Possible causes:"
      echo "- Subagent failed to commit work"
      echo "- Quality checks blocked commit"
      echo "- Branch creation succeeded but commit failed"
      STACK_VALID=0
      break
    fi

    SEEN_COMMITS[$BRANCH_SHA]="$BRANCH"
    echo "  ✓ $BRANCH @ $BRANCH_SHA"
  done

  if [ $STACK_VALID -eq 0 ]; then
    echo ""
    echo "❌ Stack verification FAILED - preserving worktrees for debugging"
    echo ""
    echo "To investigate:"
    echo "1. Check branch commits: git log --oneline $BRANCH"
    echo "2. Check worktree state: ls -la .worktrees/"
    echo "3. Review subagent output for failed task"
    echo "4. Fix manually, then re-run /spectacular:execute"
    exit 1
  fi

  echo "✅ Stack integrity verified - all branches have unique commits"
EOF
fi
```

**Why heredoc:** Orchestrator stays in main repo. Heredoc creates subshell that navigates to worktree and exits.

**Why before cleanup:** Need worktrees accessible for debugging if stacking fails.

**Why verify stack:** Catches duplicate commits (two branches pointing to same SHA) which indicates missing work.

**Red flag:** "Clean up first to free disk space" - NO. Stacking MUST happen first, and verification before cleanup.

### Step 7: Clean Up Worktrees (AFTER Stacking)

**IMPORTANT**: This step only runs if Step 5 verification passes. If any task fails, Step 5 exits with code 1, aborting the workflow. Failed task worktrees are preserved for debugging.

**Multi-repo cleanup:**

Remove worktrees from each repo:

```bash
if [ "$WORKSPACE_MODE" = "multi-repo" ]; then
  for TASK_ID in ${TASK_IDS}; do
    TASK_REPO="${TASK_REPOS[$TASK_ID]}"
    cd ${WORKSPACE_ROOT}/${TASK_REPO}
    git worktree remove ".worktrees/${RUN_ID}-task-${TASK_ID}" --force
    echo "✅ Removed ${TASK_REPO}/.worktrees/${RUN_ID}-task-${TASK_ID}"
    cd ${WORKSPACE_ROOT}
  done

  # Verify cleanup across all repos
  for REPO in ${REPOS_WITH_TASKS}; do
    REMAINING=$(cd ${WORKSPACE_ROOT}/${REPO} && git worktree list | grep "${RUN_ID}-task-" || true)
    if [ -n "$REMAINING" ]; then
      echo "⚠️  Worktrees remain in ${REPO}: $REMAINING"
    fi
  done
  echo "✅ Multi-repo worktree cleanup complete"
fi
```

**Single-repo cleanup:**

```bash
if [ "$WORKSPACE_MODE" != "multi-repo" ]; then
  for TASK_ID in {task-ids}; do
    git worktree remove ".worktrees/{runid}-task-${TASK_ID}"
  done

  # Verify cleanup
  git worktree list | grep "{runid}-task-"
  # Should be empty
fi
```

**Why after stacking:** Branches must be stacked and verified before destroying evidence.

**Why conditional**: Failed worktrees must be preserved so users can debug, fix, and manually create branches before resuming.

### Step 8: Code Review (Binary Quality Gate)

**Check review frequency setting (from execute.md Step 1.7):**

```bash
REVIEW_FREQUENCY=${REVIEW_FREQUENCY:-per-phase}
```

**If REVIEW_FREQUENCY is "end-only" or "skip":**
```
Skipping per-phase code review (frequency: {REVIEW_FREQUENCY})
Phase {N} complete - proceeding to next phase
```
Mark phase complete and continue to next phase.

**If REVIEW_FREQUENCY is "optimize":**

Analyze the completed phase to decide if code review is needed:

**High-risk indicators (REVIEW REQUIRED):**
- Schema or migration changes
- Authentication/authorization logic
- External API integrations or webhooks
- Foundation phases (Phase 1-2 establishing patterns)
- 3+ parallel tasks (coordination complexity)
- New architectural patterns introduced
- Security-sensitive code (payment, PII, access control)
- Complex business logic with multiple edge cases
- Changes affecting multiple layers (database → API → UI)

**Low-risk indicators (SKIP REVIEW):**
- Pure UI component additions (no state/logic)
- Documentation or comment updates
- Test additions without implementation changes
- Refactoring with existing test coverage
- Isolated utility functions
- Configuration file updates (non-security)

**Analyze this phase:**
- Phase number: {N}
- Tasks completed in parallel: {task-list}
- Files modified across tasks: {file-list}
- Types of changes: {describe changes}

**Decision:**
If ANY high-risk indicator present → Proceed to code review below
If ONLY low-risk indicators → Skip review:
```
✓ Phase {N} assessed as low-risk - skipping review (optimize mode)
  Reasoning: {brief explanation of why low-risk}
Phase {N} complete - proceeding to next phase
```

**If REVIEW_FREQUENCY is "per-phase" OR optimize mode decided to review:**

Use `requesting-code-review` skill to call code-reviewer agent, then parse results STRICTLY:

**CRITICAL - AUTONOMOUS EXECUTION (NO USER PROMPTS):**

This is an automated execution workflow. Code review rejections trigger automatic fix loops, NOT user prompts.

**NEVER ask user what to do, even if:**
- Issues seem "architectural" or "require product decisions"
- Scope creep with passing quality checks (implement less, not ask)
- Multiple rejections (use escalation limit at 3, not ask user)
- Uncertain how to fix (fix subagent figures it out with spec + constitution context)
- Code works but violates plan (plan violation = failure, auto-fix to plan)

**Autonomous execution means AUTONOMOUS.** User prompts break automation and violate this skill.

1. **Dispatch code review:**
   ```
   Skill tool: requesting-code-review

   Context provided to reviewer:
   - WORKTREE: .worktrees/{runid}-main
   - PHASE: {phase-number}
   - TASKS: {task-list}
   - BASE_BRANCH: {base-branch-name}
   - SPEC: specs/{run-id}-{feature-slug}/spec.md
   - PLAN: specs/{run-id}-{feature-slug}/plan.md (for phase boundary validation)

   **CRITICAL - EXHAUSTIVE FIRST-PASS REVIEW:**

   This is your ONLY opportunity to find issues. Re-review is for verifying fixes, NOT discovering new problems.

   Check EVERYTHING in this single review:
   □ Implementation correctness - logic bugs, edge cases, error handling, race conditions
   □ Test correctness - expectations match actual behavior, coverage is complete, no false positives
   □ Cross-file consistency - logic coherent across all files, no contradictions
   □ Architectural soundness - follows patterns, proper separation of concerns, no coupling issues
   □ Scope adherence - implements ONLY Phase {phase-number} work, no later-phase implementations
   □ Constitution compliance - follows all project standards and conventions

   Find ALL issues NOW. If you catch yourself thinking "I'll check that in re-review" - STOP. Check it NOW.

   Binary verdict required: "Ready to merge? Yes" (only if EVERYTHING passes) or "Ready to merge? No" (list ALL issues found)
   ```

2. **Parse output using binary algorithm:**

   Read the code review output and search for "Ready to merge?" field:

   - ✅ **"Ready to merge? Yes"** → APPROVED
     - Announce: "✅ Code review APPROVED - Phase {N} complete, proceeding"
     - Continue to next phase

   - ❌ **"Ready to merge? No"** → REJECTED
     - STOP execution
     - Report: "❌ Code review REJECTED - critical issues found"
     - List all Critical and Important issues from review
     - Dispatch fix subagent IMMEDIATELY (no user prompt, no questions)
     - Go to step 5 (re-review after fixes)

   - ❌ **"Ready to merge? With fixes"** → REJECTED
     - STOP execution
     - Report: "❌ Code review requires fixes before proceeding"
     - List all issues from review
     - Dispatch fix subagent IMMEDIATELY (no user prompt, no questions)
     - Go to step 5 (re-review after fixes)

   - ⚠️ **No output / empty response** → RETRY ONCE
     - Warn: "⚠️ Code review returned no output - retrying once"
     - This may be a transient issue (timeout, connection error)
     - Go to step 3 (retry review)
     - If retry ALSO has no output → FAILURE (go to step 4)

   - ❌ **Soft language (e.g., "APPROVED WITH MINOR SUGGESTIONS")** → REJECTED
     - STOP execution
     - Report: "❌ Code review used soft language instead of binary verdict"
     - Warn: "Binary gate requires explicit 'Ready to merge? Yes'"
     - Go to step 3 (re-review)

   - ⚠️ **Missing "Ready to merge?" field** → RETRY ONCE
     - Warn: "⚠️ Code review output missing 'Ready to merge?' field - retrying once"
     - This may be a transient issue (network glitch, model error)
     - Go to step 3 (retry review)
     - If retry ALSO missing field → FAILURE (go to step 4)

3. **Retry review (if malformed output):**
   - Dispatch `requesting-code-review` skill again with same parameters
   - Parse retry output using step 2 binary algorithm
   - If retry succeeds with "Ready to merge? Yes":
     - Announce: "✅ Code review APPROVED (retry succeeded) - Phase {N} complete, proceeding"
     - Continue to next phase
   - If retry returns valid verdict (No/With fixes):
     - Follow normal REJECTED flow (fix issues, re-review)
   - If retry ALSO has missing "Ready to merge?" field:
     - Go to step 4 (both attempts failed)

4. **Both attempts malformed (FAILURE):**
   - STOP execution immediately
   - Report: "❌ Code review failed twice with malformed output"
   - Display excerpts from both attempts for debugging
   - Suggest: "Review agent may not be following template - check code-reviewer skill"
   - DO NOT hallucinate issues from malformed text
   - DO NOT dispatch fix subagents
   - Fail execution

5. **Re-review loop (if REJECTED with valid verdict):**

   **Initialize iteration tracking:**
   ```bash
   REJECTION_COUNT=0
   ```

   **On each rejection:**
   ```bash
   REJECTION_COUNT=$((REJECTION_COUNT + 1))

   # Check escalation limit
   if [ $REJECTION_COUNT -gt 3 ]; then
     echo "⚠️  Code review rejected $REJECTION_COUNT times"
     echo ""
     echo "Issues may require architectural changes beyond subagent scope."
     echo "Reporting to user for manual intervention:"
     echo ""
     # Display all issues from latest review
     # Suggest: Review architectural assumptions, may need spec revision
     exit 1
   fi

   # Dispatch fix subagent
   echo "🔧 Dispatching fix subagent to address issues (attempt $REJECTION_COUNT)..."

   # Use Task tool to dispatch fix subagent:
   Task(Fix Phase {N} code review issues)
   Prompt: Fix the following issues found in Phase {N} code review:

   {List all issues from review output with severity (Critical/Important/Minor) and file locations}

   CONTEXT FOR FIXES:

   1. Read constitution (if exists): docs/constitutions/current/

   2. Read feature specification: specs/{run-id}-{feature-slug}/spec.md

      The spec provides architectural context for fixes:
      - WHY decisions were made (rationale for current implementation)
      - HOW features should integrate (system boundaries)
      - WHAT requirements must be met (acceptance criteria)

   3. Read implementation plan: specs/{run-id}-{feature-slug}/plan.md

      The plan provides phase boundaries and scope:
      - WHEN to implement features (which phase owns what)
      - WHAT tasks belong to Phase {N} (scope boundaries)
      - WHAT tasks belong to later phases (do NOT implement)

      **If scope creep detected (implemented work from later phases):**
      - Roll back to Phase {N} scope ONLY
      - Remove implementations that belong to later phases
      - Keep ONLY the work defined in Phase {N} tasks
      - The plan exists for a reason - respect phase boundaries

   4. Apply fixes following spec + constitution + plan boundaries

   CRITICAL: Work in .worktrees/{runid}-main
   CRITICAL: Amend existing branch or add new commit (do NOT create new branch)
   CRITICAL: Run all quality checks before completion (test, lint, build)
   CRITICAL: Verify all issues resolved before reporting completion
   CRITICAL: If scope creep, implement LESS not ask user what to keep

   # After fix completes
   echo "⏺ Re-reviewing Phase {N} after fixes (iteration $((REJECTION_COUNT + 1)))..."
   # Return to step 1 (dispatch review again)
   ```

   **On approval after fixes:**
   ```bash
   echo "✅ Code review APPROVED (after $REJECTION_COUNT fix iteration(s)) - Phase {N} complete"
   ```

   **Escalation triggers:**
   - After 3 rejections: Stop and report to user
   - Prevents infinite loops on unsolvable architectural problems
   - User can review, adjust spec, or proceed manually

**Critical:** Only "Ready to merge? Yes" allows proceeding. Everything else stops execution.

**Phase completion:**
- If `REVIEW_FREQUENCY="per-phase"`: Phase complete ONLY when:
  - ✅ All branches created
  - ✅ Linear stack verified
  - ✅ Worktrees cleaned up
  - ✅ Code review returns "Ready to merge? Yes"
- If `REVIEW_FREQUENCY="end-only"` or `"skip"`: Phase complete when:
  - ✅ All branches created
  - ✅ Linear stack verified
  - ✅ Worktrees cleaned up
  - (Code review skipped)

## Rationalization Table

| Excuse | Reality |
|--------|---------|
| "Only 1 task, skip worktrees" | N=1 still uses parallel architecture. No special case. |
| "Files don't overlap, skip isolation" | Worktrees enable parallelism, not prevent conflicts. |
| "Already spent 30min on setup" | Sunk cost fallacy. Worktrees ARE the parallel execution. |
| "Simpler to execute sequentially" | Simplicity ≠ correctness. Parallel phase = worktrees. |
| "Agents said success, skip verification" | Agent reports ≠ branch existence. Verify preconditions. |
| "Disk space pressure, clean up first" | Stacking must happen before cleanup. No exceptions. |
| "Git commands work from anywhere" | TRUE, but path resolution is CWD-relative. Verify location. |
| "I'll just do it myself" | Subagents provide fresh context and true parallelism. |
| "Worktrees are overhead" | Worktrees ARE the product. Parallelism is the value. |
| "Review rejected, let me ask user what to do" | Autonomous execution means automatic fixes. No asking. |
| "Issues are complex, user should decide" | Fix subagent handles complexity. That's the architecture. |
| "Safer to get user input before fixing" | Re-review provides safety. Fix, review, repeat until clean. |
| "Scope creep but quality passes, ask user to choose" | Plan violation = failure. Fix subagent removes extra scope automatically. |
| "Work is done correctly, just ahead of schedule" | Phases exist for review isolation. Implement less, not merge early. |
| "Spec mentions feature X, might as well implement now" | Spec = WHAT to build total. Plan = WHEN to build each piece. Check phase. |

## Red Flags - STOP and Follow Process

If you're thinking ANY of these, you're about to violate the skill:

- "This is basically sequential with N=1"
- "Files don't conflict, isolation unnecessary"
- "Worktree creation takes too long"
- "Already behind schedule, skip setup"
- "Agents succeeded, no need to verify"
- "Disk space warning, clean up now"
- "Current directory looks right"
- "Relative paths are cleaner"

**All of these mean: STOP. Follow the process exactly.**

## Common Mistakes

### Mistake 1: Treating Parallel as "Logically Independent"

**Wrong mental model:** "Parallel means tasks are independent, so I can execute them sequentially in one worktree."

**Correct model:** "Parallel means tasks execute CONCURRENTLY via multiple subagents in isolated worktrees."

**Impact:** Destroys parallelism. Turns 3-hour calendar time into 9-hour sequential execution.

### Mistake 2: Efficiency Optimization

**Wrong mental model:** "Worktrees are overhead when files don't overlap."

**Correct model:** "Worktrees are the architecture. Without them, no concurrent execution exists."

**Impact:** Sequential execution disguised as parallel. No time savings.

### Mistake 3: Cleanup Sequencing

**Wrong mental model:** "Branches exist independently of worktrees, so cleanup order doesn't matter."

**Correct model:** "Stacking before cleanup allows debugging if stacking fails and runs integration tests on complete stack."

**Impact:** Can't debug stacking failures. Premature cleanup destroys evidence.

## Quick Reference

**Mandatory sequence (no variations):**

1. Verify location (main repo root)
2. Create worktrees (ALL tasks, including N=1)
3. Install dependencies (per worktree)
4. Spawn subagents (parallel dispatch)
5. Verify branches exist (before stacking)
6. Stack branches (before cleanup)
7. Clean up worktrees (after stacking)
8. Code review

**Never skip. Never reorder. No exceptions.**

## The Bottom Line

**Parallel phases use worktrees.** Always. Even N=1. Even when files don't overlap. Even under pressure.

If you're not creating worktrees, you're not executing parallel phases - you're executing sequential phases incorrectly labeled as parallel.

The skill is the architecture. Follow it exactly.
