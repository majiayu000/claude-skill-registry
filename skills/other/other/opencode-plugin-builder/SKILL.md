---
name: opencode-plugin-builder
description: This skill should be used when creating, modifying, or debugging OpenCode plugins. It provides the complete plugin architecture, available hooks, event types, SDK client methods, and best practices learned from real-world plugin development.
---

# OpenCode Plugin Builder

## Overview

This skill provides comprehensive guidance for building OpenCode plugins - JavaScript/TypeScript modules that extend OpenCode's functionality through hooks, events, and custom tools.

## Plugin Architecture

### File Locations

Plugins can be placed in two locations:

| Location | Scope | Path |
|----------|-------|------|
| Global | All projects | `~/.config/opencode/plugin/` |
| Project | Single project | `.opencode/plugin/` |

### Load Order

Plugins load in sequence:
1. Global config (`~/.config/opencode/opencode.json`)
2. Project config (`opencode.json`)
3. Global plugin directory (`~/.config/opencode/plugin/`)
4. Project plugin directory (`.opencode/plugin/`)

### Basic Structure

```javascript
// ES Module format required
export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  // Initialization code runs once at startup
  
  return {
    // Hook implementations
  }
}
```

### Plugin Context Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `project` | `Project` | Current project information |
| `directory` | `string` | Current working directory |
| `worktree` | `string` | Git worktree path |
| `client` | `OpencodeClient` | SDK client for API calls |
| `$` | `BunShell` | Bun shell API for commands |

## Available Hooks

### Event Hook

Subscribe to system events:

```javascript
event: async ({ event }) => {
  if (event.type === 'session.created') {
    const sessionInfo = event.properties.info
    // Handle session creation
  }
}
```

### Chat Hooks

#### chat.message

Intercept and modify user messages before processing:

```javascript
"chat.message": async (input, output) => {
  // input structure (verified):
  // {
  //   sessionID: string,      // Session ID
  //   agent: string,          // Agent name (e.g., "default", "build")
  //   model: object,          // { providerID, modelID }
  //   messageID: string,      // Unique message ID
  //   variant: number         // Message variant index
  // }
  
  // output structure:
  // {
  //   message: UserMessage,   // Full message object
  //   parts: Part[]           // Array of message parts
  // }
  
  const textPart = output.parts.find(p => p.type === "text")
  if (textPart) {
    // Prepend content to user message
    textPart.text = "Prefix: " + textPart.text
  }
}
```

**Key insight:** The `input.sessionID` is always available in `chat.message`, making it ideal for per-session tracking (e.g., first-message detection).

#### chat.params

Modify LLM parameters before API call:

```javascript
"chat.params": async (input, output) => {
  // input: { sessionID, agent, model, provider, message }
  // output: { temperature, topP, topK, options }
  
  output.temperature = 0.7
}
```

### Tool Hooks

#### tool.execute.before

Intercept tool calls before execution:

```javascript
"tool.execute.before": async (input, output) => {
  // input: { tool, sessionID, callID }
  // output: { args }
  
  if (input.tool === "read" && output.args.filePath.includes(".env")) {
    throw new Error("Access denied: .env files are protected")
  }
}
```

#### tool.execute.after

Process tool results after execution:

```javascript
"tool.execute.after": async (input, output) => {
  // input: { tool, sessionID, callID }
  // output: { title, output, metadata }
  
  await client.app.log({
    body: {
      service: "my-plugin",
      level: "info",
      message: `Tool ${input.tool} completed: ${output.title}`
    }
  })
}
```

### Permission Hook

Customize permission handling:

```javascript
"permission.ask": async (input, output) => {
  // input: Permission object
  // output: { status: "ask" | "deny" | "allow" }
  
  if (input.tool === "bash" && input.command.includes("rm -rf")) {
    output.status = "deny"
  }
}
```

### Experimental Hooks

#### experimental.session.compacting

Customize context compaction:

```javascript
"experimental.session.compacting": async (input, output) => {
  // input: { sessionID }
  // output: { context: string[], prompt?: string }
  
  // Add context to default prompt
  output.context.push("Important: Preserve all file paths mentioned")
  
  // OR replace entire prompt
  output.prompt = "Custom compaction prompt..."
}
```

#### experimental.chat.system.transform

Modify system prompt:

```javascript
"experimental.chat.system.transform": async (input, output) => {
  // output: { system: string[] }
  output.system.push("Additional system instruction")
}
```

### Custom Tools Hook

Register custom tools:

```javascript
import { tool } from "@opencode-ai/plugin"

// In plugin return:
tool: {
  myTool: tool({
    description: "What the tool does",
    args: {
      param1: tool.schema.string().describe("Parameter description"),
      param2: tool.schema.number().optional(),
    },
    async execute(args, ctx) {
      // ctx: { sessionID, messageID, agent, abort: AbortSignal }
      return `Result: ${args.param1}`
    },
  }),
}
```

## Available Events

### Session Events

| Event | Properties | Description |
|-------|------------|-------------|
| `session.created` | `{ info: Session }` | New session started. Subagent sessions have `info.parentID` set to parent session ID |
| `session.updated` | `{ info: Session }` | Session modified |
| `session.deleted` | `{ info: Session }` | Session removed |
| `session.idle` | `{ sessionID }` | Session finished processing |
| `session.compacted` | `{ info: Session }` | Context was compacted |
| `session.error` | `{ sessionID, error }` | Session encountered error |
| `session.status` | `{ sessionID, status }` | Status changed |
| `session.diff` | `{ sessionID, diff: FileDiff[] }` | Files changed |

### Message Events

| Event | Properties | Description |
|-------|------------|-------------|
| `message.updated` | `{ info: Message, parts: Part[] }` | Message modified |
| `message.removed` | `{ info: Message }` | Message deleted |
| `message.part.updated` | `{ part: Part }` | Message part changed |
| `message.part.removed` | `{ part: Part }` | Message part deleted |

### Permission Events

| Event | Properties | Description |
|-------|------------|-------------|
| `permission.updated` | `{ permission: Permission }` | Permission request created |
| `permission.replied` | `{ permission: Permission }` | Permission responded to |

### File Events

| Event | Properties | Description |
|-------|------------|-------------|
| `file.edited` | `{ path, changes }` | File was edited |
| `file.watcher.updated` | `{ files }` | File watcher detected changes |

### Other Events

| Event | Description |
|-------|-------------|
| `todo.updated` | Todo list changed |
| `command.executed` | Command was run |
| `lsp.updated` | LSP server status changed |
| `lsp.client.diagnostics` | LSP diagnostics received |
| `vcs.branch.updated` | Git branch changed |

## SDK Client Methods

The `client` object provides access to OpenCode's API:

### Session Operations

```javascript
// List all sessions
const sessions = await client.session.list()

// Get session by ID
const session = await client.session.get({ path: { id: sessionID } })

// Send a prompt to session
await client.session.prompt({
  path: { id: sessionID },
  body: {
    parts: [{ type: "text", text: "Hello" }],
    noReply: true,  // Don't wait for AI response
    model: { providerID: "anthropic", modelID: "claude-sonnet-4-20250514" },
    agent: "default",
  }
})

// Abort a session
await client.session.abort({ path: { id: sessionID } })
```

### Other Client Methods

```javascript
// Get current project
const project = await client.project.current()

// Get config
const config = await client.config.get()

// Log messages (instead of console.log)
await client.app.log({
  service: "my-plugin",
  level: "info",  // debug, info, warn, error
  message: "Something happened",
  extra: { key: "value" }
})

// Show toast notification in TUI
await client.tui.showToast({
  body: { message: "Task completed!", level: "info" }
})
```

## Common Patterns

### State Persistence

Use JSON files for plugin state:

```javascript
import { readFileSync, writeFileSync, existsSync } from 'fs'
import { join } from 'path'

const DB_FILE = 'my-plugin-state.json'

function loadState(configDir) {
  const path = join(configDir, DB_FILE)
  if (!existsSync(path)) return { sessions: {} }
  
  try {
    return JSON.parse(readFileSync(path, 'utf-8'))
  } catch {
    return { sessions: {} }
  }
}

function saveState(configDir, state) {
  writeFileSync(join(configDir, DB_FILE), JSON.stringify(state, null, 2))
}
```

### Config Directory Resolution

```javascript
const configDir = process.env.HOME
  ? join(process.env.HOME, '.config', 'opencode')
  : directory
```

### External Configuration Files

Load configuration from JSON:

```javascript
function loadConfig(configDir, log) {
  const configPath = join(configDir, 'my-plugin-config.json')
  
  if (!existsSync(configPath)) {
    log?.("warn", "Config not found")
    return null
  }
  
  try {
    return JSON.parse(readFileSync(configPath, 'utf-8'))
  } catch (err) {
    log?.("error", `Error loading config: ${err.message}`)
    return null
  }
}
```

### Shell Commands

Use Bun shell API:

```javascript
// Run command
await $`git status`

// Capture output
const result = await $`echo "hello"`.text()

// With error handling
try {
  await $`some-command`
} catch (err) {
  await log("error", `Command failed: ${err.message}`)
}
```

### macOS Notifications

```javascript
async function notify($, log, title, message) {
  const safeTitle = title.replace(/"/g, '\\"')
  const safeMsg = message.replace(/"/g, '\\"')
  const script = `display notification "${safeMsg}" with title "${safeTitle}" sound name "Glass"`
  
  try {
    await $`osascript -e ${script}`
  } catch (err) {
    await log("error", `Notification failed: ${err.message}`)
  }
}
```

## Critical Gotchas

### 1. Always Use client.app.log() for Logging

**NEVER use `console.log` or `console.error` in plugins.** Always use the structured logging API:

```javascript
// WRONG - console output is not visible in OpenCode logs
console.log('[my-plugin] Something happened')
console.error('[my-plugin] Error:', err)

// CORRECT - structured logging visible in OpenCode log viewer
await client.app.log({
  body: {
    service: "my-plugin",
    level: "info",  // debug, info, warn, error
    message: "Something happened",
  }
})

await client.app.log({
  body: {
    service: "my-plugin",
    level: "error",
    message: `Error: ${err.message}`,
    extra: { stack: err.stack }
  }
})
```

For convenience, create a logging helper at plugin initialization:

```javascript
export const MyPlugin = async ({ client, ...ctx }) => {
  const log = (level, message, extra) => 
    client.app.log({ body: { service: "my-plugin", level, message, extra } })
  
  return {
    event: async ({ event }) => {
      await log("info", `Event received: ${event.type}`)
    }
  }
}
```

### 2. Session Timing: session.created vs chat.message

**CRITICAL:** In TUI mode, when a user selects a model via `/models` before sending their first message, the model is NOT set on the session when `session.created` fires. The model is attached to the first message instead.

**The Problem:**
```javascript
// WRONG - model may not be set yet in TUI flow
event: async ({ event }) => {
  if (event.type === 'session.created') {
    const session = event.properties.info
    // session.model may be undefined here in TUI mode!
    await client.session.prompt({
      path: { id: session.id },
      body: {
        parts: [{ type: "text", text: "Bootstrap content" }],
        model: session.model,  // undefined = resets to default!
      }
    })
  }
}
```

**The Solution:** For first-message injection, use `chat.message` hook instead:
```javascript
// Track which sessions have been bootstrapped
const bootstrappedSessions = new Map()

return {
  event: async ({ event }) => {
    // Just mark session as needing bootstrap
    if (event.type === 'session.created') {
      const sessionID = event.properties?.info?.id
      if (sessionID) {
        bootstrappedSessions.set(sessionID, false)
      }
    }
  },

  "chat.message": async (input, output) => {
    const textPart = output.parts.find(p => p.type === "text")
    if (!textPart) return

    const sessionID = input.sessionID
    
    // Inject on first message - model is preserved since we modify message text
    if (sessionID && bootstrappedSessions.get(sessionID) !== true) {
      textPart.text = "Bootstrap content\n\n" + textPart.text
      bootstrappedSessions.set(sessionID, true)
    }
  }
}
```

**Why this works:** Modifying `textPart.text` in `chat.message` doesn't make a separate API call - it just prepends content to the user's message. The model selection from the user's message is preserved.

### 3. Preserve Session Settings in session.prompt

When calling `session.prompt()`, always preserve the session's model and agent settings:

```javascript
// WRONG - will reset to default model/agent
await client.session.prompt({
  path: { id: sessionID },
  body: {
    noReply: true,
    parts: [{ type: "text", text: content }]
  }
})

// CORRECT - preserves session settings (if available)
await client.session.prompt({
  path: { id: sessionID },
  body: {
    noReply: true,
    parts: [{ type: "text", text: content }],
    model: sessionInfo.model,   // From event.properties.info
    agent: sessionInfo.agent,   // From event.properties.info
  }
})
```

**Note:** Even with model/agent preservation, `session.prompt()` may still cause issues if called at the wrong time. Prefer `chat.message` hook for first-message injection.

### 4. Distinguish Subagent Events

**CRITICAL:** The `session.idle` event does NOT contain `isSubagent` or `parentSessionID` properties - these are always undefined. To filter subagent events, you must track them at creation time.

**The Problem:**
```javascript
// WRONG - these properties are always undefined
if (event.type === 'session.idle') {
  if (event.properties.isSubagent || event.properties.parentSessionID) {
    return  // This never works!
  }
}
```

**The Solution:** Track subagent sessions when they're created using `info.parentID`:

```javascript
// Track subagent session IDs
const subagentSessions = new Set()

return {
  event: async ({ event }) => {
    // Capture subagent sessions at creation (they have parentID)
    if (event.type === 'session.created') {
      const sessionInfo = event.properties.info
      if (sessionInfo.parentID) {
        subagentSessions.add(sessionInfo.id)
      }
    }

    // Filter subagents on idle
    if (event.type === 'session.idle') {
      const sessionID = event.properties.sessionID
      if (subagentSessions.has(sessionID)) {
        subagentSessions.delete(sessionID)  // Cleanup
        return  // Skip subagent
      }
      // Handle main session completion
    }
  }
}
```

**Key insight:** `session.created` provides `event.properties.info.parentID` for subagent sessions, while main sessions have no `parentID`. Use this to build a tracking Set.

### 5. Plugin Initialization Errors

Return empty hooks object if initialization fails:

```javascript
export const MyPlugin = async ({ client, directory }) => {
  const log = (level, message, extra) => 
    client.app.log({ body: { service: "my-plugin", level, message, extra } })
  
  const config = loadConfig(directory, log)
  
  if (!config) {
    await log("warn", "Disabled - no config found")
    return {}  // Empty hooks, plugin is effectively disabled
  }
  
  return {
    // Normal hooks...
  }
}
```

### 6. Error Handling in Hooks

Errors thrown in hooks affect the operation:

```javascript
"tool.execute.before": async (input, output) => {
  // Throwing an error BLOCKS the tool execution
  if (shouldBlock) {
    throw new Error("Operation blocked")  // Tool will not run
  }
  
  // To log without blocking, use try/catch
  try {
    await riskyOperation()
  } catch (err) {
    await log("error", `Non-blocking error: ${err.message}`)
    // Tool continues normally
  }
}
```

### 7. Async Hook Execution

All hooks are async and should await their operations:

```javascript
// WRONG - fire and forget, may not complete
event: async ({ event }) => {
  sendNotification()  // Missing await
}

// CORRECT
event: async ({ event }) => {
  await sendNotification()
}
```

## TypeScript Support

For type safety, use the plugin types:

```typescript
import type { Plugin } from "@opencode-ai/plugin"
import { tool } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  return {
    event: async ({ event }) => {
      if (event.type === 'session.created') {
        // event.properties.info is typed as Session
      }
    },
    
    tool: {
      myTool: tool({
        description: "Typed tool",
        args: {
          input: tool.schema.string(),
        },
        async execute(args) {
          return args.input.toUpperCase()  // args.input is string
        },
      }),
    },
  }
}
```

## Dependencies

To use npm packages in local plugins, create a `package.json`:

```json
// ~/.config/opencode/package.json or .opencode/package.json
{
  "dependencies": {
    "ignore": "^5.3.0",
    "lodash": "^4.17.21"
  }
}
```

OpenCode runs `bun install` at startup to install dependencies.

## Debugging Tips

1. **Use client.app.log()** instead of console.log for structured logging
2. **Check plugin load order** - later plugins can override earlier ones
3. **Verify event types** - log `event.type` to see what events fire
4. **Test hooks in isolation** - create minimal plugins to test specific hooks
5. **Check for typos in hook names** - hooks must match exactly
6. **Use file-based debug logging** when client.app.log output isn't visible

### File-Based Debug Logging

When `client.app.log()` output isn't visible (e.g., in `--print-logs`), use temporary file logging:

```javascript
import { appendFileSync } from 'fs'

const DEBUG_FILE = '/tmp/my-plugin-debug.log'
const debugLog = (msg) => {
  try {
    appendFileSync(DEBUG_FILE, `${new Date().toISOString()} - ${msg}\n`)
  } catch (e) { /* ignore */ }
}

// In your hook:
"chat.message": async (input, output) => {
  debugLog(`chat.message called`)
  debugLog(`input keys: ${JSON.stringify(Object.keys(input))}`)
  debugLog(`sessionID: ${input.sessionID}`)
  // ... rest of hook
}
```

Then check the log: `cat /tmp/my-plugin-debug.log`

**Remember to remove debug logging before committing!**

### Testing with CLI vs TUI

- **CLI (`oc run --model X "msg"`)**: Model is set at session creation
- **TUI (`oc` then `/models` then message)**: Model is set on first message

Always test both flows when dealing with model/session timing.

## Complete Plugin Template

```javascript
import { readFileSync, writeFileSync, existsSync } from 'fs'
import { join } from 'path'

export const MyPlugin = async ({ project, client, $, directory, worktree }) => {
  // Create logging helper - ALWAYS use this instead of console.log/error
  const log = (level, message, extra) => 
    client.app.log({ body: { service: "my-plugin", level, message, extra } })
  
  // Configuration
  const configDir = process.env.HOME
    ? join(process.env.HOME, '.config', 'opencode')
    : directory
  
  // Load config/state
  const config = loadConfig(configDir, log)
  if (!config) {
    await log("warn", "Disabled - no config found")
    return {}
  }
  
  // Helper functions
  const saveState = (state) => {
    writeFileSync(join(configDir, 'my-plugin-state.json'), JSON.stringify(state, null, 2))
  }
  
  return {
    // Event handler
    event: async ({ event }) => {
      if (event.type === 'session.created') {
        const session = event.properties.info
        await log("info", `Session created: ${session.id}`)
      }
    },
    
    // Message interceptor
    "chat.message": async (input, output) => {
      // Modify messages before processing
    },
    
    // Tool guard
    "tool.execute.before": async (input, output) => {
      // Block or modify tool calls
    },
    
    // Tool logging
    "tool.execute.after": async (input, output) => {
      // Log or process tool results
    },
  }
}

function loadConfig(configDir, log) {
  const path = join(configDir, 'my-plugin-config.json')
  if (!existsSync(path)) return null
  try {
    return JSON.parse(readFileSync(path, 'utf-8'))
  } catch (err) {
    log?.("error", `Failed to load config: ${err.message}`)
    return null
  }
}
```

## Real-World Example: First-Message Injection with Session Tracking

This pattern injects content on the first message of each session while preserving model selection:

```javascript
import { readFileSync, existsSync } from 'fs'
import { join } from 'path'

export const BootstrapPlugin = async ({ project, client, $, directory, worktree }) => {
  const log = (level, message, extra) => 
    client.app.log({ body: { service: "bootstrap", level, message, extra } })

  const configDir = process.env.HOME
    ? join(process.env.HOME, '.config', 'opencode')
    : directory

  // Load configuration
  const config = loadConfig(configDir)
  if (!config) {
    await log("warn", "Disabled - no config found")
    return {}
  }

  // Track which sessions have been bootstrapped
  // Using Map for in-memory tracking (resets on restart)
  const bootstrappedSessions = new Map()

  // Helper for post-compaction injection (session already has model set)
  const injectViaPrompt = async (sessionID, content) => {
    try {
      // Fetch session to get current model/agent
      const session = await client.session.get({ path: { id: sessionID } })
      
      await client.session.prompt({
        path: { id: sessionID },
        body: {
          noReply: true,
          parts: [{ type: "text", text: content, synthetic: true }],
          model: session?.model,
          agent: session?.agent,
        }
      })
    } catch (err) {
      await log("error", `Injection failed: ${err.message}`)
    }
  }

  return {
    event: async ({ event }) => {
      const getSessionID = () => 
        event.properties?.info?.id || event.properties?.sessionID

      // Mark new sessions as needing bootstrap
      if (event.type === 'session.created') {
        const sessionID = getSessionID()
        if (sessionID) {
          bootstrappedSessions.set(sessionID, false)
        }
      }

      // Re-inject after compaction (session.prompt is safe here)
      if (event.type === 'session.compacted') {
        const sessionID = getSessionID()
        if (sessionID) {
          await injectViaPrompt(sessionID, config.compactContent)
        }
      }

      // Cleanup on session delete
      if (event.type === 'session.deleted') {
        const sessionID = getSessionID()
        if (sessionID) {
          bootstrappedSessions.delete(sessionID)
        }
      }
    },

    // First-message bootstrap - preserves model selection
    "chat.message": async (input, output) => {
      const textPart = output.parts.find(p => p.type === "text")
      if (!textPart) return

      const sessionID = input.sessionID
      let prefix = ""

      // Inject bootstrap on first message
      if (sessionID && bootstrappedSessions.get(sessionID) !== true) {
        prefix = config.bootstrapContent + "\n\n"
        bootstrappedSessions.set(sessionID, true)
      } else if (!sessionID) {
        // Fallback: always inject if no sessionID (shouldn't happen)
        prefix = config.bootstrapContent + "\n\n"
      }

      // Apply prefix
      if (prefix) {
        textPart.text = prefix + textPart.text
      }
    },
  }
}

function loadConfig(configDir) {
  const path = join(configDir, 'bootstrap-config.json')
  if (!existsSync(path)) return null
  try {
    return JSON.parse(readFileSync(path, 'utf-8'))
  } catch {
    return null
  }
}
```

**Key patterns in this example:**
1. **Session tracking with Map** - Track first-message state per session
2. **Dual injection strategy** - `chat.message` for first message, `session.prompt` for compaction
3. **Model preservation** - First message modifies text (no API call), compaction fetches session model
4. **Graceful degradation** - Falls back to injection if sessionID unavailable
