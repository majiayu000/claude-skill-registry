---
name: calendar-today
description: Show all of today's events in time order. Use when user asks what's on their schedule today, what meetings they have, or what's happening today.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Calendar Today — Today's Schedule

Show all events scheduled for today, all-day events first, then timed events in chronological order.

## Steps

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"

# CoreData epoch: seconds since 2001-01-01
# Today's window: midnight to midnight local time
TODAY_START=$(python3 -c "
from datetime import datetime, date
import calendar, time
d = date.today()
epoch_2001 = 978307200
start = int(datetime(d.year, d.month, d.day, 0, 0, 0).timestamp()) - epoch_2001
end   = int(datetime(d.year, d.month, d.day, 23, 59, 59).timestamp()) - epoch_2001
print(start, end)
")
NOW_CD=$(echo $TODAY_START | cut -d' ' -f1)
END_CD=$(echo $TODAY_START | cut -d' ' -f2)

sqlite3 "$DB" "
SELECT
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
  AND oc.occurrence_date <= $END_CD
  AND ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0
GROUP BY ci.ROWID
ORDER BY ci.all_day DESC, oc.occurrence_date, COALESCE(oc.occurrence_start_date, oc.occurrence_date);
"
```

## Output Format

Present as two sections:

**All-Day**
List all-day events by name and calendar (no time needed).

**Timed Events**
Table with columns: Time (HH:MM–HH:MM), Event, Location, Calendar.
Flag pending invites (`invitation_status = 3`) with "(pending)" note.
If `conf_url` is set, note "📍 Meet/Zoom link" or just say "has video link."

Show total event count at the bottom.
If no events: "Nothing on the calendar today."
