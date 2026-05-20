---
name: calendar-upcoming
description: Show upcoming events for the next N days grouped by date. Use when user asks about their schedule this week, next few days, what's coming up, or events in a specific date range.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Calendar Upcoming — Events for Next N Days

Show upcoming events grouped by day. Default: next 7 days.

## Arguments

`$ARGUMENTS` — time range expression:
- "3 days", "2 weeks", "next 14 days" → parse N days
- "this week" → until Sunday
- "next week" → Monday to Sunday
- "until Friday" → until that weekday
- Default (empty): 7 days

## Steps

### 1. Parse time range from `$ARGUMENTS`

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
ARGS="$ARGUMENTS"

# Determine day count from args (default 7)
DAYS=7
if echo "$ARGS" | grep -qiE '[0-9]+ day'; then
  DAYS=$(echo "$ARGS" | grep -oiE '[0-9]+')
elif echo "$ARGS" | grep -qi 'week'; then
  DAYS=14
fi

NOW_CD=$(( $(date +%s) - 978307200 ))
FUTURE_CD=$(( $(date +%s) + DAYS * 86400 - 978307200 ))

sqlite3 -separator '|' "$DB" "
SELECT
  date(oc.occurrence_date + 978307200, 'unixepoch', 'localtime') as day,
  ci.all_day,
  COALESCE(
    strftime('%H:%M', oc.occurrence_start_date + 978307200, 'unixepoch', 'localtime'),
    strftime('%H:%M', oc.occurrence_date + 978307200, 'unixepoch', 'localtime')
  ) as start_time,
  COALESCE(
    strftime('%H:%M', oc.occurrence_end_date + 978307200, 'unixepoch', 'localtime'),
    ''
  ) as end_time,
  ci.summary as title,
  COALESCE(l.title, '') as location,
  COALESCE(ci.conference_url, '') as conf_url,
  c.title as calendar,
  ci.invitation_status,
  ci.ROWID as id
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Calendar c ON ci.calendar_id = c.ROWID
LEFT JOIN Store s ON c.store_id = s.ROWID
LEFT JOIN Location l ON ci.location_id = l.ROWID
WHERE oc.occurrence_date >= $NOW_CD
  AND oc.occurrence_date <= $FUTURE_CD
  AND ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0
GROUP BY ci.ROWID, day
ORDER BY oc.occurrence_date, ci.all_day DESC, COALESCE(oc.occurrence_start_date, oc.occurrence_date);
"
```

## Output Format

Group events by date with a day header for each:

```
Monday, March 3
  All-day: Public Holiday (Holidays)
  09:00–10:00  Weekly Sync         [Google Meet]  Work
  14:00–15:00  1:1 with Alex                      Work

Tuesday, March 4
  10:00–11:00  Sprint Planning     [Zoom]         Work
```

Show weekday name + date in headers. Flag pending invites. Note video links.
If a day has no events, skip it (don't show empty days).
Total event count at end.
