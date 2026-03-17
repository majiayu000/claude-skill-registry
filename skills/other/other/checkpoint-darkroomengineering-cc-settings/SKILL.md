---
name: checkpoint
description: |
  Save and restore task state for long-running operations. Use when:
  - User says "checkpoint", "save state", "save progress"
  - User says "restore checkpoint", "list checkpoints"
  - Context window is running low and state needs persisting
  - Before risky operations that might need rollback
context: fork
allowed-tools: [Bash]
---

# Checkpoint: Save & Restore Task State

Manage checkpoints for long-running tasks. Enables recovery from interruptions and context window exhaustion.

## Subcommands

### save [label]

Save current state with an optional label.

```bash
~/.claude/scripts/checkpoint.sh save "Completed phase 3 migration"
```

### list

List all checkpoints for the current project.

```bash
~/.claude/scripts/checkpoint.sh list
```

### show [checkpoint-id]

Show details of a specific checkpoint.

```bash
~/.claude/scripts/checkpoint.sh show chk-20240115-103000
```

### restore [checkpoint-id]

Restore from the latest checkpoint, or a specific one by ID.

```bash
# Restore latest
~/.claude/scripts/checkpoint.sh restore

# Restore specific
~/.claude/scripts/checkpoint.sh restore chk-20240115-103000
```

### clean

Remove old checkpoints, keeping the last 10.

```bash
~/.claude/scripts/checkpoint.sh clean
```

## Examples

```
User: "save a checkpoint"
  -> /checkpoint save

User: "checkpoint before this refactor"
  -> /checkpoint save "Before auth refactor"

User: "list my checkpoints"
  -> /checkpoint list

User: "restore from last checkpoint"
  -> /checkpoint restore

User: "show checkpoint details"
  -> /checkpoint show <id>

User: "clean up old checkpoints"
  -> /checkpoint clean
```

## Storage

Checkpoints are stored at `~/.claude/checkpoints/<project-name>/` as JSON files with a `latest` symlink pointing to the most recent.
