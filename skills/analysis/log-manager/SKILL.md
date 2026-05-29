---
name: log-manager
description: Reads and analyzes application logs for debugging and monitoring.
---

# Log Manager Skill

Helps you read logs and identify errors in the application.

## Capabilities

- **Read Recent Logs**: Fetches the last N lines of logs from PM2.
- **Scan for Errors**: Searches log files for keywords like "Error", "Exception", "Fail".

## Scripts

### 1. Read Logs
```bash
node .agent/skills/log-manager/scripts/read_logs.js [lines] [process_name]
```
*   `lines` (optional): Number of lines to read (default: 50).
*   `process_name` (optional): Specific PM2 process name (default: all).

### 2. Scan for Errors
```bash
node .agent/skills/log-manager/scripts/scan_errors.js
```
Scans `bot.log` and PM2 error logs for issues.
