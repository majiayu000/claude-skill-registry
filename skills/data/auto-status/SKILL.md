---
name: auto-status
description: Show current auto session status, progress, and any pending gates. Activates for: auto status, auto status, session status, check auto.
---

# Auto Status Command

**Show the current auto session status and progress.**

## Usage

```bash
/sw:auto-status [OPTIONS]
```

## Options

| Option | Description |
|--------|-------------|
| `--json` | Output in JSON format (for programmatic use) |
| `--simple` | Minimal output (one-liner) |

## Examples

```bash
# Check current session
/sw:auto-status

# Get JSON output
/sw:auto-status --json

# Quick status check
/sw:auto-status --simple
```

## What It Shows

### Session Information
- **Session ID**: Unique identifier for this auto run
- **Status**: Running, completed, cancelled, or paused
- **Duration**: How long the session has been running
- **Iteration**: Current iteration out of maximum

### Progress
- Visual progress bar
- Increment queue status (total/completed/failed)
- Current increment task progress

### Warnings
- **Human Gate Pending**: Session is waiting for human approval
- **Circuit Breakers Open**: External services unavailable

## Output Example

```
🤖 Auto Session Status

Status: 🟢 RUNNING

Session ID: auto-2025-12-29-abc123
Duration: 2h 15m
Iteration: 47 / 100

Progress: [████████████████░░░░░░░░░░░░░░] 47%

📋 Increment Queue
   Total: 3 | Completed: 2 | Failed: 0

📌 Current Increment: 0003-payment-integration
   Tasks: 12 / 18 (67%)

💡 Actions:
   Cancel: /sw:cancel-auto
   Let it run: Close this tab, work will continue
```

## JSON Output Format

```json
{
  "active": true,
  "sessionId": "auto-2025-12-29-abc123",
  "status": "running",
  "iteration": 47,
  "maxIterations": 100,
  "duration": "2h 15m",
  "currentIncrement": "0003-payment-integration",
  "incrementQueue": {
    "total": 3,
    "completed": 2,
    "failed": 0
  },
  "currentProgress": {
    "tasksCompleted": 12,
    "tasksTotal": 18
  },
  "humanGatePending": false,
  "openCircuitBreakers": 0,
  "simpleMode": false
}
```

## Execution

When this command is invoked:

```bash
bash plugins/specweave/scripts/auto-status.sh [args]
```

## Related Commands

| Command | Purpose |
|---------|---------|
| `/sw:auto` | Start auto session |
| `/sw:cancel-auto` | Cancel running session |
| `/sw:approve-gate` | Approve pending human gate |

## Notes

- Status is read from `.specweave/state/auto-session.json`
- Progress is calculated from tasks.md files
- Use `--json` for integration with other tools
- The session continues even if you close the terminal
