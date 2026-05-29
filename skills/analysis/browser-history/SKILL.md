---
name: browser-history
description: Search local browser history. Use when user asks about visited pages, forgotten URLs, or time spent on sites.
---

# Browser History Search

Search the user's browser history to find visited pages, analyze browsing patterns, and retrieve forgotten information.

## When to use

- User asks about pages they visited ("what github repos did I look at last week?")
- User wants to find a forgotten page ("find that article about LLMs I read")
- User asks about browsing habits ("how much time did I spend on Twitter?")
- User wants browsing statistics ("show my most visited sites")

## Requirements

- `sqlite3` CLI

## Setup

First, detect available browsers by running:

```bash
./find-browser.sh
```

- Output: PATH,TYPE,BROWSER,LAST_MODIFIED
- **TYPE**: `firefox` or `chromium` (determines SQL syntax)
- Use the first result (most recently used browser) by default
- If multiple browsers were used recently (within last 24h), ask the user which one to search

## Querying the database

Use `?immutable=1` in the SQLite URI to read the database even when the browser is open:

```bash
sqlite3 "file:///path/to/history.db?immutable=1" "SELECT ..."
```

### Firefox databases (places.sqlite)

**Search by keyword:**
```sql
SELECT
    title,
    url,
    datetime(last_visit_date/1000000, 'unixepoch', 'localtime') as visit_date
FROM moz_places
WHERE url LIKE '%keyword%' OR title LIKE '%keyword%'
ORDER BY last_visit_date DESC
LIMIT 50;
```

**Search by date range:**
```sql
SELECT url, title, datetime(last_visit_date/1000000, 'unixepoch', 'localtime') as visit_date
FROM moz_places
WHERE last_visit_date > strftime('%s', '2025-01-01') * 1000000
  AND last_visit_date < strftime('%s', '2025-01-31') * 1000000
ORDER BY last_visit_date DESC;
```

**Time spent analysis** (uses moz_places_metadata):
```sql
SELECT
    SUM(m.total_view_time) / 1000 / 60 as minutes,
    COUNT(*) as sessions
FROM moz_places_metadata m
JOIN moz_places p ON m.place_id = p.id
WHERE p.url LIKE '%example.com%'
  AND m.created_at > strftime('%s', '2025-01-01') * 1000;
```

Note: `created_at` is in milliseconds, `last_visit_date` is in microseconds.

**Most visited sites:**
```sql
SELECT
    SUBSTR(url, INSTR(url, '://') + 3,
           INSTR(SUBSTR(url, INSTR(url, '://') + 3), '/') - 1) as domain,
    SUM(visit_count) as visits
FROM moz_places
WHERE url LIKE 'http%'
GROUP BY domain
ORDER BY visits DESC
LIMIT 20;
```

### Chromium databases (History)

**Important:** Chromium timestamps are microseconds since January 1, 1601 (Windows epoch).

Conversion: `(timestamp/1000000) - 11644473600` gives Unix epoch.

**Search by keyword:**
```sql
SELECT
    title,
    url,
    datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') as visit_date
FROM urls
WHERE url LIKE '%keyword%' OR title LIKE '%keyword%'
ORDER BY last_visit_time DESC
LIMIT 50;
```

**Search by date range:**
```sql
SELECT url, title, datetime((last_visit_time/1000000)-11644473600, 'unixepoch', 'localtime') as visit_date
FROM urls
WHERE last_visit_time > (strftime('%s', '2025-01-01') + 11644473600) * 1000000
  AND last_visit_time < (strftime('%s', '2025-01-31') + 11644473600) * 1000000
ORDER BY last_visit_time DESC;
```

## Database schema

### Firefox (moz_places)

| Column | Description |
|--------|-------------|
| `url` | Full URL |
| `title` | Page title |
| `last_visit_date` | Microseconds since Unix epoch |
| `visit_count` | Number of visits |
| `frecency` | Frequency + recency score |

### Firefox (moz_places_metadata)

| Column | Description |
|--------|-------------|
| `place_id` | Foreign key to moz_places |
| `total_view_time` | Milliseconds spent on page |
| `created_at` | Milliseconds since Unix epoch |
| `scrolling_time` | Time spent scrolling |
| `key_presses` | Number of key presses |

### Chromium (urls)

| Column | Description |
|--------|-------------|
| `url` | Full URL |
| `title` | Page title |
| `last_visit_time` | Microseconds since 1601-01-01 |
| `visit_count` | Number of visits |

## Output guidelines

- Present results in a readable format, grouped by domain when relevant
- For time analysis, show hours/minutes, not raw milliseconds
- When showing history, include the date and a clickable link
- If results are numerous, summarize by domain or time period
- You might include a small ASCII/Unicode chart (daily breakdown, histogram) if relevant

See @README.md for output examples.
