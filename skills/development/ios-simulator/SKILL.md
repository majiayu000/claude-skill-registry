---
name: ios-simulator
description: Build and run iOS app on simulator. Use when user asks to run on simulator, test on simulator, or debug iOS app locally. Handles building, deploying, and log streaming.
allowed-tools: Bash(cd:*), Bash(./scripts/*), Bash(xcrun:*), Bash(xcodebuild:*), Bash(pkill:*), Bash(rm:*)
---

# iOS Simulator Deployment & Debugging

**This is an action skill. Run commands, don't just explain them.**

## Quick Commands

**Build and run on simulator:**
```bash
cd apps/ios && ./scripts/run.sh
```

This script:
1. Builds the app (always rebuilds to pick up code changes)
2. Boots iPhone 17 Pro simulator
3. Installs and launches the app

## Debugging / Log Streaming

**Important:** `print()` does NOT show in Console.app. Use `NSLog()` or `os_log` instead.

**Stream app logs in terminal:**
```bash
xcrun simctl spawn booted log stream --predicate 'eventMessage CONTAINS "[YourTag]"' --level debug
```

**Stream all app logs:**
```bash
xcrun simctl spawn booted log stream --predicate 'subsystem == "com.bytespell.shella"' --level debug
```

**Check if app is running:**
```bash
xcrun simctl spawn booted launchctl list | grep shella
```

## Clean Build

If you suspect stale code is being used:
```bash
cd apps/ios && rm -rf .build && ./scripts/run.sh
```

## Troubleshooting

**App doesn't reflect code changes:**
- The `run.sh` script now always rebuilds, but if issues persist, do a clean build (see above)

**Logs not appearing:**
- `print()` statements don't show in Console.app - use `NSLog("message")` or `os_log`
- Make sure Console.app is filtering by "Simulator" in the sidebar
- Enable "Include Info Messages" and "Include Debug Messages" in Console.app's Action menu

**Simulator won't boot:**
```bash
xcrun simctl shutdown all
xcrun simctl boot "iPhone 17 Pro"
```

**Kill and restart app:**
```bash
xcrun simctl terminate booted com.bytespell.shella
xcrun simctl launch booted com.bytespell.shella
```

## Typical Flow

User: "run on simulator" / "test this on iOS" / "build and run"

1. Run the build+deploy script:
```bash
cd apps/ios && ./scripts/run.sh
```

2. If user needs logs, start streaming:
```bash
xcrun simctl spawn booted log stream --predicate 'eventMessage CONTAINS "[SomeTag]"' --level debug
```

3. For debugging, remind user that `print()` won't show - they need `NSLog()`.
