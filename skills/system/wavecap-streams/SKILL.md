---
name: wavecap-streams
description: Monitor and manage WaveCap audio streams. Use when the user asks about stream status, wants to list streams, check stream health, view recent transcriptions, or reset a stream.
---

# WaveCap Streams Skill

Use this skill to interact with WaveCap streams via the REST API.

## Configuration

The WaveCap server runs at `http://localhost:8000` by default. For authenticated operations (reset), you need an editor token.

## Available Operations

### List All Streams

```bash
curl -s http://localhost:8000/api/streams | jq
```

To get streams without transcription history (faster):
```bash
curl -s "http://localhost:8000/api/streams?includeTranscriptions=false" | jq
```

### Get Stream Status Summary

```bash
curl -s "http://localhost:8000/api/streams?includeTranscriptions=false" | jq '.[] | {id, name, status, error, source, lastActivityAt}'
```

### Get Recent Transcriptions for a Stream

```bash
curl -s "http://localhost:8000/api/streams/{STREAM_ID}/transcriptions?limit=10" | jq '.transcriptions[] | {timestamp, text, confidence}'
```

### Check API Health

```bash
curl -s http://localhost:8000/api/health | jq
```

### Reset a Stream (requires editor auth)

First, get an auth token:
```bash
TOKEN=$(curl -s -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"password": "YOUR_EDITOR_PASSWORD"}' | jq -r '.token')
```

Then reset the stream:
```bash
curl -s -X POST "http://localhost:8000/api/streams/{STREAM_ID}/reset" \
  -H "Authorization: Bearer $TOKEN"
```

## Stream Status Values

- `transcribing` - Stream is actively processing audio
- `queued` - Stream is waiting to start
- `stopped` - Stream has been stopped
- `error` - Stream encountered an error (check `error` field)

## Stream Source Types

- `audio` - HTTP audio stream (web URL)
- `pager` - Pager webhook feed
- `remote` - Remote audio source (e.g., from WaveCap-SDR)
- `combined` - Virtual combined view of multiple streams

## Response Format

Stream objects contain:
```json
{
  "id": "stream-id",
  "name": "Stream Name",
  "url": "http://stream-url",
  "status": "transcribing",
  "enabled": true,
  "pinned": false,
  "createdAt": "2025-01-01T00:00:00Z",
  "language": "en",
  "error": null,
  "source": "audio",
  "lastActivityAt": "2025-01-01T12:00:00Z",
  "transcriptions": [...]
}
```

## Tips

- Use `jq` to filter and format JSON responses
- For large transcription histories, use pagination with `before` parameter
- The `lastActivityAt` field shows when the stream last received content
