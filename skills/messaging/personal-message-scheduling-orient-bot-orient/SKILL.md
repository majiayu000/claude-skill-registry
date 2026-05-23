---
name: personal-message-scheduling
description: Create, manage, and execute scheduled WhatsApp and Slack messages. Use this skill when asked to "schedule a message", "create a reminder", "set up recurring notifications", "schedule standup reminders", "automate daily/weekly messages", or any task involving time-based message delivery. Supports cron expressions, recurring intervals, and one-time scheduled messages. Works on both local (localhost:4098) and production (ai.proph.bet) environments.
---

# Message Scheduling

Create automated scheduled messages for WhatsApp groups/contacts or Slack channels.

## Quick Start

1. Determine the API base URL based on environment:
   - **Local/Development**: `http://localhost:4098`
   - **Production**: `https://ai.proph.bet/dashboard`

2. Use curl to create a scheduled job:

```bash
# Set API base (local or production)
API_BASE="http://localhost:4098"  # or https://ai.proph.bet/dashboard

curl -X POST "${API_BASE}/api/schedules" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Standup Reminder",
    "scheduleType": "cron",
    "cronExpression": "0 9 * * 1-5",
    "timezone": "Asia/Jerusalem",
    "provider": "whatsapp",
    "target": "120363406740668957@g.us",
    "messageTemplate": "🔔 Standup in 10 minutes!\n\nDate: {{date}}\nDay: {{day}}",
    "enabled": true
  }'
```

## Schedule Types

### Cron (most flexible)

Use for complex schedules. See [references/cron-reference.md](references/cron-reference.md) for presets and syntax.

```json
{
  "scheduleType": "cron",
  "cronExpression": "0 9 * * 1-5"
}
```

### Recurring (interval-based)

Run at fixed intervals (in minutes):

```json
{
  "scheduleType": "recurring",
  "intervalMinutes": 60
}
```

### One-Time

Run once at a specific ISO 8601 timestamp, then auto-disable:

```json
{
  "scheduleType": "once",
  "runAt": "2026-01-15T09:00:00.000Z"
}
```

## Required Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Job name (required) |
| `scheduleType` | string | `cron`, `recurring`, or `once` |
| `provider` | string | `whatsapp` or `slack` |
| `target` | string | WhatsApp JID or Slack channel ID |
| `messageTemplate` | string | Message content with optional variables |

## Target Lookup

- **WhatsApp groups**: Use JID format `XXXXXXXXX@g.us`
- **WhatsApp contacts**: Use `9725XXXXXXXX@s.whatsapp.net`
- **Slack channels**: Use channel ID (e.g., `C01234567`)

See [references/known-targets.md](references/known-targets.md) for common targets.

## Template Variables

| Variable | Example | Description |
|----------|---------|-------------|
| `{{date}}` | `2026-01-07` | Current date (YYYY-MM-DD) |
| `{{time}}` | `14:30` | Current time (HH:MM) |
| `{{day}}` | `Tuesday` | Day of week |
| `{{month}}` | `January` | Month name |
| `{{year}}` | `2026` | Year |
| `{{datetime}}` | `2026-01-07T14:30:00.000Z` | Full ISO datetime |

## API Endpoints

All endpoints require Bearer token auth when applicable.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/schedules` | List all jobs |
| `POST` | `/api/schedules` | Create job |
| `GET` | `/api/schedules/:id` | Get job details |
| `PATCH` | `/api/schedules/:id` | Update job |
| `DELETE` | `/api/schedules/:id` | Delete job |
| `POST` | `/api/schedules/:id/toggle` | Toggle enabled |
| `POST` | `/api/schedules/:id/run` | Run immediately |
| `GET` | `/api/schedules/:id/runs` | Get run history |
| `POST` | `/api/schedules/validate-cron` | Validate cron expression |

## Common Examples

### Daily Standup Reminder (Weekdays 9 AM)

```bash
curl -X POST "${API_BASE}/api/schedules" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Daily Standup",
    "scheduleType": "cron",
    "cronExpression": "0 9 * * 1-5",
    "timezone": "Asia/Jerusalem",
    "provider": "whatsapp",
    "target": "120363406740668957@g.us",
    "messageTemplate": "🔔 **Daily Standup**\n\n📅 {{date}} ({{day}})\n\nTime for our daily sync!",
    "enabled": true
  }'
```

### Friday Weekly Summary (Friday 5 PM)

```bash
curl -X POST "${API_BASE}/api/schedules" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekly Summary",
    "scheduleType": "cron",
    "cronExpression": "0 17 * * 5",
    "timezone": "Asia/Jerusalem",
    "provider": "whatsapp",
    "target": "120363406740668957@g.us",
    "messageTemplate": "📊 **Weekly Summary**\n\nHappy Friday! {{date}}\n\n✅ Review sprint progress\n✅ Update time tracking\n\nHave a great weekend! 🎉",
    "enabled": true
  }'
```

### One-Time Meeting Reminder

```bash
curl -X POST "${API_BASE}/api/schedules" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Project Kickoff Reminder",
    "scheduleType": "once",
    "runAt": "2026-01-15T08:45:00.000Z",
    "provider": "whatsapp",
    "target": "120363406740668957@g.us",
    "messageTemplate": "⚡ Project Kickoff in 15 minutes!\n\n📅 {{date}} at {{time}}",
    "enabled": true
  }'
```

## Manage Existing Jobs

```bash
# List all jobs
curl "${API_BASE}/api/schedules"

# Disable a job
curl -X POST "${API_BASE}/api/schedules/1/toggle" \
  -H "Content-Type: application/json" \
  -d '{"enabled": false}'

# Run job now (test)
curl -X POST "${API_BASE}/api/schedules/1/run"

# Delete a job
curl -X DELETE "${API_BASE}/api/schedules/1"
```

## Timezones

Supported values: `UTC`, `Asia/Jerusalem` (default), `America/New_York`, `America/Los_Angeles`, `Europe/London`, `Europe/Paris`, `Asia/Tokyo`, `Australia/Sydney`

## Error Handling

Jobs that fail are logged with errors in the run history. Check status via:

```bash
curl "${API_BASE}/api/schedules/1/runs?limit=10"
```
