# OpenCode Plugins

Guide for creating OpenCode plugins. Use when building plugins to extend OpenCode with custom hooks, tools, or integrations.

## Plugin Location

Plugins are loaded from:
1. `.opencode/plugin/` - Project-level (preferred)
2. `~/.config/opencode/plugin/` - Global

## Basic Structure

```typescript
import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ project, client, $, directory, worktree }) => {
  // project: Current project information
  // client: OpenCode SDK client for AI interaction
  // $: Bun shell API for executing commands
  // directory: Current working directory
  // worktree: Git worktree path
  
  return {
    // Hook implementations
  }
}
```

## Available Hooks

### Core Hooks

| Hook | Signature | Purpose |
|------|-----------|---------|
| `event` | `(input: { event: Event }) => Promise<void>` | Generic event handler for all events |
| `config` | `(input: Config) => Promise<void>` | Modify configuration |
| `tool` | `{ [key: string]: ToolDefinition }` | Register custom tools |
| `auth` | `AuthHook` | Custom authentication providers |

### Chat Hooks

| Hook | Signature | Purpose |
|------|-----------|---------|
| `chat.message` | `(input, output: { message: UserMessage; parts: Part[] }) => Promise<void>` | Modify user messages before sending |
| `chat.params` | `(input, output: { temperature, topP, topK, options }) => Promise<void>` | Modify LLM parameters |

### Tool Execution Hooks

| Hook | Signature | Purpose |
|------|-----------|---------|
| `tool.execute.before` | `(input: { tool, sessionID, callID }, output: { args }) => Promise<void>` | Intercept before tool runs |
| `tool.execute.after` | `(input: { tool, sessionID, callID }, output: { title, output, metadata }) => Promise<void>` | Process after tool completes |

### Permission Hooks

| Hook | Signature | Purpose |
|------|-----------|---------|
| `permission.ask` | `(input: Permission, output: { status: "ask" \| "deny" \| "allow" }) => Promise<void>` | Auto-approve/deny permissions |

### Experimental Hooks

| Hook | Signature | Purpose |
|------|-----------|---------|
| `experimental.chat.system.transform` | `(input: {}, output: { system: string[] }) => Promise<void>` | **Modify system prompt** |
| `experimental.chat.messages.transform` | `(input: {}, output: { messages }) => Promise<void>` | Transform message history |
| `experimental.session.compacting` | `(input: { sessionID }, output: { context: string[]; prompt?: string }) => Promise<void>` | **Add context during compaction** |
| `experimental.text.complete` | `(input: { sessionID, messageID, partID }, output: { text }) => Promise<void>` | Text completion |

## Common Patterns

### Inject Context into System Prompt

Best for project-specific reminders that should appear in every conversation:

```typescript
export const ContextPlugin: Plugin = async () => {
  const REMINDER = `
## Project Guidelines
- Always run tests before committing
- Use TypeScript strict mode
`.trim()

  return {
    "experimental.chat.system.transform": async (_input, output) => {
      output.system.push(REMINDER)
    }
  }
}
```

### Preserve Context During Compaction

Ensures important context survives session compaction:

```typescript
export const CompactionPlugin: Plugin = async () => {
  return {
    "experimental.session.compacting": async (_input, output) => {
      output.context.push("## Critical Context\n- Key fact 1\n- Key fact 2")
    }
  }
}
```

### Custom Compaction Prompt

Replace the default compaction prompt entirely:

```typescript
export const CustomCompactionPlugin: Plugin = async () => {
  return {
    "experimental.session.compacting": async (_input, output) => {
      output.prompt = `You are summarizing a coding session.
Focus on: current task, files modified, next steps.`
    }
  }
}
```

### Protect Sensitive Files

Prevent reading `.env` or other sensitive files:

```typescript
export const EnvProtection: Plugin = async () => {
  return {
    "tool.execute.before": async (input, output) => {
      if (input.tool === "read" && output.args.filePath?.includes(".env")) {
        throw new Error("Reading .env files is not allowed")
      }
    }
  }
}
```

### Send Notifications

Use macOS notifications for session events:

```typescript
export const NotificationPlugin: Plugin = async ({ $ }) => {
  return {
    event: async ({ event }) => {
      if (event.type === "session.idle") {
        await $`osascript -e 'display notification "Done!" with title "OpenCode"'`
      }
    }
  }
}
```

### Custom Tools

Add project-specific tools:

```typescript
import { tool } from "@opencode-ai/plugin"

export const CustomToolsPlugin: Plugin = async () => {
  return {
    tool: {
      myTool: tool({
        description: "Does something useful",
        args: {
          input: tool.schema.string(),
          count: tool.schema.number().optional(),
        },
        async execute(args, ctx) {
          return `Processed: ${args.input} (count: ${args.count ?? 1})`
        },
      }),
    },
  }
}
```

## Event Types

Available events for the `event` hook:

### Session Events
- `session.created` - New session started
- `session.compacted` - Session was compacted
- `session.deleted` - Session deleted
- `session.diff` - Changes detected
- `session.error` - Error occurred
- `session.idle` - Session became idle
- `session.status` - Status changed
- `session.updated` - Session updated

### Message Events
- `message.updated` - Message changed
- `message.removed` - Message deleted
- `message.part.updated` - Part of message changed
- `message.part.removed` - Part of message deleted

### File Events
- `file.edited` - File was edited
- `file.watcher.updated` - File watcher detected change

### Other Events
- `command.executed` - Command ran
- `installation.updated` - Installation changed
- `lsp.client.diagnostics` - LSP diagnostics received
- `lsp.updated` - LSP state changed
- `permission.replied` - Permission answered
- `permission.updated` - Permission changed
- `server.connected` - Server connected
- `todo.updated` - Todo list changed
- `tool.execute.after` - Tool finished
- `tool.execute.before` - Tool starting

## Package Setup

For TypeScript support, ensure `.opencode/package.json` has:

```json
{
  "dependencies": {
    "@opencode-ai/plugin": "^1.0.203"
  }
}
```

Then run `bun install` in the `.opencode/` directory.

## Best Practices

1. **Use TypeScript** - Get type safety and better IDE support
2. **Keep plugins focused** - One plugin per concern
3. **Use experimental hooks carefully** - They may change
4. **Test locally first** - Plugins run on every session
5. **Don't block** - Hooks should be fast; use async for slow operations
6. **Handle errors gracefully** - Throwing stops the hook chain

## Reference

- [Official Docs](https://opencode.ai/docs/plugins/)
- [Plugin Source](https://github.com/sst/opencode/tree/dev/packages/plugin)
- [Ecosystem Examples](https://opencode.ai/docs/ecosystem/#plugins)
