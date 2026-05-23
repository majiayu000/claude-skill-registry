---
name: melee-debug
description: "[EXPERIMENTAL] Debug Melee in Dolphin emulator. Breakpoints are unreliable with JIT mode. Use for memory inspection only until stability improves."
---

# Melee Runtime Debugging (Experimental)

> **Status**: Experimental - breakpoints are flaky with JITARM64 mode. Memory reads work reliably. Not recommended for general use yet.

You can debug Melee running in the Dolphin emulator to verify function behavior, inspect memory, and trace execution during decompilation work.

## When to Use This Skill

- **Verify function behavior**: Set breakpoints on decompiled functions to confirm they work correctly
- **Understand unknown functions**: Watch memory accesses to discover what a function does
- **Debug matching issues**: Compare register values at runtime vs expected from assembly
- **Find struct layouts**: Watch memory writes to map struct field offsets

## Prerequisites

1. **Dolphin-Debug.app** at `~/Applications/Dolphin-Debug.app` (pre-signed for debugging)
2. **Melee ISO** at `~/Downloads/ssbm_v1.02_original.iso`
3. **Python package**: `dolphin-memory-engine` (already installed)

## Important Limitations

### JIT vs Interpreter Mode
- **JITARM64 (default)**: Fast but breakpoints can be flaky - game may not pause visibly
- **Interpreter**: Reliable breakpoints but too slow for practical use (causes input lag)

For most debugging, stick with JIT mode and use memory reads (which are always reliable).

### Single GDB Connection
The Dolphin GDB stub **only accepts one connection per session**. After any GDB operation:
- The connection is consumed
- Restart Dolphin for another GDB session
- Memory reads still work via `dolphin-memory-engine` (no restart needed)

### Debugging vs Memory Access
| Feature | GDB Stub | Memory Engine |
|---------|----------|---------------|
| Read memory | ✅ | ✅ (faster) |
| Write memory | ✅ | ✅ |
| Breakpoints | ✅ | ❌ |
| Single-step | ✅ | ❌ |
| Registers | ✅ | ❌ |
| Multiple uses | ❌ (restart needed) | ✅ |

## Recommended Workflow

**For memory inspection (most reliable):**
```bash
# Just launch Dolphin normally, then read memory
python -m src.dolphin_debug.cli launch --no-wait
python -m src.dolphin_debug.cli read 0x80453080 -n 32 -f f32  # Uses memory engine
```

**For breakpoints (use daemon for persistence):**
```bash
# Terminal 1: Start daemon (blocks, holds GDB connection)
python -m src.dolphin_debug.cli daemon start

# Terminal 2: Set breakpoints and control execution
python -m src.dolphin_debug.cli break <function>
python -m src.dolphin_debug.cli continue
python -m src.dolphin_debug.cli step  # Use step after continue to stabilize
python -m src.dolphin_debug.cli regs
```

## Quick Reference

### Launch and Connect
```bash
# Launch Dolphin and connect (waits for GDB stub)
python -m src.dolphin_debug.cli launch

# Connect to already-running Dolphin
python -m src.dolphin_debug.cli connect

# Check status
python -m src.dolphin_debug.cli status
```

### Memory Operations
```bash
# Read by address or symbol name
python -m src.dolphin_debug.cli read 0x80000000 -n 32
python -m src.dolphin_debug.cli read memset -n 16
python -m src.dolphin_debug.cli read ft_GetPosition -f f32

# Write memory
python -m src.dolphin_debug.cli write 0x80453F9C 50.0  # Set P1 percent
```

### Debugging (Requires Fresh GDB Connection)
```bash
# Set breakpoint
python -m src.dolphin_debug.cli break ft_ActionStateChange

# Continue until breakpoint hit
python -m src.dolphin_debug.cli continue

# Single-step
python -m src.dolphin_debug.cli step -n 5

# View registers
python -m src.dolphin_debug.cli regs

# Halt execution
python -m src.dolphin_debug.cli halt
```

### Symbol Lookup
```bash
# Find symbols by name (partial match)
python -m src.dolphin_debug.cli symbol ft_Action
python -m src.dolphin_debug.cli symbol HSD_
```

## Python API for Scripts

```python
from src.dolphin_debug import DolphinDebugger
from pathlib import Path

dbg = DolphinDebugger()
dbg.connect()

# Load symbols (31k+ from decomp)
dbg.load_symbols(Path("melee/config/GALE01/symbols.txt"))

# Memory operations
game_id = dbg.read_bytes(0x80000000, 6)  # b'GALE01'
percent = dbg.read_f32(0x80453F9C)

# Use symbol names
addr = dbg.resolve_address("ft_ActionStateChange")
data = dbg.read_bytes(addr, 32)

# Breakpoints (GDB only)
if dbg.has_gdb:
    dbg.set_breakpoint(addr)
    dbg.continue_execution()  # Blocks until hit
    regs = dbg.read_registers()
```

## Key Memory Addresses (NTSC 1.02)

| Address | Description |
|---------|-------------|
| `0x80000000` | Game ID ("GALE01") |
| `0x80479D60` | Frame counter |
| `0x8049E6C8` | Stage ID |
| `0x80453080` | P1 fighter data (FighterData*) |
| `+ 0xB0` | P1 X position (float) |
| `+ 0xB4` | P1 Y position (float) |
| `+ 0x1830` | P1 percent (float) |
| `+ 0x10` | P1 action state |

Player blocks are `0xE90` bytes apart (P2 = P1 + 0xE90).

## Workflow Examples

### Verify a Matched Function
```bash
# 1. Restart Dolphin fresh
killall Dolphin; sleep 2
python -m src.dolphin_debug.cli launch

# 2. Set breakpoint on your function
python -m src.dolphin_debug.cli break ft_MyMatchedFunction

# 3. Continue - play the game until function is called
python -m src.dolphin_debug.cli continue

# 4. When stopped, check registers match expected values
python -m src.dolphin_debug.cli regs

# 5. Inspect memory state
python -m src.dolphin_debug.cli read 0x80453080 -n 64 -f hex
```

### Find What Writes to Memory
```bash
# 1. Fresh Dolphin connection
python -m src.dolphin_debug.cli launch

# 2. Set watchpoint on the address
python -m src.dolphin_debug.cli watch 0x80453090 --write

# 3. Continue until watchpoint triggers
python -m src.dolphin_debug.cli continue

# 4. Check LR register - it shows the caller
python -m src.dolphin_debug.cli regs

# 5. Look up the address in symbols
python -m src.dolphin_debug.cli symbol <address_from_LR>
```

### Monitor Game State Without Breakpoints
```bash
# Memory engine works without fresh GDB connection
python -m src.dolphin_debug.cli read 0x80479D60 -f u32  # Frame
python -m src.dolphin_debug.cli read 0x80453080 -n 16 -f f32  # P1 data
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Breakpoints require GDB stub" | Restart Dolphin for fresh GDB connection |
| "Failed to connect" | Ensure Dolphin-Debug.app is running with a game |
| "Not connected" | Run `connect` command first |
| GDB port not open | Check `GDBPort = 9090` is in `[General]` section of Dolphin.ini |
| Memory reads fail | Try again - Dolphin might be in a transition state |
| Dolphin's Debug UI enabled | Disable it - conflicts with external GDB |

## Do NOT

1. **Don't use Dolphin's built-in Debug UI** with this skill - they conflict
2. **Don't expect multiple GDB sessions** without restarting Dolphin
3. **Don't rely on breakpoints for quick queries** - use memory reads instead
4. **Don't forget to restart Dolphin** after a GDB session ends
