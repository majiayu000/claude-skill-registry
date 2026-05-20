---
name: pause-mission
version: "1.0.0"
description: >
  Pause a running background mission. The mission will stop executing on its
  schedule until resumed. Use when the user wants to temporarily stop a mission
  without deleting it. Keywords: mission, pause, stop, suspend, disable.
metadata:
  domain: general
  category: missions
  requires-approval: false
  confidence: 0.95
  mcp-servers: []
---

# Pause Mission

Pauses a background mission so it stops executing on its schedule.

## Preconditions

- A mission ID or title is provided
- The mission exists and belongs to the current user
- The mission is currently active

## Actions

### 1. Resolve Mission ID

If the user provides a title instead of an ID, search for the matching mission:

```python
missions = await list_missions_activity({"user_id": user_id})
match = next((m for m in missions["missions"] if title in m["title"]), None)
mission_id = match["id"]
```

### 2. Pause the Mission

```python
result = await temporal_client.execute_activity(
    "update_mission_status_activity",
    {
        "mission_id": mission_id,
        "status": "paused",
        "user_id": user_id,
    }
)
```

### 3. Confirm to User

```
⏸️  Mission paused: **Cluster health monitor** (mission-abc123)

The agent will no longer run this mission automatically.
To resume it, say: "resume mission mission-abc123"
```

## Success Criteria

- [ ] Mission status updated to "paused"
- [ ] User receives confirmation

## Failure Handling

- If mission not found: list available missions and ask for clarification
- If already paused: inform the user it is already paused

## Examples

**User:** "Pause the cluster health monitor"
**User:** "Stop mission mission-abc123"
**User:** "Disable my daily news digest"
