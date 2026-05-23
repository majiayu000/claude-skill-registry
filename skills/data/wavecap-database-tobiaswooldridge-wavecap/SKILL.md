---
name: wavecap-database
description: Query and inspect the WaveCap SQLite database. Use when the user wants to run SQL queries, inspect transcription records, check event metadata, debug database issues, or analyze historical data.
---

# WaveCap Database Skill

Use this skill to directly query and inspect the WaveCap SQLite database.

## Database Location

```bash
DB_PATH="/Users/thw/Projects/WaveCap/state/runtime.sqlite"
```

## Quick Database Access

### Open interactive SQLite shell
```bash
sqlite3 "$DB_PATH"
```

### Run a single query
```bash
sqlite3 "$DB_PATH" "SELECT COUNT(*) FROM transcriptions;"
```

## Database Schema

### Streams Table
```sql
CREATE TABLE streams (
    id TEXT PRIMARY KEY,
    name TEXT,
    url TEXT,
    status TEXT,
    createdAt DATETIME,
    language TEXT,
    error TEXT,
    source TEXT DEFAULT 'audio',
    webhookToken TEXT,
    ignoreFirstSeconds REAL DEFAULT 0,
    lastActivityAt DATETIME,
    enabled BOOLEAN,
    pinned BOOLEAN DEFAULT 0
);
```

### Transcriptions Table
```sql
CREATE TABLE transcriptions (
    id TEXT PRIMARY KEY,
    streamId TEXT REFERENCES streams(id),
    text TEXT,
    timestamp DATETIME NOT NULL,
    confidence REAL,
    duration REAL,
    segments TEXT,           -- JSON array of segment data
    recordingUrl TEXT,
    correctedText TEXT,
    reviewStatus TEXT NOT NULL DEFAULT 'pending',
    reviewedAt DATETIME,
    reviewedBy TEXT,
    eventType TEXT DEFAULT 'transcription',
    pagerIncident TEXT,      -- JSON object for pager data
    eventMetadata TEXT       -- JSON object for event tracing
);
```

## Common Queries

### Count transcriptions by stream
```bash
sqlite3 "$DB_PATH" "
SELECT s.name, COUNT(t.id) as count
FROM streams s
LEFT JOIN transcriptions t ON s.id = t.streamId
GROUP BY s.id
ORDER BY count DESC;
"
```

### Recent transcriptions with text
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp) as time,
       substr(text, 1, 80) as text_preview
FROM transcriptions
WHERE eventType = 'transcription'
ORDER BY timestamp DESC
LIMIT 20;
"
```

### System events (start/stop/disconnect)
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp) as time,
       eventType,
       text,
       eventMetadata
FROM transcriptions
WHERE eventType != 'transcription'
ORDER BY timestamp DESC
LIMIT 30;
"
```

### Event metadata for debugging
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp) as time,
       eventType,
       json_extract(eventMetadata, '$.source') as source,
       json_extract(eventMetadata, '$.trigger_type') as trigger,
       text
FROM transcriptions
WHERE eventMetadata IS NOT NULL
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Find duplicate events (same text within 5 seconds)
```bash
sqlite3 "$DB_PATH" "
SELECT t1.timestamp, t1.eventType, t1.text,
       json_extract(t1.eventMetadata, '$.source') as source1,
       json_extract(t2.eventMetadata, '$.source') as source2
FROM transcriptions t1
JOIN transcriptions t2 ON t1.streamId = t2.streamId
  AND t1.text = t2.text
  AND t1.id != t2.id
  AND abs(julianday(t1.timestamp) - julianday(t2.timestamp)) * 86400 < 5
WHERE t1.eventType != 'transcription'
ORDER BY t1.timestamp DESC
LIMIT 20;
"
```

### Transcriptions by event type
```bash
sqlite3 "$DB_PATH" "
SELECT eventType, COUNT(*) as count
FROM transcriptions
GROUP BY eventType
ORDER BY count DESC;
"
```

### Review status summary
```bash
sqlite3 "$DB_PATH" "
SELECT reviewStatus, COUNT(*) as count
FROM transcriptions
WHERE eventType = 'transcription'
GROUP BY reviewStatus;
"
```

### Transcriptions with corrections
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp) as time,
       substr(text, 1, 50) as original,
       substr(correctedText, 1, 50) as corrected
FROM transcriptions
WHERE correctedText IS NOT NULL
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Stream activity timeline
```bash
sqlite3 "$DB_PATH" "
SELECT s.name,
       datetime(s.lastActivityAt) as last_activity,
       s.status,
       s.enabled
FROM streams s
ORDER BY s.lastActivityAt DESC;
"
```

### Transcriptions in time range
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp) as time, text
FROM transcriptions
WHERE timestamp > datetime('now', '-1 hour')
  AND eventType = 'transcription'
ORDER BY timestamp DESC;
"
```

### Pager incidents with details
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp) as time,
       json_extract(pagerIncident, '$.callType') as call_type,
       json_extract(pagerIncident, '$.address') as address,
       text
FROM transcriptions
WHERE pagerIncident IS NOT NULL
ORDER BY timestamp DESC
LIMIT 20;
"
```

## Database Maintenance

### Check database size
```bash
ls -lh "$DB_PATH"
```

### Check table sizes
```bash
sqlite3 "$DB_PATH" "
SELECT name,
       (SELECT COUNT(*) FROM transcriptions) as transcriptions_count,
       (SELECT COUNT(*) FROM streams) as streams_count;
"
```

### Vacuum database (reclaim space)
```bash
sqlite3 "$DB_PATH" "VACUUM;"
```

### Export transcriptions to CSV
```bash
sqlite3 -header -csv "$DB_PATH" "
SELECT timestamp, streamId, text, confidence, eventType
FROM transcriptions
ORDER BY timestamp DESC
LIMIT 1000;
" > /tmp/transcriptions_export.csv
```

### Backup database
```bash
cp "$DB_PATH" "/tmp/wavecap_backup_$(date +%Y%m%d_%H%M%S).sqlite"
```

## Indexes

The database has these indexes for performance:
- `ix_streams_last_activity` on streams(lastActivityAt)
- `ix_transcriptions_stream_timestamp` on transcriptions(streamId, timestamp)
- `ix_transcriptions_timestamp` on transcriptions(timestamp)

## Tips

- Use `datetime(timestamp)` to format timestamps readably
- Use `json_extract()` to query JSON fields (segments, pagerIncident, eventMetadata)
- Use `substr(text, 1, N)` to truncate long text in output
- The eventMetadata field contains tracing info: source, trigger_type, trigger_detail
- Event types: transcription, recording_started, recording_stopped, upstream_disconnected, upstream_reconnected
