---
name: deploy
description: Build and deploy GridRacer to a connected iOS device
model: haiku
allowed-tools:
  - Bash
  - Read
---

# Deploy to Device

Build, install, and launch GridRacer on a connected physical iOS device.

## Usage

```bash
/deploy              # Deploy to first connected device
/deploy Willow       # Deploy to specific device by name
/deploy --build-only # Build without installing/launching
```

## Prerequisites

- Device connected via USB with Developer Mode enabled
- Device registered in your Apple Developer account
- Xcode signed in with your Apple ID (one-time setup)

## Steps

### 1. Find Connected Device

List available devices:
```bash
xcrun devicectl list devices 2>&1
```

Look for devices with `connected` state. If no device specified, use the first connected one.

**If no connected device found:**
```
No connected iOS device found.

Available devices:
  - Willow (unavailable)
  - Pj's Super Phone (unavailable)

Connect a device via USB and ensure Developer Mode is enabled.
```

### 2. Build for Device

```bash
xcodebuild -scheme GridRacer \
  -destination 'platform=iOS,name=DEVICE_NAME' \
  -allowProvisioningUpdates build 2>&1
```

Check for:
- `BUILD SUCCEEDED` - Continue to install
- `BUILD FAILED` - Report errors and stop

**Common build errors:**
- "Developer Mode disabled" - Enable in Settings > Privacy & Security
- "No Accounts" - Sign into Xcode with Apple ID
- "Provisioning profile doesn't include device" - Register device in Xcode

### 3. Install App

Find the built app:
```bash
APP_PATH=$(find ~/Library/Developer/Xcode/DerivedData/GridRacer-*/Build/Products/Debug-iphoneos -name "GridRacer.app" -type d | head -1)
```

Install to device:
```bash
xcrun devicectl device install app --device "DEVICE_NAME" "$APP_PATH" 2>&1
```

### 4. Launch App (unless --build-only)

```bash
xcrun devicectl device process launch --device "DEVICE_NAME" trouarat.GridRacer 2>&1
```

### 5. Report Summary

**Success:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
GridRacer deployed to DEVICE_NAME

Build:   Succeeded
Install: Succeeded
Launch:  Running

The app is now running on your device.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

**Build failed:**
```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Deploy failed: Build error

Errors:
  - Player.swift:42: error: ...

Fix build errors and try again.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
```

## Device Management

**List all devices:**
```bash
xcrun devicectl list devices
```

**Check device connection:**
```bash
xcrun xctrace list devices
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| "Developer Mode disabled" | Settings > Privacy & Security > Developer Mode > ON |
| "No connected device" | Check USB cable, trust computer on device |
| "Provisioning profile" error | Open Xcode once to register device |
| "No Accounts" error | Xcode > Settings > Accounts > Sign in |

## Examples

**Deploy to default device:**
```bash
/deploy
```

**Deploy to specific device:**
```bash
/deploy Willow
```

**Just build, don't launch:**
```bash
/deploy --build-only
```
