---
name: beads
description: "Issue tracking with Beads (bd CLI). Use when commands need to create, query, update, or close issues, or manage dependencies."
---

# Beads Issue Tracker

## Core Concepts

- **bd ready** — tasks with no blockers
- **Status**: open → in_progress → closed
- **Types**: task, bug, feature, epic, chore
- **Priority**: 0 (critical) → 4 (low), default 2
- **Dependencies**: only `blocks` affects ready

## Operations

### Get Issue Details
```bash
bd show <id> --json
```
Returns full issue data: title, description, status, type, priority, dependencies.

### Check If Issue Exists
```bash
bd show <id>
```
Exit code 0 = exists, non-zero = not found.

### Create Issue
```bash
bd create --title "Title" --type task --priority 2 --description "Description" --json
```
Creates new issue. Use `--parent <epic-id>` for subtasks.

### Update Status
```bash
bd update <id> --status in_progress --json
```
Valid statuses: open, in_progress, closed.

### Add Dependency
```bash
bd dep add <blocked-id> <blocker-id> --type blocks
```
Makes blocker-id block blocked-id. Only `blocks` affects ready state.

### Get Dependency Tree
```bash
bd dep tree <id>
```
Shows issue hierarchy and blocking relationships.

### Find Ready Tasks
```bash
bd ready --json
```
Lists tasks with no unresolved blockers.

### Find Blocked Tasks
```bash
bd blocked --json
```
Lists tasks waiting on blockers.

### Close Issue
```bash
bd close <id> --reason "Done: summary" --json
```
Marks issue as closed with resolution reason.

### List Issues
```bash
bd list --status open --json
```
Filter by status, type, priority.

### Sync
```bash
bd sync
```
Synchronizes local state with remote.

## Quick Reference

| Action | Command |
|--------|---------|
| Show issue | `bd show <id> --json` |
| Create issue | `bd create --title "..." --type task --json` |
| Update status | `bd update <id> --status in_progress` |
| Add blocker | `bd dep add <blocked> <blocker> --type blocks` |
| Ready tasks | `bd ready --json` |
| Close issue | `bd close <id> --reason "..."` |

## References

- `references/types.md` — Issue types and priorities
- `references/dependencies.md` — Dependency types and usage
