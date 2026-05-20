---
name: nextcloud-calendar
description: |
  Create, list, and query calendar events in Nextcloud via CalDAV. Use when:
  (1) User asks to create a calendar event, (2) User asks what's on their calendar,
  (3) User says "add to calendar" or "schedule", (4) User asks about upcoming events.
  Always use Nextcloud calendar unless user specifies otherwise.
author: Claude Code
version: 1.0.0
date: 2025-01-25
---

# Nextcloud Calendar Management

## Problem
Need to create, query, or manage calendar events in the user's Nextcloud calendar.

## Context / Trigger Conditions
- User asks to create/add a calendar event
- User asks "what's on my calendar?" or similar
- User mentions scheduling something
- User says "remind me" with a date (create calendar event)
- Default calendar is always Nextcloud unless otherwise specified

## Prerequisites
- Python 3 with `caldav` and `icalendar` packages available (installed via PYTHONPATH or system packages)
- Environment variables `NEXTCLOUD_USER` and `NEXTCLOUD_APP_PASSWORD` must be set

## Solution

### Script Location
```
.claude/calendar-query.py
```

### Execution Pattern (CRITICAL)
Run the script directly with python3 (env vars are set in the environment):

```bash
python3 .claude/calendar-query.py [command] [options]
```

### Available Commands

#### List Calendars
```bash
python .claude/calendar-query.py list
```

#### Query Events
```bash
# Today's events
python .claude/calendar-query.py today

# Tomorrow's events
python .claude/calendar-query.py tomorrow

# This week
python .claude/calendar-query.py week

# This month
python .claude/calendar-query.py month

# Custom date range
python .claude/calendar-query.py events --days 14
python .claude/calendar-query.py events --date 2026-04-10

# From specific calendar
python .claude/calendar-query.py today --calendar "Work"
```

#### Create Events
```bash
# All-day event (single day)
python .claude/calendar-query.py create --title "Doctor appointment" --start "2026-03-15" --all-day

# All-day event (multi-day) - end date is EXCLUSIVE
# For April 10-13, use end date April 14
python .claude/calendar-query.py create --title "Vacation" --start "2026-04-10" --end "2026-04-14" --all-day

# Timed event
python .claude/calendar-query.py create --title "Meeting" --start "2026-03-15 14:00" --end "2026-03-15 15:00"

# With location and description
python .claude/calendar-query.py create --title "Lunch" --start "tomorrow 12:00" --location "Cafe" --description "Team lunch"

# Relative dates work
python .claude/calendar-query.py create --title "Call" --start "today 16:00"
python .claude/calendar-query.py create --title "Review" --start "tomorrow 10:00"
```

### Output Formats
```bash
# JSON output (for parsing)
python .claude/calendar-query.py today --json

# Text output (default, human-readable)
python .claude/calendar-query.py week
```

## Complete Example

To create an event "Team offsite" from March 20-22, 2026:

```bash
python3 .claude/calendar-query.py create --title "Team offsite" --start "2026-03-20" --end "2026-03-23" --all-day
```

## Important Notes

1. **End dates are exclusive** for all-day events (CalDAV standard). To create an event spanning April 10-13, set end to April 14.

2. **No delete/update commands** - The script currently only supports create and query. To modify events, user must do it manually in Nextcloud.

4. **Default calendar** is "Personal" - use `--calendar` flag for others.

## Verification
- For queries: Output shows formatted event list
- For creates: Output shows "Event created: [title]" with calendar name and start date
- Exit code 0 = success, 1 = error (check output for details)

## Common Errors

| Error | Cause | Fix |
|-------|-------|-----|
| `NEXTCLOUD_USER and NEXTCLOUD_APP_PASSWORD must be set` | Env vars not set | Ensure `NEXTCLOUD_USER` and `NEXTCLOUD_APP_PASSWORD` are in the environment |
| `Required packages not installed` | caldav/icalendar missing | Ensure PYTHONPATH includes the installed packages |
| `Calendar 'X' not found` | Wrong calendar name | Run `list` command to see available calendars |
