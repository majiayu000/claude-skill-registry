---
name: wavecap-health
description: Check WaveCap server health and system status. Use when the user asks about server status, wants to diagnose issues, check if the backend is running, or get a system overview.
---

# WaveCap Health Skill

Use this skill to check WaveCap server health and diagnose system issues.

## Quick Health Check

```bash
curl -s http://localhost:8000/api/health | jq
```

Expected response when healthy:
```json
{"status": "ok"}
```

If this fails with connection refused, the backend server is not running.

## Comprehensive System Status

Get a full system overview including all streams and their states:

```bash
curl -s "http://localhost:8000/api/streams?includeTranscriptions=false" | jq '{
  total_streams: length,
  by_status: (group_by(.status) | map({status: .[0].status, count: length})),
  by_source: (group_by(.source) | map({source: .[0].source, count: length})),
  streams: [.[] | {id, name, status, error, source, enabled, lastActivityAt}]
}'
```

## Diagnose Stream Errors

Find streams with errors:

```bash
curl -s "http://localhost:8000/api/streams?includeTranscriptions=false" | jq '[.[] | select(.error != null)] | .[] | {id, name, status, error}'
```

## Check Stream Activity

Find streams by last activity time:

```bash
curl -s "http://localhost:8000/api/streams?includeTranscriptions=false" | jq '[.[] | select(.lastActivityAt != null)] | sort_by(.lastActivityAt) | reverse | .[] | {name, status, lastActivityAt}'
```

## Check Inactive Streams

Find enabled streams that haven't had activity recently:

```bash
curl -s "http://localhost:8000/api/streams?includeTranscriptions=false" | jq --arg cutoff "$(date -u -v-1H +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '1 hour ago' +%Y-%m-%dT%H:%M:%SZ)" '[.[] | select(.enabled == true and (.lastActivityAt == null or .lastActivityAt < $cutoff))] | .[] | {id, name, status, lastActivityAt}'
```

## Backend Logs

Check the backend log file for errors:

```bash
tail -100 /Users/thw/Projects/WaveCap/state/backend.log | grep -i error
```

Recent log entries:

```bash
tail -50 /Users/thw/Projects/WaveCap/state/backend.log
```

## Check Running Processes

Verify the backend process is running:

```bash
pgrep -f "uvicorn.*wavecap" && echo "Backend is running" || echo "Backend is NOT running"
```

Check what's listening on port 8000:

```bash
lsof -i :8000 | head -5
```

## Server Configuration

View current server config:

```bash
curl -s http://localhost:8000/api/ui-config | jq
```

View logging config:

```bash
curl -s http://localhost:8000/api/logging-config | jq
```

## Common Issues

### Connection Refused
- Backend server is not running
- Check service status: `launchctl list | grep wavecap`
- Start service: `launchctl load ~/Library/LaunchAgents/com.wavecap.server.plist`

### Stream Stuck in "queued"
- May be waiting for concurrent process slot
- Check `whisper.maxConcurrentProcesses` in config

### Stream in "error" State
- Check the `error` field in stream response
- Common causes: invalid URL, network issues, audio format problems
- Try resetting the stream

### No Recent Transcriptions
- Check stream status is `transcribing`
- Verify audio source is active
- Check for silence detection thresholds in config

## Restart Backend

WaveCap runs as a macOS Launch Agent. Use launchctl to manage it:

```bash
# Check service status
launchctl list | grep wavecap

# Restart the service
launchctl unload ~/Library/LaunchAgents/com.wavecap.server.plist && launchctl load ~/Library/LaunchAgents/com.wavecap.server.plist
```

For more service management options (start, stop, logs, troubleshooting), use the **wavecap-service** skill.

## API Response Codes

| Code | Meaning |
|------|---------|
| 200 | Success |
| 401 | Authentication required |
| 403 | Forbidden (wrong role) |
| 404 | Resource not found |
| 422 | Validation error |
| 500 | Server error |
