---
name: n8n-errors-execution
description: >
  Use when debugging workflow execution failures or implementing error
  recovery in n8n. Prevents silent failures by enforcing the 4 error
  handling patterns. Covers node failures, timeout handling,
  continueOnFail pattern, Error Trigger node, error workflows, retry on
  fail configuration, Stop And Error node, and execution data inspection.
  Keywords: n8n, error, execution, retry, timeout, failure, recovery.
license: MIT
compatibility: "Designed for Claude Code. Requires n8n v1.x."
metadata:
  author: OpenAEC-Foundation
  version: "1.0"
---

# n8n Error Handling & Execution Failures

## Quick Reference

| Mechanism | Scope | Purpose | Configuration |
|-----------|-------|---------|---------------|
| Error Workflow | Workflow-level | Catch any unhandled failure, notify/recover | Workflow Settings > Error Workflow |
| continueOnFail | Per-node | Allow workflow to continue despite node failure | Node Settings > Continue On Fail |
| Retry on Fail | Per-node | Automatically retry transient failures | Node Settings > Retry On Fail |
| Stop And Error | Explicit node | Deliberately fail workflow with custom message | Add Stop And Error node |

## Error Handling Decision Tree

```
Workflow execution fails
├── Is the failure transient (API timeout, rate limit)?
│   ├── YES → Enable Retry on Fail on that node
│   │         Config: maxTries=3, waitBetweenTries=1000ms
│   │         └── Still fails after retries? → Falls to Error Workflow
│   └── NO → Continue below
├── Should the workflow continue despite this node failing?
│   ├── YES → Enable continueOnFail on that node
│   │         └── Check $json.error in next node for fallback logic
│   └── NO → Continue below
├── Is this a business logic validation failure?
│   ├── YES → Use Stop And Error node to fail explicitly
│   │         └── Error Workflow receives the custom error message
│   └── NO → Continue below
└── Unhandled failure
    └── ALWAYS configure an Error Workflow to catch it
        └── Error Trigger → Slack/Email/Database notification
```

## The 4 Error Handling Patterns

### Pattern 1: Error Workflow with Notifications

**When**: ALWAYS set up as a safety net for every production workflow.

```
Main Workflow → (fails) → Error Trigger → Slack/Email notification
```

Setup:
1. Create a new workflow with an **Error Trigger** node as the start
2. Add notification nodes (Slack, Email, HTTP Request to logging service)
3. In the main workflow, open **Workflow Settings**
4. Select the error workflow from the **Error Workflow** dropdown
5. One error workflow can serve multiple production workflows

### Pattern 2: Graceful Degradation (continueOnFail)

**When**: The failing node is non-critical and a fallback value is acceptable.

```
HTTP Request (continueOnFail=true) → IF ($json.error) → Fallback path
                                                       → Success path
```

- Enable **Continue On Fail** in the node's Settings tab
- The next node receives error data in `$json.error` instead of normal output
- ALWAYS add an IF node after to branch on error vs success

### Pattern 3: Retry with Fallback

**When**: The node calls an external API that may have transient failures.

```
API Call (retryOnFail=true, maxTries=3) → (still fails) → Error Workflow
```

- Enable **Retry On Fail** in the node's Settings tab
- Configure **Max Tries** (default: 3) and **Wait Between Tries** (default: 1000ms)
- If all retries fail, the error propagates to the Error Workflow

### Pattern 4: Deliberate Failure (Stop And Error)

**When**: Custom validation detects invalid data that MUST stop execution.

```
IF (invalid data) → Stop And Error → triggers Error Workflow
```

- Add a **Stop And Error** node after your validation logic
- Set a descriptive error message explaining what failed
- The Error Workflow receives this message in the error data

## Diagnostic Table: Symptom > Cause > Fix

| Symptom | Cause | Fix |
|---------|-------|-----|
| Workflow stops at node with red X | Node threw unhandled error | Enable continueOnFail OR fix the node config |
| "Workflow could not be started" | Trigger node misconfigured or credentials invalid | Check trigger node settings and credential validity |
| Workflow hangs indefinitely | No execution timeout configured | Set `EXECUTIONS_TIMEOUT` env var or per-workflow timeout |
| Error workflow never fires | Error workflow not assigned in Workflow Settings | Open Workflow Settings > select Error Workflow |
| Error workflow fires but no data | Error Trigger node missing in error workflow | ALWAYS start error workflow with Error Trigger node |
| Node retries but still fails | Transient issue persists beyond max retries | Increase maxTries or waitBetweenTries; check upstream service |
| `$json.error` is undefined | continueOnFail not enabled on the failing node | Enable Continue On Fail in node Settings |
| Execution timeout reached | Workflow exceeds configured timeout limit | Increase `EXECUTIONS_TIMEOUT` or optimize workflow |
| "Workflow was stopped manually" | User or API stopped execution | Check execution logs; verify no automated stop triggers |
| Node shows "No input data" | Previous node produced empty output | Add IF node to check for empty data before processing |
| Credentials error on active workflow | Credentials expired or were deleted | Re-authenticate credentials; check credential sharing |
| Sub-workflow execution fails | Caller policy blocks execution | Set `N8N_WORKFLOW_CALLER_POLICY_DEFAULT_OPTION` correctly |

## Error Workflow Data Structure

The **Error Trigger** node receives this data when an error workflow fires:

```json
{
  "execution": {
    "id": "231",
    "url": "https://n8n.example.com/execution/231",
    "retryOf": null,
    "error": {
      "message": "The error message",
      "stack": "Error stack trace..."
    },
    "lastNodeExecuted": "HTTP Request",
    "mode": "trigger"
  },
  "workflow": {
    "id": "1",
    "name": "My Workflow"
  }
}
```

Key fields:
- `execution.error.message` — The actual error description
- `execution.lastNodeExecuted` — Which node failed
- `execution.id` — Link back to the failed execution for inspection
- `workflow.name` — Which workflow triggered the error

## Execution Timeout Configuration

| Level | Setting | Default | Description |
|-------|---------|---------|-------------|
| Instance-wide | `EXECUTIONS_TIMEOUT` | `-1` (disabled) | Default timeout for ALL workflows (seconds) |
| Instance max | `EXECUTIONS_TIMEOUT_MAX` | `3600` | Maximum timeout any workflow can set (seconds) |
| Per-workflow | Workflow Settings > Timeout | Inherits instance default | Override for specific workflow |

ALWAYS set `EXECUTIONS_TIMEOUT` in production to prevent runaway executions.

## Common Execution Errors

### Authentication & Credentials
- **"401 Unauthorized"** — Credential expired or revoked. Re-authenticate in n8n.
- **"403 Forbidden"** — API key lacks required permissions. Check scopes.
- **"ECONNREFUSED"** — Target service is down or URL is wrong. Verify host/port.

### Data & Processing
- **"Cannot read property of undefined"** — Expression references missing field. Use `$json?.field` optional chaining.
- **"Too many items"** — Node received more items than it can process. Add a Limit node upstream.
- **"Payload too large"** — Request exceeds `N8N_PAYLOAD_SIZE_MAX` (default 16MB). Reduce payload or increase limit.

### Execution Environment
- **"Execution was stopped because it reached the timeout"** — Increase timeout or optimize workflow.
- **"Worker timed out"** — In queue mode, worker exceeded task runner timeout. Increase `N8N_RUNNERS_TASK_TIMEOUT`.
- **"Out of memory"** — Workflow processes too much data in memory. Use streaming or split into batches.

## Rules

- ALWAYS configure an Error Workflow for every production workflow
- ALWAYS start error workflows with the Error Trigger node
- ALWAYS set `EXECUTIONS_TIMEOUT` in production environments
- ALWAYS add an IF node after a continueOnFail node to handle the error branch
- NEVER assume retries will solve non-transient errors (auth failures, schema mismatches)
- NEVER use continueOnFail on critical nodes where failure means data is invalid
- NEVER leave production workflows without error handling — silent failures cause data loss
- ALWAYS test error workflows by deliberately triggering them (use Stop And Error node)

## Reference Files

- [methods.md](references/methods.md) — Error handling nodes, continueOnFail API, retry configuration
- [examples.md](references/examples.md) — Error workflow setup, continueOnFail patterns, retry patterns
- [anti-patterns.md](references/anti-patterns.md) — Error handling mistakes to avoid
