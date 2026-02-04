---
name: search-conversations
description: Search through Claude Code conversation history. Use when user says "search my conversations", "find when I talked about X", "what did claude say about Y", or "search claude history".
---

# Search Claude Conversations

**Purpose:** Search through Claude Code conversation history stored in the local vibe-check database

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

## Search Queries

### Search Messages by Content

```sql
SELECT
    event_session_id,
    event_type,
    SUBSTR(event_message, 1, 150) as message_preview,
    inserted_at,
    git_remote_url,
    file_name
FROM conversation_events
WHERE event_message LIKE '%{search_term}%'
    AND event_message IS NOT NULL
ORDER BY inserted_at DESC
LIMIT 20;
```

### Search by Repository

```sql
SELECT
    event_session_id,
    event_type,
    SUBSTR(event_message, 1, 150) as message_preview,
    inserted_at,
    file_name
FROM conversation_events
WHERE git_remote_url LIKE '%{repo_name}%'
ORDER BY inserted_at DESC
LIMIT 20;
```

### Search by Date Range

```sql
SELECT
    event_session_id,
    event_type,
    SUBSTR(event_message, 1, 150) as message_preview,
    inserted_at,
    git_remote_url
FROM conversation_events
WHERE DATE(inserted_at) BETWEEN '{start_date}' AND '{end_date}'
    AND event_message IS NOT NULL
ORDER BY inserted_at DESC
LIMIT 50;
```

### Search by Session ID

```sql
SELECT
    event_type,
    event_message,
    inserted_at,
    line_number
FROM conversation_events
WHERE event_session_id = '{session_id}'
ORDER BY line_number ASC;
```

### Find Sessions About a Topic

```sql
SELECT
    event_session_id,
    COUNT(*) as mentions,
    MIN(inserted_at) as first_mention,
    MAX(inserted_at) as last_mention,
    MAX(git_remote_url) as repository
FROM conversation_events
WHERE event_message LIKE '%{topic}%'
GROUP BY event_session_id
ORDER BY mentions DESC
LIMIT 10;
```

---

## Usage Flow

When user requests a search:

1. **Extract search criteria** from user's question:
   - Search term/keyword
   - Date range (if specified)
   - Repository (if specified)
   - Session ID (if specified)

2. **Construct appropriate query** based on criteria

3. **Execute query** using Bash with sqlite3

4. **Format results** in readable form:
   - Show context (date, repo, session)
   - Limit message previews to ~150 chars
   - Provide session IDs for deeper exploration
   - Provide URL to explore session in browser: https://vibecheck.wanderingstan.com/messages?session_id=SESSION_ID

5. **Offer follow-up actions**:
   - "View full session"
   - "Narrow search"
   - "Export results"

---

## Example Interactions

### Example 1: Keyword Search

```
User: "search my conversations for 'authentication'"

Claude:
Found 12 messages mentioning 'authentication':

Session a4b2c (2026-01-10, vibe-check repo) https://vibecheck.wanderingstan.com/messages?session_id=a4b2c :
  [user]: "How do I implement authentication in..."
  [assistant]: "For authentication, you should consider..."

Session f7d3e (2026-01-05, my-app repo) https://vibecheck.wanderingstan.com/messages?session_id=f7d3e :
  [assistant]: "The authentication flow uses JWT tokens..."

Would you like to:
- View full session details
- Search for related terms
- Export results
```

### Example 2: Recent Work

```
User: "what did I work on yesterday?"

Claude: [Searches for date = yesterday]

Yesterday (2026-01-12) you had 3 sessions:
1. Session abc123 (vibe-check): Worked on database skills - https://vibecheck.wanderingstan.com/messages?session_id=abc123
2. Session def456 (my-app): Fixed authentication bug - https://vibecheck.wanderingstan.com/messages?session_id=def456
3. Session ghi789 (website): Updated landing page - https://vibecheck.wanderingstan.com/messages?session_id=ghi789

Which session would you like to explore?
```

---

## Advanced Features

### Get Full Conversation Context

When user wants to see full session:

```sql
SELECT
    event_type,
    event_message,
    inserted_at,
    JSON_EXTRACT(event_data, '$.message.content[0].type') as content_type
FROM conversation_events
WHERE event_session_id = '{session_id}'
ORDER BY line_number ASC;
```

### Find Similar Sessions

Based on git repo and search term:

```sql
SELECT
    event_session_id,
    COUNT(*) as relevance_score,
    MIN(inserted_at) as session_date,
    git_remote_url
FROM conversation_events
WHERE git_remote_url = '{current_repo}'
    AND event_message LIKE '%{search_term}%'
GROUP BY event_session_id
ORDER BY relevance_score DESC
LIMIT 5;
```

---

## Error Handling

- If no results found, suggest:
  - Broader search terms
  - Different date range
  - Checking if monitor captured that period
- If database not accessible, guide user to check installation
