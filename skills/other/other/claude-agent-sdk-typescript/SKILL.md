---
name: claude-agent-sdk-typescript
description: >
  Expert guidance for building AI agents with the Claude Agent SDK in TypeScript/JavaScript.
  Use when the user writes TypeScript or JavaScript code with the SDK, imports from
  "@anthropic-ai/claude-agent-sdk", uses query(), allowedTools, permissionMode, creates
  custom tools with createSdkMcpServer, sets up hooks, integrates MCP servers, manages
  sessions, or debugs SDK issues in TypeScript/Node.js.
  Also triggers on: "@anthropic-ai/claude-agent-sdk", "allowedTools", "permissionMode",
  "npm install", "for await", "AgentDefinition", or "settingSources".
---

# Claude Agent SDK — TypeScript Guide

Production guidance for building AI agents with the Claude Agent SDK in TypeScript.

> **Naming**: The Claude Code SDK was renamed to the Claude Agent SDK (v0.1.0+).
> Package: `npm install @anthropic-ai/claude-agent-sdk` · Import: `import { query } from "@anthropic-ai/claude-agent-sdk"`

## Quick Reference — Two Interaction Modes

### 1. `query()` — Stateless, One-Shot

Best for: independent tasks, automation scripts, CI pipelines.

```typescript
import { query, type ClaudeAgentOptions } from "@anthropic-ai/claude-agent-sdk";

const options: ClaudeAgentOptions = {
  allowedTools: ["Read", "Edit", "Glob"],
  permissionMode: "acceptEdits",
};

for await (const message of query({
  prompt: "Review utils.ts for bugs. Fix any issues you find.",
  options,
})) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if ("text" in block) console.log(block.text);
      else if ("name" in block) console.log(`Tool: ${block.name}`);
    }
  }
  if (message.type === "result") {
    console.log(`Done: ${message.subtype}`);
  }
}
```

### 2. `ClaudeSDKClient` — Stateful, Multi-Turn

Best for: conversations, follow-up questions, interactive apps.

```typescript
import { ClaudeSDKClient } from "@anthropic-ai/claude-agent-sdk";

const client = new ClaudeSDKClient({
  options: {
    allowedTools: ["Read", "Write", "Bash"],
    permissionMode: "acceptEdits",
  },
});

try {
  await client.query("Analyze the codebase structure");
  for await (const msg of client.receiveMessages()) {
    console.log(msg);
  }
  // Continue the conversation with context preserved
  await client.query("Now refactor the largest file you found");
  for await (const msg of client.receiveMessages()) {
    console.log(msg);
  }
} finally {
  await client.close();
}
```

## ClaudeAgentOptions — Complete Configuration

All options are optional. Key fields (all camelCase):

| Field | Type | Description |
|-------|------|-------------|
| `allowedTools` | `string[]` | Tools Claude can use. See Built-in Tools below. |
| `disallowedTools` | `string[]` | Explicitly block specific tools. |
| `permissionMode` | `string` | `"default"`, `"acceptEdits"`, or `"bypassPermissions"`. |
| `systemPrompt` | `string \| object` | Custom instructions. Use `{ type: "preset", preset: "claude_code" }` for CC default. |
| `model` | `string` | e.g. `"sonnet"`, `"opus"`, `"haiku"`, or full model string. |
| `cwd` | `string` | Working directory for the agent. |
| `maxTurns` | `number` | Maximum agentic loop iterations. |
| `settingSources` | `string[]` | `["user", "project"]` to load Skills/CLAUDE.md from filesystem. |
| `mcpServers` | `Record<string, McpServerConfig>` | MCP server configurations. |
| `agents` | `Record<string, AgentDefinition>` | Named subagent definitions. |
| `hooks` | `object` | Lifecycle hook callbacks. |

### Built-in Tools

Tool names for `allowedTools`:

- **File ops**: `Read`, `Write`, `Edit`, `MultiEdit`
- **Search**: `Glob`, `Grep`
- **Execution**: `Bash`
- **Web**: `WebSearch`, `WebFetch`
- **Delegation**: `Task` (required for subagents)
- **Skills**: `Skill` (requires `settingSources`)

## Custom Tools via SDK MCP Server

Define in-process tools without a separate MCP server process:

```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";

const searchOrders = tool(
  "search_orders",
  "Search orders by customer ID",
  { customer_id: "string", status: "string" },
  async (args) => {
    const results = await db.queryOrders(args.customer_id, args.status);
    return { content: [{ type: "text", text: JSON.stringify(results) }] };
  }
);

const sendEmail = tool(
  "send_email",
  "Send an email notification",
  { to: "string", subject: "string", body: "string" },
  async (args) => {
    await emailService.send(args.to, args.subject, args.body);
    return { content: [{ type: "text", text: `Email sent to ${args.to}` }] };
  }
);

const server = createSdkMcpServer({
  name: "business-tools",
  tools: [searchOrders, sendEmail],
});

for await (const msg of query({
  prompt: "Find recent orders for customer C-123",
  options: {
    mcpServers: { biz: server },
    allowedTools: ["mcp__biz__search_orders", "mcp__biz__send_email"],
  },
})) {
  console.log(msg);
}
```

**Tool naming convention**: MCP tools are accessed as `mcp__<server-name>__<tool-name>`.

## Subagents

Delegate specialized tasks to isolated agents with their own context and tool permissions:

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review auth module for security issues, then write tests",
  options: {
    allowedTools: ["Read", "Grep", "Glob", "Task"], // Task is required
    agents: {
      "security-reviewer": {
        description: "Security specialist. Use for vulnerability analysis.",
        prompt: "You are a security expert. Analyze code for OWASP Top 10...",
        tools: ["Read", "Grep", "Glob"],
        model: "opus",
      },
      "test-writer": {
        description: "Test specialist. Use to generate test suites.",
        prompt: "You are a testing expert. Write comprehensive unit tests...",
        tools: ["Read", "Write", "Bash"],
        model: "sonnet",
      },
    },
  },
})) {
  if (message.type === "result") console.log(message.result);
}
```

**Factory pattern** for dynamic agents:

```typescript
import type { AgentDefinition } from "@anthropic-ai/claude-agent-sdk";

function createReviewer(language: string): AgentDefinition {
  return {
    description: `${language} code review specialist`,
    prompt: `You are an expert ${language} developer...`,
    tools: ["Read", "Grep", "Glob"],
    model: ["rust", "c++"].includes(language) ? "opus" : "sonnet",
  };
}
```

## Hooks — Lifecycle Callbacks

Available events: `PreToolUse`, `PostToolUse`, `Stop`, `SessionStart`, `SessionEnd`, `UserPromptSubmit`.

```typescript
import { query, type HookCallback } from "@anthropic-ai/claude-agent-sdk";
import { appendFileSync } from "node:fs";

const blockDangerousCommands: HookCallback = async (input) => {
  if (input.tool_name === "Bash") {
    const cmd = input.tool_input?.command ?? "";
    const dangers = ["rm -rf /", "DROP TABLE", "mkfs"];
    if (dangers.some((d) => cmd.includes(d))) {
      return {
        hookSpecificOutput: {
          hookEventName: "PreToolUse",
          permissionDecision: "deny",
          permissionDecisionReason: `Blocked dangerous command: ${cmd}`,
        },
      };
    }
  }
  return {};
};

const auditLog: HookCallback = async (input) => {
  appendFileSync(
    "audit.log",
    `${new Date().toISOString()}: ${input.tool_name}: ${JSON.stringify(input.tool_input)}\n`
  );
  return {};
};

for await (const msg of query({
  prompt: "Refactor utils.ts",
  options: {
    permissionMode: "acceptEdits",
    hooks: {
      PreToolUse: [
        { matcher: "Bash", hooks: [blockDangerousCommands] },
        { matcher: ".*", hooks: [auditLog] },
      ],
    },
  },
})) {
  if (message.type === "result") console.log(msg.result);
}
```

## MCP Integration (External Servers)

```typescript
for await (const msg of query({
  prompt: "List open issues in the repo",
  options: {
    mcpServers: {
      github: {
        type: "stdio",
        command: "npx",
        args: ["-y", "@modelcontextprotocol/server-github"],
        env: { GITHUB_TOKEN: process.env.GITHUB_TOKEN! },
      },
      postgres: {
        type: "stdio",
        command: "docker",
        args: ["run", "mcp-postgres-server"],
        env: { DATABASE_URL: process.env.DATABASE_URL! },
      },
    },
    allowedTools: ["mcp__github", "mcp__postgres"],
  },
})) {
  console.log(msg);
}
```

You can mix SDK MCP servers (in-process) and external MCP servers in the same config.

## Using Skills in the SDK

Skills are filesystem-based and must be explicitly enabled:

```typescript
for await (const msg of query({
  prompt: "Help me process this PDF",
  options: {
    cwd: "/path/to/project",
    settingSources: ["user", "project"], // REQUIRED — loads Skills from filesystem
    allowedTools: ["Skill", "Read", "Write", "Bash"],
  },
})) {
  console.log(msg);
}
```

**Common mistake**: forgetting `settingSources`. Without it, Skills won't be discovered even if `"Skill"` is in `allowedTools`.

Skill locations:
- **Project**: `.claude/skills/*/SKILL.md` (shared via git)
- **User**: `~/.claude/skills/*/SKILL.md` (personal, cross-project)

Note: The `allowed-tools` field in SKILL.md frontmatter **only works in Claude Code CLI**, not in the SDK. Use `allowedTools` in options to control tool access.

## Sessions and Conversation Management

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

let sessionId: string | undefined;

// First interaction — capture sessionId
for await (const msg of query({
  prompt: "Review this codebase and identify the top 3 issues",
  options: { allowedTools: ["Read", "Glob", "Grep"] },
})) {
  if (msg.type === "system" && "session_id" in msg) {
    sessionId = msg.session_id;
  }
  console.log(msg);
}

// Resume with context
for await (const msg of query({
  prompt: "Now fix issue #1 that you found",
  options: {
    sessionId,
    allowedTools: ["Read", "Edit", "Bash"],
    permissionMode: "acceptEdits",
  },
})) {
  console.log(msg);
}
```

## System Prompt Configuration

```typescript
// 1. Custom system prompt (v0.1.0+ default: minimal prompt)
const options = { systemPrompt: "You are a senior TypeScript engineer..." };

// 2. Claude Code's full system prompt (opt-in)
const options = {
  systemPrompt: { type: "preset", preset: "claude_code" },
};

// 3. No system prompt — SDK default (minimal)
const options = {}; // uses minimal built-in prompt
```

**Breaking change in v0.1.0**: The SDK no longer loads Claude Code's system prompt by default. If you need the old behavior, explicitly set `preset: "claude_code"`.

## Authentication

```bash
# Direct API (default)
export ANTHROPIC_API_KEY=your-api-key

# Amazon Bedrock
export CLAUDE_CODE_USE_BEDROCK=1
# + configure AWS credentials

# Google Vertex AI
export CLAUDE_CODE_USE_VERTEX=1
# + configure GCP credentials

# Microsoft Azure AI Foundry
export CLAUDE_CODE_USE_FOUNDRY=1
# + configure Azure credentials
```

## Common Patterns

### Batch Processing (Parallel Agents)

```typescript
async function processFile(filepath: string): Promise<string | undefined> {
  for await (const msg of query({
    prompt: `Review ${filepath} for security issues`,
    options: {
      allowedTools: ["Read", "Grep"],
      maxTurns: 50,
    },
  })) {
    if (msg.type === "result") return msg.result;
  }
}

const results = await Promise.all([
  processFile("auth.ts"),
  processFile("payments.ts"),
  processFile("users.ts"),
]);
```

### Structured Output Collection

```typescript
const messages: Message[] = [];
for await (const msg of query({ prompt: "Analyze this codebase", options })) {
  messages.push(msg);
}

// Extract final result
const result = messages.findLast((m) => "result" in m)?.result;
```

### Error Handling

```typescript
import { CLINotFoundError, CLIConnectionError } from "@anthropic-ai/claude-agent-sdk";

try {
  for await (const msg of query({ prompt: "...", options })) {
    console.log(msg);
  }
} catch (error) {
  if (error instanceof CLINotFoundError) {
    console.error("Claude Code CLI not found. Install: curl -fsSL https://claude.ai/install.sh | bash");
  } else if (error instanceof CLIConnectionError) {
    console.error(`Connection error: ${error.message}`);
  } else {
    throw error;
  }
}
```

## Migration from Claude Code SDK (< v0.1.0)

Key changes:
1. `@anthropic-ai/claude-code` → `@anthropic-ai/claude-agent-sdk`
2. `ClaudeCodeOptions` → `ClaudeAgentOptions` (type name)
3. System prompt no longer loads Claude Code's prompt by default
4. `settingSources` must be explicitly set (was auto-loaded before)

## Best Practices

1. **Principle of least privilege**: Only grant tools the agent actually needs.
2. **Use `permissionMode: "acceptEdits"` for automation**, `"default"` for interactive use.
3. **Prefer SDK MCP servers** over external ones for custom tools — less overhead, easier debugging.
4. **Use subagents for specialized tasks** — isolate context and apply the right model per task.
5. **Add hooks for safety** — block dangerous commands and audit tool usage in production.
6. **Set `maxTurns`** to prevent runaway agents in production environments.
7. **Use `cwd`** to scope the agent to a specific directory.
8. **Capture `sessionId`** from system messages if you need conversation continuity.

> For troubleshooting common issues, see `references/troubleshooting.md`.

## Official Resources

- Overview: https://platform.claude.com/docs/en/agent-sdk/overview
- Quickstart: https://platform.claude.com/docs/en/agent-sdk/quickstart
- TypeScript reference: https://platform.claude.com/docs/en/agent-sdk/typescript
- Migration guide: https://platform.claude.com/docs/en/agent-sdk/migration-guide
- TypeScript SDK repo: https://github.com/anthropics/claude-agent-sdk-typescript
- Demo agents: https://github.com/anthropics/claude-agent-sdk-demos
- Cookbook: https://platform.claude.com/cookbook
