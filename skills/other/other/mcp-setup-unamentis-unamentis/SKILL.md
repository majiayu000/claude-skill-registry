---
name: mcp-setup
description: Configure MCP session defaults for different project components
---

# /mcp-setup - MCP Session Configuration

## Purpose

Configures MCP (Model Context Protocol) session defaults for iOS simulator and Xcode build operations. This skill ensures the correct project, scheme, and simulator are set before any build or test operations.

**Critical Rule:** MCP defaults MUST be set before building. Building without proper defaults will fail.

## Usage

```
/mcp-setup ios        # Configure for main iOS app (default)
/mcp-setup usm        # Configure for Server Manager app
/mcp-setup show       # Show current session defaults
/mcp-setup clear      # Clear session defaults
```

## Configurations

### iOS App (default)
```
Project: $PROJECT_ROOT/UnaMentis.xcodeproj
Scheme: UnaMentis
Simulator: iPhone 16 Pro
```

### Server Manager (USM)
```
Workspace: $PROJECT_ROOT/server/server-manager/USMXcode/USM.xcworkspace
Scheme: USM
Simulator: iPhone 16 Pro
```

Where `$PROJECT_ROOT` is the absolute path to the unamentis repository on this machine (the current working directory).

## Workflow

### 1. Set Session Defaults

For iOS app:
```
mcp__XcodeBuildMCP__session-set-defaults({
  projectPath: "$PROJECT_ROOT/UnaMentis.xcodeproj",
  scheme: "UnaMentis",
  simulatorName: "iPhone 16 Pro"
})
```

For USM:
```
mcp__XcodeBuildMCP__session-set-defaults({
  workspacePath: "$PROJECT_ROOT/server/server-manager/USMXcode/USM.xcworkspace",
  scheme: "USM",
  simulatorName: "iPhone 16 Pro"
})
```

**Note:** Replace `$PROJECT_ROOT` with the actual absolute path to the unamentis directory (use `pwd` in the project root to get this).

### 2. Verify Configuration

```
mcp__XcodeBuildMCP__session-show-defaults()
```

### 3. Confirm Simulator Available

```
mcp__XcodeBuildMCP__list_sims()
```

Ensure the target simulator exists and is available.

## Success Criteria

- Session defaults set successfully
- Scheme is valid for the project
- Simulator exists and is available

## Examples

**Configure for iOS development:**
```
User: /mcp-setup ios
Claude: Configuring MCP for iOS app development...

Setting defaults:
- Project: UnaMentis.xcodeproj
- Scheme: UnaMentis
- Simulator: iPhone 16 Pro

Configuration complete. You can now use:
- /ios-build or build commands
- MCP simulator tools
```

**Configure for USM development:**
```
User: /mcp-setup usm
Claude: Configuring MCP for Server Manager development...

Setting defaults:
- Workspace: USM.xcworkspace
- Scheme: USM
- Simulator: iPhone 16 Pro

Configuration complete. Ready to build USM.
```

**Show current configuration:**
```
User: /mcp-setup show
Claude: Current MCP session defaults:

Project: $PROJECT_ROOT/UnaMentis.xcodeproj
Scheme: UnaMentis
Simulator: iPhone 16 Pro (ID: 12345678-1234-1234-1234-123456789ABC)
Configuration: Debug
```

**Clear configuration:**
```
User: /mcp-setup clear
Claude: Clearing MCP session defaults...

All session defaults cleared. Run /mcp-setup ios or /mcp-setup usm to reconfigure.
```

## Available Simulators

Common simulators (verify with `list_sims`):
- iPhone 16 Pro (preferred for CI parity)
- iPhone 17 Pro
- iPhone 15 Pro
- iPad Pro 13-inch

**Note:** iPhone 16 Pro is the default to match CI. The test runner includes automatic fallback to other available simulators if the preferred one is not found.

## Integration

This skill should be run:
- At the start of a development session
- When switching between iOS app and USM development
- Before any build or test operations
- When the simulator needs to change
