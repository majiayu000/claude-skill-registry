---
name: simulator
description: "(ePost) List, boot, shutdown, and manage iOS simulators using XcodeBuildMCP or xcrun simctl"
user-invokable: true
context: fork
agent: epost-implementer
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash
  - mcp__xcodebuildmcp__list_sims
  - mcp__xcodebuildmcp__boot_sim
  - mcp__xcodebuildmcp__open_sim
  - mcp__xcodebuildmcp__install_app_sim
  - mcp__xcodebuildmcp__launch_app_sim
  - mcp__xcodebuildmcp__stop_app_sim
  - mcp__xcodebuildmcp__screenshot
  - mcp__xcodebuildmcp__describe_ui
  - mcp__xcodebuildmcp__doctor
metadata:
  argument-hint: "[--list | --boot | --shutdown | --install | --launch | --screenshot]"
---

# iOS Simulator Command

List, boot, shutdown, and manage iOS simulators using XcodeBuildMCP or xcrun simctl.

## Usage
```
/simulator --list                    # List available simulators
/simulator --boot "iPhone 16 Pro"    # Boot simulator
/simulator --shutdown                # Shutdown booted simulator
/simulator --install MyApp.app       # Install app
/simulator --launch com.myapp.bundle # Launch app
/simulator --screenshot              # Take screenshot
```

## Your Process

1. **Reference Build Skill**
   - Use `ios-development/references/build.md` for simulator patterns

2. **Parse Action**
   - `--list`: List available simulators
   - `--boot <name>`: Boot specific simulator
   - `--shutdown`: Shutdown booted simulator
   - `--install <app>`: Install app on simulator
   - `--launch <bundleId>`: Launch app by bundle ID
   - `--screenshot`: Take screenshot of simulator

3. **Execute Action (MCP preferred)**
   - Use MCP tools if available
   - Fallback: xcrun simctl commands via Bash

## MCP Tool Usage

### List Simulators
```swift
mcp__xcodebuildmcp__list_sims()
```

### Boot Simulator
```swift
mcp__xcodebuildmcp__boot_sim({
  simulatorId: 'iPhone-16-Pro-UUID'
})
mcp__xcodebuildmcp__open_sim({
  simulatorId: 'iPhone-16-Pro-UUID'
})
```

### Install App
```swift
mcp__xcodebuildmcp__install_app_sim({
  simulatorId: 'UUID',
  appPath: '/path/to/MyApp.app'
})
```

### Launch App
```swift
mcp__xcodebuildmcp__launch_app_sim({
  simulatorId: 'UUID',
  bundleId: 'com.myapp.bundle'
})
```

### Stop App
```swift
mcp__xcodebuildmcp__stop_app_sim({
  simulatorId: 'UUID',
  bundleId: 'com.myapp.bundle'
})
```

### Screenshot
```swift
mcp__xcodebuildmcp__screenshot({
  simulatorId: 'UUID',
  outputPath: '/path/to/screenshot.png'
})
```

## Fallback Commands (without MCP)

### List
```bash
xcrun simctl list devices available
```

### Boot
```bash
xcrun simctl boot "iPhone 16 Pro"
open -a Simulator
```

### Shutdown
```bash
xcrun simctl shutdown booted
```

### Install
```bash
xcrun simctl install booted MyApp.app
```

### Launch
```bash
xcrun simctl launch booted com.myapp.bundle
```

### Screenshot
```bash
xcrun simctl io booted screenshot screenshot.png
```

## Rules
- Use MCP tools when available
- Always use `list_sims` to get device UDIDs before booting
- Shutdown simulators when done to free resources
- Use simulator for faster iteration, device for final validation
- Provide clear feedback on action results

## Completion Report

```markdown
## Simulator Operation Complete

### Action
- [Action performed]: Success / Failed

### Simulator Details
- Device: iPhone 16 Pro
- UDID: [UUID]
- Status: Booted / Shutdown

### App Details (if applicable)
- Bundle ID: com.myapp.bundle
- App Path: /path/to/MyApp.app

### Output
- [Any output from the operation]

### Next Steps
- [ ] Run app
- [ ] Run tests
- [ ] Take screenshot
```
