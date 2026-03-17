---
name: mrc-monitor
description: Real-time token monitoring for MRC canteen order system. Monitors Firebase Firestore for token status and notifies when orders are ready. Use when user sends commands like "mrc 73", "token 97", or "monitor 42" to monitor one or multiple canteen tokens. Handles multiple tokens simultaneously, sends independent notifications per token, and auto-exits when all tokens are ready.
---

# MRC Canteen Monitor

Monitor MRC canteen order tokens and notify when they're ready for pickup.

## Quick Start

When user sends any command containing canteen tokens:

1. Extract all token numbers from the message
2. Start the background monitor script
3. Respond immediately with confirmation

## Command Recognition

Users may send tokens with various prefixes:
- "mrc 73" or "mrc 73 97 42"
- "token 73" or "token 73 97"
- "monitor 73"
- "check 73" (one-time check only)

## Starting the Monitor

Extract all numbers from the user message and start the background monitor:

```bash
python3 skills/mrc-monitor/scripts/monitor.py <platform> <channel_id> <token1> <token2> ...
```

Where:
- `platform`: "telegram" or "discord"
- `channel_id`: Current channel identifier (platform prefix is optional, e.g., `telegram_123` or `123` both work)
- `token1`, `token2`, ...: Token numbers to monitor

Example:
```bash
python3 skills/mrc-monitor/scripts/monitor.py telegram telegram_6046286675 73 97 42
# or
python3 skills/mrc-monitor/scripts/monitor.py telegram 6046286675 73 97 42
```

## Background Execution

Start the monitor as a background process so the agent responds immediately:

```python
import subprocess

# channel_id can be with or without platform prefix (both work)
cmd = ['python3', 'skills/mrc-monitor/scripts/monitor.py',
       platform, channel_id] + [str(t) for t in tokens]
subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
```

## Agent Response

After starting the monitor, respond immediately with:

```
✅ Monitoring tokens: 73, 97, 42
Checking every 15 seconds.
I'll notify you here when they're ready! 🍕
```

## One-Time Check

For "check 73" commands, perform a single Firebase query and respond with status without starting a background monitor.

## Monitor Behavior

The monitor script:
- Polls Firebase Firestore every 15 seconds
- Checks all monitored tokens in each poll
- Sends "🍕 Order X is ready!" notification when a token's status is "Ready"
- Removes notified tokens from the watch list
- Exits automatically when all tokens are notified
- Handles errors gracefully with retries
- Logs all activity to `skills/mrc-monitor/logs/monitor_YYYYMMDD_HHMMSS.log`

## Error Handling

The script automatically handles:
- Network timeouts (retries up to 5 times)
- HTTP errors (including rate limits)
- Unexpected errors (stops after 5 consecutive failures)
- Signal termination (SIGTERM, SIGINT)

On fatal errors, the script sends a notification before exiting.

## Firebase Details

- **Project**: kanteen-mrc-blr-24cfa
- **Collection**: orders
- **Document fields**:
  - `studentId` (string): "student-{token_number}"
  - `status` (string): "Preparing", "Ready", "Completed"
