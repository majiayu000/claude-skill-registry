---
name: auto-run
description: "Autonomous dispatch-reconcile loop for batch task processing. Use with /auto-run --through <id> to execute tasks unattended. Requires beads tasks to exist. Supports --resume for checkpoint recovery and --skip-milestone-review."
allowed-tools: Bash, Read, Glob, Grep, Write, Edit, Skill, TeamCreate, TeamDelete, TaskCreate, TaskUpdate, TaskList, SendMessage, Task, AskUserQuestion
---

# Autonomous Orchestrator Loop: $ARGUMENTS

You are an autonomous orchestrator. You dispatch workers, handle their completions, reconcile results, and dispatch newly unblocked tasks — repeating until all work is done or limits are reached.

## Section 1: Argument Parsing

Arguments: `$ARGUMENTS`

Parse the following flags:
- `--max-batches N` — Stop after N dispatch rounds (default: unlimited)
- `--max-hours H` — Stop after H hours (default: unlimited)
- `--max-concurrent N` — Max parallel workers per batch (default: 3)
- `--dry-run` — Show what would be dispatched without acting
- `--resume` — Resume from checkpoint (skip orient)
- `--skip-milestone-review` — Skip the milestone review phase after tasks complete
- `--milestone-review-iterations N` — Max milestone review iterations (default: 5)
- `--through <task-id>` — Complete everything needed to finish this task, then stop
- `--epic <epic-id>` — Complete all tasks within this epic, then stop
- `--only <id1> <id2> ...` — Only dispatch these specific tasks (and their blockers)

## Section 2: Initial Setup

### Check for Checkpoint

Read checkpoint at `docs/auto-run-checkpoint.json` (resolve from main repo root via `git worktree list | head -1 | awk '{print $1}'`).

**If `--resume` AND checkpoint exists with status "running":**
1. Read checkpoint state (including scope config)
2. Log resumption context: batch number, completed list, in-progress list, scope
3. Check if any previously in-progress tasks have since completed — look for session summaries:
   ```bash
   ls docs/session_summaries/<task-id>*.txt 2>/dev/null
   ```
4. If summaries found → reconcile them first:
   Call `/reconcile-summary --yes --no-cleanup` via Skill tool
5. Skip orient, proceed to dispatch loop (Section 3)

**If fresh start (no checkpoint or no `--resume`):**
1. Run `/orient` via Skill tool
2. Resolve scope (see Section 2.1)
3. Write initial checkpoint

Write checkpoint JSON to `docs/auto-run-checkpoint.json` with:
- `version`: 1
- `status`: "running"
- `start_time`: current ISO8601 timestamp
- `config`: parsed flags (max_batches, max_hours, max_concurrent)
- `scope`: resolved scope (see 2.1)
- `batch_number`: 0
- `tasks`: { completed: [], failed: [], in_progress: [], branch_isolation_failures: [] }
- `stats`: { total_dispatched: 0, total_completed: 0, total_failed: 0, total_batches: 0, total_branch_isolation_failures: 0 }

### 2.1 Resolve Scope

Determine which tasks are in-scope for this auto-run:

**If `--through <task-id>`:**
Walk the dependency graph backward from `<task-id>` to find all transitive blockers:
```bash
bd show <task-id>  # get BLOCKED BY list
# Recursively resolve each blocker's blockers
```
Build a set of all task IDs that must complete for `<task-id>` to be unblocked and completable. Include `<task-id>` itself. Store as `scope.task_ids` in checkpoint. Set `scope.mode` to "through" and `scope.target` to `<task-id>`.

**If `--epic <epic-id>`:**
List all tasks that are children/subtasks of this epic:
```bash
bd list --all | grep <epic-id>
```
Store all child task IDs as `scope.task_ids`. Set `scope.mode` to "epic" and `scope.target` to `<epic-id>`.

**If `--only <id1> <id2> ...`:**
Use exactly those task IDs. Also resolve their transitive blockers (tasks that must complete first) and include those in scope. Store as `scope.task_ids`. Set `scope.mode` to "only".

**If no scope flags:**
`scope.task_ids` = null (all ready tasks are in scope). Set `scope.mode` to "all".

Log the resolved scope:
```
Auto-run scope: N tasks [list IDs]. Target: <task-id or epic-id or "all">
```

### First Dispatch

1. Run `bd ready` to get available tasks
2. Filter ready tasks to only those in `scope.task_ids` (if set; if null, use all)
3. If no in-scope ready tasks:
   - Check if target task is already closed → exit with completion report
   - Otherwise report "No ready tasks in scope" and exit
4. If ready tasks exist:
   - Calculate count = min(ready_count, max_concurrent)
   - Call `/dispatch <specific-task-ids> --count <count> --no-plan --yes` via Skill tool, passing only in-scope task IDs
4a. After dispatch returns, check its output for branch isolation failures:
   - If dispatch reported failures, record them in checkpoint `tasks.branch_isolation_failures` (see schema below)
   - Only count successfully isolated workers as `in_progress`
   - Failed tasks return to the ready pool automatically (they were unassigned by dispatch)
   - **Circuit breaker**: If a task ID already appears in `branch_isolation_failures` from a prior batch with `attempts >= 2`, move it to `failed` with reason `"branch_isolation_repeated_failure"` and log: "Task <id> failed branch isolation twice — flagged for human attention."
5. Update checkpoint: add dispatched tasks to `in_progress`, set `batch_number: 1`

## Section 3: Main Loop (Event-Driven)

The loop is driven by Agent Teams. When a teammate finishes, you receive their message as a new conversation turn. Each time you receive a teammate message:

### Step A — Identify Completion

Extract task ID from the teammate's message or idle notification. Check for session summary:
```bash
ls docs/session_summaries/<task-id>*.txt 2>/dev/null
```

### Step B — Reconcile

**If summary exists:**
Call `/reconcile-summary <task-id> --no-cleanup --yes` via Skill tool.

After reconciliation, check if the completed task touched frontend files:
```bash
# Check the session summary for frontend file extensions
grep -E '\.(tsx|jsx|vue|svelte|html|css|scss)' docs/session_summaries/<task-id>*.txt 2>/dev/null
```

If frontend files were modified, note for milestone review:
```
Frontend changes detected in <task-id> — Playwright browser verification will run during milestone review.
```

**If no summary (teammate may have failed):**
1. Send one follow-up message to the teammate asking for status (SendMessage)
2. If still stuck after the follow-up: mark as failed
3. Create investigation task:
   ```bash
   bd create --title="Investigate: <task-id> failed" --type=task --priority=1
   ```

Update checkpoint: move task from `in_progress` to `completed` (or `failed`).

**Circuit breaker:** If the same task ID appears in the checkpoint's `failed` list with `attempts >= 2`, skip it and log: "Task <id> failed twice — flagged for human attention."

### Step C — Check Limits

- If `--max-batches` reached → write checkpoint with `status: "paused"`, report "Auto-run paused. N tasks remain.", exit.
- If `--max-hours` elapsed (compare current time to `start_time` in checkpoint) → same.

### Step D — Dispatch Next Batch

1. Run `bd ready`
2. Filter to in-scope tasks only (if `scope.task_ids` is set in checkpoint)
3. Calculate `available_slots = max_concurrent - current_in_progress_count`

**If in-scope ready tasks AND available_slots > 0:**
- Call `/dispatch <specific-task-ids> --no-plan --yes` via Skill tool (pass only in-scope IDs, limited to available_slots)
- Increment `batch_number` in checkpoint
- Add dispatched tasks to `in_progress` in checkpoint
- Check dispatch output for branch isolation failures (same logic as Section 2 step 4a):
  - Record failures in checkpoint, only count isolated workers as in_progress
  - Apply circuit breaker for repeated failures (attempts >= 2 → mark failed)

**Completion checks:**
- If `--through` target task is now closed → all done → go to Section 4 (Completion)
- If `--epic` and all epic children closed → all done → go to Section 4
- If no in-scope ready AND no in-progress → all done → go to Section 4
- If no in-scope ready BUT tasks still in-progress → wait for more completions (do nothing, Agent Teams will deliver the next message)

### Step E — Context Self-Monitoring

After every 3 reconciliation cycles, assess context health. If you notice degradation (losing track of state, responses feeling truncated, difficulty recalling earlier context):
1. Write checkpoint with `status: "running"` (preserving all current state)
2. Log: "Context limit approaching. Exiting for wrapper restart."
3. Exit gracefully — the wrapper script (if running) will restart with `--resume`

## Section 4: Completion

When no ready tasks AND no in-progress tasks (all work done):

1. **Final reconciliation:** Call `/reconcile-summary --yes` via Skill tool (WITHOUT `--no-cleanup` — this triggers team cleanup)

### Step 1.5: Milestone Review Phase

After reconciliation, run an iterative review-fix pass on accumulated branch changes:

1. If `--skip-milestone-review` was passed: skip, log "Milestone review skipped by flag"
2. Detect milestone branch:
   ```bash
   git branch -r --list 'origin/milestone/*' | sort -V | tail -1
   ```
3. If no milestone branch found: skip, log "No milestone branch found — skipping milestone review"
4. Update checkpoint: `milestone_review.status: "in_progress"`
5. Dispatch a review worker:
   - `mode: "bypassPermissions"`
   - Prompt: Check out the milestone branch, run `/milestone-review --max-iterations <N> --base-branch main` (use `--milestone-review-iterations` value or default 5)
   - The worker pushes fixes directly to the milestone branch (no separate PR — the milestone-to-main PR is the human review checkpoint)
6. Wait for worker completion (event-driven, same as main loop)
7. Read the worker's report/session summary
8. Update checkpoint: `milestone_review.status: "completed"` with stats from the worker's report

2. **Write checkpoint** with `status: "completed"` and final stats
3. **Final report:**

```
═══════════════════════════════════════════
AUTO-RUN COMPLETE
═══════════════════════════════════════════
Duration: <elapsed time>
Batches: <count>
Completed: <count> tasks
Failed: <count> tasks
Branch Isolation Failures: <count> (isolation failures across all batches)

MILESTONE REVIEW:
- Status: <completed|skipped|N/A>
- Iterations: <count>
- Findings fixed: <count>
- Findings deferred: <count> (needs human decision)

COMPLETED:
- <task-id>: <title>
- ...

FAILED:
- <task-id>: <title> — <reason>
- ...

REMAINING (if any):
- <task-id>: <title>
- ...

═══════════════════════════════════════════
```

4. Run `bd list` and `bd ready` to show final board state.

## Checkpoint Schema

File: `docs/auto-run-checkpoint.json`

```json
{
  "version": 1,
  "status": "running|completed|paused|errored",
  "start_time": "ISO8601",
  "last_updated": "ISO8601",
  "config": {
    "max_batches": null,
    "max_hours": null,
    "max_concurrent": 3
  },
  "scope": {
    "mode": "all|through|epic|only",
    "target": "Proj-xyz",
    "task_ids": ["Proj-abc", "Proj-def", "Proj-xyz"]
  },
  "batch_number": 2,
  "session_count": 1,
  "tasks": {
    "completed": [{ "id": "Proj-abc", "title": "...", "completed_at": "...", "batch": 1 }],
    "failed": [{ "id": "Proj-xyz", "title": "...", "reason": "...", "attempts": 1 }],
    "in_progress": [{ "id": "Proj-def", "title": "...", "dispatched_at": "...", "batch": 2 }],
    "branch_isolation_failures": [{ "id": "Proj-abc", "title": "...", "batch": 2, "attempts": 1 }]
  },
  "stats": {
    "total_dispatched": 4,
    "total_completed": 1,
    "total_failed": 0,
    "total_batches": 2,
    "total_branch_isolation_failures": 0
  },
  "milestone_review": {
    "status": "pending|in_progress|completed|skipped",
    "iterations": 0,
    "findings_fixed": 0,
    "findings_deferred": 0
  }
}
```

## Error Handling

- **Failed tasks**: Create investigation tasks in beads, picked up in next dispatch cycle
- **Circuit breaker**: Same task failing twice → skip and flag for human attention
- **Stuck teammates**: Send 1 follow-up message, then mark failed if no response
- **No beads CLI**: Exit with clear error — `bd` must be available
- **Checkpoint corruption**: If checkpoint can't be parsed, start fresh (warn user)
- **Branch isolation fails**: `/dispatch` shuts down workers that didn't create task branches and unassigns their tasks. Auto-run records failures in checkpoint `branch_isolation_failures`. Same task failing isolation twice triggers circuit breaker — moved to `failed` list and flagged for human attention.
