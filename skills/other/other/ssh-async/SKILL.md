---
name: ssh-async
description: Maintain persistent asynchronous SSH sessions with bidirectional input/output across multiple commands. Use when Codex must keep an SSH shell open, send commands incrementally, inspect prompts or streamed output, reuse one authenticated connection for a task, or safely start/stop a long-lived remote session for debugging, administration, deployment, log inspection, or interactive line-based workflows on remote hosts.
---

# OpenCROW I/O - SSH Async

Prefer the `opencrow-ssh-mcp` server for session lifecycle, reads, and writes. Fall back to `scripts/sshx` only when you need to inspect or debug the backend directly.

## MCP First

- Use `toolbox_info`, `toolbox_verify`, and `toolbox_capabilities` first.
- Use the generic session tools:
  - `session_start`
  - `session_send`
  - `session_read`
  - `session_status`
  - `session_stop`
- Keep one named session per host/task flow so the MCP server can return stable artifacts under `/tmp/codex-ssh-async/<name>/`.

Use `scripts/sshx` to manage long-lived SSH sessions instead of one-shot `ssh` invocations when you are operating outside MCP.

## Workflow

1. Start a named session to a remote host.
2. Send shell input while the daemon keeps receiving remote output asynchronously.
3. Read logs with `--tail` for recent context or `--follow` for streaming output.
4. Stop the session explicitly when done.

## Commands

```bash
# Start an interactive login shell
scripts/sshx start --name demo --host 10.0.0.5 --user ubuntu

# Start with a specific identity file and port
scripts/sshx start --name prod --host prod.example.com --user deploy --port 2222 \
  --identity ~/.ssh/deploy_ed25519

# Send a command to the open shell
scripts/sshx send --name prod --data 'uname -a' --newline

# Read recent output
scripts/sshx read --name prod --tail 60

# Follow output live
scripts/sshx read --name prod --follow

# Inspect metadata and process state
scripts/sshx status --name prod

# Stop the session
scripts/sshx stop --name prod
```

## Operational Rules

- Use one session per host/task flow so prompts, working directory, and shell state stay coherent.
- Prefer key-based authentication. The helper runs `ssh` in batch mode and will fail fast instead of hanging on password prompts.
- Append `--newline` for normal shell commands.
- Read with `--tail` before `--follow` so prompt/output context is visible first.
- Stop sessions explicitly to avoid leaving remote shells running.
- If `status` reports `running: false`, inspect `daemon.log` and `io.log` before restarting.

## Files and State

Session state lives at `/tmp/codex-ssh-async/<name>/`:

- `io.log`: timestamped TX/RX events with escaped control characters
- `rx.raw`: raw PTY output bytes from the SSH session
- `daemon.log`: daemon stdout/stderr and launcher failures
- `meta.json`: target metadata and SSH arguments
- `pid`: daemon PID

## Limitations

- This tool is designed for line-oriented shell workflows, not full-screen TUIs such as `vim`, `top`, or `less`.
- Password, OTP, and passphrase prompts are not supported because the session daemon is intentionally non-interactive during startup.
- If the remote command disables prompts or uses unusual terminal control sequences, inspect `rx.raw` in addition to `io.log`.

## References

- For usage patterns and recovery steps, read `references/patterns.md`.
