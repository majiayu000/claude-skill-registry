---
name: swarm
description: Dispatch parallel agents.
practices:
- microservices
- team-topologies
- mythical-man-month
hexagonal_role: supporting
consumes:
- implement
- vibe
produces:
- .agents/swarm/results/*.json
context_rel:
- kind: customer-of
  with: crank
skill_api_version: 1
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude:
    - HISTORY
  intel_scope: full
metadata:
  tier: orchestration
  dependencies:
  - implement
  - vibe
output_contract: .agents/swarm/results/*.json
---
# Swarm Skill

Spawn isolated agents to execute tasks in parallel. Fresh context per agent (Ralph Wiggum pattern).

## Loop position

Move **5 (wave execution)** of the [operating loop](../../docs/architecture/operating-loop.md), specifically the parallel-fork primitive `/crank` invokes. Refuses to spawn parallel agents on a wave that has not cleared the wave-validity check in the [slice validation plan](../../docs/templates/slice-validation.md): write scopes must be disjoint, no shared migration/contract/CLI surface, integration order declared when it matters, one owner per slice, discard path per slice. Parallelism is explicit ownership, not swarm chaos. Default to sequential when the wave-validity rows are not all green.

**Integration modes:**
- **Direct** - Create TaskList tasks, invoke `/swarm`
- **Via Crank** - `/crank` creates tasks from beads, invokes `/swarm` for each wave

> **Requires multi-agent runtime.** Swarm needs a runtime that can spawn parallel subagents. If unavailable, work must be done sequentially in the current session.

## Architecture (Mayor-First)

```
Mayor (this session)
    |
    +-> Plan: TaskCreate with dependencies
    |
    +-> Identify wave: tasks with no blockers
    |
    +-> Select spawn backend (gc if available; runtime-native: Claude teams in Claude runtime, Codex sub-agents in Codex runtime; fallback tasks if unavailable)
    |
    +-> Assign: TaskUpdate(taskId, owner="worker-<id>", status="in_progress")
    |
    +-> Spawn workers via selected backend
    |       Workers receive pre-assigned task, execute atomically
    |
    +-> Wait for completion (wait() | SendMessage | TaskOutput)
    |
    +-> Validate: Review changes when complete
    |
    +-> Cleanup backend resources (close_agent | TeamDelete | none)
    |
    +-> Repeat: New team + new plan if more work needed
```

## Execution

Read [references/execution-steps.md](references/execution-steps.md) when you need the full procedural detail (Steps 0–6): backend detection, gc dispatch, task typing + file manifests, context briefing, manifest auto-population, advisory bead clustering, wave identification, pre-spawn conflict check, test-file naming validation, multi-wave base-SHA refresh, and worker dispatch.

Every TaskCreate **must** include `metadata.issue_type` plus a `metadata.files` array.
Do not spawn workers with overlapping file manifests into the same shared-worktree wave.

## Example Flow

```
Mayor: "Let's build a user auth system"

1. /plan -> Creates tasks:
   #1 [pending] Create User model
   #2 [pending] Add password hashing (blockedBy: #1)
   #3 [pending] Create login endpoint (blockedBy: #1)
   #4 [pending] Add JWT tokens (blockedBy: #3)
   #5 [pending] Write tests (blockedBy: #2, #3, #4)

2. /swarm -> Spawns agent for #1 (only unblocked task)

3. Agent #1 completes -> #1 now completed
   -> #2 and #3 become unblocked

4. /swarm -> Spawns agents for #2 and #3 in parallel

5. Continue until #5 completes

6. /vibe -> Validate everything
```

### Scope-Escape Protocol

When a worker discovers work outside their assigned scope, they MUST NOT modify files outside their file manifest. Instead, append to `.agents/swarm/scope-escapes.jsonl`:

```json
{"worker": "<worker-id>", "finding": "<description>", "suggested_files": ["path/to/file"], "timestamp": "<ISO8601>"}
```

For richer scope-escape narration (status classification, concrete next step, evidence), see [references/scope-escape-template.md](references/scope-escape-template.md). Use the template when a single-line JSONL entry is insufficient for the operator to act on.

The lead reviews scope escapes after each wave and creates follow-up tasks as needed.

## Key Points

- **Runtime-native local mode** - Auto-selects the native backend for the current runtime (gc pool, Claude teams, or Codex sub-agents)
- **Universal orchestration contract** - Same swarm behavior across Claude and Codex sessions
- **Pre-assigned tasks** - Mayor assigns tasks before spawning; workers never race-claim
- **Fresh worker contexts** - New sub-agents/teammates per wave preserve Ralph isolation
- **Wave execution** - Only unblocked tasks spawn
- **Mayor orchestrates** - You control the flow, workers write results to disk
- **Thin results** - Workers write `.agents/swarm/results/<id>.json`, orchestrator reads files (NOT Task returns or SendMessage content)
- **Retry via message/input** - Use `send_input` (Codex) or `SendMessage` (Claude) for coordination only
- **Atomic execution** - Each worker works until task done
- **Graceful degradation** - If multi-agent unavailable, work executes sequentially in current session

## Workflow Integration

This ties into the full workflow:

```
/research -> Understand the problem
/plan -> Decompose into beads issues
/crank -> Autonomous epic loop
    +-- /swarm -> Execute each wave in parallel
/vibe -> Validate results
/post-mortem -> Extract learnings
```

**Direct use (no beads):**
```
TaskCreate -> Define tasks
/swarm -> Execute in parallel
```

The knowledge flywheel captures learnings from each agent.

## Task Management Commands

```
# List all tasks
TaskList()

# Mark task complete after notification
TaskUpdate(taskId="1", status="completed")

# Add dependency between tasks
TaskUpdate(taskId="2", addBlockedBy=["1"])
```

## Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--max-workers=N` | Max concurrent workers | 5 |
| `--from-wave <json-file>` | Load wave from OL hero hunt output (see OL Wave Integration) | - |
| `--per-task-commits` | Commit per task instead of per wave (for attribution/audit) | Off (per-wave) |

## When to Use Swarm

| Scenario | Use |
|----------|-----|
| Multiple independent tasks | `/swarm` (parallel) |
| Sequential dependencies | `/swarm` with blockedBy |
| Mix of both | `/swarm` spawns waves, each wave parallel |

## Why This Works: Ralph Wiggum Pattern

Follows the [Ralph Wiggum Pattern](https://ghuntley.com/ralph/): **fresh context per execution unit**.

- **Wave-scoped worker set** = spawn workers -> execute -> cleanup -> repeat (fresh context each wave)
- **Mayor IS the loop** - Orchestration layer, manages state across waves
- **Workers are atomic** - One task, one spawn, one result
- **TaskList as memory** - State persists in task status, not agent context
- **Filesystem for EVERYTHING** - Code artifacts AND result status written to disk, not passed through context
- **Backend messaging for signals only** - Short coordination signals (under 100 tokens), never work details

Ralph alignment source: `../shared/references/ralph-loop-contract.md`.

## Integration with Crank

When `/crank` invokes `/swarm`: Crank bridges beads to TaskList, swarm executes with fresh-context agents, crank syncs results back.

| You Want | Use | Why |
|----------|-----|-----|
| Fresh-context parallel execution | `/swarm` | Each spawned agent is a clean slate |
| Autonomous epic loop | `/crank` | Loops waves via swarm until epic closes |
| Just swarm, no beads | `/swarm` directly | TaskList only, skip beads |
| RPI progress gates | `/ratchet` | Tracks progress; does not execute work |

---

## OL Wave Integration

Read [references/ol-wave-integration.md](references/ol-wave-integration.md) when you invoke `/swarm --from-wave <json-file>` — covers pre-flight `ol` CLI check, input JSON format, task creation from wave entries, completion backflow via `ol hero ratchet`, and example flow.

---

## References

- **Executable acceptance:** [references/swarm.feature](references/swarm.feature) — wave-validity gate, fresh-context workers, conflict-free ownership, results+cleanup (soc-qk4b)
- **Local Mode Details:** `skills/swarm/references/local-mode.md`
- **Validation Contract:** `skills/swarm/references/validation-contract.md`

---

## Examples

### Building a User Auth System

**User says:** `/swarm`

**What happens:**
1. Agent identifies unblocked tasks from TaskList (e.g., "Create User model")
2. Agent selects spawn backend using runtime-native priority (Claude session -> Claude teams; Codex session -> Codex sub-agents)
3. Agent spawns worker for task #1, assigns ownership via TaskUpdate
4. Worker completes, team lead validates changes
5. Agent identifies next wave (tasks #2 and #3 now unblocked)
6. Agent spawns two workers in parallel for Wave 2

**Result:** Multi-wave execution with fresh-context workers per wave, zero race conditions.

### Direct Swarm Without Beads

**User says:** Create three tasks for API refactor, then `/swarm`

**What happens:**
1. User creates TaskList tasks with TaskCreate
2. Agent calls `/swarm` without beads integration
3. Agent identifies parallel tasks (no dependencies)
4. Agent spawns all three workers simultaneously
5. Workers execute atomically, report to team lead via SendMessage or task completion
6. Team lead validates all changes, commits once per wave

**Result:** Parallel execution of independent tasks using TaskList only.

---

## Worktree Isolation (Multi-Epic Dispatch)

Read [references/shared-checkout-discipline.md](references/shared-checkout-discipline.md) **first** when the target checkout (`~/dev/<repo>`) is shared with peer agents — it documents when worktrees are mandatory (vs. optional) and the three failure modes (branch-deletion data loss, swarm attribution confounded, destructive-recovery temptation) that motivate the discipline.

Read [references/worktree-isolation.md](references/worktree-isolation.md) when you need to dispatch workers across multiple epics or run waves with overlapping files — covers isolation semantics per backend, effort levels, post-spawn verification, manual worktree creation/routing/merge-back, the Merge Arbiter Protocol, cleanup, and the `--worktrees` / `--no-worktrees` parameters.

---

## Troubleshooting

Read [references/troubleshooting.md](references/troubleshooting.md) for full diagnostics.

| Problem | See |
|---------|-----|
| Worktree isolation did not engage | [references/troubleshooting.md](references/troubleshooting.md) |
| Workers produce file conflicts | [references/troubleshooting.md](references/troubleshooting.md) |
| Team creation fails | [references/troubleshooting.md](references/troubleshooting.md) |
| Codex agents unavailable | [references/troubleshooting.md](references/troubleshooting.md) |
| Workers timeout or hang | [references/troubleshooting.md](references/troubleshooting.md) |
| gc backend detected but workers unresponsive | [references/troubleshooting.md](references/troubleshooting.md) |
| Tasks assigned but workers never spawn | [references/troubleshooting.md](references/troubleshooting.md) |

## Reference Documents

- [references/shared-checkout-discipline.md](references/shared-checkout-discipline.md)
- [references/agent-genie-coordination-contract.md](references/agent-genie-coordination-contract.md) — Eight-field contract each parallel stream declares before claiming work- [references/conflict-recovery.md](references/conflict-recovery.md)
- [references/cold-start-contexts.md](references/cold-start-contexts.md)
- [references/backend-background-tasks.md](references/backend-background-tasks.md)
- [references/backend-claude-teams.md](references/backend-claude-teams.md)
- [references/backend-codex-subagents.md](references/backend-codex-subagents.md)
- [references/backend-inline.md](references/backend-inline.md)
- [references/claude-code-latest-features.md](references/claude-code-latest-features.md)
- [references/execution-steps.md](references/execution-steps.md)
- [references/local-mode.md](references/local-mode.md)
- [references/ol-wave-integration.md](references/ol-wave-integration.md)
- [references/ralph-loop-contract.md](references/ralph-loop-contract.md)
- [references/troubleshooting.md](references/troubleshooting.md)
- [references/validation-contract.md](references/validation-contract.md)
- [references/worker-pitfalls.md](references/worker-pitfalls.md)
- [references/worker-specs.md](references/worker-specs.md)
- [references/worktree-isolation.md](references/worktree-isolation.md)
- [../shared/references/backend-background-tasks.md](../shared/references/backend-background-tasks.md)
- [../shared/references/backend-claude-teams.md](../shared/references/backend-claude-teams.md)
- [../shared/references/backend-codex-subagents.md](../shared/references/backend-codex-subagents.md)
- [../shared/references/backend-inline.md](../shared/references/backend-inline.md)
- [../shared/references/claude-code-latest-features.md](../shared/references/claude-code-latest-features.md)
- [references/pre-spawn-friction-gates.md](references/pre-spawn-friction-gates.md)
- [references/scope-escape-template.md](references/scope-escape-template.md)
- [references/worker-pre-task-checks.md](references/worker-pre-task-checks.md)
- [../shared/references/ralph-loop-contract.md](../shared/references/ralph-loop-contract.md)
