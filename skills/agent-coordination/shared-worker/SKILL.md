---
name: shared-worker
description: Base worker behavior for all Ralph agents - worker pool model, exit conditions, heartbeat. Extend for agent-specific behavior.
category: orchestration
---

# Shared Worker

> "Complete work, send message, exit. Watchdog orchestrates by spawning agents on demand."

---

## Worker Pool Model

**In event-driven mode, agents do NOT run continuously.**

```
┌─────────────────────────────────────────────────────────────────┐
│                      WATCHDOG (Orchestrator)                     │
│                                                                   │
│  1. Monitor message queues                                       │
│  2. Route messages between agents                                │
│  3. Spawn agent when messages exist in their queue               │
│  4. Wait for agent to exit                                       │
│  5. Respawn agent when new messages arrive                       │
└───────────────────────────┬─────────────────────────────────────┘
                            │
                ┌───────────▼─────────────┐
                │  Message Flow:          │
                │  PM → Workers           │
                │  Workers → PM           │
                │  Workers → Watchdog     │
                └──────────────────────────┘
```

### Agent Lifecycle

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   START     │ ──▶ │  DO WORK     │ ──▶ │   EXIT      │
│ (read       │     │ (complete    │     │ (send       │
│  messages)  │     │  single task) │     │  message)   │
└─────────────┘     └──────────────┘     └─────────────┘
```

**Key Principle:** Each agent run does ONE unit of work, then exits. Watchdog restarts when needed.

---

## Mandatory Exit Check (First Step)

**On EVERY startup, check coordinator status FIRST:**

```bash
# Read prd.json.session
{
  "session": {
    "status": "running|completed|terminated|max_iterations_reached"
  }
}
```

**If status is `completed`, `terminated`, or `max_iterations_reached`:**

1. Update your status to `"exiting"`
2. Log exit to handoff-log.json
3. Output: `<promise>WORKER_EXIT</promise>`
4. Stop

**If status is `running`:** Continue normal workflow.

---

## Startup Workflow

### 1. Check for Pending Messages (MANDATORY)

```bash
# Use Glob to find messages in your inbox
Glob: .claude/session/messages/{your-agent}/msg-*.json

# Read each message using Read tool
# Process based on message type
```

### 2. Send Acknowledgment (MANDATORY)

After reading ANY message, send acknowledgment to watchdog:

```json
{
  "id": "msg-watchdog-{timestamp}-{seq}",
  "from": "{your-agent}",
  "to": "watchdog",
  "type": "message_acknowledged",
  "priority": "normal",
  "payload": {
    "originalMessageId": "{original-message-id}",
    "status": "processed"
  },
  "timestamp": "{ISO-8601-UTC}",
  "status": "pending"
}
```

### 3. Update Heartbeat

Read prd.json, update your `agents.{your-agent}` entry:

```json
{
  "agents": {
    "{your-agent}": {
      "status": "working",
      "currentTaskId": "feat-001",
      "lastSeen": "{ISO-8601-UTC}"
    }
  }
}
```

### 4. Process Messages

| Message Type             | Action                      |
| ------------------------ | --------------------------- |
| `task_assign`            | Begin implementation        |
| `bug_report`             | Fix bugs, re-submit         |
| `answer`                 | Apply response, continue    |
| `validation_request`     | Run validation              |
| `wake_up`                | Resume if idle              |
| `retrospective_initiate` | Contribute to retrospective |
| `shutdown`               | Exit gracefully             |

---

## Working State

### When You Start Working

Update prd.json.agents.{your-agent}:

```json
{
  "status": "working",
  "currentTaskId": "{taskId}",
  "lastSeen": "{NOW}"
}
```

### Heartbeat While Working

**Update heartbeat every 60 seconds** while actively working:

```json
{
  "agents": {
    "{your-agent}": {
      "status": "working",
      "lastSeen": "{NOW}"
    }
  }
}
```

**Quick update pattern:**

1. Read prd.json
2. Update `lastSeen` timestamp
3. Write back

**DO NOT skip heartbeat** - PM needs to know you're alive!

---

## Idle Behavior

**When you have NO assigned task:**

### 1. Update Heartbeat (Every 30 seconds)

```json
{
  "agents": {
    "{your-agent}": {
      "lastSeen": "{NOW}",
      "status": "idle"
    }
  }
}
```

### 2. Poll for Coordinator Status

Read `prd.json.session.status`:

- If `running` → Continue waiting
- If `completed/terminated/max_iterations_reached` → Exit

### 3. Wait 30 Seconds

Repeat until:

- Messages arrive in your queue
- Coordinator status changes to terminal state
- Watchdog spawns you with work

---

## Sending Completion

### When Work Is Complete

**Step 1:** Send completion message to PM

```json
{
  "id": "msg-pm-{timestamp}-{seq}",
  "from": "{your-agent}",
  "to": "pm",
  "type": "task_complete",
  "priority": "normal",
  "payload": {
    "taskId": "{taskId}",
    "success": true,
    "summary": "Implementation complete"
  },
  "timestamp": "{ISO-8601-UTC}",
  "status": "pending"
}
```

**Step 2:** Update status to idle

```json
{
  "agents": {
    "{your-agent}": {
      "status": "idle",
      "currentTaskId": null,
      "lastSeen": "{NOW}"
    }
  }
}
```

**Step 3:** Exit

Watchdog will respawn you when new messages arrive.

---

## When Blocked

**If you need clarification:**

### 1. Send Question to PM

```json
{
  "id": "msg-pm-{timestamp}-{seq}",
  "from": "{your-agent}",
  "to": "pm",
  "type": "question",
  "priority": "high",
  "payload": {
    "question": "How should I handle X?",
    "context": "Current situation..."
  },
  "timestamp": "{ISO-8601-UTC}",
  "status": "pending"
}
```

### 2. Update Status to Awaiting

```json
{
  "agents": {
    "{your-agent}": {
      "status": "awaiting_pm",
      "lastSeen": "{NOW}"
    }
  }
}
```

### 3. Exit

Watchdog has 10-minute timeout (configurable via `RALPH_AWAITING_TIMEOUT`) before alerting PM.

---

## Single Source of Truth (prd.json)

**prd.json is the single source of truth.**

### What You Update

Update `prd.json.agents.{your-agent}`:

| Field           | Description                                     |
| --------------- | ----------------------------------------------- |
| `status`        | `idle`, `working`, `awaiting_pm`, `awaiting_gd` |
| `lastSeen`      | ISO timestamp of last update                    |
| `currentTaskId` | Task you're working on (null if idle)           |

### What PM Controls

- `items[{taskId}].status` — PM updates based on your messages
- `items[{taskId}].passes` — PM updates based on QA validation

---

## Status Reference Summary

**For complete status values, see `shared-core` skill.**

Quick reference:

| Your Status   | When to Use                        |
| ------------- | ---------------------------------- |
| `idle`        | No task assigned, monitoring       |
| `working`     | Actively working on task           |
| `awaiting_pm` | Waiting for PM response            |
| `awaiting_gd` | Waiting for Game Designer response |

---

## Event-Driven vs Sequential Mode

| Aspect           | Event-Driven                         | Sequential                           |
| ---------------- | ------------------------------------ | ------------------------------------ |
| Agent spawning   | Watchdog spawns when messages exist  | One agent at a time, handoff between |
| Message delivery | JSON files in queues                 | Handoff signal file                  |
| Parallel work    | Yes - multiple agents simultaneously | No - agents take turns               |
| Communication    | Read/Write tools with JSON           | File-based handoff                   |

---

## Exit Conditions

**Workers MUST check coordinator status and exit when:**

| Condition                                              | Action          |
| ------------------------------------------------------ | --------------- |
| `prd.json.session.status === "completed"`              | Exit gracefully |
| `prd.json.session.status === "terminated"`             | Exit gracefully |
| `prd.json.session.status === "max_iterations_reached"` | Exit gracefully |
| Watchdog sends `shutdown` message                      | Exit gracefully |

**Output:** `<promise>WORKER_EXIT</promise>`

---

## Context Window Management

**CRITICAL:** Reset context when reaching ~70% capacity.

**Detection:** After large work chunks, check context usage.

**Reset Procedure (Automatic):**

1. Read and save current prd.json state
2. Note your current task
3. Stop-hook will detect reset and continue with fresh context

**After Reset:**

- Re-read prd.json
- Continue from where you left off
- Do NOT repeat completed work

---

## Anti-Patterns

| Don't                       | Do Instead                 |
| --------------------------- | -------------------------- |
| Stay running after work     | Exit immediately           |
| Use loops to poll           | Let watchdog spawn you     |
| Skip heartbeat update       | Update every 30-60 seconds |
| Forget acknowledgment       | Always send to watchdog    |
| Use PowerShell for file ops | Use Glob/Read/Write tools  |

---

## References

- `shared-core` — Status values, heartbeat details, session structure
- `shared-messaging` — Message formats, acknowledgment protocol
- `shared-state` — File ownership, atomic updates (Edit tool)
- `shared-context` — Context window auto-reset procedures
