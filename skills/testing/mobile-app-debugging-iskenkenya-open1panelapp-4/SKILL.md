---
name: mobile-app-debugging
description: Debug issues specific to mobile applications including platform-specific problems, device constraints, and connectivity issues.
---

# Mobile App Debugging

## Overview

Mobile app debugging addresses platform-specific issues, device hardware limitations, and mobile-specific network conditions.

## When to Use

- App crashes on mobile
- Performance issues on device
- Platform-specific bugs
- Network connectivity issues
- Device-specific problems

## Instructions

### 1. **iOS Debugging**

```yaml
Xcode Debugging:

Attach Debugger:
  - Xcode → Run on device
  - Set breakpoints in code
  - Step through execution
  - View variables
  - Console logs

View Logs:
  - Xcode → Window → Devices & Simulators
  - Select device → View Device Logs
  - Filter by app name
  - Check system logs for crashes

Inspect Memory:
  - Xcode → Debug → View Memory Graph
  - Identify retain cycles
  - Check object count
  - Monitor allocation growth

---

Common iOS Issues:

App Crash (SIGABRT):
  Cause: Exception in Objective-C
  Solution: Check console for error message
  Debug: Set breakpoint on exception

Memory Warning (SIGKILL):
  Cause: Too much memory usage
  Solution: Reduce memory footprint
  Optimize: Image caching, data structures

Networking:
  Issue: Network requests fail on device
  Check: Network connectivity status
  Solution: Implement Network Link Conditioner
  Test: Throttle network in Xcode
```

### 2. **Android Debugging**

```yaml
Android Studio:

Attach Debugger:
  - Run → Debug
  - Set breakpoints
  - Step through code
  - Watch variables
  - Evaluate expressions

Logcat:
  - Displays all app logs
  - Filter by tag
  - Filter by process
  - Show errors and warnings

Device Monitor:
  - Memory profiler
  - CPU profiler
  - Network profiler
  - Battery usage

---

Common Android Issues:

App Crash (ANR):
  Cause: Long-running operation on main thread
  Solution: Move to background thread
  Example: Use AsyncTask or coroutines

Memory Leak:
  Cause: Activity not garbage collected
  Solution: Clear references in onDestroy
  Debug: Android Profiler shows retained objects

Networking:
  Issue: Network requests timeout
  Check: Network connectivity
  Solution: Implement timeout and retry
  Test: Simulate poor network
```

### 3. **Cross-Platform Issues**

```yaml
React Native Debugging:

Console Logs:
  - Run app with: react-native run-android
  - View logs: adb logcat | grep ReactNativeJS
  - Or use remote debugger

Remote Debugging:
  - Shake device → Enable Remote Debugging
  - Chrome DevTools debugging
  - Set breakpoints in JS
  - Inspect state

Performance:
  - Perf Monitor: Shake → Perf Monitor
  - Shows FPS, RAM, Bridge traffic
  - Identify frame drops
  - Check excessive bridge calls

---

Flutter Debugging:

Device Logs:
  flutter logs
  Shows all device and app output

Debugging:
  flutter run --debug
  Set breakpoints in IDE
  Step through code

Hot Reload:
  Useful for rapid iteration
  Hot restart for full reload
  Useful for debugging UI changes

---

Common Mobile Issues:

Network Connectivity:
  Issue: App works on WiFi, fails on cellular
  Solution: Test on both networks
  Debug: Use network throttler
  Implement: Retry logic, offline support

Device Specific:
  Issue: Works on simulator, fails on device
  Solution: Always test on real device
  Causes:
    - Memory constraints
    - Performance differences
    - Platform differences
    - Screen size issues

Battery/Memory:
  Issue: Excessive battery drain
  Debug: Use power profiler
  Optimize: Reduce background work
  Monitor: Location tracking, networking
```

### 4. **Mobile Testing & Debugging Checklist**

```yaml
Device Testing:

[ ] Test on both iOS and Android
[ ] Test on old and new devices
[ ] Test with poor network (3G throttle)
[ ] Test in airplane mode
[ ] Test with low battery
[ ] Test with low memory
[ ] Test with location disabled
[ ] Test with notifications disabled
[ ] Test rotation changes
[ ] Test while backgrounded

Performance:

[ ] <16ms per frame (60 FPS)
[ ] Memory usage <100MB
[ ] Battery drain acceptable
[ ] Network requests efficient
[ ] Background tasks minimal

Networking:

[ ] Works on WiFi
[ ] Works on cellular
[ ] Handles network timeouts
[ ] Handles offline mode
[ ] Retries failed requests
[ ] Shows loading indicators
[ ] Shows error messages

UI/UX:

[ ] Responsive touch targets (44x44 min)
[ ] Readable text (16pt minimum)
[ ] Colors accessible
[ ] Orientation changes handled
[ ] Keyboard shows/hides correctly
[ ] Safe areas respected (notches)

---

Tools:

Testing Devices:
  - iOS: iPhone SE (small), iPhone 12/13 (modern)
  - Android: Pixel 4 (standard), Pixel 6 (new)
  - Virtual: Simulators for iteration

Device Management:
  - TestFlight (iOS)
  - Google Play Beta (Android)
  - Firebase Test Lab
  - BrowserStack

Monitoring:
  - Crashlytics
  - Firebase Analytics
  - App Performance Monitoring
  - Custom event tracking
```

## Key Points

- Always test on real devices
- Simulate poor network conditions
- Monitor memory and CPU
- Test on old and new devices
- Use platform-specific debugging tools
- Check device logs for crashes
- Test network edge cases
- Monitor battery/memory impact
- Use profilers to identify bottlenecks
- Implement proper error handling
