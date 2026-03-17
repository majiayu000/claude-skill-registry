---
name: resume-mission
version: "1.0.0"
description: >
  Resume a paused background mission. The mission will resume executing on its
  original schedule. Use when the user wants to restart a previously paused
  mission. Keywords: mission, resume, restart, enable, activate, unpause.
metadata:
  domain: general
  category: missions
  requires-approval: false
  confidence: 0.95
  mcp-servers: []
---

# Resume Mission

Resumes a paused background mission, restoring it to its original schedule.

## Preconditions

- A mission ID or title is provided
- The mission exists and belongs to the current user
- The mission is currently paused

## Actions

### 1. Resolve Mission ID

If the user provides a title instead of an ID, search for the matching mission.

### 2. Resume the Mission

```python
from kubani.nexus.missions.scheduler import compute_next_run

# Recompute next_run_at so it fires at the correct next interval
next_run_at = compute_next_run(mission["schedule"])

result = await temporal_client.execute_activity(
    "update_mission_status_activity",
    {
        "mission_id": mission_id,
        "status": "active",
        "user_id": user_id,
    }
)
```

### 3. Confirm to User

```
▶️  Mission resumed: **Cluster health monitor** (mission-abc123)

The agent will resume checking your cluster health every 30 minutes.
Next run: 15:00
```

## Success Criteria

- [ ] Mission status updated to "active"
- [ ] next_run_at recomputed correctly
- [ ] User receives confirmation with next run time

## Failure Handling

- If mission not found: list available missions
- If already active: inform the user it is already running

## Examples

**User:** "Resume the cluster health monitor"
**User:** "Restart mission mission-abc123"
**User:** "Re-enable my daily news digest"
