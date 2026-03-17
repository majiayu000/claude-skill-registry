---
name: android-screen-capture
description: Start Android screen mirroring using scrcpy. Displays device screen in real-time on Mac with optional console logs. Use when viewing Android screen, mirroring device, or monitoring app with logs.
---

# Android Screen Capture

## Overview

Native macOS app that mirrors an Android device screen using `scrcpy` with an integrated console for live app logs. Matches the iPhone screen capture experience with a unified interface.

## When to Use

Invoke this skill when the user:
- Asks to "start Android screen capture"
- Wants to "see their Android screen"
- Wants to "mirror their Android device"
- Mentions viewing or displaying their Android device
- Says "show me my Android phone"

## Prerequisites

- Android device connected via USB
- **USB debugging enabled** (Settings → System → Developer options → USB debugging)
- **Developer Mode enabled** (Settings → About Phone → tap Build number 7 times)
- Device authorized for debugging
- **scrcpy installed**: `brew install scrcpy`
- **ADB installed**: `brew install android-platform-tools`

## Instructions

1. Navigate to screen capture directory:
   ```bash
   cd miso/platforms/android/development/screen-capture/imp
   ```

2. Run the screen capture app:
   ```bash
   ./android_screencap.sh
   ```

3. The app will:
   - Build automatically if needed
   - Detect your connected Android device
   - Launch scrcpy for screen mirroring
   - Show a toolbar with device info and console button

## Features

- **Integrated window**: Toolbar at top with scrcpy below
- **Console toggle**: Green ">" button opens live log panel
- **Click to resize**: Click the window to toggle full/half size
- **Draggable**: Drag by toolbar, scrcpy follows
- **Live logs**: Console shows `[APP]` prefixed logs from your app via `adb logcat`

## What to Tell the User

- A dark borderless window will appear with your Android screen
- **Green ">" button** in toolbar opens the console panel with live logs
- **Click anywhere** on the window to toggle between full and half size
- **Drag the toolbar** to move the window (scrcpy follows)
- Close window or Cmd+Q to quit

## Keyboard Shortcuts (in scrcpy area)

- **⌘+f**: Toggle fullscreen
- **⌘+r**: Rotate screen
- **⌘+g**: Resize to 1:1 (pixel-perfect)
- **⌘+c**: Copy device clipboard to computer

## Taking Screenshots

```bash
./screenshot.sh output_filename.png
```

## Reading Logs (for Claude)

```bash
adb logcat -v brief -d | grep "\[APP\]" | tail -30
```

## Common Issues

**"Device not found"**:
- Check USB debugging enabled
- Accept authorization prompt on device
- Verify with: `adb devices`

**scrcpy doesn't follow when dragging**:
- Grant accessibility permissions in System Settings → Privacy & Security → Accessibility

**scrcpy not installed**:
- Install: `brew install scrcpy`

**No logs in console**:
- Ensure app uses Logger with `[APP]` prefix
- Check app is running on device

## Files

- `main.swift` - Native macOS app source
- `build.sh` - Compiles the Swift app
- `android_screencap.sh` - Builds (if needed) and launches
- `screenshot.sh` - Captures device screenshot
