---
name: ctask
description: Manages tasks using the ctask CLI wrapper over a local SQLite database. Use when tracking work items, creating tasks, managing dependencies, adding comments, labeling, or reviewing task status. Triggers on task tracking, ticket management, work planning, backlog management.
user-invocable: false
allowed-tools:
  - Bash(ctask:*)
---

# ctask — Local Task Tracker

Use the `ctask` CLI to track tasks, dependencies, comments, and labels in a local SQLite database.

## Prerequisites

`ctask` must be on `$PATH`. Database auto-initializes on first use.

## CLI Reference

### Create a task
```bash
ctask create "Title" [--desc "Description"] [--priority low|medium|high|critical] [--project "name"]
```

### List tasks
```bash
ctask list [--status open|in_progress|blocked|done|cancelled] [--priority <p>] [--project <name>] [--all]
```
Default: excludes cancelled tasks. Use `--all` to show everything.

### Show task details
```bash
ctask show <id>
```
Returns task fields, labels, dependencies (blocked by / blocks), and comments.

### Update a task
```bash
ctask update <id> [--title "New title"] [--desc "New desc"] [--status <s>] [--priority <p>] [--project "name"]
```

### Comments
```bash
ctask comment <id> <body>       # Add comment
ctask comments <id>             # List comments
```

### Dependencies
```bash
ctask block <id> --by <blocker_id>    # Task <id> is blocked by <blocker_id>
ctask unblock <id> --by <blocker_id>  # Remove dependency
ctask deps <id>                        # Show what blocks/is blocked by
```

### Labels
```bash
ctask label <id> <label>       # Add label
ctask unlabel <id> <label>     # Remove label
ctask labels <id>              # List labels
```

### Other
```bash
ctask delete <id>              # Permanently delete task
ctask search <query>           # Search title and description
```

## When to Act

| User says... | Do this |
|-------------|---------|
| "track this" / "add a task" / "remember to..." | `ctask create` — infer title from context, ask project if ambiguous |
| "what's open" / "what am I working on" | `ctask list --status open` |
| "I finished X" / marks work done | `ctask update <id> --status done` + `ctask comment <id> "outcome"` |
| "X depends on Y" / "can't do X until Y" | `ctask block <X> --by <Y>` |
| "I'm stuck on X" | `ctask update <id> --status blocked` + `ctask comment <id> "why"` |
| starts working on a task | `ctask update <id> --status in_progress` |

Always `ctask list` first to avoid creating duplicates.

## Enums

- **Statuses**: open, in_progress, blocked, done, cancelled
- **Priorities**: low, medium, high, critical (list output sorts by priority desc, then date desc)

## Guidelines

- Always quote titles with double-quotes to avoid shell issues.
- Comments are engineering logs, not status updates:
  - Bad: "done" / "updated status"
  - Good: "Fixed by switching to connection pooling — was hitting PG max_connections under load"
- When completing: `update --status done` + closing comment summarizing the outcome.
- When blocked: `update --status blocked` + comment explaining why + `block` if another task is the blocker.
- Use `--project` to scope tasks when working across multiple projects.
