---
name: capacitor-mcp
description: Model Context Protocol (MCP) tools for Capacitor mobile development. Covers device management, app deployment, log streaming, and automated testing via MCP. Use this skill when users want to automate mobile development tasks or integrate AI agents with mobile tooling.
---

# Capacitor MCP Tools

Guide to using Model Context Protocol (MCP) for Capacitor mobile development automation.

## When to Use This Skill

- User wants to automate mobile development
- User asks about MCP integration
- User wants AI-assisted mobile testing
- User needs programmatic device control
- User wants to stream logs via MCP

## What is MCP?

MCP (Model Context Protocol) is an open standard for connecting AI models to external tools and data sources. For Capacitor development, MCP enables:

- Automated app deployment
- Real-time log streaming
- Device management
- Screenshot capture
- Automated testing

## Setting Up MCP for Capacitor

### 1. Install MCP Server

```bash
# Install the Capacitor MCP server
bun add -g @anthropic/mcp-server-capacitor
```

### 2. Configure MCP

Create `~/.config/mcp/capacitor.json`:

```json
{
  "mcpServers": {
    "capacitor": {
      "command": "mcp-server-capacitor",
      "args": ["--project", "/path/to/your/capacitor/app"]
    }
  }
}
```

### 3. Available MCP Tools

## iOS MCP Tools

### Device Management

```typescript
// List available iOS devices
mcp.ios.listDevices()
// Returns: [{ name: "iPhone 15", udid: "xxx", state: "Booted" }]

// Boot a simulator
mcp.ios.bootSimulator({ name: "iPhone 15 Pro" })

// Shutdown simulator
mcp.ios.shutdownSimulator({ udid: "xxx" })
```

### App Deployment

```typescript
// Build iOS app
mcp.ios.build({
  scheme: "App",
  configuration: "Debug",
  destination: "platform=iOS Simulator,name=iPhone 15"
})

// Install app on device
mcp.ios.install({
  device: "booted",
  appPath: "./ios/App/build/Debug-iphonesimulator/App.app"
})

// Launch app
mcp.ios.launch({
  device: "booted",
  bundleId: "com.yourapp.id"
})
```

### Log Streaming

```typescript
// Stream logs from iOS device
const logStream = mcp.ios.streamLogs({
  device: "booted",
  predicate: 'process == "App"',
  level: "debug"
})

logStream.on('log', (entry) => {
  console.log(entry.timestamp, entry.level, entry.message)
})

// Stop streaming
logStream.stop()
```

### Screenshots

```typescript
// Capture screenshot
mcp.ios.screenshot({
  device: "booted",
  outputPath: "./screenshot.png"
})

// Record video
mcp.ios.recordVideo({
  device: "booted",
  outputPath: "./recording.mp4",
  duration: 30 // seconds
})
```

## Android MCP Tools

### Device Management

```typescript
// List connected Android devices
mcp.android.listDevices()
// Returns: [{ name: "Pixel 8", serial: "xxx", state: "device" }]

// Start emulator
mcp.android.startEmulator({ avd: "Pixel_8_API_34" })

// Kill emulator
mcp.android.killEmulator({ serial: "emulator-5554" })
```

### App Deployment

```typescript
// Build Android app
mcp.android.build({
  variant: "debug",
  projectPath: "./android"
})

// Install APK
mcp.android.install({
  serial: "emulator-5554",
  apkPath: "./android/app/build/outputs/apk/debug/app-debug.apk"
})

// Launch app
mcp.android.launch({
  serial: "emulator-5554",
  package: "com.yourapp.id",
  activity: ".MainActivity"
})
```

### Log Streaming

```typescript
// Stream logcat
const logStream = mcp.android.logcat({
  serial: "emulator-5554",
  package: "com.yourapp.id",
  level: "D"
})

logStream.on('log', (entry) => {
  console.log(entry.tag, entry.level, entry.message)
})

// Stop streaming
logStream.stop()

// Get recent logs
const recentLogs = mcp.android.getLogcat({
  serial: "emulator-5554",
  lines: 100,
  filter: "Capacitor:*"
})
```

### Screenshots

```typescript
// Capture screenshot
mcp.android.screenshot({
  serial: "emulator-5554",
  outputPath: "./screenshot.png"
})

// Record screen
mcp.android.recordScreen({
  serial: "emulator-5554",
  outputPath: "./recording.mp4",
  duration: 30
})
```

## Capacitor CLI MCP Tools

### Project Management

```typescript
// Sync web assets to native
mcp.capacitor.sync({ platform: "ios" })
mcp.capacitor.sync({ platform: "android" })

// Run capacitor commands
mcp.capacitor.run({
  platform: "ios",
  target: "iPhone 15 Pro"
})

// Open native IDE
mcp.capacitor.open({ platform: "ios" })
```

### Plugin Management

```typescript
// List installed plugins
mcp.capacitor.listPlugins()

// Add plugin
mcp.capacitor.addPlugin({ name: "@capgo/capacitor-native-biometric" })

// Update plugins
mcp.capacitor.updatePlugins()
```

## Automated Testing with MCP

### UI Testing

```typescript
// Define test scenario
async function testLogin() {
  // Launch app
  await mcp.ios.launch({ bundleId: "com.yourapp.id" })

  // Wait for app ready
  await mcp.ios.waitForElement({
    device: "booted",
    accessibility: "login-button"
  })

  // Capture initial state
  await mcp.ios.screenshot({ outputPath: "./test-login-1.png" })

  // Tap element
  await mcp.ios.tap({
    device: "booted",
    accessibility: "login-button"
  })

  // Type text
  await mcp.ios.typeText({
    device: "booted",
    accessibility: "email-input",
    text: "test@example.com"
  })

  // Assert element exists
  const element = await mcp.ios.findElement({
    device: "booted",
    accessibility: "welcome-message"
  })

  if (element) {
    console.log("Login test passed!")
  }
}
```

### Performance Testing

```typescript
// Monitor performance during test
async function performanceTest() {
  // Start performance monitoring
  const perfMonitor = mcp.ios.startPerformanceMonitoring({
    device: "booted",
    metrics: ["cpu", "memory", "fps"]
  })

  // Run test scenario
  await runTestScenario()

  // Stop and get results
  const results = perfMonitor.stop()

  console.log("Average CPU:", results.cpu.average)
  console.log("Peak Memory:", results.memory.peak)
  console.log("Average FPS:", results.fps.average)
}
```

## MCP Server Implementation

### Creating Custom MCP Tools

```typescript
// mcp-server.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js"
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js"

const server = new Server({
  name: "capacitor-mcp",
  version: "1.0.0"
}, {
  capabilities: {
    tools: {}
  }
})

// Register iOS log streaming tool
server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "ios_stream_logs") {
    const { device, predicate } = request.params.arguments

    const process = spawn("xcrun", [
      "simctl", "spawn", device, "log", "stream",
      "--predicate", predicate
    ])

    // Stream logs back to client
    process.stdout.on("data", (data) => {
      server.sendNotification("log", { data: data.toString() })
    })

    return { content: [{ type: "text", text: "Log streaming started" }] }
  }
})

// Start server
const transport = new StdioServerTransport()
await server.connect(transport)
```

## Integration Examples

### Claude Desktop Integration

Add to `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "capacitor": {
      "command": "node",
      "args": ["/path/to/capacitor-mcp-server/index.js"],
      "env": {
        "CAPACITOR_PROJECT": "/path/to/your/app"
      }
    }
  }
}
```

### VS Code Integration

Install MCP extension and configure:

```json
// .vscode/settings.json
{
  "mcp.servers": {
    "capacitor": {
      "command": "mcp-server-capacitor",
      "args": ["--project", "${workspaceFolder}"]
    }
  }
}
```

## Available MCP Servers for Mobile

| Server | Description |
|--------|-------------|
| `mcp-server-capacitor` | Capacitor project management |
| `mcp-server-ios` | iOS device/simulator control |
| `mcp-server-android` | Android device/emulator control |
| `mcp-server-appium` | Mobile UI testing |

## Resources

- MCP Specification: https://modelcontextprotocol.io
- MCP SDK: https://github.com/modelcontextprotocol/sdk
- Anthropic MCP Servers: https://github.com/anthropics/mcp-servers
