---
name: managing-calendar
description: |
  Manage Google Calendar events via MCP server.
  Use when scheduling meetings, checking availability, listing events,
  or processing meeting requests from emails.
  NOT when managing Outlook calendars (different API).
---

# Google Calendar MCP Skill

FastMCP server for Google Calendar management.

## Quick Start

```bash
# Start MCP server
python src/mcp_servers/google_calendar_server.py
```

## MCP Tools

1. `list_events(calendar_id, max_results, time_min, time_max)` - List upcoming events
2. `create_event(summary, start_time, end_time, description, location, attendees)` - Create new event
3. `update_event(event_id, summary, description, location)` - Modify existing event
4. `delete_event(event_id)` - Cancel event

## Production Gotchas

### Timezone Handling
All times are stored in UTC by default. Client must convert:

```python
# Server always uses UTC
'start': {
    'dateTime': start_time,
    'timeZone': 'UTC',  # Always UTC internally
}

# Convert for user display
from datetime import timezone
local_time = utc_time.astimezone(timezone.utc)
```

### ISO Format Required
Time parameters MUST be ISO 8601 format:

```python
# ✓ CORRECT
create_event(start_time="2026-01-30T10:00:00")

# ✗ WRONG - Natural language
create_event(start_time="tomorrow 10am")

# ✗ WRONG - Missing T separator
create_event(start_time="2026-01-30 10:00:00")
```

### Calendar ID Conventions
- `'primary'` - User's main calendar (default)
- Email address - Shared calendar access
- Calendar ID from Google - For secondary calendars

### Attendees Are Optional But Important
Omitting attendees creates a private event:

```python
# Private event (no notifications)
create_event(summary="Focus time", start_time=..., end_time=...)

# Meeting with notifications
create_event(
    summary="Team sync",
    start_time=...,
    end_time=...,
    attendees=["alice@example.com", "bob@example.com"]
)
```

### Separate Token File
Calendar uses different OAuth token than Gmail:
- `token_calendar.json` - Calendar access
- `token.json` / `token_email.json` - Gmail access

### Event ID Required for Updates
You must first retrieve the event ID before updating:

```python
# ✗ FAILS - No ID
update_event(summary="New title")

# ✓ WORKS - Get ID from list_events first
events = list_events()
event_id = events[0]['id']
update_event(event_id=event_id, summary="New title")
```

## Configuration

Required in `config/`:
- `credentials.json` - Google OAuth credentials
- `token_calendar.json` - Calendar OAuth token

OAuth Scopes:
```python
SCOPES = ['https://www.googleapis.com/auth/calendar']
```

## Setup

### 1. Enable Google Calendar API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Enable "Google Calendar API"
3. Create OAuth credentials (Desktop app)
4. Download as `config/credentials.json`

### 2. First Run

```bash
python src/mcp_servers/google_calendar_server.py
```

This opens a browser for OAuth consent. Token saves to `token_calendar.json`.

## Rate Limits

Google Calendar API limits:
- 1,000,000 queries per day
- 500 queries per 100 seconds per user

Not typically a concern for personal use.

## Audit Logging

All operations logged via `utils/audit_logger.py`:
- Domain: `AuditDomain.PERSONAL`
- Actions: `calendar.list_events`, `calendar.create_event`, etc.

## Verification

Run: `python scripts/verify.py`

## Related Skills

- `watching-gmail` - Detect meeting requests in emails
- `digital-fte-orchestrator` - Process calendar-related tasks
