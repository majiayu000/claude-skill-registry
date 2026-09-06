---
name: gdb
description: 'Use when running GDB: breakpoints, watchpoints, segfault or hang debugging, reverse debugging, remote gdbserver, core dumps, pretty-printers, Python scripting, or multi-threaded debugging.'
---

# GDB

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A C or C++ program needs a GDB session: breakpoints, watchpoints, stepping, crash or hang diagnosis, reverse debugging, remote debugging with gdbserver, core files, or Python scripting. |
| Authority | Read-only. Emits analysis and commands for the operator to run on the target; no file writes, no rollback needed. No remote mutation. |
| Side effect | Diagnostic commands and a verdict in chat. Nothing is written. |
| Done | The bug is localized to a frame, variable, or instruction, or the next diagnostic step is stated with its reason. |

## Inputs

1. Binary (required): compiled with `-g`; `-Og` or `-O0` gives the most debuggable code.
2. Symptom (required): crash, hang, wrong value, or a question about program state.
3. Core file, PID, or remote target (optional): for post-mortem, attach, or gdbserver workflows.

## Procedure

1. Build with debug info.

   ```bash
   gcc -g -Og -o prog main.c
   ```

   For release builds use `-g -O2` and keep an unstripped copy; split symbols with `objcopy` as in `core-dumps`. Done when: the binary carries debug info.
2. Start the session.

   ```bash
   gdb ./prog                            # load a binary
   gdb ./prog core                       # binary plus core dump
   gdb -p 12345                          # attach to a running process
   gdb --args ./prog arg1 arg2           # pass arguments
   gdb -batch -ex 'run' -ex 'bt' ./prog  # non-interactive, for CI
   ```

   Done when: GDB has a live inferior or a loaded core.
3. Control execution.

   | Command | Shortcut | Effect |
   |---|---|---|
   | `run [args]` | `r` | Start the program |
   | `continue` | `c` | Resume after a stop |
   | `next` | `n` | Step over, source line |
   | `step` | `s` | Step into, source line |
   | `nexti` | `ni` | Step over, one instruction |
   | `stepi` | `si` | Step into, one instruction |
   | `finish` | | Run to the end of the function |
   | `until N` | | Run to line N |
   | `return [val]` | | Force a return from the function |
   | `quit` | `q` | Exit |

   Done when: the program is stopped at the point of interest.
4. Set breakpoints and watchpoints.

   ```gdb
   break main                          # function
   break file.c:42                     # line
   break *0x400abc                     # address
   break foo if x > 10                 # conditional
   tbreak foo                          # fires once
   rbreak ^mylib_.*                    # regex over function names
   catch throw                         # C++ exception
   catch syscall mmap                  # syscall

   watch x                             # break when x is written
   watch *(int*)0x601060               # watch an address
   rwatch x                            # break on read
   awatch x                            # break on read or write

   info breakpoints
   delete 3 / disable 3 / enable 3
   ignore 3 100                        # skip the next 100 hits
   commands 3 ... end                  # run commands on each hit
   ```

   Done when: execution stops at the condition that matters.
5. Inspect state.

   ```gdb
   print x / print/x x                 # value, hex
   print *ptr                          # dereference
   print arr[0]@10                     # ten elements from arr[0]
   display x                           # print on every stop
   info locals / info args
   info registers rip rsp rbp
   x/10wx 0x7fff0000                   # examine memory: count/format/unit
   x/s 0x400abc                        # as string
   x/i $rip                            # current instruction
   backtrace / bt full
   frame 2 / up / down
   ```

   Done when: the variable, register, or memory region in question is read.
6. Debug threads.

   ```gdb
   info threads
   thread 3
   thread apply all bt full
   set scheduler-locking on            # only the current thread runs while stepping
   ```

   Done when: each thread's state is known. For deadlock cycles and race reports, use `concurrency-debugging`.
7. Reverse debug when the bug is easier to catch going backward.

   ```gdb
   (gdb) record                        # software record, slow but universal
   (gdb) run
   (gdb) reverse-continue              # back to the last event
   (gdb) reverse-next / reverse-step / reverse-finish
   (gdb) record btrace                 # hardware branch trace (Intel PT or BTS)
   (gdb) record instruction-history    # replay recorded instructions
   ```

   Done when: the execution history reaches the state before the bug.
8. Debug a remote or embedded target with gdbserver.

   ```bash
   gdbserver :1234 ./prog              # on the target
   gdbserver :1234 --attach 5678       # attach variant
   ```

   ```gdb
   (gdb) target remote 192.168.1.10:1234
   ```

   For cross-compiled targets use the matching GDB, for example `aarch64-linux-gnu-gdb`. Done when: the host GDB controls the target process.
9. Configure `~/.gdbinit` once.

   ```gdb
   set history save on
   set history size 1000
   set print pretty on
   set print array on
   set print array-indexes on
   set pagination off
   set confirm off
   ```

   Done when: the session defaults are set.

For the full command cheatsheet see `references/cheatsheet.md`. For pretty-printers and the Python API see `references/scripting.md`.

## Failure and recovery

| Symptom | Cause | Fix |
|---|---|---|
| `No symbol table` | Built without `-g` | Rebuild with `-g` |
| `??` frames in the backtrace | Missing debug info or stack corruption | Install the debug package; suspect a stack smash |
| `Cannot access memory at address` | Null or freed pointer | Check the pointer; run under ASan |
| `SIGABRT` in the backtrace | `abort()` or a failed assertion | Walk up frames to the check |
| GDB hangs on `run` | Program waits on stdin | `run < /dev/null` |
| Breakpoint lands wrong | Optimizer moved the code | Rebuild with `-Og`, or step with `nexti`; see `debug-optimized-builds` |

## Output

The bug localized to a frame, variable, register, or instruction, with the commands that produced the evidence; or the named blocker (no symbols, no core, unreachable target) with its fix.
