---
name: sentry-alerts-issues
description: Use when configuring Sentry alerts, managing issues, or setting up notifications. Covers alert rules, issue triage, and integrations.
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Grep
  - Glob
---

# Sentry - Alerts & Issue Management

Configure alerts, manage issues, and set up notifications.

## Alert Types

### Issue Alerts

Trigger when an issue matches specific conditions:

- New issue created
- Issue changes state (resolved → unresolved)
- Issue frequency exceeds threshold
- Issue affects specific users/releases

### Metric Alerts

Trigger based on aggregate metrics:

- Error count exceeds threshold
- Transaction latency (p50, p95, p99)
- Failure rate percentage
- Apdex score drops

### Uptime Monitoring

Monitor endpoint availability:

- HTTP status codes
- Response time thresholds
- SSL certificate expiration

## Alert Conditions

### Frequency-Based

```
When an issue is seen more than 100 times in 1 hour
```

### User Impact

```
When an issue affects more than 50 unique users in 1 hour
```

### First Seen

```
When a new issue is created
```

### Regression

```
When an issue changes state from resolved to unresolved
```

## Alert Actions

### Notification Channels

- **Email**: Individual or team distribution
- **Slack**: Channel or direct messages
- **PagerDuty**: On-call escalation
- **Discord**: Webhook notifications
- **Microsoft Teams**: Channel posts
- **Webhooks**: Custom integrations

### Issue Actions

- Assign to team member
- Add tags
- Create ticket (Jira, Linear, GitHub)

## Issue States

### Lifecycle

1. **Unresolved**: Active issue needing attention
2. **Resolved**: Fixed in a release
3. **Ignored**: Intentionally dismissed
4. **Archived**: Historical, no longer tracked

### Substates

- **For Review**: Needs triage
- **Escalating**: Increasing in frequency
- **Regressed**: Previously resolved, now recurring
- **New**: First seen recently

## Issue Management

### Merge Issues

Combine duplicate issues with different stack traces:

1. Select issues to merge
2. Choose primary issue
3. All events appear under primary

### Ignore Rules

```
Ignore this issue:
- Forever
- Until it happens again
- For the next 24 hours
- Until it affects 100 users
```

### Ownership Rules

```
# Define in project settings
path:src/payments/* #payments-team
path:src/auth/* user@example.com
tags.component:checkout #checkout-team
```

## API Integration

### List Issues

```bash
curl "https://sentry.io/api/0/projects/{org}/{project}/issues/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN"
```

### Update Issue

```bash
curl -X PUT "https://sentry.io/api/0/issues/{issue_id}/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status": "resolved"}'
```

### Create Alert Rule

```bash
curl -X POST "https://sentry.io/api/0/projects/{org}/{project}/rules/" \
  -H "Authorization: Bearer $SENTRY_AUTH_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "High Error Rate",
    "conditions": [...],
    "actions": [...],
    "frequency": 30
  }'
```

## Integration Examples

### Slack Alert

```json
{
  "action": "notify_slack",
  "workspace": "your-workspace",
  "channel": "#alerts",
  "tags": ["level", "environment"]
}
```

### PagerDuty Escalation

```json
{
  "action": "notify_pagerduty",
  "service": "your-service-key",
  "severity": "critical"
}
```

### Jira Ticket Creation

```json
{
  "action": "create_jira_ticket",
  "integration": "jira-integration-id",
  "project": "PROJ",
  "issueType": "Bug"
}
```

## Best Practices

1. Start with conservative thresholds, tune over time
2. Use different channels for different severities
3. Set up on-call rotation for critical alerts
4. Review and archive stale issues regularly
5. Define ownership rules for automatic assignment
6. Create runbooks for common alert types
7. Use metric alerts for SLO monitoring
