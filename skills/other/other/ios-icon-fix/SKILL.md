---
name: ios-icon-fix
description: Remove alpha channel (transparency) from iOS app icons. Apple App Store rejects icons with transparency. Use this after regenerating app icons or before iOS archive/upload to fix the "Invalid large app icon - can't be transparent or contain an alpha channel" error.
---

# iOS Icon Fix

Remove alpha channel from iOS app icons to comply with Apple App Store requirements.

## When to Use

- Before uploading to App Store Connect / TestFlight
- After regenerating iOS app icons
- When you see error: "Invalid large app icon... can't be transparent or contain an alpha channel"

## Usage

Run the script:

```bash
python3 .claude/skills/ios-icon-fix/scripts/remove_alpha.py
```

Or specify a custom path:

```bash
python3 .claude/skills/ios-icon-fix/scripts/remove_alpha.py path/to/AppIcon.appiconset
```

## What It Does

1. Finds all PNG icons in the appiconset directory
2. For each icon with alpha channel:
   - Creates white background
   - Composites the icon onto it
   - Saves without alpha
3. Verifies all icons have no transparency

## Requirements

- Python 3
- Pillow: `pip install Pillow`

## Default Icon Location

```
decentpaste-app/src-tauri/gen/apple/Assets.xcassets/AppIcon.appiconset/
```
