---
name: android-local-build-debug
description: Build, install, and debug TermLink on real Android devices with adb. Use for local packaging, selecting target serials (da34332c or MQS7N19402011743), launching the app, collecting logcat, and reproducing mobile issues.
---

# Android Local Build Debug

Use this skill for repeatable local Android build + install + real-device debugging.

Run commands from repository root:
`E:\coding\TermLink`

## Target Devices

Use this priority by default:
1. `da34332c`
2. `MQS7N19402011743`

If multiple devices are online, always pass `-Serial`.

## Default Debug Configuration

The file `android/local-debug-config.json` contains default server profile for debug builds:
- Base URL: `http://192.168.50.12:3010`
- Terminal Type: `TERMLINK_WS`
- Auth Type: `BASIC`
- Username: `admin`
- Password: `admin`

This file is gitignored and will be copied to APK assets during build.

## Quick Start

1. Build debug APK:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/build-debug-apk.ps1
```

2. Install and launch:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/install-debug-apk.ps1
```

3. Stream logs:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/logcat-termlink.ps1
```

4. Validate local server config:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/validate-server-config.ps1
```

## Standard Debug Loop

1. Run doctor:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/adb-doctor.ps1
```

2. Rebuild and reinstall:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/build-debug-apk.ps1
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/install-debug-apk.ps1 -Serial da34332c
```

3. Launch app:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/launch-termlink.ps1 -Serial da34332c
```

4. Reproduce issue and collect logs:
```powershell
powershell -ExecutionPolicy Bypass -File ./skills/android-local-build-debug/scripts/logcat-termlink.ps1 -Serial da34332c
```

## Rules

- Always use `adb -s <serial>` in scripts and manual commands.
- Keep package fixed to `com.termlink.app`.
- Prefer PID-filtered logcat; fall back to tag filter if PID is unavailable.
- Use JDK 21 for Android build.
- Store private validation URL in `local-config.ps1` (gitignored).
