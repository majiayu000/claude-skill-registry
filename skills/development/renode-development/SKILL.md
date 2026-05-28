---
name: renode-development
description: Day-to-day Renode development workflow for TMNL: .resc edits, firmware swaps, UART verification, and troubleshooting.
model_invoked: true
triggers:
  - "renode dev"
  - "renode development"
  - "renode troubleshoot"
  - "renode uart"
  - "renode monitor"
  - "resc script"
  - "nrf52840"
allowed-tools: [Bash, Read, Write]
---

# Renode Development Workflow (TMNL)

## When to Use

- Editing `.resc` scripts or swapping firmware.
- Debugging UART output or monitor commands.
- Troubleshooting silent telemetry.

## Canonical Sources

- `embedded/renode/nrf52840/nrf52840-telemetry.resc`
- `embedded/renode/scripts/renode-init.sh`
- `embedded/renode/README.md`

## Standard Loop

1. Update `.resc` (firmware path, UART port, or board).
2. Restart Renode via `renode-init.sh`.
3. Verify monitor access (`nc 127.0.0.1 1234`).
4. Verify UART traffic (`nc 127.0.0.1 5501`).

## Pattern 1: Swap Firmware

**When:** You need a different ELF or build.

```text
sysbus LoadELF @path/to/firmware.elf
```

Restart the tmux session after editing:

```bash
tmux kill-session -t tmnl-renode
embedded/renode/scripts/renode-init.sh
```

## Pattern 2: Adjust UART Port

**When:** Port collision or multi-session debugging.

```text
CreateServerSocketTerminal 5501 "uart_socket" false
connector Connect sysbus.uart0 uart_socket
```

Set the matching environment override before launch:

```bash
export TMNL_RENODE_UART_PORT=5501
embedded/renode/scripts/renode-init.sh
```

## Pattern 3: Monitor Commands

**When:** You need control over machine state.

```text
help
machine Start
machine Reset
sysbus.uart0
```

## Pattern 4: Inject Monitor Commands (tmux)

**When:** You need to drive the monitor without switching panes.

```bash
embedded/renode/scripts/renode-send-keys.sh "machine Reset"
embedded/renode/scripts/renode-send-keys.sh "machine Start"
```

## Decision Tree: UART Silence

```
UART silent?
├─ Monitor reachable? -> nc 127.0.0.1 1234
├─ Connector present? -> ensure "connector Connect sysbus.uart0 uart_socket"
└─ Firmware loaded?   -> verify LoadELF path in .resc
```

## DO NOTs (Strict)

- DO NOT use PTY UART terminals. Use TCP sockets + nc.
- DO NOT run Renode with GUI in tmux workflows.
- DO NOT start multiple Renode sessions on the same ports.
- DO NOT bypass `.resc` scripts with manual monitor setup.

## Guardrails (Mandatory)

- Keep `CreateServerSocketTerminal` in every `.resc` script.
- Use `--disable-gui` (handled by `renode-init.sh`).
- Keep UART and monitor ports documented in README.
- Use one tmux session per Renode instance.

## Highly Suggested

- Keep firmware paths relative to `embedded/renode/`.
- Validate the monitor socket before debugging UART.
- Keep a known-good `.resc` for quick rollback.

## Files to Edit

- `embedded/renode/nrf52840/nrf52840-telemetry.resc`
- `embedded/renode/scripts/renode-init.sh`
- `embedded/renode/scripts/renode-send-keys.sh`
- `embedded/renode/README.md`
