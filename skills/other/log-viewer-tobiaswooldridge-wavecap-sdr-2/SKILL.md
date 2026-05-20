---
name: log-viewer
description: View and analyze WaveCap-SDR server logs, debug output, and error messages. Use when troubleshooting server issues, debugging API errors, monitoring SDR device status, or investigating capture/channel problems.
---

# Log Viewer for WaveCap-SDR

This skill provides tools to view, search, and analyze logs from the WaveCap-SDR server including API errors, SDR device messages, and debug output.

## When to Use This Skill

Use this skill when:
- Troubleshooting API errors (500, 4xx responses)
- Investigating SDR device connection issues
- Debugging capture or channel problems
- Monitoring server health and status
- Reviewing recent API requests
- Checking for SoapySDR driver messages

## Log Sources

| Source | Description | Location |
|--------|-------------|----------|
| Server stdout | API requests, startup messages | Terminal/console |
| Server stderr | Errors, warnings, SoapySDR | Terminal/console |
| Debug log | Detailed error tracebacks | `/tmp/wavecapsdr_error.log` |
| SoapySDR | SDR driver messages | Embedded in stderr |

## Usage Instructions

### Step 1: View Recent Error Logs

Check the debug error log for recent exceptions:

```bash
cat /tmp/wavecapsdr_error.log 2>/dev/null || echo "No error log found"
```

Or use the helper script:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/log-viewer/view_logs.py --errors
```

### Step 2: Get Server Status

Check if the server is running and get process info:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/log-viewer/view_logs.py --status
```

### Step 3: View API Request History

Get recent API requests from server logs (if available):

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/log-viewer/view_logs.py --requests
```

### Step 4: Check SDR Device Logs

View SoapySDR-related messages:

```bash
PYTHONPATH=backend backend/.venv/bin/python .claude/skills/log-viewer/view_logs.py --sdr
```

### Step 5: Test API Health

Verify API is responding and check health endpoint:

```bash
curl -s http://127.0.0.1:8087/api/v1/health | jq
```

## Helper Script Reference

```bash
# View all available log info
python view_logs.py --all

# View only errors
python view_logs.py --errors

# View server status
python view_logs.py --status

# View recent API requests
python view_logs.py --requests

# View SDR device logs
python view_logs.py --sdr

# Specify custom port
python view_logs.py --port 8087 --all

# Filter by time (last N minutes)
python view_logs.py --errors --minutes 5
```

## Common Log Patterns

### Successful API Request
```
INFO:     127.0.0.1:12345 - "GET /api/v1/captures HTTP/1.1" 200 OK
```

### Failed API Request
```
INFO:     127.0.0.1:12345 - "PATCH /api/v1/captures/c1 HTTP/1.1" 500 Internal Server Error
```

### SDR Device Message
```
[SOAPY] Using stream format: CF32
[DEBUG] Device RTLSDR: Available antennas: ('RX',)
```

### Error Traceback (in /tmp/wavecapsdr_error.log)
```
--- 2025-11-22 12:34:56.789 ---
[ERROR] update_capture failed: Device timeout
Traceback (most recent call last):
  ...
```

## API Endpoints for Log Analysis

### GET /api/v1/health
Returns server health status.

```json
{
  "status": "healthy",
  "captures": 2,
  "channels": 2,
  "devices": 3
}
```

### GET /api/v1/captures
Returns all captures with their current state and any error messages.

```json
[
  {
    "id": "c1",
    "state": "running",
    "errorMessage": null
  }
]
```

### GET /api/v1/channels/{chan_id}/metrics/extended
Returns detailed channel metrics including stream health.

## Troubleshooting Common Issues

### Issue: API Returns 500 Internal Server Error
**Steps**:
1. Check `/tmp/wavecapsdr_error.log` for traceback
2. Look for device-related errors in the log
3. Verify SDR device is connected: `SoapySDRUtil --find`
4. Check server stderr for SoapySDR errors

### Issue: Capture Stuck in "starting" State
**Steps**:
1. Check for SDR driver errors in logs
2. Verify device isn't in use by another process
3. Look for timeout messages
4. Try restarting the capture

### Issue: No Audio / Channel Not Working
**Steps**:
1. Check channel state via API
2. Look for demodulator errors in logs
3. Verify capture is running
4. Check signal metrics (RSSI, SNR)

## Files in This Skill

- `SKILL.md`: This file - instructions for using the skill
- `view_logs.py`: Helper script for viewing and analyzing logs
