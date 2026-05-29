---
name: b2c-logs
description: Retrieve and monitor log files from B2C Commerce instances. Use when fetching recent errors, searching log entries, filtering by level/time, or real-time tailing. The `logs get` command is optimized for coding agents with JSON output.
---

# B2C Logs Skill

Use the `b2c` CLI to retrieve and monitor log files on Salesforce B2C Commerce instances. The `logs get` command is designed for agent-friendly, non-interactive log retrieval with structured JSON output.

## Agent-Friendly Log Retrieval

The `logs get` command is optimized for coding agents:
- Exits immediately after retrieving logs (non-interactive)
- Supports `--json` for structured output
- Filters by time, level, and text search
- Auto-normalizes file paths for IDE click-to-open

## Examples

### Get Recent Logs

```bash
# Get last 20 entries from error and customerror logs (default)
b2c logs get

# Get last 50 entries
b2c logs get --count 50

# JSON output for programmatic parsing
b2c logs get --json
```

### Filter by Time

```bash
# Entries from the last 5 minutes
b2c logs get --since 5m

# Entries from the last 1 hour
b2c logs get --since 1h

# Entries from the last 2 days
b2c logs get --since 2d

# Entries after a specific time (ISO 8601)
b2c logs get --since "2026-01-25T10:00:00"
```

### Filter by Log Level

```bash
# Only ERROR level entries
b2c logs get --level ERROR

# ERROR and FATAL entries
b2c logs get --level ERROR --level FATAL
```

### Search Text

```bash
# Search for "OrderMgr" in messages
b2c logs get --search OrderMgr

# Search for payment errors
b2c logs get --search "PaymentProcessor"
```

### Combined Filters

```bash
# Recent errors containing "PaymentProcessor"
b2c logs get --since 1h --level ERROR --search "PaymentProcessor" --json

# Last hour of errors and fatals from specific log types
b2c logs get --filter error --filter warn --since 1h --level ERROR --level FATAL
```

### List Available Log Files

```bash
# List all log files
b2c logs list

# List specific log types
b2c logs list --filter error --filter customerror

# JSON output
b2c logs list --json
```

### Real-Time Tailing (Human Use)

For interactive log monitoring (not for agents):

```bash
# Tail error and customerror logs
b2c logs tail

# Tail specific log types
b2c logs tail --filter debug --filter error

# Tail only ERROR and FATAL level entries
b2c logs tail --level ERROR --level FATAL

# Tail with text search
b2c logs tail --search "PaymentProcessor"

# Combined filtering
b2c logs tail --filter customerror --level ERROR --search "OrderMgr"

# Stop with Ctrl+C
```

## Downloading Full Log Files

To download the complete log file, use the `file` field from the JSON output with `b2c-cli:b2c-webdav`:

```bash
b2c webdav get error-odspod-0-appserver-20260126.log --root=logs -o -
```

## JSON Output Structure

When using `--json`, `logs get` returns:

```json
{
  "count": 1,
  "entries": [
    {
      "file": "error-odspod-0-appserver-20260126.log",
      "timestamp": "2026-01-26 04:38:03.022 GMT",
      "level": "ERROR",
      "message": "PipelineCallServlet|156679877|Sites-Site|...",
      "raw": "[2026-01-26 04:38:03.022 GMT] ERROR PipelineCallServlet|..."
    }
  ]
}
```

| Field | Description |
|-------|-------------|
| `file` | Source log file name (use with `b2c-cli:b2c-webdav` to download full file) |
| `level` | Log level: ERROR, WARN, INFO, DEBUG, FATAL, TRACE |
| `timestamp` | Entry timestamp |
| `message` | Log message (paths normalized for IDE click-to-open) |
| `raw` | Raw unprocessed log line |

## Log Types

Common log file prefixes:

| Prefix | Description |
|--------|-------------|
| `error` | System errors |
| `customerror` | Custom script errors (`Logger.error()`) |
| `warn` | Warnings |
| `debug` | Debug output (when enabled) |
| `info` | Informational messages |
| `jobs` | Job execution logs |
| `api` | API problems and violations |
| `deprecation` | Deprecated API usage |
| `quota` | Quota warnings |

## More Commands

See `b2c logs --help` for all available commands and options.

## Related Skills

- `b2c-cli:b2c-webdav` - Direct WebDAV file access for downloading full log files
- `b2c-cli:b2c-config` - Verify configuration and credentials
