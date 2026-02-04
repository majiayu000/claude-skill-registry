---
name: claude-agent-sdk
description: Build coding agents with the Claude Agent SDK. Use when creating agentic workflows, implementing todo tracking, monitoring agent progress, building multi-turn conversations, streaming responses, or integrating custom tools with Claude Code.
---

# Claude Agent SDK

Build autonomous coding agents using the official Claude Agent SDK for TypeScript.

## Quick Start

```bash
npm install @anthropic-ai/claude-agent-sdk
export ANTHROPIC_API_KEY='your-key'
```

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Create a hello world function",
  options: { maxTurns: 10 }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

---

## Core Concepts

### The query() Function

Primary interface for interacting with Claude Code. Returns an async generator that streams messages.

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

const result = query({
  prompt: string | AsyncIterable<SDKUserMessage>,
  options?: Options
});
```

### Key Options

```typescript
interface Options {
  maxTurns?: number;              // Max conversation turns
  model?: string;                 // Claude model to use
  permissionMode?: PermissionMode; // 'default' | 'acceptEdits' | 'bypassPermissions' | 'plan'
  cwd?: string;                   // Working directory
  tools?: string[] | { type: 'preset'; preset: 'claude_code' };
  allowedTools?: string[];        // Whitelist specific tools
  disallowedTools?: string[];     // Blacklist specific tools
  mcpServers?: Record<string, McpServerConfig>; // Custom MCP servers
  hooks?: Partial<Record<HookEvent, HookCallbackMatcher[]>>;
  canUseTool?: CanUseTool;        // Custom permission function
  includePartialMessages?: boolean; // Stream partial messages
  maxBudgetUsd?: number;          // Budget limit
  systemPrompt?: string | { type: 'preset'; preset: 'claude_code'; append?: string };
}
```

### Message Types

```typescript
type SDKMessage =
  | SDKAssistantMessage  // Claude's responses
  | SDKUserMessage       // User inputs
  | SDKResultMessage     // Final result (success or error)
  | SDKSystemMessage     // System init message
  | SDKPartialAssistantMessage; // Streaming chunks
```

#### Processing Messages

```typescript
for await (const message of query({ prompt, options })) {
  switch (message.type) {
    case "system":
      console.log("Session started:", message.session_id);
      break;
    case "assistant":
      // Process tool calls
      for (const block of message.message.content) {
        if (block.type === "text") {
          console.log(block.text);
        } else if (block.type === "tool_use") {
          console.log(`Tool: ${block.name}`, block.input);
        }
      }
      break;
    case "result":
      if (message.subtype === "success") {
        console.log("Final:", message.result);
        console.log("Cost:", message.total_cost_usd);
      } else {
        console.error("Error:", message.errors);
      }
      break;
  }
}
```

---

## Todo Tracking

Track and display task progress using the TodoWrite tool.

### Todo Lifecycle

1. **pending** - Task not yet started
2. **in_progress** - Currently working on (one at a time)
3. **completed** - Task finished

### Todo Structure

```typescript
interface Todo {
  content: string;     // Task description (imperative form)
  status: 'pending' | 'in_progress' | 'completed';
  activeForm: string;  // Present continuous form for display
}
```

### Monitoring Todo Changes

```typescript
for await (const message of query({
  prompt: "Optimize my React app and track progress",
  options: { maxTurns: 15 }
})) {
  if (message.type === "assistant") {
    for (const block of message.message.content) {
      if (block.type === "tool_use" && block.name === "TodoWrite") {
        const todos = block.input.todos;
        displayProgress(todos);
      }
    }
  }
}

function displayProgress(todos: Todo[]) {
  const completed = todos.filter(t => t.status === "completed").length;
  const inProgress = todos.filter(t => t.status === "in_progress").length;

  console.log(`\nProgress: ${completed}/${todos.length} completed`);
  console.log(`Working on: ${inProgress} task(s)\n`);

  todos.forEach((todo, i) => {
    const icon = todo.status === "completed" ? "done" :
                 todo.status === "in_progress" ? ">>>" : "[ ]";
    const text = todo.status === "in_progress" ? todo.activeForm : todo.content;
    console.log(`${i + 1}. ${icon} ${text}`);
  });
}
```

### TodoTracker Class

```typescript
class TodoTracker {
  private todos: Todo[] = [];

  displayProgress() {
    if (this.todos.length === 0) return;

    const completed = this.todos.filter(t => t.status === "completed").length;
    const total = this.todos.length;

    console.log(`Progress: ${completed}/${total} completed`);

    this.todos.forEach((todo, index) => {
      const icon = todo.status === "completed" ? "[x]" :
                  todo.status === "in_progress" ? "[>]" : "[ ]";
      const text = todo.status === "in_progress" ? todo.activeForm : todo.content;
      console.log(`${index + 1}. ${icon} ${text}`);
    });
  }

  async trackQuery(prompt: string) {
    for await (const message of query({
      prompt,
      options: { maxTurns: 20 }
    })) {
      if (message.type === "assistant") {
        for (const block of message.message.content) {
          if (block.type === "tool_use" && block.name === "TodoWrite") {
            this.todos = block.input.todos;
            this.displayProgress();
          }
        }
      }
    }
  }
}
```

---

## Custom Tools

Extend Claude with custom functionality using MCP servers.

### Creating Custom Tools

```typescript
import { query, tool, createSdkMcpServer } from "@anthropic-ai/claude-agent-sdk";
import { z } from "zod";

const customServer = createSdkMcpServer({
  name: "my-tools",
  version: "1.0.0",
  tools: [
    tool(
      "get_weather",
      "Get current temperature for a location",
      {
        latitude: z.number().describe("Latitude coordinate"),
        longitude: z.number().describe("Longitude coordinate")
      },
      async (args) => {
        const response = await fetch(
          `https://api.open-meteo.com/v1/forecast?latitude=${args.latitude}&longitude=${args.longitude}&current=temperature_2m`
        );
        const data = await response.json();
        return {
          content: [{
            type: "text",
            text: `Temperature: ${data.current.temperature_2m}C`
          }]
        };
      }
    )
  ]
});
```

### Using Custom Tools

Custom MCP tools require **streaming input mode** with async generators:

```typescript
async function* generateMessages() {
  yield {
    type: "user" as const,
    message: {
      role: "user" as const,
      content: "What's the weather in San Francisco?"
    }
  };
}

for await (const message of query({
  prompt: generateMessages(),
  options: {
    mcpServers: {
      "my-tools": customServer
    },
    allowedTools: [
      "mcp__my-tools__get_weather"  // Tool name format: mcp__{server}__{tool}
    ],
    maxTurns: 5
  }
})) {
  if (message.type === "result" && message.subtype === "success") {
    console.log(message.result);
  }
}
```

### Database Query Tool Example

```typescript
const dbServer = createSdkMcpServer({
  name: "database",
  tools: [
    tool(
      "query_db",
      "Execute a database query",
      {
        query: z.string().describe("SQL query to execute"),
        params: z.array(z.any()).optional().describe("Query parameters")
      },
      async (args) => {
        const results = await db.query(args.query, args.params || []);
        return {
          content: [{
            type: "text",
            text: `Found ${results.length} rows:\n${JSON.stringify(results, null, 2)}`
          }]
        };
      }
    )
  ]
});
```

---

## Streaming & Multi-turn Conversations

### Streaming Input Mode

Use async generators for multi-turn conversations:

```typescript
async function* chatSession() {
  yield {
    type: "user" as const,
    message: { role: "user" as const, content: "Hello!" }
  };

  // Wait for response, then continue...
  yield {
    type: "user" as const,
    message: { role: "user" as const, content: "What's your name?" }
  };
}

for await (const message of query({
  prompt: chatSession(),
  options: { maxTurns: 10 }
})) {
  // Process messages
}
```

### Including Partial Messages

Enable streaming chunks for real-time display:

```typescript
for await (const message of query({
  prompt: "Write a story",
  options: { includePartialMessages: true }
})) {
  if (message.type === "stream_event") {
    const event = message.event;
    if (event.type === "content_block_delta" && event.delta.type === "text_delta") {
      process.stdout.write(event.delta.text);
    }
  }
}
```

### Session Resumption

```typescript
// First query - capture session_id
let sessionId: string;
for await (const message of query({ prompt: "Start a project" })) {
  if (message.type === "system") {
    sessionId = message.session_id;
  }
}

// Resume later
for await (const message of query({
  prompt: "Continue where we left off",
  options: { resume: sessionId }
})) {
  // Continues previous session
}
```

---

## Hooks & Permissions

### Hook Events

```typescript
type HookEvent =
  | 'PreToolUse'      // Before tool execution
  | 'PostToolUse'     // After tool execution
  | 'PostToolUseFailure'
  | 'Notification'
  | 'UserPromptSubmit'
  | 'SessionStart'
  | 'SessionEnd'
  | 'Stop'
  | 'SubagentStart'
  | 'SubagentStop'
  | 'PreCompact'
  | 'PermissionRequest';
```

### Using Hooks

```typescript
for await (const message of query({
  prompt: "Build an API",
  options: {
    hooks: {
      PreToolUse: [{
        matcher: "Bash",  // Only for Bash tool
        hooks: [async (input, toolUseId, { signal }) => {
          console.log(`Executing: ${input.tool_input.command}`);
          return { continue: true };
        }]
      }],
      PostToolUse: [{
        hooks: [async (input) => {
          console.log(`Tool ${input.tool_name} completed`);
          return { continue: true };
        }]
      }]
    }
  }
})) {
  // Process messages
}
```

### Permission Modes

```typescript
// Default - prompts for permission
options: { permissionMode: 'default' }

// Auto-accept file edits
options: { permissionMode: 'acceptEdits' }

// Bypass all permissions (requires allowDangerouslySkipPermissions)
options: {
  permissionMode: 'bypassPermissions',
  allowDangerouslySkipPermissions: true
}

// Plan mode - no execution
options: { permissionMode: 'plan' }
```

### Custom Permission Logic

```typescript
const result = query({
  prompt: "Deploy my app",
  options: {
    canUseTool: async (toolName, input, { signal, suggestions }) => {
      // Allow read-only tools
      if (["Read", "Glob", "Grep"].includes(toolName)) {
        return { behavior: "allow", updatedInput: input };
      }

      // Block dangerous commands
      if (toolName === "Bash" && input.command?.includes("rm -rf")) {
        return {
          behavior: "deny",
          message: "Destructive commands not allowed",
          interrupt: true
        };
      }

      // Default allow
      return { behavior: "allow", updatedInput: input };
    }
  }
});
```

---

## Error Handling

### Result Subtypes

```typescript
for await (const message of query({ prompt, options })) {
  if (message.type === "result") {
    switch (message.subtype) {
      case "success":
        console.log("Completed:", message.result);
        console.log("Cost: $" + message.total_cost_usd);
        break;
      case "error_max_turns":
        console.error("Max turns exceeded");
        break;
      case "error_during_execution":
        console.error("Execution error:", message.errors);
        break;
      case "error_max_budget_usd":
        console.error("Budget exceeded");
        break;
    }

    // Check permission denials
    if (message.permission_denials?.length > 0) {
      console.log("Denied tools:", message.permission_denials);
    }
  }
}
```

### Abort Operations

```typescript
const abortController = new AbortController();

// Cancel after 30 seconds
setTimeout(() => abortController.abort(), 30000);

for await (const message of query({
  prompt: "Long running task",
  options: { abortController }
})) {
  // Process or abort
}
```

---

## Subagents

Define specialized agents programmatically:

```typescript
for await (const message of query({
  prompt: "Review this PR",
  options: {
    agents: {
      "code-reviewer": {
        description: "Reviews code for quality and best practices",
        tools: ["Read", "Grep", "Glob"],
        prompt: "You are a code reviewer. Analyze code for bugs, security issues, and style.",
        model: "opus" 
      },
      "test-writer": {
        description: "Writes unit tests for code",
        tools: ["Read", "Write", "Edit", "Bash"],
        prompt: "You write comprehensive unit tests.",
        model: "opus"
      }
    }
  }
})) {
  // Process messages
}
```

---

## Available Models

```typescript
options: {
  model: "claude-opus-4-5-20251101"    // Most capable
  // or
  model: "claude-sonnet-4-5-20250929"  // Balanced
  // or
  model: "claude-haiku-4-5-20251001"   // Fastest
}
```

---

## Resources

- [TypeScript SDK Reference](https://platform.claude.com/docs/en/agent-sdk/typescript)
- [Todo Tracking](https://platform.claude.com/docs/en/agent-sdk/todo-tracking)
- [Custom Tools](https://platform.claude.com/docs/en/agent-sdk/custom-tools)
- [SDK Demos](https://github.com/anthropics/claude-agent-sdk-demos)
