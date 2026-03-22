---
name: calendar-core
description: Background technical reference for Apple Calendar data on macOS. Auto-loaded when any calendar-* skill executes. Contains DB path, CoreData epoch conversion, schema, canonical query, and filtering rules.
user-invocable: false
allowed-tools: Bash
metadata:
  openclaw:
    requires:
      bins: [sqlite3, python3]
---

# Apple Calendar — Local Data Reference

## Database Location

```
$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb
```

WAL mode — always accompanied by `.sqlitedb-shm` and `.sqlitedb-wal`. Reads work fine against the live database without locking.

```bash
DB="$HOME/Library/Group Containers/group.com.apple.calendar/Calendar.sqlitedb"
sqlite3 "$DB" "SELECT ..."
```

## Critical: CoreData Epoch (NOT Unix Epoch)

All timestamps are seconds since **January 1, 2001**, not 1970. Convert in SQLite:

```sql
datetime(field + 978307200, 'unixepoch', 'localtime')
```

Convert current time to CoreData timestamp in bash:
```bash
NOW_CD=$(( $(date +%s) - 978307200 ))
FUTURE_CD=$(( $(date +%s) + N * 86400 - 978307200 ))
```

## Critical: OccurrenceCache for Recurring Events

**Never query `CalendarItem.start_date` directly for date-range queries.** It only holds the original first occurrence. Future instances of recurring events only exist in `OccurrenceCache`.

Always use `OccurrenceCache` as the entry point for any time-windowed query.

`occurrence_start_date` is NULL for some recurring events — use `COALESCE(occurrence_start_date, occurrence_date)` for start time.

## SQLite Schema

### Key Tables

| Table | Key Columns |
|---|---|
| CalendarItem | ROWID, summary, start_date, end_date, start_tz, end_tz, all_day, description, url, conference_url, location_id, has_attendees, has_recurrences, status, invitation_status, hidden, organizer_id, self_attendee_id, calendar_id |
| OccurrenceCache | event_id (→CalendarItem.ROWID), occurrence_date, occurrence_start_date, occurrence_end_date |
| Calendar | ROWID, title, color, type, store_id |
| Store | ROWID, name (email/account name), type, disabled |
| Location | ROWID, title, latitude, longitude, address |
| Participant | ROWID, owner_id (→CalendarItem.ROWID), email, entity_type, role, status |
| Recurrence | ROWID, owner_id, frequency, interval, specifier |

### CalendarItem.status Values
- `0` — none / tentative
- `1` — confirmed
- `2` — cancelled (exclude these)

### CalendarItem.invitation_status Values
- `0` — none (own events)
- `3` — pending invite (not yet accepted)

### Store.type Values
- `0` — local
- `1` — local
- `5` — "Found in Mail" — **always exclude** (auto-created duplicates from email invites)

### Participant.entity_type Values
- `7` — attendee
- `8` — organizer

### Participant.status Values
- `0` — needs-action
- `1` — accepted
- `2` — declined
- `3` — tentative

### Participant.role Values
- `0` — non-participant / unknown
- `1` — required
- `2` — optional

### Recurrence.frequency Values
- `1` — daily
- `2` — weekly
- `3` — monthly
- `4` — yearly

## Standard Exclusion Filters

Always apply:
```sql
WHERE ci.hidden = 0          -- exclude hidden events
  AND ci.status != 2         -- exclude cancelled events
  AND s.type != 5            -- exclude "Found in Mail" duplicates
  AND s.disabled = 0         -- active accounts only
```

## Canonical Query Template

```sql
SELECT
  ci.ROWID as id,
  ci.summary as title,
  COALESCE(
    datetime(oc.occurrence_start_date + 978307200, 'unixepoch', 'localtime'),
    datetime(oc.occurrence_date + 978307200, 'unixepoch', 'localtime')
  ) as start_local,
  datetime(oc.occurrence_end_date + 978307200, 'unixepoch', 'localtime') as end_local,
  ci.all_day,
  ci.start_tz as timezone,
  COALESCE(l.title, '') as location,
  ci.conference_url,
  ci.has_attendees,
  ci.has_recurrences,
  ci.status,
  ci.invitation_status,
  c.title as calendar_name,
  s.name as account_name
FROM OccurrenceCache oc
JOIN CalendarItem ci ON oc.event_id = ci.ROWID
LEFT JOIN Calendar c ON ci.calendar_id = c.ROWID
LEFT JOIN Store s ON c.store_id = s.ROWID
LEFT JOIN Location l ON ci.location_id = l.ROWID
WHERE oc.occurrence_date >= NOW_CD
  AND oc.occurrence_date <= FUTURE_CD
  AND ci.hidden = 0
  AND ci.status != 2
  AND s.type != 5
  AND s.disabled = 0
GROUP BY ci.ROWID, date(oc.occurrence_date + 978307200, 'unixepoch', 'localtime')
ORDER BY oc.occurrence_date;
```

`GROUP BY ci.ROWID, date(...)` deduplicates multi-day spanning events that appear once per day in `OccurrenceCache`.

## Fetching Attendees (On-Demand Per Event)

Only fetch attendees for specific events — never bulk join, it's slow:

```sql
SELECT email, entity_type, role, status
FROM Participant
WHERE owner_id = EVENT_ROWID
ORDER BY entity_type DESC, status;
```

Filter `s.disabled = 0` to get only active accounts. Discover your active accounts with:

```sql
SELECT s.name, s.type, COUNT(*) as calendars
FROM Store s
JOIN Calendar c ON c.store_id = s.ROWID
WHERE s.type != 5 AND s.disabled = 0
GROUP BY s.ROWID
ORDER BY s.name;
```
