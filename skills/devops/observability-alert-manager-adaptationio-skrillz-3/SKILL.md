---
name: observability-alert-manager
description: Configure Grafana alerts for Claude Code anomalies and thresholds. Use when setting up monitoring alerts for sessions, errors, context usage, or subagents.
---

# Observability Alert Manager

Configure and manage Grafana alerts for Claude Code monitoring using enhanced telemetry.

## Data Source

Primary: `{job="claude_code_enhanced"}` in Loki

## Operations

### `create-alert`
Define new alert rule.
**Parameters**: name, query (LogQL), threshold, duration, severity, notification.

### `list-alerts`
Show all configured alerts and their status.

### `test-alert`
Simulate alert conditions.

### `delete-alert`
Remove alert rule.

## Pre-built Alert Templates

### Session Alerts
1. **Long Session Duration**: Session >1 hour
   ```logql
   {job="claude_code_enhanced", event_type="session_end"} | json | duration_seconds > 3600
   ```

2. **High Turn Count**: Session >50 turns
   ```logql
   {job="claude_code_enhanced", event_type="session_end"} | json | turn_count > 50
   ```

3. **Session Error Spike**: >5 errors in session
   ```logql
   {job="claude_code_enhanced", event_type="session_end"} | json | error_count > 5
   ```

### Error Alerts
4. **High Error Rate**: >5 errors/hour
   ```logql
   count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error"} [1h]) > 5
   ```

5. **Specific Tool Failures**: Bash errors
   ```logql
   count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error", tool="Bash"} [1h]) > 3
   ```

### Context Alerts
6. **High Context Usage**: >80% context window
   ```logql
   {job="claude_code_enhanced", event_type="context_utilization"} | json | context_percentage > 80
   ```

7. **Auto Compaction Triggered**: Context full
   ```logql
   {job="claude_code_enhanced", event_type="context_compact", trigger="auto"}
   ```

### Subagent Alerts
8. **Excessive Subagent Spawning**: >10 subagents/session
   ```logql
   {job="claude_code_enhanced", event_type="session_end"} | json | subagents_spawned > 10
   ```

### Activity Alerts
9. **Telemetry Staleness**: No data >10min
   ```logql
   absent_over_time({job="claude_code_enhanced"} [10m])
   ```

10. **Unusual Activity Spike**: >100 tool calls/hour
    ```logql
    count_over_time({job="claude_code_enhanced", event_type="tool_call"} [1h]) > 100
    ```

### Prompt Pattern Alerts
11. **Debugging Session Spike**: Many debugging prompts
    ```logql
    count_over_time({job="claude_code_enhanced", event_type="user_prompt", pattern="debugging"} [1h]) > 10
    ```

## Example Alert Configurations

### Create High Error Rate Alert
```bash
create-alert \
  --name "High Error Rate" \
  --query 'count_over_time({job="claude_code_enhanced", event_type="tool_result", status="error"} [1h]) > 5' \
  --severity warning \
  --notification slack
```

### Create Context Usage Alert
```bash
create-alert \
  --name "High Context Usage" \
  --query '{job="claude_code_enhanced", event_type="context_utilization"} | json | context_percentage > 80' \
  --severity info \
  --notification email
```

### Create Session Duration Alert
```bash
create-alert \
  --name "Long Session Warning" \
  --query '{job="claude_code_enhanced", event_type="session_end"} | json | duration_seconds > 3600' \
  --severity info \
  --notification dashboard
```

## Grafana Alert Setup

### Via Grafana UI
1. Navigate to Alerting → Alert rules
2. Create new rule with Loki data source
3. Enter LogQL query from templates above
4. Configure conditions and notifications

### Via API
```bash
curl -X POST http://localhost:3000/api/ruler/grafana/api/v1/rules/claude-code \
  -H "Content-Type: application/json" \
  -u admin:admin \
  -d '{
    "name": "claude-code-alerts",
    "rules": [
      {
        "alert": "HighErrorRate",
        "expr": "count_over_time({job=\"claude_code_enhanced\", status=\"error\"} [1h]) > 5",
        "for": "5m",
        "labels": {"severity": "warning"},
        "annotations": {"summary": "High error rate detected"}
      }
    ]
  }'
```

## Notification Channels

- **Slack**: Webhook integration
- **Email**: SMTP configuration
- **PagerDuty**: Incident management
- **Dashboard**: On-screen annotations

## Alert Severity Levels

| Level | Use Case |
|-------|----------|
| `critical` | Immediate action required |
| `warning` | Needs attention soon |
| `info` | Informational, no action needed |

## Scripts

- `scripts/create-alert.sh` - Create new alert
- `scripts/list-alerts.sh` - List all alerts
- `scripts/test-alerts.sh` - Test alert conditions
- `scripts/import-alert-templates.sh` - Import all pre-built templates
