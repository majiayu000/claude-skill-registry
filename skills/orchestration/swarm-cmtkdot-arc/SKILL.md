---
name: swarm
description: Use when many beads are independent and file conflicts are rare. No lead agent needed — workers self-coordinate through shared bead state.
invocation: agent
---

# Swarm

Parallel execution model that identifies independent beads and spawns workers to process them concurrently. Swarm maximizes throughput when the dependency graph has wide parallelism. Unlike team mode, swarm has no lead agent — workers self-coordinate through the shared bead state.

## Invocation Contract

Inputs:
- Bead graph with dependency states
- Worker limit and execution constraints

Outputs:
- Parallel task assignments and transitions
- Completion summary with throughput and blockers

## Execution Cycle

1. **Identify ready beads** — Scan for all beads in `pending` state whose dependencies are fully `closed`. These are the "ready set."

2. **Spawn workers** — Launch workers up to the configured limit (default: 3). Each worker claims one ready bead by transitioning it to `in_progress`. No two workers may claim the same bead.

3. **Track completion** — As workers finish beads (transition to `closed`), check whether their completion unblocks downstream beads. Add newly unblocked beads to the ready set.

4. **Replenish queue** — When a worker finishes, immediately assign it the next ready bead if one exists. Continue until the ready set is empty and all workers are idle.

5. **Enforce exit criteria** — After the last bead closes, run plan-level exit criteria commands. Swarm is complete only when all exit criteria pass.

## Conflict Prevention

Since workers run in parallel without a coordinator, file conflicts must be prevented by design:

- **Disjoint files**: Beads that touch entirely different files can safely run in parallel. This is the common case when beads are well-decomposed.
- **Shared files**: If two ready beads touch the same file, serialize them — only one enters the ready set; the other waits. Flag this as a dependency gap in the bead decomposition.
- **Build artifacts**: Workers must not run build/compile steps concurrently unless the build system supports parallel compilation. Serialize verification steps that share build output.

### Detection mechanism

Before claiming a ready bead, each worker must:

1. Read the bead's declared file touch-points (files it creates or modifies).
2. Check all `in_progress` beads for overlapping file touch-points.
3. If overlap exists, skip the bead and move to the next ready bead in the queue.
4. If no non-overlapping bead is available, wait for an `in_progress` bead to close before retrying.

This is a best-effort mechanism that depends on accurate file touch-points in bead descriptions. If beads have incomplete or inaccurate file declarations, conflicts may still occur.

**Important**: Swarm mode assumes predominantly disjoint files. If your bead set has significant shared-file overlap, use **team mode** instead — the lead agent provides explicit serialization and conflict resolution that swarm cannot.

## Coordination Primitives

Swarm workers self-coordinate through Beads state rather than a lead agent:

- **Self-assignment**: Use `bd slot` to atomically claim the next available bead. This is the preferred swarm primitive — it combines lock + claim in one operation, avoiding the two-step race condition of `bd lock` + `bd update --claim`.
- **Gate integration**: Gate beads (`bd gate create`) are external blockers managed by humans or CI. Workers treat them as dependency blockers — report pending gates in progress updates but never attempt to close them.

## Stale Bead Detection

Before entering the execution cycle, run the Standard Recovery Procedure from `beads-schema` > Recovery Semantics:
1. Process crash markers from `<repo-root>/.arc/crashes/`.
2. Detect and reset stale `in_progress` beads (threshold: `ARC_STALE_THRESHOLD`, default 600s).
3. Report recovered beads. Skip silently if none.

See `beads-schema` for crash marker protocol, staleness configuration, and cleanup contract.

## Worktree Isolation

When `--worktree` is enabled via `/arc:core:execute`, each worker gets a dedicated git worktree instead of sharing the main working directory.

### How it changes swarm behavior

- **Full filesystem isolation**: Each worker operates in `<worktree-root>/<bead-id>/` on branch `arc/<bead-id>`. No shared working directory means no file conflicts between concurrent workers.
- **Conflict detection becomes unnecessary**: The touch-point overlap check (steps 1-4 in Detection mechanism above) is skipped — workers cannot interfere with each other's files.
- **All ready beads can run in parallel**: Without file overlap constraints, the ready set is limited only by the worker count, not by shared files.

### Worktree lifecycle in swarm

1. **Create**: Before a worker claims a bead, create its worktree per the `worktree` skill: `git worktree add -b arc/<bead-id> <worktree-root>/<bead-id> <baseline>`.
2. **Execute**: The worker runs entirely inside its worktree directory.
3. **Merge back**: After a bead's verification passes, merge its branch into the baseline in dependency order. Only one merge-back runs at a time.
4. **Cleanup**: Remove the worktree and delete the branch after successful merge.

### Merge conflicts

If a merge conflict occurs during merge-back, the bead transitions to `blocked` with reason "merge conflict" and surfaces to the user. Other workers continue on their independent beads. The conflict must be resolved before downstream beads that depend on the blocked bead can proceed.

## Error Handling

- **Worker failure**: If a worker's verification fails, that worker pauses and diagnoses. Other workers continue on their independent beads. The failed bead remains `in_progress` until fixed.
- **Deadlock**: If no beads are ready but unclosed beads remain, report the blocked beads and their reasons. Stop the swarm.
- **Infrastructure failure**: If a system-level issue affects all workers, pause the swarm and report.
- **Zombie beads**: Follow the canonical zombie handling procedure in `beads-schema` > Zombie Beads (skip, block, log).

## Progress Reporting

After each bead completes, report:
- Active worker count and their current beads
- Completed bead count / total bead count
- Ready set size (beads available for next workers)

## When to Use Swarm vs. Other Execution Modes

- **Loop** — Sequential. Use when beads are tightly dependent or count is small.
- **Swarm** — Parallel without lead. Use when many beads are independent and file conflicts are rare.
- **Team** — Parallel with lead coordination. Use when shared-file conflicts are expected or TDD ordering requires cross-bead coordination.

## Related Skills

- `beads-schema` defines the bead structure consumed by swarm.
- `plan-schema` defines the exit criteria that terminate the swarm.
- `worktree` defines the worktree lifecycle when `--worktree` is enabled.
- `loop` and `team` are alternative execution models.
