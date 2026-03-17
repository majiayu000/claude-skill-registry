---
name: android-deploy-usb
description: Build and deploy Android app to connected device via USB. Fast deployment (~2-5 seconds) using Gradle and ADB. Use when deploying, installing, or building Android apps to physical devices.
---

# Android USB Deploy

## Overview

Builds an Android app using Gradle and installs it directly to a USB-connected Android device via ADB (Android Debug Bridge). This is the fastest way to test on real hardware during development.

## When to Use

Invoke this skill when the user:
- Asks to "deploy to Android"
- Wants to "install the app on device"
- Says "build and deploy Android"
- Mentions testing on physical Android device
- Wants to "push to device"

## Prerequisites

- Android device connected via USB
- **USB Debugging enabled** (Settings → System → Developer options → USB debugging)
- **Developer Mode enabled** (Settings → About Phone → tap Build number 7 times)
- ADB installed (`brew install android-platform-tools` on macOS)
- Device authorized for debugging (RSA key accepted)
- **JAVA_HOME** must be set: `export JAVA_HOME="/opt/homebrew/opt/openjdk"`

## Instructions

1. Navigate to the Android app directory (look for build.gradle.kts):
   ```bash
   cd path/to/android/app
   ```

2. Set JAVA_HOME environment variable:
   ```bash
   export JAVA_HOME="/opt/homebrew/opt/openjdk"
   ```

3. Run the install-device.sh script:
   ```bash
   ./install-device.sh
   ```

4. The script will:
   - Check if device is connected via `adb devices`
   - Build the APK with `./gradlew assembleDebug`
   - Install with `adb install -r app/build/outputs/apk/debug/app-debug.apk`
   - Launch the app with `adb shell am start`

5. Inform the user:
   - Initial build may take longer (~10-30 seconds)
   - Subsequent builds are faster (~2-5 seconds)
   - App will launch automatically on device
   - Check device screen to see the app running

## Expected Output

```
📱 Installing NoobTest to connected device...
✅ Found device: ABC123XYZ
🔨 Building...
✅ Build complete
📲 Installing...
✅ Installation complete
🚀 Launching app...
🎉 App installed and launched!
```

## How It Works

The deployment process:
1. **Check device**: `adb devices` confirms connection
2. **Build APK**: `./gradlew assembleDebug` compiles the app
3. **Install**: `adb install -r` (replace existing installation)
4. **Launch**: `adb shell am start -n com.miso.noobtest/.MainActivity`

## Common Issues

**"no devices found"**:
- Enable USB debugging in Developer Options
- Accept RSA authorization prompt on device
- Try: `adb kill-server && adb start-server`
- Check USB cable supports data (not just charging)

**"Unable to locate a Java Runtime"**:
- Set JAVA_HOME: `export JAVA_HOME="/opt/homebrew/opt/openjdk"`
- Verify: `echo $JAVA_HOME`
- Install OpenJDK if missing: `brew install openjdk`

**"INSTALL_FAILED_UPDATE_INCOMPATIBLE"**:
- App signatures don't match existing installation
- Uninstall first: `adb uninstall com.miso.noobtest`
- Try installation again

**"device unauthorized"**:
- Check device screen for RSA key authorization prompt
- Accept the authorization
- Replug device and try again

**"adb: command not found"**:
- Install Android platform tools: `brew install android-platform-tools`

## Build Speed

- **First build**: ~10-30 seconds (downloads dependencies)
- **Incremental builds**: ~2-5 seconds
- Much faster than iOS due to Gradle's incremental compilation

## Package Name

The script is configured for the specific app's package name (e.g., `com.miso.noobtest` for Firefly/NoobTest). Different apps have different package names configured in build.gradle.kts.

## Gradle Note

Always set `JAVA_HOME` before running Gradle commands. This is a critical requirement on macOS with Homebrew-installed Java.

