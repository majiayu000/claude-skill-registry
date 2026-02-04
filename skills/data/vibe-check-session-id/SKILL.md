---
name: get-session-id
description: Get the current Claude Code session ID and log file path. Use when user says "get session id", "what is my session id", "current session", "session info", or "what session is this".
---

# Get Current Session ID

**Purpose:** Retrieve the current Claude Code session ID and log file path by emitting a unique marker and querying the vibe-check database.

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

## How It Works

This skill uses a clever technique to find the current session:

1. **Generate a unique marker** - Create a random string that won't appear anywhere else
2. **Emit the marker** - Output it into the conversation so vibe-check logs it
3. **Wait briefly** - Allow time for vibe-check to process and write to the database
4. **Query for the marker** - Search `conversation_events.event_data` for the unique string
5. **Extract session info** - Return `event_session_id` and `file_name` from the matching row

---

## Execution Steps

### Step 1: Generate and Emit Marker

Generate a unique marker string using this format:
```
VIBE_SESSION_MARKER_[random 16 character hex string]
```

Example: `VIBE_SESSION_MARKER_a7f3b2c9e4d1f8a6`

**IMPORTANT:** You MUST output this marker text directly into your response. Say something like:

```
Looking up session info...
Session marker: VIBE_SESSION_MARKER_a7f3b2c9e4d1f8a6
```

This ensures the marker gets logged by vibe-check.

### Step 2: Wait for Logging

Wait 2 seconds to allow vibe-check to process and log the marker:

```bash
sleep 2
```

### Step 3: Query the Database

Find the marker in the database:

```sql
SELECT
    event_session_id,
    file_name,
    inserted_at,
    event_type
FROM conversation_events
WHERE event_data LIKE '%VIBE_SESSION_MARKER_[your-marker-here]%'
ORDER BY inserted_at DESC
LIMIT 1;
```

Replace `[your-marker-here]` with the actual marker string you generated.

### Step 4: Present Results

---

## Response Format

After finding the session info, present it clearly:

```
Current Session Information

Session ID: abc123def456
Log File: /Users/you/.claude/projects/xyz/abc123.jsonl
Detected at: 2026-01-18 10:30:45

This session has been active since [start time if you query for it].
```

---

## Complete Query Example

Here's the full query to run (substitute your marker and database path from `vibe-check status`):

```bash
sqlite3 "file:$HOME/.vibe-check/vibe_check.db?mode=ro" \
  "SELECT event_session_id, file_name, inserted_at FROM conversation_events WHERE event_data LIKE '%VIBE_SESSION_MARKER_abc123%' ORDER BY inserted_at DESC LIMIT 1;"
```

---

## Troubleshooting

### No results found

If the marker isn't found:
1. Wait longer (try 5 seconds) - vibe-check might be slow
2. Check if vibe-check monitor is running: `ps aux | grep vibe-check`
3. Verify the database exists at the expected path
4. Try the alternate database location

### Multiple results

The query orders by `inserted_at DESC` and limits to 1, so you'll get the most recent match.

---

## Additional Session Info

Once you have the session ID, you can get more details:

```sql
-- Get session statistics
SELECT
    MIN(inserted_at) as session_start,
    MAX(inserted_at) as session_end,
    COUNT(*) as total_events,
    COUNT(CASE WHEN event_type = 'user' THEN 1 END) as user_messages,
    COUNT(CASE WHEN event_type = 'assistant' THEN 1 END) as assistant_messages,
    git_remote_url as repository,
    event_git_branch as branch
FROM conversation_events
WHERE event_session_id = '[session_id]'
GROUP BY event_session_id;
```

---

## Use Cases

- **Debugging:** Find which session you're in when troubleshooting
- **Cross-referencing:** Link current conversation to database records
- **Session tracking:** Identify the log file for manual inspection
- **Handoffs:** Share session ID with another tool or person
