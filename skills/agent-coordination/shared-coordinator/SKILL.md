---
name: shared-coordinator
description: PM coordinator for both event-driven and single-agent orchestration modes
category: orchestration
---

# Shared Coordinator

> "PM coordinates tasks, assigns work, monitors health, runs retrospectives."

**This skill covers coordinator behavior for both orchestration modes:**

- Event-driven mode — Parallel agents, message-based communication
- Single-agent mode — Sequential agents, handoff-based communication

**For complete PM workflow, see `pm-workflow` skill.**

---

## Coordinator Role Overview

As PM coordinator, you:

1. **Select tasks** from PRD based on priority and dependencies
2. **Assign tasks** to workers (Developer, QA, TechArtist, GameDesigner)
3. **Monitor worker health** via agent state files (`current-task-*.md`)
4. **Sync state** between agent files and prd.json (PM-ONLY access)
5. **Track completion** through task status and QA validation
6. **Run retrospectives** after each completed task
7. **Detect session completion** when all tasks pass

**Key Points:**

- Workers update their own `current-task-{agent}.md` files
- PM reads all agent state files to monitor status
- PM syncs changes to `prd.json.agents.*` section
- Workers NEVER read prd.json (saves ~109KB per read)

---

### Startup (First Run)

Create session directory and initialize state files:

```bash
# Create session directory
mkdir -p .claude/session/messages/{pm,developer,qa,techartist,gamedesigner,watchdog}

# Initialize handoff-log.json
{ "handoffs": [] }

# Initialize coordinator-progress.txt
# (See Progress Logging section below)
```

### Idle Behavior (When No Active Task)

**When `prd.json.session.currentTask` is null OR `status === "passed"`:**

1. **Update heartbeat** (every 30 seconds):

   ```json
   {
     "agents": {
       "pm": {
         "lastSeen": "{NOW}",
         "status": "idle"
       }
     }
   }
   ```

2. **Check worker heartbeats** — Log warning if worker not seen in 60+ seconds

3. **Check for completion** — All PRD items `passes: true`?

4. **Select next task** — See Task Selection below

### Task Assignment Flow

**Step 1:** Select task from PRD (see Task Selection Algorithm)

**Step 2:** Read the COMPLETE task from prd.json.items[{taskId}]

**Step 3:** Update agent's state file with FULL task details:

```json
// Read agent's state file
Read: .claude/session/current-task-developer.json

// Update state object
{
  "state": {
    "status": "working",
    "lastSeen": "{NOW}",
    "currentTaskId": "{taskId}",
    "pid": 0
  },
  // Update task fields with COMPLETE task from PRD
  "id": "{taskId}",
  "title": "{FULL_TITLE_FROM_PRD}",
  "description": "{FULL_DESCRIPTION_FROM_PRD}",
  "category": "{category}",
  "priority": "{priority}",
  "tier": "{tier}",
  "status": "assigned",
  "passes": false,
  "agent": "developer",
  "dependencies": [...],
  "gddReference": "{gddReference}",
  "gddVersion": "{gddVersion}",
  "acceptanceCriteria": [...],
  "verificationSteps": [...],
  "retryCount": 0,
  "bugs": [],
  "assignedAt": "{NOW}",
  "completedAt": null
}
```

**Step 4:** Update PRD atomically:

```json
{
  "items": [
    {
      "id": "{taskId}",
      "status": "assigned",
      "agent": "developer",
      "assignedAt": "{NOW}"
    }
  ],
  "agents": {
    "developer": {
      "status": "working",
      "currentTaskId": "{taskId}",
      "lastSeen": "{NOW}"
    }
  },
  "session": {
    "currentTask": {
      "id": "{taskId}",
      "status": "assigned",
      "assignedAt": "{NOW}"
    }
  }
}
```

**Step 5:** Send message to worker's queue:

```json
{
  "id": "msg-developer-{NOW}-001",
  "from": "pm",
  "to": "developer",
  "type": "task_assign",
  "priority": "normal",
  "payload": {
    "taskId": "{taskId}",
    "title": "{TITLE}",
    "acceptanceCriteria": ["..."]
  },
  "timestamp": "{NOW}",
  "status": "pending"
}
```

### Completion Detection

**A task is ONLY complete when:**

1. Developer → `status: "awaiting_qa"`
2. QA validates → `status: "passed"`
3. PM runs retrospective → `currentTask: null`
4. PM marks `prd.json.items[{taskId}].passes: true`

**Session complete when:** ALL PRD items have `passes: true`

---

### Handoff Protocol

When you need another agent, output:

```
HANDOFF:agent_name:base64_context
```

### Startup (First Run)

```bash
# Create session directory
mkdir -p .claude/session

# Initialize prd.json.session
{
  "sessionId": "ralph-single-{TIMESTAMP}",
  "startedAt": "{ISO_TIMESTAMP}",
  "maxIterations": 200,
  "iteration": 0,
  "status": "running",
  "orchestrationMode": "single-agent",
  "currentAgent": "pm",
  "stats": {
    "totalTasks": "{COUNT FROM PRD}",
    "completed": 0,
    "failed": 0
  }
}

# Initialize handoff-log.json
{ "handoffs": [], "orchestrationMode": "single-agent" }
```

### Receiving Handoff Context

If you receive handoff context (from QA or Developer):

1. **Acknowledge** the handoff:

   ```
   Received handoff from [agent]: [reason]
   ```

2. **Read current state files**:
   - `prd.json.session`
   - `prd.json.items` (for task details)
   - `prd.json.agents` (for agent status)

3. **Process based on reason**:

   | Handoff Reason       | Action                              |
   | -------------------- | ----------------------------------- |
   | `validation_passed`  | Mark complete, select next task     |
   | `validation_failed`  | Review bugs, re-assign to developer |
   | `need_clarification` | Answer questions, update specs      |
   | `error`              | Investigate, decide next steps      |

### Task Assignment Flow

1. **Select next task** from PRD
2. **Update `prd.json.items[{taskId}]`**: `status: "assigned"`, `assignedTo: "developer"`
3. **Update `prd.json.session.currentAgent`**: `"developer"`
4. **Update `prd.json.agents.developer`**: `status: "active"`, `currentTask: "{taskId}"`
5. **Save state completely** (CRITICAL before handoff)
6. **Signal ready:** `AGENT_READY_FOR_HANDOFF`
7. **Output handoff phrase:** `HANDOFF:developer:{BASE64_CONTEXT}`

### Processing Validation Results

**When QA hands off with `validation_passed`:**

1. Increment `prd.json.session.iteration`
2. Check max iterations — if `iteration >= maxIterations`: Set `status = "max_iterations_reached"`, output `<promise>RALPH_COMPLETE</promise>`
3. Run retrospective (required before next task)
4. Mark PRD item complete: `passes: true`, `completedAt: "{NOW}"`
5. Check for completion — if ALL items `passes: true`: Output `<promise>RALPH_COMPLETE</promise>`
6. Otherwise: Select and assign next task

**When QA hands off with `validation_failed`:**

1. Increment iteration counter
2. Check max iterations
3. Read bugs from handoff context
4. Update `prd.json.items[{taskId}]` with bug details
5. Handoff to Developer with fix instructions

---

### Status Values

**For complete status reference, see `shared-core` skill.**

Quick reference — `prd.json.session.status`:

- `running` — Session active
- `completed` — All tasks done
- `terminated` — Cancelled
- `max_iterations_reached` — Hit iteration limit

### Iteration Counting

**Each development cycle (assignment → completion) counts as 1 iteration:**

1. Increment `prd.json.session.iteration` after QA validation
2. Check if `iteration >= maxIterations`
3. If at limit, output `<promise>RALPH_COMPLETE</promise>` and set `status = "max_iterations_reached"`

### Progress Logging

Append to `.claude/session/coordinator-progress.txt`:

```markdown
### [{TIMESTAMP}] {TASK_ID}: {TITLE} - COMPLETE

- Implemented by: developer
- Validated by: qa
- Commit: {HASH}

Acceptance criteria:
✓ {CRITERION_1}
✓ {CRITERION_2}
```

### Session Completion Report

When all tasks complete, generate `.claude/session/final-report.md`:

```markdown
# Ralph Session Report

Session: {SESSION_ID}
Started: {START_TIME}
Completed: {END_TIME}
Duration: {DURATION}
Iterations: {TOTAL}

## Summary

✓ {COMPLETED} tasks completed successfully
✓ {COMMITS} commits made
✓ {PASS_RATE}% validation pass rate

## Completed Tasks

{LIST}

## Next Steps

{RECOMMENDATIONS}
```

---

## What PM Controls

| Field                             | You Control       | Notes                                 |
| --------------------------------- | ----------------- | ------------------------------------- |
| `prd.json.session`                | ✅ Full ownership | Session state                         |
| `prd.json.items[{taskId}].status` | ✅ Yes            | Task flow management                  |
| `prd.json.items[{taskId}].passes` | ✅ Yes            | Based on QA validation                |
| `prd.json.items[{taskId}].agent`  | ✅ Yes            | Task assignment                       |
| `prd.json.agents.{agent}`         | ✅ Yes            | **SYNCED from agent state files**     |
| `current-task-pm.json`            | ✅ Full ownership | PM coordinator state                  |
| `current-task-{worker}.md`        | ✅ Read/Write     | **READ** all, **WRITE** on assignment |

**PM's Sync Pattern:**
**CRITICAL: Tasks move between agent state files as they progress through workflow.**

1. **After processing each message:**
   - Read all agent state files
   - Update Worker Status Summary in current-task-pm.json
   - Sync changes to prd.json.agents section

2. **When assigning a task:**
   - Copy COMPLETE task JSON to worker's task fields
   - Update worker's state object
   - Update both state file AND prd.json
   - Send task message

3. **When receiving completion (HANDOFF pattern):**
   - Read agent state file for status
   - **HAND OFF task to next agent's state file** (see below)
   - Update prd.json accordingly

4. **When archiving completed task:**
   - Add to prd_completed.json
   - **CLEAR task from ALL agent state files**
   - Delete from prd.json.items

---

## Exit Conditions

Output `<promise>RALPH_COMPLETE</promise>` when:

- All PRD items have `passes: true`
- QA has completed validation
- **OR** `iteration >= maxIterations`

Stop gracefully when `/cancel-ralph` is invoked.

---
