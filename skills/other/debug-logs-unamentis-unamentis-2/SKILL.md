---
name: debug-logs
description: Structured debugging workflow with log server capture and analysis
---

# /debug-logs - Log Server Debugging

## Purpose

Provides a structured debugging workflow using the centralized log server. This skill ensures consistent log capture, analysis, and timeline reconstruction for troubleshooting issues.

**Critical Rule:** The log server MUST be running. Without it, debugging is guesswork.

## Usage

```
/debug-logs              # Check log server status and show recent logs
/debug-logs clear        # Clear logs before reproducing an issue
/debug-logs capture      # Clear, wait for reproduction, then analyze
/debug-logs analyze      # Analyze current logs for issues
```

## Log Server Details

- **Port:** 8765
- **Web UI:** http://localhost:8765/
- **Health:** http://localhost:8765/health
- **Logs API:** http://localhost:8765/logs
- **Clear API:** POST http://localhost:8765/clear

## Workflow

### 1. Ensure Log Server Running
```bash
curl -s http://localhost:8765/health
```
If not running, start it:
```bash
python3 scripts/log_server.py &
```

### 2. Clear Logs (for fresh capture)
```bash
curl -s -X POST http://localhost:8765/clear
```
Always clear before reproducing an issue to get clean data.

### 3. Reproduce the Issue
Inform user to reproduce the problem. Wait for them to confirm.

### 4. Fetch Logs
```bash
curl -s http://localhost:8765/logs
```
Returns JSON array of log entries.

### 5. Analyze Logs

**Identify blocking points:**
- Find the last log message before a freeze
- Look for incomplete operations
- Check for error messages

**Timeline reconstruction:**
- Sort by timestamp
- Trace the sequence of events
- Identify where flow stopped

**Pattern detection:**
- Repeated errors
- Performance anomalies
- Missing expected log entries

## Log Entry Format

Each log entry contains:
```json
{
  "timestamp": "2024-01-15T10:30:45.123Z",
  "level": "INFO|WARN|ERROR",
  "source": "component-name",
  "message": "Log message content",
  "metadata": {}
}
```

## Success Criteria

- Log server confirmed running
- Logs captured successfully
- Issue identified with specific log evidence
- Actionable fix identified

## Examples

**Check log server and view logs:**
```
User: /debug-logs
Claude: Checking log server status...

Log server: RUNNING (port 8765)
Log count: 47 entries

Recent logs (last 10):
[10:30:45] INFO  AudioEngine: Starting recording session
[10:30:45] INFO  STTService: Connecting to Deepgram
[10:30:46] INFO  STTService: Connection established
[10:30:47] INFO  AudioEngine: Audio buffer ready
[10:30:48] WARN  LLMService: Response timeout warning
[10:30:49] ERROR LLMService: Connection reset by peer
...
```

**Clear and capture workflow:**
```
User: /debug-logs capture
Claude: Starting log capture workflow...

1. Log server: RUNNING
2. Clearing logs... DONE

Please reproduce the issue now. Let me know when done.

User: Done, the app froze when I tapped the mic button.

Claude: Analyzing captured logs...

Found 23 log entries. Analysis:

BLOCKING POINT IDENTIFIED:
[10:32:15.456] AudioEngine: Requesting microphone permission
[10:32:15.789] AudioEngine: Waiting for permission callback
-- NO FURTHER LOGS --

The app froze waiting for microphone permission callback.

Root cause: Permission prompt may not be showing, or callback never fired.

Suggested investigation:
1. Check if permission prompt appeared
2. Verify AVAudioSession configuration
3. Check for main thread blocking
```

**Analyze specific error pattern:**
```
User: /debug-logs analyze
Claude: Analyzing current logs for issues...

Log entries: 156
Time range: 10:15:00 - 10:45:00

ISSUES DETECTED:

1. REPEATED ERROR (47 occurrences):
   LLMService: Rate limit exceeded
   First: 10:20:15, Last: 10:44:58
   Pattern: Every 30 seconds

2. PERFORMANCE ANOMALY:
   STTService: Response time > 2000ms (12 occurrences)
   Average: 2,450ms (target: <500ms)

3. MISSING EXPECTED LOGS:
   No TTS initialization logs found
   Expected: "TTSService: Initializing with provider..."

Recommendations:
- Check API rate limits and implement backoff
- Investigate STT latency spikes
- Verify TTS service is starting correctly
```

## Debugging Tips

1. **Always clear before capture** - Fresh logs make analysis easier
2. **Check the last log before freeze** - This identifies the blocking operation
3. **Look for ERROR level entries** - Often the direct cause
4. **Trace async operations** - Look for started but never completed
5. **Compare timestamps** - Identify unexpected delays
