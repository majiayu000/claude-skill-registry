---
name: android-stop-app
description: Stop the Android app running on connected device. Cleanly terminates the app using force-stop. Use when stopping the app for debugging, testing, or cleanup.
---

# Android Stop App

## Overview

Stops the Android app running on a connected device by using `adb shell am force-stop`. This cleanly terminates all app processes, clearing memory while preserving app data.

## When to Use

Invoke this skill when the user:
- Asks to "stop the Android app"
- Wants to "kill the app"
- Says "terminate the Android app on device"
- Mentions shutting down or closing the Android app
- Needs to stop before deploying new version

## Prerequisites

- Android device connected via USB
- USB debugging enabled
- ADB installed (`brew install android-platform-tools`)
- Device authorized
- App must be running on the device

## Instructions

1. Navigate to the Android app directory:
   ```bash
   cd path/to/android/app
   ```

2. Run the stop script:
   ```bash
   ./stop-app.sh
   ```

3. The script will:
   - Use `adb shell am force-stop` to terminate the app
   - Report success

4. Inform the user:
   - The app has been stopped
   - Safe to call even if app isn't running
   - Uses force-stop for clean shutdown (not kill)

## Expected Output

```
🛑 Stopping NoobTest on device...
✅ App stopped
```

## How It Works

The script uses:
- `adb shell am force-stop com.miso.noobtest`

This Android framework command:
- Stops all processes associated with the package
- Clears app from memory
- Preserves app data and settings
- Clean shutdown (not emergency kill)

## force-stop vs kill

**force-stop** (recommended):
- Android framework command
- Clean shutdown
- Preserves app data
- Safe for development

**kill** (not recommended):
- OS-level signal
- Abrupt termination
- May leave resources in inconsistent state
- Only use if force-stop fails

## Common Use Cases

**Before deploying new version**:
```bash
./stop-app.sh
./install-device.sh
```

**Pairing with restart**:
```bash
./stop-app.sh
# Make configuration changes
./restart-app.sh
```

**Clean state testing**:
```bash
./stop-app.sh
# Clear app data manually if needed
adb shell pm clear com.miso.noobtest
# Then install fresh
```

## Common Issues

**"no devices found"**:
- Check USB connection
- Ensure USB debugging enabled
- Verify authorized: `adb devices`
- Try: `adb kill-server && adb start-server`

**"adb: command not found"**:
- Install Android platform tools: `brew install android-platform-tools`
- Check PATH includes adb

**App still running after force-stop**:
- Rare, but check with: `adb shell pidof com.miso.noobtest`
- If still running, restart device
- Or use: `adb shell pm clear com.miso.noobtest` (nukes app data too)

## Safety

This script is safe to call repeatedly:
- Won't error if app isn't running
- Uses clean shutdown method
- Reports status clearly
- No risk to app data or installation

## Package Name

The script is configured for the specific app's package name (e.g., `com.miso.noobtest` for Firefly/NoobTest). Package name is defined in build.gradle.kts under `applicationId`.

## Data Preservation

`force-stop` does NOT clear:
- App installation
- App data (SharedPreferences, databases, files)
- App permissions
- User settings

To fully clear app state, use:
```bash
adb shell pm clear com.miso.noobtest
```

But this will require reinstallation and setup.
