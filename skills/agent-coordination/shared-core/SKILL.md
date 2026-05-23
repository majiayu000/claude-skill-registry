---
name: shared-core
description: Core orchestration concepts - session structure, status values, heartbeat, commit format. Single source of truth for all Ralph agents.
category: orchestration
---

# Shared Core

> "This is the canonical reference for shared Ralph behavior. Agent-specific docs should reference these rules, not duplicate them."

---

## Single Source of Truth

Workers read lightweight state files, PM syncs with prd.json

### State File Architecture

| File                             | Who Reads         | Who Writes  | Size  | Purpose                            |
| -------------------------------- | ----------------- | ----------- | ----- | ---------------------------------- |
| `current-task-developer.json`    | Developer, PM     | Developer   | ~1KB  | Developer's current task state     |
| `current-task-qa.json`           | QA, PM            | QA          | ~1KB  | QA's current task state            |
| `current-task-techartist.json`   | Tech Artist, PM   | Tech Artist | ~1KB  | Tech Artist's current task state   |
| `current-task-gamedesigner.json` | Game Designer, PM | Game Design | ~1KB  | Game Designer's current task state |
| `current-task-pm.json`           | PM                | PM          | ~2KB  | PM coordinator state               |
| `prd.json`                       | **PM only**       | PM only     | 110KB | Full PRD with all tasks            |

**Key Principle:** Workers NEVER read prd.json. They read only their own state file.

### prd.json Role

**prd.json is now PM-ONLY.** It serves as:

1. **PM's task database** - All tasks, dependencies, priorities
2. **Session state record** - Iteration, max iterations, completion
3. **Sync source** - PM syncs between agent files and PRD

**Workers do NOT read prd.json** because:

- 110KB file bloats context windows
- Workers only need their current task info
- PM handles all coordination decisions

**PM reads both:**

- All agent state files (for worker status)
- prd.json (for task database)

---

## prd.json Schema (PM Reference Only)

### prd.json Schema

```json
{
  "session": {
    "sessionId": "string",
    "startedAt": "ISO-8601",
    "maxIterations": 200,
    "iteration": 0,
    "status": "running|completed|terminated|max_iterations_reached",
    "currentTask": { "id": "string", "status": "string" } | null,
    "stats": { "totalTasks": 0, "completed": 0, "failed": 0, "commits": 0 }
  },
  "agents": {
    "pm": { "status": "idle", "lastSeen": "ISO-8601", "currentTaskId": "string|null" },
    "developer": { "status": "idle", "lastSeen": "ISO-8601", "currentTaskId": "string|null" },
    "qa": { "status": "idle", "lastSeen": "ISO-8601", "currentTaskId": "string|null" },
    "techartist": { "status": "idle", "lastSeen": "ISO-8601", "currentTaskId": "string|null" },
    "gamedesigner": { "status": "idle", "lastSeen": "ISO-8601", "currentTaskId": "string|null" }
  },
  "items": [
    {
      "id": "string",
      "title": "string",
      "category": "architectural|integration|functional|visual|shader|polish",
      "priority": "high|medium|low",
      "status": "pending|assigned|in_progress|awaiting_qa|passed|needs_fixes|blocked|in_retrospective|retrospective_synthesized|playtest_phase|playtest_complete|prd_refinement|task_ready|skill_research|completed",
      "passes": false,
      "agent": "developer|qa|techartist|gamedesigner",
      "dependencies": ["taskId1", "taskId2"],
      "acceptanceCriteria": [],
      "verificationSteps": [],
      "retryCount": 0,
      "bugs": []
    }
  ],
  "backlogFile": "prd_backlog.json"
}
```

### Session Directory

```
.claude/session/
├── current-task-developer.json   # Developer state (read by dev, PM)
├── current-task-qa.json          # QA state (read by qa, PM)
├── current-task-techartist.json  # Tech Artist state (read by ta, PM)
├── current-task-gamedesigner.json # Game Designer state (read by gd, PM)
├── current-task-pm.json          # PM coordinator state
├── handoff-log.json             # Task handoff history
├── continue-loop.flag           # Restart signal
├── work-in-progress.json        # Saved state for resume
├── coordinator-progress.txt     # Human-readable log
└── messages/                    # Message queues (event-driven)
    ├── pm/
    ├── developer/
    ├── qa/
    ├── techartist/
    └── gamedesigner/
```

---

## Unified Status Values (Single Source of Truth)

**This is the authoritative reference for ALL status values in Ralph.**

### Task Status Values (`prd.json.items[{taskId}].status`)

| Status                      | Used By              | Meaning                                   | passes |
| --------------------------- | -------------------- | ----------------------------------------- | ------ |
| `pending`                   | PM                   | Task not yet started                      | false  |
| `assigned`                  | PM                   | Task assigned to worker, waiting to start | false  |
| `in_progress`               | Worker (self-report) | Worker actively working                   | false  |
| `awaiting_qa`               | PM                   | Worker finished, waiting for QA           | false  |
| `passed`                    | QA (set), PM (reads) | **QA PASSED** - triggers retrospective    | true   |
| `needs_fixes`               | PM (after QA fail)   | QA found bugs, reassign                   | false  |
| `blocked`                   | PM                   | Max attempts, manual escalation           | false  |
| `in_retrospective`          | PM                   | Worker retrospective active               | true   |
| `retrospective_synthesized` | PM                   | Retrospective complete, committed         | true   |
| `playtest_phase`            | PM                   | Game Designer playtest active             | true   |
| `playtest_complete`         | PM                   | Playtest findings reviewed                | true   |
| `prd_refinement`            | PM                   | PRD reorganization in progress            | true   |
| `task_ready`                | PM                   | Ready for skill research                  | true   |
| `skill_research`            | PM                   | PM improving ALL skills                   | true   |
| `completed`                 | PM                   | All phases complete, archived             | true   |

### Agent Status Values (`prd.json.agents.{agent}.status`)

| Status                     | Meaning                       | Who Sets |
| -------------------------- | ----------------------------- | -------- |
| `idle`                     | Agent not working             | Self/PM  |
| `working`                  | Agent actively working        | Self     |
| `working_on_retrospective` | Contributing to retrospective | Self     |
| `awaiting_pm`              | Waiting for PM response       | Self     |
| `awaiting_gd`              | Waiting for Game Designer     | Self     |
| `waiting`                  | General waiting state         | Self     |

### Status Transition Rules

1. **Only PM sets task status** (except `in_progress` - workers self-report)
2. **Only QA sets `passed`** (PM then transitions to `in_retrospective`)
3. **Only PM transitions to `completed`** (after skill_research)

---

## Task Status Flow Diagrams

### Core Task Flow (Implementation)

```
pending → assigned → in_progress → awaiting_qa → passed
                                        ↓
                                   needs_fixes
                                        ↓
                                   blocked (after max attempts)
```

### Post-Validation Phased Workflow

```
passed
  → prd_refinement (PM reorganizes PRD and PRD Backlog)
  → task_ready
  → skill_research (PM improves skills IF needed)
  → completed (archived)
```

---

### For PM Coordinator

**PM reads both agent state files AND prd.json.**

**After processing each message:**

1. Read all agent state files to update Worker Status Summary
2. Sync changes to prd.json.agents section
3. Update prd.json if task status changes

**PM heartbeat pattern:**

- Update current-task-pm.md with coordinator status
- Sync to prd.json.agents.pm
- Update lastSeen timestamp

### Event-Driven Mode Exit Sequence

In event-driven mode, agents exit after work:

```
1. Complete your work
2. Determine exit status:
   - "idle" - Done
   - "awaiting_pm" - Sent question to PM
   - "awaiting_gd" - Sent question to Game Designer
3. Send status_update message
4. Exit
```

**The status_update message is critical** - tells supervisor your actual state.

---

## Exit Conditions

**Workers MUST check coordinator status every poll and exit when:**

| Condition                                                                          | Action          |
| ---------------------------------------------------------------------------------- | --------------- |
| `current-task-{agent}.json` shows `session.state.status: "completed"`              | Exit gracefully |
| `current-task-{agent}.json` shows `session.state.status: "terminated"`             | Exit gracefully |
| `current-task-{agent}.json` shows `session.state.status: "max_iterations_reached"` | Exit gracefully |
| Detected `<promise>RALPH_COMPLETE</promise>`                                       | Exit gracefully |

**For PM Coordinator:** Read `current-task-pm.json` for session status, or prd.json.session.

---

## Commit Format (Universal)

```
[ralph] [{{AGENT}}] {{PRD_ID}}: {{Brief description}}

- Change 1
- Change 2

PRD: {{PRD_ID}} | Agent: {{AGENT}} | Iteration: {{N}}
```

### Universal Commit Rule

**CRITICAL: Every agent MUST commit their file changes.**

### When to Commit

| When                              | Must Commit? |
| --------------------------------- | ------------ |
| Source file modifications         | ✅ Yes       |
| Configuration changes             | ✅ Yes       |
| PRD updates                       | ✅ Yes       |
| Documentation changes             | ✅ Yes       |
| Skill file updates                | ✅ Yes       |
| Heartbeat updates (lastSeen only) | ❌ No        |
| Temporary message files           | ❌ No        |

### Each Agent's Commit Scope

| Agent             | Must Commit These Files                                                             |
| ----------------- | ----------------------------------------------------------------------------------- |
| **PM**            | `prd.json`, `.claude/session/coordinator-progress.txt`, skill files, retrospectives |
| **Developer**     | Source files, tests, own progress files                                             |
| **Tech Artist**   | Assets, shaders, visual components, own progress files                              |
| **QA**            | `prd.json` (validation fields), bug reports, own progress files                     |
| **Game Designer** | `docs/design/`, GDD, own progress files                                             |

---
