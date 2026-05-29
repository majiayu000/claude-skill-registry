---
name: metrics-dashboard
description: Tracks pipeline velocity, success rates, and cycle times. Use to view performance metrics, identify bottlenecks, and generate reports.
---

# Metrics Dashboard

Aggregates pipeline run data to track velocity, success rates, and identify improvement areas.

## Data Sources

- `runs/*/status.json` - Phase timestamps, success/failure
- `runs/*/ticket.json` - Ticket metadata
- Git history - Commit and PR data
- Notion - Ticket status transitions

## Workflow

### 1. Collect Run Data

```bash
find runs/ -name "status.json" -type f | while read f; do
  jq -c '{
    id: .ticketId,
    status: .status,
    started: .intakeAt,
    completed: .completedAt,
    phases: .phaseTimestamps
  }' "$f"
done > /tmp/runs-data.jsonl
```

### 2. Calculate Metrics

**Cycle Time:**

```bash
jq -s '
  map(select(.completed != null)) |
  map(.cycleTime = ((.completed | fromdate) - (.started | fromdate)) / 3600) |
  {
    avgCycleTimeHours: (map(.cycleTime) | add / length),
    minCycleTimeHours: (map(.cycleTime) | min),
    maxCycleTimeHours: (map(.cycleTime) | max)
  }
' /tmp/runs-data.jsonl
```

**Success Rate:**

```bash
jq -s '{
  total: length,
  completed: (map(select(.status == "done")) | length),
  failed: (map(select(.status == "failed")) | length),
  inProgress: (map(select(.status | test("^(implementing|review|pr-created)$"))) | length)
} | .successRate = (.completed / .total * 100)' /tmp/runs-data.jsonl
```

**Phase Duration:**

```bash
jq -s '
  map(.phases) | flatten | group_by(.phase) |
  map({phase: .[0].phase, avgMinutes: (map(.durationSeconds) | add / length / 60)})
' /tmp/runs-data.jsonl
```

### 3. Generate Dashboard

```markdown
# Pipeline Metrics Dashboard

**Period:** Last 30 days | **Generated:** {timestamp}

## Summary

| Metric            | Value   | Trend      |
| ----------------- | ------- | ---------- |
| Tickets Completed | 12      | ↑ +3       |
| Success Rate      | 83%     | ↑ +5%      |
| Avg Cycle Time    | 2.5 hrs | ↓ -0.5 hrs |

## Cycle Time Breakdown

Intake ████ 5 min | Research ████████ 15 min | Planning ██████ 10 min
Implement █████████████ 25 min | Quality ████ 8 min | Review ██████ 12 min

## Success by Type

| Type     | Count | Success | Avg Time |
| -------- | ----- | ------- | -------- |
| Bug Fix  | 5     | 100%    | 1.2 hrs  |
| Feature  | 4     | 75%     | 3.5 hrs  |
| Refactor | 3     | 67%     | 2.8 hrs  |

## Failure Analysis

| Failure Point    | Count | %   |
| ---------------- | ----- | --- |
| Quality gates    | 2     | 40% |
| CI failures      | 1     | 20% |
| Review rejection | 1     | 20% |

## Recommendations

1. **Reduce implementation time** - Consider more parallel subagents
2. **Improve quality gates** - 40% of failures at this stage
```

### 4. Save Dashboard

```bash
echo "$DASHBOARD" > "$RUN_DIR/../metrics-$(date +%Y-%m-%d).md"

cat > runs/metrics-summary.json << EOF
{"generatedAt": "$(date -Iseconds)", "period": "30d", "totalRuns": $TOTAL, "successRate": $SUCCESS_RATE, "avgCycleTimeHours": $AVG_CYCLE}
EOF

# Append to history
jq -c '{date: now | strftime("%Y-%m-%d"), metrics: .}' runs/metrics-summary.json >> runs/metrics-history.jsonl
```

## Custom Queries

```bash
# Tickets by assignee
jq -s 'group_by(.assignee) | map({assignee: .[0].assignee, count: length})' /tmp/runs-data.jsonl

# Slowest tickets
jq -s 'sort_by(.cycleTime) | reverse | .[0:5]' /tmp/runs-data.jsonl

# Failed at phase
jq -s 'map(select(.status == "failed")) | group_by(.failedAtPhase)' /tmp/runs-data.jsonl
```

## Notion Integration (Optional)

Prompt user before syncing metrics to Notion.

## Output Artifacts

| File                  | Location | Description             |
| --------------------- | -------- | ----------------------- |
| metrics-{date}.md     | `runs/`  | Point-in-time dashboard |
| metrics-summary.json  | `runs/`  | Latest metrics JSON     |
| metrics-history.jsonl | `runs/`  | Historical trends       |
