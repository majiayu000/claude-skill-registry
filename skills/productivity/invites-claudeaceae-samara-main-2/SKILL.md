---
name: invites
description: View and manage calendar invitations - check pending invites, accept/decline meeting requests, create events
context: fork
allowed-tools:
  - Bash
  - Read
---

# Calendar Invitations & Events

Check pending calendar invitations, respond to meeting requests, and create new events.

## Quick Status

```bash
~/.claude-mind/system/bin/calendar-invites list --text
```

## Commands

### List Pending Invitations

```bash
# Human-readable format
~/.claude-mind/system/bin/calendar-invites list --text

# JSON format (default)
~/.claude-mind/system/bin/calendar-invites list --json

# Custom date range
~/.claude-mind/system/bin/calendar-invites list --days 7

# Specific calendar
~/.claude-mind/system/bin/calendar-invites list --calendar "Work"
```

### Show Event Details

```bash
~/.claude-mind/system/bin/calendar-invites show "EVENT_ID"
```

### Respond to Invitations

```bash
# Accept an invitation (via AppleScript)
~/.claude-mind/system/bin/calendar-invites accept "EVENT_ID"

# Decline an invitation
~/.claude-mind/system/bin/calendar-invites decline "EVENT_ID"

# Mark as tentative/maybe
~/.claude-mind/system/bin/calendar-invites maybe "EVENT_ID"

# Accept all pending invitations (via AppleScript)
~/.claude-mind/system/bin/calendar-invites accept-all

# Accept all via UI automation (more reliable)
~/.claude-mind/system/bin/calendar-invites accept-all-ui
```

### Sync/Refresh Calendars

```bash
# Force calendar sync with server
~/.claude-mind/system/bin/calendar-invites sync
```

### Create Events

```bash
# Basic event (1 hour duration)
~/.claude-mind/system/bin/calendar-invites create --title "Team Meeting" --start "2026-01-20T14:00"

# Event with duration
~/.claude-mind/system/bin/calendar-invites create --title "Lunch" --start "2026-01-20 12:00" --duration 90

# Event with specific end time
~/.claude-mind/system/bin/calendar-invites create --title "Workshop" --start "2026-01-20 09:00" --end "2026-01-20 12:00"

# All-day event
~/.claude-mind/system/bin/calendar-invites create --title "Vacation" --start "2026-01-25" --all-day

# Multi-day all-day event
~/.claude-mind/system/bin/calendar-invites create --title "Conference" --start "2026-01-25" --end "2026-01-27" --all-day

# Event with location and notes
~/.claude-mind/system/bin/calendar-invites create --title "Client Call" --start "2026-01-20 15:00" \
    --location "Zoom" --notes "Discuss Q1 planning" --calendar "Work"
```

**Create Options:**
- `--title` - Event title (required)
- `--start` - Start date/time (required). Formats: ISO8601, "2026-01-20 14:00", "2026-01-20"
- `--end` - End date/time (optional)
- `--duration` - Duration in minutes (default: 60)
- `--calendar` - Calendar name (default: system default)
- `--location` - Event location
- `--notes` - Event notes/description
- `--url` - Event URL
- `--all-day` - Create an all-day event

### List Available Calendars

```bash
~/.claude-mind/system/bin/calendar-invites calendars
```

### Open in Calendar.app

```bash
~/.claude-mind/system/bin/calendar-invites open "EVENT_ID"
```

## JSON Output Format

The `list --json` command returns:

```json
{
  "invitations": [
    {
      "event_id": "ABC123-DEF456",
      "title": "Weekly Sync",
      "start": "2026-01-20T09:00:00-05:00",
      "end": "2026-01-20T10:00:00-05:00",
      "calendar": "Work",
      "organizer": {
        "name": "Jane Smith",
        "email": "jane@example.com"
      },
      "my_status": "pending",
      "location": "Zoom",
      "attendees": [...]
    }
  ],
  "count": 1
}
```

## Workflow

1. **Check invitations**: Run `list --text` to see what's pending
2. **Review if needed**: Use `show` for full details on specific events
3. **Respond**: Use `accept`, `decline`, or `maybe`
4. **Bulk accept**: Use `accept-all` for routine meetings

## Limitations

- **EventKit is read-only for responses**: Apple's EventKit API does not allow setting `participantStatus`
- **AppleScript limitations**: Direct property setting sometimes doesn't trigger server-side updates
- **UI automation is most reliable**: The `accept-all-ui` command clicks actual buttons in Calendar.app
- **Sync delays**: Calendar providers (Exchange, Google, iCloud) may have sync delays
- **Recurring events**: Response may only affect the next occurrence

## Response Methods (Fallback Chain)

1. **CalDAV** (primary) - Proper iTIP protocol, notifies organizers, server-side
2. **AppleScript** (fallback) - Local property change, may not sync
3. **UI automation** (`accept-all-ui`) - Clicks buttons in Calendar.app
4. **Manual** - Calendar.app opens for you to respond

### Direct CalDAV Commands

```bash
# List pending invitations via CalDAV inbox
~/.claude-mind/system/bin/calendar-caldav inbox

# Accept via CalDAV (proper protocol)
~/.claude-mind/system/bin/calendar-caldav accept "EVENT_UID"

# Accept all pending via CalDAV
~/.claude-mind/system/bin/calendar-caldav accept-all

# Decline via CalDAV
~/.claude-mind/system/bin/calendar-caldav decline "EVENT_UID"
```

## Troubleshooting

**If authorization fails:**
1. Check System Settings > Privacy & Security > Calendars
2. Ensure Terminal has calendar access

**If invitations don't appear:**
1. Run `calendar-invites sync` to force refresh
2. Check that calendar is syncing in Calendar.app preferences

**If responses don't work:**
1. Check CalDAV credentials: `~/.claude-mind/system/bin/calendar-caldav test`
2. Try `accept-all-ui` instead of `accept-all` (uses UI automation)
3. The script falls back to opening Calendar.app

**CalDAV setup:**
- Credentials stored in `~/.claude-mind/config/caldav-credentials.json`
- Requires app-specific password from appleid.apple.com
