---
name: implement-plan
description: "Execute an approved implementation plan with beads-backed task tracking."
allowed-tools: Read, Glob, Grep, Write, Edit, Bash, Task
---

# Implement Plan

Execute plans with persistent beads-backed progress tracking.

## When To Use

- User says "implement plan", "execute plan", "build it"
- User references a plan file with "@thoughts/shared/plans/..."

## Core Behavior

1. **Parse plan into beads tasks** with dependencies
2. **Track progress via bd** (survives /clear, /compact)
3. **Check context at 50%** → pause, sync, suggest compact
4. **Resume via bd ready** after compact

---

## Workflow

### Phase 1: Pre-Implementation Check

```bash
# Check if beads initialized
if [ ! -d .beads ]; then
  bd init --stealth
fi

# Sync any existing state
bd sync
```

```
1. Check current context level
2. If context > 30%:
   → bd sync (save state)
   → Output: "Context at X%. Recommend /compact before starting."
   → Stop and wait
3. If context < 30%:
   → Proceed to Phase 2
```

### Phase 2: Setup - Create Beads Tasks

```bash
# Create epic for the plan
bd create "Implement: [Plan Name]" -t epic --json
# Returns bd-xxxx (epic ID)

# Create task group 1
bd create "Group 1: [Description]" --deps parent:$EPIC_ID -p 1 --json
bd create "Task 1.1: [Description]" --deps parent:$GROUP1_ID -p 1 --json
bd create "Task 1.2: [Description]" --deps parent:$GROUP1_ID -p 1 --json

# Create task group 2 (depends on group 1)
bd create "Group 2: [Description]" --deps parent:$EPIC_ID -p 1 --json
bd dep add $GROUP2_ID $GROUP1_ID --type blocks

# ... continue for all groups
```

**Task grouping**: 3-5 tasks per group, dependencies between groups.

### Phase 3: Execute (by group)

```bash
# Get first ready task
bd ready --json

# For each task:
bd update $TASK_ID --status in_progress --json
```

For each task:
```
1. Implement the task
2. Test
3. Commit: "feat(scope): description - step X.Y"
4. Close the task:
   bd close $TASK_ID --reason "commit: abc123" --json
5. Check context level
6. If context > 50%:
   → bd sync
   → Output: "Context at Y%. Recommend /compact."
   → Output: "After compact, say 'continue' - beads knows where you are"
   → Stop
```

### Phase 3b: Parallel Execution for Independent Tasks

**Key Insight:** Within a task group, tasks without dependencies on each other can run in parallel.

#### Dependency Analysis

```bash
# Get all ready tasks (may be multiple!)
bd ready --json
# Returns: [{"id": "bd-a1b2", "title": "Task A"}, {"id": "bd-c3d4", "title": "Task B"}]
```

If multiple tasks are ready simultaneously, they have NO dependencies on each other.

#### Parallel Execution Pattern

```
1. ANALYZE: Get all ready tasks
2. CLASSIFY:
   - File-disjoint? (different files) → Can parallelize
   - Same files? → Must be sequential
3. SPAWN: For file-disjoint tasks, spawn background agents:

Task:
  subagent_type: general-purpose
  description: "Implement Task A"
  prompt: |
    Implement: [Task A description]
    Files: [list of files]
    Tests: [test requirements]
    Commit when done with message: "feat(scope): Task A"
  run_in_background: true

Task:
  subagent_type: general-purpose
  description: "Implement Task B"
  prompt: |
    Implement: [Task B description]
    Files: [list of files]
    Tests: [test requirements]
    Commit when done with message: "feat(scope): Task B"
  run_in_background: true

4. CONTINUE: Main agent can work on another task or wait
5. POLL: Check background agents via TaskOutput
6. CLOSE: Mark completed tasks in beads
```

#### Example: Parallel Independent Tasks

```
Given ready tasks:
- bd-a1: "Create user model" (touches: models/user.py)
- bd-b2: "Create product model" (touches: models/product.py)
- bd-c3: "Add auth middleware" (touches: middleware/auth.py)

Analysis: All touch DIFFERENT files → Parallelize ALL

Spawn 3 background agents simultaneously.
Main agent polls periodically.
As each completes: bd close <id> --reason "commit: xyz"
```

#### Parallel Execution Benefits

| Sequential | Parallel |
|------------|----------|
| Task A (5 min) | Spawn A, B, C (instant) |
| Task B (5 min) | All run concurrently |
| Task C (5 min) | Poll when ready |
| **Total: 15 min** | **Total: 5 min** |

#### When NOT to Parallelize

- Tasks modify same files
- Task B uses output from Task A
- Beads shows dependency: `bd dep tree` shows blocker
- Context already high (>40%) - sequential is safer

### Phase 4: Completion

```bash
# All tasks done
bd close $EPIC_ID --reason "Plan completed" --json
bd sync

# Verify
bd list --status closed --json | grep $EPIC_ID
```

---

## Beads Task Structure

```
Epic: "Implement: Auth System"
├── Group 1: "Setup" (3 tasks)
│   ├── Task 1.1: "Create user model"
│   ├── Task 1.2: "Add password hashing"
│   └── Task 1.3: "Create auth middleware"
├── Group 2: "Endpoints" (4 tasks) [blocked by Group 1]
│   ├── Task 2.1: "Login endpoint"
│   ├── Task 2.2: "Logout endpoint"
│   ├── Task 2.3: "Register endpoint"
│   └── Task 2.4: "Password reset"
└── Group 3: "Tests" (3 tasks) [blocked by Group 2]
    ├── Task 3.1: "Unit tests"
    ├── Task 3.2: "Integration tests"
    └── Task 3.3: "E2E tests"
```

---

## Context Thresholds

| Level | Action |
|-------|--------|
| < 30% | Start/continue normally |
| 30-50% | Continue with caution |
| > 50% | **Pause, bd sync, suggest compact** |
| > 70% | **Stop immediately**, bd sync |

---

## Resuming After Compact

After `/compact`, beads knows exactly where you are:

```bash
bd sync              # Pull latest state
bd ready --json      # Shows next unblocked task
bd list --status in_progress --json  # Shows any in-progress
```

User just says "continue" and you pick up exactly where you left off.

---

## Commit Format

```
type(scope): description - step X.Y

Types: feat, fix, refactor, test, docs, chore
```

Each commit references the beads task:
```bash
bd close $ID --reason "commit: abc123"
```

---

## Session End (Critical!)

Before ending any session:

```bash
bd sync  # ALWAYS sync before session end
```

This ensures all progress is persisted and resumable.

---

## Handling Issues

### Context Running Low
1. Complete current task if close
2. `bd sync` to save all progress
3. Output: "Context at X%. Stopping."
4. Suggest: "/compact then 'continue'"

### Unexpected Complexity
1. Create new beads task for the complexity:
   ```bash
   bd create "Handle edge case: X" --deps parent:$CURRENT -p 0 --json
   ```
2. If blocking, pause and ask user
3. Don't deviate from plan without approval

### Test Failures
1. Fix immediately if simple
2. Create blocker task if complex:
   ```bash
   bd create "Fix: test failure in X" -t bug -p 0 --json
   ```

---

## Keywords

implement plan, execute plan, run plan, build it, continue, bd ready
