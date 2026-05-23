---
name: creating-opencode-plugins
description: Use when creating OpenCode plugins that hook into command, file, LSP, message, permission, server, session, todo, tool, or TUI events - provides plugin structure, event API specifications, and implementation patterns for JavaScript/TypeScript event-driven modules
---

# Creating OpenCode Plugins

## Overview

OpenCode plugins are JavaScript/TypeScript modules that hook into 25+ events across the OpenCode AI assistant lifecycle. Plugins export an async function receiving context (project, client, $, directory, worktree) and return an event handler.

## When to Use

**Create an OpenCode plugin when:**
- Intercepting file operations (prevent sharing .env files)
- Monitoring command execution (notifications, logging)
- Processing LSP diagnostics (custom error handling)
- Managing permissions (auto-approve trusted operations)
- Reacting to session lifecycle (cleanup, initialization)
- Extending tool capabilities (custom tool registration)
- Enhancing TUI interactions (custom prompts, toasts)

**Don't create for:**
- Simple prompt instructions (use agents instead)
- One-time scripts (use bash tools)
- Static configuration (use settings files)

## Quick Reference

### Plugin Structure

```javascript
export const MyPlugin = async (context) => {
  // context: { project, client, $, directory, worktree }

  return {
    event: async ({ event }) => {
      // event: { type: 'event.name', data: {...} }

      switch(event.type) {
        case 'file.edited':
          // Handle file edits
          break;
        case 'tool.execute.before':
          // Pre-process tool execution
          break;
      }
    }
  };
};
```

### Event Categories

| Category | Events | Use Cases |
|----------|--------|-----------|
| **command** | `command.executed` | Track command history, notifications |
| **file** | `file.edited`, `file.watcher.updated` | File validation, auto-formatting |
| **installation** | `installation.updated` | Dependency tracking |
| **lsp** | `lsp.client.diagnostics`, `lsp.updated` | Custom error handling |
| **message** | `message.*.updated/removed` | Message filtering, logging |
| **permission** | `permission.replied/updated` | Permission policies |
| **server** | `server.connected` | Connection monitoring |
| **session** | `session.created/deleted/error/idle/status/updated/compacted/diff` | Session management |
| **todo** | `todo.updated` | Todo synchronization |
| **tool** | `tool.execute.before/after` | Tool interception, augmentation |
| **tui** | `tui.prompt.append`, `tui.command.execute`, `tui.toast.show` | UI customization |

### Plugin Manifest (package.json or separate config)

```json
{
  "name": "env-protection",
  "description": "Prevents sharing .env files",
  "version": "1.0.0",
  "author": "Security Team",
  "plugin": {
    "file": "plugin.js",
    "location": "global"
  },
  "hooks": {
    "file": ["file.edited"],
    "permission": ["permission.replied"]
  }
}
```

## Implementation

### Complete Example: Environment File Protection

```javascript
// .opencode/plugin/env-protection.js

export const EnvProtectionPlugin = async ({ project, client }) => {
  const sensitivePatterns = [
    /\.env$/,
    /\.env\..+$/,
    /credentials\.json$/,
    /\.secret$/,
  ];

  const isSensitiveFile = (filePath) => {
    return sensitivePatterns.some(pattern => pattern.test(filePath));
  };

  return {
    event: async ({ event }) => {
      switch (event.type) {
        case 'file.edited': {
          const { path } = event.data;

          if (isSensitiveFile(path)) {
            console.warn(`⚠️  Sensitive file edited: ${path}`);
            console.warn('This file should not be shared or committed.');
          }
          break;
        }

        case 'permission.replied': {
          const { action, target, decision } = event.data;

          // Block read/share operations on sensitive files
          if ((action === 'read' || action === 'share') &&
              isSensitiveFile(target) &&
              decision === 'allow') {

            console.error(`🚫 Blocked ${action} operation on sensitive file: ${target}`);

            // Override permission decision
            return {
              override: true,
              decision: 'deny',
              reason: 'Sensitive file protection policy'
            };
          }
          break;
        }
      }
    }
  };
};
```

### Example: Command Execution Notifications

```javascript
// .opencode/plugin/notify.js

export const NotifyPlugin = async ({ project, $ }) => {
  let commandStartTime = null;

  return {
    event: async ({ event }) => {
      switch (event.type) {
        case 'command.executed': {
          const { command, args, status } = event.data;
          commandStartTime = Date.now();

          console.log(`▶️  Executing: ${command} ${args.join(' ')}`);
          break;
        }

        case 'tool.execute.after': {
          const { tool, duration, success } = event.data;

          if (duration > 5000) {
            // Notify for long-running operations
            await $`osascript -e 'display notification "Completed in ${duration}ms" with title "${tool}"'`;
          }

          console.log(`✅ ${tool} completed in ${duration}ms`);
          break;
        }
      }
    }
  };
};
```

### Example: Custom Tool Registration

```javascript
// .opencode/plugin/custom-tools.js

export const CustomToolsPlugin = async ({ client }) => {
  // Register custom tool on initialization
  await client.registerTool({
    name: 'lint',
    description: 'Run linter on current file with auto-fix option',
    parameters: {
      type: 'object',
      properties: {
        fix: {
          type: 'boolean',
          description: 'Auto-fix issues'
        }
      }
    },
    handler: async ({ fix }) => {
      const result = await $`eslint ${fix ? '--fix' : ''} .`;
      return {
        output: result.stdout,
        errors: result.stderr
      };
    }
  });

  return {
    event: async ({ event }) => {
      // Monitor tool usage
      if (event.type === 'tool.execute.before') {
        console.log(`🔧 Tool: ${event.data.tool}`);
      }
    }
  };
};
```

## Installation Locations

| Location | Path | Scope | Use Case |
|----------|------|-------|----------|
| **Global** | `~/.config/opencode/plugin/` | All projects | Security policies, global utilities |
| **Project** | `.opencode/plugin/` | Current project | Project-specific hooks, validators |

## Common Mistakes

| Mistake | Why It Fails | Fix |
|---------|--------------|-----|
| Synchronous event handler | Blocks event loop | Use `async` handlers |
| Missing error handling | Plugin crashes on error | Wrap in try/catch |
| Heavy computation in handler | Slows down operations | Defer to background process |
| Mutating event data directly | Causes side effects | Return override object |
| Not checking event type | Handles wrong events | Use switch/case on `event.type` |
| Forgetting context destructuring | Missing key utilities | Destructure `{ project, client, $, directory, worktree }` |

## Event Data Structures

```typescript
// File Events
interface FileEditedEvent {
  type: 'file.edited';
  data: {
    path: string;
    content: string;
    timestamp: number;
  };
}

// Tool Events
interface ToolExecuteBeforeEvent {
  type: 'tool.execute.before';
  data: {
    tool: string;
    args: Record<string, any>;
    user: string;
  };
}

interface ToolExecuteAfterEvent {
  type: 'tool.execute.after';
  data: {
    tool: string;
    duration: number;
    success: boolean;
    output?: any;
    error?: string;
  };
}

// Permission Events
interface PermissionRepliedEvent {
  type: 'permission.replied';
  data: {
    action: 'read' | 'write' | 'execute' | 'share';
    target: string;
    decision: 'allow' | 'deny';
  };
}
```

## Testing Plugins

```javascript
// Test plugin locally before installation
import { EnvProtectionPlugin } from './env-protection.js';

const mockContext = {
  project: { root: '/test/project' },
  client: {},
  $: async (cmd) => ({ stdout: '', stderr: '' }),
  directory: '/test/project',
  worktree: null
};

const plugin = await EnvProtectionPlugin(mockContext);

// Simulate event
await plugin.event({
  event: {
    type: 'file.edited',
    data: { path: '.env', content: 'SECRET=123', timestamp: Date.now() }
  }
});
```

## Real-World Impact

**Security**: Prevent accidental sharing of credentials (env-protection plugin blocks .env file reads)

**Productivity**: Auto-notify on long-running commands (notify plugin sends system notifications)

**Quality**: Auto-format files on save (file.edited hook runs prettier)

**Monitoring**: Track tool usage patterns (tool.execute hooks log analytics)

## Claude Code Event Mapping

When porting Claude Code hook behavior to OpenCode plugins, use these event mappings:

| Claude Hook | OpenCode Event | Description |
|-------------|----------------|-------------|
| `PreToolUse` | `tool.execute.before` | Run before tool execution, can block |
| `PostToolUse` | `tool.execute.after` | Run after tool execution |
| `UserPromptSubmit` | `message.*` events | Process user prompts |
| `SessionEnd` | `session.idle` | Session completion |

### Example: Claude-like Hook Behavior

```javascript
export const CompatiblePlugin = async (context) => {
  return {
    // Equivalent to Claude's PreToolUse hook
    'tool.execute.before': async (input, output) => {
      if (shouldBlock(input)) {
        throw new Error('Blocked by policy');
      }
    },

    // Equivalent to Claude's PostToolUse hook
    'tool.execute.after': async (result) => {
      console.log(`Tool completed: ${result.tool}`);
    },

    // Equivalent to Claude's SessionEnd hook
    event: async ({ event }) => {
      if (event.type === 'session.idle') {
        await cleanup();
      }
    }
  };
};
```

## Plugin Composition

Combine multiple plugins using [opencode-plugin-compose](https://github.com/ericc-ch/opencode-plugins):

```javascript
import { compose } from "opencode-plugin-compose";

const composedPlugin = compose([
  envProtectionPlugin,
  notifyPlugin,
  customToolsPlugin
]);
// Runs all hooks in sequence
```

## Non-Convertibility Note

**Important**: OpenCode plugins cannot be directly converted from Claude Code hooks due to fundamental differences:

- **Event models differ**: Claude has 4 hook events, OpenCode has 32+
- **Formats differ**: Claude uses executable scripts, OpenCode uses JS/TS modules
- **Execution context differs**: Different context objects and return value semantics

When porting Claude hooks to OpenCode plugins, you'll need to rewrite the logic using the OpenCode plugin API.

---

**Schema Reference**: `packages/converters/schemas/opencode-plugin.schema.json`

**Documentation**: https://opencode.ai/docs/plugins/
