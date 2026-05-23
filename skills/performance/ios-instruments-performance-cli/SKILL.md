---
name: ios-instruments-performance-cli
description: Use Xcode Instruments command line tools to analyze iOS app performance, detect memory leaks, optimize launch times, monitor CPU usage, and identify performance bottlenecks for the iOS project
allowed-tools: Bash, Read, Write
---

# iOS Instruments Performance CLI

## Instructions

When helping with iOS app performance optimization using Instruments command line tools:

### 1. Setup Analysis Environment

**CRITICAL: Always use device UUID, never device names**

- Get device UUID: `xcrun simctl list devices available | grep "iPhone"`
- Device names like "iPhone 17 Pro" are ambiguous and will fail
- Use UUID format: `F464E766-555C-4B95-B8CC-763702A70791`

**Clean installation state (REQUIRED)**

- Always uninstall app before profiling: `xcrun simctl uninstall $DEVICE_UUID <bundle id>`
- Multiple app installations cause "process is ambiguous" errors
- Alternative: Completely erase simulator for cleanest state

**Build configuration**

- Build in Release mode for accurate performance measurements

### 2. Choose Appropriate Instrument Template

Use `xcrun xctrace list templates` to see available templates:

- **App Launch** - Essential for launch time optimization (most common)
- **Time Profiler** - CPU performance analysis
- **Allocations** - Memory usage tracking
- **Leaks** - Memory leak detection
- **Network** - API calls and network activity
- **Animation Hitches** - UI performance issues

### 3. Run Performance Analysis

**Standard workflow:**

```bash
DEVICE_UUID="F464E766-555C-4B95-B8CC-763702A70791" # this is sample uuid, run command line to get exist uuid
xcrun simctl uninstall $DEVICE_UUID <bundle id>
xcrun simctl install $DEVICE_UUID /path/to/<app name>.app
sleep 2
xcrun xctrace record --template "App Launch" --device $DEVICE_UUID \
  --launch -- /path/to/<app name>.app 2>&1
```

**Important notes:**

- Trace files auto-generate names like `Launch_<app name>.app_2025-10-30_3.55.40 PM_39E6A410.trace`
- `--output` parameter may be ignored; accept auto-generated names
- Wait 2 seconds after installation before profiling
- Use `2>&1` to capture all output
- Recording duration: 10-30s for launch, 2-5m for other analyses

### 4. Analyze Results

**Finding trace files:**

```bash
ls -lt *.trace | head -1  # Most recent trace
find . -name "*.trace" -type d -mmin -5  # Files from last 5 minutes
```

**Analysis approaches:**

- **CLI export often fails** - "trace is malformed" errors are common
- **Recommended**: Open in Instruments.app GUI for reliable analysis

  ```bash
  open -a Instruments.app Launch_<app name>*.trace
  ```

- Parse signpost markers for performance metrics
- Identify bottlenecks in launch sequence, memory allocations, CPU hotspots

### 5. Common Optimization Patterns

Based on successful optimizations:

- **Lazy initialization** - Defer expensive dependency resolution
- **Background operations** - Move non-critical setup off main thread
- **Deferred bindings** - Set up subscriptions after UI appears
- **Font loading** - Register fonts asynchronously
- **Method swizzling** - Only essential swizzles during launch

### Critical Pitfalls to Avoid

❌ Using device names instead of UUIDs
❌ Skipping clean installation step
❌ Building in Debug mode
❌ Trying to export trace immediately after recording
❌ Assuming --output path will be used
❌ Not waiting between installation and profiling

### Reference Documentation

See [examples](./examples.md) in this skill directory for:

- Detailed command examples with correct syntax
- Complete troubleshooting guide with solutions
- Real-world lessons learned
- Production-ready workflow scripts
