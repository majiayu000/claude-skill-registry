---
name: mobile-android
description: Android emulator, app commands, and ADB automation conventions.
---

# Mobile Android — Session Behavior + ADB Automation

## Mobile Commands (Session Behavior)

When the user asks to start the app in the emulator, run:
- `yarn mobile -- --start`

Before any mobile action (start/open/reload/stop/screenshot/tap/type/key), ensure the emulator is running by running:
- `yarn avd -- --start`

When the user asks to reload the app, run:
- `yarn mobile -- --send "r" C-m`

When the user asks to open the app, run:
- `yarn mobile -- --send "a"`
- `yarn mobile -- --send C-m`

When the user asks to start the app (generic), run:
- `yarn mobile -- --start`

When the user asks to stop the app, run:
- `yarn mobile -- --stop`

When the user asks to clear the app data, run:
- `yarn mobile -- --clear-app`

When the user asks to show mobile logs, run:
- `yarn mobile -- --logs`

When the user asks to take a snapshot/picture/screenshot of the app, run:
- `adb exec-out screencap -p > tmp/screenshot.png && img_to_public tmp/screenshot.png || echo 'Failed to capture screenshot'`

If the user asks for multiple actions (e.g., open the app and take a screenshot), apply each relevant command above in order without asking follow-up questions.

## APK Build (Session Behavior)

When the user asks to build the APK, run:
- `yarn build --android`

## Mobile UI Automation (ADB)

Taps and text input must follow these rules:
- Always capture a fresh screenshot before tapping when coordinates are inferred.
- If the user provides exact coordinates, tap without further confirmation.
- If the user names a UI element and coordinates are derived via `yarn mobile-ui -- --find` or `--tap-found`, tap immediately without asking for confirmation.
- If multiple devices are attached, ask which `adb` serial to use and include `-s <serial>` in all commands.

Commands:
- Tap: `adb shell input tap <x> <y>`
- Type text (focused input): `adb shell input text "<text>"`
- Key events (Enter/Back/etc.): `adb shell input keyevent <KEYCODE>`
- Helper (preferred): `yarn mobile-ui -- --tap x y`, `yarn mobile-ui -- --type "text"`, `yarn mobile-ui -- --key KEYCODE_ENTER`, `yarn mobile-ui -- --screenshot`
- UI element coordinates (preferred): use `yarn mobile-ui -- --find "<Element>"` to print the bbox and center point, then tap the center.
- One-step tap: `yarn mobile-ui -- --tap-found "<Element>"` (auto-screenshots if needed).

Examples:
- Tap coordinates: `yarn mobile-ui -- --tap 120 640`
- Type text: `yarn mobile-ui -- --type "hello"`
- Press Enter: `yarn mobile-ui -- --key KEYCODE_ENTER`

Screenshot retention:
- Keep latest at `tmp/screenshot.png` and also save timestamped copies in `tmp/screenshots/`.
