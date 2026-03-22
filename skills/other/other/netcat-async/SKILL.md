---
name: netcat-async
description: Maintain bidirectional netcat-style TCP communications with persistent asynchronous input/output. Use when Codex must keep a connection open across multiple commands, send messages while receiving background output, inspect connection logs, or safely start/stop reusable sessions for protocol testing, CTF services, debugging sockets, or interactive line-based services.
---

# OpenCROW I/O - Netcat Async

Prefer the `opencrow-netcat-mcp` server for session lifecycle, reads, and writes. Fall back to `scripts/ncx` only when you need to inspect or debug the backend directly.

## MCP First

- Use `toolbox_info`, `toolbox_verify`, and `toolbox_capabilities` first.
- Use the generic session tools:
  - `session_start`
  - `session_send`
  - `session_read`
  - `session_status`
  - `session_stop`
- Keep one named session per target flow so the MCP server can report stable artifacts under `/tmp/codex-nc-async/<name>/`.

Use `scripts/ncx` to manage long-lived TCP sessions instead of one-shot `nc` invocations when you are operating outside MCP.

## Workflow

1. Start a named session.
2. Send one or more payloads while the daemon keeps receiving output asynchronously.
3. Read logs (`tail` for recent data, `follow` for streaming).
4. Stop the session when done.

## Commands

```bash
# Start session
scripts/ncx start --name demo --host 127.0.0.1 --port 9001

# Send text (append newline for line-oriented protocols)
scripts/ncx send --name demo --data 'ping' --newline

# Read latest output
scripts/ncx read --name demo --tail 40

# Follow output live
scripts/ncx read --name demo --follow

# Check metadata and process state
scripts/ncx status --name demo

# Stop session
scripts/ncx stop --name demo
```

## Operational Rules

- Use one session per target/service flow (`--name` scoped per host+port interaction).
- Prefer `--newline` for interactive text protocols.
- Read with `--tail` before `--follow` to avoid missing context.
- Stop sessions explicitly to avoid stale daemons.
- If `status` reports `running: false`, inspect `daemon.log` and restart.

## Files and State

Session state lives at `/tmp/codex-nc-async/<name>/`:

- `io.log`: timestamped TX/RX events
- `rx.raw`: raw received bytes
- `daemon.log`: daemon stdout/stderr
- `meta.json`: session metadata
- `pid`: daemon PID

## References

- For usage patterns and recovery steps, read `references/patterns.md`.
