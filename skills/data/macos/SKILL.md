---
name: macos
description: macOS platform-specific development with menu bar apps, window management, AppKit integration, and notarization. Use when building Mac apps, creating menu bar extras, or distributing outside App Store.
versions:
  macos: 26
  xcode: 26
user-invocable: false
references: references/app-structure.md, references/build-tools.md, references/appkit-integration.md, references/notarization.md
related-skills: swift-core, swiftui-core, mcp-tools, build-distribution
---

# macOS Platform

macOS-specific development with window management and distribution tools.

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing macOS patterns
2. **fuse-ai-pilot:research-expert** - Verify latest macOS 26 docs via Context7/Exa
3. **mcp__XcodeBuildMCP__build_macos** - Build for macOS validation

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

### When to Use

- Building Mac desktop applications
- Creating menu bar apps (MenuBarExtra)
- Multi-window applications
- Keyboard shortcuts and menus
- Notarization for distribution
- AppKit integration

### Why macOS Skill

| Feature | Benefit |
|---------|---------|
| MenuBarExtra | Background utility apps |
| Window management | Multi-window support |
| Keyboard shortcuts | Power user productivity |
| Notarization | Gatekeeper-safe distribution |

---

## MCP Tools Available

### Build Tools
- `build_macos` - Build for macOS
- `build_run_macos` - Build and launch
- `test_macos` - Run macOS tests
- `launch_mac_app` - Start built app
- `stop_mac_app` - Terminate app

---

## Reference Guide

| Need | Reference |
|------|-----------|
| MenuBarExtra, Settings, Windows | [app-structure.md](references/app-structure.md) |
| XcodeBuildMCP macOS tools | [build-tools.md](references/build-tools.md) |
| NSViewRepresentable, menus | [appkit-integration.md](references/appkit-integration.md) |
| Code signing, notarization | [notarization.md](references/notarization.md) |

---

## Best Practices

1. **Keyboard shortcuts** - Support power users
2. **Menu bar integration** - For utility apps
3. **Multiple windows** - Use WindowGroup/Window
4. **Settings window** - Use Settings scene
5. **Notarization** - Required for distribution
6. **Sandbox** - Enable for App Store
