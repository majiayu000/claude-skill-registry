---
name: team
description: Use when executing large plans with mixed dependencies, shared-file conflicts, or TDD ordering that requires lead coordination. Requires CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1.
invocation: agent
---

# Team

Coordinated multi-agent execution with a lead agent and self-claiming workers. Team mode is the most capable execution model — use it for large plans with mixed dependencies, shared-file conflicts, or when TDD ordering requires cross-bead coordination.

## Invocation Contract

Inputs:
- Bead-derived task graph
- Team mode environment (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`)

Outputs:
- Coordinated lead/worker execution plan
- Team completion report with dependency and gate status

**Prerequisite**: Set `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` in the environment.

## Roles

### Lead Agent

The lead coordinates but never implements. Responsibilities:
- Translate bead dependencies into task dependencies
- Assign initial task priorities
- Monitor worker progress and health
- Resolve conflicts between workers (shared files, merge issues)
- Enforce TDD ordering across the task graph
- Run final exit criteria after all tasks close

### Workers

Workers implement but never coordinate. Responsibilities:
- Self-claim the highest-priority unblocked task
- Implement the bead's objective within its declared file scope
- Run verification commands and report results
- Report blockers immediately rather than attempting workarounds

## Coordination Primitives

Team mode uses explicit coordination through Beads primitives:

- **Bead locking**: Workers must `bd lock <id>` before claiming any bead. This is mandatory in team mode (unlike loop where it's unnecessary). Lock failure means another worker claimed it — move to the next available task.
- **Worker assignment**: The lead uses `bd pin <id> --worker <name>` for deterministic bead assignment. Pinned beads appear only in the assigned worker's queue.
- **Gate beads**: The lead creates gate beads (`bd gate create --type human --label review:<change-id>`) as review checkpoints. Workers see gates as dependency blockers — they cannot proceed past a gate until the lead or a human closes it.

## TDD Ordering

Enforce test-driven development ordering across the task graph:

1. **Test beads first** — Beads that create or modify test files execute before their corresponding implementation beads.
2. **Implementation beads second** — Beads that implement features execute after their test beads close.
3. **Non-testable beads last** — Configuration, documentation, or infrastructure beads that cannot be test-driven execute after the core implementation is stable.

The lead must identify and enforce this ordering even when the original bead dependency graph does not explicitly encode it.

## Resilience

### Crashed Worker

If a worker becomes unresponsive (no progress beyond `ARC_STALE_THRESHOLD` seconds, default 600 — see `beads-schema` > Recovery Semantics):
1. Mark the worker's current task as `blocked` with reason "worker crashed."
2. Spawn a replacement worker.
3. The replacement claims the blocked task or the next available one.

On startup, the lead runs the Standard Recovery Procedure from `beads-schema` > Recovery Semantics, including crash marker processing and stale bead detection.

### Idle Worker

If a worker reports no available work but unclosed tasks remain:
1. Check for tasks the idle worker could unblock by completing prerequisite work.
2. If genuinely no work is available, the worker waits or is released.
3. Nudge idle workers with newly unblocked tasks as they become available.

### Shared-File Conflicts

When two workers need to modify the same file:
1. The lead serializes access — only one worker modifies the file at a time.
2. The second worker waits or works on a different task.
3. After the first worker closes its task, the second worker pulls the latest state before proceeding.

### Worktree Isolation

When `--worktree` is enabled via `/arc:core:execute`, the lead creates worktrees per worker at execution startup, providing full filesystem isolation.

**Setup**: The lead creates a worktree for each bead before assigning it: `git worktree add -b arc/<bead-id> <worktree-root>/<bead-id> <baseline>`. Workers are assigned worktree paths via the team ledger (`worktree_path` and `worktree_branch` fields). The worktree root is resolved via the `worktree` skill's directory selection process and may be project-local (`.worktrees/`) or external (`../project.worktrees/`).

**Worker isolation**: Each worker operates entirely within its assigned worktree directory. Shared-file serialization (described above) becomes unnecessary — each worker has full isolation.

**Merge-back ordering**: The lead manages merge-back after each bead's verification passes. TDD ordering is respected: test branches merge before implementation branches. Only one merge-back runs at a time.

**Conflict handling**: If a merge conflict occurs during merge-back, the lead pauses the conflicting bead (status `blocked`, reason "merge conflict") and surfaces it to the user. Other workers continue unaffected.

### All Tasks Blocked

If all remaining tasks are in `blocked` state:
1. The lead reports the deadlock with blocking reasons for each task.
2. Preserve all state for debugging.
3. Stop execution and surface the issue to the user.

### Zombie Bead Handling

Follow the canonical procedure from `beads-schema` > Zombie Beads:
1. Check `spec_id` and label for every bead from `bd ready`. In team mode, also verify presence in the team ledger.
2. Skip, block (`bd update <zombie-id> --status blocked --notes "Zombie: not in active scope"`), and log zombie bead IDs.

See `beads-schema` for the full protocol.

## When to Use Team vs. Other Execution Modes

- **Loop** — Sequential. Use for small plans or tight linear dependencies.
- **Swarm** — Parallel without coordination. Use when beads are independent and file conflicts are rare.
- **Team** — Parallel with lead coordination. Use for large plans, shared-file scenarios, or when TDD ordering enforcement is needed.

## Team Ledger Schema

The lead creates `.arc/team-ledger.json` at execution startup. This file is the shared state between the lead, workers, and team hooks.

```json
{
  "tasks": {
    "<bead-id>": {
      "objective": "<string>",
      "depends_on": ["<bead-id>"],
      "assigned_to": "<worker-name>" | null,
      "status": "pending" | "blocked" | "in_progress" | "completed",
      "completion_gate_commands": ["<shell command>"],
      "verification": "<human-readable description>",
      "gate_status": null | "passed" | "failed" | "retrying",
      "completed_at": null | "<ISO-8601>",
      "file_touch_points": ["<file-path>"],
      "worktree_path": "<worktree-root>/<bead-id>" | null,
      "worktree_branch": "arc/<bead-id>" | null
    }
  },
  "created_at": "<ISO-8601>",
  "source_change": "<openspec-change-id>"
}
```

Field semantics:
- `depends_on`: Bead IDs that must be `completed` before this task is workable.
- `status`: `blocked` = has unmet deps; `pending` = ready to claim; `in_progress` = claimed by a worker; `completed` = done and gated.
- `completion_gate_commands`: Shell commands the `team-phase-gate` hook runs on task completion.
- `file_touch_points`: Files this task modifies. Used by the idle gate and swarm conflict detection.
- `gate_status`: Set by the phase gate hook after running gate commands.
- `worktree_path`: Worktree directory for this task. Set when `--worktree` is enabled; `null` otherwise.
- `worktree_branch`: Git branch for this task's worktree. Set when `--worktree` is enabled; `null` otherwise.

The ledger is created by `/arc:core:execute --mode team` and consumed by `team-idle-gate.sh` and `team-phase-gate.sh`.

## Related Skills

- `beads-schema` defines the bead structure that tasks are created from.
- `plan-schema` defines the exit criteria the lead enforces.
- `worktree` defines the worktree lifecycle when `--worktree` is enabled.
- `loop` and `swarm` are simpler execution alternatives.
