---
name: list-missions
version: "1.0.0"
description: >
  List all proactive background missions for the current user. Shows mission
  titles, schedules, statuses, and last run times. Use when the user asks to
  see their missions, what's running in the background, or what scheduled tasks
  exist. Keywords: missions, list, show, background, scheduled, active, paused.
metadata:
  domain: general
  category: missions
  requires-approval: false
  confidence: 0.95
  mcp-servers: []
---

# List Missions

Lists all proactive background missions for the current user.

## Preconditions

- User is authenticated (user_id is available)

## Actions

### 1. Fetch Missions

Call the `list_missions_activity` Temporal activity:

```python
result = await temporal_client.execute_activity(
    "list_missions_activity",
    {
        "user_id": user_id,
        "status": None,  # None = all statuses; or "active", "paused", etc.
    }
)
missions = result["missions"]
```

### 2. Format the Response

Present missions as a structured list:

```
📋 Your Background Missions (3 active, 1 paused)

🟢 Cluster health monitor (mission-abc123)
   Schedule: Every 30 minutes | Next run: 14:30
   Last run: 14:00 — No anomalies found
   Policy: nexus-proactive | Tool budget: 15

🟢 Daily AI news digest (mission-def456)
   Schedule: Daily at 9am | Next run: Tomorrow 09:00
   Last run: Today 09:00 — Digest sent
   Policy: nexus | Tool budget: 20

⏸️  Weekly cost report (mission-ghi789)
   Schedule: Weekly Monday | Status: PAUSED
   Last run: Last Monday — Report generated
```

### 3. If No Missions Exist

```
You don't have any background missions yet.

To create one, try:
- "Monitor my cluster health every 30 minutes"
- "Send me a daily summary of AI news at 9am"
- "Check for new GitHub issues in my repos every hour"
```

## Success Criteria

- [ ] All missions returned and formatted clearly
- [ ] Status indicators are accurate
- [ ] Next run time is shown for active missions

## Failure Handling

If the database is unreachable, return a friendly error and suggest retrying.

## Examples

**User request:** "What missions are running?"

**Response:** Formatted list as shown above.

**User request:** "Show me only my active missions"

**Extracted parameters:**
```json
{ "status": "active" }
```
