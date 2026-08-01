---
name: adb-android-control
description: 'Comprehensive Android device control via ADB (Android Debug Bridge).
  Use when user asks about: Android device management, app installation/uninstallation,
  APK operations, package management, file tran'
---

---
name: adb-android-control
description: Comprehensive Android device control via ADB (Android Debug Bridge). Use when user asks about: Android device management, app installation/uninstallation, APK operations, package management, file transfer (push/pull), screenshots, screen recording, input simulation (tap/swipe/text/keyevents), shell commands, logcat viewing, device info (battery/memory/storage), automation scripts, wireless ADB connection, scrcpy mirroring. Keywords: adb, android, phone, tablet, device, apk, install app, uninstall app, screenshot, screen record, tap, swipe, type text, keyevent, logcat, push file, pull file, shell, package, activity, intent, broadcast, dumpsys, getprop, settings, input, sendevent, monkey, am start, pm list, device info, battery status, wireless adb, connect device.
---

# ADB Android Control Skill

Complete Android device control and automation via ADB (Android Debug Bridge) for Claude Code.

## When to Use This Skill

Use this skill when user asks about:

- **Device Management**: Connect, disconnect, check status, device info
- **App Operations**: Install, uninstall, list packages, clear data, force stop
- **File Transfer**: Push/pull files between host and device
- **Screen Control**: Screenshots, screen recording, mirroring
- **Input Simulation**: Taps, swipes, text input, key events
- **Shell Access**: Run commands on device
- **Debugging**: Logcat, dumpsys, process info
- **Automation**: Scripted workflows, batch operations

## Quick Reference

### Device Connection

```bash
# Check connected devices
adb devices

# Connect wirelessly (device already paired)
adb connect <device-ip>:<port>

# Disconnect
adb disconnect <device-ip>:<port>

# Kill ADB server (troubleshooting)
adb kill-server && adb start-server
```

### App Management

```bash
# List all packages
adb shell pm list packages

# List third-party apps only
adb shell pm list packages -3

# Search for specific package
adb shell pm list packages | grep -i "keyword"

# Install APK
adb install /path/to/app.apk

# Install with options
adb install -r app.apk          # Replace existing
adb install -d app.apk          # Allow downgrade
adb install -g app.apk          # Grant all permissions

# Uninstall app
adb uninstall com.example.app

# Keep data when uninstalling
adb uninstall -k com.example.app

# Clear app data
adb shell pm clear com.example.app

# Force stop app
adb shell am force-stop com.example.app

# Get app info
adb shell dumpsys package com.example.app

# Get APK path
adb shell pm path com.example.app

# Extract APK from device
adb pull $(adb shell pm path com.example.app | cut -d: -f2) ./app.apk

# Disable/Enable app
adb shell pm disable-user com.example.app
adb shell pm enable com.example.app

# List disabled packages
adb shell pm list packages -d
```

### File Operations

```bash
# Push file to device
adb push local_file.txt /sdcard/

# Push directory
adb push ./local_dir /sdcard/

# Pull file from device
adb pull /sdcard/file.txt ./

# Pull directory
adb pull /sdcard/DCIM ./photos

# List files on device
adb shell ls -la /sdcard/

# Create directory
adb shell mkdir -p /sdcard/MyFolder

# Delete file
adb shell rm /sdcard/file.txt

# Delete directory
adb shell rm -rf /sdcard/MyFolder

# Check storage space
adb shell df -h

# Find files
adb shell find /sdcard -name "*.jpg" -type f
```

### Screenshots & Screen Recording

```bash
# Take screenshot (save on device)
adb shell screencap /sdcard/screenshot.png

# Take screenshot (direct to local)
adb exec-out screencap -p > screenshot.png

# Screen recording (max 180 seconds)
adb shell screenrecord /sdcard/video.mp4

# Screen recording with options
adb shell screenrecord --time-limit 30 --size 720x1280 --bit-rate 4000000 /sdcard/video.mp4

# Stop recording: Ctrl+C or wait for time limit

# Pull recording
adb pull /sdcard/video.mp4 ./
```

### Input Simulation

```bash
# Tap at coordinates (x, y)
adb shell input tap 500 1000

# Swipe (x1, y1, x2, y2, duration_ms)
adb shell input swipe 500 1500 500 500 300

# Swipe up (scroll down)
adb shell input swipe 500 1500 500 500 200

# Swipe down (scroll up)
adb shell input swipe 500 500 500 1500 200

# Swipe left
adb shell input swipe 800 1000 200 1000 200

# Swipe right
adb shell input swipe 200 1000 800 1000 200

# Long press
adb shell input swipe 500 1000 500 1000 1000

# Input text (no spaces)
adb shell input text "HelloWorld"

# Input text with spaces (use %s)
adb shell input text "Hello%sWorld"

# Key events
adb shell input keyevent KEYCODE_HOME
adb shell input keyevent KEYCODE_BACK
adb shell input keyevent KEYCODE_MENU
adb shell input keyevent KEYCODE_POWER
adb shell input keyevent KEYCODE_VOLUME_UP
adb shell input keyevent KEYCODE_VOLUME_DOWN
adb shell input keyevent KEYCODE_ENTER
adb shell input keyevent KEYCODE_DEL          # Backspace
adb shell input keyevent KEYCODE_TAB
adb shell input keyevent KEYCODE_ESCAPE

# Key event codes (numeric)
adb shell input keyevent 3    # Home
adb shell input keyevent 4    # Back
adb shell input keyevent 26   # Power
adb shell input keyevent 24   # Volume Up
adb shell input keyevent 25   # Volume Down
adb shell input keyevent 66   # Enter
adb shell input keyevent 67   # Backspace
adb shell input keyevent 82   # Menu

# Wake up device
adb shell input keyevent KEYCODE_WAKEUP

# Lock device
adb shell input keyevent KEYCODE_SLEEP

# Toggle power (wake/sleep)
adb shell input keyevent KEYCODE_POWER

# Open recent apps
adb shell input keyevent KEYCODE_APP_SWITCH

# Take screenshot via key
adb shell input keyevent KEYCODE_SYSRQ
```

### Activity & Intent Management

```bash
# Start activity
adb shell am start -n com.package.name/.ActivityName

# Start with action
adb shell am start -a android.intent.action.VIEW -d "https://google.com"

# Open URL in browser
adb shell am start -a android.intent.action.VIEW -d "https://example.com"

# Open settings
adb shell am start -a android.settings.SETTINGS

# Open specific settings
adb shell am start -a android.settings.WIFI_SETTINGS
adb shell am start -a android.settings.BLUETOOTH_SETTINGS
adb shell am start -a android.settings.DISPLAY_SETTINGS
adb shell am start -a android.settings.SOUND_SETTINGS
adb shell am start -a android.settings.APPLICATION_SETTINGS

# Send broadcast
adb shell am broadcast -a android.intent.action.BOOT_COMPLETED

# Start service
adb shell am startservice -n com.package.name/.ServiceName

# Kill background processes
adb shell am kill-all

# Force stop all background apps
adb shell am kill-all
```

### Device Information

```bash
# Get device model
adb shell getprop ro.product.model

# Get Android version
adb shell getprop ro.build.version.release

# Get SDK version
adb shell getprop ro.build.version.sdk

# Get serial number
adb shell getprop ro.serialno

# Get all properties
adb shell getprop

# Get battery info
adb shell dumpsys battery

# Get memory info
adb shell dumpsys meminfo

# Get CPU info
adb shell dumpsys cpuinfo

# Get display info
adb shell dumpsys display | grep -i "mBaseDisplayInfo"

# Get screen resolution
adb shell wm size

# Get screen density
adb shell wm density

# Get WiFi info
adb shell dumpsys wifi | grep -i "mWifiInfo"

# Get IP address
adb shell ip addr show wlan0

# Get network stats
adb shell dumpsys netstats

# Get running processes
adb shell ps -A

# Get top processes (like top)
adb shell top -n 1

# Get storage info
adb shell df -h
```

### Logcat (System Logs)

```bash
# View all logs (streaming)
adb logcat

# Clear log buffer
adb logcat -c

# View recent logs (dump and exit)
adb logcat -d

# Filter by tag
adb logcat -s "MyTag:*"

# Filter by priority (V/D/I/W/E/F)
adb logcat "*:E"          # Errors only
adb logcat "*:W"          # Warnings and above

# Filter specific app
adb logcat --pid=$(adb shell pidof -s com.example.app)

# Save logs to file
adb logcat -d > logs.txt

# View with timestamps
adb logcat -v time

# View with thread info
adb logcat -v threadtime

# Specific buffer
adb logcat -b crash       # Crash logs
adb logcat -b events      # Event logs
adb logcat -b main        # Main log
adb logcat -b system      # System log
```

### System Settings

```bash
# Get setting value
adb shell settings get system screen_brightness
adb shell settings get global airplane_mode_on
adb shell settings get secure android_id

# Set system settings
adb shell settings put system screen_brightness 128

# Set global settings
adb shell settings put global airplane_mode_on 1

# List all settings
adb shell settings list system
adb shell settings list global
adb shell settings list secure

# Common settings changes
# Brightness (0-255)
adb shell settings put system screen_brightness 200

# Screen timeout (ms)
adb shell settings put system screen_off_timeout 60000

# Enable/disable animations
adb shell settings put global window_animation_scale 0
adb shell settings put global transition_animation_scale 0
adb shell settings put global animator_duration_scale 0
```

### Network Operations

```bash
# Enable/disable WiFi
adb shell svc wifi enable
adb shell svc wifi disable

# Enable/disable mobile data
adb shell svc data enable
adb shell svc data disable

# Enable/disable airplane mode
adb shell settings put global airplane_mode_on 1
adb shell am broadcast -a android.intent.action.AIRPLANE_MODE

# Get WiFi networks
adb shell dumpsys wifi | grep "SSID"

# Port forwarding
adb forward tcp:8080 tcp:8080

# Reverse port forwarding
adb reverse tcp:8080 tcp:8080

# Remove port forward
adb forward --remove tcp:8080

# List forwards
adb forward --list
```

### Power & Reboot

```bash
# Reboot device
adb reboot

# Reboot to recovery
adb reboot recovery

# Reboot to bootloader
adb reboot bootloader

# Shutdown device (root required)
adb shell reboot -p

# Keep device awake while connected
adb shell svc power stayon usb

# Disable stay awake
adb shell svc power stayon false

# Get battery level
adb shell dumpsys battery | grep level

# Get charging status
adb shell dumpsys battery | grep status
```

### Advanced Operations

```bash
# Run shell interactively
adb shell

# Run as specific user
adb shell run-as com.example.app

# Get current activity
adb shell dumpsys activity activities | grep "mResumedActivity"

# Get current window
adb shell dumpsys window windows | grep -E "mCurrentFocus|mFocusedApp"

# UI dump (for automation)
adb shell uiautomator dump /sdcard/ui.xml
adb pull /sdcard/ui.xml ./

# Get UI hierarchy
adb exec-out uiautomator dump /dev/tty

# Monkey testing (random events)
adb shell monkey -p com.example.app -v 500

# Grant permission
adb shell pm grant com.example.app android.permission.CAMERA

# Revoke permission
adb shell pm revoke com.example.app android.permission.CAMERA

# List permissions
adb shell pm list permissions -g

# Check if permission granted
adb shell dumpsys package com.example.app | grep "permission"

# Backup app data
adb backup -apk -shared -all -f backup.ab

# Restore backup
adb restore backup.ab
```

## Automation Workflows

### Workflow 1: App Testing Automation

```bash
#!/bin/bash
# Automated app testing workflow

APP_PACKAGE="com.example.app"
APK_PATH="./app.apk"

echo "Installing app..."
adb install -r "$APK_PATH"

echo "Launching app..."
adb shell am start -n "$APP_PACKAGE/.MainActivity"
sleep 3

echo "Taking initial screenshot..."
adb exec-out screencap -p > screenshot_initial.png

echo "Performing test actions..."
adb shell input tap 540 960     # Tap center
sleep 1
adb shell input swipe 540 1500 540 500 300  # Scroll
sleep 1
adb shell input tap 540 500     # Tap button

echo "Taking final screenshot..."
adb exec-out screencap -p > screenshot_final.png

echo "Collecting logs..."
adb logcat -d --pid=$(adb shell pidof -s "$APP_PACKAGE") > app_logs.txt

echo "Test complete!"
```

### Workflow 2: Device Health Check

```bash
#!/bin/bash
# Device health check

echo "=== DEVICE HEALTH CHECK ==="
echo ""

echo "Device Info:"
echo "  Model: $(adb shell getprop ro.product.model)"
echo "  Android: $(adb shell getprop ro.build.version.release)"
echo "  SDK: $(adb shell getprop ro.build.version.sdk)"
echo ""

echo "Battery Status:"
adb shell dumpsys battery | grep -E "level|status|temperature"
echo ""

echo "Storage:"
adb shell df -h /data | tail -1
echo ""

echo "Memory:"
adb shell cat /proc/meminfo | head -3
echo ""

echo "Running Apps:"
adb shell ps -A | wc -l
echo ""

echo "=== END HEALTH CHECK ==="
```

### Workflow 3: Bulk Screenshot

```bash
#!/bin/bash
# Take multiple screenshots with delay

COUNT=${1:-5}
DELAY=${2:-2}
OUTPUT_DIR="./screenshots_$(date +%Y%m%d_%H%M%S)"

mkdir -p "$OUTPUT_DIR"

for i in $(seq 1 $COUNT); do
    echo "Taking screenshot $i of $COUNT..."
    adb exec-out screencap -p > "$OUTPUT_DIR/screen_$i.png"
    sleep $DELAY
done

echo "Screenshots saved to $OUTPUT_DIR"
```

### Workflow 4: App Data Extraction

```bash
#!/bin/bash
# Extract app data

PACKAGE="$1"
OUTPUT_DIR="./app_data_$(date +%Y%m%d_%H%M%S)"

if [ -z "$PACKAGE" ]; then
    echo "Usage: $0 <package_name>"
    exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Getting APK..."
APK_PATH=$(adb shell pm path "$PACKAGE" | cut -d: -f2 | tr -d '\r')
adb pull "$APK_PATH" "$OUTPUT_DIR/app.apk"

echo "Dumping package info..."
adb shell dumpsys package "$PACKAGE" > "$OUTPUT_DIR/package_info.txt"

echo "Dumping permissions..."
adb shell dumpsys package "$PACKAGE" | grep "permission" > "$OUTPUT_DIR/permissions.txt"

echo "Done! Data saved to $OUTPUT_DIR"
```

## Termux Auto-Connect & Monitoring

Persistent ADB connections with automatic port scanning, connection monitoring, and multi-network support.

### Quick Setup

```bash
cd ~/.claude/skills/adb-android-control/termux
./setup.sh ZFOLD7 192.168.1.103:34591
```

This installs:
- Auto-connect service (reconnects every 30s)
- Boot script (starts on Termux launch)
- Connection monitor (detects port changes)
- Control script (`adb-control`)

### adb-control Command

Main control interface for all ADB automation:

```bash
adb-control status   # Show connection status, services, signal
adb-control start    # Start all services and monitor
adb-control stop     # Stop all services
adb-control restart  # Restart everything
adb-control scan     # Scan for new ADB port (30000-50000)
adb-control log 50   # View last 50 lines of logs
adb-control monitor  # Run monitor in foreground
```

### Configuration Files

**~/.adb_devices** - Device addresses:
```bash
# Format: NAME=IP:PORT
ZFOLD7=192.168.1.103:33467
PIXEL=192.168.1.104:5555
```

**device.env** - Device specs and multi-network config:
```bash
DEVICE_SERIAL="RFCY7036LSY"
DEVICE_ANDROID_ID="54116884d88102e3"
ADB_HOME_IP="192.168.1.103"
ADB_RECONNECT_INTERVAL="30"
```

### Auto Port Scanning

Android Wireless Debugging changes port on:
- WiFi disconnect/reconnect
- Screen lock/unlock
- Wireless debugging toggle

The system automatically:
1. Detects connection failure
2. Pings IP to check if host reachable
3. Scans ports 30000-50000 for ADB
4. Updates config with new port
5. Reconnects automatically

Manual scan:
```bash
python3 scripts/adb_port_scan.py 192.168.1.103 30000 50000
```

### Connection Monitor

Continuous monitoring of ADB and WiFi state:

```bash
# Check current status
python3 scripts/connection_monitor.py status

# Single check for changes
python3 scripts/connection_monitor.py check

# Continuous monitoring (runs in background on boot)
python3 scripts/connection_monitor.py run 30
```

**Detects:**
- Connection drops
- Port changes
- Network switches
- Signal strength changes (>10dB)

**Actions:**
- Auto-updates config on port change
- Sends Termux notification on important events
- Logs all events to `~/.adb_monitor.log`

### Radio Scanner

WiFi and Bluetooth status with signal metrics:

```bash
python3 scripts/radio_scan.py          # All info
python3 scripts/radio_scan.py wifi     # WiFi only
python3 scripts/radio_scan.py bluetooth # Bluetooth only
python3 scripts/radio_scan.py caps     # Radio capabilities
```

**Output includes:**
- SSID, BSSID, RSSI (dBm), frequency, channel
- Link speed (TX/RX Mbps)
- WiFi standard (802.11ac/ax)
- MIMO support, 6GHz capability
- Bluetooth state, connected devices

### USB Device Detection

Identify USB devices connected via OTG:

```bash
# List USB devices
termux-usb -l

# Identify device (grant permission when prompted)
termux-usb -r -e scripts/usb_identify.py /dev/bus/usb/001/002
```

### Log Files

| File | Contents |
|------|----------|
| ~/.adb_connect.log | Connection events, port changes |
| ~/.adb_monitor.log | Monitor events, signal changes |
| ~/.adb_state.json | Last known connection state |
| ~/.adb_devices | Device configuration |

### Service Control

```bash
# Termux services
sv status adb-autoconnect
sv restart adb-autoconnect
sv down adb-autoconnect

# Monitor process
cat ~/.adb_monitor.pid
kill $(cat ~/.adb_monitor.pid)
```

### Boot Sequence

On Termux startup (`~/.termux/boot/adb-autoconnect`):
1. Wake lock acquired
2. Load device config
3. Try connecting with saved port
4. If fails → scan for new port
5. Start auto-connect service
6. Start connection monitor
7. Send "ADB Ready" notification

## Python Scripts

### Core Scripts

| Script | Purpose |
|--------|---------|
| adb_controller.py | ADB operations with error handling |
| adb_automation.py | UI automation, app testing |
| adb_monitor.py | Logcat streaming, metrics |

### Termux Integration

| Script | Purpose |
|--------|---------|
| connection_monitor.py | ADB/WiFi state monitoring |
| adb_port_scan.py | Port scanner for wireless ADB |
| radio_scan.py | WiFi/Bluetooth scanner |
| usb_identify.py | USB device identification |
| adb-control.sh | Unified control interface |

## Common Key Event Codes

| Key | Code | Name |
|-----|------|------|
| Home | 3 | KEYCODE_HOME |
| Back | 4 | KEYCODE_BACK |
| Call | 5 | KEYCODE_CALL |
| End Call | 6 | KEYCODE_ENDCALL |
| Volume Up | 24 | KEYCODE_VOLUME_UP |
| Volume Down | 25 | KEYCODE_VOLUME_DOWN |
| Power | 26 | KEYCODE_POWER |
| Camera | 27 | KEYCODE_CAMERA |
| Menu | 82 | KEYCODE_MENU |
| Enter | 66 | KEYCODE_ENTER |
| Backspace | 67 | KEYCODE_DEL |
| Tab | 61 | KEYCODE_TAB |
| Space | 62 | KEYCODE_SPACE |
| Escape | 111 | KEYCODE_ESCAPE |
| Recent Apps | 187 | KEYCODE_APP_SWITCH |
| Mute | 164 | KEYCODE_VOLUME_MUTE |

## Error Handling

### Common Issues

**Device not found:**
```bash
adb kill-server && adb start-server
adb devices
```

**Device offline:**
```bash
adb disconnect <device-ip>:<port>
adb connect <device-ip>:<port>
```

**Permission denied:**
```bash
# Some operations require root
adb root   # If device is rooted
```

**Connection refused:**
```bash
# Re-pair device
adb pair <device-ip>:PORT PAIRING_CODE
```

## Current Device

Connected device: `<device-ip>:<port>`

To verify connection:
```bash
adb -s <device-ip>:<port> shell getprop ro.product.model
```

## Keywords for Detection

adb, android, phone, tablet, mobile device, apk, install app, uninstall, package, screenshot, screencap, screen recording, screenrecord, tap, swipe, touch, input, keyevent, key press, type text, logcat, logs, push file, pull file, transfer, shell command, device info, battery, storage, wifi, settings, activity, intent, broadcast, dumpsys, getprop, monkey test, ui automator, automation, wireless adb, connect device, app management, force stop, clear data, permissions
