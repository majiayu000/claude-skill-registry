---
name: senses
description: Monitor satellite services and sense events. Check service status, view logs, trigger manual runs, or diagnose issues. Trigger words: senses, satellites, services, watchers, bluesky, github, location.
context: fork
allowed-tools:
  - Bash
  - Read
  - Grep
  - Glob
---

# Satellite Senses Monitor

Monitor the background services that extend the organism's sensory capabilities.

## Service Inventory

| Service | launchd Label | Port | Purpose |
|---------|---------------|------|---------|
| bluesky-watcher | com.claude.bluesky-watcher | — | Poll Bluesky for mentions, follows, replies |
| github-watcher | com.claude.github-watcher | — | Poll GitHub for notifications |
| location-receiver | co.organelle.location-receiver | 8081 | Receive GPS from Overland app |
| mcp-memory-bridge | com.claude.memory-bridge | 8765 | MCP interface for Claude Desktop/Web |

## Quick Status Check

Run these commands to check satellite health:

```bash
# Check which launchd services are loaded
launchctl list | grep -E "claude|organelle" | grep -v "^-.*78"

# Check for running satellite processes
pgrep -fl "bluesky-watcher\|github-watcher\|location.*server\|memory-bridge" || echo "No satellite processes running"

# Check listening ports (location-receiver: 8081, memory-bridge: 8765)
lsof -i :8081 -i :8765 2>/dev/null | grep LISTEN || echo "No satellites listening on ports"

# Check for pending sense events (should be empty if Samara is processing)
ls ~/.claude-mind/senses/*.event.json 2>/dev/null || echo "No pending events"
```

## Service Status Details

### Bluesky Watcher
```bash
# Check launchd status
launchctl list com.claude.bluesky-watcher 2>/dev/null || echo "Not loaded"

# View recent logs
tail -20 ~/.claude-mind/logs/bluesky-watcher.log 2>/dev/null || echo "No log file"

# Check last run time
grep "Bluesky watcher complete" ~/.claude-mind/logs/bluesky-watcher.log | tail -1
```

### GitHub Watcher
```bash
# Check launchd status
launchctl list com.claude.github-watcher 2>/dev/null || echo "Not loaded"

# View recent logs
tail -20 ~/.claude-mind/logs/github-watcher.log 2>/dev/null || echo "No log file"

# Check last run time
grep "GitHub watcher complete" ~/.claude-mind/logs/github-watcher.log | tail -1
```

### Location Receiver
```bash
# Check if listening on port 8081
lsof -i :8081 2>/dev/null | grep LISTEN && echo "Running" || echo "Not running"

# View recent logs
tail -20 ~/.claude-mind/logs/location-receiver.log 2>/dev/null || echo "No log file"
```

### MCP Memory Bridge
```bash
# Check if listening on port 8765
lsof -i :8765 2>/dev/null | grep LISTEN && echo "Running" || echo "Not running"

# View recent logs
tail -20 ~/.claude-mind/logs/memory-bridge.log 2>/dev/null || echo "No log file"
```

## Manual Trigger

Run a watcher immediately instead of waiting for the 15-minute launchd interval:

### Run Bluesky Watcher Now
```bash
/Users/claude/Developer/samara-main/services/bluesky-watcher/venv/bin/python \
  /Users/claude/Developer/samara-main/services/bluesky-watcher/server.py
```

### Run GitHub Watcher Now
```bash
python3 /Users/claude/Developer/samara-main/services/github-watcher/server.py
```

## Recent Sense Events

View events recently processed by Samara:

```bash
# Events processed today
grep -i "SenseRouter\|sense event" ~/.claude-mind/logs/samara.log | grep "$(date +%Y-%m-%d)" | tail -20

# Any errors in sense processing
grep -i "error.*sense\|sense.*error" ~/.claude-mind/logs/samara.log | tail -10
```

## Troubleshooting

### Service Not Running
```bash
# Reload a launchd service
launchctl unload ~/Library/LaunchAgents/com.claude.SERVICE.plist 2>/dev/null
launchctl load ~/Library/LaunchAgents/com.claude.SERVICE.plist

# Or restart manually
# For bluesky-watcher (requires venv):
/Users/claude/Developer/samara-main/services/bluesky-watcher/venv/bin/python \
  /Users/claude/Developer/samara-main/services/bluesky-watcher/server.py

# For github-watcher:
python3 /Users/claude/Developer/samara-main/services/github-watcher/server.py
```

### Events Not Processing
```bash
# Check if Samara is running
pgrep -fl Samara || echo "Samara not running - start it: open /Applications/Samara.app"

# Check SenseDirectoryWatcher status
grep "SenseDirectoryWatcher" ~/.claude-mind/logs/samara.log | tail -5

# Verify senses directory exists
ls -la ~/.claude-mind/senses/
```

### Missing Dependencies
```bash
# Bluesky watcher needs atproto in venv
ls /Users/claude/Developer/samara-main/services/bluesky-watcher/venv/bin/python || \
  echo "venv missing - create with: python3 -m venv venv && ./venv/bin/pip install atproto"

# GitHub watcher needs gh CLI authenticated
gh auth status
```

## Output Format

When reporting status, use this format:

**Satellites:**
- **bluesky-watcher**: Running/Loaded | Last run: [timestamp] | [OK/Issues found]
- **github-watcher**: Running/Loaded | Last run: [timestamp] | [OK/Issues found]
- **location-receiver**: Listening :8081 / Not running
- **mcp-memory-bridge**: Listening :8765 / Not running

**Recent Events:** [count] events processed today
**Pending Events:** [count] or "None"

## Guidelines

- Satellites are optional extensions — degraded mode is OK
- Polling watchers (bluesky, github) run every 15 minutes via launchd
- HTTP services (location, memory-bridge) run continuously
- Event files in `~/.claude-mind/senses/` are deleted after processing
- Check Samara logs for sense routing issues, service logs for fetch issues
