---
name: iphone-screen-capture
description: Start the iPhone screen capture app to mirror a connected iPhone's screen on macOS. Use when the user wants to view their iPhone screen, mirror their device, or start screen capture.
---

# iPhone Screen Capture

## Overview

Native macOS app that mirrors a connected iPhone's screen on the Mac desktop using AVFoundation. Features an integrated console for live app logs via `pymobiledevice3`.

## When to Use

Invoke this skill when the user:
- Asks to "start screen capture"
- Wants to "see their iPhone screen"
- Wants to "mirror their iPhone"
- Mentions viewing or displaying their connected device
- Says "show me my phone"

## Prerequisites

- iPhone connected via USB
- Device trusted (tap "Trust This Computer" on iPhone)
- `pymobiledevice3` installed for console logs (`pip3 install pymobiledevice3`)

## Instructions

1. Navigate to the screen capture directory:
   ```bash
   cd miso/platforms/ios/development/screen-capture/imp
   ```

2. Run the screen capture script:
   ```bash
   ./iphone_screencap.sh
   ```

## Features

- **Borderless window** (390x844) styled like an iPhone
- **Console toggle**: Click ">" button in top-right to open live log panel
- **Click to resize**: Click window to toggle between full and half size
- **Draggable**: Move window by clicking and dragging anywhere
- **Live logs**: Console shows `[APP]` prefixed logs via `pymobiledevice3 syslog`

## What to Tell the User

- A borderless window will appear showing their iPhone screen
- **Click the ">" button** to open the console panel with live logs
- **Click anywhere** on the window to toggle full/half size
- Close window or Cmd+Q to quit

## Taking Screenshots

```bash
./screenshot.sh /tmp/screenshot.png
```

## Reading Logs (for Claude)

When console is open, logs stream via pymobiledevice3. Claude can also read logs with:
```bash
pymobiledevice3 syslog live 2>/dev/null | grep "\[APP\]" | head -20
```

## Troubleshooting

**iPhone screen not showing**:
- Check USB connection
- Ensure iPhone is unlocked
- Accept "Trust This Computer" prompt
- Disconnect and reconnect device

**Console not working**:
- Install pymobiledevice3: `pip3 install pymobiledevice3`
- Check device is trusted

## Files

- `main.swift` - Native macOS app source
- `build.sh` - Compiles the Swift app
- `iphone_screencap.sh` - Builds (if needed) and launches
- `screenshot.sh` - Captures device screenshot
