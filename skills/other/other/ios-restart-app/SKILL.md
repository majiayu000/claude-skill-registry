---
name: ios-restart-app
description: Restart the iOS app on connected iPhone without rebuilding. Terminates and relaunches the app remotely. Use when testing changes that don't require rebuild, or refreshing app state.
---

# iOS Restart App

## Overview

Restarts the iOS app on a connected iPhone by terminating the existing instance and launching it again. This is useful for testing configuration changes, clearing app state, or refreshing the app without rebuilding.

## When to Use

Invoke this skill when the user:
- Asks to "restart the app"
- Wants to "reload the app"
- Says "relaunch on device"
- Mentions refreshing or resetting the app
- Wants to test without rebuilding

## Prerequisites

- iPhone connected via USB
- App must be installed on the device (use ios-deploy-usb first if not)
- Device trusted
- The project must be in an iOS app directory

## Instructions

1. Navigate to the iOS app directory:
   ```bash
   cd path/to/ios/app
   ```

2. Run the restart script:
   ```bash
   ./restart-app.sh
   ```

3. The script will:
   - Auto-detect the connected iPhone
   - Terminate any running instance of the app
   - Launch the app again
   - Activate it (bring to foreground)

4. Inform the user:
   - The app has been restarted on the device
   - This does NOT rebuild - only restarts the existing installation
   - Use ios-deploy-usb if code changes need to be deployed first

## Expected Output

```
🔄 Restarting NoobTest on device...
✅ App restarted
```

## How It Works

The script uses:
- `xcodebuild -showdestinations` to find the device ID
- `xcrun devicectl device process launch` with `--terminate-existing` to kill and restart
- `--activate` flag to bring the app to the foreground

## When to Use vs Deploy

**Use restart-app when**:
- Testing configuration files or assets that don't require rebuild
- Clearing app state (memory, caches)
- You just want to refresh the running app
- Changes are external (server-side, network config, etc.)

**Use ios-deploy-usb when**:
- You changed Swift code
- You added/modified UI
- You updated dependencies
- Any code that needs recompilation

## Common Issues

**No device detected**:
- Check USB connection
- Ensure device is trusted
- Try disconnecting and reconnecting

**App not installed**:
- Run ios-deploy-usb first to build and install
- Verify app appears on iPhone home screen

**Device busy**:
- Wait a moment and try again
- Stop any other Xcode operations

## Speed

This is very fast (< 2 seconds) since there's no build step. It's ideal for rapid iteration when testing non-code changes.

## Bundle ID

The script is configured for the specific app's bundle ID. For Firefly/NoobTest, this is `com.miso.noobtest`. Different apps will have different bundle IDs configured in the script.
