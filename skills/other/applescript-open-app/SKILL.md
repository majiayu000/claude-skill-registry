---
name: applescript-open-app
description: Open, launch, activate, or quit macOS apps by name using AppleScript or osascript. Use when the user asks to open/launch/activate/quit an app ("open Xcode", "quit Discord"), or when AppleScript-based app control is required.
---

# AppleScript Open App

## Overview
Use a performance-first launch path for opening apps (`open -a`) with AppleScript fallback for compatibility, and AppleScript for graceful quits.

## Quick Start
- Prefer `scripts/open_app.sh` for a reliable one-liner interface.
- Prefer `scripts/quit_app.sh` for quitting an app.
- Pass the app name exactly as it appears in Finder (for example, "Xcode", "Safari", "Final Cut Pro").

```bash
scripts/open_app.sh "Safari"
```
```bash
scripts/quit_app.sh "Discord"
```

## Tasks

### Open an app by name
- Run `scripts/open_app.sh "<App Name>"`.
- The script uses fast LaunchServices activation first, then falls back to AppleScript activation only when needed.
- If the app is not installed, surface the AppleScript error and ask for the correct name.

### Open a new instance (only when asked)
- Use `open -na "<App Name>"` only if the user explicitly requests a new instance.
- Otherwise use AppleScript activation.

### Quit an app by name
- Run `scripts/quit_app.sh "<App Name>"`.
- The script checks whether the app is running before sending `quit`, avoiding slow error-path exits for already-closed apps.
- If the app is not installed, surface the AppleScript error and ask for the correct name.

### Handle ambiguous names
- If multiple apps share a name, ask for the exact display name or bundle id.
- If a bundle id is provided, use AppleScript with `application id`.

```bash
osascript -e 'tell application id "com.apple.Safari" to activate'
```

## AppleScript snippet

```bash
osascript -e 'tell application "Safari" to activate'
```
```bash
osascript -e 'tell application "Safari" to quit'
```

## Resources

### scripts/
- `open_app.sh`: Fast `open -a` launch/activate with AppleScript fallback.
- `quit_app.sh`: Graceful AppleScript quit with running-state guard.
