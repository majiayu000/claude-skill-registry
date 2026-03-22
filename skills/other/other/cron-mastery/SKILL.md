---
name: cron-mastery
version: 1.0.0
description: Master cron scheduling for automated tasks, reminders, and periodic workflows.
metadata:
  openclaw:
    emoji: ⏰
    category: automation
---

# Cron Mastery

Schedule automated tasks, reminders, and periodic workflows using OpenClaw's cron system.

## Quick Reference

### Schedule Types

| Type | Format | Example |
|------|--------|---------|
| **at** | ISO timestamp | `2026-02-20T09:00:00Z` |
| **every** | Interval in ms | `everyMs: 3600000` (1 hour) |
| **cron** | Cron expression | `0 9 * * 1-5` (9am weekdays) |

### Common Patterns

```yaml
# Daily at 9am
cron: "0 9 * * *"

# Every hour
everyMs: 3600000

# Monday at 8am
cron: "0 8 * * 1"

# Every 30 minutes during business hours
cron: "*/30 9-17 * * 1-5"
```

## Use Cases

### 1. Daily Morning Brief

```json
{
  "name": "morning-brief",
  "schedule": {"kind": "cron", "expr": "0 8 * * *", "tz": "Europe/Berlin"},
  "payload": {"kind": "agentTurn", "message": "Generate morning brief: check emails, calendar, priorities"},
  "sessionTarget": "isolated"
}
```

### 2. Periodic Health Checks

```json
{
  "name": "health-check",
  "schedule": {"kind": "every", "everyMs": 3600000},
  "payload": {"kind": "systemEvent", "text": "Heartbeat: check system status"},
  "sessionTarget": "main"
}
```

### 3. Reminder

```json
{
  "name": "meeting-reminder",
  "schedule": {"kind": "at", "at": "2026-02-20T14:30:00Z"},
  "payload": {"kind": "systemEvent", "text": "Reminder: Meeting in 30 minutes"},
  "sessionTarget": "main"
}
```

## Job Management

| Action | Command |
|--------|---------|
| List jobs | `cron(action="list")` |
| Add job | `cron(action="add", job={...})` |
| Update | `cron(action="update", jobId="xxx", patch={...})` |
| Remove | `cron(action="remove", jobId="xxx")` |
| Run now | `cron(action="run", jobId="xxx")` |
| History | `cron(action="runs", jobId="xxx")` |

## Best Practices

1. **Use isolated sessions** for agentTurn jobs (clean context)
2. **Set notify=true** for user-facing reminders
3. **Use descriptive names** for easy identification
4. **Test before scheduling** — use `run(action="run")` first
5. **Review runs periodically** — check for failures

## Heartbeat vs Cron

| Use | Cron | Heartbeat |
|-----|------|-----------|
| Exact timing | ✅ | ❌ |
| Isolated execution | ✅ | ❌ |
| User reminders | ✅ | ⚠️ |
| Batch checks | ❌ | ✅ |
| Context-dependent | ❌ | ✅ |

## Example: Self-Improving Agent Schedule

```json
{
  "name": "weekly-learning-review",
  "schedule": {"kind": "cron", "expr": "0 10 * * 0", "tz": "Europe/Berlin"},
  "payload": {
    "kind": "agentTurn",
    "message": "Review self-improving-agent learnings. Consolidate to MEMORY.md. Report insights."
  },
  "sessionTarget": "isolated",
  "notify": true
}
```
