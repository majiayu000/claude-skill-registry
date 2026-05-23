---
name: team-lifecycle
description: Full lifecycle orchestrator - spec/impl/test. Spawn-wait-close pipeline with inline discuss subagent, shared explore cache, fast-advance, and consensus severity routing.
---

# Team Lifecycle Orchestrator

Full lifecycle team orchestration for specification, implementation, and testing workflows. The orchestrator drives a multi-agent pipeline through five phases: requirement clarification, session initialization, task chain creation, pipeline coordination (spawn/wait/close loop), and completion reporting.

Key design principles:

- **Inline discuss subagent**: Produce roles (analyst, writer, reviewer) call a discuss subagent internally rather than spawning a dedicated discussion agent. This halves spec pipeline beats from 12 to 6.
- **Shared explore cache**: All agents share a centralized `explorations/` directory with `cache-index.json`, eliminating duplicate codebase exploration.
- **Fast-advance spawning**: After an agent completes, the orchestrator immediately spawns the next agent in a linear chain without waiting for a full coordination cycle.
- **Consensus severity routing**: Discussion verdicts route through HIGH/MEDIUM/LOW severity tiers, each with distinct orchestrator behavior (revision, warn-proceed, or pass-through).
- **Beat model**: Each pipeline step is a single beat -- spawn agent, wait for result, process output, spawn next. The orchestrator processes one beat per cycle, then yields.

---

## Architecture

```
+-------------------------------------------------------------+
|  Team Lifecycle Orchestrator                                  |
|  Phase 1 -> Phase 2 -> Phase 3 -> Phase 4 -> Phase 5         |
|  Require    Init       Dispatch   Coordinate   Report         |
+----------+------------------------------------------------+--+
           |
     +-----+------+----------+-----------+-----------+
     v            v          v           v           v
+---------+ +---------+ +---------+ +---------+ +---------+
| Phase 1 | | Phase 2 | | Phase 3 | | Phase 4 | | Phase 5 |
| Require | | Init    | | Dispatch| | Coord   | | Report  |
+---------+ +---------+ +---------+ +---------+ +---------+
     |            |          |          |||          |
  params       session     tasks     agents      summary
                                    /  |  \
                              spawn  wait  close
                              /        |        \
                       +------+   +-------+   +--------+
                       |agent1|   |agent2 |   |agent N |
                       +------+   +-------+   +--------+
                          |           |            |
                     (may call discuss/explore subagents internally)
```

**Phase 4 Beat Cycle (single beat)**:

```
  event (phase advance / user resume)
      |
      v
  [Orchestrator]
      +-- read state file
      +-- find ready tasks (pending + all blockers completed)
      +-- spawn agent(s) for ready task(s)
      +-- wait(agent_ids, timeout)
      +-- process results (consensus routing, artifacts)
      +-- update state file
      +-- close completed agents
      +-- fast-advance: immediately spawn next if linear successor
      +-- yield (wait for next event or user command)
```

---

## Agent Registry

| Agent | Role File | Responsibility | Pattern |
|-------|-----------|----------------|---------|
| analyst | ~/.codex/agents/analyst.md | Seed analysis, context gathering, DISCUSS-001 | 2.8 Inline Subagent |
| writer | ~/.codex/agents/writer.md | Document generation, DISCUSS-002 to DISCUSS-005 | 2.8 Inline Subagent |
| planner | ~/.codex/agents/planner.md | Multi-angle exploration, plan generation | 2.9 Cached Exploration |
| executor | ~/.codex/agents/executor.md | Code implementation | 2.1 Standard |
| tester | ~/.codex/agents/tester.md | Test-fix cycles | 2.3 Deep Interaction |
| reviewer | ~/.codex/agents/reviewer.md | Code review + spec quality, DISCUSS-006 | 2.8 Inline Subagent |
| architect | ~/.codex/agents/architect.md | Architecture consulting (on-demand) | 2.1 Standard |
| fe-developer | ~/.codex/agents/fe-developer.md | Frontend implementation | 2.1 Standard |
| fe-qa | ~/.codex/agents/fe-qa.md | Frontend QA, GC loop | 2.3 Deep Interaction |

> All agent role files MUST be deployed to `~/.codex/agents/` before use.
> Pattern 2.8 = agent internally spawns discuss subagent for multi-perspective critique.
> Pattern 2.9 = agent uses shared explore cache before work.
> Pattern 2.3 = orchestrator may use send_input for iterative correction loops.

---

## Subagent Registry

| Subagent | Agent File | Callable By | Purpose |
|----------|-----------|-------------|---------|
| discuss | ~/.codex/agents/discuss-agent.md | analyst, writer, reviewer | Multi-perspective critique via CLI tools |
| explore | ~/.codex/agents/explore-agent.md | analyst, planner, any agent | Codebase exploration with shared cache |

Subagents are spawned by **agents themselves** (not by the orchestrator). An agent reads the subagent spec, spawns it inline via `spawn_agent`, waits for the result, and closes it. The orchestrator never directly manages subagent lifecycle.

---

## Fast-Advance Spawning

After `wait()` returns a completed agent result, the orchestrator checks whether the next pipeline step is a simple linear successor (exactly one task becomes ready, no parallel window, no checkpoint).

**Decision table**:

| Condition | Action |
|-----------|--------|
| 1 ready task, simple linear successor, no checkpoint | Immediately `spawn_agent` for next task (fast-advance) |
| Multiple ready tasks (parallel window) | Spawn all ready tasks in batch, then `wait` on all |
| No ready tasks, other agents still running | Yield, wait for those agents to complete |
| No ready tasks, nothing running | Pipeline complete, proceed to Phase 5 |
| Checkpoint task completed (e.g., QUALITY-001) | Pause, output checkpoint message, wait for user |

**Fast-advance failure recovery**:
When the orchestrator detects that a fast-advanced agent has failed (wait returns error or timeout with no result):

1. Record failure in state file
2. Mark that task as "pending" again in state
3. Spawn a fresh agent for the same task
4. If the same task fails 3+ times, pause pipeline and report to user

---

## Consensus Severity Routing

When a produce agent (analyst, writer, reviewer) reports a discuss result, the orchestrator parses the verdict from the agent output.

**Output format from agents** (written to their artifact, also in wait() result):

```
DISCUSS_RESULT:
- verdict: <consensus_reached | consensus_blocked>
- severity: <HIGH | MEDIUM | LOW>
- average_rating: <N>/5
- divergences: <summary>
- action_items: <list>
- recommendation: <revise | proceed-with-caution | escalate>
- discussion_path: <path-to-discussion-record>
```

**Routing table**:

| Verdict | Severity | Orchestrator Action |
|---------|----------|---------------------|
| consensus_reached | - | Proceed normally, fast-advance to next task |
| consensus_blocked | LOW | Treat as reached with notes, proceed normally |
| consensus_blocked | MEDIUM | Log warning to `wisdom/issues.md`, include divergence in next task context, proceed |
| consensus_blocked | HIGH | Create revision task (see below) OR pause for user |
| consensus_blocked | HIGH (DISCUSS-006) | Always pause for user decision (final sign-off gate) |

**Revision task creation** (HIGH severity, not DISCUSS-006):

```javascript
// Add revision entry to state file
const revisionTask = {
  id: "<original-task-id>-R1",
  owner: "<same-agent-role>",
  blocked_by: [],
  description: "Revision of <original-task-id>: address consensus-blocked divergences.\n"
    + "Session: <session-dir>\n"
    + "Original artifact: <artifact-path>\n"
    + "Divergences: <divergence-details>\n"
    + "Action items: <action-items-from-discuss>\n"
    + "InlineDiscuss: <same-round-id>",
  status: "pending",
  is_revision: true
}

// Max 1 revision per task. If already revised once, pause for user.
if (stateHasRevision(originalTaskId)) {
  // Pause pipeline, ask user
} else {
  // Insert revision task into state, spawn agent
}
```

---

## Phase Execution

| Phase | File | Summary |
|-------|------|---------|
| Phase 1 | [phases/01-requirement-clarification.md](phases/01-requirement-clarification.md) | Parse user input, detect mode, frontend auto-detection, gather parameters |
| Phase 2 | [phases/02-team-initialization.md](phases/02-team-initialization.md) | Create session directory, initialize state file, wisdom, explore cache |
| Phase 3 | [phases/03-task-chain-creation.md](phases/03-task-chain-creation.md) | Build pipeline task chain based on mode, write to state file |
| Phase 4 | [phases/04-pipeline-coordination.md](phases/04-pipeline-coordination.md) | Main spawn/wait/close loop, fast-advance, consensus routing, checkpoints |
| Phase 5 | [phases/05-completion-report.md](phases/05-completion-report.md) | Summarize results, list artifacts, offer next steps |

### Phase 0: Session Resume Check (before Phase 1)

Before entering Phase 1, the orchestrator checks for interrupted sessions:

1. Scan `.workflow/.team/TLS-*/team-session.json` for files with `status: "active"` or `status: "paused"`
2. No sessions found -> proceed to Phase 1
3. Single session found -> resume it (Session Reconciliation below)
4. Multiple sessions found -> ask user to select

**Session Reconciliation** (when resuming):

1. Read state file -> get pipeline state
2. For each task in state file:
   - If status is "in_progress" but no agent is running -> reset to "pending" (interrupted)
   - If status is "completed" -> verify artifact exists
3. Rebuild task readiness from reconciled state
4. Proceed to Phase 4 with reconciled state (spawn ready tasks)

---

## Pipeline Definitions

### Spec-only (6 beats)

```
RESEARCH-001(+D1) -> DRAFT-001(+D2) -> DRAFT-002(+D3) -> DRAFT-003(+D4) -> DRAFT-004(+D5) -> QUALITY-001(+D6)
```

Each task includes inline discuss. `(+DN)` = inline discuss round N executed by the agent internally.

### Impl-only (3 beats with parallel window)

```
PLAN-001 -> IMPL-001 -> TEST-001 || REVIEW-001
```

TEST-001 and REVIEW-001 run in parallel after IMPL-001 completes.

### Full-lifecycle (9 beats)

```
[Spec pipeline: RESEARCH-001 -> DRAFT-001 -> ... -> QUALITY-001]
    |
    CHECKPOINT: pause for user confirmation
    |
PLAN-001(blockedBy: QUALITY-001) -> IMPL-001 -> TEST-001 || REVIEW-001
```

### FE-only (3 beats)

```
PLAN-001 -> DEV-FE-001 -> QA-FE-001
```

GC loop: if QA-FE verdict is NEEDS_FIX, dynamically create DEV-FE-002 -> QA-FE-002 (max 2 rounds).

### Fullstack (4 beats with dual parallel)

```
PLAN-001 -> IMPL-001 || DEV-FE-001 -> TEST-001 || QA-FE-001 -> REVIEW-001
```

REVIEW-001 is blocked by both TEST-001 and QA-FE-001.

### Full-lifecycle-FE (12 tasks)

```
[Spec pipeline] -> PLAN-001 -> IMPL-001 || DEV-FE-001 -> TEST-001 || QA-FE-001 -> REVIEW-001
```

PLAN-001 blockedBy QUALITY-001. Spec-to-impl checkpoint applies.

---

## Task Metadata Registry

| Task ID | Agent | Phase | Dependencies | Description | Inline Discuss |
|---------|-------|-------|-------------|-------------|---------------|
| RESEARCH-001 | analyst | spec | (none) | Seed analysis and context gathering | DISCUSS-001 |
| DRAFT-001 | writer | spec | RESEARCH-001 | Generate Product Brief | DISCUSS-002 |
| DRAFT-002 | writer | spec | DRAFT-001 | Generate Requirements/PRD | DISCUSS-003 |
| DRAFT-003 | writer | spec | DRAFT-002 | Generate Architecture Document | DISCUSS-004 |
| DRAFT-004 | writer | spec | DRAFT-003 | Generate Epics and Stories | DISCUSS-005 |
| QUALITY-001 | reviewer | spec | DRAFT-004 | 5-dimension spec quality + sign-off | DISCUSS-006 |
| PLAN-001 | planner | impl | (none or QUALITY-001) | Multi-angle exploration and planning | - |
| IMPL-001 | executor | impl | PLAN-001 | Code implementation | - |
| TEST-001 | tester | impl | IMPL-001 | Test-fix cycles | - |
| REVIEW-001 | reviewer | impl | IMPL-001 | 4-dimension code review | - |
| DEV-FE-001 | fe-developer | impl | PLAN-001 | Frontend implementation | - |
| QA-FE-001 | fe-qa | impl | DEV-FE-001 | 5-dimension frontend QA | - |

---

## Cadence Control

### Beat Model

Event-driven pipeline. Each beat = orchestrator processes one event -> spawns agent(s) -> waits -> processes result -> yields.

```
Beat Cycle (single beat)
======================================================================
  Event                 Orchestrator                  Agents
----------------------------------------------------------------------
  advance/resume --> +- read state file ------+
                     |  find ready tasks       |
                     |  spawn agent(s) --------+--> [Agent A] executes
                     |  wait(ids, timeout) ----+--> [Agent B] executes
                     +- process results -------+         |
                     |  update state file      |         |
                     |  close agents           |         |
                     +- yield -----------------+         |
                                                         |
  next beat <--- result from wait() <-------------------+
======================================================================

  Fast-Advance (skips full yield for linear successors)
======================================================================
  [Agent A] completes via wait()
    +- 1 ready task? simple linear successor?
    |   YES -> spawn Agent B immediately, enter wait() again
    |   NO  -> yield, wait for user/event
======================================================================
```

### Pipeline Beat View

```
Spec-only (6 beats, was 12 in v3)
-------------------------------------------------------
Beat  1         2         3         4         5         6
      |         |         |         |         |         |
    R1+D1 --> W1+D2 --> W2+D3 --> W3+D4 --> W4+D5 --> Q1+D6
    ^                                                     ^
  pipeline                                            sign-off
   start                                               pause

R=RESEARCH  W=DRAFT(writer)  Q=QUALITY  D=DISCUSS(inline)

Impl-only (3 beats, with parallel window)
-------------------------------------------------------
Beat  1         2              3
      |         |         +----+----+
      PLAN --> IMPL --> TEST || REVIEW    <-- parallel window
                         +----+----+
                           pipeline
                            done

Full-lifecycle (9 beats)
-------------------------------------------------------
Beat 1-6: [Spec pipeline as above]
                                    |
Beat 6 (Q1+D6 done):      CHECKPOINT -- user confirms then resume
                                    |
Beat 7      8           9
 PLAN --> IMPL --> TEST || REVIEW

Fullstack (with dual parallel windows)
-------------------------------------------------------
Beat  1              2                    3                4
      |         +----+----+         +----+----+           |
      PLAN --> IMPL || DEV-FE --> TEST || QA-FE -->  REVIEW
              ^                ^                   ^
         parallel 1       parallel 2          sync barrier
```

### Checkpoints

| Trigger | Position | Behavior |
|---------|----------|----------|
| Spec-to-impl transition | QUALITY-001 completed | Pause, output "SPEC PHASE COMPLETE", wait for user |
| GC loop max reached | QA-FE max 2 rounds | Stop iteration, report current QA state |
| Pipeline stall | No ready + no running | Check for missing tasks, report to user |
| DISCUSS-006 HIGH severity | Final sign-off | Always pause for user decision |

### Stall Detection

| Check | Condition | Resolution |
|-------|-----------|-----------|
| Agent unresponsive | wait() timeout on active agent | Close agent, reset task to pending, respawn |
| Pipeline deadlock | No ready + no running + has pending | Inspect blocked_by chains, report blockage to user |
| GC loop exceeded | DEV-FE / QA-FE iteration > 2 rounds | Terminate loop, output latest QA report |
| Fast-advance orphan | Task is "in_progress" in state but agent closed | Reset to pending, respawn |

---

## Agent Spawn Template

When the orchestrator spawns an agent for a pipeline task, it uses this template:

```javascript
const agentId = spawn_agent({
  message: `
## TASK ASSIGNMENT

### MANDATORY FIRST STEPS (Agent Execute)
1. **Read role definition**: ~/.codex/agents/<agent-role>.md (MUST read first)
2. Read session state: <session-dir>/team-session.json
3. Read wisdom files: <session-dir>/wisdom/*.md (if exists)

---

## Session
Session directory: <session-dir>
Task ID: <task-id>
Pipeline mode: <mode>

## Scope
<scope-description>

## Task
<task-description>

## InlineDiscuss
<discuss-round-id or "none">

## Dependencies
Completed predecessors: <list of completed task IDs and their artifact paths>

## Constraints
- Only process <PREFIX>-* tasks
- All output prefixed with [<agent-role>] tag
- Write artifacts to <session-dir>/<artifact-subdir>/
- Before each major output, read wisdom files for cross-task knowledge
- After task completion, write discoveries to <session-dir>/wisdom/
- If InlineDiscuss is set, call discuss subagent after primary artifact creation

## Completion Protocol
When work is complete, output EXACTLY:

TASK_COMPLETE:
- task_id: <task-id>
- status: <success | failed>
- artifact: <path-to-primary-artifact>
- discuss_verdict: <consensus_reached | consensus_blocked | none>
- discuss_severity: <HIGH | MEDIUM | LOW | none>
- summary: <one-line summary>
`
})
```

---

## Session Directory

```
.workflow/.team/TLS-<slug>-<date>/
+-- team-session.json           # Pipeline state (replaces TaskCreate/TaskList)
+-- spec/                       # Spec artifacts
|   +-- spec-config.json
|   +-- discovery-context.json
|   +-- product-brief.md
|   +-- requirements/
|   +-- architecture/
|   +-- epics/
|   +-- readiness-report.md
|   +-- spec-summary.md
+-- discussions/                # Discussion records (written by discuss subagent)
+-- plan/                       # Plan artifacts
|   +-- plan.json
|   +-- tasks/                  # Detailed task specs
+-- explorations/               # Shared explore cache
|   +-- cache-index.json        # { angle -> file_path }
|   +-- explore-<angle>.json
+-- architecture/               # Architect assessments + design-tokens.json
+-- analysis/                   # Analyst design-intelligence.json (UI mode)
+-- qa/                         # QA audit reports
+-- wisdom/                     # Cross-task knowledge accumulation
|   +-- learnings.md            # Patterns and insights
|   +-- decisions.md            # Architecture and design decisions
|   +-- conventions.md          # Codebase conventions
|   +-- issues.md               # Known risks and issues
+-- .msg/                       # Message bus (UI integration)
|   +-- meta.json               # Pipeline metadata (stages, roles, team_name)
|   +-- messages.jsonl          # NDJSON event log
+-- shared-memory.json          # Cross-agent state
```

---

## State File Schema (team-session.json)

The state file replaces Claude's TaskCreate/TaskList/TaskGet/TaskUpdate system. The orchestrator owns this file exclusively.

```json
{
  "session_id": "TLS-<slug>-<date>",
  "mode": "<spec-only | impl-only | full-lifecycle | fe-only | fullstack | full-lifecycle-fe>",
  "scope": "<project description>",
  "status": "<active | paused | completed>",
  "started_at": "<ISO8601>",
  "updated_at": "<ISO8601>",
  "tasks_total": 0,
  "tasks_completed": 0,
  "pipeline": [
    {
      "id": "RESEARCH-001",
      "owner": "analyst",
      "status": "pending | in_progress | completed | failed",
      "blocked_by": [],
      "description": "...",
      "inline_discuss": "DISCUSS-001",
      "agent_id": null,
      "artifact_path": null,
      "discuss_verdict": null,
      "discuss_severity": null,
      "started_at": null,
      "completed_at": null,
      "revision_of": null,
      "revision_count": 0
    }
  ],
  "active_agents": [],
  "completed_tasks": [],
  "revision_chains": {},
  "wisdom_entries": [],
  "checkpoints_hit": [],
  "gc_loop_count": 0
}
```

---

## Message Bus (.msg/)

The `.msg/` directory provides pipeline metadata for the frontend UI. This is the **same format** used by Claude version's `team_msg` tool with `type: "state_update"`.

### meta.json

Pipeline metadata read by the API for frontend display:

```json
{
  "status": "active",
  "pipeline_mode": "<mode>",
  "pipeline_stages": ["role1", "role2", "..."],
  "roles": ["coordinator", "role1", "role2", "..."],
  "team_name": "lifecycle",
  "role_state": {
    "<role>": {
      "status": "completed",
      "task_id": "TASK-ID",
      "_updated_at": "<ISO8601>"
    }
  },
  "updated_at": "<ISO8601>"
}
```

**pipeline_stages by mode**:

| Mode | pipeline_stages |
|------|-----------------|
| spec-only | `["analyst", "writer", "reviewer"]` |
| impl-only | `["planner", "executor", "tester", "reviewer"]` |
| fe-only | `["planner", "fe-developer", "fe-qa"]` |
| fullstack | `["planner", "executor", "fe-developer", "tester", "fe-qa", "reviewer"]` |
| full-lifecycle | `["analyst", "writer", "planner", "executor", "tester", "reviewer"]` |
| full-lifecycle-fe | `["analyst", "writer", "planner", "executor", "fe-developer", "tester", "fe-qa", "reviewer"]` |

### messages.jsonl

NDJSON event log (one JSON object per line):

```json
{"id":"MSG-001","ts":"<ISO8601>","from":"coordinator","to":"coordinator","type":"state_update","summary":"Session initialized","data":{...}}
{"id":"MSG-002","ts":"<ISO8601>","from":"analyst","to":"coordinator","type":"impl_complete","summary":"RESEARCH-001 completed","data":{...}}
```

**Message types**: `state_update`, `impl_complete`, `impl_progress`, `test_result`, `review_result`, `error`, `shutdown`

---

## Session Resume

When the orchestrator detects an existing active/paused session:

1. Read `team-session.json` from session directory
2. For each task with status "in_progress":
   - No matching active agent -> task was interrupted -> reset to "pending"
   - Has matching active agent -> verify agent is still alive (attempt wait with 0 timeout)
3. Reconcile: ensure all expected tasks for the mode exist in state
4. Create missing tasks with correct blocked_by dependencies
5. Verify dependency chain integrity (no cycles, no dangling references)
6. Update state file with reconciled state
7. Proceed to Phase 4 to spawn ready tasks

---

## User Commands

During pipeline execution, the user may issue commands:

| Command | Action |
|---------|--------|
| `check` / `status` | Output execution status graph (read-only, no advancement) |
| `resume` / `continue` | Check agent states, advance pipeline |
| New session request | Phase 0 detects, enters normal Phase 1-5 flow |

**Status graph output format**:

```
[orchestrator] Pipeline Status
[orchestrator] Mode: <mode> | Progress: <completed>/<total> (<percent>%)

[orchestrator] Execution Graph:
  Spec Phase: (if applicable)
    [V RESEARCH-001(+D1)] -> [V DRAFT-001(+D2)] -> [>>> DRAFT-002(+D3)]
    -> [o DRAFT-003(+D4)] -> [o DRAFT-004(+D5)] -> [o QUALITY-001(+D6)]
  Impl Phase: (if applicable)
    [o PLAN-001]
      +- BE: [o IMPL-001] -> [o TEST-001] -> [o REVIEW-001]
      +- FE: [o DEV-FE-001] -> [o QA-FE-001]

  V=completed  >>>=running  o=pending  .=not created

[orchestrator] Active Agents:
  > <task-id> (<agent-role>) - running <elapsed>

[orchestrator] Ready to spawn: <task-ids>
[orchestrator] Commands: 'resume' to advance | 'check' to refresh
```

---

## Lifecycle Management

### Timeout Protocol

| Phase | Timeout | On Timeout |
|-------|---------|------------|
| Phase 1 (requirements) | None (interactive) | N/A |
| Phase 2 (init) | 60s | Fail with error |
| Phase 3 (dispatch) | 60s | Fail with error |
| Phase 4 per agent | 15 min (spec agents), 30 min (impl agents) | Send convergence request via `send_input`, wait 2 min more, then close |
| Phase 5 (report) | 60s | Output partial report |

**Convergence request** (sent via `send_input` on timeout):

```javascript
send_input({
  id: <agent-id>,
  message: `
## TIMEOUT NOTIFICATION

Execution timeout reached. Please:
1. Save all current progress to artifact files
2. Output TASK_COMPLETE with status: partial
3. Include summary of completed vs remaining work
`
})
```

### Cleanup Protocol

When the pipeline completes (or is aborted):

```javascript
// Close all active agents
for (const agentEntry of state.active_agents) {
  try {
    close_agent({ id: agentEntry.agent_id })
  } catch (e) {
    // Agent already closed, ignore
  }
}

// Update state file
state.status = "completed"  // or "aborted"
state.updated_at = new Date().toISOString()
// Write state file
```

---

## Error Handling

| Scenario | Detection | Resolution |
|----------|-----------|------------|
| Agent timeout | wait() returns timed_out | send_input convergence request, retry wait 2 min, then close + reset task |
| Agent crash / unexpected close | wait() returns error status | Reset task to pending, respawn agent (max 3 retries) |
| 3+ failures on same task | Retry count in state file | Pause pipeline, report to user |
| Fast-advance orphan | Task in_progress but no active agent and > 5 min elapsed | Reset to pending, respawn |
| Consensus blocked HIGH | DISCUSS_RESULT parsed from agent output | Create revision task (max 1) or pause |
| Consensus blocked HIGH on DISCUSS-006 | Same as above but final sign-off round | Always pause for user |
| Revision also blocked | Revision task returns blocked HIGH | Pause pipeline, escalate to user |
| Session file corrupt | JSON parse error | Attempt recovery from last known good state, or report error |
| Pipeline stall | No ready + no running + has pending | Inspect blocked_by, report blockage details |
| Unknown agent output format | TASK_COMPLETE not found in wait result | Log warning, attempt to extract status, mark as partial |
| Duplicate task in state | Task ID already exists during dispatch | Skip creation, log warning |
| Missing dependency | blocked_by references non-existent task | Log error, halt pipeline |

---

## Frontend Auto-Detection

During Phase 1, the orchestrator detects whether frontend work is needed:

| Signal | Detection | Pipeline Upgrade |
|--------|----------|-----------------|
| FE keywords in description | Match: component, page, UI, React, Vue, CSS, HTML, Tailwind, Svelte, Next.js, Nuxt, shadcn, design system | impl-only -> fe-only or fullstack |
| BE keywords also present | Match: API, database, server, endpoint, backend, middleware | impl-only -> fullstack |
| FE framework in project | Detect react/vue/svelte/next in package.json | full-lifecycle -> full-lifecycle-fe |

---

## Inline Discuss Protocol (for agents)

Produce agents (analyst, writer, reviewer) call the discuss subagent after completing their primary artifact. The protocol is documented here for reference; each agent's role file contains the specific invocation.

**Discussion round mapping**:

| Agent | After Task | Discuss Round | Perspectives |
|-------|-----------|---------------|-------------|
| analyst | RESEARCH-001 | DISCUSS-001 | product, risk, coverage |
| writer | DRAFT-001 | DISCUSS-002 | product, technical, quality, coverage |
| writer | DRAFT-002 | DISCUSS-003 | quality, product, coverage |
| writer | DRAFT-003 | DISCUSS-004 | technical, risk |
| writer | DRAFT-004 | DISCUSS-005 | product, technical, quality, coverage |
| reviewer | QUALITY-001 | DISCUSS-006 | all 5 (product, technical, quality, risk, coverage) |

**Agent-side discuss invocation** (inside the agent, not orchestrator):

```javascript
// Agent spawns discuss subagent internally
const discussId = spawn_agent({
  message: `
## MANDATORY FIRST STEPS (Agent Execute)
1. **Read agent definition**: ~/.codex/agents/discuss-agent.md (MUST read first)

---

## Multi-Perspective Critique: <round-id>

### Input
- Artifact: <artifact-path>
- Round: <round-id>
- Perspectives: <perspective-list>
- Session: <session-dir>
- Discovery Context: <session-dir>/spec/discovery-context.json

### Execution
Per-perspective CLI analysis -> divergence detection -> consensus determination -> write record.

### Output
Write discussion record to: <session-dir>/discussions/<round-id>-discussion.md
Return verdict summary with: verdict, severity, average_rating, action_items, recommendation.
`
})

const discussResult = wait({ ids: [discussId], timeout_ms: 300000 })
close_agent({ id: discussId })
// Agent includes discuss result in its TASK_COMPLETE output
```

---

## Shared Explore Protocol (for agents)

Any agent needing codebase context calls the explore subagent. Results are cached in `explorations/`.

**Agent-side explore invocation** (inside the agent, not orchestrator):

```javascript
// Agent spawns explore subagent internally
const exploreId = spawn_agent({
  message: `
## MANDATORY FIRST STEPS (Agent Execute)
1. **Read agent definition**: ~/.codex/agents/explore-agent.md (MUST read first)

---

## Explore Codebase

Query: <query>
Focus angle: <angle>
Keywords: <keyword-list>
Session folder: <session-dir>

## Cache Check
1. Read <session-dir>/explorations/cache-index.json (if exists)
2. If matching angle found AND file exists -> return cached result
3. If not found -> proceed to exploration

## Output
Write JSON to: <session-dir>/explorations/explore-<angle>.json
Update cache-index.json with new entry.
Return summary: file count, pattern count, top 5 files, output path.
`
})

const exploreResult = wait({ ids: [exploreId], timeout_ms: 300000 })
close_agent({ id: exploreId })
```

**Cache lookup rules**:

| Condition | Action |
|-----------|--------|
| Exact angle match exists in cache-index.json | Return cached result |
| No match | Execute exploration, cache result |
| Cache file missing but index has entry | Remove stale entry, re-explore |

---

## Wisdom Accumulation

Cross-task knowledge accumulation. Orchestrator creates `wisdom/` at session init.

**Directory**:

```
<session-dir>/wisdom/
+-- learnings.md      # Patterns and insights discovered
+-- decisions.md      # Architecture and design decisions made
+-- conventions.md    # Codebase conventions identified
+-- issues.md         # Known risks and issues flagged
```

**Agent responsibilities**:
- On start: read all wisdom files for cross-task context
- During work: append discoveries to appropriate wisdom file
- On complete: include significant findings in TASK_COMPLETE summary

---

## Role Isolation Rules

| Allowed | Prohibited |
|---------|-----------|
| Agent processes only its own prefix tasks | Processing other agents' tasks |
| Agent communicates results via TASK_COMPLETE output | Direct agent-to-agent communication |
| Agent calls discuss/explore subagents internally | Agent modifying orchestrator state file |
| Agent writes artifacts to its designated directory | Agent writing to other agents' directories |
| Agent reads wisdom files and shared-memory.json | Agent deleting or overwriting other agents' artifacts |

Orchestrator additionally prohibited: directly write/modify code, call implementation tools, execute analysis/test/review work.

---

## GC Loop (Frontend QA)

For FE pipelines, QA-FE may trigger a fix-retest cycle:

```
Round 1: DEV-FE-001 -> QA-FE-001
  QA-FE verdict: NEEDS_FIX?
    YES -> Round 2: DEV-FE-002(blocked_by: QA-FE-001) -> QA-FE-002(blocked_by: DEV-FE-002)
    QA-FE-002 verdict: NEEDS_FIX?
      YES -> max rounds reached (2), stop loop, report current state
      NO  -> proceed to next pipeline step
    NO -> proceed to next pipeline step
```

The orchestrator dynamically adds DEV-FE-NNN and QA-FE-NNN tasks to the state file when a GC loop iteration is needed.

---

## Mode-to-Pipeline Quick Reference

| Mode | Total Tasks | First Task | Checkpoint |
|------|-------------|------------|------------|
| spec-only | 6 | RESEARCH-001 | None (QUALITY-001 is final) |
| impl-only | 4 | PLAN-001 | None |
| fe-only | 3 (+GC) | PLAN-001 | None |
| fullstack | 6 | PLAN-001 | None |
| full-lifecycle | 10 | RESEARCH-001 | After QUALITY-001 |
| full-lifecycle-fe | 12 (+GC) | RESEARCH-001 | After QUALITY-001 |

---

## Shared Spec Resources

| Resource | Path (relative to skill) | Usage |
|----------|--------------------------|-------|
| Document Standards | specs/document-standards.md | YAML frontmatter, naming, structure |
| Quality Gates | specs/quality-gates.md | Per-phase quality gates |
| Product Brief Template | templates/product-brief.md | DRAFT-001 |
| Requirements Template | templates/requirements-prd.md | DRAFT-002 |
| Architecture Template | templates/architecture-doc.md | DRAFT-003 |
| Epics Template | templates/epics-template.md | DRAFT-004 |


---

## Coordinator Role Constraints (Main Agent)

**CRITICAL**: The coordinator (main agent executing this skill) is responsible for **orchestration only**, NOT implementation.

15. **Coordinator Does NOT Execute Code**: The main agent MUST NOT write, modify, or implement any code directly. All implementation work is delegated to spawned team agents. The coordinator only:
    - Spawns agents with task assignments
    - Waits for agent callbacks
    - Merges results and coordinates workflow
    - Manages workflow transitions between phases

16. **Patient Waiting is Mandatory**: Agent execution takes significant time (typically 10-30 minutes per phase, sometimes longer). The coordinator MUST:
    - Wait patiently for `wait()` calls to complete
    - NOT skip workflow steps due to perceived delays
    - NOT assume agents have failed just because they're taking time
    - Trust the timeout mechanisms defined in the skill

17. **Use send_input for Clarification**: When agents need guidance or appear stuck, the coordinator MUST:
    - Use `send_input()` to ask questions or provide clarification
    - NOT skip the agent or move to next phase prematurely
    - Give agents opportunity to respond before escalating
    - Example: `send_input({ id: agent_id, message: "Please provide status update or clarify blockers" })`

18. **No Workflow Shortcuts**: The coordinator MUST NOT:
    - Skip phases or stages defined in the workflow
    - Bypass required approval or review steps
    - Execute dependent tasks before prerequisites complete
    - Assume task completion without explicit agent callback
    - Make up or fabricate agent results

19. **Respect Long-Running Processes**: This is a complex multi-agent workflow that requires patience:
    - Total execution time may range from 30-90 minutes or longer
    - Each phase may take 10-30 minutes depending on complexity
    - The coordinator must remain active and attentive throughout the entire process
    - Do not terminate or skip steps due to time concerns
