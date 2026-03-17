---
name: ralph-rollback
description: Rollback to a previous checkpoint
allowed-tools: Read, Write, Bash, AskUserQuestion
---

# RALPH-ROLLBACK - Rollback to Checkpoint

Rollback RALPH to a previous checkpoint, discarding work since then.

## Commands

| Command | Description |
|---------|-------------|
| `/ralph-rollback` | Rollback to last good checkpoint |
| `/ralph-rollback cp-123456` | Rollback to specific checkpoint |
| `/ralph-rollback --list` | List available checkpoints |

## Process

1. List available checkpoints
2. User selects checkpoint (or default to last)
3. Remove checkpoints after target
4. Update completed subtasks list
5. Git reset if needed
6. Set state to PAUSED

## List Checkpoints

```
╔════════════════════════════════════════════════════════════════╗
║                 Available Checkpoints                           ║
╚════════════════════════════════════════════════════════════════╝

Checkpoints (newest first):

  [3] cp-1706180600000 - ST-001-3 (2026-01-25 10:30:00)
      Changes: +45 lines, 2 files

  [2] cp-1706180400000 - ST-001-2 (2026-01-25 10:20:00)
      Changes: +32 lines, 1 file

  [1] cp-1706180200000 - ST-001-1 (2026-01-25 10:10:00)
      Changes: +15 lines, 1 file

Select checkpoint to rollback to:
```

## Rollback Confirmation

```
╔════════════════════════════════════════════════════════════════╗
║                 Rollback Confirmation                           ║
╚════════════════════════════════════════════════════════════════╝

⚠ You are about to rollback to: cp-1706180400000 (ST-001-2)

This will DISCARD:
  - ST-001-3 work (+45 lines, 2 files)
  - 1 checkpoint

Git status:
  - Will revert 1 commit
  - Uncommitted changes will be lost

? Proceed with rollback?
  ○ Yes, rollback (I understand changes will be lost)
  ○ No, cancel
```

## Rollback Complete

```
╔════════════════════════════════════════════════════════════════╗
║                 Rollback Complete                               ║
╚════════════════════════════════════════════════════════════════╝

✓ Rolled back to: cp-1706180400000

Removed:
  - 1 checkpoint
  - 1 completed subtask

Current state:
  Status: ⏸️ PAUSED
  Last completed: ST-001-2
  Next subtask: ST-001-3

To continue: /ralph-resume
```

## Use Cases

- Implementation went wrong direction
- Tests are failing after changes
- Need to try different approach
- Discovered better solution
