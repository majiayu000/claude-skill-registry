---
name: wterm
description: "Web terminal server: manage the wterm-server daemon for browser-based shell access (local or remote via Tailscale). This skill should be used when checking wterm status, listing or creating terminal sessions, killing sessions, or managing the wterm LaunchAgent. Trigger on: wterm, web terminal, remote terminal, remote shell, browser terminal, terminal sessions."
argument-hint: [status|list|create|kill <id>|restart]
---

# wterm

Manage the wterm-server daemon — a Node.js service providing browser-based shell access via `@wterm/react` + `node-pty`. Access locally at `https://wterm.localhost` (via portless) or remotely from any tailnet device at `http://<hostname>:3036`.

## Commands

### Check status

```bash
bash ~/.claude/skills/wterm/scripts/status.sh
```

Reports whether the daemon is running, its PID, port, and active session count.

### List sessions

```bash
bash ~/.claude/skills/wterm/scripts/list-sessions.sh
```

Shows all active PTY sessions (id, name, command, PID, client count, last activity).

### Create a session

```bash
bash ~/.claude/skills/wterm/scripts/create-session.sh           # default: zsh
bash ~/.claude/skills/wterm/scripts/create-session.sh claude     # Claude Code
bash ~/.claude/skills/wterm/scripts/create-session.sh /bin/bash  # explicit shell
```

Spawns a new PTY session. Default shell is zsh. Pass `claude` to start a Claude Code session.

### Kill a session

```bash
bash ~/.claude/skills/wterm/scripts/kill-session.sh <session-id>
```

Terminates a session by its hex ID (get IDs from `list-sessions.sh`).

### Restart the daemon

```bash
bash ~/.claude/skills/wterm/scripts/restart.sh
```

Restarts the wterm-server LaunchAgent. All active sessions are lost.

## Architecture

- **Daemon**: `~/daimones/wterm-server/` — TypeScript, node-pty, ws, Vite React SPA
- **Port**: 3036 (bound to `0.0.0.0` for Tailscale access)
- **Auth**: Bearer token from `WTERM_AUTH_TOKEN` in `~/.config/env/secrets.env`. Auth is fail-closed — server rejects all requests if no token is configured.
- **LaunchAgent**: `com.minoan.wterm-server` — RunAtLoad, KeepAlive
- **Logs**: `~/.claude/logs/wterm-server.{out,err}.log`

## Gotchas

- Sessions default to zsh, not Claude Code. Pass `claude` explicitly to create-session.sh.
- The daemon must be running on the host machine. If status shows not running, use `restart.sh` or check `launchctl list | grep wterm`.
- Auth token is required for remote access. If scripts return 401, verify `WTERM_AUTH_TOKEN` is set in `~/.config/env/secrets.env`.
- Restarting the daemon kills all active sessions — the scrollback buffer is in-memory only.
