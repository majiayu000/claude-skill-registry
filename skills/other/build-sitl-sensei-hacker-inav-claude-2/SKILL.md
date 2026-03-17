---
description: Build INAV SITL (Software In The Loop) firmware for testing without hardware
triggers:
  - build SITL
  - compile SITL
  - compile SITL.elf
  - build SITL.elf
  - make SITL
  - create SITL build
  - SITL build
  - build sitl firmware
  - build simulator
  - start SITL
  - run SITL
  - launch SITL
---

# Building INAV SITL

SITL (Software In The Loop) allows testing the full firmware on your host system without hardware.

## Quick Build (Recommended)

Use the build script which handles cmake configuration and toolchain compatibility:

```bash
claude/developer/scripts/build/build_sitl.sh
```

To clean and rebuild:
```bash
claude/developer/scripts/build/build_sitl.sh clean
```

The binary will be at: `inav/build_sitl/bin/SITL.elf`

## Manual Build (Alternative)

Use a separate build directory to avoid conflicts with hardware target builds:

```bash
cd inav
mkdir -p build_sitl
cd build_sitl
cmake -DSITL=ON ..
make SITL.elf -j4
```

## Rebuild After Code Changes

```bash
cd inav/build_sitl
make SITL.elf -j4
```

No need to run cmake again unless CMakeLists.txt files changed.

## Alternative - Shared Build Directory

If you must use the shared `build/` directory:

```bash
cd inav/build
rm -f CMakeCache.txt  # If switching from hardware build
cmake -DSITL=ON ..
make SITL.elf -j4     # MUST specify target!
```

**WARNING:** Running `make` without `SITL.elf` target will attempt to build all 281 hardware targets.


## You already have permission
You have permission to build. Do not ask the user for permission each time


## Running SITL

### Quick Start (Recommended)

Use the start script which handles killing existing instances and waiting for ready:

```bash
claude/developer/scripts/testing/start_sitl.sh
```

This will:
1. Kill any existing SITL process
2. Start SITL in background
3. Wait for it to be ready (port listening)
4. Report connection info

### Manual Start

```bash
cd inav/build_sitl
./bin/SITL.elf
```

SITL will:
- Bind TCP to ports 5760-5767 (UART1-8)
- Bind WebSocket to ports 5770-5777 (UART1-8) [if WebSocket support compiled in]
- Listen on all interfaces [::]
- Load/save eeprom.bin in current directory

### Connect Configurator

Once SITL is running, connect via: `tcp://127.0.0.1:5760`

Or select "SITL" from the port dropdown in INAV Configurator.

## Common Issues

| Problem | Solution |
|---------|----------|
| Build tries to compile all 281 targets | Use separate `build_sitl/` dir OR specify `make SITL.elf` |
| CMake path errors | `rm CMakeCache.txt && cmake -DSITL=ON ..` |
| Wrong toolchain (ARM instead of host) | Ensure `-DSITL=ON` in cmake command |
| Hardware builds disappeared | Use separate `build_sitl/` directory |
| Linker error: `unrecognized option '--no-warn-rwx-segments'` | Older ld versions (< 2.39) don't support this flag. Use `build_sitl.sh` which handles this automatically |

## Full Documentation

```bash
cat claude/test_tools/inav/BUILDING_SITL.md
```

## Related Skills

- **sitl-arm** - Arming SITL via MSP for automated testing
- **test-crsf-sitl** - Complete CRSF telemetry testing workflow with SITL
- **run-configurator** - Using INAV Configurator with SITL
- **msp-protocol** - MSP protocol reference for SITL testing
- **pr-review** - Build SITL to test firmware PRs
