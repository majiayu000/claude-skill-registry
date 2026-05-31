---
name: beads
description: 'Track bd issues and dependencies for Codex agents. Triggers: "beads", "bd", "track issue", "create task", "find work", "ready issues".'
---

# $beads — Issue Tracking (Codex Tailoring)

This override captures the Codex-native execution model for beads-based issue tracking.

## Key Distinction

Codex agents use `bd` CLI directly for issue management. There is no task-queue abstraction — agents read issues via `bd ready`, claim via `bd update --claim`, and close via `bd close`. The orchestrator assigns work to sub-agents by including the issue ID in the spawn prompt.

## Codex-Native Flow

### Finding Work

```bash
bd ready                    # unblocked issues
bd list --status=open       # all open
bd show <id>                # details + dependencies
```

### Creating Issues

```bash
bd create --title="<title>" --description="<desc>" --type=task --priority=2
bd dep add <child> <parent>  # child depends on parent
```

### Working Issues

1. `bd update <id> --claim` — claim before starting
2. Implement the work
3. `bd close <id>` — mark complete after verification

### Multi-Agent Coordination

When spawning workers via `spawn_agent(...)`, include the issue ID in the prompt:

```
spawn_agent(prompt="Implement issue <id>: <title>. Details: <description>. Files: <file-list>.")
```

Workers close their own issues after verification. The orchestrator validates via `bd list --status=open` after `wait_agent(...)` returns.

## Constraints

1. Always use `bd` CLI — never track issues in markdown files or inline state.
2. One issue per worker. If a worker needs to split work, it creates child issues with `bd create` + `bd dep add`.
3. Workers must `bd close` their issue only after the acceptance criteria pass.
