---
name: py-start-local
description: Start Flask server locally for development. Runs server in foreground or background with nohup. Use when starting local Python server for testing or development.
---

# Python Start Local Server

## Overview

Starts a Flask server locally on your development machine for testing and development. Can run in foreground (interactive) or background (persistent) mode.

## When to Use

Invoke this skill when the user:
- Asks to "start the server"
- Wants to "run the Flask app"
- Says "start local server"
- Mentions running the Python server locally
- Wants to test server changes locally

## Prerequisites

- Python 3 installed
- Flask installed: `pip3 install flask`
- Other dependencies installed: `pip3 install -r requirements.txt`
- Server code (app.py) in current directory

## Instructions

### Option 1: Foreground Mode (Development)

1. Navigate to the server directory:
   ```bash
   cd path/to/server/imp/py
   ```

2. Run the Flask app directly:
   ```bash
   python3 app.py
   ```

3. Inform the user:
   - Server running on http://localhost:8080
   - Auto-reload on code changes (if debug=True)
   - Detailed error messages in terminal
   - Press Ctrl+C to stop
   - Terminal must stay open

### Option 2: Background Mode (Persistent)

1. Navigate to the server directory:
   ```bash
   cd path/to/server/imp/py
   ```

2. Run the start script:
   ```bash
   ./start.sh
   ```

3. The script will:
   - Kill any existing server on port 8080
   - Start server with `nohup python3 app.py`
   - Save process ID to `server.pid`
   - Log output to `server.log`
   - Run in background (terminal can close)

4. Inform the user:
   - Server started in background
   - Access at http://localhost:8080 or http://0.0.0.0:8080
   - View logs: `tail -f server.log`
   - Stop with: `./stop.sh` or py-stop-local skill
   - Process ID saved in server.pid

## Expected Output

**Foreground mode**:
```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

**Background mode**:
```
Firefly server started on port 8080
PID: 12345
Logs: tail -f server.log
Stop: ./stop.sh
Access at: http://localhost:8080
```

## Modes Comparison

**Foreground** (python3 app.py):
- ✅ Auto-reload on code changes
- ✅ Detailed error messages
- ✅ Interactive debugger
- ❌ Stops when terminal closes
- ❌ Blocks terminal
- **Use for**: Active development

**Background** (./start.sh):
- ✅ Persists after terminal close
- ✅ Logs to file
- ✅ Easy stop/restart
- ❌ No auto-reload
- ❌ Less visible errors
- **Use for**: Local testing, demos

## Accessing the Server

Once started, access via:
- http://localhost:8080
- http://0.0.0.0:8080
- http://127.0.0.1:8080

From other devices on same network:
- http://YOUR_LOCAL_IP:8080
- Find your IP: `ifconfig | grep "inet " | grep -v 127.0.0.1`

## Flask Configuration

The server typically runs with:
- **Host**: `0.0.0.0` (accepts external connections)
- **Port**: `8080`
- **Debug mode**: `True` (development) or `False` (background)

## Verification

Test the server is running:
```bash
curl http://localhost:8080/api/ping
```

Expected response:
```json
{"message":"Firefly server is running","status":"ok"}
```

## Common Issues

**"Address already in use"**:
```
OSError: [Errno 48] Address already in use
```
- Port 8080 already occupied
- Kill existing process: `lsof -ti:8080 | xargs kill`
- Or use py-stop-local skill first

**"Module not found"**:
```
ModuleNotFoundError: No module named 'flask'
```
- Install Flask: `pip3 install flask`
- Install all deps: `pip3 install -r requirements.txt`

**"Permission denied"**:
- Don't use ports < 1024 without sudo
- Port 8080 should work fine
- Check file permissions on app.py

**Can't access from other devices**:
- Ensure Flask uses `host='0.0.0.0'` not `'127.0.0.1'`
- Check macOS firewall allows Python incoming connections
- Verify devices on same network

## Monitoring Logs

**Foreground mode**:
- Logs appear directly in terminal
- Error stack traces visible immediately

**Background mode**:
- View logs: `tail -f server.log`
- Last 20 lines: `tail -20 server.log`
- Search logs: `grep "ERROR" server.log`

## Stopping the Server

**Foreground mode**:
- Press Ctrl+C in terminal

**Background mode**:
- Use `./stop.sh` script
- Or use py-stop-local skill
- Or kill manually: `lsof -ti:8080 | xargs kill`

## Development Workflow

Typical workflow:
```bash
# Start in foreground for development
python3 app.py

# Make changes to app.py
# Flask auto-reloads (if debug=True)

# Test changes
curl http://localhost:8080/api/ping

# When done, Ctrl+C to stop
```

## start.sh Script Details

The start.sh script:
```bash
# Kill any existing server on port 8080
lsof -ti:8080 | xargs kill -9 2>/dev/null

# Start server in background with nohup
nohup python3 app.py > server.log 2>&1 &

# Save process ID
echo $! > server.pid
```

This ensures clean startup and process tracking.

## Flask Debug Mode

Debug mode (in app.py):
```python
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)
```

- **debug=True**: Auto-reload, detailed errors (development)
- **debug=False**: Stable, minimal output (production/background)

## Notes

- Flask development server is single-threaded
- For production, use gunicorn or similar WSGI server
- localhost vs 0.0.0.0: use 0.0.0.0 to accept external connections
- Port 8080 is standard for development (no sudo required)
