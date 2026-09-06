---
name: lldb
description: 'Use when debugging with LLDB on macOS, FreeBSD, or Linux-clang, mapping GDB commands to LLDB, Xcode or VS Code integration, LLDB Python scripting, or debugging Swift and Objective-C.'
---

# LLDB

## Contract

| Field | Bound contract |
|---|---|
| Trigger | A program needs debugging with LLDB on macOS, FreeBSD, or a clang-built Linux tree, a GDB habit needs its LLDB equivalent, or LLDB needs driving from Xcode, VS Code, or Python. |
| Authority | Read-only. Emits analysis and commands for the operator to run on the target; no file writes, no rollback needed. No remote mutation. |
| Side effect | Diagnostic commands and a verdict in chat. Nothing is written. |
| Done | The bug is localized to a frame, variable, or instruction, or the GDB-to-LLDB mapping for the needed command is given. |

## Inputs

1. Binary (required): built with `-g`.
2. Symptom (required): crash, hang, wrong value, or a GDB command that needs its LLDB form.
3. Core file or PID (optional): for post-mortem or attach workflows.

## Procedure

1. Start the session.

   ```bash
   lldb ./prog                      # load a binary
   lldb ./prog -- arg1 arg2         # with arguments
   lldb -p 12345                    # attach to a PID
   lldb -c core.1234                # load a core
   lldb ./prog core.1234            # binary plus core
   ```

   Done when: LLDB has a live process or a loaded core.
2. Map GDB habits to LLDB. The common cases:

   | GDB | LLDB |
   |---|---|
   | `run [args]` | `process launch [args]` / `r` |
   | `continue` | `process continue` / `c` |
   | `next` | `thread step-over` / `n` |
   | `step` | `thread step-in` / `s` |
   | `nexti` | `thread step-inst-over` / `ni` |
   | `stepi` | `thread step-inst` / `si` |
   | `finish` | `thread step-out` / `finish` |
   | `break main` | `breakpoint set -n main` / `b main` |
   | `break file.c:42` | `breakpoint set -f file.c -l 42` / `b file.c:42` |
   | `break *0x400abc` | `breakpoint set -a 0x400abc` / `b -a 0x400abc` |
   | `watch x` | `watchpoint set variable x` / `wa s v x` |
   | `print x` | `frame variable x` / `p x` |
   | `info locals` | `frame variable` / `fr v` |
   | `backtrace` | `thread backtrace` / `bt` |
   | `frame N` | `frame select N` / `f N` |
   | `info threads` | `thread list` |
   | `thread apply all bt` | `thread backtrace all` |
   | `x/10wx addr` | `memory read -s4 -fx -c10 addr` / `x/10xw addr` |
   | `set var = 42` | `expression var = 42` / `expr var = 42` |

   The full map lives in `references/gdb-lldb-map.md`. Done when: the needed command has its LLDB form.
3. Set breakpoints.

   ```lldb
   b main
   breakpoint set --name foo --condition 'x > 0'
   b file.c:42
   breakpoint set --file file.c --line 42
   b -a 0x100003f20                          # address
   breakpoint set --func-regex '^MyClass::'  # regex
   breakpoint set -o -n foo                  # one-shot
   breakpoint list                           # br l
   breakpoint delete 2
   breakpoint disable 1 / breakpoint enable 1
   breakpoint command add 1                  # commands on hit, end with DONE
   ```

   Done when: execution stops at the condition that matters.
4. Inspect state.

   ```lldb
   p x / p *ptr / p arr[0]
   frame variable                     # arguments and locals
   expression x * 2 + 1               # evaluate any expression
   register read / register read rip rsp
   memory read --size 4 --format x --count 10 0x7fff0000
   x/10xw 0x7fff0000                  # GDB-compatible syntax works
   image lookup --type MyClass        # type info
   type lookup MyClass
   ```

   Done when: the variable, register, or memory region in question is read.
5. Set watchpoints.

   ```lldb
   watchpoint set variable x                  # write watchpoint
   watchpoint set variable -w read x          # read watchpoint
   watchpoint set variable -w read_write x
   watchpoint set expression -- &x            # by address
   watchpoint list / watchpoint delete 1
   ```

   Done when: the write or read that corrupts state is trapped.
6. Debug threads.

   ```lldb
   thread list
   thread select 3
   thread backtrace all
   thread backtrace --count 5
   thread step-over                     # steps this thread only
   ```

   Done when: each thread's state is known.
7. Use the Apple-specific surface.

   ```lldb
   image lookup --address 0x18ab12345   # symbol in the shared cache
   image lookup --name objc_msgSend
   b "-[NSArray objectAtIndex:]"        # Objective-C method breakpoint
   po myObject                          # print-object, calls -description
   image list / image list -b           # loaded libraries
   ```

   Done when: Objective-C or shared-cache frames resolve.
8. Drive LLDB from VS Code. Install the CodeLLDB extension and add a `launch.json` configuration:

   ```json
   {
     "name": "Debug (lldb)",
     "type": "lldb",
     "request": "launch",
     "program": "${workspaceFolder}/build/prog",
     "args": [],
     "cwd": "${workspaceFolder}",
     "preLaunchTask": "build"
   }
   ```

   Done when: F5 launches the program under LLDB.
9. Script LLDB with Python.

   ```python
   import lldb

   def print_all_threads(debugger, command, result, internal_dict):
       target = debugger.GetSelectedTarget()
       process = target.GetProcess()
       for thread in process:
           print(f"Thread {thread.GetIndexID()}: {thread.GetName()}")
           for frame in thread:
               print(f"  {frame}")

   def __lldb_init_module(debugger, internal_dict):
       debugger.HandleCommand('command script add -f myscript.print_all_threads pthreads')
   ```

   Load with `command script import /path/to/myscript.py`. Done when: the script command runs inside LLDB.

## Failure and recovery

- `<unavailable>` for a variable: the value was optimized out; see `debug-optimized-builds`.
- A GDB command has no LLDB form: check `references/gdb-lldb-map.md`; where no equivalent exists, the table says so.
- Breakpoint on an Objective-C method misses: quote the full selector, `b "-[Class method:]"`.
- `expression` fails on a function call: the function may be inlined or stripped; call it by address or evaluate the expression manually.
- Core will not load: confirm the binary matches the core; `target create ./prog --core core` needs the exact executable.

## Output

The bug localized to a frame, variable, register, or instruction, with the LLDB commands that produced the evidence; or the GDB-to-LLDB mapping for the command that was asked about.
