---
name: spool-workflow
description: Spool workflow delegation - delegates all workflow content to Spool CLI instruction artifacts.
---

This skill delegates workflow operations to the Spool CLI.

**Principle**: The Spool CLI is the source of truth for workflow instructions. Skills should be thin wrappers that invoke the CLI and follow its output.

## Available CLI Commands

### Change Management

```bash
spool create change "<name>" --module <module-id>
spool list [--json]
spool list --ready                    # Show only changes ready for implementation
spool list --pending                  # Show changes with 0/N tasks complete
spool list --partial                  # Show changes with 1..N-1/N tasks complete
spool list --completed                # Show changes with N/N tasks complete
spool status --change "<change-id>"
```

### Agent Instructions

```bash
spool agent instruction proposal --change "<change-id>"
spool agent instruction specs --change "<change-id>"
spool agent instruction design --change "<change-id>"
spool agent instruction tasks --change "<change-id>"
spool agent instruction apply --change "<change-id>"
spool agent instruction review --change "<change-id>"
spool agent instruction archive --change "<change-id>"
```

### Task Management

```bash
spool tasks status <change-id>
spool tasks next <change-id>
spool tasks ready                     # Show ready tasks across all changes
spool tasks ready <change-id>         # Show ready tasks for a specific change
spool tasks start <change-id> <task-id>
spool tasks complete <change-id> <task-id>
```

## Workflow Pattern

1. Run the appropriate `spool agent instruction` command
2. Read the output carefully
3. Follow the printed instructions exactly
4. Use `spool tasks` to track progress

## Related Skills

- `spool-write-change-proposal` - Create new changes
- `spool-apply-change-proposal` - Implement changes
- `spool-review` - Review changes
- `spool-archive` - Archive completed changes
- `spool-tasks` - Manage tasks
- `spool-commit` - Create commits
