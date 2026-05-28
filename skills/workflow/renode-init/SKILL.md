---
name: renode-init
description: Headless tmux launch workflow for Renode in TMNL. Invoke when starting or restarting Renode sessions, UART sockets, or monitor panes.
model_invoked: true
triggers:
  - 'renode init'
  - 'renode-init'
  - 'renode tmux'
  - 'tmux renode'
  - 'headless renode'
  - 'uart socket'
allowed-tools: [Bash, Read, Write]
---

# Renode Init Workflow (TMNL)

## When to Use

- Starting Renode headless with tmux.
- Recreating or reattaching a Renode session.
- Ensuring UART and monitor sockets are wired.

## Canonical Sources

- `embedded/renode/scripts/renode-init.sh`
- `embedded/renode/nrf52840/nrf52840-telemetry.resc`
- `embedded/renode/README.md`

## Mandatory Flow

1. Start the tmux session:

```bash
embedded/renode/scripts/renode-init.sh
```

2. Attach to the session:

```bash
tmux attach -t tmnl-renode
```

3. Verify sockets:

```bash
nc 127.0.0.1 1234
nc 127.0.0.1 5501
```

## Decision Trees

### Session Creation

```
Need a Renode session?
├─ tmux session exists? -> tmux attach -t tmnl-renode
└─ no session           -> renode-init.sh
```

### UART Port Override

```
Need a non-default UART port?
├─ Yes -> set TMNL_RENODE_UART_PORT before renode-init.sh
└─ No  -> use default 5501
```

## Environment Overrides

```bash
export TMNL_RENODE_SESSION=tmnl-renode
export TMNL_RENODE_SCRIPT=embedded/renode/nrf52840/nrf52840-telemetry.resc
export TMNL_RENODE_UART_PORT=5501
export TMNL_RENODE_MONITOR_ADDR=127.0.0.1:1234
```

## DO NOTs (Strict)

- DO NOT use PTY UART terminals. Use TCP sockets + nc.
- DO NOT launch Renode GUI when running in tmux.
- DO NOT start multiple Renode tmux sessions.
- DO NOT change ports without updating nc and docs.

## Guardrails (Mandatory)

- Use `--disable-gui` (script handles this).
- Keep `CreateServerSocketTerminal` in the `.resc` script.
- Keep three windows: `renode`, `uart`, `console`.
- Keep a single session name: `tmnl-renode`.

## Highly Suggested

- Kill a stale session before restart:

```bash
tmux kill-session -t tmnl-renode
```

- Use `TMNL_RENODE_SCRIPT` when switching `.resc` files.
- Keep scripts and firmware paths under `embedded/renode/`.

## Quick Commands

```bash
embedded/renode/scripts/renode-init.sh
tmux attach -t tmnl-renode
tmux kill-session -t tmnl-renode
```

## Files to Edit

- `embedded/renode/scripts/renode-init.sh`
- `embedded/renode/nrf52840/nrf52840-telemetry.resc`
- `embedded/renode/README.md`
