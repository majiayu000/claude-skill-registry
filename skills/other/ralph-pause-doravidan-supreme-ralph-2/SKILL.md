---
name: ralph-pause
description: Pause RALPH execution after current subtask
allowed-tools: Read, Write
---

# RALPH-PAUSE - Pause Execution

Pause RALPH execution gracefully after the current subtask completes.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-pause` | Pause after current subtask |
| `/ralph-pause "reason"` | Pause with reason |

## Process

1. Set state to PAUSED in `.ralph/intervention.json`
2. RALPH checks for pause signal after each subtask
3. Current work completes, then pauses
4. No work is lost

## Output

```
╔════════════════════════════════════════════════════════════════╗
║                 RALPH Paused                                    ║
╚════════════════════════════════════════════════════════════════╝

Status: ⏸️ PAUSED

RALPH will pause after current subtask completes.
Reason: User requested pause

Current subtask: ST-001-3 (in progress)
Completed subtasks: 2
Checkpoints saved: 2

To resume: /ralph-resume
To rollback: /ralph-rollback
To cancel: /ralph-cancel
```

## Use Cases

- Need to review changes before continuing
- Want to make manual adjustments
- Taking a break from development
- Need to discuss approach with team
