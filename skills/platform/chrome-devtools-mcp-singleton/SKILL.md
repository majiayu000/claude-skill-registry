---
name: chrome-devtools-mcp-singleton
description: Run and manage a single-instance Chrome DevTools MCP server on this machine, including start/stop/status/dedupe workflows and safe cleanup to prevent multiple chrome-devtools-mcp processes from running concurrently. Use when you need a singleton MCP server for Chrome DevTools or when EMFILE/process-spawn issues require enforcing exactly one chrome-devtools-mcp instance.
---

# Chrome DevTools MCP Singleton

Use the bundled script to start/stop the Chrome DevTools MCP server and enforce a single running instance.

## Script

- `scripts/run_chrome_devtools_mcp.sh` (relative to this skill folder, e.g. `~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh`)

## Commands

- Show status (PID + log path):
```bash
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh status
```

- Start (dedupes automatically):

```bash
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh start -- --headless --isolated
```

- Run in foreground with stdio (for MCP clients expecting stdio JSON-RPC):

```bash
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh run -- --headless --isolated
```

- Stop (kills all chrome-devtools-mcp instances):

```bash
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh stop
```

- Dedupe only (keep one, kill extras):

```bash
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh dedupe
```

## Smoke tests

- Server smoke (start/status/dedupe/log check):

```bash
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/mcp-smoke.sh
```

- MCP client smoke (opens 2 pages + reads titles):

```bash
cd ~/.codex/skills/chrome-devtools-mcp-singleton/scripts/mcp-client
npm install
node mcp-client-test.mjs
```

## Common args (pass after `--`)

The MCP server supports flags like `--browserUrl` (connect to a running Chrome), `--headless`, `--executablePath`, `--isolated`, and `--channel`. Use these to control how Chrome is started and which profile is used. See the package docs for full options.

Examples:

```bash
# Use a specific Chrome binary
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh start -- --headless --isolated --executablePath "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# Attach to an already running Chrome instance
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh start -- --browserUrl http://127.0.0.1:9222

# Use a specific Chrome channel (if supported by the MCP server)
~/.codex/skills/chrome-devtools-mcp-singleton/scripts/run_chrome_devtools_mcp.sh start -- --channel stable
```

## Environment variables

- `CHROME_DEVTOOLS_MCP_CMD` (default: `npx -y chrome-devtools-mcp@latest`)
- `CHROME_DEVTOOLS_MCP_ARGS` (space-separated default args)
- `CHROME_DEVTOOLS_MCP_STATE_DIR` (default: `/tmp/chrome-devtools-mcp-singleton`)
- `CHROME_DEVTOOLS_MCP_KEEPALIVE` (default: `1` to keep stdin open for stdio servers)

Common env examples:

```bash
# Always start with defaults (shared across invocations)
export CHROME_DEVTOOLS_MCP_ARGS="--headless --isolated"

# Point to a specific MCP binary or pinned version
export CHROME_DEVTOOLS_MCP_CMD="npx -y chrome-devtools-mcp@0.4.3"

# Use a separate state directory (PID + logs)
export CHROME_DEVTOOLS_MCP_STATE_DIR="/tmp/chrome-devtools-mcp-singleton-alt"

# Disable stdin keepalive (foreground only; background may exit immediately)
export CHROME_DEVTOOLS_MCP_KEEPALIVE=0
```

## Logs & state

- PID file: `${CHROME_DEVTOOLS_MCP_STATE_DIR:-/tmp/chrome-devtools-mcp-singleton}/pid`
- Log file: `${CHROME_DEVTOOLS_MCP_STATE_DIR:-/tmp/chrome-devtools-mcp-singleton}/server.log`

View logs:

```bash
tail -n 200 /tmp/chrome-devtools-mcp-singleton/server.log
```

## Notes

- The script enforces a single instance system-wide by killing extra `chrome-devtools-mcp` processes.
- Use `--isolated` to avoid sharing a persistent Chrome profile between runs.
- `start` keeps stdin open in the background so the MCP server does not exit immediately.
