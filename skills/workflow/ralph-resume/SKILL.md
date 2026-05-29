---
name: ralph-resume
description: Resume RALPH execution from last checkpoint
allowed-tools: Read, Write, Bash
---

# RALPH-RESUME - Resume Execution

Resume RALPH execution from where it was paused.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-resume` | Resume from last checkpoint |

## Process

1. Load intervention state from `.ralph/intervention.json`
2. Find last checkpoint
3. Set state to RUNNING
4. Continue with next subtask

## Output

```
╔════════════════════════════════════════════════════════════════╗
║                 RALPH Resumed                                   ║
╚════════════════════════════════════════════════════════════════╝

Status: ▶️ RUNNING

Resuming from checkpoint: cp-1706180400000
Last completed: ST-001-2

Progress:
  Completed subtasks: 2/5
  Next subtask: ST-001-3

Continuing RALPH execution...
```

## Use Cases

- Continue after reviewing changes
- Resume after break
- Continue after manual adjustments
