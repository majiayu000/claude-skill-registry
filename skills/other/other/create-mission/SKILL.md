---
name: create-mission
version: "1.0.0"
description: >
  Create a new proactive background mission for the Nexus agent. A mission is a
  scheduled, autonomous task that the agent executes on a cron schedule without
  user interaction. Use this skill when the user asks to monitor something
  automatically, run a recurring check, or set up a background task.
  Keywords: mission, create, schedule, monitor, background, recurring, automatic,
  proactive, cron, periodic.
metadata:
  domain: general
  category: missions
  requires-approval: false
  confidence: 0.95
  mcp-servers: []
---

# Create Mission

Creates a new proactive background mission that the Nexus agent will execute
autonomously on a schedule.

## Preconditions

Before applying this skill, verify:

- User has provided a clear goal for the mission
- A schedule has been specified or can be inferred (default: every hour)
- The goal is achievable with the available MCP tools

## Actions

### 1. Determine Mission Parameters

Extract from the user's request:

```yaml
title: Short human-readable title (max 80 chars)
goal: Natural language description of what the agent should do
schedule: Cron expression (default: "0 * * * *" = every hour)
mcp_policy: "nexus" for safe missions, "nexus-proactive" for cluster access
max_tool_calls: 1-50 (default: 20)
notify_on: ["anomaly", "error"] — when to notify the user
```

**Schedule reference:**
| Schedule | Cron Expression |
|---|---|
| Every 5 minutes | `*/5 * * * *` |
| Every 15 minutes | `*/15 * * * *` |
| Every 30 minutes | `*/30 * * * *` |
| Every hour | `0 * * * *` |
| Every 6 hours | `0 */6 * * *` |
| Twice daily | `0 9,21 * * *` |
| Daily at 9am | `0 9 * * *` |
| Weekly Monday | `0 9 * * 1` |

**Policy reference:**
- `nexus` — memory, skills, fetch (safe, no cluster access)
- `nexus-proactive` — adds kubernetes, discord, temporal (for monitoring missions)

**notify_on options:**
- `always` — notify after every run
- `anomaly` — notify when the agent flags something unusual
- `error` — notify when the mission fails
- `completion` — notify when the mission completes
- `never` — silent mode

### 2. Validate Parameters

- Confirm the cron expression is valid (5-field standard cron)
- Confirm max_tool_calls is between 1 and 50
- Confirm the goal is specific enough to be actionable

### 3. Create the Mission

Call the `create_mission_activity` Temporal activity:

```python
result = await temporal_client.execute_activity(
    "create_mission_activity",
    {
        "user_id": user_id,
        "title": title,
        "goal": goal,
        "schedule": schedule,
        "mcp_policy": mcp_policy,
        "max_tool_calls": max_tool_calls,
        "notify_on": notify_on,
    }
)
```

### 4. Confirm to User

Respond with a confirmation that includes:
- Mission title and ID
- Schedule in human-readable form
- When the first run will occur
- What the agent will do

## Success Criteria

The skill succeeds when:

- [ ] Mission created in the database
- [ ] next_run_at is computed and stored
- [ ] User receives a clear confirmation with mission ID

## Failure Handling

If creation fails:

1. If invalid cron: explain valid cron syntax and suggest a preset
2. If goal is too vague: ask for clarification
3. If database error: retry once, then report the error

## Examples

**User request:** "Monitor my cluster health every 30 minutes and alert me if anything is wrong"

**Extracted parameters:**
```json
{
  "title": "Cluster health monitor",
  "goal": "Check the overall health of the Kubernetes cluster. Look for pods in CrashLoopBackOff or Error state, nodes with high resource usage, and any recent events that indicate problems. Flag anything that requires attention.",
  "schedule": "*/30 * * * *",
  "mcp_policy": "nexus-proactive",
  "max_tool_calls": 15,
  "notify_on": ["anomaly", "error"]
}
```

**Response to user:**
```
✅ Mission created: **Cluster health monitor** (mission-abc123)

The agent will check your cluster health every 30 minutes, starting at 14:30.
You'll be notified if any anomalies are found or if the mission encounters an error.

To manage this mission:
- Pause: "pause mission mission-abc123"
- View history: "show mission history for mission-abc123"
- Delete: "delete mission mission-abc123"
```
