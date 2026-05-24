---
name: shared-worker-protocol
description: Worker pool architecture with ActorSupervisor spawning agents. Use proactively when implementing worker agent behavior or understanding exit patterns.
category: orchestration
tags: [actor-model, supervisor, worker, exit, lifecycle]
dependencies: [shared-ralph-event-protocol, shared-message-handling, shared-ralph-core]
---

# Worker Protocol

> "Complete work, send message via pipe, exit. Supervisor restarts if needed."

## When to Use This Skill

Use **when**:
- Implementing worker agent behavior
- Understanding when/how to exit
- Understanding supervisor auto-restart

Use **proactively**:
- Reference before implementing agent message loops
- After completing work, before exiting

---

## Quick Start

<examples>
Example 1: Agent connection and message loop
```powershell
# Source runtime library
. "$PSScriptRoot\..\..\scripts\agent-runtime.ps1"

# Connect to watchdog
Connect-ToWatchdog -AgentName "developer" -SessionDir ".\.claude\session"

# Enter message loop
Enter-AgentLoop -MessageHandler {
    param($Message)
    switch ($Message.type) {
        "WorkAssign" {
            Send-WorkComplete -TaskId $Message.payload.taskId -Result "success"
        }
    }
}
```

Example 2: Send work complete
```powershell
Send-WorkComplete -TaskId "feat-001" -Result "success" -Notes "Complete"
```

Example 3: Exit conditions
- Work complete → `WorkComplete` → Exit (code 0)
- Need clarification → `Query` → Exit (code 0)
- Shutdown received → Exit (code 42)
```
</examples>

---

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              ACTOR SUPERVISOR (Watchdog)                      │
│  1. StartActor(agentName) - creates bidirectional pipe       │
│  2. Wait for agent connection via agent-runtime.ps1          │
│  3. Supervise() - check for crashes, restart with backoff    │
│  4. Route messages between agents via pipes                  │
│  5. StopAll() - graceful shutdown                            │
└───────────────────────────┬───────────────────────────────────┘
                            │
                ┌───────────▼─────────────┐
                │  PM ↔ Workers (pipes)   │
                │  Event Log (source)     │
                └──────────────────────────┘
```

---

## Agent Lifecycle

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   CONNECT   │ ──▶ │  DO WORK     │ ──▶ │   EXIT      │
│ (agent-     │     │ (receive via │     │ (supervisor  │
│  runtime)   │     │  pipe,       │     │  may restart)│
└─────────────┘     │  process)    │     └─────────────┘
                    └──────────────┘
```

**Key Principle**: Each agent run processes messages, completes work, exits. Supervisor restarts when needed.

---

## Event-Driven vs Sequential Mode

| Aspect | Event-Driven | Sequential |
|--------|-------------|------------|
| Agent spawning | On demand | One at a time |
| Message delivery | Named pipes | Handoff file |
| Parallel work | Yes | No |
| Startup | `/ralph-coordinator-event` | `/ralph-coordinator-single` |
| Connection | `agent-runtime.ps1` | Handoff files |

---

## Exit Conditions

| Condition | Action | Exit Code | Restarted |
|-----------|--------|-----------|-----------|
| Work complete | Send `WorkComplete` | 0 | No (new task will spawn) |
| Need clarification | Send `Query` | 0 | No |
| Blocking issue | Send `WorkBlocked` | 0 | No |
| Shutdown received | - | 42 | No |
| Crash | - | Non-zero | Yes (with backoff) |

**Supervisor restart strategy**:
- Exponential backoff: 5s, 10s, 20s, 40s, 60s (max)
- Max 3 restarts per agent
- Graceful exits (0 or 42) are not restarted

---

## V2 vs V1

| Aspect | V1 (Legacy) | V2 (Current) |
|--------|-------------|--------------|
| Agent lifecycle | File queue monitoring | Pipe-based event loop |
| Delivery latency | 2-5 seconds | <10 milliseconds |
| Crash recovery | Manual health checks | Automatic (ActorSupervisor) |
| State persistence | Multiple files | Single event log |
| Message types | 47+ types | 12 core types |
| Restart strategy | None | Exponential backoff |

---

## Complete Worker Example

```powershell
# Source runtime library
. "$PSScriptRoot\..\..\scripts\agent-runtime.ps1"

# Connect to watchdog
$connected = Connect-ToWatchdog -AgentName "developer" -SessionDir ".\.claude\session"
if (-not $connected) { exit 1 }

# Enter message loop
Enter-AgentLoop -MessageHandler {
    param($Message)

    switch ($Message.type) {
        "WorkAssign" {
            $taskId = $Message.payload.taskId
            # Do work...
            Send-WorkComplete -TaskId $taskId -Result "success"
        }
        "Query" {
            Send-Message -To "pm" -Type "Response" -Payload @{
                answer = "Here's the answer..."
            } -InReplyTo $Message.id
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

## Related Skills

| Skill | Purpose |
|-------|---------|
| `shared-ralph-event-protocol` | V2 message protocol |
| `shared-message-handling` | V2 message delivery |
| `shared-ralph-core` | Core instructions |
