---
name: beads-schema
description: Use when creating, validating, or decomposing beads. Defines required fields, state model, granularity guidelines, and valid transitions.
invocation: agent
---

# Beads Schema

Define and enforce the required structure for Arc beads. A bead is the smallest self-contained unit of work that can be independently executed, verified, and tracked. Plans decompose into beads; execution skills (loop, swarm, team) consume beads.

## Invocation Contract

Inputs:
- OpenSpec change/task context
- Existing bead list (if updating)

Outputs:
- Bead definitions with required fields
- Validation decision (pass/fail with missing fields)

## Required Fields

Every bead must include:

### Objective

A single sentence describing what this bead accomplishes. Must be verifiable — "Add input validation to the login form" not "Improve the login form."

### Files and Touch Points

Exact list of files to create, modify, or delete. For modifications, specify which functions, classes, or sections are affected. This enables conflict detection in parallel execution and accurate progress tracking.

### Dependency Links

Explicit references to other beads that must complete before this one can start. Use bead IDs: "depends on bead-003, bead-004." If a bead has no dependencies, mark it explicitly as independent. The dependency graph feeds directly into execution scheduling.

### Verification Commands

Concrete, runnable commands that prove the bead's objective is met:
- Unit test commands with expected outcomes
- Type-check or lint commands for the affected files
- Build verification if applicable

Never use vague verification like "check it works." Specify: `pytest tests/test_login.py::test_input_validation -v`.

### Traceability

Link back to the OpenSpec change or task that this bead implements. Format: `spec: change-007/task-02`. This enables audit trails and progress reporting against the specification.

### Spec ID

Machine-readable identifier set via `--spec-id` on `bd create`. Distinct from the human-readable `spec:` traceability link above.

- Format: `openspec/changes/<name>/tasks.md#<task-id>`
- Set on every bead: `bd create --spec-id "openspec/changes/<name>/tasks.md#<task-id>"`
- Enables filtering: `bd list --spec "openspec/"` to see all beads for a change
- Epic beads use the tasks.md path without a fragment: `--spec-id "openspec/changes/<name>/tasks.md"`

## State Model

Beads transition through these states:

- **pending** — Not yet started. All beads begin here.
- **in_progress** — Actively being worked on by a worker or the loop executor.
- **blocked** — Cannot proceed because a dependency has not completed or an external issue prevents progress. Must include a reason.
- **closed** — Objective met and verification passed. Terminal state.

Valid transitions:
- `pending` to `in_progress` (claimed by a worker)
- `in_progress` to `closed` (verification passed)
- `in_progress` to `blocked` (dependency or external blocker found)
- `blocked` to `in_progress` (blocker resolved)

Invalid transitions:
- `pending` to `closed` (must pass through in_progress)
- `closed` to any state (terminal, no transitions out)

### Zombie Beads

Content-addressed storage can resurrect previously deleted beads into the ready queue. All execution modes must handle zombies identically:

1. Before processing any bead from `bd ready`, verify its `spec_id` and label match the active spec (or team ledger in team mode).
2. Beads not matching are zombies from prior runs or deleted specs.
3. **Skip** the zombie — do not assign it to workers or attempt execution.
4. **Block** the zombie to prevent re-surfacing: `bd update <zombie-id> --status blocked --notes "Zombie: spec_id mismatch, not in active scope"`
5. **Log** skipped zombie bead IDs for operator review.

This is the canonical behavior. Loop, swarm, and team all follow this procedure — skip, block, log.

## Recovery Semantics

Canonical recovery procedure for all execution modes (loop, swarm, team). Run on execution startup before entering the main cycle.

### Staleness Threshold

Beads stuck in `in_progress` beyond the staleness threshold are presumed abandoned and reset to `pending`.

- **Default**: 600 seconds (10 minutes)
- **Override via env**: `ARC_STALE_THRESHOLD=<seconds>` (e.g., `ARC_STALE_THRESHOLD=1800` for 30-minute beads)
- **Override via config**: `.arc/config.json` field `stale_threshold` (seconds)
- **Resolution order**: env var > config file > default (600)

**Important**: Without a heartbeat mechanism, any bead whose worker is legitimately running but hasn't called `bd update` or `bd close` will appear stale after the threshold. Set the threshold conservatively for your project's longest expected bead duration. A future heartbeat mechanism (periodic `bd update <id> --notes "heartbeat:<ISO-8601>"`) would decouple legitimate long-running work from abandoned beads.

### Standard Recovery Procedure

1. **Process crash markers**: Check `<repo-root>/.arc/crashes/` for marker files. For each marker:
   - Reset the bead: `bd update <bead-id> --status pending --notes "Recovered from crash: <error>"`
   - Only after confirming the reset succeeded, remove the marker file
   - If `bd update` fails, leave the marker in place for the next recovery cycle
2. **Detect stale beads**: Query `bd list --status in_progress --json`. Compare each bead's `updated_at` against `now - $ARC_STALE_THRESHOLD`. Beads older than the threshold are stale.
3. **Reset stale beads**: `bd update <id> --status pending --notes "Reset: stale in_progress (no update >${ARC_STALE_THRESHOLD}s)"`
4. **Report**: Log all recovered beads before entering the main execution cycle. Skip silently if none.

### Crash Marker Protocol

When a worker encounters an unrecoverable error and `bd update` itself fails:

1. **Write path**: Always `<repo-root>/.arc/crashes/<bead-id>.json`, where `<repo-root>` is the directory containing `.beads/`. In worktree mode, this is the **main repo root**, NOT the worktree directory. Workers must resolve the repo root before writing.
2. **Schema**: `{"bead_id":"<id>","error":"<msg>","timestamp":"<ISO-8601>","worktree_path":"<path-or-null>"}`
3. **Read path**: Recovery always checks `<repo-root>/.arc/crashes/` — one location regardless of worktree configuration.
4. **Cleanup contract**: The sequence is strictly ordered:
   a. `bd update <id> --status pending --notes "Recovered from crash: <error>"`
   b. Confirm the update succeeded (check exit code)
   c. `rm .arc/crashes/<id>.json`
   Never remove a marker without confirming the bead state was actually reset. If step (a) fails, leave the marker for the next recovery cycle.

## Gate Beads

Gate beads are non-implementable approval checkpoints that participate in the dependency graph. Downstream beads block until the gate closes.

- Create: `bd gate create --type human --label review:<change-id>`
- Types: `human` (manual approval required), `ci` (automated check)
- Gates have no implementation code — they exist solely as dependency blockers
- Close a gate: the gate owner (human or CI) marks it closed; dependent beads unblock automatically

## Bead Types

- **Standard beads** — Default `bd create`. Single unit of implementable work.
- **Formula beads** (v0.34+) — `bd pour <formula>` for atomic set creation. Creates multiple beads from a template in one operation.
- **Molecules** (v0.34+) — Persistent work graphs for epic+child patterns. Group related beads under a parent that tracks aggregate progress.
- **Wisps** (v0.34+) — Ephemeral workflows for CI/CD experiments. Auto-delete after completion or expiry.

## Coordination Primitives

### bd lock

Exclusive lock for parallel execution safety.

- **Acquire**: `bd lock <id>` — fails immediately if another worker holds the lock.
- **TTL**: Locks expire after the staleness threshold (`ARC_STALE_THRESHOLD`, default 600s). A lock held past its TTL is considered abandoned and can be acquired by another worker.
- **Release**: `bd lock release <id>` — explicit release. Workers MUST release locks on both success and failure paths.
- **Implicit release**: `bd close <id>` and `bd update <id> --claim` both release any held lock on the bead as a side effect.
- **Crash behavior**: Unreleased locks past TTL are cleaned up during the Standard Recovery Procedure. No manual intervention needed.

### bd pin

Explicit assignment in team mode.

- `bd pin <id> --worker <name>` — the lead pins beads to specific workers for deterministic scheduling.
- Pinning does NOT acquire a lock. The assigned worker must still `bd lock <id>` before starting work.
- Pinned beads appear only in the assigned worker's queue.

### bd slot

Atomic self-claiming in swarm mode.

- `bd slot` — worker requests the next available bead. Beads selects and assigns one atomically (lock + claim in one operation).
- Preferred over `bd lock` + `bd update --claim` in swarm mode because it eliminates the two-step race.
- NOT for use in team mode — bypasses lead coordination.

### Primitive Composition

| Mode | Claim mechanism | Why |
|------|----------------|-----|
| **Loop** | `bd update <id> --claim` | Single executor, no contention. No lock needed. |
| **Swarm** | `bd slot` | Atomic self-assignment. Avoids lock-then-claim gap. |
| **Team** | `bd lock <id>` then `bd update <id> --claim`, with `bd lock release <id>` on claim failure | Lead coordinates via `bd pin`; worker locks for execution safety. |

Invalid combinations:
- `bd slot` + `bd lock` on the same bead (double-lock)
- `bd pin` + `bd slot` on the same bead (assignment conflict — pin is for team, slot is for swarm)
- `bd lock` without subsequent `bd update --claim` or `bd lock release` (orphaned lock)

## Granularity Guidelines

A well-sized bead:
- Touches 1-3 files (not 10+)
- Completes in a single focused work session
- Has a verification command that runs in under 30 seconds
- Can be described in one sentence

Split a bead if it touches more than 3 files, requires multiple unrelated changes, or has verification that depends on other beads' changes being present.

Merge beads if two beads touch the same file for the same logical change and neither can be verified independently.

## Related Skills

- `plan-schema` defines the plan that beads decompose from.
- `loop` executes beads sequentially.
- `swarm` executes independent beads in parallel.
- `team` executes beads with coordinated multi-agent workers.
