---
name: bazinga-db-core
description: Session lifecycle and system operations. Use when creating sessions, saving state, getting dashboard data, or running system queries.
version: 2.0.0
allowed-tools: [Bash, Read]
---

# BAZINGA-DB Core Skill

You are the bazinga-db-core skill. You manage session lifecycle, state snapshots, and system-level database operations.

## When to Invoke This Skill

**Invoke when:**
- Creating or retrieving orchestration sessions
- Saving/restoring orchestrator or PM state
- Getting dashboard snapshots for status reporting
- Running custom SELECT queries
- Checking database integrity or recovering

**Do NOT invoke when:**
- Managing task groups or plans → Use `bazinga-db-workflow`
- Logging interactions or reasoning → Use `bazinga-db-agents`
- Managing context packages → Use `bazinga-db-context`

## Script Location

**Path:** `.claude/skills/bazinga-db/scripts/bazinga_db.py`

All commands use this script with `--quiet` flag:
```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet <command> [args...]
```

## Commands

### create-session

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet create-session \
  "<session_id>" "<mode>" "<user_request>"
```

Creates a new orchestration session.

**Parameters:**
- `session_id`: Unique identifier (e.g., `bazinga_abc123`)
- `mode`: `simple` or `parallel`
- `user_request`: Original user request text

**Returns:** `{"session_id": "...", "status": "active", "mode": "..."}`

### get-session

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-session "<session_id>"
```

**Returns:** Full session object with all fields.

### list-sessions

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet list-sessions [limit]
```

**Parameters:**
- `limit`: Optional, defaults to 10

**Returns:** Array of recent sessions ordered by created_at DESC.

### update-session-status

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet update-session-status \
  "<session_id>" "<status>"
```

**Valid status values:** `active`, `paused`, `completed`, `failed`, `cancelled`

### save-state

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet save-state \
  "<session_id>" "<state_type>" '<json_state>' [--group-id <id>]
```

Saves state snapshot with UPSERT semantics (insert or update).

**Parameters:**
- `session_id`: Session identifier
- `state_type`: `orchestrator`, `pm`, `group_status`, or `investigation`
- `json_state`: JSON object with state data
- `--group-id`: Optional group isolation key (default: `global`)
  - Use `global` for session-level state (orchestrator, pm)
  - Use task group ID for group-specific state (investigation)

**Example with group_id:**
```bash
python3 .../bazinga_db.py --quiet save-state \
  "bazinga_abc123" "investigation" '{"status": "in_progress"}' --group-id "CALC"
```

**Note:** Uses UPSERT - safe to call multiple times for same (session_id, state_type, group_id).

### get-state

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet get-state \
  "<session_id>" "<state_type>" [--group-id <id>]
```

**Parameters:**
- `--group-id`: Optional group isolation key (default: `global`)

**Returns:** Latest state snapshot for the specified type and group.

### dashboard-snapshot

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet dashboard-snapshot "<session_id>"
```

**Returns:** Complete dashboard data including:
- Session details
- Task groups with status
- Success criteria
- Recent orchestration logs
- Reasoning timeline

### query

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet query "<sql_select>"
```

Execute custom SELECT query (read-only).

**Example:**
```bash
python3 .../bazinga_db.py --quiet query "SELECT COUNT(*) FROM sessions WHERE status='completed'"
```

### integrity-check

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet integrity-check
```

Runs SQLite integrity check. Returns `{"status": "ok"}` or error details.

### recover-db

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet recover-db
```

Attempts to recover corrupted database from WAL.

### detect-paths

```bash
python3 .claude/skills/bazinga-db/scripts/bazinga_db.py --quiet detect-paths
```

Shows auto-detected paths for database and project root.

## Output Format

Return ONLY raw JSON output. No formatting, markdown, or commentary.

## Error Handling

- Missing session: Returns `{"error": "Session not found: <id>"}`
- Invalid status: Returns `{"error": "Invalid status: <status>"}`
- Database locked: Retry after 100ms (automatic)

## References

- Full schema: `.claude/skills/bazinga-db/references/schema.md`
- All commands: `.claude/skills/bazinga-db/references/command_examples.md`
- CLI help: `python3 .../bazinga_db.py help`
