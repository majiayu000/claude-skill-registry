---
name: adb
description: >
  Manipulates Android devices via ADB with emphasis on Wear OS. Provides scripts
  for screenshots, screen recording, tile management, WearableService
  inspection, package operations, and device configuration. Use when working
  with adb, Android devices, Wear OS watches, tiles, wearable data layer,
  dumpsys, or device debugging.
compatibility: >
  Requires adb. Some scripts require magick (ImageMagick), aapt, or scrcpy.
  Designed for filesystem-based agents with bash access.
---

# Android ADB

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

See `references/command-index.md` for detailed usage and raw ADB equivalents.

### Device Basics

- `scripts/adb-devices`: List connected devices.
- `scripts/adb-device-properties`: Show key device properties (model,
  manufacturer, etc.).
- `scripts/adb-api-level`: Get the device API level (SDK version).
- `scripts/adb-keyevent-wakeup` / `sleep`: Wake up or put device to sleep.

### Media Capture

- `scripts/adb-screenshot`: Take a screenshot (handles Wear OS round screens).
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

## Raw ADB Fallback

If scripts fail (e.g., missing dependencies like `magick`), inspect the script
to find the core `adb` command.

1. Open the script in `scripts/`.
2. Find the `require` lines to identify dependencies.
3. Locate the core `adb` command(s).
4. Run them manually.

### Examples

#### Tile Workflow (Wear OS)

```bash
# From adb-tile-add:
adb shell am broadcast \
  -a com.google.android.wearable.app.DEBUG_SURFACE \
  --es operation add-tile \
  --ecn component "com.example/.MyTileService"

# From adb-tile-show:
adb shell am broadcast \
  -a com.google.android.wearable.app.DEBUG_SYSUI \
  --es operation show-tile \
  --ei index 0
```

#### WearableService Dump

```bash
# From wearableservice-capabilities:
adb exec-out dumpsys activity service WearableService | \
  sed -n '/CapabilityService/,/######/p'
```

#### Screenshot With Circular Mask

```bash
# From adb-screenshot (for square Wear OS displays):
adb exec-out "screencap -p" | magick - \
  -alpha set -background none -fill white \
  \( +clone -channel A -evaluate set 0 +channel \
     -draw "circle %[fx:(w-1)/2],%[fx:(h-1)/2] %[fx:(w-1)/2],0.5" \) \
  -compose dstin -composite output.png
```

#### Activity Discovery

```bash
# From adb-activities: Query launcher activities
adb shell cmd package query-activities \
  -a android.intent.action.MAIN \
  -c android.intent.category.LAUNCHER

# Query TV/Leanback activities
adb shell cmd package query-activities \
  -a android.intent.action.MAIN \
  -c android.intent.category.LEANBACK_LAUNCHER

# Query settings activities
adb shell cmd package query-activities \
  -c android.intent.category.PREFERENCE
```

## Safety Notes

- **Debug Broadcasts**: Tile management relies on Wear OS debug broadcasts
  (`com.google.android.wearable.app.DEBUG_SURFACE`) which may not work on
  production builds without developer options or specific system images.
- **USB Debugging**: Requires `adb` authorization.
- **Destructive Actions**: Scripts like `adb-tile-remove` or
  `packagename uninstall` modify device state.
