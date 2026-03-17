---
name: py-deploy-remote
description: Deploy Flask server to remote machine (185.96.221.52). Stops remote server, copies files via scp, restarts server, and verifies. Use when deploying Python server updates to remote Mac mini.
---

# Python Remote Server Deploy

## Overview

Deploys a Flask server application to a remote machine by stopping the running server, copying updated files via scp/ssh, restarting the server, and verifying it's accessible. Designed for the Firefly server running on a Mac mini at 185.96.221.52:8080.

## When to Use

Invoke this skill when the user:
- Asks to "deploy the server"
- Wants to "push server updates"
- Says "deploy to remote" or "deploy to Mac mini"
- Mentions updating the remote Flask server
- Wants to deploy Python server changes

## Prerequisites

- SSH access to remote server configured
- SSH config alias set up in `~/.ssh/config`:
  ```
  Host microserver
      HostName 185.96.221.52
      User microserver
  ```
- Python 3 and Flask installed on remote server
- Remote directory exists: `~/firefly-server/`
- Server is accessible at `http://185.96.221.52:8080`

## Instructions

1. Navigate to the Python server directory:
   ```bash
   cd path/to/server/imp/py
   ```

2. Run the remote deployment (this is a multi-step process):

   **Step 1: Stop the remote server**
   ```bash
   ./remote-shutdown.sh
   ```
   This sends shutdown command to `http://185.96.221.52:8080/api/shutdown`

   **Step 2: Copy updated files**
   ```bash
   scp *.py *.txt *.sh microserver@185.96.221.52:~/firefly-server/
   ```

   **Step 3: Start the server**
   ```bash
   ssh microserver@185.96.221.52 "cd ~/firefly-server && ./start.sh"
   ```

   **Step 4: Verify server is running**
   ```bash
   curl http://185.96.221.52:8080/api/ping
   ```

3. Inform the user:
   - Deployment typically takes 3-5 seconds total
   - Server runs in background with nohup
   - Verify the ping response shows `"status":"ok"`
   - Server accessible at http://185.96.221.52:8080

## Expected Output

```
🛑 Stopping remote server...
Shutdown command sent to server

📦 Copying files to Mac mini...
app.py           100% 1234   1.2MB/s   00:00
requirements.txt 100% 56     56KB/s    00:00
start.sh         100% 391    391KB/s   00:00

✅ Files copied
🚀 Starting server...
Firefly server started on port 8080

🔍 Verifying server...
{"message":"Firefly server is running","status":"ok"}

✅ Deployment complete!
📡 Server running at: http://185.96.221.52:8080
```

## Deployment Steps Explained

**1. Shutdown**:
- Sends POST to `/api/shutdown` endpoint
- Server performs clean shutdown
- Faster than SSH kill command

**2. File Copy**:
- Uses `scp` to transfer all Python, text, and shell files
- SSH config alias (`microserver`) required for automation
- Overwrites existing files on remote

**3. Start Server**:
- SSH into remote machine
- Execute `start.sh` which:
  - Kills any process on port 8080
  - Starts server with `nohup python3 app.py`
  - Saves PID to `server.pid`
  - Logs to `server.log`

**4. Verification**:
- Curls the `/api/ping` endpoint
- Checks for `"ok"` in response
- Confirms server is accessible

## Remote Server Details

- **Host**: 185.96.221.52 (Mac mini on local network)
- **User**: microserver
- **Port**: 8080
- **Directory**: ~/firefly-server/
- **Logs**: ~/firefly-server/server.log
- **PID file**: ~/firefly-server/server.pid

### Database Access

- **PostgreSQL**: localhost:5432 (only accessible via SSH)
- **Database**: firefly
- **Application user**: firefly_user (password: firefly123)
- **Admin user**: microserver (empty password) - for schema changes

**psql is not in PATH** - use full path:
```bash
/opt/homebrew/Cellar/postgresql@16/16.10/bin/psql
```

**Query database via SSH**:
```bash
# As application user
ssh microserver@185.96.221.52 "/opt/homebrew/Cellar/postgresql@16/16.10/bin/psql -U firefly_user -d firefly -c 'SELECT * FROM posts LIMIT 5;'"

# As admin (for schema changes)
ssh microserver@185.96.221.52 "/opt/homebrew/Cellar/postgresql@16/16.10/bin/psql -U microserver -d firefly -c 'ALTER TABLE ...;'"
```

**Run database migrations**:
```bash
ssh microserver@185.96.221.52 "cd ~/firefly-server && python3 migration_script.py"
```

After creating new tables, grant permissions:
```sql
GRANT SELECT ON new_table TO firefly_user;
```

## Common Issues

**"Connection refused" when shutting down**:
- Server may already be stopped (not an error)
- Continue with file copy and restart

**"Permission denied" during scp**:
- Check SSH key authentication is set up
- Verify SSH config alias exists
- Try manual: `ssh microserver@185.96.221.52 "ls ~/firefly-server"`

**Server not responding after restart**:
- Check remote logs: `ssh microserver@185.96.221.52 "tail ~/firefly-server/server.log"`
- Verify Python dependencies: `ssh microserver@185.96.221.52 "pip3 list | grep -i flask"`
- Check port not blocked by firewall

**"Address already in use"**:
- Previous process didn't stop cleanly
- Kill manually: `ssh microserver@185.96.221.52 "lsof -ti:8080 | xargs kill -9"`
- Wait a few seconds and try start.sh again

## SSH Config Setup

If SSH config alias isn't set up, create `~/.ssh/config`:

```
Host microserver
    HostName 185.96.221.52
    User microserver
```

This enables using `microserver` instead of full `user@host` format.

## Speed

- Stop server: <1 second
- Copy files: 1-2 seconds (local network)
- Start server: 1-2 seconds
- Verification: <1 second

**Total**: ~3-5 seconds

## Server Management Commands

After deployment, you can:

**View logs**:
```bash
ssh microserver@185.96.221.52 "tail -f ~/firefly-server/server.log"
```

**Check status**:
```bash
curl http://185.96.221.52:8080/api/ping
```

**Manual restart**:
```bash
ssh microserver@185.96.221.52 "cd ~/firefly-server && ./stop.sh && ./start.sh"
```

## Security Notes

- Server runs without authentication (development only)
- Uses HTTP not HTTPS (local network only)
- `/api/shutdown` endpoint allows remote shutdown
- For production: add authentication, use HTTPS, remove shutdown endpoint

## Typical Use Case

After making changes to Flask server code:
1. Test locally first
2. Deploy to remote with this skill
3. Verify via ping endpoint
4. Test from mobile clients on same network
