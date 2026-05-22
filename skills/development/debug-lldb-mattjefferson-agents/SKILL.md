---
name: debug-lldb
description: Capture and analyze thread backtraces with LLDB/GDB to debug hangs, deadlocks, UI freezes, IPC stalls, or high-CPU loops across any language or project. Use when an app becomes unresponsive, switching contexts stalls, or you need thread stacks to locate lock inversion or blocking calls.
---

# Debug Lldb

## Overview

Capture stack traces from a live process to explain stalls and freezes, then triage for deadlocks, blocking IPC, or tight loops. Prefer repeat sampling so the hang signature is obvious.

## Workflow

### 1) Identify the process

- Use `ps`/`pgrep` to get the PID.
- Prefer the foreground app PID (not the dev server).

### 2) Capture backtraces (fast path)

- Use the bundled script:
  - `scripts/collect_stacks.sh --pid <pid> --out /tmp/hang --repeat 3 --sleep 0.5`
  - Or by name: `scripts/collect_stacks.sh --name "<process-substring>" --out /tmp/hang`
- Run in a separate terminal if the current one is interactive with the hung app.

### 3) Capture backtraces (manual)

- macOS (LLDB):
  - `lldb -p <pid> -o 'thread backtrace all' -o 'detach' -o 'quit' > /tmp/hang.txt 2>&1`
- Linux (GDB):
  - `gdb -q -p <pid> -ex "thread apply all bt" -ex "detach" -ex "quit" > /tmp/hang.txt 2>&1`
- Windows:
  - Use WinDbg or cdb to capture all-thread backtraces.

### 4) Triage the hang

- Compare 3–5 samples taken 0.2–1s apart.
- Use `references/triage.md` for quick pattern matching (deadlock vs busy loop vs blocking I/O).

### 5) Attach context

- Include what action triggered the stall and the exact time window.
- Add relevant app logs around the stall.

## Resources

### scripts/

- `scripts/collect_stacks.sh` - attach to a PID or process name and capture N stack dumps.

### references/

- `references/triage.md` - quick patterns for deadlocks, blocking IPC, and busy loops.
