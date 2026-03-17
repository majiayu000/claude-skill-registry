---
name: ios-stop-app
description: Stop the iOS app running on connected iPhone. Cleanly terminates the app using SIGTERM. Use when stopping the app for debugging, testing, or cleanup.
---

# iOS Stop App

## Overview

Stops the iOS app running on a connected iPhone by sending SIGTERM signal to the app process. This cleanly terminates the app, allowing it to perform cleanup operations before exiting.

## When to Use

Invoke this skill when the user:
- Asks to "stop the app"
- Wants to "kill the app"
- Says "terminate the app on device"
- Mentions shutting down or closing the app
- Needs to stop before deploying new version

## Prerequisites

- iPhone connected via USB
- `pymobiledevice3` installed (`pip3 install pymobiledevice3`)
- Device trusted
- App must be running on the device

## Instructions

1. Navigate to the iOS app directory:
   ```bash
   cd path/to/ios/app
   ```

2. Run the stop script:
   ```bash
   ./stop-app.sh
   ```

3. The script will:
   - Auto-detect the connected iPhone
   - Find the app's process ID using `pymobiledevice3`
   - Send SIGTERM signal to terminate cleanly
   - Report success or if app wasn't running

4. Inform the user:
   - The app has been stopped
   - Safe to call even if app isn't running
   - Use SIGTERM (not SIGKILL) for clean shutdown

## Expected Output

When app is running:
```
🛑 Stopping NoobTest on device...
✅ App stopped
```

When app is not running:
```
🛑 Stopping NoobTest on device...
⚠️  NoobTest is not running
```

## How It Works

The script:
1. Uses `xcodebuild -showdestinations` to get device ID
2. Runs `pymobiledevice3 processes pgrep NoobTest` to find process ID
3. Extracts PID from output
4. Uses `xcrun devicectl device process signal` to send SIGTERM

## SIGTERM vs SIGKILL

The script uses **SIGTERM** (signal 15), not SIGKILL:
- SIGTERM allows the app to clean up (save state, close connections)
- SIGKILL would force immediate termination without cleanup
- SIGTERM is the proper way to stop an app during development

## Common Use Cases

**Before deploying new version**:
```bash
./stop-app.sh
./install-device.sh
```

**Pairing with restart**:
```bash
./stop-app.sh
# Make changes
./restart-app.sh
```

**Clean state testing**:
Stop the app, clear data/caches manually, then restart fresh.

## Common Issues

**pymobiledevice3 not found**:
- Install it: `pip3 install pymobiledevice3`
- Ensure Python bin directory is in PATH

**No device detected**:
- Check USB connection
- Ensure device is trusted
- Try disconnecting and reconnecting

**App not stopping**:
- Check app is actually running on device
- Try restarting the device if process is stuck

## Safety

This script is safe to call repeatedly:
- Won't error if app isn't running
- Uses clean shutdown signal
- Reports status clearly

## Bundle ID

The script is configured for the specific app's bundle ID (e.g., `com.miso.noobtest` for Firefly/NoobTest). Different apps have different bundle IDs.
