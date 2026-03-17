---
name: beads
description: Git-backed issue tracker for AI agents. Use when managing tasks, dependencies, or multi-step work. Triggers on task tracking, issue management, dependency graphs, ready work queues, or mentions of "beads" / "bd" CLI.
metadata:
  openclaw:
    emoji: 📿
    requires:
      bins: [bd]
    install:
      - id: brew
        kind: brew
        formula: beads
        bins: [bd]
        label: Install beads (brew)
      - id: npm
        kind: npm
        package: "@beads/bd"
        bins: [bd]
        label: Install beads (npm)
---

# Beads

Distributed, git-backed graph issue tracker for AI agents. Replaces markdown plans with a dependency-aware task graph stored as JSONL in `.beads/`.

## Quick Start

```bash
# Initialize (non-interactive for agents)
bd init --quiet

# Check ready work
bd ready --json

# Create a task
bd create "Complete task X" -p 1 --json

# View task
bd show bd-a1b2 --json
```

## Core Workflow

1. `bd ready --json` — Find unblocked work
2. `bd update <id> --status in_progress` — Claim task
3. Do the work
4. `bd close <id> --reason "Done"` — Complete task
5. `bd sync` — Force sync before ending session

## Agent-Critical Rules

- **Always use `--json`** for machine-readable output
- **Never use `bd edit`** — opens $EDITOR, unusable by agents
- **Use `bd update`** instead: `bd update <id> --title "New title" --description "New desc"`
- **Run `bd sync`** at end of session to flush changes to git

## Commands

### Initialize

```bash
bd init --quiet              # Non-interactive, auto-installs hooks
bd init --prefix myproj      # Custom ID prefix
bd init --stealth            # Local only, don't commit .beads/
bd init --contributor        # Fork workflow (separate planning repo)
```

### Create Issues

```bash
bd create "Title" -p 1 --json                    # Priority 1 (0=critical, 3=low)
bd create "Title" -t epic -p 0 --json            # Create epic
bd create "Subtask" -p 1 --json                  # Under epic: bd-a3f8.1, .2, .3
bd create "Found issue" --deps discovered-from:bd-a1b2 --json
```

Types: `task`, `bug`, `feature`, `epic`
Priorities: `0` (P0/critical) to `3` (P3/low)

### Query Issues

```bash
bd ready --json                    # Unblocked tasks (the work queue)
bd ready --priority 0 --json       # Only P0s
bd ready --assignee agent-1 --json # Assigned to specific agent

bd list --json                     # All issues
bd list --status open --json       # Open issues
bd list --priority 1 --json        # P1 issues

bd show bd-a1b2 --json             # Issue details + audit trail
bd blocked --json                  # Issues waiting on dependencies
bd stats --json                    # Statistics
```

### Update Issues

```bash
bd update bd-a1b2 --status in_progress --json
bd update bd-a1b2 --title "New title" --json
bd update bd-a1b2 --description "Details" --json
bd update bd-a1b2 --priority 0 --json
bd update bd-a1b2 --assignee agent-1 --json
bd update bd-a1b2 --design "Design notes" --json
bd update bd-a1b2 --notes "Additional notes" --json
```

Status values: `open`, `in_progress`, `blocked`, `closed`

### Close Issues

```bash
bd close bd-a1b2 --reason "Completed" --json
bd close bd-a1b2 bd-b2c3 --reason "Batch close" --json
```

### Dependencies

```bash
bd dep add bd-child bd-parent      # child blocked by parent
bd dep add bd-a1b2 bd-b2c3 --type related    # Related link
bd dep add bd-a1b2 bd-epic --type parent     # Parent-child

bd dep tree bd-a1b2                # Visualize dependency tree
bd dep remove bd-child bd-parent   # Remove dependency
bd dep cycles                      # Detect circular deps
```

Dependency types: `blocks` (default), `related`, `parent`, `discovered-from`

### Git Sync

```bash
bd sync                    # Export → commit → pull → import → push
bd hooks install           # Install git hooks for auto-sync
```

The daemon auto-syncs with 30s debounce. Use `bd sync` to force immediate sync.

### Maintenance

```bash
bd admin compact --dry-run --json   # Preview compaction
bd admin compact --days 90          # Compact issues closed >90 days
bd doctor                           # Check database health
```

## Hierarchical IDs (Epics)

```bash
bd create "Project Alpha" -t epic -p 1 --json   # Returns: bd-a3f8
bd create "Phase 1" -p 1 --json                 # Returns: bd-a3f8.1
bd create "Research" -p 1 --json                # Returns: bd-a3f8.2
bd create "Review" -p 1 --json                  # Returns: bd-a3f8.3
```

Up to 3 levels: `bd-a3f8` → `bd-a3f8.1` → `bd-a3f8.1.1`

## Multi-Agent Coordination

```bash
# Agent claims work
bd update bd-a1b2 --status in_progress --assignee agent-1 --json

# Query assigned work
bd ready --assignee agent-1 --json

# Track discovered work
bd create "Found issue" --deps discovered-from:bd-a1b2 --json
```

## Commit Convention (Optional)

For git-tracked projects, include issue ID in commit messages for traceability:
```bash
git commit -m "Complete research phase (bd-a1b2)"
```

## Session End Checklist

Before ending a session:

```bash
bd sync                    # Flush all changes
bd ready --json            # Show next work for handoff
```
