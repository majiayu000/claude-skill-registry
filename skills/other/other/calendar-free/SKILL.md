---
name: calendar-free
description: Find free time slots in a day or week. Use when user asks when they're free, wants to schedule something, or needs to find an open time window.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Calendar Free — Find Open Time Slots

Find available time slots in a day, considering existing events. Working hours assumed 08:00–18:00 local time unless specified.

## Arguments

`$ARGUMENTS`:
- Empty → today
- `"tomorrow"`, `"Monday"`, `"2026-03-05"` → specific date
- `"this week"` → all days this week
- `"1 hour"` → minimum slot duration (default: 30 min)
- `"afternoon"` → restrict to 12:00–18:00

## Steps

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
ARGS="$ARGUMENTS"

# Determine target date(s)
TARGET_DATE=$(python3 -c "
import sys, re
from datetime import date, timedelta
args = '''$ARGS'''.lower()
today = date.today()
if 'tomorrow' in args:
    d = today + timedelta(days=1)
elif 'monday' in args: d = today + timedelta(days=(0-today.weekday())%7)
elif 'tuesday' in args: d = today + timedelta(days=(1-today.weekday())%7)
elif 'wednesday' in args: d = today + timedelta(days=(2-today.weekday())%7)
elif 'thursday' in args: d = today + timedelta(days=(3-today.weekday())%7)
elif 'friday' in args: d = today + timedelta(days=(4-today.weekday())%7)
else:
    m = re.search(r'\d{4}-\d{2}-\d{2}', args)
    d = date.fromisoformat(m.group()) if m else today
print(d.isoformat())
")

# Working hours window (CoreData timestamps)
DAY_START=$(python3 -c "
from datetime import datetime
d = datetime.strptime('${TARGET_DATE} 08:00:00', '%Y-%m-%d %H:%M:%S')
print(int(d.timestamp()) - 978307200)
")
DAY_END=$(python3 -c "
from datetime import datetime
d = datetime.strptime('${TARGET_DATE} 18:00:00', '%Y-%m-%d %H:%M:%S')
print(int(d.timestamp()) - 978307200)
")

# Fetch all timed events on that day
sqlite3 -separator '|' "$DB" "
SELECT
  ci.summary,
  COALESCE(oc.occurrence_start_date, oc.occurrence_date) as start_cd,
  COALESCE(oc.occurrence_end_date, oc.occurrence_date + 3600) as end_cd,
  strftime('%H:%M', COALESCE(oc.occurrence_start_date, oc.occurrence_date) + 978307200, 'unixepoch', 'localtime') as start_t,
  strftime('%H:%M', COALESCE(oc.occurrence_end_date, oc.occurrence_date + 3600) + 978307200, 'unixepoch', 'localtime') as end_t
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Store s ON (SELECT store_id FROM Calendar WHERE ROWID = ci.calendar_id)
WHERE oc.occurrence_date >= $DAY_START
  AND oc.occurrence_date <= $DAY_END
  AND ci.hidden = 0
  AND ci.status != 2
  AND ci.all_day = 0
  AND s.type != 5
  AND s.disabled = 0
GROUP BY ci.ROWID
ORDER BY start_cd;
" | python3 -c "
import sys
from datetime import datetime

epoch_2001 = 978307200
day_start_unix = $DAY_START + epoch_2001
day_end_unix   = $DAY_END   + epoch_2001

def fmt(unix_ts):
    return datetime.fromtimestamp(unix_ts).strftime('%H:%M')

events = []
for line in sys.stdin:
    parts = line.strip().split('|')
    if len(parts) >= 5:
        title, start_cd, end_cd, start_t, end_t = parts[:5]
        events.append((int(start_cd) + epoch_2001, int(end_cd) + epoch_2001, title))

events.sort()

# Find free slots
cursor = day_start_unix
free_slots = []
for start, end, title in events:
    if start > cursor + 1800:  # at least 30 min gap
        free_slots.append((cursor, start, start - cursor))
    if end > cursor:
        cursor = end

if cursor < day_end_unix - 1800:
    free_slots.append((cursor, day_end_unix, day_end_unix - cursor))

print(f'Schedule for $TARGET_DATE:')
print()
if events:
    print('Busy:')
    for start, end, title in events:
        print(f'  {fmt(start)}-{fmt(end)}  {title}')
    print()

if free_slots:
    print('Free slots:')
    for start, end, dur in free_slots:
        h, m = divmod(int(dur/60), 60)
        label = f'{h}h {m}m' if h else f'{m}m'
        print(f'  {fmt(start)}-{fmt(end)}  ({label})')
else:
    print('No free slots during working hours.')
"
```

## Output Format

```
Schedule for Monday March 3:

Busy:
  09:00-10:00  Weekly Sync
  14:00-15:00  1:1 with Alex

Free slots:
  08:00-09:00  (1h)
  10:00-14:00  (4h)
  15:00-18:00  (3h)
```

Note the longest free block explicitly. If asking for a specific duration (e.g. "1 hour free"), highlight only slots that fit.
