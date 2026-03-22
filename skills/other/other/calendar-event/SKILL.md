---
name: calendar-event
description: Get full details of a specific event including attendees, description, video link, location, and recurrence. Use when user asks about a specific meeting or event details.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Calendar Event — Full Event Details

Fetch complete details for a specific event: attendees, description, video link, location, recurrence.

## Arguments

`$ARGUMENTS`:
- Event ROWID: `"1234"`
- Title search: `"weekly sync"`, `"standup"`, `"1:1 with Alex"`

## Steps

### 1. Find the event

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
ARGS="$ARGUMENTS"

# Try as ROWID first, then fall back to title search
if echo "$ARGS" | grep -qE '^[0-9]+$'; then
  WHERE="ci.ROWID = $ARGS"
else
  WHERE="ci.summary LIKE '%${ARGS}%'"
fi

sqlite3 -separator '|' "$DB" "
SELECT
  ci.ROWID,
  ci.summary,
  COALESCE(
    datetime(oc.occurrence_start_date + 978307200, 'unixepoch', 'localtime'),
    datetime(oc.occurrence_date + 978307200, 'unixepoch', 'localtime')
  ) as start_local,
  datetime(oc.occurrence_end_date + 978307200, 'unixepoch', 'localtime') as end_local,
  ci.all_day,
  ci.start_tz,
  COALESCE(l.title, '') as location,
  COALESCE(l.address, '') as address,
  COALESCE(ci.conference_url, '') as conf_url,
  COALESCE(ci.url, '') as url,
  ci.has_attendees,
  ci.has_recurrences,
  ci.status,
  ci.invitation_status,
  c.title as calendar,
  s.name as account,
  ci.description
FROM CalendarItem ci
LEFT JOIN OccurrenceCache oc ON oc.event_id = ci.ROWID
LEFT JOIN Calendar c ON ci.calendar_id = c.ROWID
LEFT JOIN Store s ON c.store_id = s.ROWID
LEFT JOIN Location l ON ci.location_id = l.ROWID
WHERE $WHERE
  AND ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
GROUP BY ci.ROWID
ORDER BY COALESCE(oc.occurrence_date, ci.start_date) DESC
LIMIT 1;
"
```

### 2. Fetch attendees (if has_attendees = 1)

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
EVENT_ID="$EVENT_ROWID"

sqlite3 -separator '|' "$DB" "
SELECT
  CASE entity_type WHEN 8 THEN 'organizer' ELSE 'attendee' END as role,
  email,
  CASE status
    WHEN 0 THEN 'needs-action'
    WHEN 1 THEN 'accepted'
    WHEN 2 THEN 'declined'
    WHEN 3 THEN 'tentative'
  END as status,
  CASE role WHEN 2 THEN 'optional' ELSE 'required' END as attendance
FROM Participant
WHERE owner_id = $EVENT_ID
ORDER BY entity_type DESC, status;
"
```

### 3. Fetch recurrence rule (if has_recurrences = 1)

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
EVENT_ID="$EVENT_ROWID"

sqlite3 -separator '|' "$DB" "
SELECT
  CASE frequency
    WHEN 1 THEN 'Daily'
    WHEN 2 THEN 'Weekly'
    WHEN 3 THEN 'Monthly'
    WHEN 4 THEN 'Yearly'
  END as freq,
  interval,
  specifier
FROM Recurrence
WHERE owner_id = $EVENT_ID
LIMIT 1;
"
```

## Output Format

Present as a structured event card:

```
📅 [Title]
   Date:     Monday, March 3, 2026
   Time:     09:00 – 10:00 (WIB)
   Location: [room/address if set]
   Video:    [Meet/Zoom URL if set]
   Calendar: [calendar] · [account]
   Recurrence: Every week

Attendees (N):
  Organizer: name@email.com
  ✓ accepted@email.com
  ? tentative@email.com
  ✗ declined@email.com
  ○ pending@email.com

Description:
  [first 500 chars of description]
```

Extract Google Meet links from description if `conference_url` is empty (pattern: `meet.google.com/...`).
If search returns multiple events, list them with ROWIDs and ask which one.
