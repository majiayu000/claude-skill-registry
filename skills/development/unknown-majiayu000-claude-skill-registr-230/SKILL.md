---
name: claude-agent-sdk
description: |
  Build autonomous AI agents with Claude Agent SDK. Structured outputs (v0.1.45, Nov 2025) guarantee JSON schema validation, plugins system, hooks for event-driven workflows. Use when: building coding agents with validated JSON responses, SRE systems, security auditors, or troubleshooting CLI not found, structured output validation, session forking errors.
---

# Claude Agent SDK - Structured Outputs & Error Prevention Guide

**Package**: @anthropic-ai/claude-agent-sdk@0.1.50 (Nov 21, 2025)
**Breaking Changes**: v0.1.45 - Structured outputs (Nov 2025), v0.1.0 - No default system prompt, settingSources required

---

## What's New in v0.1.45+ (Nov 2025)

**Major Features:**

### 1. Structured Outputs (v0.1.45, Nov 14, 2025)
- **JSON schema validation** - Guarantees responses match exact schemas
- **`outputFormat` parameter** - Define output structure with JSON schema or Zod
- **Access validated results** - Via `message.structured_output`
- **Beta header required**: `structured-outputs-2025-11-13`
- **Type safety** - Full TypeScript inference with Zod schemas

**Example:**
```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const schema = z.object({
  summary: z.string(),
  sentiment: z.enum(['positive', 'neutral', 'negative']),
  confidence: z.number().min(0).max(1)
});

const response = query({
  prompt: "Analyze this code review feedback",
  options: {
    model: "claude-sonnet-4-5",
    outputFormat: {
      type: "json_schema",
      json_schema: {
        name: "AnalysisResult",
        strict: true,
        schema: zodToJsonSchema(schema)
      }
    }
  }
});

for await (const message of response) {
  if (message.type === 'result' && message.structured_output) {
    // Guaranteed to match schema
    const validated = schema.parse(message.structured_output);
    console.log(`Sentiment: ${validated.sentiment}`);
  }
}
```

### 2. Plugins System (v0.1.27)
- **`plugins` array** - Load local plugin paths
- **Custom plugin support** - Extend agent capabilities

### 3. Hooks System (v0.1.0+)
- **Event-driven callbacks** - PreToolUse, PostToolUse, Notification, UserPromptSubmit
- **Session event hooks** - Monitor and control agent behavior

### 4. Additional Options
- **`fallbackModel`** - Automatic model fallback on failures
- **`maxThinkingTokens`** - Control extended thinking budget
- **`strictMcpConfig`** - Strict MCP configuration validation
- **`continue`** - Resume with new prompt (differs from `resume`)
- **`permissionMode: 'plan'`** - New permission mode for planning workflows

📚 **Docs**: https://platform.claude.com/docs/en/agent-sdk/structured-outputs

---

## The Complete Claude Agent SDK Reference

## Table of Contents

1. [Core Query API](#core-query-api)
2. [Tool Integration](#tool-integration-built-in--custom)
3. [MCP Servers](#mcp-servers-model-context-protocol)
4. [Subagent Orchestration](#subagent-orchestration)
5. [Session Management](#session-management)
6. [Permission Control](#permission-control)
7. [Filesystem Settings](#filesystem-settings)
8. [Message Types & Streaming](#message-types--streaming)
9. [Error Handling](#error-handling)
10. [Known Issues](#known-issues-prevention)

---

## Core Query API

**Key signature:**
```typescript
query(prompt: string | AsyncIterable<SDKUserMessage>, options?: Options)
  -> AsyncGenerator<SDKMessage>
```

**Critical Options:**
- `outputFormat` - Structured JSON schema validation (v0.1.45+)
- `settingSources` - Filesystem settings loading ('user'|'project'|'local')
- `canUseTool` - Custom permission logic callback
- `agents` - Programmatic subagent definitions
- `mcpServers` - MCP server configuration
- `permissionMode` - 'default'|'acceptEdits'|'bypassPermissions'|'plan'

---

## Tool Integration (Built-in + Custom)

**Tool Control:**
- `allowedTools` - Whitelist (takes precedence)
- `disallowedTools` - Blacklist
- `canUseTool` - Custom permission callback (see Permission Control section)

**Built-in Tools:** Read, Write, Edit, Bash, Grep, Glob, WebSearch, WebFetch, Task, NotebookEdit, BashOutput, KillBash, ListMcpResources, ReadMcpResource

---

## MCP Servers (Model Context Protocol)

**Server Types:**
- **In-process** - `createSdkMcpServer()` with `tool()` definitions
- **External** - stdio, HTTP, SSE transport

**Tool Definition:**
```typescript
tool(name: string, description: string, zodSchema, handler)
```

**Handler Return:**
```typescript
{ content: [{ type: "text", text: "..." }], isError?: boolean }
```

### External MCP Servers (stdio)

```typescript
const response = query({
  prompt: "List files and analyze Git history",
  options: {
    mcpServers: {
      // Filesystem server
      "filesystem": {
        command: "npx",
        args: ["@modelcontextprotocol/server-filesystem"],
        env: {
          ALLOWED_PATHS: "/Users/developer/projects:/tmp"
        }
      },
      // Git operations server
      "git": {
        command: "npx",
        args: ["@modelcontextprotocol/server-git"],
        env: {
          GIT_REPO_PATH: "/Users/developer/projects/my-repo"
        }
      }
    },
    allowedTools: [
      "mcp__filesystem__list_files",
      "mcp__filesystem__read_file",
      "mcp__git__log",
      "mcp__git__diff"
    ]
  }
});
```

### External MCP Servers (HTTP/SSE)

```typescript
const response = query({
  prompt: "Analyze data from remote service",
  options: {
    mcpServers: {
      "remote-service": {
        url: "https://api.example.com/mcp",
        headers: {
          "Authorization": "Bearer your-token-here",
          "Content-Type": "application/json"
        }
      }
    },
    allowedTools: ["mcp__remote-service__analyze"]
  }
});
```

### MCP Tool Naming Convention

**Format**: `mcp__<server-name>__<tool-name>`

**CRITICAL:**
- Server name and tool name MUST match configuration
- Use double underscores (`__`) as separators
- Include in `allowedTools` array

**Examples:** `mcp__weather-service__get_weather`, `mcp__filesystem__read_file`

---

## Subagent Orchestration

### AgentDefinition Type

```typescript
type AgentDefinition = {
  description: string;        // When to use this agent
  prompt: string;             // System prompt for agent
  tools?: string[];           // Allowed tools (optional)
  model?: 'sonnet' | 'opus' | 'haiku' | 'inherit';  // Model (optional)
}
```

**Field Details:**

- **description**: When to use agent (used by main agent for delegation)
- **prompt**: System prompt (defines role, inherits main context)
- **tools**: Allowed tools (if omitted, inherits from main agent)
- **model**: Model override (`haiku`/`sonnet`/`opus`/`inherit`)

**Usage:**
```typescript
agents: {
  "security-checker": {
    description: "Security audits and vulnerability scanning",
    prompt: "You check security. Scan for secrets, verify OWASP compliance.",
    tools: ["Read", "Grep", "Bash"],
    model: "sonnet"
  }
}
```

---

## Session Management

**Options:**
- `resume: sessionId` - Continue previous session
- `forkSession: true` - Create new branch from session
- `continue: prompt` - Resume with new prompt (differs from `resume`)

**Session Forking Pattern (Unique Capability):**

```typescript
// Explore alternative without modifying original
const forked = query({
  prompt: "Try GraphQL instead of REST",
  options: {
    resume: sessionId,
    forkSession: true  // Creates new branch, original session unchanged
  }
});
```

**Capture Session ID:**
```typescript
for await (const message of response) {
  if (message.type === 'system' && message.subtype === 'init') {
    sessionId = message.session_id;  // Save for later resume/fork
  }
}
```

---

## Permission Control

**Permission Modes:**
```typescript
type PermissionMode = "default" | "acceptEdits" | "bypassPermissions" | "plan";
```

- `default` - Standard permission checks
- `acceptEdits` - Auto-approve file edits
- `bypassPermissions` - Skip ALL checks (use in CI/CD only)
- `plan` - Planning mode (v0.1.45+)

### Custom Permission Logic

```typescript
const response = query({
  prompt: "Deploy application to production",
  options: {
    permissionMode: "default",
    canUseTool: async (toolName, input) => {
      // Allow read-only operations
      if (['Read', 'Grep', 'Glob'].includes(toolName)) {
        return { behavior: "allow" };
      }

      // Deny destructive bash commands
      if (toolName === 'Bash') {
        const dangerous = ['rm -rf', 'dd if=', 'mkfs', '> /dev/'];
        if (dangerous.some(pattern => input.command.includes(pattern))) {
          return {
            behavior: "deny",
            message: "Destructive command blocked for safety"
          };
        }
      }

      // Require confirmation for deployments
      if (input.command?.includes('deploy') || input.command?.includes('kubectl apply')) {
        return {
          behavior: "ask",
          message: "Confirm deployment to production?"
        };
      }

      // Allow by default
      return { behavior: "allow" };
    }
  }
});
```

### canUseTool Callback

```typescript
type CanUseToolCallback = (
  toolName: string,
  input: any
) => Promise<PermissionDecision>;

type PermissionDecision =
  | { behavior: "allow" }
  | { behavior: "deny"; message?: string }
  | { behavior: "ask"; message?: string };
```

**Examples:**

```typescript
// Block all file writes
canUseTool: async (toolName, input) => {
  if (toolName === 'Write' || toolName === 'Edit') {
    return { behavior: "deny", message: "No file modifications allowed" };
  }
  return { behavior: "allow" };
}

// Require confirmation for specific files
canUseTool: async (toolName, input) => {
  const sensitivePaths = ['/etc/', '/root/', '.env', 'credentials.json'];
  if ((toolName === 'Write' || toolName === 'Edit') &&
      sensitivePaths.some(path => input.file_path?.includes(path))) {
    return {
      behavior: "ask",
      message: `Modify sensitive file ${input.file_path}?`
    };
  }
  return { behavior: "allow" };
}

// Log all tool usage
canUseTool: async (toolName, input) => {
  console.log(`Tool requested: ${toolName}`, input);
  await logToDatabase(toolName, input);
  return { behavior: "allow" };
}
```

---

## Filesystem Settings

**Setting Sources:**
```typescript
type SettingSource = 'user' | 'project' | 'local';
```

- `user` - `~/.claude/settings.json` (global)
- `project` - `.claude/settings.json` (team-shared)
- `local` - `.claude/settings.local.json` (gitignored overrides)

**Default:** NO settings loaded (`settingSources: []`)

### Settings Priority

When multiple sources loaded, settings merge in this order (highest priority first):

1. **Programmatic options** (passed to `query()`) - Always win
2. **Local settings** (`.claude/settings.local.json`)
3. **Project settings** (`.claude/settings.json`)
4. **User settings** (`~/.claude/settings.json`)

**Example:**

```typescript
// .claude/settings.json
{
  "allowedTools": ["Read", "Write", "Edit"]
}

// .claude/settings.local.json
{
  "allowedTools": ["Read"]  // Overrides project settings
}

// Programmatic
const response = query({
  options: {
    settingSources: ["project", "local"],
    allowedTools: ["Read", "Grep"]  // ← This wins
  }
});

// Actual allowedTools: ["Read", "Grep"]
```

**Best Practice:** Use `settingSources: ["project"]` in CI/CD for consistent behavior.

---

## Message Types & Streaming

**Message Types:**
- `system` - Session init/completion (includes `session_id`)
- `assistant` - Agent responses
- `tool_call` - Tool execution requests
- `tool_result` - Tool execution results
- `error` - Error messages
- `result` - Final result (includes `structured_output` for v0.1.45+)

**Streaming Pattern:**
```typescript
for await (const message of response) {
  if (message.type === 'system' && message.subtype === 'init') {
    sessionId = message.session_id;  // Capture for resume/fork
  }
  if (message.type === 'result' && message.structured_output) {
    // Structured output available (v0.1.45+)
    const validated = schema.parse(message.structured_output);
  }
}
```

---

## Error Handling

**Error Codes:**

| Error Code | Cause | Solution |
|------------|-------|----------|
| `CLI_NOT_FOUND` | Claude Code not installed | Install: `npm install -g @anthropic-ai/claude-code` |
| `AUTHENTICATION_FAILED` | Invalid API key | Check ANTHROPIC_API_KEY env var |
| `RATE_LIMIT_EXCEEDED` | Too many requests | Implement retry with backoff |
| `CONTEXT_LENGTH_EXCEEDED` | Prompt too long | Use session compaction, reduce context |
| `PERMISSION_DENIED` | Tool blocked | Check permissionMode, canUseTool |
| `TOOL_EXECUTION_FAILED` | Tool error | Check tool implementation |
| `SESSION_NOT_FOUND` | Invalid session ID | Verify session ID |
| `MCP_SERVER_FAILED` | Server error | Check server configuration |

---

## Known Issues Prevention

This skill prevents **12** documented issues:

### Issue #1: CLI Not Found Error
**Error**: `"Claude Code CLI not installed"`
**Source**: SDK requires Claude Code CLI
**Why It Happens**: CLI not installed globally
**Prevention**: Install before using SDK: `npm install -g @anthropic-ai/claude-code`

### Issue #2: Authentication Failed
**Error**: `"Invalid API key"`
**Source**: Missing or incorrect ANTHROPIC_API_KEY
**Why It Happens**: Environment variable not set
**Prevention**: Always set `export ANTHROPIC_API_KEY="sk-ant-..."`

### Issue #3: Permission Denied Errors
**Error**: Tool execution blocked
**Source**: `permissionMode` restrictions
**Why It Happens**: Tool not allowed by permissions
**Prevention**: Use `allowedTools` or custom `canUseTool` callback

### Issue #4: Context Length Exceeded
**Error**: `"Prompt too long"`
**Source**: Input exceeds model context window
**Why It Happens**: Large codebase, long conversations
**Prevention**: SDK auto-compacts, but reduce context if needed

### Issue #5: Tool Execution Timeout
**Error**: Tool doesn't respond
**Source**: Long-running tool execution
**Why It Happens**: Tool takes too long (>5 minutes default)
**Prevention**: Implement timeout handling in tool implementations

### Issue #6: Session Not Found
**Error**: `"Invalid session ID"`
**Source**: Session expired or invalid
**Why It Happens**: Session ID incorrect or too old
**Prevention**: Capture `session_id` from `system` init message

### Issue #7: MCP Server Connection Failed
**Error**: Server not responding
**Source**: Server not running or misconfigured
**Why It Happens**: Command/URL incorrect, server crashed
**Prevention**: Test MCP server independently, verify command/URL

### Issue #8: Subagent Definition Errors
**Error**: Invalid AgentDefinition
**Source**: Missing required fields
**Why It Happens**: `description` or `prompt` missing
**Prevention**: Always include `description` and `prompt` fields

### Issue #9: Settings File Not Found
**Error**: `"Cannot read settings"`
**Source**: Settings file doesn't exist
**Why It Happens**: `settingSources` includes non-existent file
**Prevention**: Check file exists before including in sources

### Issue #10: Tool Name Collision
**Error**: Duplicate tool name
**Source**: Multiple tools with same name
**Why It Happens**: Two MCP servers define same tool name
**Prevention**: Use unique tool names, prefix with server name

### Issue #11: Zod Schema Validation Error
**Error**: Invalid tool input
**Source**: Input doesn't match Zod schema
**Why It Happens**: Agent provided wrong data type
**Prevention**: Use descriptive Zod schemas with `.describe()`

### Issue #12: Filesystem Permission Denied
**Error**: Cannot access path
**Source**: Restricted filesystem access
**Why It Happens**: Path outside `workingDirectory` or no permissions
**Prevention**: Set correct `workingDirectory`, check file permissions

---

## Official Documentation

- **Agent SDK Overview**: https://platform.claude.com/docs/en/api/agent-sdk/overview
- **TypeScript API**: https://platform.claude.com/docs/en/api/agent-sdk/typescript
- **Structured Outputs**: https://platform.claude.com/docs/en/agent-sdk/structured-outputs
- **GitHub (TypeScript)**: https://github.com/anthropics/claude-agent-sdk-typescript
- **CHANGELOG**: https://github.com/anthropics/claude-agent-sdk-typescript/blob/main/CHANGELOG.md

---

**Token Efficiency**:
- **Without skill**: ~12,000 tokens (MCP setup, permission patterns, session forking, structured outputs, error handling)
- **With skill**: ~3,600 tokens (focused on v0.1.45+ features + error prevention + advanced patterns)
- **Savings**: ~70% (~8,400 tokens)

**Errors prevented**: 12 documented issues with exact solutions
**Key value**: Structured outputs (v0.1.45+), session forking, canUseTool patterns, settingSources priority, MCP naming, error codes

---

**Last verified**: 2025-11-22 | **Skill version**: 2.0.0 | **Changes**: Added v0.1.45 structured outputs, plugins, hooks, new options. Removed tutorial/basic examples (~750 lines). Focused on knowledge gaps + error prevention + advanced patterns.
