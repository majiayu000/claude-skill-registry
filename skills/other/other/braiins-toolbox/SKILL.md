---
name: braiins-toolbox
description: Comprehensive Braiins Toolbox skill - batch management tool for Bitcoin mining operations with GUI and CLI for firmware, system, miner, tuner, and cooling management
---

# Braiins Toolbox

Comprehensive skill for Braiins Toolbox - a batch management application for efficiently managing Bitcoin mining operations with both GUI (web-based) and CLI interfaces.

## Description

This skill provides complete coverage of Braiins Toolbox's management capabilities, including:

- **Batch Operations** - Manage multiple mining devices simultaneously
- **Network Scanning** - Discover Antminers, Whatsminers, Avalons, Icerivers, and Braiins devices
- **Firmware Management** - Install, uninstall, and upgrade Braiins OS remotely
- **System Management** - Reboot, collect data/logs, locate devices, execute commands
- **Miner Management** - Configure pools, start/stop mining, manage workers
- **Performance Tuning** - Set power/hashrate targets, enable Dynamic Power Scaling (DPS)
- **Cooling Management** - Configure fan speeds, temperatures, and cooling modes
- **Custom Contracts** - Apply contract codes for special mining agreements
- **Keyboard Shortcuts** - Complete keyboard navigation and Command Palette (Ctrl+P / ⌘+P)

**Official Resources:**
- [Braiins Toolbox Download](https://braiins.com/toolbox)
- [Braiins Toolbox Academy](https://academy.braiins.com/en/braiins-toolbox/introduction/)
- [GitHub Repository](https://github.com/braiins/braiins-toolbox)

## When to Use This Skill

Use this skill when you need to:
- **Manage mining fleets** with batch operations across dozens or hundreds of devices
- **Scan networks** to discover Bitcoin mining hardware (Antminers, Whatsminers, Avalons, Icerivers)
- **Deploy Braiins OS** remotely to multiple miners simultaneously
- **Configure mining pools** across entire mining operations
- **Optimize performance** with power and hashrate targets
- **Enable DPS** (Dynamic Power Scaling) for energy cost optimization
- **Manage cooling** with temperature and fan speed controls
- **Troubleshoot devices** by collecting hardware data and logs
- **Automate workflows** with CLI scripting for mining operations
- **Monitor device status** with live data updates (hashrate, power, temperature)
- **Apply custom contracts** for specialized mining arrangements
- **Navigate with keyboard** using shortcuts and Command Palette for efficiency

## Quick Reference

### Platform Support
- **Windows** - GUI: Double-click icon, CLI: `braiins-toolbox.exe --version`
- **macOS** (Monterey 12.4+, Intel/Apple Silicon) - GUI: Double-click icon, CLI: `/Applications/Braiins\ Toolbox.app/Contents/MacOS/braiins-toolbox`
- **Linux 64-bit** (x86_64, aarch64) - GUI/CLI: `./braiins-toolbox`
- **Linux 32-bit** (armv7) - GUI/CLI: `./braiins-toolbox`

### Supported Devices
- **Braiins**: Mini Miner family
- **Antminers**: S21, S19, S17 families
- **Whatsminers**: M5x, M3x, M2x families
- **Avalons** (Beta): A15xy, A14xy, A13xy, A12xy, A11xy, A10xy families
- **Icerivers**: KAS family

### Prerequisites
- **Braiins OS**: Version 23.03 or newer (some features work with Bitmain/MicroBT stock firmware)
- **Network Ports**: 22 (SSH), 80 (HTTP), 50051 (public API)
- **Internet Access**: Devices need access to `e5a33065.bos.braiins.com:3336` for Braiins OS installation

### Quick Start Commands
```bash
# Scan network for devices
$ ./braiins-toolbox scan '10.10.10-11.*'

# Install Braiins OS on discovered devices
$ ./braiins-toolbox firmware install '10.10.10-11.*'

# Install with contract code
$ ./braiins-toolbox firmware install --contract-code 'XYZ' '10.10.10-11.*'

# Configure mining pool
$ ./braiins-toolbox miner set-pool-urls --url 'stratum+tcp://user@stratum.braiins.com:3333' '10.10.10-11.*'

# Set power target to 3318W
$ ./braiins-toolbox tuner target --power 3318 '10.10.10-11.*'

# Enable DPS (Dynamic Power Scaling)
$ ./braiins-toolbox tuner set-dps on '10.10.10-11.*'

# Reboot devices
$ ./braiins-toolbox system reboot '10.10.10-11.*'
```

### Keyboard Shortcuts (GUI)
```
Command Palette:
  • ⌘+P / Ctrl+P - Open Command Palette for navigation and batch actions

Device List:
  • ⌘+F / Ctrl+F - Search devices
  • ⌘+A / Ctrl+A - Select all devices
  • ⌘+← / ⌘+→ (Ctrl+← / Ctrl+→) - Navigate pages
  • Tab / Shift+Tab - Move between elements
  • ↑ / ↓ - Navigate list items
  • Enter - Confirm selection
  • Esc - Cancel/Close
```

## Available References

### Getting Started
- `references/introduction.md` - Overview, features, prerequisites, supported platforms
- `references/quick-start.md` - GUI and CLI quick start guide with essential commands
- `references/user-interface.md` - Device List, static/live data, keyboard shortcuts, Command Palette

### Core Features
- `references/network-scan.md` - Network scanning for device discovery, IP ranges, output formats
- `references/firmware-management.md` (22KB) - Install/uninstall/upgrade Braiins OS, contract codes, options
- `references/system-management.md` (21KB) - Reboot, data collection, device location, command execution
- `references/miner-management.md` (26KB) - Pool configuration, mining control, worker management
- `references/performance-management.md` (17KB) - Power/hashrate targets, DPS configuration, tuner options
- `references/cooling-management.md` - Fan speeds, temperature thresholds, cooling modes

### Maintenance & Updates
- `references/limitations.md` - Known limitations and constraints
- `references/troubleshooting.md` - Common issues and solutions
- `references/support-contact.md` - Support channels
- `references/whats-new.md` (17KB) - Version history and changelog

## Usage

### GUI Mode

The web-based GUI provides:
1. **Device List Tab** - View all discovered miners with customizable columns, sorting, filtering
2. **Device Management Tab** - Define networks to scan, configure batch operations
3. **Pool Presets** - Save and apply pool configurations across devices
4. **Braiins OS Updates** - Access latest firmware versions with "What's New" section
5. **Logs Tab** - Review action logs and system logs
6. **Shortcuts Tab** - Keyboard shortcut cheat sheet
7. **Manual Tab** - Link to complete Braiins Toolbox Academy documentation

**Live vs. Static Data**:
- **Static Data**: Device model, firmware version, MAC/IP addresses, pool configs (filterable, exportable to CSV)
- **Live Data**: Hashrate, power consumption, temperature, fan speed (refreshed periodically, marked with special icon)

### CLI Mode

The CLI consists of 8 main commands:
- **scan** - Network discovery
- **firmware** - Install, uninstall, upgrade Braiins OS
- **system** - Reboot, data collection, device location, command execution
- **miner** - Pool configuration, mining control
- **tuner** - Performance optimization, DPS configuration
- **cooling** - Fan and temperature management
- **custom-contract** - Apply contract codes
- **self** - Toolbox self-management

### Global Options
```bash
--gui-listen-address <IP:PORT>      # GUI listen address (default: 127.0.0.1:8888)
--gui-config-path <PATH>            # GUI config file path (default: .config/braiins-toolbox/config.toml)
--pool-presets-file-path <PATH>     # Pool presets file path
--password <PASS>                   # Custom web password for miners
--timeout <SECS>                    # Network operation timeout (default: 8 seconds)
--scan-rate <RATE>                  # IP addresses scanned per second (default: 2000)
--logfile-path <PATH>               # Toolbox log file path
--max-log-size <SIZE>               # Max size of all log files (default: 1GB)
--help                              # Display help
--version                           # Display version
```

## Key Features

### Network Scanning
- **IP Range Support**: Flexible notation (10.10.10-11.*, 192.168.*.*)
- **File Input**: Load IP lists from text files (--ip-file)
- **Output Formats**: Table (detailed), Plain (IP list only), CSV (full export)
- **Filters**: --installable-only (show only devices ready for Braiins OS), --all-devices (include unrecognized/password-protected)
- **Periodic Refresh**: GUI auto-refreshes device list (v24.02+)

### Firmware Management
- **Batch Installation**: Install Braiins OS on multiple devices simultaneously
- **Version Control**: Specify target version with --target-version (format: YY.MM.patchlevel)
- **Contract Codes**: Apply custom contracts during installation (--contract-code)
- **Configuration on Install**: Set pools, power targets, DPS, cooling during deployment
- **Concurrency Control**: --concurrency to limit parallel installations
- **Hardware Compatibility**: Automatic checks prevent installation on unsupported hardware

### Performance Tuning
- **Power Targets**: Set exact wattage targets (e.g., --power 3318)
- **Hashrate Targets**: Set TH/s targets (e.g., --hashrate 100)
- **DPS (Dynamic Power Scaling)**: Auto-adjust power based on electricity prices/availability
  - **Power Step**: Incremental power adjustments
  - **Min Power Target**: Minimum power before shutdown
  - **Hashrate Step**: Incremental hashrate adjustments
  - **Shutdown Options**: Auto-shutdown when reaching minimum target (--shutdown-enabled, --shutdown-duration)

### Cooling Management
- **Cooling Modes**: Auto, Manual, Disabled
- **Temperature Control**: Set hot/dangerous temperature thresholds
- **Fan Requirements**: Minimum operational fans (--min-required-fans)
- **Immersion Support**: Disable fans for immersion cooling setups

### Keyboard Navigation (GUI)
- **Command Palette** (⌘+P / Ctrl+P): Navigate tabs, execute batch actions, confirm selections
- **Device List Shortcuts**: Search (⌘+F), select all (⌘+A), navigate pages (⌘+← / ⌘+→)
- **Mouse-Free Workflow**: Complete device management without mouse/touchpad

## Examples

### Scan and Install Workflow
```bash
# 1. Scan network to find installable devices
$ ./braiins-toolbox scan --installable-only '10.10.*.2'

# 2. Install Braiins OS with pool configuration and DPS enabled
$ ./braiins-toolbox firmware install \
  --url 'stratum+tcp://user@stratum.braiins.com:3333' \
  --dps \
  --power-step 100 \
  --min-power-target 2000 \
  '10.10.*.2'

# 3. Verify installation
$ ./braiins-toolbox scan --format table '10.10.*.2'
```

### Performance Optimization
```bash
# Set power target to 3000W on all S19 miners
$ ./braiins-toolbox tuner target --power 3000 '10.10.*.2'

# Add 20 TH/s hashrate increase
$ ./braiins-toolbox tuner target --hashrate +20 '10.10.*.2'

# Enable DPS with auto-shutdown
$ ./braiins-toolbox tuner set-dps on \
  --power-step 200 \
  --min-power-target 2500 \
  --shutdown-enabled true \
  --shutdown-duration 2 \
  '10.10.*.2'
```

### System Management
```bash
# Collect hardware data and logs from devices
$ ./braiins-toolbox system collect-data '10.10.10-11.*'

# Locate specific device (LED blink)
$ ./braiins-toolbox system locate-device on '10.10.10.5'

# Reboot all devices
$ ./braiins-toolbox system reboot '10.10.10-11.*'
```

### Export and Reporting
```bash
# Export device list to CSV
$ ./braiins-toolbox scan --format csv '10.10.*.*' --output devices.csv

# Get plain IP list for scripting
$ ./braiins-toolbox scan --format plain '10.10.10-11.*' > ips.txt

# Scan from file and export results
$ ./braiins-toolbox scan --ip-file input.txt --output results.csv
```

## Notes

- **Braiins OS Requirement**: Most features require Braiins OS 23.03+; some features work with stock firmware
- **Network Configuration**: Ensure firewall allows ports 22 (SSH), 80 (HTTP), 50051 (API)
- **Internet Access**: Braiins OS installation requires `e5a33065.bos.braiins.com:3336` access
- **Configuration Validation**: Invalid config values (e.g., power-step out of range) won't fail installation but will use defaults; check `/var/log/boser/boser.log` for details
- **Live Data Refresh**: GUI refreshes live data only for visible devices (current page)
- **CLI vs GUI**: Same binary provides both interfaces; GUI opens in default web browser
- **Keyboard Shortcuts**: Command Palette (⌘+P / Ctrl+P) enables complete mouse-free workflow

## Limitations

See `references/limitations.md` for complete list of known constraints:
- Braiins OS version requirements for specific features
- Stock firmware compatibility limitations
- Network and firewall requirements
- Platform-specific considerations

## Troubleshooting

See `references/troubleshooting.md` for common issues and solutions:
- Installation failures
- Network connectivity problems
- Device discovery issues
- Configuration validation errors

## Academy Content Integration

✅ **Successfully Scraped** (13 Academy pages, ~129.5KB):
- Introduction and platform prerequisites
- Quick start guides for GUI and CLI
- Complete user interface documentation with keyboard shortcuts
- Network scanning with IP ranges and output formats
- Firmware management (install/uninstall/upgrade with 22KB of options)
- System management commands (21KB)
- Miner management and pool configuration (26KB)
- Performance tuning with DPS and power/hashrate targets (17KB)
- Cooling management with fan and temperature controls
- Limitations, troubleshooting, support contacts
- Version history and "What's New" changelog (17KB)

---

**Generated by Skill Seeker** | Comprehensive Multi-Source Scraper
**Last Updated**: 2025-12-28
**Total References**: 13 files (129.5KB)
**Sources**: Braiins Toolbox Academy (Playwright-scraped JavaScript-rendered content)
