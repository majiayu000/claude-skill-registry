---
name: swarm
description: 'Spawn isolated agents for parallel task execution. Local mode auto-selects runtime-native teams (Claude Native Teams in Claude sessions, Codex sub-agents in Codex sessions). Distributed mode uses tmux + Agent Mail (process isolation, persistence). Triggers: "swarm", "spawn agents", "parallel work", "run in parallel", "parallel execution".'
metadata:
  tier: execution
  dependencies:
    - implement # required - executes `/implement <bead-id>` in distributed mode
    - vibe      # optional - integration with validation
---

# Swarm Skill

Spawn isolated agents to execute tasks in parallel. Fresh context per agent (Ralph Wiggum pattern).

**Execution Modes:**
- **Local** (default) - Runtime-native spawning (Claude Native Teams in Claude sessions; Codex sub-agents in Codex sessions; fallback tasks only if needed)
- **Distributed** (`--mode=distributed`) - tmux sessions + Agent Mail for robust coordination

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
    +-> Select spawn backend (runtime-native first: Claude teams in Claude runtime, Codex sub-agents in Codex runtime; fallback tasks if unavailable)
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

Given `/swarm`:

### Step 0: Detect Multi-Agent Capabilities (MANDATORY)

Use runtime capability detection, not hardcoded tool names. Swarm requires:
- **Spawn parallel subagents** — create workers that run concurrently
- **Agent messaging** (optional) — for coordination and retry

See `skills/shared/SKILL.md` for the capability contract.

**After detecting your backend, read the matching reference for concrete spawn/wait/message/cleanup examples:**
- Claude feature contract → `skills/shared/references/claude-code-latest-features.md`
- Claude Native Teams → `skills/shared/references/backend-claude-teams.md`
- Codex Sub-Agents / CLI → `skills/shared/references/backend-codex-subagents.md`
- Background Tasks → `skills/shared/references/backend-background-tasks.md`
- Inline (no spawn) → `skills/shared/references/backend-inline.md`

See also `references/local-mode.md` for swarm-specific execution details (worktrees, validation, git commit policy, wave repeat).

### Step 1: Ensure Tasks Exist

Use TaskList to see current tasks. If none, create them:

```
TaskCreate(subject="Implement feature X", description="Full details...")
TaskUpdate(taskId="2", addBlockedBy=["1"])  # Add dependencies after creation
```

### Step 2: Identify Wave

Find tasks that are:
- Status: `pending`
- No blockedBy (or all blockers completed)

These can run in parallel.

### Steps 3-6: Spawn Workers, Validate, Finalize

**For detailed local mode execution (team creation, worker spawning, race condition prevention, git commit policy, validation contract, cleanup, and repeat logic), read `skills/swarm/references/local-mode.md`.**

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

## Key Points

- **Runtime-native local mode** - Auto-selects the native backend for the current runtime (Claude teams or Codex sub-agents)
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
| `--mode=local\|distributed` | Execution mode | `local` |
| `--max-workers=N` | Max concurrent workers | 5 |
| `--from-wave <json-file>` | Load wave from OL hero hunt output (see OL Wave Integration) | - |
| `--bead-ids` | Specific beads to work (comma-separated, distributed mode) | Auto from `bd ready` |
| `--wait` | Wait for all workers to complete (distributed mode) | false |
| `--timeout` | Max time to wait if `--wait` (distributed mode) | 30m |

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

Ralph alignment source: `skills/shared/references/ralph-loop-contract.md`.

## Integration with Crank

When `/crank` invokes `/swarm`: Crank bridges beads to TaskList, swarm executes with fresh-context agents, crank syncs results back.

| You Want | Use | Why |
|----------|-----|-----|
| Fresh-context parallel execution | `/swarm` | Each spawned agent is a clean slate |
| Autonomous epic loop | `/crank` | Loops waves via swarm until epic closes |
| Just swarm, no beads | `/swarm` directly | TaskList only, skip beads |
| RPI progress gates | `/ratchet` | Tracks progress; does not execute work |

---

## Distributed Mode

Use `--mode=distributed` when you need full agent orchestration beyond what local mode provides:

- **Process isolation** — each worker runs in its own tmux session, not sharing the lead's process
- **Crash recovery** — workers survive if the Mayor disconnects (tmux sessions persist)
- **Agent Mail messaging** — bidirectional coordination (ACCEPTED, PROGRESS, DONE, HELP_REQUEST)
- **File reservations** — conflict detection before workers edit shared files
- **Debuggable** — `tmux attach -t <session>` to inspect stuck workers live

**When to use:** Long-running work (>10 min), need to debug stuck workers, Mayor might disconnect, complex multi-file coordination. Local mode is faster to launch but provides less control.

**For the full distributed mode specification, read `skills/swarm/references/distributed-mode.md`.**

---

## OL Wave Integration

When `/swarm --from-wave <json-file>` is invoked, the swarm reads wave data from an OL hero hunt output file and executes it with completion backflow to OL.

### Pre-flight

```bash
# --from-wave requires ol CLI on PATH
which ol >/dev/null 2>&1 || {
    echo "Error: ol CLI required for --from-wave. Install ol or use swarm without wave integration."
    exit 1
}
```

If `ol` is not on PATH, exit immediately with the error above. Do not fall back to normal swarm mode.

### Input Format

The `--from-wave` JSON file contains `ol hero hunt` output:

```json
{
  "wave": [
    {"id": "ol-527.1", "title": "Add auth middleware", "spec_path": "quests/ol-527/specs/ol-527.1.md", "priority": 1},
    {"id": "ol-527.2", "title": "Fix rate limiting", "spec_path": "quests/ol-527/specs/ol-527.2.md", "priority": 2}
  ],
  "blocked": [
    {"id": "ol-527.3", "title": "Integration tests", "blocked_by": ["ol-527.1", "ol-527.2"]}
  ],
  "completed": [
    {"id": "ol-527.0", "title": "Project setup"}
  ]
}
```

### Execution

1. **Parse the JSON file** and extract the `wave` array.

2. **Create TaskList tasks** from wave entries (one `TaskCreate` per entry):

```
for each entry in wave:
    TaskCreate(
        subject="[{entry.id}] {entry.title}",
        description="OL bead {entry.id}\nSpec: {entry.spec_path}\nPriority: {entry.priority}\n\nRead the spec file at {entry.spec_path} for full requirements.",
        metadata={
            "ol_bead_id": entry.id,
            "ol_spec_path": entry.spec_path,
            "ol_priority": entry.priority
        }
    )
```

3. **Execute swarm normally** on those tasks (Step 2 onward from main execution flow). Tasks are ordered by priority (lower number = higher priority).

4. **Completion backflow**: After each worker completes a bead task AND passes validation, the team lead runs the OL ratchet command to report completion back to OL:

```bash
# Extract quest ID from bead ID (e.g., ol-527.1 -> ol-527)
QUEST_ID=$(echo "$BEAD_ID" | sed 's/\.[^.]*$//')

ol hero ratchet "$BEAD_ID" --quest "$QUEST_ID"
```

**Ratchet result handling:**

| Exit Code | Meaning | Action |
|-----------|---------|--------|
| 0 | Bead complete in OL | Mark task completed, log success |
| 1 | Ratchet validation failed | Mark task as failed, log the validation error from stderr |

5. **After all wave tasks complete**, report a summary that includes both swarm results and OL ratchet status for each bead.

### Example

```
/swarm --from-wave /tmp/wave-ol-527.json

# Reads wave JSON -> creates 2 tasks from wave entries
# Spawns workers for ol-527.1 and ol-527.2
# On completion of ol-527.1:
#   ol hero ratchet ol-527.1 --quest ol-527 -> exit 0 -> bead complete
# On completion of ol-527.2:
#   ol hero ratchet ol-527.2 --quest ol-527 -> exit 0 -> bead complete
# Wave done: 2/2 beads ratcheted in OL
```

---

## References

- **Local Mode Details:** `skills/swarm/references/local-mode.md`
- **Distributed Mode:** `skills/swarm/references/distributed-mode.md`
- **Validation Contract:** `skills/swarm/references/validation-contract.md`
- **Agent Mail Protocol:** See `skills/shared/agent-mail-protocol.md` for message format specifications
- **Parser (Go):** `cli/internal/agentmail/` - shared parser for all message types

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

### Loading Wave from OL

**User says:** `/swarm --from-wave /tmp/wave-ol-527.json`

**What happens:**
1. Agent validates `ol` CLI is on PATH (pre-flight check)
2. Agent reads wave JSON from OL hero hunt output
3. Agent creates TaskList tasks from wave entries (priority-sorted)
4. Agent spawns workers for all unblocked beads
5. On completion, agent runs `ol hero ratchet <bead-id> --quest <quest-id>` for each bead
6. Agent reports backflow status to user

**Result:** OL beads executed with completion reporting back to Olympus.

---

## Worktree Isolation (Multi-Epic Dispatch)

**Default behavior:** Auto-detect and prefer runtime-native isolation first.

In Claude runtime, first verify teammate profiles with `claude agents` and use agent definitions with `isolation: worktree` for write-heavy parallel waves. If native isolation is unavailable, use manual `git worktree` fallback below.

**When to use worktrees:** Activate worktree isolation when:
- Dispatching workers across **multiple epics** (each epic touches different packages)
- Wave has **>3 workers touching overlapping files** (detected via `git diff --name-only`)
- Tasks span **independent branches** that shouldn't cross-contaminate

Evidence: 4 parallel agents in shared worktree produced 1 build break and 1 algorithm duplication (see `.agents/evolve/dispatch-comparison.md`). Worktree isolation prevents collisions by construction.

### Detection: Do I Need Worktrees?

```bash
# Heuristic: multi-epic = worktrees needed
# Single epic with independent files = shared worktree OK

# Check if tasks span multiple epics
# e.g., task subjects contain different epic IDs (ol-527, ol-531, ...)
# If yes: use worktrees
# If no: proceed with default shared worktree
```

### Creation: One Worktree Per Epic

Before spawning workers, create an isolated worktree per epic:

```bash
# For each epic ID in the wave:
git worktree add /tmp/swarm-<epic-id> -b swarm/<epic-id>
```

Example for 3 epics:
```bash
git worktree add /tmp/swarm-ol-527 -b swarm/ol-527
git worktree add /tmp/swarm-ol-531 -b swarm/ol-531
git worktree add /tmp/swarm-ol-535 -b swarm/ol-535
```

Each worktree starts at HEAD of current branch. The worker branch (`swarm/<epic-id>`) is ephemeral — deleted after merge.

### Worker Routing: Inject Worktree Path

Pass the worktree path as the working directory in each worker prompt:

```
WORKING DIRECTORY: /tmp/swarm-<epic-id>

All file reads, writes, and edits MUST use paths rooted at /tmp/swarm-<epic-id>.
Do NOT operate on /path/to/main/repo directly.
```

Workers run in isolation — changes in one worktree cannot conflict with another.

**Result file path:** Workers still write results to the main repo's `.agents/swarm/results/`:
```bash
# Worker writes to main repo result path (not the worktree)
RESULT_DIR=/path/to/main/repo/.agents/swarm/results
```

The orchestrator path for `.agents/swarm/results/` is always the main repo, not the worktree.

### Merge-Back: After Validation

After a worker's task passes validation, merge the worktree branch back to main:

```bash
# From the main repo (not worktree)
git merge --no-ff swarm/<epic-id> -m "chore: merge swarm/<epic-id> (epic <epic-id>)"
```

Merge order: respect task dependencies. If epic B blocked by epic A, merge A before B.

**On merge conflict:** The team lead resolves conflicts manually. Workers must not merge — lead-only commit policy still applies.

### Cleanup: Remove Worktrees After Merge

```bash
# After successful merge:
git worktree remove /tmp/swarm-<epic-id>
git branch -d swarm/<epic-id>
```

Run cleanup even on partial failures (same reaper pattern as team cleanup).

### Full Pre-Spawn Sequence (Worktree Mode)

```
1. Detect: does this wave need worktrees? (multi-epic or file overlap)
2. For each epic:
   a. git worktree add /tmp/swarm-<epic-id> -b swarm/<epic-id>
3. Spawn workers with worktree path injected into prompt
4. Wait for completion (same as shared mode)
5. Validate each worker's changes (run tests inside worktree)
6. For each passing epic:
   a. git merge --no-ff swarm/<epic-id>
   b. git worktree remove /tmp/swarm-<epic-id>
   c. git branch -d swarm/<epic-id>
7. Commit all merged changes (team lead, sole committer)
```

### Parameters

| Parameter | Description | Default |
|-----------|-------------|---------|
| `--worktrees` | Force worktree isolation for this wave | Off (auto-detect) |
| `--no-worktrees` | Force shared worktree even for multi-epic | Off |

---

## Troubleshooting

### Workers produce file conflicts
Cause: Multiple workers editing the same file in parallel.
Solution: Use worktree isolation (`--worktrees`) for multi-epic dispatch. For single-epic waves, use wave decomposition to group workers by file scope. Homogeneous waves (all Go, all docs) prevent conflicts.

### Team creation fails
Cause: Stale team from prior session not cleaned up.
Solution: Run `rm -rf ~/.claude/teams/<team-name>` then retry.

### Codex agents unavailable
Cause: `codex` CLI not installed or API key not configured.
Solution: Run `which codex` to verify installation. Check `~/.codex/config.toml` for API credentials.

### Workers timeout or hang
Cause: Worker task too large or blocked on external dependency.
Solution: Break tasks into smaller units. Add timeout metadata to worker tasks.

### OL wave integration fails with "ol CLI required"
Cause: `--from-wave` used but `ol` CLI not on PATH.
Solution: Install Olympus CLI or run swarm without `--from-wave` flag.

### Tasks assigned but workers never spawn
Cause: Backend selection failed or spawning API unavailable.
Solution: Check which spawn backend was selected (look for "Using: <backend>" message). Verify Codex CLI (`which codex`) or native team API availability.
