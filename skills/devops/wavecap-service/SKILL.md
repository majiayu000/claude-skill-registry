---
name: wavecap-service
description: Manage WaveCap as a macOS service. Use when the user wants to start, stop, restart the service, check service status, view service logs, or manage the launchd configuration.
---

# WaveCap Service Management Skill

Use this skill to manage WaveCap as a macOS Launch Agent service.

## Service Configuration

- **Plist location**: `~/Library/LaunchAgents/com.wavecap.server.plist`
- **Service name**: `com.wavecap.server`
- **Logs**: `~/Library/Logs/wavecap-server.log` and `wavecap-server-error.log`

## Service Status

Check if the service is running:

```bash
launchctl list | grep wavecap
```

Output format: `PID  EXIT_CODE  LABEL`
- If PID is a number and EXIT_CODE is `0`: service is running
- If PID is `-` and EXIT_CODE is non-zero: service exited with error

Quick status check:

```bash
launchctl list com.wavecap.server 2>/dev/null && echo "Service is loaded" || echo "Service is not loaded"
```

## Start Service

Load and start the service:

```bash
launchctl load ~/Library/LaunchAgents/com.wavecap.server.plist
```

## Stop Service

Unload and stop the service:

```bash
launchctl unload ~/Library/LaunchAgents/com.wavecap.server.plist
```

## Restart Service

Stop then start:

```bash
launchctl unload ~/Library/LaunchAgents/com.wavecap.server.plist && launchctl load ~/Library/LaunchAgents/com.wavecap.server.plist
```

## View Logs

### Recent stdout (application logs):

```bash
tail -50 ~/Library/Logs/wavecap-server.log
```

### Recent stderr (errors):

```bash
tail -50 ~/Library/Logs/wavecap-server-error.log
```

### Follow logs in real-time:

```bash
tail -f ~/Library/Logs/wavecap-server.log
```

### Check for errors:

```bash
grep -i error ~/Library/Logs/wavecap-server-error.log | tail -20
```

## Verify Server is Responding

After starting, verify the server is healthy:

```bash
curl -s http://localhost:8000/api/health | jq
```

Expected: `{"status": "ok"}`

## Troubleshooting

### Service Won't Start

1. Check error log:
   ```bash
   cat ~/Library/Logs/wavecap-server-error.log
   ```

2. Verify plist syntax:
   ```bash
   plutil -lint ~/Library/LaunchAgents/com.wavecap.server.plist
   ```

3. Try running manually to see errors:
   ```bash
   /Users/thw/Projects/WaveCap/backend/.venv/bin/python -m wavecap_backend
   ```

### Service Keeps Restarting

Check exit codes in error log. Common issues:
- Missing dependencies (ffmpeg not in PATH)
- Port 8000 already in use
- Configuration errors

Find what's using port 8000:
```bash
lsof -i :8000
```

### View Plist Configuration

```bash
cat ~/Library/LaunchAgents/com.wavecap.server.plist
```

### Clear Logs

```bash
: > ~/Library/Logs/wavecap-server.log
: > ~/Library/Logs/wavecap-server-error.log
```

## Service Behavior

- **RunAtLoad**: Starts automatically when you log in
- **KeepAlive**: Automatically restarts if it crashes
- **WorkingDirectory**: `/Users/thw/Projects/WaveCap/backend`

## Disable Auto-Start

To stop the service from starting on login (but keep the plist):

```bash
launchctl unload -w ~/Library/LaunchAgents/com.wavecap.server.plist
```

To re-enable:

```bash
launchctl load -w ~/Library/LaunchAgents/com.wavecap.server.plist
```

## Remove Service Completely

```bash
launchctl unload ~/Library/LaunchAgents/com.wavecap.server.plist
rm ~/Library/LaunchAgents/com.wavecap.server.plist
```

## Convert to Launch Daemon (System-Wide)

To run at boot (even without user login), convert to a Launch Daemon:

```bash
# Stop agent
launchctl unload ~/Library/LaunchAgents/com.wavecap.server.plist

# Move to system location
sudo mv ~/Library/LaunchAgents/com.wavecap.server.plist /Library/LaunchDaemons/

# Set permissions
sudo chown root:wheel /Library/LaunchDaemons/com.wavecap.server.plist
sudo chmod 644 /Library/LaunchDaemons/com.wavecap.server.plist

# Load daemon
sudo launchctl load /Library/LaunchDaemons/com.wavecap.server.plist
```

Note: The plist may need a `UserName` key added to run as your user instead of root.
