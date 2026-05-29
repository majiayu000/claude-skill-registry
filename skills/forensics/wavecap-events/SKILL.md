---
name: wavecap-events
description: Debug and trace WaveCap system events. Use when the user wants to investigate duplicate events, trace event sources, debug recording start/stop issues, or understand event flow.
---

# WaveCap Events Debugging Skill

Use this skill to debug and trace system events in WaveCap (recording started/stopped, upstream disconnect/reconnect).

## Database Location

```bash
DB_PATH="/Users/thw/Projects/WaveCap/state/runtime.sqlite"
```

## Event Types

| Event Type | Description |
|------------|-------------|
| `transcription` | Normal speech transcription |
| `recording_started` | Stream began recording/transcribing |
| `recording_stopped` | Stream stopped recording |
| `upstream_disconnected` | Lost connection to audio source |
| `upstream_reconnected` | Reconnected to audio source |

## Event Metadata Fields

System events include hidden `eventMetadata` JSON with:
- `source`: Where the event was emitted from (handle_status_change, upstream_disconnect, upstream_reconnect, shutdown)
- `trigger_type`: What triggered the event (automatic_resume, user_request, service_shutdown, system_activity, etc.)
- `trigger_detail`: Additional context about the trigger

## Debugging Queries

### View recent system events with metadata
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp, 'localtime') as time,
       eventType,
       json_extract(eventMetadata, '$.source') as source,
       json_extract(eventMetadata, '$.trigger_type') as trigger,
       substr(text, 1, 60) as message
FROM transcriptions
WHERE eventType != 'transcription'
ORDER BY timestamp DESC
LIMIT 30;
"
```

### Find duplicate recording_started events
```bash
sqlite3 "$DB_PATH" "
SELECT t1.id, datetime(t1.timestamp, 'localtime') as time,
       json_extract(t1.eventMetadata, '$.source') as source,
       json_extract(t1.eventMetadata, '$.trigger_type') as trigger,
       t1.text
FROM transcriptions t1
WHERE t1.eventType = 'recording_started'
  AND EXISTS (
    SELECT 1 FROM transcriptions t2
    WHERE t2.streamId = t1.streamId
      AND t2.eventType = 'recording_started'
      AND t2.id != t1.id
      AND abs(julianday(t1.timestamp) - julianday(t2.timestamp)) * 86400 < 10
  )
ORDER BY t1.timestamp DESC
LIMIT 20;
"
```

### Track stream lifecycle (starts and stops)
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp, 'localtime') as time,
       eventType,
       json_extract(eventMetadata, '$.trigger_type') as trigger,
       substr(text, 1, 70) as message
FROM transcriptions
WHERE eventType IN ('recording_started', 'recording_stopped')
ORDER BY timestamp DESC
LIMIT 40;
"
```

### Events for a specific stream
```bash
STREAM_ID="broadcastify-2653"
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp, 'localtime') as time,
       eventType,
       json_extract(eventMetadata, '$.source') as source,
       text
FROM transcriptions
WHERE streamId = '$STREAM_ID'
  AND eventType != 'transcription'
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Upstream connectivity events
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp, 'localtime') as time,
       eventType,
       json_extract(eventMetadata, '$.trigger_detail') as detail,
       text
FROM transcriptions
WHERE eventType IN ('upstream_disconnected', 'upstream_reconnected')
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Events by source location
```bash
sqlite3 "$DB_PATH" "
SELECT json_extract(eventMetadata, '$.source') as source,
       eventType,
       COUNT(*) as count
FROM transcriptions
WHERE eventMetadata IS NOT NULL
GROUP BY source, eventType
ORDER BY count DESC;
"
```

### Events by trigger type
```bash
sqlite3 "$DB_PATH" "
SELECT json_extract(eventMetadata, '$.trigger_type') as trigger,
       eventType,
       COUNT(*) as count
FROM transcriptions
WHERE eventMetadata IS NOT NULL
GROUP BY trigger, eventType
ORDER BY count DESC;
"
```

### Recent service restarts (automatic_resume events)
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp, 'localtime') as time,
       streamId,
       text
FROM transcriptions
WHERE eventType = 'recording_started'
  AND json_extract(eventMetadata, '$.trigger_type') = 'automatic_resume'
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Shutdown events
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp, 'localtime') as time,
       streamId,
       text
FROM transcriptions
WHERE json_extract(eventMetadata, '$.trigger_type') = 'service_shutdown'
   OR json_extract(eventMetadata, '$.source') = 'shutdown'
ORDER BY timestamp DESC
LIMIT 20;
"
```

### Events in the last hour
```bash
sqlite3 "$DB_PATH" "
SELECT datetime(timestamp, 'localtime') as time,
       eventType,
       json_extract(eventMetadata, '$.source') as source,
       substr(text, 1, 50) as message
FROM transcriptions
WHERE timestamp > datetime('now', '-1 hour')
  AND eventType != 'transcription'
ORDER BY timestamp;
"
```

### Gap analysis (time between events)
```bash
sqlite3 "$DB_PATH" "
WITH events AS (
  SELECT timestamp,
         eventType,
         LAG(timestamp) OVER (ORDER BY timestamp) as prev_time
  FROM transcriptions
  WHERE eventType != 'transcription'
)
SELECT datetime(timestamp, 'localtime') as time,
       eventType,
       ROUND((julianday(timestamp) - julianday(prev_time)) * 86400, 1) as gap_seconds
FROM events
WHERE prev_time IS NOT NULL
ORDER BY timestamp DESC
LIMIT 30;
"
```

## Event Source Locations (Code Reference)

| Source | File | Description |
|--------|------|-------------|
| `handle_status_change` | stream_manager.py | Worker status transitions |
| `upstream_disconnect` | stream_manager.py | Audio source connection lost |
| `upstream_reconnect` | stream_manager.py | Audio source reconnected |
| `shutdown` | stream_manager.py | Service shutdown cleanup |

## Trigger Types (Code Reference)

| Trigger Type | Description |
|--------------|-------------|
| `automatic_resume` | Service restart resuming enabled streams |
| `automatic_synchronization` | Re-aligning stream state |
| `user_request` | Manual start/stop from UI |
| `service_shutdown` | Graceful service shutdown |
| `source_stream_ended` | Upstream audio ended naturally |
| `stream_error` | Error occurred in stream |
| `system_activity` | Generic system-triggered event |

## Tips

- Events without `eventMetadata` are from before the tracing was added
- Use `datetime(timestamp, 'localtime')` for local time display
- Duplicate events within seconds usually indicate a bug in event emission
- The `text` field includes human-readable trigger info in parentheses
