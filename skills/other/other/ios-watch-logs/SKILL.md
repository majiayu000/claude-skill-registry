---
name: ios-watch-logs
description: Start real-time log streaming from connected iPhone to console and file. Shows only app's explicit log messages with [APP] prefix. Use when monitoring app behavior, debugging, or viewing logs.
---

# iOS Watch Logs

## Overview

Streams logs from a USB-connected iPhone in real-time using `pymobiledevice3`, filtering to show only the app's explicit log messages (those with `[APP]` prefix).

## When to Use

Invoke this skill when the user:
- Asks to "watch iOS logs"
- Wants to "see what the app is doing"
- Says "monitor the iPhone"
- Asks to "stream logs from iPhone"
- Wants to debug or see real-time app behavior
- Says "show me the logs"

## Prerequisites

- iPhone connected via USB
- `pymobiledevice3` installed (`pip3 install pymobiledevice3`)
- Device must be trusted
- App must be running on the device to see logs

## Option 1: Use Screen Capture App (Recommended)

The iPhone screen capture app has an integrated console:

```bash
cd miso/platforms/ios/development/screen-capture/imp
./iphone_screencap.sh
```

Click the ">" button to open the live log console.

## Option 2: Terminal Streaming

Stream logs directly in terminal:

```bash
pymobiledevice3 syslog live 2>/dev/null | grep "\[APP\]"
```

## Option 3: Claude Reading Logs

Claude can read recent logs with:

```bash
timeout 3 pymobiledevice3 syslog live 2>/dev/null | grep "\[APP\]" | tail -30
```

## Log Format

The app's Logger class prefixes messages with `[APP]`:
```
NoobTest{...}[12345] <INFO>: [APP] [PostView] Loading post 14
NoobTest{...}[12345] <DEBUG>: [APP] [Network] Response: 200 OK
```

## Adding Logs in Code

Use the app's Logger class in Swift:
```swift
Logger.shared.info("[MyFeature] Something happened")
Logger.shared.debug("[MyFeature] Debug info: \(value)")
Logger.shared.error("[MyFeature] Error: \(error)")
```

## Common Issues

**No logs appearing**:
- Ensure the app is running on the device
- Check that logs use `[APP]` prefix
- Verify pymobiledevice3 is installed: `pip3 install pymobiledevice3`
- Device must be trusted and unlocked

**pymobiledevice3 not found**:
- Install: `pip3 install pymobiledevice3`

**Only system logs showing**:
- The app's Logger must prefix messages with `[APP]`
- This filters out thousands of framework/system messages

## Notes

- The `[APP]` prefix filters out thousands of system messages
- Screen capture app console auto-scrolls to latest logs
- Use `timeout` command to get a snapshot without blocking
