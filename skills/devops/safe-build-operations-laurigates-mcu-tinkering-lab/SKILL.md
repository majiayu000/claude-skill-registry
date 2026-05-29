---
name: safe-build-operations
description: Safely execute build, flash, and monitor operations for ESP32/MCU projects. Prevents dangerous operations and validates commands before execution.
allowed-tools: Bash(make:*), Bash(idf.py:*), Bash(ls:*), Bash(pwd:*), Read, Glob, Grep
---

# Safe Build Operations Skill

This skill enables safe execution of build system operations with appropriate safeguards.

## When to Use
- Building firmware projects
- Flashing devices
- Monitoring serial output
- Cleaning build artifacts
- Running development workflows

## Permitted Operations

### Build Commands
```bash
make build-all
make build-esp32
make robocar-build-all
make robocar-build-main
make robocar-build-cam
make esp32-webserver-build
make esp32-audio-build
make llm-telegram-build
```

### Flash Commands
```bash
make robocar-flash-main PORT=/dev/ttyUSB0
make robocar-flash-cam PORT=/dev/ttyUSB0
make esp32-webserver-flash PORT=/dev/ttyUSB0
make esp32-audio-flash PORT=/dev/ttyUSB0
make llm-telegram-flash PORT=/dev/ttyUSB0
```

### Monitor Commands
```bash
make robocar-monitor-main PORT=/dev/ttyUSB0
make robocar-monitor-cam PORT=/dev/ttyUSB0
make esp32-webserver-monitor PORT=/dev/ttyUSB0
```

### Clean Commands
```bash
make clean-all
make robocar-clean
make esp32-clean
make llm-telegram-clean
```

### Development Workflows
```bash
make robocar-develop-main PORT=/dev/ttyUSB0
make robocar-develop-cam PORT=/dev/ttyUSB0
make llm-telegram-develop PORT=/dev/ttyUSB0
```

### Code Quality
```bash
make lint
make lint-c
make lint-python
make format
make format-check
```

## Safety Checks

### Before Flashing ESP32-CAM
1. Remind user about GPIO0 → GND requirement
2. Verify port is specified or use default
3. Confirm device is connected

### Before Clean Operations
1. Confirm user intent (data loss prevention)
2. List what will be cleaned

### Port Validation
Common ports:
- macOS: `/dev/cu.usbserial-*`
- Linux: `/dev/ttyUSB*`, `/dev/ttyACM*`
- Windows: `COM*`

## Prohibited Operations

This skill does NOT allow:
- Arbitrary shell commands
- File deletion outside build directories
- Network operations
- Git operations (use dedicated commands)
- System configuration changes

## Usage Examples

### Build a project
"Build the robocar main controller"
→ `make robocar-build-main`

### Flash with specific port
"Flash the camera to /dev/ttyUSB0"
→ Remind about GPIO0, then `make robocar-flash-cam PORT=/dev/ttyUSB0`

### Full development workflow
"I want to work on the telegram bot"
→ `make llm-telegram-develop PORT=/dev/ttyUSB0`

### Check code quality
"Run the linters"
→ `make lint`
