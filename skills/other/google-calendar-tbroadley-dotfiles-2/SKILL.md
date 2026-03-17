---
name: google-calendar
description: View and manage Google Calendar events. Check today's schedule, upcoming meetings, and calendar availability.
---

# Google Calendar Integration

This skill provides access to Google Calendar via the Google Calendar API.

## Setup Required

Uses OAuth with persistent refresh token (same setup for Calendar, Gmail, Drive).

**One-time setup:**
```bash
google-oauth-setup <path-to-client-secret.json>
```

See `claude/skills/SETUP.md` for detailed OAuth setup instructions.

**Get Access Token (auto-refreshes):**
```bash
ACCESS_TOKEN=$(google-oauth-token)
```

**Required header for all requests:**
```bash
-H "x-goog-user-project: ${GOOGLE_QUOTA_PROJECT}"
```

## When to Use

Use this skill when the user:
- Asks about their calendar or schedule
- Wants to see today's or upcoming meetings
- Asks "what's on my calendar?"
- Needs to check availability
- Mentions meetings or events

## API Endpoints

Base URL: `https://www.googleapis.com/calendar/v3`

### List Calendars

```bash
curl -s "https://www.googleapis.com/calendar/v3/users/me/calendarList" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {summary, id}'
```

### Get Events

**Today's Events:**
```bash
TODAY=$(date -u +"%Y-%m-%dT00:00:00Z")
TOMORROW=$(date -v+1d -u +"%Y-%m-%dT00:00:00Z")

curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "timeMin=${TODAY}" \
  --data-urlencode "timeMax=${TOMORROW}" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Next 7 Days:**
```bash
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
WEEK=$(date -v+7d -u +"%Y-%m-%dT%H:%M:%SZ")

curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "timeMin=${NOW}" \
  --data-urlencode "timeMax=${WEEK}" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  --data-urlencode "maxResults=20" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

**Specific Date Range:**
```bash
curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "timeMin=2024-01-15T00:00:00Z" \
  --data-urlencode "timeMax=2024-01-22T00:00:00Z" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Search Events

```bash
curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "q=standup" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  --data-urlencode "maxResults=10" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Get Single Event

```bash
curl -s "https://www.googleapis.com/calendar/v3/calendars/primary/events/{EVENT_ID}" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}"
```

### Free/Busy Query

```bash
curl -s -X POST "https://www.googleapis.com/calendar/v3/freeBusy" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "timeMin": "2024-01-15T00:00:00Z",
    "timeMax": "2024-01-16T00:00:00Z",
    "items": [{"id": "primary"}]
  }'
```

## Common Workflows

### What's on my calendar today?
```bash
ACCESS_TOKEN=$(google-oauth-token)

TODAY=$(date -u +"%Y-%m-%dT00:00:00Z")
TOMORROW=$(date -v+1d -u +"%Y-%m-%dT00:00:00Z")

curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "timeMin=${TODAY}" \
  --data-urlencode "timeMax=${TOMORROW}" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {
    summary,
    start: (.start.dateTime // .start.date),
    end: (.end.dateTime // .end.date),
    location
  }'
```

### What meetings do I have this week?
```bash
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
WEEK=$(date -v+7d -u +"%Y-%m-%dT%H:%M:%SZ")

curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "timeMin=${NOW}" \
  --data-urlencode "timeMax=${WEEK}" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {
    summary,
    start: (.start.dateTime // .start.date),
    attendees: [.attendees[]?.email] | join(", ")
  }'
```

### When is my next meeting?
```bash
NOW=$(date -u +"%Y-%m-%dT%H:%M:%SZ")

curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "timeMin=${NOW}" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  --data-urlencode "maxResults=1" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[0] | {summary, start: .start.dateTime}'
```

### Find a specific meeting
```bash
curl -s -G "https://www.googleapis.com/calendar/v3/calendars/primary/events" \
  --data-urlencode "q=1:1" \
  --data-urlencode "singleEvents=true" \
  --data-urlencode "orderBy=startTime" \
  --data-urlencode "maxResults=5" \
  -H "Authorization: Bearer ${ACCESS_TOKEN}" | jq '.items[] | {summary, start: .start.dateTime}'
```

## Event Properties

Key fields in event responses:
- **summary**: Event title
- **start.dateTime** / **start.date**: Start time (dateTime for timed events, date for all-day)
- **end.dateTime** / **end.date**: End time
- **location**: Meeting location or video link
- **description**: Event description
- **attendees**: Array of attendee objects with email, responseStatus
- **hangoutLink**: Google Meet link if present
- **htmlLink**: Link to view event in Google Calendar

## Parameters

| Parameter | Description |
|-----------|-------------|
| `timeMin` | Lower bound (exclusive) for event end time (RFC3339) |
| `timeMax` | Upper bound (exclusive) for event start time (RFC3339) |
| `singleEvents` | Expand recurring events into instances (set to `true`) |
| `orderBy` | `startTime` (requires singleEvents=true) or `updated` |
| `maxResults` | Max events to return (default 250) |
| `q` | Free text search terms |

## Notes

- Times must be in RFC3339 format (e.g., `2024-01-15T09:00:00Z` or with timezone offset)
- Use `singleEvents=true` to expand recurring events
- `primary` refers to the user's primary calendar; use calendar ID for others
- Access tokens expire after 1 hour; refresh as needed
- All-day events use `start.date` instead of `start.dateTime`
