---
name: emumanager
description: >
  Manages Android SDK, emulators, and AVDs. Use when bootstrapping Android SDK,
  creating/starting/stopping AVDs, downloading system images, or troubleshooting
  emulator issues. Supports mobile, Wear OS, TV, and Automotive devices. Covers
  sdkmanager, avdmanager, emulator CLI. Triggers: android emulator, android
  virtual device, avd, system image, wear os emulator, tv emulator, automotive
  emulator, bootstrap android sdk.
compatibility: >
  Requires Java 17+, curl, and unzip. Hardware acceleration (KVM on Linux, HVF
  on macOS) required for emulators. Needs network access for downloading SDK
  components. Designed for filesystem-based agents with bash access.
---

# Android Emulator Manager

## Important: Use Script First

**ALWAYS use `scripts/emumanager` over raw `sdkmanager`, `avdmanager`, or
`emulator` commands.** The script is located in the `scripts/` subdirectory of
this skill's folder. It provides features that raw commands do not:

- Automatic system image selection for device types (--mobile, --wear, --tv)
- Boot completion detection with timeout
- Sensible defaults and helpful error messages
- Diagnostics via `doctor` subcommand

**When to read the script source:** If the script doesn't do exactly what you
need, or fails due to missing dependencies, read the script source. It encodes
solutions to SDK quirks and boot detection edge cases—use it as reference when
building similar functionality.

## Quick Start

### Environment Variables

```bash
export ANDROID_HOME="${ANDROID_HOME:-$HOME/.local/share/android-sdk}"
export ANDROID_USER_HOME="${ANDROID_USER_HOME:-$HOME/.android}"
```

### Prerequisites

- Java 17 or higher
- Hardware acceleration: KVM on Linux, HVF (Hypervisor Framework) on macOS
- Network access for downloading SDK components

### Highest-Value Commands

```bash
# First-time setup (installs cmdline-tools, platform-tools, build-tools, emulator)
scripts/emumanager bootstrap

# Diagnose issues (Java version, hardware acceleration, disk space)
scripts/emumanager doctor

# Create a mobile/phone AVD with latest API
scripts/emumanager create my_phone --mobile

# Start the AVD
scripts/emumanager start my_phone

# List all AVDs (shows running status)
scripts/emumanager list

# Show detailed AVD information
scripts/emumanager info my_phone
```

## Subcommand Overview

### bootstrap

Set up SDK environment. Installs cmdline-tools, platform-tools, build-tools,
emulator, and a platform.

```bash
scripts/emumanager bootstrap
scripts/emumanager bootstrap --no-emulator  # Skip emulator installation
```

### doctor

Run diagnostics to check for common issues: Java version, hardware acceleration,
SDK tools, disk space, orphaned AVD files.

```bash
scripts/emumanager doctor
```

### list

List all available AVDs with running status.

```bash
scripts/emumanager list              # Show all AVDs with status
scripts/emumanager list --names-only # Just AVD names
scripts/emumanager list --running-only
scripts/emumanager list --stopped-only
```

### info

Show detailed information about an AVD: system image, API level, screen config,
RAM, storage, Play Store status.

```bash
scripts/emumanager info my_phone
```

### create

Create a new AVD with device type or specific image.

```bash
scripts/emumanager create my_phone --mobile   # Mobile/phone (default)
scripts/emumanager create my_watch --wear     # Wear OS
scripts/emumanager create my_tv --tv          # Android/Google TV
scripts/emumanager create my_car --auto       # Android Automotive

# With specific system image
scripts/emumanager create my_avd "system-images;android-36;google_apis_playstore;arm64-v8a"
```

### start

Start an AVD. Waits for boot to complete.

```bash
scripts/emumanager start my_phone              # Quick Boot (fast)
scripts/emumanager start my_phone --cold-boot  # Cold boot (bypass snapshots)
scripts/emumanager start my_phone --wipe-data  # Factory reset + cold boot
```

### stop

Stop a running AVD.

```bash
scripts/emumanager stop my_phone
```

### delete

Delete an AVD and clean up files. Stops the AVD first if running.

```bash
scripts/emumanager delete my_phone
```

### download

Download a specific system image.

```bash
scripts/emumanager download "system-images;android-36;google_apis_playstore;arm64-v8a"
```

### images

List available system images for the host architecture (API level >= 33).
Installed images are marked with `*`.

```bash
scripts/emumanager images
```

### outdated

Show outdated SDK packages.

```bash
scripts/emumanager outdated
```

### update

Update all installed SDK packages to latest versions.

```bash
scripts/emumanager update
```

## Device Types

The `create` command supports device type flags that automatically select the
latest appropriate system image for the host architecture:

| Flag                 | Device Type       | System Image Pattern                   |
| -------------------- | ----------------- | -------------------------------------- |
| `--mobile`/`--phone` | Mobile/Phone      | `google_apis_playstore`                |
| `--wear`/`--watch`   | Wear OS           | `android-wear` / `android-wear-signed` |
| `--tv`               | Android/Google TV | `android-tv` / `google-tv`             |
| `--auto`             | Automotive        | `android-automotive-playstore`         |

If no device type or image is specified, defaults to mobile/phone.

## Start Mode Options

| Mode          | Flag          | Description                          |
| ------------- | ------------- | ------------------------------------ |
| Quick Boot    | (default)     | Fast startup using snapshots         |
| Cold Boot     | `--cold-boot` | Bypass Quick Boot, perform full boot |
| Factory Reset | `--wipe-data` | Wipe all data and cold boot          |

## Common Workflows

### First-Time Setup

```bash
scripts/emumanager bootstrap
scripts/emumanager doctor
```

### Creating and Running a Phone Emulator

```bash
scripts/emumanager create my_phone --mobile
scripts/emumanager start my_phone
```

### Creating a Wear OS Emulator

```bash
scripts/emumanager create my_watch --wear
scripts/emumanager start my_watch
```

### Factory Resetting an AVD

```bash
scripts/emumanager start my_phone --wipe-data
```

### Checking for SDK Updates

```bash
scripts/emumanager outdated
scripts/emumanager update
```

## Safety Notes

- Script requires Java 17+ to run SDK tools
- Hardware acceleration (KVM/HVF) is required for x86_64/arm64 emulators
- System image downloads can be several GB
- Some operations require network access
- The script avoids destructive actions unless explicitly requested
- Use `ANDROID_SERIAL` environment variable when multiple emulators are running

## Reference Documentation

- `references/command-index.md` - Detailed subcommand reference
- `references/troubleshooting.md` - Common issues and solutions
