---
description: Use mwptools CLI utilities for FC settings management, blackbox download, and CLI terminal access
triggers:
  - mwptools
  - fc-get
  - fc-set
  - backup settings
  - restore settings
  - cli settings
  - cliterm
  - cli terminal
  - cli mode
  - flashgo
  - download blackbox
  - blackbox download
  - gps passthrough
---

# mwptools CLI Utilities

mwptools provides CLI utilities for INAV development and testing. Located at `~/inavflight/mwptools/`.

## Installation Check

First, check if tools are installed:

```bash
which fc-get cliterm flashgo 2>/dev/null || echo "Not installed"
```

If not installed:

```bash
cd ~/inavflight/mwptools
meson setup _build --prefix=~/.local --strip
ninja -C _build install
```

## CLI Settings Backup/Restore

### Backup Settings (fc-get)

```bash
# Auto-detect FC and dump settings
fc-get /tmp/my-settings.txt

# With specific device
fc-get -d /dev/ttyACM0 /tmp/my-settings.txt
```

### Restore Settings (fc-set)

```bash
# Restore settings (creates timestamped backup of original)
fc-set /tmp/my-settings.txt

# Without backup
fc-set -n /tmp/my-settings.txt
```

**Workflow for firmware update:**
1. `fc-get /tmp/backup.txt` - Save current settings
2. Flash new firmware
3. `fc-set /tmp/backup.txt` - Restore settings

## Interactive CLI Terminal (cliterm)

```bash
# Auto-detect and enter CLI
cliterm

# Specific device
cliterm -d /dev/ttyACM0

# SITL connection (localhost:5670)
cliterm -s

# GPS passthrough (for u-center)
cliterm -g

# MSC mode (USB mass storage)
cliterm -m
```

**Key bindings:**
- `Ctrl-D` - Quit CLI without saving
- `Ctrl-C` - Exit cliterm

## Blackbox Download (flashgo)

```bash
# Check flash usage
flashgo -info

# Download to auto-generated filename
flashgo

# Download to specific file
flashgo -file my_log.TXT -dir /tmp/

# Download and erase
flashgo -erase

# Erase only
flashgo -only-erase
```

## Common Development Workflows

### Before Major Changes

```bash
# 1. Backup current settings
fc-get ~/backups/pre-change-$(date +%Y%m%d).txt

# 2. Make firmware changes and flash
./build.sh MATEKF405SE
# ... flash ...

# 3. Restore settings
fc-set ~/backups/pre-change-*.txt
```

### Debug Session with CLI

```bash
# Interactive CLI for testing commands
cliterm

# Inside CLI:
# status
# get
# set acc_hardware = AUTO
# save
```

### Blackbox Analysis

```bash
# Download logs
flashgo -dir /tmp/blackbox/

# Analyze with mwptools scripts
cd ~/inavflight/mwptools/src/bbox-replay
./inav-parse_bb_compass.rb --plot /tmp/blackbox/LOG00001.TXT
```

## Documentation

Full reference: `claude/developer/docs/mwptools-reference.md`

Online docs: https://stronnag.codeberg.page/mwptools/
