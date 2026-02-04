---
name: analyze-tools
description: Analyze which tools Claude uses most frequently. Use when user says "what tools do I use most", "tool usage stats", "analyze my claude tools", or "which tools does claude use".
---

# Analyze Claude Tool Usage

**Purpose:** Analyze which tools Claude uses most frequently in conversations

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

## Understanding Tool Data

Tool usage is stored in the JSON event_data field. Assistant messages contain tool_use content blocks.

The structure is:
```json
{
  "type": "assistant",
  "message": {
    "content": [
      {
        "type": "tool_use",
        "name": "Read",
        "input": {...}
      }
    ]
  }
}
```

---

## Tool Analysis Queries

### Extract All Tool Uses

```sql
SELECT
    json_extract(value, '$.name') as tool_name,
    COUNT(*) as usage_count
FROM conversation_events,
     json_each(json_extract(event_data, '$.message.content'))
WHERE event_type = 'assistant'
    AND json_extract(value, '$.type') = 'tool_use'
    AND json_extract(value, '$.name') IS NOT NULL
GROUP BY tool_name
ORDER BY usage_count DESC;
```

### Tool Usage Over Time

```sql
SELECT
    DATE(inserted_at) as date,
    json_extract(value, '$.name') as tool_name,
    COUNT(*) as usage_count
FROM conversation_events,
     json_each(json_extract(event_data, '$.message.content'))
WHERE event_type = 'assistant'
    AND json_extract(value, '$.type') = 'tool_use'
    AND json_extract(value, '$.name') IS NOT NULL
    AND DATE(inserted_at) >= DATE('now', '-30 days')
GROUP BY date, tool_name
ORDER BY date DESC, usage_count DESC;
```

### Tool Usage by Repository

```sql
SELECT
    CASE
        WHEN git_remote_url IS NULL THEN '(no repo)'
        ELSE SUBSTR(git_remote_url, INSTR(git_remote_url, '/') + 1)
    END as repository,
    json_extract(value, '$.name') as tool_name,
    COUNT(*) as usage_count
FROM conversation_events,
     json_each(json_extract(event_data, '$.message.content'))
WHERE event_type = 'assistant'
    AND json_extract(value, '$.type') = 'tool_use'
    AND json_extract(value, '$.name') IS NOT NULL
GROUP BY git_remote_url, tool_name
ORDER BY usage_count DESC
LIMIT 30;
```

### Tool Combinations (Most Common Pairs)

```sql
WITH tool_sessions AS (
    SELECT
        event_session_id,
        json_extract(value, '$.name') as tool_name
    FROM conversation_events,
         json_each(json_extract(event_data, '$.message.content'))
    WHERE event_type = 'assistant'
        AND json_extract(value, '$.type') = 'tool_use'
        AND json_extract(value, '$.name') IS NOT NULL
)
SELECT
    a.tool_name as tool_1,
    b.tool_name as tool_2,
    COUNT(DISTINCT a.event_session_id) as sessions_together
FROM tool_sessions a
JOIN tool_sessions b ON a.event_session_id = b.event_session_id
WHERE a.tool_name < b.tool_name
GROUP BY a.tool_name, b.tool_name
ORDER BY sessions_together DESC
LIMIT 15;
```

### Sessions by Tool Intensity

```sql
SELECT
    event_session_id,
    COUNT(*) as total_tool_uses,
    COUNT(DISTINCT json_extract(value, '$.name')) as unique_tools,
    MIN(inserted_at) as session_start,
    git_remote_url
FROM conversation_events,
     json_each(json_extract(event_data, '$.message.content'))
WHERE event_type = 'assistant'
    AND json_extract(value, '$.type') = 'tool_use'
GROUP BY event_session_id
ORDER BY total_tool_uses DESC
LIMIT 20;
```

---

## Response Format

When triggered, provide:

1. **Overview** - Most used tools overall
2. **Trends** - Tool usage patterns over time
3. **Context** - Which repos use which tools
4. **Insights** - Interesting patterns

### Example Output

```
🔧 Claude Tool Usage Analysis

Top Tools (All Time):
1. Read: 487 uses (32.4%)
2. Bash: 312 uses (20.8%)
3. Edit: 289 uses (19.2%)
4. Grep: 178 uses (11.8%)
5. Glob: 156 uses (10.4%)
6. Write: 82 uses (5.5%)

Recent Trends (Last 7 days):
- Read usage increased 23%
- Task tool emerging (+45 uses)
- Bash usage stable

By Repository:
- vibe-check: Heavy Read + Bash (database work)
- my-app: Heavy Edit + Write (active development)
- docs: Heavy Write (documentation)

Common Tool Combinations:
- Grep → Read (78 sessions)
- Glob → Read (65 sessions)
- Read → Edit (52 sessions)

Most Tool-Intensive Session:
- Session abc123 (vibe-check, 2026-01-10)
  42 tool uses, 8 unique tools
```

---

## Advanced Analysis (if requested)

### File Operation Patterns

Analyze Read/Write/Edit patterns to show which files Claude works with most.

### Error Analysis

Search for tool errors in responses to identify common issues.

### Efficiency Metrics

Calculate avg tools per session, tools per message, etc.

---

## Visualization Suggestions

If user wants visual analysis, suggest:
- Export to CSV and visualize in spreadsheet
- Generate simple text-based charts
- Create timeline of tool adoption
