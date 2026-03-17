---
name: setup-android
description: >-
  Set up Android development environment for React Native/Expo.
  Use when configuring Android Studio, Gradle, emulators, or troubleshooting
  Android-specific build issues.
  Invoked by: "android setup", "android studio", "gradle", "android environment", "android emulator".
---

# Android Development Setup SOP

**Version**: 1.0.0
**Last Updated**: 2026-01-11
**Status**: Active

> **Note**: This is a template. Replace placeholders like `{PROJECT_NAME}` and `{BUNDLE_ID}` with your actual project values.

---

## Overview

### Purpose
Configure a complete Android development environment for building and running the mobile app on Android emulators and physical devices. This guide covers JDK installation, Android Studio setup, SDK configuration, emulator creation, and environment variables.

### When to Use
**ALWAYS**: Setting up Android development on macOS/Windows/Linux, Android Studio configuration, emulator setup, Gradle issues, SDK configuration
**SKIP**: iOS-only development, web development

---

## Quick Start

1. **Install JDK 17**: `brew install openjdk@17` (macOS) or Adoptium (Windows)
2. **Install Android Studio**: Download from developer.android.com/studio
3. **Configure SDK**: Install Android 14 (API 34) via SDK Manager
4. **Set Environment Variables**: Add ANDROID_HOME and PATH entries
5. **Create Emulator**: Tools > Device Manager > Create Device
6. **Run**: `task run-android`

---

## Process Workflow

### Flow Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Install JDK    │────>│  Install        │────>│  Configure      │
│  17             │     │  Android Studio │     │  SDK            │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                                                        v
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│  Run on         │<────│  Create         │<────│  Set Env        │
│  Emulator       │     │  Emulator       │     │  Variables      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
```

### Phase Summary
| Phase | Description | Time |
|-------|-------------|------|
| 1 | Install JDK 17 | 5-10 min |
| 2 | Install Android Studio | 15-30 min |
| 3 | Configure SDK | 10 min |
| 4 | Set Environment Variables | 5 min |
| 5 | Create Emulator | 10 min |
| 6 | Verify Installation | 5 min |

---

## Phase 1: Install JDK 17

Android requires JDK 17.

### macOS

```bash
brew install openjdk@17

# Add to PATH (add to ~/.zshrc or ~/.bashrc)
export JAVA_HOME=$(/usr/libexec/java_home -v 17)
export PATH="$JAVA_HOME/bin:$PATH"
```

### Windows

Download and install from [Adoptium](https://adoptium.net/) (Eclipse Temurin JDK 17).

### Linux

```bash
sudo apt install openjdk-17-jdk
```

### Verify Installation

```bash
java --version
# Should show version 17.x.x
```

---

## Phase 2: Install Android Studio

### Download

Download from [developer.android.com/studio](https://developer.android.com/studio)

### Installation Components

During installation, ensure these components are selected:

- Android SDK
- Android SDK Platform
- Android Virtual Device (AVD)

### First Launch

1. Open Android Studio
2. Complete the setup wizard
3. Accept all license agreements

---

## Phase 3: Configure SDK

### Open SDK Manager

1. Open **Android Studio**
2. Go to **Settings/Preferences > Languages & Frameworks > Android SDK**

### SDK Platforms

In **SDK Platforms** tab, install:
- Android 14 (API 34) - or latest

### SDK Tools

In **SDK Tools** tab, ensure these are installed:
- Android SDK Build-Tools
- Android SDK Command-line Tools
- Android Emulator
- Android SDK Platform-Tools

---

## Phase 4: Set Environment Variables

### macOS / Linux

Add to your shell profile (`~/.zshrc` or `~/.bashrc`):

```bash
# macOS
export ANDROID_HOME=$HOME/Library/Android/sdk

# Linux
# export ANDROID_HOME=$HOME/Android/Sdk

export PATH=$PATH:$ANDROID_HOME/emulator
export PATH=$PATH:$ANDROID_HOME/platform-tools
export PATH=$PATH:$ANDROID_HOME/tools
export PATH=$PATH:$ANDROID_HOME/tools/bin
```

Then reload your shell:
```bash
source ~/.zshrc  # or ~/.bashrc
```

### Windows

1. Open **System Properties > Environment Variables**
2. Add new System Variable:
   - Name: `ANDROID_HOME`
   - Value: `C:\Users\<username>\AppData\Local\Android\Sdk`
3. Add to `Path`:
   - `%ANDROID_HOME%\emulator`
   - `%ANDROID_HOME%\platform-tools`

### Verify

```bash
adb --version
# Should output version info
```

---

## Phase 5: Create Android Emulator

### Using Android Studio

1. Open **Android Studio**
2. Go to **Tools > Device Manager** (or click phone icon in toolbar)
3. Click **Create Device**
4. Select a device (e.g., Pixel 7)
5. Select a system image (API 34 recommended)
6. Click **Finish**

### Start Emulator

From Android Studio:
- Click the **Play** button next to your device in Device Manager

From command line:
```bash
# List available emulators
emulator -list-avds

# Start emulator
emulator -avd <avd_name>
```

---

## Phase 6: Verify Installation

### Run All Checks

```bash
# Check Java version
java --version

# Check ADB
adb --version

# Check emulator
emulator -list-avds

# Check connected devices
adb devices
```

### Test Android Build

```bash
# Ensure environment is set up
task setup-dev

# Start emulator first (from Android Studio or command line)
# Then run
task run-android
```

---

## Running on Android Emulator

### Quick Start

```bash
# Ensure environment is set up
task setup-dev

# Start emulator first (from Android Studio or command line)
# Then run
task run-android
```

### Verify Device Connection

```bash
adb devices
# Should list your emulator or connected device
```

---

## Running on Physical Device

### Enable Developer Options

1. Go to **Settings > About Phone**
2. Tap **Build Number** 7 times
3. Go back to **Settings > Developer Options**
4. Enable **USB Debugging**

### Connect Device

1. Connect via USB
2. Accept the debugging prompt on your device
3. Verify connection:
   ```bash
   adb devices
   # Should list your device
   ```

### Run

```bash
task run-android
```

---

## Debugging with React Native

### Enable Hot Reload

1. Shake device or press `Cmd+M` (macOS) / `Ctrl+M` (Windows)
2. Select **Enable Fast Refresh**

### Open Developer Menu

- Emulator: `Cmd+M` (macOS) or `Ctrl+M` (Windows)
- Physical device: Shake the device

### View Logs

```bash
# All React Native logs
adb logcat *:S ReactNative:V ReactNativeJS:V

# Filter for your app (replace with your bundle ID)
adb logcat | grep "{BUNDLE_ID}"
```

### Connect Debugger

1. Open Developer Menu
2. Select **Debug with Chrome** or **Open Debugger**
3. Chrome DevTools will open at `localhost:8081/debugger-ui`

---

## Android Studio Tips

### Sync Gradle

If you see Gradle sync issues:

1. Open `android/` folder in Android Studio
2. Click **Sync Project with Gradle Files** (elephant icon)

### Invalidate Caches

For strange build issues:

1. **File > Invalidate Caches**
2. Select **Invalidate and Restart**

---

## Quick Reference

### Common Commands

```bash
# Run on Android
task run-android

# Build native project only
task build-android

# Regenerate native project
task generate

# Connect ADB for debugging
task adb-connect

# View logs
adb logcat | grep "ReactNative"

# List devices
adb devices

# List emulators
emulator -list-avds

# Start emulator
emulator -avd <avd_name>
```

### ADB Commands

```bash
# List devices
adb devices

# Install APK
adb install app.apk

# Uninstall app (replace with your bundle ID)
adb uninstall {BUNDLE_ID}

# Clear app data (replace with your bundle ID)
adb shell pm clear {BUNDLE_ID}

# Reverse port (for Metro connection)
adb reverse tcp:8081 tcp:8081

# Take screenshot
adb exec-out screencap -p > screenshot.png

# Record screen
adb shell screenrecord /sdcard/recording.mp4
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "SDK location not found" | Create `android/local.properties` with `sdk.dir=/Users/<username>/Library/Android/sdk` |
| "INSTALL_FAILED_INSUFFICIENT_STORAGE" | Run `emulator -avd <avd_name> -wipe-data` or increase storage in AVD settings |
| "Unable to load script" | Start Metro with `task start`, then run `task run-android`; for physical device run `adb reverse tcp:8081 tcp:8081` |
| Emulator slow | Enable hardware acceleration (HAXM/Hypervisor), use x86_64 images, allocate more RAM |
| Build fails with memory error | Add `org.gradle.jvmargs=-Xmx4g -XX:MaxMetaspaceSize=512m` to `android/gradle.properties` |
| JAVA_HOME not set | Add `export JAVA_HOME=$(/usr/libexec/java_home -v 17)` to shell profile |
| Gradle sync failed | Open android/ in Android Studio and click "Sync Project with Gradle Files" |
| ADB not found | Ensure `ANDROID_HOME` and PATH are set correctly |

---

## Node.js Version Management

For consistent Node.js versions, use Volta (same as iOS setup):

```bash
# Install Volta
curl https://get.volta.sh | bash

# Setup Node 20
volta install node@20
volta pin node@20
```

Verify:
```bash
node --version  # Should show v20.x.x
volta --version # Should show version info
```

---

## Related Skills

| Skill | Purpose | When to Use |
|-------|---------|-------------|
| `/setup-dev` | Full environment setup | Complete development environment |
| `/setup-ios` | iOS environment | Setting up iOS development |
| `/setup-env` | Environment variables | Configuring .env files |
| `/help` | Issue diagnosis | When encountering build errors |
| `/deploy` | App deployment | Building for Play Store |

> **Note**: Skill paths (`/skill-name`) work after deployment. In the template repo, skills are in domain folders.

---

**End of SOP**
