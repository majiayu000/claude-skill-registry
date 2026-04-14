---
name: swarm
description: 'Spawn isolated agents for parallel task execution. Auto-selects runtime-native teams (Claude Native Teams in Claude sessions, Codex sub-agents in Codex sessions). Triggers: "swarm", "spawn agents", "parallel work", "run in parallel", "parallel execution".'
skill_api_version: 1
context:
  window: fork
  intent:
    mode: task
  sections:
    exclude: [HISTORY]
  intel_scope: full
metadata:
  tier: orchestration
  dependencies:
    - implement # required - executes `/implement <bead-id>` per task
    - vibe      # optional - integration with validation
output_contract: ".agents/swarm/results/*.json"
---

# Swarm Skill

Spawn isolated agents to execute tasks in parallel. Fresh context per agent (Ralph Wiggum pattern).

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

Given `/swarm`:

### Step 0: Detect Multi-Agent Capabilities (MANDATORY)

Use runtime capability detection, not hardcoded tool names. Swarm requires:
- **Spawn parallel subagents** — create workers that run concurrently
- **Agent messaging** (optional) — for coordination and retry

See `skills/shared/SKILL.md` for the capability contract.

**After detecting your backend, read the matching reference for concrete spawn/wait/message/cleanup examples:**
- Shared Claude feature contract → `skills/shared/references/claude-code-latest-features.md`
- Local mirrored contract for runtime-local reads → `references/claude-code-latest-features.md`
- Claude Native Teams → `references/backend-claude-teams.md`
- Codex Sub-Agents / CLI → `references/backend-codex-subagents.md`
- Background Tasks → `references/backend-background-tasks.md`
- Inline (no spawn) → `references/backend-inline.md`

See also `references/local-mode.md` for swarm-specific execution details (worktrees, validation, git commit policy, wave repeat).

### Step 0.5: gc Backend Detection (Before Worker Dispatch)

Before spawning workers via Claude teams or Codex sub-agents, check if gc is available:

```bash
if command -v gc &>/dev/null && gc status --json 2>/dev/null | jq -e '.controller.state == "running"' >/dev/null 2>&1; then
    SWARM_BACKEND="gc"
else
    SWARM_BACKEND="native"  # fallback to Claude teams / Codex sub-agents
fi
```

When `SWARM_BACKEND="gc"`:
- Use `gc session nudge <worker-alias> "<task prompt>"` instead of `spawn_agent()`
- Monitor workers via `gc session peek <worker-alias> --lines 50`
- Workers already use `bd` for issue tracking — no change needed
- Results still written to `.agents/swarm/results/` — no change needed
- gc pool auto-scaling handles worker lifecycle (based on `scale_check = "bd ready --count"`)

### Step 1: Ensure Tasks Exist

Use TaskList to see current tasks. If none, create them:

```
TaskCreate(subject="Implement feature X", description="Full details...",
  metadata={"issue_type": "feature", "files": ["src/feature_x.py", "tests/test_feature_x.py"], "validation": {...}})
TaskUpdate(taskId="2", addBlockedBy=["1"])  # Add dependencies after creation
```

#### Task Typing + File Manifest

Every TaskCreate **must** include `metadata.issue_type` plus a `metadata.files` array. `issue_type` drives active constraint applicability and validation policy; `files` enable mechanical conflict detection before spawning a wave.
This is how the prevention ratchet applies shift-left mechanically: active compiled findings use issue type plus changed files to decide whether a task should be blocked, warned, or left alone.

- Use canonical issue types: `feature`, `bug`, `task`, `docs`, `chore`, `ci`.
- Preserve the same `metadata.issue_type` on TaskUpdate / TaskCompleted payloads so task-validation can apply active constraints without guessing.
- Pull file lists from the plan, issue description, or codebase exploration during planning.
- If you cannot enumerate files yet, add a planning step to identify them before spawning workers. An empty or missing manifest signals the need for more planning, not unconstrained workers.
- Workers receive the manifest in their prompt and are instructed to stay within it (see `references/local-mode.md` worker prompt template).
- The worker prompt MUST include the `metadata.files` array as the FILE MANIFEST section. Workers grep for existing function signatures before writing new code to avoid duplication.

```json
{
  "issue_type": "feature",
  "files": ["cli/cmd/ao/goals.go", "cli/cmd/ao/goals_test.go"],
  "validation": {
    "tests": "go test ./cli/cmd/ao/...",
    "files_exist": ["cli/cmd/ao/goals.go"]
  }
}
```

### Step 1a: Build Context Briefing (Before Worker Dispatch)

```bash
if command -v ao &>/dev/null; then
    ao context assemble --task='<swarm objective or wave description>'
fi
```

This produces a 5-section briefing (GOALS, HISTORY, INTEL, TASK, PROTOCOL) at `.agents/rpi/briefing-current.md` with secrets redacted. Include the briefing path in each worker's TaskCreate description so workers start with full project context.

**Output schema size guard:** When 5+ workers in a wave share the same output schema (e.g., `verdict.json`), cache it to `.agents/council/output-schema.json` and reference by path instead of inlining ~500 tokens per worker. For ≤4 workers, inline is fine. See council skill's caching guidance reference for details.

Worker prompt signpost:
- Claude workers should include: `Knowledge artifacts are in .agents/. See .agents/AGENTS.md for navigation. Use \`ao lookup --query "topic"\` for learnings.`
- Codex workers cannot rely on `.agents/` file access in sandbox. The lead should search `.agents/learnings/` for relevant material and inline the top 3 results directly in the worker prompt body.

### Step 1.5: Auto-Populate File Manifests

**Skip this step if all tasks already have populated `metadata.files` arrays.**

If any task is missing its file manifest, auto-generate it before Step 2:

1. **Spawn haiku Explore agents** (one per task missing manifests) to identify files:
   ```
   Agent(subagent_type="Explore", model="haiku",
     prompt="Given this task: '<task subject + description>', identify all files
     that will need to be created or modified. Return a JSON array of file paths.")
   ```

2. **Inject manifests** back into tasks:
   ```
   TaskUpdate(taskId=task.id, metadata={"files": [explored_files]})
   ```

Once all tasks have manifests, proceed to Step 2 where the Pre-Spawn Conflict Check enforces file ownership.

### Step 1.6: Advisory Bead Clustering

When tasks come from bd and `scripts/bd-cluster.sh` exists, run `scripts/bd-cluster.sh --json 2>/dev/null || true` before Step 2. Summarize any clusters as consolidation hints only; never run `--apply` here, and keep Step 2's file-manifest and dependency gates authoritative.

### Step 2: Identify Wave

**Pre-Spawn Friction Gates:** Before spawning workers, execute all 6 friction gates (base sync, file manifest, dependency graph, misalignment breaker, wave cap, base-SHA ancestry). See `references/pre-spawn-friction-gates.md`.

Find tasks that are:
- Status: `pending`
- No blockedBy (or all blockers completed)

These can run in parallel.

#### Pre-Spawn Conflict Check

Before spawning a wave, scan all worker file manifests for overlapping files:

```
wave_tasks = [tasks with status=pending and no blockers]
all_files = {}
for task in wave_tasks:
    for f in task.metadata.files:
        if f in all_files:
            CONFLICT: f is claimed by both all_files[f] and task.id
        all_files[f] = task.id
```

**On conflict detection:**
- **Serialize** the conflicting workers into separate sub-waves (preferred -- simplest fix), OR
- **Isolate** them with worktree isolation (`--worktrees`) so each operates on a separate branch.

Do not spawn workers with overlapping file manifests into the same shared-worktree wave. This is the primary cause of build breaks and merge conflicts in parallel execution.

**Display ownership table** before spawning:
```
File Ownership Map (Wave N):
┌─────────────────────────────┬──────────┬──────────┐
│ File                        │ Owner    │ Conflict │
├─────────────────────────────┼──────────┼──────────┤
│ src/auth/middleware.go       │ task-1   │         │
│ src/auth/middleware_test.go  │ task-1   │         │
│ src/api/routes.go            │ task-2   │         │
│ src/config/settings.go       │ task-1,3 │ YES     │
└─────────────────────────────┴──────────┴──────────┘
Conflicts: 1 (resolved: serialized task-3 into sub-wave 2)
```

#### Test File Naming Validation

When workers create new test files, validate naming against loaded standards:

1. **Detection:** Same language detection as /crank (go.mod → Go, pyproject.toml → Python, etc.)
2. **Validation:** Load the Testing section of the relevant standard. For Go, this means:
   - New test files must match `<source>_test.go` or `<source>_extra_test.go`
   - Reject `cov*_test.go` or arbitrary prefixes
3. **Serial-first for monolith packages:** If multiple workers target the same package AND that package has a shared `testutil_test.go` or `>5` existing test files, force serial execution within that package.

### Step 2.5: Pre-Spawn Base-SHA Refresh (Multi-Wave Only)

When executing wave 2+ (not the first wave), verify workers branch from the latest commit — not a stale SHA from before the prior wave's changes were committed.

```bash
# PSEUDO-CODE
# Capture current HEAD after prior wave's commit
CURRENT_SHA=$(git rev-parse HEAD)

# If using worktrees, verify they're up to date
if [[ -n "$WORKTREE_PATH" ]]; then
    (cd "$WORKTREE_PATH" && git pull --rebase origin "$(git branch --show-current)" 2>/dev/null || true)
fi
```

**Cross-reference prior wave diff against current wave file manifests:**

```bash
# PSEUDO-CODE
# Files changed in prior wave
PRIOR_WAVE_FILES=$(git diff --name-only "${WAVE_START_SHA}..HEAD")

# Check for overlap with current wave manifests
for task in $WAVE_TASKS; do
    TASK_FILES=$(echo "$task" | jq -r '.metadata.files[]')
    OVERLAP=$(comm -12 <(echo "$PRIOR_WAVE_FILES" | sort) <(echo "$TASK_FILES" | sort))
    if [[ -n "$OVERLAP" ]]; then
        echo "WARNING: Task $task touches files modified in prior wave: $OVERLAP"
        echo "Workers MUST read the latest version (post-prior-wave commit)"
    fi
done
```

**Why:** Without base-SHA refresh, wave 2+ workers may read stale file versions from before wave 1 changes were committed. This causes workers to overwrite prior wave edits or implement against outdated code. See crank Step 5.7 (wave checkpoint) for the SHA tracking pattern.

### Steps 3-6: Spawn Workers, Validate, Finalize

**For detailed local mode execution (team creation, worker spawning, race condition prevention, git commit policy, validation contract, cleanup, and repeat logic), read `skills/swarm/references/local-mode.md`.**

> **Platform pitfalls:** Include relevant pitfalls from `references/worker-pitfalls.md` in worker prompts for the target language/platform. For example, inject the Bash section for shell script tasks, the Go section for Go tasks, etc. This prevents common worker failures from known platform gotchas.

#### gc Worker Dispatch (when `SWARM_BACKEND="gc"`)

When gc is the selected backend, dispatch and monitor workers through gc sessions instead of Claude teams or Codex sub-agents:

```bash
# Dispatch a task to a gc-managed worker
gc session nudge <worker-alias> "Implement task #<id>: <subject>. Files: <manifest>. Write results to .agents/swarm/results/<id>.json"

# Monitor worker progress
gc session peek <worker-alias> --lines 50

# Check all worker statuses
gc status --json | jq '.sessions[] | {alias, state, last_activity}'
```

**gc dispatch follows the same orchestration contract as native backends:**
- Pre-assigned tasks (mayor assigns before nudge)
- File manifest enforcement (included in nudge prompt)
- Results written to `.agents/swarm/results/<id>.json`
- Lead-only commit policy (workers do not commit)
- Scope-escape protocol (workers append to `.agents/swarm/scope-escapes.jsonl`)

**gc-specific behaviors:**
- Worker lifecycle managed by gc pool auto-scaling — no explicit cleanup needed
- Use `gc session peek` for progress checks instead of `SendMessage` / `send_input`
- If a worker is idle or unresponsive, `gc session nudge` can re-prompt it
- gc sessions persist across waves — the same worker alias can be reused without respawning

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
            "issue_type": entry.issue_type,
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

### Isolation Semantics Per Spawn Backend

| Backend | Isolation Mechanism | How It Works |
|---------|-------------------|--------------|
| **Claude teams** (`Task` with `team_name`) | `isolation: worktree` in agent definition | Runtime creates an isolated git worktree per teammate; changes are invisible to other agents and the main tree until merged |
| **Background tasks** (`Task` with `run_in_background`) | `isolation: worktree` in agent definition | Same worktree isolation as teams; each background agent gets its own worktree |
| **gc pool** (`gc session nudge`) | gc-managed sessions | Each gc worker runs in its own session; isolation is managed by gc pool lifecycle and bd issue ownership |
| **Inline** (no spawn) | None | Operates directly on the main working tree; no isolation possible |

**Sparse checkout for large repos:** Set `worktree.sparsePaths` in project settings to limit worktree checkouts to relevant directories. This reduces clone time and disk usage for monorepos where workers only need a subset of the tree.

### Effort Levels for Workers

Use the effort command to right-size model reasoning per worker role:

| Worker Role | Recommended Effort | Rationale |
|-------------|-------------------|-----------|
| Research/exploration | `low` | Fast, broad scanning — depth not needed |
| Implementation (code) | `high` | Deep reasoning for correct implementation |
| Docs/chore | `low` | Fast execution for simple tasks |

**Key diagnostic:** When `isolation: worktree` is specified but worker changes appear in the main working tree (no separate worktree path in the Task result), **isolation did NOT engage**. This is a silent failure — the runtime accepted the parameter but did not create a worktree.

### Post-Spawn Isolation Verification

After spawning workers with `isolation: worktree`, the lead MUST verify isolation engaged:

1. **Check Task result** for a `worktreePath` field. If present, isolation is active.
2. **If `worktreePath` is absent** but `isolation: worktree` was specified:
   - Log warning: "Isolation did not engage for worker-N. Changes may be in main working tree."
   - **For waves with 2+ workers touching overlapping files:** abort the wave, fall back to serial execution to prevent conflicts.
   - **For waves with fully independent file sets:** may proceed with caution, but monitor for conflicts.
3. **If isolation consistently fails:** fall back to manual `git worktree` creation (see below) or switch to serial inline execution.

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

**Base-SHA ancestry check before merge-back:** Worktree branches rooted off non-main commits pull unintended branch ancestry during `git merge --no-ff`, causing extra files to land. Before merging:
- **Single-commit worktree branches:** Prefer `git cherry-pick <sha>` over `git merge --no-ff`. Cherry-pick applies only the commit's diff and avoids pulling unintended ancestry.
- **Multi-commit worktree branches:** Run `git rebase main swarm/<epic-id>` before `git merge --no-ff` to re-root the branch onto current main HEAD and eliminate stale ancestry.

**Merge Arbiter Protocol:**

Replace manual conflict resolution with a structured sequential rebase:

1. **Merge order:** Dependency-sorted (leaves first), then by task ID for ties
2. **Sequential rebase** (one branch at a time):
   ```bash
   # For each branch in merge order:
   git rebase main swarm/<epic-id>
   ```
3. **On rebase conflict:**
   - Check the file-ownership map from Step 1.5
   - If the conflicting file has a single owner → use that owner's version
   - If the conflicting file has multiple owners → use the version from the task being merged (current branch)
   - Run tests after resolution to verify
4. **If tests fail after conflict resolution:**
   - Spawn a fix-up worker scoped ONLY to the conflicting files
   - Worker receives: both versions, test output, ownership context
   - Max 3 fix-up retries per conflict
   - If still failing after 3 retries → abort merge for this branch, escalate to human
5. **Display merge status table** after all merges complete:
   ```
   Merge Status:
   ┌────────────────────┬──────────┬────────────┬───────────┐
   │ Branch             │ Status   │ Conflicts  │ Fix-ups   │
   ├────────────────────┼──────────┼────────────┼───────────┤
   │ swarm/task-1       │ MERGED   │ 0          │ 0         │
   │ swarm/task-2       │ MERGED   │ 1 (auto)   │ 0         │
   │ swarm/task-3       │ MERGED   │ 1 (fixup)  │ 1         │
   └────────────────────┴──────────┴────────────┴───────────┘
   ```

Workers must not merge — lead-only commit policy still applies.

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

### Worktree isolation did not engage
Cause: `isolation: worktree` was specified but the Task result has no `worktreePath` — worker changes land in the main tree.
Solution: Verify agent definitions include `isolation: worktree`. If the runtime does not support declarative isolation, fall back to manual `git worktree add` (see Worktree Isolation section). For overlapping-file waves, abort and switch to serial execution.

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

### gc backend detected but workers unresponsive
Cause: gc controller is running but worker sessions are idle or not accepting nudges.
Solution: Run `gc status --json` to check session states. Use `gc session peek <alias> --lines 50` to inspect last activity. If a session is stuck, restart it via gc pool commands. Verify `scale_check = "bd ready --count"` returns pending work.

### Tasks assigned but workers never spawn
Cause: Backend selection failed or spawning API unavailable.
Solution: Check which spawn backend was selected (look for "Using: <backend>" message). Verify Codex CLI (`which codex`) or native team API availability.

## Reference Documents

- [references/conflict-recovery.md](references/conflict-recovery.md)
- [references/cold-start-contexts.md](references/cold-start-contexts.md)
- [references/backend-background-tasks.md](references/backend-background-tasks.md)
- [references/backend-claude-teams.md](references/backend-claude-teams.md)
- [references/backend-codex-subagents.md](references/backend-codex-subagents.md)
- [references/backend-inline.md](references/backend-inline.md)
- [references/claude-code-latest-features.md](references/claude-code-latest-features.md)
- [references/local-mode.md](references/local-mode.md)
- [references/ralph-loop-contract.md](references/ralph-loop-contract.md)
- [references/validation-contract.md](references/validation-contract.md)
- [references/worker-pitfalls.md](references/worker-pitfalls.md)
- [../shared/references/backend-background-tasks.md](../shared/references/backend-background-tasks.md)
- [../shared/references/backend-claude-teams.md](../shared/references/backend-claude-teams.md)
- [../shared/references/backend-codex-subagents.md](../shared/references/backend-codex-subagents.md)
- [../shared/references/backend-inline.md](../shared/references/backend-inline.md)
- [../shared/references/claude-code-latest-features.md](../shared/references/claude-code-latest-features.md)
- [references/pre-spawn-friction-gates.md](references/pre-spawn-friction-gates.md)
- [../shared/references/ralph-loop-contract.md](../shared/references/ralph-loop-contract.md)
