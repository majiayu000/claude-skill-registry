---
name: android-restart-app
description: Restart the Android app on connected device without rebuilding. Force-stops and relaunches the app remotely. Use when testing changes that don't require rebuild, or refreshing app state.
---

# Android Restart App

## Overview

Restarts the Android app on a connected device by force-stopping the existing instance and launching it again. This is useful for testing configuration changes, clearing app state, or refreshing the app without rebuilding.

## When to Use

Invoke this skill when the user:
- Asks to "restart the Android app"
- Wants to "reload the app"
- Says "relaunch on device"
- Mentions refreshing or resetting the Android app
- Wants to test without rebuilding

## Prerequisites

- Android device connected via USB
- App must be installed on the device (use android-deploy-usb first if not)
- USB debugging enabled
- ADB installed
- Device authorized

## Instructions

1. Navigate to the Android app directory:
   ```bash
   cd path/to/android/app
   ```

2. Run the restart script:
   ```bash
   ./restart-app.sh
   ```

3. The script will:
   - Force-stop the running app with `adb shell am force-stop`
   - Launch the app again with `adb shell am start`
   - Activate it (bring to foreground)

4. Inform the user:
   - The app has been restarted on the device
   - This does NOT rebuild - only restarts the existing installation
   - Use android-deploy-usb if code changes need to be deployed first

## Expected Output

```
🔄 Restarting NoobTest on device...
✅ App restarted
```

## How It Works

The script uses:
- `adb shell am force-stop com.miso.noobtest` to kill the app process
- `adb shell am start -n com.miso.noobtest/.MainActivity` to launch again

## When to Use vs Deploy

**Use restart-app when**:
- Testing configuration files or assets that don't require rebuild
- Clearing app state (memory, caches)
- You just want to refresh the running app
- Changes are external (server-side, network config, etc.)

**Use android-deploy-usb when**:
- You changed Kotlin code
- You added/modified UI (Compose)
- You updated dependencies in build.gradle.kts
- Any code that needs recompilation

## Common Issues

**"no devices found"**:
- Check USB connection
- Ensure USB debugging is enabled
- Verify device authorized: `adb devices`
- Try: `adb kill-server && adb start-server`

**App not installed**:
- Run android-deploy-usb first to build and install
- Verify app on device home screen or app drawer

**App doesn't start**:
- Check logcat for errors: `adb logcat | grep NoobTest`
- Verify MainActivity class name matches package
- Check app permissions if needed

## Speed

This is very fast (< 2 seconds) since there's no build step. It's ideal for rapid iteration when testing non-code changes or clearing app state.

## Package Name

The script is configured for the specific app's package name. For Firefly/NoobTest, this is `com.miso.noobtest`. Different apps will have different package names configured in build.gradle.kts under `applicationId`.

## Force-Stop Note

`adb shell am force-stop` is a clean shutdown that:
- Stops all app processes
- Clears memory but keeps app data
- Safer than killing process with `kill` command
- Recommended way to stop Android apps during development
