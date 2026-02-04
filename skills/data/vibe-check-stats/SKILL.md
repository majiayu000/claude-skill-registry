---
name: claude-stats
description: Query Claude Code usage statistics from the vibe-check database. Use when user says "claude stats", "usage stats", "my claude usage", or "how much have I used claude".
---

# Claude Usage Statistics

**Purpose:** Query the local vibe-check database to show Claude Code usage statistics

---

## Database Location

To find the database location, run:
```bash
vibe-check status
```

The default location is: `~/.vibe-check/vibe_check.db`

**Note:** If the status shows no PID, vibe-check is not running and the database may be stale. Start it with `vibe-check start`.

## Important: Use Read-Only Mode

To avoid database locks when the monitor is running, always use read-only mode:

```bash
sqlite3 "file:/path/to/vibe_check.db?mode=ro" "SELECT ..."
```

Example:
```bash
sqlite3 "file:$HOME/.vibe-check/vibe_check.db?mode=ro" "SELECT COUNT(*) FROM conversation_events;"
```

---

## Core Queries

### Overview Stats

```sql
SELECT
    COUNT(*) as total_events,
    COUNT(DISTINCT event_session_id) as total_sessions,
    COUNT(DISTINCT DATE(inserted_at)) as days_active,
    MIN(DATE(inserted_at)) as first_use,
    MAX(DATE(inserted_at)) as last_use
FROM conversation_events;
```

### Event Type Breakdown

```sql
SELECT
    event_type,
    COUNT(*) as count,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM conversation_events), 1) as percentage
FROM conversation_events
GROUP BY event_type
ORDER BY count DESC;
```

### Daily Activity

```sql
SELECT
    DATE(inserted_at) as date,
    COUNT(*) as events,
    COUNT(DISTINCT event_session_id) as sessions
FROM conversation_events
GROUP BY DATE(inserted_at)
ORDER BY date DESC
LIMIT 14;
```

### Repository Breakdown

```sql
SELECT
    CASE
        WHEN git_remote_url IS NULL THEN '(no repo)'
        WHEN git_remote_url LIKE '%.git' THEN
            REPLACE(SUBSTR(git_remote_url,
                CASE
                    WHEN INSTR(git_remote_url, '/') > 0
                    THEN LENGTH(git_remote_url) - INSTR(SUBSTR(git_remote_url, -50), '/') + 2
                    ELSE 1
                END
            ), '.git', '')
        ELSE git_remote_url
    END as repository,
    COUNT(DISTINCT event_session_id) as sessions,
    COUNT(*) as events
FROM conversation_events
GROUP BY git_remote_url
ORDER BY sessions DESC
LIMIT 10;
```

---

## Response Format

When triggered, you should:

1. **Check database exists** - Use Bash to verify the database file
2. **Run overview query** - Get basic stats
3. **Run event breakdown** - Show what types of events are most common
4. **Show recent activity** - Last 7-14 days of usage
5. **Show top repositories** - Where user uses Claude most
6. **Present in readable format** - Use tables or formatted text

### Example Output

```
📊 Claude Code Usage Statistics

Overview:
- Total events: 3,247
- Sessions: 153
- Days active: 45
- First use: 2024-11-28
- Last use: 2026-01-13

Event Types:
- assistant: 1,679 (51.7%)
- user: 1,110 (34.2%)
- file-history-snapshot: 282 (8.7%)
- queue-operation: 106 (3.3%)
- summary: 75 (2.3%)

Top Repositories:
1. vibe-check: 45 sessions, 892 events
2. my-app: 32 sessions, 567 events
...
```

---

## Advanced Queries (if requested)

### Busiest Hours

```sql
SELECT
    STRFTIME('%H', inserted_at) as hour,
    COUNT(*) as events
FROM conversation_events
GROUP BY hour
ORDER BY events DESC
LIMIT 10;
```

### Session Duration Analysis

```sql
SELECT
    event_session_id,
    MIN(inserted_at) as session_start,
    MAX(inserted_at) as session_end,
    COUNT(*) as events,
    ROUND((JULIANDAY(MAX(inserted_at)) - JULIANDAY(MIN(inserted_at))) * 24 * 60, 1) as duration_minutes
FROM conversation_events
GROUP BY event_session_id
ORDER BY duration_minutes DESC
LIMIT 10;
```

---

## Error Handling

If database not found:
- Check both possible locations
- Inform user vibe-check may not be installed
- Provide installation instructions

If database empty:
- Inform user no data has been collected yet
- Suggest checking if monitor is running
