---
name: py-server-logs
description: View Flask server logs from local or remote server. Shows real-time or recent log entries for debugging. Use when monitoring server activity, debugging issues, or checking server status.
---

# Python Server Logs

## Overview

Views logs from Flask servers (local or remote) to monitor activity, debug issues, and check server status. Supports real-time streaming and historical log viewing.

## When to Use

Invoke this skill when the user:
- Asks to "see server logs"
- Wants to "check what the server is doing"
- Says "view logs" or "monitor server"
- Mentions debugging server issues
- Wants to see recent server activity

## Prerequisites

**Local server**:
- Server running in background mode (creates server.log)
- In server directory with log file

**Remote server**:
- SSH access configured
- SSH config alias set up (microserver)
- Remote server running

## Instructions

### View Local Server Logs

**Real-time streaming** (follows log as it grows):
```bash
cd path/to/server/imp/py
tail -f server.log
```

**Last 20 lines**:
```bash
tail -20 server.log
```

**Last 50 lines**:
```bash
tail -50 server.log
```

**All logs**:
```bash
cat server.log
```

**Search logs**:
```bash
grep "ERROR" server.log
grep "api/ping" server.log
grep "POST" server.log
```

### View Remote Server Logs

**Real-time streaming**:
```bash
ssh microserver@185.96.221.52 "tail -f ~/firefly-server/server.log"
```

**Last 20 lines**:
```bash
ssh microserver@185.96.221.52 "tail -20 ~/firefly-server/server.log"
```

**Search remote logs**:
```bash
ssh microserver@185.96.221.52 "grep 'ERROR' ~/firefly-server/server.log"
```

## What to Tell User

**Local logs**:
- Show command to view logs
- Mention Ctrl+C to stop streaming
- Indicate log file location
- Suggest useful search patterns

**Remote logs**:
- Same as local, but via SSH
- Mention network connection required
- Log format is identical

## Log Format

Flask logs typically show:
```
127.0.0.1 - - [05/Oct/2024 18:15:23] "GET /api/ping HTTP/1.1" 200 -
127.0.0.1 - - [05/Oct/2024 18:15:24] "POST /api/posts HTTP/1.1" 200 -
```

Format:
- **IP address**: Client making request
- **Timestamp**: When request occurred
- **Method**: GET, POST, etc.
- **Path**: API endpoint
- **Status**: HTTP response code (200=OK, 500=error, etc.)

## Common Log Patterns

**Successful requests**:
```bash
grep "200" server.log
```

**Errors**:
```bash
grep -E "(ERROR|500|404)" server.log
```

**Specific endpoint**:
```bash
grep "/api/ping" server.log
```

**Recent activity**:
```bash
tail -20 server.log
```

**POST requests only**:
```bash
grep "POST" server.log
```

## Integration with Claude Code

Claude can read logs directly:
```bash
# Last 20 lines
tail -20 server.log

# Search for specific issue
grep "ERROR" server.log
```

This enables Claude to:
- Debug server issues
- Verify requests are reaching server
- Check for errors or warnings
- Monitor API usage patterns

## Troubleshooting

**"No such file or directory"**:
- Log file doesn't exist yet
- Server wasn't started in background mode
- Check: `ls -la server.log`
- Start server with start.sh to create logs

**Logs not updating**:
- Server may be running in foreground (logs to terminal)
- Check if process is running: `lsof -ti:8080`
- Verify server.log is the active log file

**Too much output**:
- Use `tail` instead of `cat` for large logs
- Filter with `grep` for specific patterns
- Consider log rotation for production

**Can't access remote logs**:
- Check SSH connection: `ssh microserver@185.96.221.52 "ls"`
- Verify path: `~/firefly-server/server.log`
- Check permissions on remote log file

## Log Levels

Flask can log at different levels:
- **DEBUG**: Detailed information for diagnosing problems
- **INFO**: General informational messages
- **WARNING**: Warning messages for potential issues
- **ERROR**: Error messages for serious problems
- **CRITICAL**: Critical errors causing server failure

Flask development server logs most requests at INFO level.

## Clearing Logs

**Local**:
```bash
# Clear log file
> server.log
# Or delete and recreate
rm server.log
touch server.log
```

**Remote**:
```bash
ssh microserver@185.96.221.52 "> ~/firefly-server/server.log"
```

This is useful before testing to see only new logs.

## Advanced Usage

**Follow logs and filter**:
```bash
tail -f server.log | grep "ERROR"
```

**Count requests per endpoint**:
```bash
grep -o "/api/[a-z]*" server.log | sort | uniq -c
```

**Show only errors**:
```bash
grep -E "ERROR|500" server.log
```

**Last hour of logs** (if timestamps in log):
```bash
# Depends on log format
grep "$(date +%H:)" server.log
```

## Foreground vs Background Logging

**Foreground server** (`python3 app.py`):
- Logs to terminal (stdout)
- No server.log file
- See logs in terminal directly
- Use py-server-logs for background servers only

**Background server** (`./start.sh`):
- Logs to server.log
- Terminal output redirected
- Use tail/grep to view
- This skill is designed for this mode

## Remote Server Path

For Firefly server specifically:
- **Path**: ~/firefly-server/server.log
- **Host**: microserver@185.96.221.52
- **Via SSH**: ssh microserver@185.96.221.52

## Stopping Log Stream

When using `tail -f`:
- Press **Ctrl+C** to stop streaming
- Terminal returns to prompt
- Log file continues to grow

## Log Rotation

For production servers, implement log rotation:
- Prevents log files from growing too large
- Archives old logs
- Can use `logrotate` utility on Linux/macOS

For development, manual clearing is sufficient.

## Notes

- Local and remote logs have identical format
- Logs persist across server restarts
- Log file grows continuously (monitor size)
- Background mode required for log file
- Real-time streaming with `tail -f` is most useful for active debugging
