---
name: checkpoint
description: Deprecated. Use /compact instead. Claude has built-in memory that persists across sessions.
triggers:
  - save
allowed-tools: Read, Write, TaskList, Grep
model: opus
user-invocable: false
disable-model-invocation: true
---

# Checkpoint (Deprecated)

This skill is deprecated in v6.0. Claude Code has built-in memory and `/compact` that handle session persistence automatically.

## What to Use Instead

| Need | Solution |
|------|----------|
| Save context before clearing | `/compact` (reclaims ~40% tokens with context summary) |
| Persist learnings across sessions | Claude's built-in memory (automatic) |
| Save prd.json before compaction | PreCompact hook handles this automatically |
| Clear context completely | `/clear` (reclaims ~70%, loses context) |

## Migration

If `.claude/checkpoint.md` exists from a previous session, it is safe to delete. All important context is now managed by Claude's memory system and prd.json.
