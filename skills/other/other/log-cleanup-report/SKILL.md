---
name: log-cleanup-report
description: Analyze log file sizes and signal-to-noise ratio. Shows what's consuming disk space and recommends cleanup actions. Use before archiving or when logs are getting too large.
---

# Log Cleanup Report

Analyze IQRight log files to understand disk usage and identify optimization opportunities.

## Step 1: Log File Inventory

Check all log locations:
- `logs/IQRight_Daemon.debug*` (server logs)
- `logs/IQRight_FE_WEB.debug*` (web app logs)
- `log/device_status.log` (device health, note: different directory)

For each, report: file name, size, line count.

## Step 2: Date Ranges

Extract first and last timestamps from each log file to understand the time span covered.

## Step 3: Signal-to-Noise Analysis

Count in the server log:
- **Noise**: `No packet received` lines (idle timeouts)
- **Signal**: `Received data from scanner`, `MQTT-TX`, `ERROR`, `HELLO`, `Connected`, `Disconnected`, `SWITCHING TO`

Calculate:
- Signal percentage: (signal lines / total) * 100
- Noise percentage: (noise lines / total) * 100
- Signal-to-noise ratio

### Adaptive Logging Check

If the log contains `SWITCHING TO ACTIVE MODE` or `Server started in IDLE mode`, the adaptive logging (Feb 2026) is active. In this case, noise should be minimal.

If the log contains massive amounts of `No packet received (timeout)`, the server is running pre-Feb 2026 code and should be upgraded.

## Step 4: Recommendations

Based on findings:

**If timeout lines > 50% of total**:
- Server needs adaptive logging upgrade (reduces logs by 90%+)
- Current idle mode: logs every timeout vs new: logs once per 5 min

**If total log size > 200MB**:
- Archive rotated logs older than 1 week
- Consider gzip compression for `.debug.MMDDYY` files
- Check `MAX_LOG_SIZE` and `BACKUP_COUNT` in config

**If signal-to-noise < 1:100**:
- Most of the log is wasted disk space
- Adaptive logging is the primary fix
- Secondary: raise log level from DEBUG to INFO for idle periods

**General maintenance**:
- Rotated logs (`.debug.MMDDYY`) can be compressed or deleted after analysis
- Device status logs are small and can be kept longer
- Web app logs follow same rotation as server logs

## Output Format

```
=== LOG CLEANUP REPORT ===

Files:
  {filename}  {size}  {lines}  {date range}
  ...
  Total: {size}  {lines}

Signal-to-Noise:
  Signal lines: {N} ({pct}%)
  Noise lines:  {N} ({pct}%)
  Ratio: 1:{N}

Adaptive Logging: ACTIVE / NOT DETECTED

Recommendations:
  1. ...
  2. ...

Estimated savings: {N} MB
```

Reference: See `docs/LOG_ANALYSIS_SKILLS.md` section 1 for log structure and adaptive logging details.