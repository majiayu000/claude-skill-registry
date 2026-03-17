---
name: ac-checkpoint-manager
description: Manage checkpoints for rollback capability. Use when creating save points, rolling back changes, managing recovery points, or restoring previous states.
---

# AC Checkpoint Manager

Manage checkpoints for safe rollback during autonomous development.

## Purpose

Creates and manages checkpoints that enable rollback to known-good states, providing safety during autonomous operation.

## Quick Start

```python
from scripts.checkpoint_manager import CheckpointManager

manager = CheckpointManager(project_dir)
checkpoint = await manager.create_checkpoint("before-refactor")
await manager.restore_checkpoint(checkpoint.id)
```

## Checkpoint Types

- **Auto**: Created automatically at key points
- **Manual**: Created on explicit request
- **Feature**: Created after each feature completion
- **Session**: Created at session boundaries

## Checkpoint Structure

```
.claude/checkpoints/
├── checkpoint-20240115-100000/
│   ├── metadata.json
│   ├── feature_list.json
│   ├── execution-state.json
│   └── git-ref.txt
├── checkpoint-20240115-110000/
│   └── ...
```

## Auto-Checkpoint Points

- Before starting new feature
- After completing feature
- Before risky operations
- At context compaction

## Workflow

```
1. CREATE    → Snapshot current state
2. STORE     → Save files and git ref
3. VALIDATE  → Verify checkpoint integrity
4. (on rollback)
5. RESTORE   → Restore from checkpoint
6. VERIFY    → Confirm restoration
```

## Integration

- Used by: `ac-state-tracker` for state recovery
- Used by: `ac-task-executor` before risky operations

## API Reference

See `scripts/checkpoint_manager.py` for full implementation.
