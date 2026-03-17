---
# VERSION: 2.88.0
name: checkpoint-manager
description: "Session checkpoint management: save, restore, list, clear state snapshots"
user-invocable: true
allowed-tools:
  - Read
  - Write
  - Bash
---

## v2.88 Key Changes (MODEL-AGNOSTIC)

- **Model-agnostic**: Uses model configured in `~/.claude/settings.json` or CLI/env vars
- **No flags required**: Works with the configured default model
- **Flexible**: Works with GLM-5, Claude, Minimax, or any configured model
- **Settings-driven**: Model selection via `ANTHROPIC_DEFAULT_*_MODEL` env vars

# Checkpoint Manager

Manage session state checkpoints for the Ralph orchestration system.

## Subcommands

### save - Create checkpoint
```
/checkpoint save "before-refactor"
@cp save "Pre-deployment state"
```

### restore - Restore checkpoint
```
/checkpoint restore "before-refactor"
@cp restore cp_20260107_143015
```

### list - List all checkpoints
```
/checkpoint list
@cp list
```

### clear - Remove checkpoint(s)
```
/checkpoint clear "old-checkpoint"
@cp clear --all
```

## Storage

Checkpoints are stored in `~/.ralph/checkpoints/` as JSON files.

## Output Examples

### Save Output
```
✅ Checkpoint saved: cp_20260214_143015_before-refactor
📁 Location: ~/.ralph/checkpoints/cp_20260214_143015.json
⏱️  Expires: 24 hours (2026-02-15 14:30:15)
```

### List Output
```
╭───────────────────────────────────────────────────────╮
│                  CHECKPOINTS (3)                       │
├───────────────────────────────────────────────────────┤
│ cp_20260214_143015  │ before-refactor      │ 2h ago  │
│ cp_20260214_120000  │ pre-deployment       │ 5h ago  │
│ cp_20260213_180000  │ feature-complete     │ 1d ago  │
╰───────────────────────────────────────────────────────╯
```

## Workflow Integration

```
/checkpoint save "Before risky changes"
  ↓ (make changes)
/checkpoint restore "Before risky changes"  # if needed
  ↓ (or continue)
/checkpoint clear "Before risky changes"   # cleanup
```

## Related Skills

- `/orchestrator` - Full orchestration workflow
- `/loop` - Iterative execution with checkpointing
- `/gates` - Quality validation before checkpoints
