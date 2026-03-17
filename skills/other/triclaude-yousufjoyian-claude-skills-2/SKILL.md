---
name: triclaude
description: Pull, sync, and launch TriClaude - the multi-terminal console with Claude voice advisor. Provides localhost and Tailscale URLs.
---

# TriClaude Manager

This skill manages the TriClaude application - pulling latest code, syncing to runtime, ensuring services are running, and providing access URLs.

## Quick Reference

| Component | Location |
|-----------|----------|
| Git Repo | `/home/yousuf/local_workspaces/triclaude` |
| Runtime Cache | `/home/yousuf/dev/cache/triclaude` |
| Launch Script | `/home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/launch_triclaude.sh` |
| Desktop Shortcut | `/home/yousuf/Desktop/TriClaude.desktop` |
| GitHub | `yousufjoyian/triclaude` |

## Ports

| Service | Port |
|---------|------|
| Web UI (Vite) | 3001 |
| Project API | 7690 |
| Consigliere | 7695 |
| WS Relay | 7899 |
| Command Bridge | 8765 (legacy) |
| Dynamic Terminals (ttyd) | 7700+ |

## Shortcut Bar

The shortcut bar sends commands to ttyd terminals via WebSocket relay (port 7899).

**How it works:**
1. Click on a terminal panel to make it "active" (green indicator)
2. Press any shortcut button to send to that terminal
3. Yellow indicator = no terminal selected yet

**Available shortcuts:**
| Button | Action | Value |
|--------|--------|-------|
| 2 | Keypress | Sends "2" |
| ESC | Keypress | Escape key |
| UT | Text | "ultrathink" |
| ⏎ (Enter) | Keypress | Enter/Return |
| Y | Text | "yes" |
| C | Text | "continue" |
| Commit | Text | "commit" |
| Context | Text | "extract context" |

**Technical:** Uses `ttydService.ts` which connects via WebSocket relay at `ws://<host>:7899/relay/<ttydPort>`. The relay server (`ws_relay.py`) forwards to `ws://127.0.0.1:<ttydPort>/ws` to bypass origin restrictions.

## When to Use This Skill

Trigger phrases:
- "pull triclaude"
- "update triclaude"
- "start triclaude"
- "triclaude status"
- "launch triclaude"

## What This Skill Does

1. **Pull latest** from GitHub to `/home/yousuf/local_workspaces/triclaude`
2. **Sync to cache** via rsync to `/home/yousuf/dev/cache/triclaude`
3. **Check services** - verify all 4 services are running
4. **Start missing services** if needed
5. **Provide URLs** for localhost and Tailscale access

## Execution Steps

### Step 1: Pull Latest from GitHub

```bash
cd /home/yousuf/local_workspaces/triclaude && git pull
```

### Step 2: Sync to Runtime Cache

```bash
rsync -av --exclude=node_modules --exclude=package-lock.json --exclude=dist --exclude=.git /home/yousuf/local_workspaces/triclaude/ /home/yousuf/dev/cache/triclaude/
```

### Step 3: Check Running Services

```bash
# Check all services
curl -s http://localhost:7690/api/health > /dev/null && echo "Project API: UP" || echo "Project API: DOWN"
ss -tlnp 2>/dev/null | grep -q ":7695" && echo "Consigliere: UP" || echo "Consigliere: DOWN"
ss -tlnp 2>/dev/null | grep -q ":8765" && echo "Bridge: UP" || echo "Bridge: DOWN"
curl -s http://localhost:3001 > /dev/null && echo "Web UI: UP" || echo "Web UI: DOWN"
```

### Step 4: Start Missing Services (if needed)

If services are down, either:
- Tell user to restart via desktop shortcut, OR
- Start individual services:

```bash
# Project API
python3 /home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/project_api.py &

# Consigliere
nix-shell -p python312Packages.websockets --run \
  "python3 /home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/consigliere_server.py" &

# Command Bridge
nix-shell -p python312Packages.websockets --run \
  "python3 /home/yousuf/local_workspaces/triclaude/bridge/command_server.py" &

# Web UI (from cache dir)
cd /home/yousuf/dev/cache/triclaude && npx vite --port 3001 --host &
```

### Step 5: Get Tailscale IP

```bash
ip -4 addr show tailscale0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}'
```

### Step 6: Provide Access URLs

After all steps, output:

```
TriClaude v4.1 Ready

Localhost:
  http://localhost:3001

Android (Tailscale):
  http://<TAILSCALE_IP>:3001

Services:
  Project API:   http://localhost:7690  [UP/DOWN]
  Consigliere:   ws://localhost:7695    [UP/DOWN]
  Bridge:        ws://localhost:8765    [UP/DOWN]
  Web UI:        http://localhost:3001  [UP/DOWN]
```

## Full Automated Script

Run all steps in sequence:

```bash
#!/bin/bash
echo "=== TriClaude Pull & Sync ==="

# 1. Pull latest
echo "[1/5] Pulling latest from GitHub..."
cd /home/yousuf/local_workspaces/triclaude && git pull

# 2. Sync to cache
echo "[2/5] Syncing to runtime cache..."
rsync -av --exclude=node_modules --exclude=package-lock.json --exclude=dist --exclude=.git /home/yousuf/local_workspaces/triclaude/ /home/yousuf/dev/cache/triclaude/ >/dev/null 2>&1

# 3. Rebuild (production mode - no hot reload)
echo "[3/5] Rebuilding production bundle..."
cd /home/yousuf/dev/cache/triclaude && npx vite build > /dev/null 2>&1
echo "  Build complete. Refresh browser to see changes."

# 4. Check services
echo "[4/5] Checking services..."
API_UP=$(curl -s http://localhost:7690/api/health > /dev/null 2>&1 && echo "UP" || echo "DOWN")
CONSIGLIERE_UP=$(ss -tlnp 2>/dev/null | grep -q ":7695" && echo "UP" || echo "DOWN")
BRIDGE_UP=$(ss -tlnp 2>/dev/null | grep -q ":8765" && echo "UP" || echo "DOWN")
WEB_UP=$(curl -s http://localhost:3001 > /dev/null 2>&1 && echo "UP" || echo "DOWN")

# 5. Get Tailscale IP
TAILSCALE_IP=$(ip -4 addr show tailscale0 2>/dev/null | grep -oP '(?<=inet\s)\d+(\.\d+){3}' || echo "not connected")

# Output
echo ""
echo "[5/5] Status Report"
echo "========================================"
echo "  TriClaude v4.1"
echo "========================================"
echo ""
echo "Access URLs:"
echo "  Localhost:  http://localhost:3001"
echo "  Android:    http://$TAILSCALE_IP:3001"
echo ""
echo "Services:"
echo "  Project API:   $API_UP"
echo "  Consigliere:   $CONSIGLIERE_UP"
echo "  Bridge:        $BRIDGE_UP"
echo "  Web UI:        $WEB_UP"
echo ""

if [ "$API_UP" = "DOWN" ] || [ "$WEB_UP" = "DOWN" ]; then
  echo "WARNING: Some services are down."
  echo "Restart via: Desktop shortcut 'TriClaude'"
fi
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Services down | Use desktop shortcut to restart all |
| Code not updating | Check rsync ran, rebuild with `npx vite build`, refresh browser |
| Tailscale not connected | Run `sudo tailscale up` |
| Bridge offline | Start manually with nix-shell command above |
| Terminal won't connect | Add a project first, then launch Claude/Terminal |

## Architecture

```
GitHub (yousufjoyian/triclaude)
    ↓ git pull
local_workspaces/triclaude (git repo, source of truth)
    ↓ rsync
dev/cache/triclaude (runtime, build here → serve dist/)
    ↓
Browser → localhost:3001 or Tailscale:3001
```

## Related Files

- Launch script: `/home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/launch_triclaude.sh`
- Project API: `/home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/project_api.py`
- Consigliere: `/home/yousuf/GoogleDrive/PROJECTS/APPS/TriClaude/scripts/consigliere_server.py`
- Bridge: `/home/yousuf/local_workspaces/triclaude/bridge/command_server.py`
- Desktop shortcut: `/home/yousuf/Desktop/TriClaude.desktop`
