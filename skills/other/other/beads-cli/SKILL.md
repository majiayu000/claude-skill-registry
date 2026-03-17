---
name: beads-cli
description: Task tracking with the bd (Beads) CLI. Use when creating tasks, claiming work, closing beads, managing dependencies, or when the user mentions "beads", "bd", or "tasks".
---

# Beads CLI (bd)

Task tracking across sessions. All issue tracking goes through `bd`.

## When This Applies

| Signal | Action |
|--------|--------|
| Need to create a task | `bd create` |
| Looking for work | `bd ready --json` |
| Claiming a task | `bd update --status in_progress` |
| Finishing a task | `bd close` |
| Managing dependencies | `bd dep add/tree` |

---

## Core Workflow

```bash
# Finding work
bd ready --json                    # Unblocked tasks ready for work
bd blocked                         # Tasks waiting on dependencies
bd list                            # All tasks

# Task lifecycle
bd create "Title" -t bug -p 1      # Create with type, priority
bd update bd-42 --status in_progress --assignee YOUR_NAME  # Claim
bd close bd-42 --reason "Completed: summary"               # Complete

# Viewing
bd show bd-42                      # Full task details
bd info                            # Project summary
```

---

## Dependencies

```bash
bd dep add bd-child bd-blocker --type blocks        # Child blocked by blocker
bd dep add bd-a bd-b --type related                 # Related tasks
bd dep add bd-child bd-parent --type parent-child   # Hierarchy
bd dep add bd-new bd-old --type discovered-from     # Found during work
bd dep tree bd-42                                   # Visualize dependencies
bd dep cycles                                       # Find circular deps
```

---

## Task Types and Priority

| Type | Use For |
|------|---------|
| `bug` | Defects, errors |
| `feature` | New functionality |
| `task` | General work items |
| `epic` | Parent/container beads |
| `chore` | Maintenance, cleanup |

| Priority | Meaning |
|----------|---------|
| `0` | Critical (do first) |
| `1` | High |
| `2` | Normal |
| `3` | Low |
| `4` | Backlog |

---

## Child Beads

Hierarchical IDs: `bd-a1b2.1`, `bd-a1b2.3.1`

```bash
bd create "Sub-task" --parent bd-123 -p 1
```

---

## Claiming Protocol (Multi-Agent)

**CRITICAL: Always claim parent AND all sub-beads together.**

```bash
bd update bd-123 --status in_progress --assignee YOUR_NAME
bd update bd-123.1 --status in_progress --assignee YOUR_NAME
bd update bd-123.2 --status in_progress --assignee YOUR_NAME
```

**Why:** If you only claim parent, other agents see sub-beads as "ready" → CONFLICT.

---

## Closing Protocol

**CRITICAL: Close sub-beads first, then parent.**

```bash
bd close bd-123.1 --reason "Completed: implemented X"
bd close bd-123.2 --reason "Completed: added tests"
bd close bd-123 --reason "Completed: full feature done"
```

---

## Maintenance

```bash
bd doctor                          # Health check
bd doctor --fix                    # Auto-fix issues
bd compact --analyze --json        # Analyze for compaction
bd --readonly list                 # Safe read-only mode
```

---

## Key Rules

| Rule | Why |
|------|-----|
| Always commit `.beads/` with code | Keeps state in sync |
| Never edit `.beads/*.jsonl` directly | Use `bd` commands only |
| Always set `--assignee` when claiming | Prevents conflicts |
| Never use other TODO systems | Beads is authoritative |

---

## Quick Reference

```bash
bd ready --json          # What's available?
bd update ID --status in_progress --assignee NAME   # Claim
bd close ID --reason "..."   # Complete
bd create "Title" -t TYPE -p PRIORITY   # Create
bd dep add CHILD BLOCKER --type blocks   # Add dependency
bd doctor --fix          # Health check
```

---

## See Also

- `beads-viewer/` — Graph analysis with `bv`
- `advance/` — Full bead lifecycle (claiming, working, closing)
