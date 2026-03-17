---
name: get-mission-history
version: "1.0.0"
description: >
  Show the execution history of a background mission. Displays recent runs,
  their outcomes, tool call counts, anomalies found, and notifications sent.
  Use when the user asks to see what a mission has done, its run history,
  or past results. Keywords: mission, history, runs, results, log, past, outcomes.
metadata:
  domain: general
  category: missions
  requires-approval: false
  confidence: 0.95
  mcp-servers: []
---

# Get Mission History

Shows the execution history for a background mission.

## Preconditions

- A mission ID or title is provided
- The mission exists and belongs to the current user

## Actions

### 1. Resolve Mission ID

Fetch the mission to confirm it exists.

### 2. Fetch Run History

```python
result = await temporal_client.execute_activity(
    "list_mission_runs_activity",
    {
        "mission_id": mission_id,
        "limit": 20,
    }
)
runs = result["runs"]
```

### 3. Format the Response

Present runs in a clear table format:

```
📊 Mission History: **Cluster health monitor** (mission-abc123)
Schedule: Every 30 minutes | Status: Active | Total runs: 47

Recent runs (last 10):

Run #47 — 2025-02-23 14:00 UTC ✅ Completed (12 tool calls, 45s)
  No anomalies found. All pods healthy.

Run #46 — 2025-02-23 13:30 UTC ⚠️  Anomaly (15 tool calls, 52s)
  ⚡ Notification sent: "Pod nginx-abc in CrashLoopBackOff (3 restarts)"

Run #45 — 2025-02-23 13:00 UTC ✅ Completed (8 tool calls, 31s)
  No anomalies found.

Run #44 — 2025-02-23 12:30 UTC ❌ Failed (2 tool calls, 5s)
  Error: Could not connect to Kubernetes API. Retrying next run.
```

### 4. If No Runs Exist

```
No runs recorded yet for this mission.
The first run is scheduled for: 15:00
```

## Success Criteria

- [ ] Run history retrieved and formatted clearly
- [ ] Status icons used for quick scanning
- [ ] Notification text shown for anomaly runs

## Failure Handling

- If mission not found: list available missions
- If no runs: inform the user and show next scheduled run

## Examples

**User:** "Show me the history for the cluster health monitor"
**User:** "What has mission mission-abc123 done?"
**User:** "Show me the last 5 runs of my news digest"
