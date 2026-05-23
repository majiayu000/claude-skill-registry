---
name: calendar-conflicts
description: Find overlapping calendar events (double-bookings). Use when user asks about scheduling conflicts, overlapping meetings, or double-booked time slots.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Calendar Conflicts — Find Overlapping Events

Detect time-overlapping events (double-bookings). All-day events are excluded since they don't block time slots.

## Arguments

`$ARGUMENTS` — time range (default: next 7 days):
- "today", "this week", "next 14 days"
- "2026-03-01" → specific date
- Empty → next 7 days

## Steps

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
ARGS="$ARGUMENTS"

DAYS=7
if echo "$ARGS" | grep -qiE '[0-9]+ day'; then DAYS=$(echo "$ARGS" | grep -oiE '[0-9]+'); fi
if echo "$ARGS" | grep -qi 'week'; then DAYS=7; fi
if echo "$ARGS" | grep -qi 'today'; then DAYS=1; fi

NOW_CD=$(( $(date +%s) - 978307200 ))
FUTURE_CD=$(( $(date +%s) + DAYS * 86400 - 978307200 ))

# Fetch all timed events in window, detect overlaps in Python
sqlite3 -separator '|' "$DB" "
SELECT
  ci.ROWID,
  ci.summary,
  date(COALESCE(oc.occurrence_start_date, oc.occurrence_date) + 978307200, 'unixepoch', 'localtime') as day,
  COALESCE(oc.occurrence_start_date, oc.occurrence_date) as start_cd,
  COALESCE(oc.occurrence_end_date, oc.occurrence_date + 3600) as end_cd,
  strftime('%H:%M', COALESCE(oc.occurrence_start_date, oc.occurrence_date) + 978307200, 'unixepoch', 'localtime') as start_time,
  strftime('%H:%M', COALESCE(oc.occurrence_end_date, oc.occurrence_date + 3600) + 978307200, 'unixepoch', 'localtime') as end_time,
  c.title as calendar
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Calendar c ON ci.calendar_id = c.ROWID
LEFT JOIN Store s ON c.store_id = s.ROWID
WHERE oc.occurrence_date >= $NOW_CD
  AND oc.occurrence_date <= $FUTURE_CD
  AND ci.hidden = 0
  AND ci.status != 2
  AND ci.all_day = 0
  AND s.type != 5
  AND s.disabled = 0
GROUP BY ci.ROWID, day
ORDER BY day, start_cd;
" | python3 -c "
import sys

events = []
for line in sys.stdin:
    parts = line.strip().split('|')
    if len(parts) >= 8:
        rowid, title, day, start_cd, end_cd, start_time, end_time, calendar = parts[:8]
        events.append({'id': rowid, 'title': title, 'day': day,
                       'start': int(start_cd), 'end': int(end_cd),
                       'start_time': start_time, 'end_time': end_time, 'cal': calendar})

conflicts = []
for i in range(len(events)):
    for j in range(i+1, len(events)):
        a, b = events[i], events[j]
        if a['day'] != b['day']:
            break
        # Overlap: a.start < b.end AND a.end > b.start
        if a['start'] < b['end'] and a['end'] > b['start']:
            conflicts.append((a, b))

if not conflicts:
    print('No conflicts found.')
else:
    print(f'{len(conflicts)} conflict(s) found:')
    for a, b in conflicts:
        print(f\"  {a['day']}: [{a['start_time']}-{a['end_time']}] {a['title']} ({a['cal']})\")
        print(f\"         overlaps [{b['start_time']}-{b['end_time']}] {b['title']} ({b['cal']})\")
        print()
"
```

## Output Format

List each conflict pair:
```
Monday March 3:
  [09:00–10:00] Weekly Sync (Work) overlaps
  [09:30–10:30] Sprint Planning (Work)
```

No conflicts: "No overlapping events in the next 7 days."
