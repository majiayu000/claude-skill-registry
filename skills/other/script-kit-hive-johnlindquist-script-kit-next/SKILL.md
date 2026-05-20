---
name: script-kit-hive
description: Hive/beads task management for Script Kit agents. Use when working with the issue tracking system, managing beads, or coordinating agent work. Covers issue lifecycle, progress reporting, and file reservations.
---

# Hive / Beads Task Management

Task tracking and coordination for Script Kit agents.

## Directory Structure

`.hive/`:
- `issues.jsonl` - task tracking
- `memories.jsonl` - semantic learnings

## Issue Record Format

```json
{"id":"cell--...","title":"...","status":"open","priority":1,"issue_type":"task","created_at":"...","updated_at":"...","parent_id":null,"dependencies":[],"labels":[],"comments":[]}
```

## Enums

- `issue_type`: `epic|task|bug|feature|chore`
- `status`: `open|in_progress|blocked|closed`
- `priority`: 0 critical, 1 high, 2 medium, 3 low

## MCP Commands (Don't Use CLI)

- query/next: `hive_query(...)`, `hive_ready()`
- create: `hive_create(...)`, `hive_create_epic(...)`
- update: `hive_start({id})`, `hive_update({id,...})`
- finish: `swarm_complete(...)` (**not** `hive_close()`)

## Epic/Subtask Example

```ts
hive_create_epic({
  epic_title: "Add search functionality",
  epic_description: "Implement fuzzy search for script list",
  subtasks: [
    { title: "Add search input UI", files: ["src/main.rs"], priority: 0 },
    { title: "Implement fuzzy matching", files: ["src/scripts.rs"], priority: 1 },
    { title: "Add keyboard navigation", files: ["src/main.rs"], priority: 1 }
  ]
});
```

## Mandatory Lifecycle

`swarmmail_init()` → `hive_start()` → progress at 25/50/75 → `swarm_complete()`

## Progress Reporting

```ts
swarm_progress({
  project_key: "/path/to/project",
  agent_name: "your-agent-name",
  bead_id: "cell--xxxxx",
  status: "in_progress",
  progress_percent: 50,
  message: "Completed X, now working on Y",
  files_touched: ["src/main.rs"]
});
```

## File Reservations

```ts
swarmmail_reserve({
  paths: ["src/main.rs", "src/theme.rs"],
  reason: "cell--xxxxx: Implement feature X",
  exclusive: true
});
```

## Required Log Fields

When relevant: `correlation_id`, `duration_ms`, `bead_id`, `agent_name`, `files_touched`

## Anti-Patterns (Don't Do These)

- Skip `swarmmail_init()` (work not tracked)
- Use `hive_close()` (reservation release breaks) → use `swarm_complete()`
- Edit unreserved files → reserve first
- Commit without verification gate
- Skip 25/50/75 progress updates

## When Blocked

Notify coordinator + mark bead blocked (include concrete reason).

## Scope Change

Request permission; don't silently expand beyond reserved files.

## Pre-Commit Checklist

- check / clippy / test pass
- only reserved files modified
- bead status updated
- progress reported
- correlation IDs present (where applicable)
