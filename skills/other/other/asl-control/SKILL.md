---
name: asl-control
description: Monitor and control AllStar Link amateur radio nodes via REST API
metadata: {"openclaw":{"emoji":"📡","requires":{"bins":["python3"],"env":["ASL_PI_IP","ASL_API_KEY"]}}}
---

# AllStar Link Node Control

Control and monitor your AllStar Link node through the ASL Agent REST API.

---

## Prerequisites

This skill is a **client**. It talks to an ASL3 agent backend that must be running independently on a Raspberry Pi (or any host reachable over your network).

**You need:**

- A Raspberry Pi running the `asl-agent` FastAPI service (see `backend/` in this repo for the server code)
- The Pi must be reachable from wherever OpenClaw runs -- Tailscale is the recommended way
- The Pi's `config.yaml` (at `/opt/asl-agent/config.yaml`) contains your API key and node number

**Environment variables** (set in your secrets file, e.g. `~/.config/secrets/api-keys.env`):

- `ASL_PI_IP` -- IP address of the Pi (Tailscale IP preferred, works from anywhere)
- `ASL_API_KEY` -- Bearer token from the Pi's `config.yaml`
- `ASL_API_BASE` -- (optional) override the full base URL if you're not on port 8073. Format: `http://host:port`
- `ASL_STATE_DIR` -- (optional) override where favorites/net state files are stored. Default: `~/.openclaw/state/asl-control/`

---

## Usage

All commands go through the Python client. Always source your secrets first:

```bash
source ~/.config/secrets/api-keys.env
python3 {baseDir}/scripts/asl-tool.py <command> [flags]
```

Every command supports `--out json` (default, machine-readable) or `--out text` (human-readable one-liner).

### Quick reference

```bash
# Status & monitoring
python3 {baseDir}/scripts/asl-tool.py status --out text
python3 {baseDir}/scripts/asl-tool.py nodes --out text
python3 {baseDir}/scripts/asl-tool.py report --out text
python3 {baseDir}/scripts/asl-tool.py audit --lines 20

# Connect / disconnect
python3 {baseDir}/scripts/asl-tool.py connect 55553 --out text
python3 {baseDir}/scripts/asl-tool.py connect 55553 --monitor-only --out text
python3 {baseDir}/scripts/asl-tool.py disconnect 55553 --out text

# Favorites
python3 {baseDir}/scripts/asl-tool.py favorites list
python3 {baseDir}/scripts/asl-tool.py favorites set mynet 55553
python3 {baseDir}/scripts/asl-tool.py favorites remove mynet
python3 {baseDir}/scripts/asl-tool.py connect-fav mynet --out text

# Net profiles (timed sessions, auto-disconnect default)
python3 {baseDir}/scripts/asl-tool.py net list
python3 {baseDir}/scripts/asl-tool.py net set ares 55553 --duration-minutes 90
python3 {baseDir}/scripts/asl-tool.py net start ares --out text
python3 {baseDir}/scripts/asl-tool.py net status --out text
python3 {baseDir}/scripts/asl-tool.py net tick --out text
python3 {baseDir}/scripts/asl-tool.py net stop --out text
python3 {baseDir}/scripts/asl-tool.py net remove ares

# Watch (JSON-line event stream)
python3 {baseDir}/scripts/asl-tool.py watch --interval 5 --emit-initial
```

### State files

Favorites and net session state live outside the repo, so they survive updates:

- `~/.openclaw/state/asl-control/favorites.json`
- `~/.openclaw/state/asl-control/net-profiles.json`
- `~/.openclaw/state/asl-control/net-session.json`

### Net tick (cron)

Auto-disconnect only fires when `net tick` runs. Wire it to cron for enforcement:

```bash
* * * * * /bin/bash -c 'source ~/.config/secrets/api-keys.env && python3 /path/to/asl-tool.py net tick --out text >> ~/.openclaw/state/asl-control/tick.log 2>&1'
```

---

## Natural language dispatch

When the user asks in natural language, translate to the Python client:

- "Check my node" -> `asl-tool.py report --out text`
- "What's connected?" -> `asl-tool.py nodes --out text`
- "Connect to node 55553" -> `asl-tool.py connect 55553 --out text`
- "Connect to node 55553 monitor only" -> `asl-tool.py connect 55553 --monitor-only --out text`
- "Connect to <favorite name>" -> `asl-tool.py connect-fav "<name>" --out text`
- "Disconnect from node 55553" -> `asl-tool.py disconnect 55553 --out text`
- "List my favorites" -> `asl-tool.py favorites list --out text`
- "Start net <name>" -> `asl-tool.py net start <name> --out text`
- "Net status" -> `asl-tool.py net status --out text`
- "Show audit log" -> `asl-tool.py audit --lines 20 --out text`

---

## Notes

- Tailscale IP is preferred over LAN IP for `ASL_PI_IP` (works from anywhere on the mesh)
- Some nodes auto-reconnect after disconnect due to the AllStar scheduler on your node. That's an ASL config behavior, not an API bug. Disable the scheduler first if you need connections to stay dropped.
- All commands are logged to the audit trail on the Pi at `/opt/asl-agent/audit.log`
