---
name: renode-for-tmnl
description: Renode practices for TMNL with tmux, UART sockets, telemetry, and guardrails.
allowed-tools: [Bash, Read, Write]
---

# Renode for TMNL

## When to Use

- You need Renode setup, UART integration, or telemetry simulation.
- You want a headless tmux workflow with UART and monitor panes.
- You are writing or running `.resc` scripts for Renode.

## Canonical Sources

- Renode UART integration docs (CreateServerSocketTerminal, connector Connect).
- TMNL scripts: `embedded/renode/scripts/renode-init.sh`.
- Renode scripts: `embedded/renode/nrf52840/nrf52840-telemetry.resc`.

## The Only Supported TMNL Path (Current)

```
Renode (headless) -> UART socket (TCP) -> nc (tmux pane) -> telemetry ingest
```

We use TCP UART sockets (not PTY) to allow `nc` everywhere.

## Decision Trees

### UART Exposure

```
Need UART access?
├─ Want nc everywhere?  -> CreateServerSocketTerminal (MANDATORY)
└─ Want PTY tooling?    -> CreateUartPtyTerminal (DO NOT for TMNL)
```

### Renode Launch Mode

```
Running inside tmux?
├─ Yes -> renode-init.sh (MANDATORY)
└─ No  -> renode --disable-gui -e 'i @script.resc' (ALLOWED)
```

## DO NOTs (Strict)

- DO NOT use PTY UART for TMNL. Use TCP sockets + nc.
- DO NOT start Renode with GUI when running in tmux.
- DO NOT rely on ad-hoc commands. Use `.resc` scripts.
- DO NOT mix registries or ports without documenting overrides.

## Guardrails (Mandatory)

- Always pass `--disable-gui` for headless runs.
- Always expose UART with `CreateServerSocketTerminal`.
- Always use `connector Connect <uart> <socket>`.
- Always pin ports in the script (default: 5501).

## Highly Suggested

- Keep Renode in tmux session `tmnl-renode`.
- Keep three windows: `renode`, `uart`, `console`.
- Use `nc` for both UART and monitor.

## Standard Commands

Start headless Renode + UART + monitor in tmux:

```bash
embedded/renode/scripts/renode-init.sh
```

Attach:

```bash
tmux attach -t tmnl-renode
```

UART socket (default):

```bash
nc 127.0.0.1 5501
```

Monitor socket (default):

```bash
nc 127.0.0.1 1234
```

## Pitfalls

- If UART appears silent, ensure firmware is loaded and `connector Connect` is present.
- If `nc` shows no output, check Renode monitor for UART traffic.
- If multiple Renode sessions run, port conflicts will be silent. Use one session.

## Files to Edit

- `embedded/renode/nrf52840/nrf52840-telemetry.resc`
- `embedded/renode/scripts/renode-init.sh`
- `embedded/renode/README.md`
