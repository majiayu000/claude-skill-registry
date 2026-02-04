---
name: recent-work
description: Show recent Claude Code sessions and work history. Use when user says "what have I been working on", "recent work", "what did I do today", or "show recent sessions".
---

# Recent Claude Work

**Purpose:** Show recent Claude Code sessions and what you've been working on

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

---

## Recent Sessions Query

### Sessions with Summary

```sql
WITH session_summary AS (
    SELECT
        event_session_id,
        MIN(inserted_at) as session_start,
        MAX(inserted_at) as session_end,
        COUNT(*) as event_count,
        COUNT(DISTINCT CASE WHEN event_type = 'user' THEN line_number END) as user_messages,
        COUNT(DISTINCT CASE WHEN event_type = 'assistant' THEN line_number END) as assistant_messages,
        git_remote_url,
        event_git_branch,
        git_commit_hash,
        file_name
    FROM conversation_events
    WHERE event_session_id IS NOT NULL
    GROUP BY event_session_id
)
SELECT
    event_session_id,
    session_start,
    session_end,
    ROUND((JULIANDAY(session_end) - JULIANDAY(session_start)) * 24 * 60, 1) as duration_minutes,
    user_messages,
    assistant_messages,
    event_count as total_events,
    git_remote_url as repository,
    event_git_branch as branch,
    file_name
FROM session_summary
ORDER BY session_start DESC
LIMIT 20;
```

### First User Message Per Session

Get context about what each session was about:

```sql
SELECT
    ce.event_session_id,
    ce.event_message as first_message,
    ce.inserted_at,
    CASE
        WHEN ce.git_remote_url IS NULL THEN '(no repo)'
        ELSE SUBSTR(ce.git_remote_url, LENGTH(ce.git_remote_url) - INSTR(REVERSE(ce.git_remote_url), '/') + 2)
    END as repository
FROM conversation_events ce
INNER JOIN (
    SELECT event_session_id, MIN(line_number) as first_line
    FROM conversation_events
    WHERE event_type = 'user'
        AND event_message IS NOT NULL
        AND event_session_id IS NOT NULL
    GROUP BY event_session_id
) first ON ce.event_session_id = first.event_session_id
    AND ce.line_number = first.first_line
ORDER BY ce.inserted_at DESC
LIMIT 20;
```

### Today's Activity

```sql
SELECT
    event_session_id,
    MIN(inserted_at) as started_at,
    COUNT(*) as events,
    git_remote_url as repository,
    event_git_branch as branch
FROM conversation_events
WHERE DATE(inserted_at) = DATE('now')
GROUP BY event_session_id
ORDER BY started_at DESC;
```

### This Week's Work Summary

```sql
SELECT
    DATE(inserted_at) as date,
    COUNT(DISTINCT event_session_id) as sessions,
    COUNT(*) as total_events,
    COUNT(DISTINCT git_remote_url) as repositories_used,
    GROUP_CONCAT(DISTINCT CASE
        WHEN git_remote_url IS NOT NULL
        THEN SUBSTR(git_remote_url, LENGTH(git_remote_url) - INSTR(REVERSE(git_remote_url), '/') + 2)
    END) as repos
FROM conversation_events
WHERE DATE(inserted_at) >= DATE('now', '-7 days')
GROUP BY DATE(inserted_at)
ORDER BY date DESC;
```

---

## Response Format

When triggered, provide a structured summary:

### Example: "what have I been working on"

```
📝 Recent Claude Code Sessions

Today (2026-01-13):
  Session abc123 (9:30 AM, 23 min) - vibe-check
    "can you help me create claude code skills for the database"
    → 45 events, 8 user messages, 12 assistant messages

  Session def456 (2:15 PM, 8 min) - my-app
    "fix the login bug"
    → 18 events, 3 user messages, 5 assistant messages

Yesterday (2026-01-12):
  Session ghi789 (10:00 AM, 45 min) - website
    "redesign the landing page"
    → 87 events, 15 user messages, 28 assistant messages

This Week Summary:
  Mon 01/13: 2 sessions, vibe-check + my-app
  Sun 01/12: 1 session, website
  Sat 01/11: 3 sessions, my-app, docs, vibe-check
  ...
```

### Example: "what did I do today"

```
Today's Activity (2026-01-13):

2 sessions, 63 total events

Morning Session (9:30 AM - 9:53 AM):
  Repository: vibe-check
  Branch: main
  Started with: "can you help me create claude code skills..."
  → Created 4 new skills, modified vibe-check.py

Afternoon Session (2:15 PM - 2:23 PM):
  Repository: my-app
  Branch: fix-auth
  Started with: "fix the login bug"
  → Modified auth.js, added tests
```

---

## Time-Based Views

### Last N Sessions

```sql
-- Get detailed view of last 10 sessions
SELECT
    event_session_id,
    MIN(inserted_at) as start_time,
    MAX(inserted_at) as end_time,
    COUNT(*) as events,
    git_remote_url
FROM conversation_events
WHERE event_session_id IS NOT NULL
GROUP BY event_session_id
ORDER BY start_time DESC
LIMIT 10;
```

### By Time Period

- Today: `WHERE DATE(inserted_at) = DATE('now')`
- Yesterday: `WHERE DATE(inserted_at) = DATE('now', '-1 day')`
- This week: `WHERE DATE(inserted_at) >= DATE('now', '-7 days')`
- This month: `WHERE DATE(inserted_at) >= DATE('now', 'start of month')`

---

## Interactive Follow-ups

After showing recent work, offer:
- "View full session details"
- "Search for specific topic"
- "See tool usage in session"
- "Export session history"

---

## Additional Context

When available, include:
- Branch names (shows feature context)
- Commit hashes (shows if work was committed)
- Repository info (shows which project)
- Session duration (shows complexity)
- Message counts (shows interaction level)
