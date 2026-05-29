---
name: mcp-debugging
description: Debug MCP server issues and analyze logs for the Orient. Use this skill when investigating tool failures, API errors, slow operations, or troubleshooting MCP tool behavior. Covers log file locations, JSON log format, correlation IDs for request tracing, common debugging commands, and log rotation configuration.
---

# MCP Server Debugging

## Log Files

| File                 | Purpose                      |
| -------------------- | ---------------------------- |
| `logs/mcp-debug.log` | All debug logs (JSON format) |
| `logs/mcp-error.log` | Error-only logs              |

## JSON Log Structure

```json
{
  "timestamp": "2024-12-09 14:30:45.123",
  "level": "INFO",
  "message": "Tool completed: ai_first_health_check",
  "correlationId": "550e8400-e29b-41d4-a716-446655440000",
  "service": "mcp-server",
  "operation": "tool_call",
  "durationMs": 1234,
  "meta": { ... }
}
```

**Key Fields:**

- `correlationId` - UUID linking all logs for a single tool invocation
- `service` - Component (mcp-server, slack-service, slides-service, config)
- `durationMs` - Operation duration in milliseconds
- `meta` - Context (JQL queries, issue counts, API responses)

## Quick Debugging Commands

### Check Recent Errors

```bash
tail -20 logs/mcp-error.log | jq .
```

### Trace a Request (by correlation ID)

```bash
grep "550e8400" logs/mcp-debug.log | jq .
```

### Check Tool Calls

```bash
tail -100 logs/mcp-debug.log | grep "tool_call" | jq '{tool: .tool, status: .status}'
```

### Check Tool Arguments

```bash
tail -100 logs/mcp-debug.log | jq '{tool: .tool, args: .args}' | head -20
```

### Find Slow Operations (>3s)

```bash
grep durationMs logs/mcp-debug.log | jq 'select(.durationMs > 3000)'
```

### Watch Logs Real-Time

```bash
tail -f logs/mcp-debug.log | jq .
```

### Filter by Service

```bash
tail -f logs/mcp-debug.log | grep '"service":"jira"' | jq .
```

## Common Debugging Scenarios

### MCP Tool Not Working

1. Check if tool was invoked:

   ```bash
   grep "Tool invoked: TOOL_NAME" logs/mcp-debug.log | tail -5
   ```

2. Check completion status:

   ```bash
   grep "TOOL_NAME" logs/mcp-debug.log | grep -E '"status":"(success|error)"' | tail -5 | jq .
   ```

3. Trace full request using correlation ID

### Jira API Issues

```bash
# Check Jira errors
grep '"service":"jira' logs/mcp-debug.log | grep '"level":"ERROR"' | jq .

# See JQL queries
grep '"service":"jira' logs/mcp-debug.log | jq 'select(.meta.jql) | {operation: .operation, jql: .meta.jql}'
```

### Google Slides API Issues

```bash
# Check initialization
grep '"service":"slides' logs/mcp-debug.log | grep "initialize" | jq .

# Check operations
grep '"service":"slides' logs/mcp-debug.log | jq '{operation: .operation, slideId: .meta.slideId, status: .status}'
```

### Config Loading Issues

```bash
grep '"service":"config"' logs/mcp-debug.log | jq .
```

## Log Level Configuration

Set via `LOG_LEVEL` environment variable:

- `error` - Only errors
- `warn` - Errors and warnings
- `info` - Normal operation (default)
- `debug` - Verbose debugging

```bash
LOG_LEVEL=debug npm run start
```

## Log Rotation

| Variable       | Default | Description              |
| -------------- | ------- | ------------------------ |
| `LOG_MAX_SIZE` | `10m`   | Max size before rotation |
| `LOG_MAX_DAYS` | `14d`   | Days to keep debug logs  |

Log files are named: `mcp-debug-YYYY-MM-DD.log`
Old logs are compressed: `mcp-debug-YYYY-MM-DD.log.gz`

## Sensitive Data

Logs automatically redact:

- API tokens
- Passwords
- Secrets
- Authorization headers

`[REDACTED]` in logs is intentional security behavior.

## Debugging Tips

1. **Start with correlation ID** - Links all related log entries
2. **Check timestamps** - Look for unusual gaps (hanging operations)
3. **Compare durations** - Sudden increases indicate API issues
4. **Look at meta field** - Detailed context (issue counts, JQL, responses)
5. **Use jq for filtering** - JSON format makes extraction easy
6. **Check stderr during startup** - Human-readable logs for immediate visibility
