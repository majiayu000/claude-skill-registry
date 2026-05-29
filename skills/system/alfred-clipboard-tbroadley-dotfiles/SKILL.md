---
name: alfred-clipboard
description: Access Alfred's clipboard history. Search recent copies, find text you copied earlier, and analyze clipboard patterns.
---

# Alfred Clipboard History

This skill provides read-only access to Alfred's clipboard history via its SQLite database.

## Requirements

- Alfred Powerpack (clipboard history is a Powerpack feature)
- Clipboard history enabled in Alfred preferences

## Database Location

```
~/Library/Application Support/Alfred/Databases/clipboard.alfdb
```

To find it manually: Alfred Preferences → Advanced → "Reveal in Finder" → Databases folder

## When to Use

Use this skill when the user:
- Asks about something they copied earlier
- Wants to search their clipboard history
- Needs to find text they copied but lost
- Asks about recent clipboard items
- Mentions "clipboard" or "copied"

## Database Schema

```sql
CREATE TABLE clipboard(
    item,           -- The copied content (text)
    ts decimal,     -- Unix timestamp
    app,            -- Source application name
    apppath,        -- Path to source application
    dataType integer,  -- Type of data (0=text, 1=image, 2=file)
    dataHash        -- Hash of the content
);
```

## Important Warning

**This database is not intended to be user-serviceable.** Only run SELECT queries - never UPDATE, DELETE, or INSERT. Make a copy of the database before querying if you're concerned about corruption.

## Common Queries

### View Recent Clipboard Items
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, substr(item, 1, 100) as content, app
   FROM clipboard
   ORDER BY ts DESC
   LIMIT 20;"
```

### Search Clipboard History
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, substr(item, 1, 200) as content, app
   FROM clipboard
   WHERE item LIKE '%search term%'
   ORDER BY ts DESC
   LIMIT 10;"
```

### Get Full Content of Recent Item
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT item FROM clipboard ORDER BY ts DESC LIMIT 1;"
```

### Items from Today
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, substr(item, 1, 100) as content, app
   FROM clipboard
   WHERE date(ts, 'unixepoch', 'localtime') = date('now', 'localtime')
   ORDER BY ts DESC;"
```

### Items from Specific App
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, substr(item, 1, 100) as content
   FROM clipboard
   WHERE app = 'Google Chrome'
   ORDER BY ts DESC
   LIMIT 20;"
```

### Most Used Source Apps
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT app, count(*) as copies
   FROM clipboard
   GROUP BY app
   ORDER BY copies DESC
   LIMIT 10;"
```

### Text Items Only (exclude images/files)
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, substr(item, 1, 100) as content
   FROM clipboard
   WHERE dataType = 0
   ORDER BY ts DESC
   LIMIT 20;"
```

### Count Total Clipboard Items
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT count(*) FROM clipboard;"
```

### Items from Last Hour
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, substr(item, 1, 100) as content, app
   FROM clipboard
   WHERE ts > strftime('%s', 'now', '-1 hour')
   ORDER BY ts DESC;"
```

## Data Types

- `0` - Text
- `1` - Image
- `2` - File reference

Note: Image and file content is stored differently; the `item` field for these may not be directly readable as text.

## Common Workflows

### "What did I copy earlier that had [keyword]?"
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, item, app
   FROM clipboard
   WHERE item LIKE '%keyword%'
   ORDER BY ts DESC
   LIMIT 5;"
```

### "Show me everything I copied from Slack today"
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, substr(item, 1, 150) as content
   FROM clipboard
   WHERE app = 'Slack'
   AND date(ts, 'unixepoch', 'localtime') = date('now', 'localtime')
   ORDER BY ts DESC;"
```

### "Find that URL I copied"
```bash
sqlite3 ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime') as time, item, app
   FROM clipboard
   WHERE item LIKE 'http%'
   ORDER BY ts DESC
   LIMIT 10;"
```

## Output Formatting

For JSON output:
```bash
sqlite3 -json ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT * FROM clipboard ORDER BY ts DESC LIMIT 5;"
```

For CSV output:
```bash
sqlite3 -csv ~/Library/Application\ Support/Alfred/Databases/clipboard.alfdb \
  "SELECT datetime(ts, 'unixepoch', 'localtime'), item, app FROM clipboard ORDER BY ts DESC LIMIT 10;"
```

## Notes

- Alfred's clipboard history has a configurable retention period (default 24 hours, 7 days, 1 month, or 3 months)
- Very long items are truncated in the examples above using `substr()` for readability
- The database may be locked while Alfred is writing to it; retry if you get a lock error
- Consider copying the database to a temp location before querying for safety

## Sources

- [Searching Alfred's Clipboard History Programmatically](https://rmoff.net/2020/05/18/searching-alfreds-clipboard-history-programatically/)
- [Alfred Clipboard History Archive](https://github.com/April-June-August/alfred-clipboard-history-archive)
