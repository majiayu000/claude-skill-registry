---
name: android-watch-logs
description: Start real-time log streaming from connected Android device using adb logcat. Shows only app's log messages. Use when monitoring app behavior, debugging, or viewing Android logs.
---

# Android Watch Logs

## Overview

Streams logs from a USB-connected Android device in real-time using `adb logcat`, filtering to show only the app's explicit log messages (those with `[APP]` prefix).

## When to Use

Invoke this skill when the user:
- Asks to "watch Android logs"
- Wants to "see what the Android app is doing"
- Says "monitor the Android device"
- Asks to "stream logcat"
- Wants to debug or see real-time Android app behavior
- Says "show me the Android logs"

## Prerequisites

- Android device connected via USB
- USB debugging enabled
- ADB installed (`brew install android-platform-tools`)
- Device authorized for debugging
- App must be running on device to see logs

## Option 1: Use Screen Capture App (Recommended)

The Android screen capture app has an integrated console:

```bash
cd miso/platforms/android/development/screen-capture/imp
./android_screencap.sh
```

Click the green ">" button to open the live log console.

## Option 2: Terminal Streaming

Stream logs directly in terminal:

```bash
# Clear buffer and stream filtered logs
adb logcat -c && adb logcat -v brief | grep "\[APP\]"
```

## Option 3: Claude Reading Logs

Claude can read recent logs with:

```bash
adb logcat -v brief -d | grep "\[APP\]" | tail -30
```

## Log Format

The app's Logger class prefixes messages with `[APP]`:
```
I/MisoLogger(12345): [APP] [PostView] COMPOSE 14 'Dinner' expanded=false
I/MisoLogger(12345): [APP] [IMAGE_LOAD] COMPLETE 14 'Dinner' size=112KB time=261ms
```

## Adding Logs in Code

Use the app's Logger class in Kotlin:
```kotlin
Logger.info("[MyFeature] Something happened")
Logger.debug("[MyFeature] Debug info: $value")
Logger.error("[MyFeature] Error: ${e.message}")
```

Or directly with Android Log (add `[APP]` prefix):
```kotlin
Log.i("MisoLogger", "[APP] My message")
```

## Common Issues

**No logs appearing**:
- Ensure the app is running on the device
- Check that logs use `[APP]` prefix
- Verify adb is working: `adb devices`
- Try clearing log buffer: `adb logcat -c`

**adb not found**:
- Install: `brew install android-platform-tools`

**Device unauthorized**:
- Accept RSA key prompt on device
- Replug device and try again

## Notes

- The `[APP]` prefix filters out thousands of system messages
- Screen capture app console auto-scrolls to latest logs
- Use `-d` flag to dump logs without blocking (for scripts)
