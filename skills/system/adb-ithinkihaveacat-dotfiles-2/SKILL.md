---
name: adb
description: >
  Manipulates Android devices via ADB with emphasis on Wear OS. Provides scripts
  for screenshots, screen recording, tile management, WearableService
  inspection, package operations, and device configuration. Use when working
  with adb, Android devices, Wear OS watches, tiles, wearable data layer,
  dumpsys, or device debugging. Triggers: adb, android device, wear os,
  wearable, tile, screenshot, screen recording, dumpsys, logcat.
compatibility: >
  Requires adb. Some scripts require magick (ImageMagick), aapt, or scrcpy.
  Designed for filesystem-based agents with bash access.
---

# Android ADB

## Important: Use Scripts First

**ALWAYS prefer the scripts in `scripts/` over raw `adb` commands.** Scripts are
located in the `scripts/` subdirectory of this skill's folder. They provide
features that raw commands do not, such as:

- Automatic circular masking for Wear OS screenshots
- Device wake-up before capture
- Clipboard integration on macOS
- Sensible default filenames and error handling

**When to read the script source:** If a script doesn't do exactly what you
need, or fails due to missing dependencies, read the script source. The scripts
encode solutions to edge cases and platform quirks that may not be obvious—use
them as reference when building similar functionality.

## Quick Start

Target specific devices using the `ANDROID_SERIAL` environment variable if
multiple devices are connected.

### Highest-Value Commands

- **Screenshot (auto-masks circular Wear OS displays):**
  `scripts/adb-screenshot`

- **Wear OS Tile Debugging Workflow:**
  `scripts/adb-tile-add com.example/.MyTileService` -> output gives INDEX
  `scripts/adb-tile-show INDEX`

- **Inspect Wear OS Data Layer:** `scripts/wearableservice-capabilities`
  `scripts/wearableservice-nodes`

- **Package Information:** `scripts/packagename tiles PACKAGE_NAME`
  `scripts/packagename services PACKAGE_NAME`

- **Device Info:** `scripts/adb-device-properties`

- **Discover Activities:** `scripts/adb-activities` (find launcher, TV, settings
  activities)

## Script Index

See `references/command-index.md` for detailed usage.

### Device Basics

- `scripts/adb-devices`: List connected devices.
- `scripts/adb-device-properties`: Show key device properties (model,
  manufacturer, etc.).
- `scripts/adb-api-level`: Get the device API level (SDK version).
- `scripts/adb-keyevent-wakeup` / `sleep`: Wake up or put device to sleep.

### Media Capture

- `scripts/adb-screenshot`: Take a screenshot. **Always use this instead of raw
  `adb shell screencap`.** Features: auto-detects square Wear OS displays and
  applies circular mask, wakes device before capture, copies to macOS clipboard,
  generates timestamped filenames by default.
- `scripts/adb-screenrecord`: Record the screen to a file.

### Tile Management (Wear OS)

- `scripts/adb-tile-add`: Add a tile component for debugging.
- `scripts/adb-tile-show`: Show an added tile.
- `scripts/adb-tile-remove`: Remove a tile.
- `scripts/adb-tiles`: List currently added tiles.

### Activity Discovery

- `scripts/adb-activities`: List activities tagged by category (Launcher, Home,
  TV/Leanback, Settings). Use `--launcher-only`, `--tv-only`, `--settings-only`
  to filter. Add `--all` to include system apps.

### Package Operations

- `scripts/packagename`: Comprehensive package tool (uninstall, launch, stop,
  clear-cache).
- `scripts/adb-logcat-package`: Show logcat filtered for a specific package.
- `scripts/apk-tiles`: List tiles declared in an APK file.

### Wear OS Data Layer

- `scripts/wearableservice-capabilities`: Dump advertised capabilities.
- `scripts/wearableservice-nodes`: List connected nodes.
- `scripts/wearableservice-items`: List data items.

### Display & Demo Mode

- `scripts/adb-demo-on` / `off`: Toggle Android demo mode (clean status bar).
- `scripts/adb-fontscale-default` / `large`: Change font size.
- `scripts/adb-settings-theme`: Toggle dark/light theme.
- `scripts/adb-touches-on` / `off`: Show/hide taps on screen.

## Safety Notes

- **Debug Broadcasts**: Tile management relies on Wear OS debug broadcasts
  (`com.google.android.wearable.app.DEBUG_SURFACE`) which may not work on
  production builds without developer options or specific system images.
- **USB Debugging**: Requires `adb` authorization.
- **Destructive Actions**: Scripts like `adb-tile-remove` or
  `packagename uninstall` modify device state.
