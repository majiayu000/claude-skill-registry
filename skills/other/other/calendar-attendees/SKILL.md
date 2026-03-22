---
name: calendar-attendees
description: Find meetings with a specific person, or list attendees of a specific event. Use when user asks who is in a meeting, whether someone is invited, or what meetings they share with a person.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Calendar Attendees — People and Meeting Roster

Two modes:
1. **Person → Meetings**: Find all events where a specific person is an attendee
2. **Event → Attendees**: List all attendees of a specific event

## Arguments

`$ARGUMENTS`:
- Person name or email: `"alice"`, `"alice@example.com"`, `"bob"`
- Event ROWID: `"1234"`
- Combined: `"standup attendees"`, `"who is in the weekly sync"`

## Steps

### Mode 1: Find meetings with a person

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
PERSON="$ARGUMENTS"

NOW_CD=$(( $(date +%s) - 978307200 ))
FUTURE_CD=$(( $(date +%s) + 30 * 86400 - 978307200 ))

echo "=== UPCOMING MEETINGS WITH: $PERSON ==="
sqlite3 -separator '|' "$DB" "
SELECT
  date(COALESCE(oc.occurrence_start_date, oc.occurrence_date) + 978307200, 'unixepoch', 'localtime') as event_date,
  COALESCE(
    strftime('%H:%M', oc.occurrence_start_date + 978307200, 'unixepoch', 'localtime'),
    'all-day'
  ) as start_time,
  ci.summary as title,
  p.email as attendee_email,
  CASE p.status
    WHEN 0 THEN 'pending'
    WHEN 1 THEN 'accepted'
    WHEN 2 THEN 'declined'
    WHEN 3 THEN 'tentative'
  END as their_status,
  c.title as calendar,
  ci.ROWID as id
FROM Participant p
JOIN CalendarItem ci ON p.owner_id = ci.ROWID
JOIN OccurrenceCache oc ON oc.event_id = ci.ROWID
LEFT JOIN Calendar c ON ci.calendar_id = c.ROWID
LEFT JOIN Store s ON c.store_id = s.ROWID
WHERE (p.email LIKE '%${PERSON}%')
  AND p.entity_type = 7
  AND oc.occurrence_date >= $NOW_CD
  AND oc.occurrence_date <= $FUTURE_CD
  AND ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0
GROUP BY ci.ROWID, event_date
ORDER BY oc.occurrence_date;
"
```

### Mode 2: List attendees for a specific event

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
EVENT_ID="$ARGUMENTS"

sqlite3 -separator '|' "$DB" "
SELECT
  CASE entity_type WHEN 8 THEN 'organizer' ELSE 'attendee' END as type,
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

## Output Format

**Person search:** Group matches by meeting. Show event title, date/time, and that person's RSVP status.
Show total count of shared upcoming meetings.

**Event attendees:** Group as Organizer, Accepted, Declined, Tentative, Pending.
Show counts per group (e.g. "8 accepted, 2 declined, 3 pending").
