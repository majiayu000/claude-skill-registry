---
name: ralph-handoff
description: Handoff protocol for single-agent orchestration mode
category: orchestration
---

# Ralph Handoff Protocol

This skill defines how agents communicate handoff requests in single-agent orchestration mode. Only ONE agent is active at a time - the watchdog process monitors agent output and orchestrates handoffs.

## Overview

Instead of 3 agents polling simultaneously (consuming tokens continuously), this model:

1. Runs ONE agent at a time
2. Agent outputs handoff phrase when work is complete or another agent is needed
3. Watchdog detects handoff, gracefully stops current agent, starts next agent
4. Context is passed to next agent via state files + handoff message

## Handoff Phrase Format

When you need another agent to take over, output this exact format:

```
HANDOFF:agent_name:base64_context
```

Where:

- `agent_name` is one of: `pm`, `developer`, `qa`
- `base64_context` is a Base64-encoded JSON object with handoff details

### Example

```
HANDOFF:developer:eyJmcm9tIjoicG0iLCJyZWFzb24iOiJ0YXNrX2Fzc2lnbm1lbnQiLCJ0YXNrIjp7ImlkIjoiZmVhdC0wMDEiLCJ0aXRsZSI6IkFkZCB1c2VyIGF1dGgiLCJwcmlvcml0eSI6ImhpZ2gifX0=
```

## Context JSON Structure

The context object should include:

```json
{
  "from": "pm", // Your agent name
  "reason": "task_assignment", // Why handoff is needed
  "timestamp": "2026-01-20T...", // When you're handing off
  "task": {
    // Task-specific details
    "id": "feat-001",
    "title": "Add user authentication",
    "action": "implement", // What the next agent should do
    "notes": "Focus on JWT tokens" // Any additional context
  }
}
```

## Handoff Reasons

| Reason               | From      | To        | Description                                     |
| -------------------- | --------- | --------- | ----------------------------------------------- |
| `task_assignment`    | PM        | Developer | New task assigned for implementation            |
| `ready_for_qa`       | Developer | QA        | Implementation complete, needs validation       |
| `validation_passed`  | QA        | PM        | Tests passed, task complete                     |
| `validation_failed`  | QA        | Developer | Bugs found, needs fixes                         |
| `need_clarification` | Developer | PM        | Questions about specs                           |
| `all_complete`       | PM        | -         | All PRD items done (use RALPH_COMPLETE instead) |

## Before Handoff: Save State

**CRITICAL**: Before outputting a handoff phrase, you MUST:

1. **Save all state to files**:
   - Update `prd.json.session` with current status
   - Update `prd.json.items[{taskId}]` with task progress
   - Update `prd.json.agents.{agent}` with your agent status
   - Commit any code changes (Developer only)

2. **Signal readiness**:

   ```
   AGENT_READY_FOR_HANDOFF
   ```

3. **Output handoff phrase**:
   ```
   HANDOFF:next_agent:context
   ```

The watchdog waits up to 30 seconds for `AGENT_READY_FOR_HANDOFF` before forcefully stopping you.

## Helper: Encoding Context

PowerShell:

```powershell
$context = @{ from = "pm"; reason = "task_assignment"; task = @{ id = "feat-001" } }
$json = $context | ConvertTo-Json -Compress
$bytes = [System.Text.Encoding]::UTF8.GetBytes($json)
$base64 = [System.Convert]::ToBase64String($bytes)
Write-Host "HANDOFF:developer:$base64"
```

Bash:

```bash
context='{"from":"pm","reason":"task_assignment","task":{"id":"feat-001"}}'
encoded=$(echo -n "$context" | base64 -w0)
echo "HANDOFF:developer:$encoded"
```

## Receiving Handoff Context

When you start and receive handoff context, you'll see:

```
## HANDOFF CONTEXT (FROM PREVIOUS AGENT)
You are receiving control from another agent. Here is the context:

From: pm
Reason: task_assignment
Task Details: {"id":"feat-001","title":"Add user auth"}

Please acknowledge this handoff and continue the work accordingly.
Read prd.json.session and prd.json.items for full state.
```

**Your first action should be:**

1. Acknowledge the handoff: "Received handoff from PM for task feat-001"
2. Read `prd.json.session`, `prd.json.agents`, and `prd.json.items` to get full context
3. Begin the assigned work

## Completion Protocol

When ALL PRD items have `passes: true`, the PM agent outputs:

```
<promise>RALPH_COMPLETE</promise>
```

This signals the watchdog to end the session gracefully.

## Key Differences from Polling Mode

| Aspect          | Polling Mode           | Single-Agent Mode    |
| --------------- | ---------------------- | -------------------- |
| Active agents   | 3 simultaneous         | 1 at a time          |
| Token usage     | Continuous for all 3   | Only active agent    |
| Communication   | File polling every 30s | Handoff phrases      |
| Agent switching | Implicit via state     | Explicit handoff     |
| Watchdog role   | Monitor all processes  | Orchestrate handoffs |

## Error Handling

If you encounter an error that prevents work:

1. Save any partial state
2. Output error context in handoff:
   ```json
   {
     "from": "developer",
     "reason": "error",
     "task": { "id": "feat-001" },
     "error": "Build failed: missing dependency X"
   }
   ```
3. Handoff to PM for resolution:
   ```
   HANDOFF:pm:base64_error_context
   ```
