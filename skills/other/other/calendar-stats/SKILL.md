---
name: calendar-stats
description: Show calendar statistics — meeting volume, hours in meetings, busiest days, top calendars, and meeting load by day of week. Use when user asks how many meetings they have, how busy they are, or wants a time audit.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Calendar Stats — Meeting Volume and Time Audit

Show meeting statistics for a time period.

## Arguments

`$ARGUMENTS` — time range (default: last 30 days):
- "last week", "this month", "last 90 days"
- "2026-01-01 to 2026-03-01" → date range
- Empty → last 30 days

## Steps

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
ARGS="$ARGUMENTS"

DAYS=30
if echo "$ARGS" | grep -qiE '[0-9]+ day'; then DAYS=$(echo "$ARGS" | grep -oiE '[0-9]+' | head -1); fi
if echo "$ARGS" | grep -qi 'week'; then DAYS=7; fi
if echo "$ARGS" | grep -qi '90'; then DAYS=90; fi

START_CD=$(( $(date +%s) - DAYS * 86400 - 978307200 ))
END_CD=$(( $(date +%s) - 978307200 ))

echo "=== OVERVIEW ==="
sqlite3 "$DB" "
SELECT
  COUNT(DISTINCT ci.ROWID) as total_events,
  SUM(CASE WHEN ci.all_day = 0 THEN
    MAX(0, MIN(COALESCE(oc.occurrence_end_date, oc.occurrence_date + 3600),
               COALESCE(oc.occurrence_start_date, oc.occurrence_date) + 86400)
        - COALESCE(oc.occurrence_start_date, oc.occurrence_date))
  ELSE 0 END) / 3600.0 as total_hours,
  COUNT(DISTINCT CASE WHEN ci.has_attendees = 1 THEN ci.ROWID END) as meetings_with_others,
  COUNT(DISTINCT CASE WHEN ci.all_day = 1 THEN ci.ROWID END) as all_day_events
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Store s ON (SELECT store_id FROM Calendar WHERE ROWID = ci.calendar_id)
WHERE oc.occurrence_date >= $START_CD
  AND oc.occurrence_date <= $END_CD
  AND ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0;
"

echo ""
echo "=== BY DAY OF WEEK ==="
sqlite3 -separator '|' "$DB" "
SELECT
  CASE strftime('%w', oc.occurrence_date + 978307200, 'unixepoch')
    WHEN '0' THEN 'Sunday'
    WHEN '1' THEN 'Monday'
    WHEN '2' THEN 'Tuesday'
    WHEN '3' THEN 'Wednesday'
    WHEN '4' THEN 'Thursday'
    WHEN '5' THEN 'Friday'
    WHEN '6' THEN 'Saturday'
  END as weekday,
  COUNT(DISTINCT ci.ROWID) as events,
  ROUND(SUM(CASE WHEN ci.all_day = 0 THEN
    MAX(0, COALESCE(oc.occurrence_end_date, oc.occurrence_date + 3600)
        - COALESCE(oc.occurrence_start_date, oc.occurrence_date))
  ELSE 0 END) / 3600.0, 1) as hours
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Store s ON (SELECT store_id FROM Calendar WHERE ROWID = ci.calendar_id)
WHERE oc.occurrence_date >= $START_CD AND oc.occurrence_date <= $END_CD
  AND ci.hidden = 0 AND ci.status != 2 AND s.type != 5 AND s.disabled = 0
GROUP BY strftime('%w', oc.occurrence_date + 978307200, 'unixepoch')
ORDER BY events DESC;
"

echo ""
echo "=== TOP CALENDARS ==="
sqlite3 -separator '|' "$DB" "
SELECT c.title, s.name, COUNT(DISTINCT ci.ROWID) as events
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
JOIN Calendar c ON ci.calendar_id = c.ROWID
JOIN Store s ON c.store_id = s.ROWID
WHERE oc.occurrence_date >= $START_CD AND oc.occurrence_date <= $END_CD
  AND ci.hidden = 0 AND ci.status != 2 AND s.type != 5 AND s.disabled = 0
GROUP BY c.ROWID ORDER BY events DESC LIMIT 10;
"

echo ""
echo "=== BUSIEST DAYS ==="
sqlite3 -separator '|' "$DB" "
SELECT
  date(oc.occurrence_date + 978307200, 'unixepoch', 'localtime') as day,
  COUNT(DISTINCT ci.ROWID) as events
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Store s ON (SELECT store_id FROM Calendar WHERE ROWID = ci.calendar_id)
WHERE oc.occurrence_date >= $START_CD AND oc.occurrence_date <= $END_CD
  AND ci.hidden = 0 AND ci.status != 2 AND s.type != 5 AND s.disabled = 0
GROUP BY day ORDER BY events DESC LIMIT 5;
"
```

## Output Format

**Summary:** Total events, total hours in meetings, meetings with others vs. solo, all-day events.

**By Day of Week:** Bar-style ranking — which days are busiest (events + hours).

**Top Calendars:** Which calendars have the most events.

**Busiest Days:** Top 5 days with most events.

Compute average meetings per day. Note if meeting load is high (>4 timed meetings/day on average = "heavy").
