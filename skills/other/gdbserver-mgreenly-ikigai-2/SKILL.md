---
name: gdbserver
description: GDB Server skill for the ikigai project
---

# GDB Server

## Description
Remote debugging with gdbserver for TUI apps that use alternate screen buffer.

## Why gdbserver

This app uses the alternate terminal buffer. Running GDB directly would conflict with the TUI. gdbserver separates the debugger from the application's terminal.

## Workflow

Terminal 1 - Start app under gdbserver:
```bash
gdbserver :1234 ./ikigai
```

Terminal 2 - Connect with GDB:
```bash
gdb ./ikigai -ex "target remote :1234"
```

## Key Commands

```gdb
bt                  # Backtrace
frame N             # Select stack frame
info locals         # Local variables
print var           # Inspect variable
list                # Source at current location
break file:line     # Set breakpoint
continue            # Resume execution
step / next         # Step into / over
```

## When Crashes Occur

gdbserver keeps the crashed process frozen. Connect and inspect:
```bash
gdb ./ikigai -ex "target remote :1234"
(gdb) bt            # See crash location
(gdb) info registers
(gdb) print *ptr    # Inspect state at crash
```

## Limitations

- TUI output not visible (process attached to gdbserver)
- Very early crashes may need coredump analysis instead
- Inspect internal state via variables, not screen output

## References

- GDB manual: https://sourceware.org/gdb/current/onlinedocs/gdb/
- See `coredump.md` for early crash debugging
