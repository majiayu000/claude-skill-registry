---
name: command-parallel-exec
description: Use the /parallel-exec slash command to run tasks with automatic agent parallelization. Use when: work can be decomposed into parallel subtasks.
---

# Command: /parallel-exec

Run the `/parallel-exec` workflow defined in `.claude/commands/parallel-exec.md`.

## Usage
`/parallel-exec <task> [mode] [parallel] [dry_run]`

## Notes
- Supports modes like auto, chain, and decompose.
- Full workflow details: `.claude/commands/parallel-exec.md`.
