---
name: whatsapp-logs
description: Read and analyze WhatsApp bot logs for debugging, monitoring, and troubleshooting. Use this skill when asked to "check WhatsApp logs", "debug the bot", "find WhatsApp errors", "analyze bot performance", "trace a message", "why did the bot fail", or any investigation of WhatsApp bot behavior. Covers log file locations, JSON log format, message tracing, error analysis, and common debugging patterns.
---

# WhatsApp Bot Log Analysis

## Log Files

| File Pattern                         | Purpose                          |
| ------------------------------------ | -------------------------------- |
| `logs/whatsapp-debug-YYYY-MM-DD.log` | All WhatsApp bot activity (JSON) |
| `logs/whatsapp-error-YYYY-MM-DD.log` | WhatsApp errors only             |

Get today's logs:

```bash
ls -la logs/whatsapp-*.log 2>/dev/null | tail -5
```

## JSON Log Structure

```json
{
  "timestamp": "2026-01-04 14:30:45.123",
  "level": "INFO",
  "message": "Received message",
  "service": "whatsapp",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "operation": "handleMessage",
  "durationMs": 1234,
  "meta": {
    "from": "972501234567",
    "isGroup": false,
    "textPreview": "What's in progress?"
  }
}
```

**Key Fields:**

- `service` - Always "whatsapp" for bot logs
- `correlationId` - UUID linking logs for a single request
- `operation` - What operation was performed
- `durationMs` - Time taken in milliseconds
- `meta.from` - Sender phone number
- `meta.isGroup` - Whether message came from a group

## Quick Commands

### View Recent Activity

```bash
tail -50 logs/whatsapp-debug-$(date +%Y-%m-%d).log | jq .
```

### Check Errors Today

```bash
cat logs/whatsapp-error-$(date +%Y-%m-%d).log 2>/dev/null | jq .
```

### Watch Logs Real-Time

```bash
tail -f logs/whatsapp-debug-$(date +%Y-%m-%d).log | jq .
```

### Find Messages From a Phone Number

```bash
grep '"from":"972501234567"' logs/whatsapp-debug-*.log | jq .
```

### Check Connection Status

```bash
grep -E "(Connected|Disconnected|reconnect)" logs/whatsapp-debug-*.log | tail -10 | jq .
```

## Common Debugging Scenarios

### Bot Not Responding

```bash
# Check if messages are being received
grep "Received message" logs/whatsapp-debug-$(date +%Y-%m-%d).log | tail -5 | jq '{time: .timestamp, from: .meta.from, text: .meta.textPreview}'

# Check for processing errors
grep -E '"level":"ERROR"' logs/whatsapp-debug-$(date +%Y-%m-%d).log | tail -10 | jq .
```

### Connection Issues

```bash
# Check connection events
grep -E "(connection|reconnect|disconnect)" logs/whatsapp-debug-*.log | jq '{time: .timestamp, msg: .message}'

# Check QR code events
grep "QR" logs/whatsapp-debug-*.log | tail -5 | jq .
```

### Voice Message Issues

```bash
# Check transcription activity
grep -E "(transcri|voice|audio)" logs/whatsapp-debug-*.log | jq '{time: .timestamp, msg: .message, duration: .meta.duration}'
```

### Group Message Issues

```bash
# Check group activity
grep '"isGroup":true' logs/whatsapp-debug-*.log | tail -10 | jq '{time: .timestamp, group: .meta.groupId, from: .meta.from}'

# Check group metadata fetching
grep "group.*metadata" logs/whatsapp-debug-*.log | jq .
```

### Image Processing Issues

```bash
# Check image downloads
grep -E "(image|media)" logs/whatsapp-debug-*.log | jq '{time: .timestamp, msg: .message, size: .meta.size}'
```

### Agent/Claude Issues

```bash
# Check agent processing
grep '"service":"whatsapp"' logs/whatsapp-debug-*.log | grep -E "(process|agent)" | jq .
```

## Trace a Single Request

1. Find the correlation ID from an error or message:

```bash
grep "Received message" logs/whatsapp-debug-$(date +%Y-%m-%d).log | tail -1 | jq .correlationId
```

2. Trace all related logs:

```bash
grep "CORRELATION_ID_HERE" logs/whatsapp-debug-*.log | jq .
```

## Performance Analysis

### Find Slow Operations (>5s)

```bash
grep durationMs logs/whatsapp-debug-*.log | jq 'select(.durationMs > 5000) | {msg: .message, duration: .durationMs}'
```

### Message Processing Times

```bash
grep "Sent response" logs/whatsapp-debug-*.log | jq '{time: .timestamp, duration: .meta.responseTime}'
```

### Count Messages Today

```bash
grep "Received message" logs/whatsapp-debug-$(date +%Y-%m-%d).log | wc -l
```

### Error Rate

```bash
echo "Errors: $(cat logs/whatsapp-error-$(date +%Y-%m-%d).log 2>/dev/null | wc -l)"
echo "Total: $(cat logs/whatsapp-debug-$(date +%Y-%m-%d).log | wc -l)"
```

## Log Rotation Configuration

| Setting     | Value | Description                    |
| ----------- | ----- | ------------------------------ |
| Max Size    | 20MB  | Rotates when file exceeds size |
| Max Days    | 14d   | Keeps logs for 14 days         |
| Compression | Yes   | Old logs are gzipped           |
| Error Logs  | 7d    | Error logs kept for 7 days     |

Log files are named: `whatsapp-debug-YYYY-MM-DD.log`
Old logs are compressed: `whatsapp-debug-YYYY-MM-DD.log.gz`

## Reading Compressed Logs

```bash
# Read compressed log
zcat logs/whatsapp-debug-2026-01-01.log.gz | jq . | head -50

# Search in compressed logs
zgrep "error" logs/whatsapp-debug-*.log.gz | head -20
```

## Log Level Configuration

Set via `LOG_LEVEL` environment variable when starting the bot:

- `error` - Only errors
- `warn` - Errors and warnings
- `info` - Normal operation (default)
- `debug` - Verbose debugging

```bash
LOG_LEVEL=debug npm run whatsapp
```

## Debugging Tips

1. **Start with errors** - Check `whatsapp-error-*.log` first
2. **Use correlation IDs** - Links all logs for a single message flow
3. **Check timestamps** - Gaps indicate hanging operations
4. **Look at meta field** - Contains phone numbers, group IDs, message previews
5. **Use jq for filtering** - JSON format enables powerful queries
6. **Compare durations** - Sudden increases indicate API issues
7. **Check both log files** - Debug logs show full flow, error logs show failures
