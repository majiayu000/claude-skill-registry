---
name: shared-message-handling
description: Message delivery and processing via bidirectional named pipes in Ralph V2 event-driven mode. Use when connecting agents to watchdog, sending/receiving messages, or handling message processing loops.
category: infrastructure
tags: [messaging, v2, pipes, event-driven]
dependencies: [shared-ralph-core, shared-ralph-event-protocol]
---

# Message Handling (V2)

> "Messages delivered via named pipes – connect, process, exit, repeat."

## When to Use This Skill

Use **when**:
- Connecting to the watchdog as a Ralph agent
- Sending messages to other agents
- Processing received messages
- Understanding message flow in V2 event-driven mode

Use **proactively**:
- At agent startup to establish connection
- When implementing message handlers
- When debugging communication issues

---

## Quick Start

<examples>
Example 1: PM assigns task to Developer
```
PM sends → { type: "WorkAssign", to: "developer", payload: { taskId: "feat-001" } }
Developer receives → Reads task, begins implementation
```

Example 2: Worker completes work
```
Developer sends → { type: "WorkComplete", to: "pm", payload: { taskId: "feat-001" } }
PM receives → Sets status: "awaiting_qa", forwards to QA
```

Example 3: QA validation result
```
QA sends → { type: "ValidationResult", to: "pm", payload: { passed: true } }
PM receives → Triggers retrospective phase
```
</examples>

---

## Agent Connection

### Step 1: Source Runtime Library

```powershell
. "$PSScriptRoot\..\..\scripts\agent-runtime.ps1"
```

### Step 2: Connect to Watchdog

```powershell
Connect-ToWatchdog -AgentName "developer" -SessionDir ".\.claude\session"
```

### Step 3: Enter Message Loop

```powershell
Enter-AgentLoop -MessageHandler {
    param($Message)

    switch ($Message.type) {
        "WorkAssign" {
            $taskId = $Message.payload.taskId
            # ... do work ...
        }
        "Query" {
            # Handle question
        }
        "System" {
            if ($Message.payload.systemEvent -eq "shutdown") {
                # Loop exits automatically
            }
        }
    }
}
```

---

## Message Types Reference

### PM Receives

| Type | From | Action |
|------|------|--------|
| `WorkComplete` | qa | Trigger retrospective |
| `ProblemReport` | qa | Reassign to worker |
| `Query` | developer/qa | Research and respond |
| `WorkBlocked` | developer/qa | Assess severity, provide guidance |
| `Playtest` | gamedesigner | Review playtest findings |
| `DesignUpdate` | gamedesigner | Incorporate acceptance criteria |
| `ResearchUpdate` | gamedesigner | Review recommendations |
| `Retrospective` | any | Track for completion |
| `AgentStatus` | any | Update agent status |

### Developer Receives

| Type | From | Action |
|------|------|--------|
| `WorkAssign` | pm | Read task, begin implementation |
| `Response` | pm | Use PM guidance, continue |
| `Retrospective` | pm | Contribute to retrospective |
| `ValidationRequest` | qa | Fix bugs found |

### QA Receives

| Type | From | Action |
|------|------|--------|
| `WorkAssign` | pm | Run validation suite |
| `Response` | pm | Use PM guidance |
| `Retrospective` | pm | Contribute to retrospective |

---

## Sending Messages

Use functions from `agent-runtime.ps1`:

```powershell
# Send work complete
Send-WorkComplete -TaskId "feat-001" -Result "success" -Notes "Complete"

# Send query
Send-Message -To "pm" -Type "Query" -Payload @{
    question = "Edge case handling?"
    context = @{ taskId = "feat-001" }
}

# Send problem report
Send-ProblemReport -TaskId "feat-001" -ProblemType "bug" -Severity "high"
```

---

## Message Processing Priority

| Priority | Types | Action |
|----------|-------|--------|
| URGENT | `System` (shutdown), `WorkBlocked` | Immediate attention |
| HIGH | `Query`, `ProblemReport` | Respond promptly |
| NORMAL | `WorkComplete`, `WorkAssign`, `ValidationRequest` | Process in order |
| LOW | `AgentStatus` | Log and continue |

---

## V2 Message Format

```json
{
  "id": "msg-20250125-120000-001",
  "type": "WorkAssign",
  "from": "pm",
  "to": "developer",
  "timestamp": "2025-01-25T12:00:00Z",
  "payload": {
    "taskId": "feat-001",
    "workType": "implementation",
    "title": "Implement feature"
  },
  "inReplyTo": "msg-20250125-115500-042"
}
```

---

## Troubleshooting

### Connection Timeout

- Verify watchdog V2 is running
- Check `.claude/session/` exists
- Ensure pipe name: `ralph-{agent}-main`

### No Messages Received

- Verify PM is sending messages to your agent
- Check watchdog logs: `.claude/session/logs/watchdog.log`
- Verify pipe is connected

### Unexpected Shutdown

- Check for unhandled exceptions in message handler
- Verify event log for crash details
- Supervisor will restart automatically

---

## Anti-Patterns

❌ **DON'T:**
- Use file-based message queues
- Manually create/delete message files
- Poll for messages (loop handles this)
- Stay running after work is complete

✅ **DO:**
- Use `agent-runtime.ps1` for connection
- Use `Enter-AgentLoop` for message processing
- Use `Send-*` functions to send messages
- Exit when work is complete

---

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-ralph-event-protocol` | Complete V2 message protocol |
| `shared-ralph-core` | Session structure |
| `shared-worker-protocol` | Worker exit patterns |
