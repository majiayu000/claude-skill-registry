---
name: calendar-recurring
description: List all recurring meetings and meeting series. Use when user asks about standing meetings, recurring events, weekly syncs, or wants to see their regular meeting cadence.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Calendar Recurring — Standing Meetings and Series

List all active recurring events, grouped by frequency.

## Arguments

`$ARGUMENTS` — optional filter:
- Empty → all recurring events
- `"weekly"` → only weekly recurring
- `"standup"` → search by name

## Steps

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
FILTER="$ARGUMENTS"

NOW_CD=$(( $(date +%s) - 978307200 ))

KEYWORD_FILTER=""
if [ -n "$FILTER" ] && ! echo "$FILTER" | grep -qiE '^(weekly|daily|monthly|yearly)$'; then
  KEYWORD_FILTER="AND ci.summary LIKE '%${FILTER}%'"
fi

FREQ_FILTER=""
case "$(echo $FILTER | tr '[:upper:]' '[:lower:]')" in
  daily)   FREQ_FILTER="AND r.frequency = 1" ;;
  weekly)  FREQ_FILTER="AND r.frequency = 2" ;;
  monthly) FREQ_FILTER="AND r.frequency = 3" ;;
  yearly)  FREQ_FILTER="AND r.frequency = 4" ;;
esac

sqlite3 -separator '|' "$DB" "
SELECT
  ci.summary as title,
  CASE r.frequency
    WHEN 1 THEN 'Daily'
    WHEN 2 THEN 'Weekly'
    WHEN 3 THEN 'Monthly'
    WHEN 4 THEN 'Yearly'
    ELSE 'Unknown'
  END as freq,
  r.interval as every_n,
  COALESCE(
    strftime('%H:%M', oc_next.occurrence_start_date + 978307200, 'unixepoch', 'localtime'),
    strftime('%H:%M', oc_next.occurrence_date + 978307200, 'unixepoch', 'localtime')
  ) as time_of_day,
  date(oc_next.occurrence_date + 978307200, 'unixepoch', 'localtime') as next_occurrence,
  COALESCE(l.title, '') as location,
  COALESCE(ci.conference_url, '') as conf_url,
  c.title as calendar,
  ci.has_attendees,
  ci.ROWID as id
FROM CalendarItem ci
JOIN Recurrence r ON r.owner_id = ci.ROWID
LEFT JOIN (
  SELECT event_id, MIN(occurrence_date) as occurrence_date, occurrence_start_date
  FROM OccurrenceCache
  WHERE occurrence_date >= $NOW_CD
  GROUP BY event_id
) oc_next ON oc_next.event_id = ci.ROWID
LEFT JOIN Calendar c ON ci.calendar_id = c.ROWID
LEFT JOIN Store s ON c.store_id = s.ROWID
LEFT JOIN Location l ON ci.location_id = l.ROWID
WHERE ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0
  AND oc_next.occurrence_date IS NOT NULL
  $FREQ_FILTER
  $KEYWORD_FILTER
ORDER BY r.frequency, r.interval, COALESCE(oc_next.occurrence_start_date, oc_next.occurrence_date);
"
```

## Output Format

Group by frequency:

**Daily (N)**
- [time] Title — Every N days — [location/video]

**Weekly (N)**
- [time] Title — Every week — [calendar]
- [time] Title — Every 2 weeks (biweekly)

**Monthly (N)**
- [time] Title — Monthly

Show `has_attendees` flag so user knows which are solo vs. group meetings.
Note next occurrence date for each.
