---
description: Build INAV firmware for specific hardware targets (flight controllers)
triggers:
  - build inav target
  - compile inav target
  - build firmware
  - compile firmware
  - build MATEKF
  - compile MATEKF
  - build target
  - make target
  - build flight controller
  - compile flight controller
---

# Building INAV Firmware Targets

Build INAV firmware for specific flight controller boards.

## Prerequisites

Install required tools (one-time setup):

```bash
# Ubuntu/Debian
sudo apt update && sudo apt upgrade
sudo apt install git make ruby cmake gcc

# Fedora
sudo dnf -y update
sudo dnf install git make ruby cmake gcc

# Arch
sudo pacman -Syu
sudo pacman -S git make ruby cmake gcc
```

## First-Time Setup

Initialize the build environment (only needed once):

```bash
cd inav
mkdir -p build
cd build
cmake ..
```

This will automatically download the ARM cross-compiler if needed.

**Note:** If you want to use your distro's cross-compiler instead:
```bash
cmake -DCOMPILER_VERSION_CHECK=OFF ..
```

## Building a Single Target

**Simple method (no Docker needed):**

```bash
cd inav/build
make MATEKF405
```

Replace `MATEKF405` with your target board name.

### Clean build when switching versions
To clean the build direcrory between major versions such as 8.x.y and 9.x.y, run the following in the build/ directory:
```bash
make clean
cmake ..
```

**Important:** You do NOT need Docker to build INAV firmware. The cmake build system automatically downloads the ARM cross-compiler to `inav/tools/` and uses it directly. Docker is optional and only used by the `build.sh` wrapper script.

## Building Multiple Targets

```bash
cd inav/build
# Build specific targets
make MATEKF405 MATEKF722

# Parallel build using all but 1 CPU core
make -j 4 MATEKF405 MATEKF722
```

## Finding Available Targets

```bash
cd inav/build
make help | less
```

Or search for specific targets:
```bash
make help | grep MATEK
```

## Output Location

Firmware hex files are created in the `build/` directory:
```
inav/build/inav_x.y.z_TARGETNAME.hex
```

## Cleaning Builds

```bash
# Clean everything
cd inav/build
make clean

# Clean specific target
make clean_MATEKF405

# Clean multiple targets
make clean_MATEKF405 clean_MATEKF722
```

## After Git Pull

When you pull new code changes, you don't need to re-run cmake:

```bash
cd inav
git pull
cd build
make MATEKF405
```

## Build Failures

If a build fails due to target configuration issues (flash overflow, DMA conflicts), use the **target-developer** agent to diagnose and fix the target configuration:
```
/task target-developer "Diagnose flash overflow on MATEKF405"
```

## You already have permission
You have permission to build. Do not ask the user for permission each time

## Common Targets

Popular flight controller targets:

- **Matek:** MATEKF405, MATEKF722, MATEKF405SE, MATEKF722SE
- **JHEMCU:** JHEF405, JHEF722
- **SpeedyBee:** SPEEDYBEEF405, SPEEDYBEEF7

## Build for serial printf debugging
This will allow LOG_DEBUG lines to be used for troubleshooting (serial printf debugging):
make CPPFLAGS="-DUSE_BOOTLOG=1024 -DUSE_LOG" BROTHERHOBBYH743

## Next Steps

After building, you can:
1. Flash using INAV Configurator (GUI)
2. Flash using command-line tools (see **flash-firmware-dfu** skill)
3. Use msp-tool or flash.sh helper tools

## Target Directory Split Verification

When splitting multi-target directories (e.g., OMNIBUSF4 with multiple variants), see:
`claude/developer/docs/debugging/target-split-verification.md`

**Scripts:** `claude/developer/scripts/analysis/`

```bash
python3 comprehensive_verification.py   # Multi-tool verification
python3 verify_target_conditionals.py   # Pattern matching
python3 split_omnibus_targets.py        # Functional verification (gcc -E)
```

## Related Skills and Agents

**Skills:**
- **flash-firmware-dfu** - Flash firmware to flight controller via DFU
- **build-sitl** - Build SITL for testing without hardware
- **find-symbol** - Find function definitions in firmware code
- **msp-protocol** - MSP protocol reference

**Agents:**
- **inav-builder** - Primary agent for all firmware builds (use instead of manual cmake/make commands)
- **target-developer** - Use if build fails due to target configuration issues (flash overflow, DMA conflicts)
- **fc-flasher** - Use AFTER successful build to flash firmware with settings preservation

## References

- Full documentation: `inav/docs/development/Building in Linux.md`
- Target split verification: `claude/developer/docs/debugging/target-split-verification.md`
- Performance debugging: `claude/developer/docs/debugging/performance-debugging.md`
