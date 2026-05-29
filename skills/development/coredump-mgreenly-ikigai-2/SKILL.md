---
name: coredump
description: Core Dump Analysis skill for the ikigai project
---

# Core Dump Analysis

## Description
Post-mortem debugging using core dumps for crashes that occur before gdbserver can catch them.

## When to Use

- Crashes during very early startup
- Crashes before gdbserver fully initializes
- When you need to reproduce and analyze offline
- Segfaults, aborts, or other fatal signals

## Enable Core Dumps

```bash
# Enable for current session
ulimit -c unlimited

# Verify
ulimit -c
```

## Generate and Analyze

```bash
# Run until crash
./ikigai
# Produces: core or core.<pid>

# Analyze
gdb ./ikigai core
```

## Key Commands

```gdb
bt                  # Backtrace - where it crashed
bt full             # Backtrace with local variables
frame N             # Select stack frame
info locals         # Variables in current frame
print var           # Inspect variable
list                # Source at crash point
info registers      # CPU state at crash
x/20x $sp           # Examine stack memory
```

## Finding the Core File

```bash
# Check core pattern
cat /proc/sys/kernel/core_pattern

# Common locations
ls -la core*
ls -la /var/crash/
```

## Workflow

1. Enable core dumps: `ulimit -c unlimited`
2. Run app until crash
3. Load core: `gdb ./ikigai core`
4. Get backtrace: `bt full`
5. Inspect frames and variables

## References

- GDB manual: https://sourceware.org/gdb/current/onlinedocs/gdb/
- See `gdbserver.md` for live debugging
