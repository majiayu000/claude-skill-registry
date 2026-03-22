---
name: calendar-search
description: Search calendar events by title, location, or description keyword. Use when user asks to find a specific meeting, event, or anything that happened or is coming up.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Calendar Search — Find Events by Keyword

Search across all calendar events by title, location, or description.

## Arguments

`$ARGUMENTS` — search query with optional modifiers:
- `"standup"` → search title/location/description
- `"standup last week"` → add time filter
- `"calendar:Work standup"` → filter by calendar name
- `"from:2025-01-01 to:2025-03-01 sprint"` → date range

## Steps

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
QUERY="$ARGUMENTS"

# Extract keyword (strip known modifiers for SQL LIKE)
KEYWORD=$(echo "$QUERY" | sed 's/last [0-9]* \(day\|week\|month\)s\?//gi' | sed 's/calendar:[^ ]*//gi' | xargs)

# Default: search all time (no date filter) — show most recent 50 matches
sqlite3 -separator '|' "$DB" "
SELECT
  date(COALESCE(oc.occurrence_start_date, oc.occurrence_date) + 978307200, 'unixepoch', 'localtime') as event_date,
  COALESCE(
    strftime('%H:%M', oc.occurrence_start_date + 978307200, 'unixepoch', 'localtime'),
    'all-day'
  ) as start_time,
  ci.summary as title,
  COALESCE(l.title, '') as location,
  c.title as calendar,
  ci.ROWID as id
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Calendar c ON ci.calendar_id = c.ROWID
LEFT JOIN Store s ON c.store_id = s.ROWID
LEFT JOIN Location l ON ci.location_id = l.ROWID
WHERE ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0
  AND (
    ci.summary LIKE '%${KEYWORD}%'
    OR l.title LIKE '%${KEYWORD}%'
    OR ci.description LIKE '%${KEYWORD}%'
  )
GROUP BY ci.ROWID, event_date
ORDER BY COALESCE(oc.occurrence_start_date, oc.occurrence_date) DESC
LIMIT 50;
"
```

## Output Format

Table: Date | Time | Event | Location | Calendar

Show total match count. If over 50 results, note the limit.
If no results: suggest broadening the search or checking spelling.
