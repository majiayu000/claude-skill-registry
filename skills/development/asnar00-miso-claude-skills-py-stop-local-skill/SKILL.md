---
name: py-stop-local
description: Stop local Flask server running on port 8080. Kills process cleanly using lsof or PID file. Use when stopping local Python development server.
---

# Python Stop Local Server

## Overview

Stops a locally running Flask server by killing the process on port 8080. Works for both foreground and background server instances.

## When to Use

Invoke this skill when the user:
- Asks to "stop the server"
- Wants to "kill the Flask app"
- Says "stop local server"
- Mentions shutting down the Python server
- Needs to stop before deploying or restarting

## Prerequisites

- Server must be running on port 8080
- Either a PID file exists (server.pid) or lsof command available
- macOS or Linux system

## Instructions

### Option 1: Using stop.sh Script

1. Navigate to the server directory:
   ```bash
   cd path/to/server/imp/py
   ```

2. Run the stop script:
   ```bash
   ./stop.sh
   ```

3. The script will:
   - Read PID from server.pid file
   - Kill the process
   - Clean up PID file
   - Report success

### Option 2: Manual Stop by Port

If no script available:
```bash
lsof -ti:8080 | xargs kill
```

This finds and kills any process using port 8080.

### Option 3: Foreground Server

If running in foreground mode:
- Press **Ctrl+C** in the terminal

## Expected Output

**Using stop.sh**:
```
🛑 Stopping Firefly server...
✅ Server stopped (PID: 12345)
```

**Manual stop**:
```
# Silent if successful, or:
kill: 12345: No such process (if already stopped)
```

## How It Works

**stop.sh script**:
```bash
if [ -f server.pid ]; then
    PID=$(cat server.pid)
    kill $PID
    rm server.pid
    echo "Server stopped"
else
    # Fallback: kill by port
    lsof -ti:8080 | xargs kill
fi
```

**lsof method**:
- `lsof -ti:8080`: Lists process IDs using port 8080
- `xargs kill`: Pipes PIDs to kill command
- Clean termination (SIGTERM)

## Verification

Check server is stopped:
```bash
# Try to curl - should fail
curl http://localhost:8080/api/ping

# Check port is free
lsof -ti:8080
# (no output = port free)
```

## Common Issues

**"No such process"**:
- Server already stopped (not an error)
- PID file may be stale
- Delete server.pid if it exists

**"Operation not permitted"**:
- Server running as different user
- Try with sudo (not recommended)
- Check process owner: `ps aux | grep python3`

**Port still in use after stop**:
- Process didn't terminate cleanly
- Force kill: `lsof -ti:8080 | xargs kill -9`
- Wait a few seconds for port to free

**server.pid file not found**:
- Server wasn't started with start.sh
- Use manual stop: `lsof -ti:8080 | xargs kill`
- Or kill foreground server with Ctrl+C

## Kill Signals

**SIGTERM** (default `kill`):
- Polite termination request
- Allows cleanup
- Process can catch and handle
- Used by stop.sh

**SIGKILL** (`kill -9`):
- Immediate termination
- No cleanup possible
- Cannot be caught
- Use as last resort

Always try SIGTERM first.

## When to Stop

**Before deploying**:
```bash
./stop.sh
# Make changes
./start.sh
```

**Before testing different port**:
```bash
./stop.sh
# Edit app.py to use different port
python3 app.py
```

**Before remote deployment**:
```bash
./stop.sh  # Stop local
# Deploy to remote with py-deploy-remote
```

**When switching modes**:
```bash
# Stop background server
./stop.sh
# Start foreground for debugging
python3 app.py
```

## Port Conflicts

If port 8080 is used by another app:

**Find what's using port**:
```bash
lsof -i:8080
```

**Output shows**:
```
COMMAND  PID   USER   FD   TYPE DEVICE SIZE/OFF NODE NAME
python3  12345 user   3u  IPv4  0x...  0t0  TCP *:8080 (LISTEN)
```

**Kill specific process**:
```bash
kill 12345
```

## Cleanup

The stop script cleans up:
- Terminates Python process
- Removes server.pid file
- Frees port 8080

Logs (server.log) are preserved for review.

## Safe to Call Repeatedly

This operation is idempotent:
- Safe to call if server already stopped
- Won't error on missing PID
- Graceful failure on no process found

## Integration with Other Skills

**Restart workflow**:
1. py-stop-local
2. Make code changes
3. py-start-local

**Deploy workflow**:
1. py-stop-local (local server)
2. py-deploy-remote (to production)
3. py-start-local (resume local development)

## Alternative: Process Manager

For production, use a process manager:
- **supervisord**: Automatic restart, logging
- **systemd**: System-level service
- **pm2**: Node.js-based process manager

But for development, manual start/stop is simpler.

## Notes

- Only stops server on current machine
- Does not affect remote deployments
- Port 8080 becomes available immediately after stop
- Logs remain in server.log for review
- PID file is automatically cleaned up
