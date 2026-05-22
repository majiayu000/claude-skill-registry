---
name: agile-coordinator
description: "Orchestrate multiple worker agents to implement groomed tasks. Use when multiple ready tasks need implementation, when you want autonomous multi-task execution, or when coordinating batch development work. Keywords: coordinator, orchestrator, multi-task, parallel, workers, batch, autonomous."
license: MIT
compatibility: Requires git, GitHub CLI (gh), context network with backlog structure, and Claude Code's Task tool.
metadata:
  author: agent-skills
  version: "1.0"
  domain: agile-software
  type: orchestrator
  mode: generative
  orchestrates:
    - agile-workflow
  maturity: developing
---

# Agile Coordinator

Orchestrates multiple worker agents to implement groomed tasks from the backlog, handling task assignment, progress monitoring, merge coordination, and verification.

## Core Principle

**Coordinate, don't implement.** The coordinator assigns tasks to workers, monitors their progress, coordinates merges, and verifies results. Workers execute the actual implementation via the `agile-workflow` skill.

## Quick Reference

### When to Use
- Multiple ready tasks in the backlog need implementation
- You want autonomous batch execution of development work
- You need coordinated merges to avoid conflicts
- You want progress tracking across multiple tasks

### Invocation

```bash
/agile-coordinator                    # Auto-discover and execute ready tasks
/agile-coordinator TASK-001 TASK-002  # Execute specific tasks
/agile-coordinator --dry-run          # Preview execution plan only
/agile-coordinator --parallel         # Run workers in parallel
/agile-coordinator --sequential       # Run workers one at a time (default)
```

### Flags

| Flag | Description | Default |
|------|-------------|---------|
| `--sequential` | Execute tasks one at a time | Yes |
| `--parallel` | Execute tasks concurrently | No |
| `--max-workers N` | Maximum concurrent workers | 2 |
| `--dry-run` | Show plan without executing | No |
| `--autonomous` | Auto-continue at all checkpoints | Yes |
| `--supervised` | Pause after each task completes | No |
| `--verbose` | Show all worker updates | No |
| `--summary-only` | Show major milestones only | Yes |

---

## Workflow Phases

### Phase 1: Discovery

Read the backlog to find tasks ready for implementation.

```
Actions:
1. Read context/backlog/ for task files
2. Filter to status: ready
3. Parse task metadata (priority, size, dependencies)
4. Sort by priority (high → medium → low)
5. Present findings

Output: List of ready tasks with metadata
```

### Phase 2: Planning

Create an execution plan based on task characteristics.

```
Actions:
1. Determine execution mode (sequential or parallel)
2. Check for task dependencies (A must complete before B)
3. Assign tasks to workers in priority order
4. Generate worker instructions

Output: Execution plan with task assignments
```

**Checkpoint: TASKS_DISCOVERED**
- Display: Ready tasks and proposed execution plan
- Auto-continue: If --autonomous flag and tasks found
- Options: `continue`, `reorder`, `exclude [TASK-ID]`, `stop`

### Phase 3: Execution

Spawn and monitor worker agents.

```
For SEQUENTIAL mode:
  for each task in queue:
    1. Spawn worker with Task tool
    2. Worker runs agile-workflow for the task
    3. Monitor progress via file system
    4. When complete: proceed to merge phase
    5. On failure: handle error, decide continue/stop

For PARALLEL mode:
  1. Spawn workers up to max_workers
  2. Monitor all workers concurrently
  3. As workers complete: queue their PRs for merge
  4. Spawn next worker if tasks remain
  5. Continue until all tasks processed
```

**Checkpoint: WORKER_COMPLETE** (per worker)
- Display: Worker summary, PR number, next action
- Auto-continue: If successful and --autonomous
- Options: `continue`, `retry`, `skip`, `stop`

### Phase 4: Merging

Execute merges sequentially to avoid conflicts.

```
Actions:
1. For each completed PR in merge queue:
   a. git checkout main && git pull
   b. Merge PR (via gh pr merge or git merge)
   c. Verify merge succeeded
   d. Delete feature branch
2. If conflict: pause and alert user

Output: All PRs merged to main
```

### Phase 5: Verification

Verify system integrity after all merges.

```
Actions:
1. git checkout main && git pull --rebase
2. npm run build (verify build passes)
3. npm test (run full test suite)
4. Check for regressions
5. Generate verification report

Output: Verification status (PASSED/FAILED)
```

**Checkpoint: VERIFIED**
- Display: Test results, build status
- Auto-continue: If all tests pass
- Options: `done`, `investigate`, `revert`

### Phase 6: Summary

Generate comprehensive completion report.

```
Output:
- Tasks completed with PR numbers and commits
- Metrics (workers spawned, PRs merged, tests added)
- Verification status
- Remaining backlog tasks
```

---

## Worker Protocol

Workers are spawned using Claude Code's Task tool and run `agile-workflow` for their assigned task.

### Worker Instruction Template

See [templates/worker-instruction.md](templates/worker-instruction.md)

Key requirements for workers:
1. Run `agile-workflow` with autonomous mode
2. Write progress to `.coordinator/workers/{worker-id}/progress.json`
3. Do NOT self-merge - signal ready-to-merge status instead
4. Handle all agile-workflow checkpoints automatically

### Progress Tracking

Workers report progress via file system:

```json
// .coordinator/workers/worker-1/progress.json
{
  "worker_id": "worker-1",
  "task_id": "TASK-006",
  "status": "in_progress|completed|failed|ready-to-merge",
  "phase": "implement|review|pr-prep|pr-complete",
  "pr_number": null,
  "branch": "task/TASK-006-description",
  "last_update": "2026-01-20T10:15:00Z",
  "milestones": [
    {"phase": "implement", "timestamp": "..."},
    {"phase": "review", "timestamp": "..."}
  ]
}
```

---

## State Tracking

The coordinator maintains state in `.coordinator/state.json`:

```json
{
  "session_id": "coord-2026-01-20-abc123",
  "state": "EXECUTING",
  "config": {
    "execution_mode": "sequential",
    "autonomy_level": "autonomous"
  },
  "tasks": {
    "queued": ["TASK-008"],
    "in_progress": ["TASK-007"],
    "completed": ["TASK-006"],
    "failed": []
  },
  "workers": [...],
  "merge_queue": [],
  "verification": null
}
```

See [references/state-tracking.md](references/state-tracking.md) for details.

---

## Failure Handling

| Failure Type | Detection | Recovery |
|--------------|-----------|----------|
| Worker fails | Progress shows `failed` | Offer retry, skip, or abort |
| Tests fail | npm test exits non-zero | Worker retries up to 2x |
| Merge conflict | git merge fails | Pause, alert user |
| Verification fails | Post-merge tests fail | Offer investigate or revert |

See [references/failure-handling.md](references/failure-handling.md) for details.

---

## Integration with agile-workflow

The coordinator spawns workers that execute `agile-workflow`:

```
agile-coordinator (orchestrator)
    │
    ├── Worker 1 → agile-workflow --task TASK-006
    ├── Worker 2 → agile-workflow --task TASK-007
    └── Worker 3 → agile-workflow --task TASK-008
```

Key integration points:
- Workers run agile-workflow in autonomous mode
- Coordinator handles merges (workers create PRs but don't merge)
- Progress synced via file system
- Coordinator runs verification after all merges

---

## Anti-Patterns

### AP1: Parallel Merges
**Pattern**: Merging multiple PRs simultaneously
**Problem**: Creates merge conflicts, corrupts main branch
**Fix**: Always merge sequentially, pull before each merge

### AP2: Worker Self-Merge
**Pattern**: Workers merge their own PRs
**Problem**: Race conditions, uncoordinated merges
**Fix**: Workers signal ready-to-merge, coordinator executes merges

### AP3: No Verification
**Pattern**: Skipping post-merge verification
**Problem**: Regressions go undetected
**Fix**: Always run full test suite after merges complete

---

## Example Interaction

```
User: /agile-coordinator

Coordinator: Discovering ready tasks...

Found 2 ready tasks:
1. TASK-006 - Persistent Message Status (medium priority, medium size)
2. TASK-007 - Add Unit Tests (high priority, large size)

Execution Plan:
- Mode: sequential
- Order: TASK-006 → TASK-007

Proceed? [continue/reorder/stop]

User: continue

Coordinator: Starting TASK-006...
[Spawns Worker 1]

**Milestone**: TASK-006 - PR #123 created, CI passing

Coordinator: Merging PR #123...
**Milestone**: TASK-006 complete (commit abc123)

Coordinator: Starting TASK-007...
[Spawns Worker 2]

**Milestone**: TASK-007 - PR #124 created, CI passing

Coordinator: Merging PR #124...
**Milestone**: TASK-007 complete (commit def456)

Coordinator: Running verification...
- Build: PASSED
- Tests: 47/47 passing
- Coverage: 82%

## Summary
Tasks completed: 2
- TASK-006: PR #123 merged (commit abc123)
- TASK-007: PR #124 merged (commit def456)

Verification: PASSED
```

---

## Integration Graph

### Inbound (From Other Skills)
| Source Skill | Trigger | Action |
|--------------|---------|--------|
| requirements-elaboration | Tasks groomed | Coordinator can execute |
| github-agile | Backlog ready | Coordinator discovers tasks |

### Outbound (To Other Skills)
| This Action | Triggers Skill | For |
|-------------|----------------|-----|
| Spawn worker | agile-workflow | Task implementation |
| Verification fails | research | Debug investigation |

### Complementary Skills
| Skill | Relationship |
|-------|--------------|
| agile-workflow | Workers execute this skill |
| github-agile | Manages backlog this reads |

---

## Design Constraints

- Requires Claude Code's Task tool for spawning workers
- Workers cannot directly communicate with each other
- File system used for progress coordination
- Sequential merges only (parallel merges disabled)
- Assumes context network backlog structure

## What You Do NOT Do

- Implement tasks directly (workers do this)
- Merge PRs in parallel (always sequential)
- Skip verification (always verify after merges)
- Continue after critical failures without user consent
