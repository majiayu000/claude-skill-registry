---
name: ios
description: iOS platform-specific development with XcodeBuildMCP tools for simulator, device, UI automation, and debugging. Use when building iPhone apps, testing on simulator/device, or automating UI interactions.
versions:
  ios: 26
  xcode: 26
user-invocable: false
references: references/simulator-tools.md, references/device-tools.md, references/ui-automation.md, references/debugging.md, references/uikit-integration.md
related-skills: swift-core, swiftui-core, ipados, mcp-tools
---

# iOS Platform

iOS-specific development with XcodeBuildMCP automation tools.

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing iOS patterns
2. **fuse-ai-pilot:research-expert** - Verify latest iOS 26 docs via Context7/Exa
3. **mcp__XcodeBuildMCP__discover_projs** - Find Xcode projects

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building iPhone applications
- Testing on iOS Simulator
- Deploying to physical devices
- Automating UI interactions
- Debugging app behavior
- UIKit integration in SwiftUI

### Why iOS Skill

| Feature | Benefit |
|---------|---------|
| XcodeBuildMCP | Automated build and test |
| UI Automation | Scripted user interactions |
| Simulator tools | Fast iteration cycle |
| Device tools | Real hardware testing |

---

## MCP Tools Available

### Simulator Tools
- `build_sim` - Build for simulator
- `boot_sim` - Start simulator
- `launch_app_sim` - Run app
- `test_sim` - Execute tests

### Device Tools
- `build_device` - Build for device
- `install_app_device` - Deploy to device
- `list_devices` - Show connected devices

### UI Automation
- `tap`, `swipe` - Touch interactions
- `screenshot` - Capture screen
- `snapshot_ui` - Get view hierarchy

---

## Reference Guide

| Need | Reference |
|------|-----------|
| Simulator build/test | [simulator-tools.md](references/simulator-tools.md) |
| Device deployment | [device-tools.md](references/device-tools.md) |
| Touch automation | [ui-automation.md](references/ui-automation.md) |
| LLDB debugging | [debugging.md](references/debugging.md) |
| UIKit in SwiftUI | [uikit-integration.md](references/uikit-integration.md) |

---

## Best Practices

1. **Build validation** - Always build before commit
2. **Simulator first** - Faster iteration
3. **Device testing** - Required before release
4. **Accessibility IDs** - Enable UI automation
5. **Screenshots** - Document UI states
6. **Test on oldest supported** - iOS version compatibility
