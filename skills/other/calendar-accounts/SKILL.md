---
name: calendar-accounts
description: List all synced calendar accounts and individual calendars with event counts. Use when user asks what calendars they have, what accounts are synced, or wants an overview of their calendar setup.
user-invocable: true
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3]
---

# Calendar Accounts — All Synced Calendars

List every synced account and their individual calendars with upcoming event counts.

## Steps

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"

echo "=== ALL CALENDARS BY ACCOUNT ==="
sqlite3 -separator '|' "$DB" "
SELECT
  s.name as account,
  CASE s.type
    WHEN 0 THEN 'Local'
    WHEN 1 THEN 'Local'
    WHEN 2 THEN 'CalDAV/Google'
    WHEN 3 THEN 'Exchange'
    WHEN 5 THEN 'Found in Mail'
    ELSE 'Other'
  END as account_type,
  s.disabled as is_disabled,
  c.title as calendar_name,
  c.ROWID as cal_id,
  COUNT(DISTINCT ci.ROWID) as total_events
FROM Store s
JOIN Calendar c ON c.store_id = s.ROWID
LEFT JOIN CalendarItem ci ON ci.calendar_id = c.ROWID
  AND ci.hidden = 0
  AND ci.status != 2
WHERE s.type != 5
GROUP BY c.ROWID
ORDER BY s.disabled, s.name, c.title;
"

echo ""
echo "=== UPCOMING EVENTS (next 30 days) PER CALENDAR ==="
NOW_CD=$(( $(date +%s) - 978307200 ))
FUTURE_CD=$(( $(date +%s) + 30 * 86400 - 978307200 ))
sqlite3 -separator '|' "$DB" "
SELECT
  c.title as calendar_name,
  s.name as account,
  COUNT(DISTINCT ci.ROWID) as upcoming_count
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
JOIN Calendar c ON ci.calendar_id = c.ROWID
JOIN Store s ON c.store_id = s.ROWID
WHERE oc.occurrence_date >= $NOW_CD
  AND oc.occurrence_date <= $FUTURE_CD
  AND ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0
GROUP BY c.ROWID
ORDER BY upcoming_count DESC;
"
```

## Output Format

**Active Accounts:**
Table grouped by account — show: Account (email), Type, Calendars, Total Events.

**Upcoming (next 30 days):**
Ranked list of calendars by upcoming event count.

Flag disabled accounts separately as "(disabled)".
Note any "Found in Mail" store exists but is excluded as auto-generated duplicates.
