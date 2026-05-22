---
name: opencrow-pwn-toolbox
description: Use the Anaconda `ctf` environment and installed exploit tooling for binary exploitation and runtime-debugging tasks. Use when Codex needs `pwntools`, `pwndbg`, `gdb`, `checksec`, `patchelf`, `qemu-user`, `pwninit`, or other pwn-focused helpers.
---

# OpenCROW Pwn Toolbox

Prefer the `opencrow-pwn-mcp` server for typed ELF triage, cyclic work, patching, and one-gadget search. Fall back to the direct scripts only when you need to debug the underlying `ctf`-environment execution path.

## MCP First

- Use `toolbox_info`, `toolbox_verify`, and `toolbox_capabilities` first.
- Use the typed pwn operations:
  - `pwn_python`
  - `pwn_checksec`
  - `pwn_cyclic`
  - `pwn_patch_binary`
  - `pwn_one_gadget`
- Treat the existing helper scripts as the implementation fallback, not the primary interface.

Use this skill for exploit development, ELF triage, debugger-heavy workflows, loader/libc patching, one-gadget hunting, and architecture-emulated pwn work in the `ctf` environment.

## Quick Start

Run inline Python in `ctf`:

```bash
python ~/.codex/skills/opencrow-pwn-toolbox/scripts/run_pwn_python.py --code 'from pwn import *; print(cyclic(32))'
```

Run an exploit or helper script:

```bash
python ~/.codex/skills/opencrow-pwn-toolbox/scripts/run_pwn_python.py --file /absolute/path/to/exploit.py
```

Verify the mapped stack:

```bash
python ~/.codex/skills/opencrow-pwn-toolbox/scripts/verify_toolkit.py
```

## Workflow

1. Start here when the task is "get code execution" rather than "understand the binary."
2. Triage the target with `checksec`, `file`, and libc/loader metadata.
3. Use `pwntools` for scripting, local process control, remote sockets, packing, cyclic patterns, and ROP helpers.
4. Move into `gdb` or `pwndbg` once the exploit depends on runtime state.
5. Read [references/tooling.md](references/tooling.md) when choosing between the debugger, patching, or emulation tools.

## Tool Selection

- Use `pwntools` for exploit scripts, process or remote I/O, ELF inspection, cyclic patterns, and ROP chain construction.
- Use `checksec`, `patchelf`, and `pwninit` early to understand or normalize the challenge runtime.
- Use `gdb` and `pwndbg` for breakpoints, heap inspection, and exploit debugging.
- Use `seccomp-tools` when syscall filtering or sandboxing matters.
- Use `one_gadget` when the libc version is known and you want fast candidate constraints for shell-spawning gadgets.
- Use `qemu-user` and `qemu-user-static` when the shipped challenge binary is not native to the host architecture.
- Use `gcc` and `nasm` for shellcode stubs, helper binaries, or local harnesses.

## Resources

- `scripts/run_pwn_python.py`: execute inline code or a `.py` file inside the `ctf` environment.
- `scripts/verify_toolkit.py`: confirm that the mapped Python and native pwn tools are installed.
- `references/tooling.md`: quick selection notes for exploit workflows.
