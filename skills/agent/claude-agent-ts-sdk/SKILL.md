---
name: claude-agent-ts-sdk
description: Build Claude agents using TypeScript with the @anthropic-ai/claude-agent-sdk. Use this skill when implementing conversational agents, building tools for agents, setting up streaming responses, or debugging agent implementations. Covers the tool wrapping pattern, SDK initialization, agent architecture, and best practices.
license: MIT
category: development-tools
---

# Claude Agent TypeScript SDK

Build production-ready Claude agents using TypeScript and the `@anthropic-ai/claude-agent-sdk`. This skill provides battle-tested patterns for creating modular, composable agent tools.

## Quick Start

```typescript
import { query, createSdkMcpServer, tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

// 1. Define tools
const greetTool = tool(
  'greet',
  'Greet a user by name',
  z.object({
    name: z.string().describe('User name'),
  }).shape,
  async ({ name }) => ({
    content: [{ type: 'text', text: `Hello, ${name}!` }],
  })
);

// 2. Create MCP server
const server = createSdkMcpServer({
  name: 'my-agent',
  version: '1.0.0',
  tools: [greetTool],
});

// 3. Query with streaming
const messages = query({
  prompt: 'Greet Alice',
  options: {
    systemPrompt: 'You are a helpful agent.',
    permissionMode: 'bypassPermissions',
    mcpServers: { 'my-agent': server },
  },
});

// 4. Process stream
for await (const event of messages) {
  if (event.type === 'assistant') {
    for (const content of event.message.content) {
      if (content.type === 'text') {
        console.log(content.text);
      }
    }
  }
}
```

## When to Use This Skill

Use when:
- **Implementing agents**: Building CLI tools, web servers, or plugins
- **Creating tools**: Defining agent capabilities and integrations
- **Handling streams**: Processing agent responses in real-time
- **Debugging**: Troubleshooting agent implementations
- **Migrating**: Converting from MCP servers to tool wrapping approach

## Core Concepts

### 1. Tools

Tools are the building blocks of agent capabilities. Use the `tool()` function to create them:

```typescript
import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

const myTool = tool(
  'tool_name',           // Name (lowercase, underscores)
  'What it does',        // Clear description
  z.object({            // Zod schema for validation
    param: z.string().describe('Parameter description'),
  }).shape,
  async (params) => {   // Implementation
    return {
      content: [{ type: 'text', text: 'Result' }],
    };
  }
);
```

**Key Points:**
- Use Zod for schema validation
- Descriptions guide Claude's tool selection
- Return format: `{ content: [{ type: 'text', text: string }] }`
- **For advanced patterns, see references/tools.md**

### 2. MCP Servers

Wrap tools in MCP servers for query execution:

```typescript
import { createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';

const server = createSdkMcpServer({
  name: 'server-name',
  version: '1.0.0',
  tools: [tool1, tool2],
});
```

**Important:** Create servers at query time, not module level (enables dynamic tool selection).

### 3. Query and Streaming

Execute agent queries with real-time streaming:

```typescript
import { query } from '@anthropic-ai/claude-agent-sdk';

const messages = query({
  prompt: 'User request here',
  options: {
    systemPrompt: 'Agent role and instructions',
    permissionMode: 'bypassPermissions',  // For standalone servers
    mcpServers: {
      'server-name': server,
    },
  },
});

for await (const event of messages) {
  // Process events: 'assistant', 'user', 'error'
}
```

**For streaming patterns and event handling, see references/streaming.md**

### 4. System Prompts

System prompts define agent behavior (100-170+ lines recommended):

```typescript
const SYSTEM_PROMPT = `You are a specialized agent that...

## Available Tools
[Detailed tool descriptions]

## Workflow
[Step-by-step instructions]

## Output Format
[Expected response structure]
`;
```

**For system prompt best practices, see references/system-prompts.md**

## Architecture Patterns

Choose the pattern that fits your use case:

### Pattern 1: CLI/Specialized Agent
**Best for:** Command-line tools, batch processing

```typescript
export async function runAgent(userPrompt: string) {
  const server = createSdkMcpServer({ name: 'cli-agent', version: '1.0.0', tools });
  const messages = query({ prompt: userPrompt, options: { systemPrompt, permissionMode: 'bypassPermissions', mcpServers: { 'cli-agent': server } } });

  for await (const event of messages) {
    if (event.type === 'assistant') {
      for (const content of event.message.content) {
        if (content.type === 'text') process.stdout.write(content.text);
      }
    }
  }
}
```

### Pattern 2: Web Server Agent
**Best for:** Web applications, APIs, real-time UIs

```typescript
app.post('/agent/stream', async (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  const server = createSdkMcpServer({ name: 'web-agent', version: '1.0.0', tools });
  const messages = query({ prompt: req.body.prompt, options: { systemPrompt, mcpServers: { 'web-agent': server } } });

  for await (const event of messages) {
    res.write(`data: ${JSON.stringify(event)}\n\n`);
  }
  res.end();
});
```

### Pattern 3: Plugin/Framework
**Best for:** Extensible systems, plugin architectures

```typescript
export class AgentEngine {
  async stream(prompt: string) {
    const tools = this.plugin.getTools();
    const server = createSdkMcpServer({ name: this.plugin.name, version: '1.0.0', tools });
    const messages = query({ prompt, options: { systemPrompt: this.plugin.systemPrompt, permissionMode: 'bypassPermissions', mcpServers: { [this.plugin.name]: server } } });

    for await (const event of messages) {
      await this.plugin.handleEvent(event);
    }
  }
}
```

**For complete architecture patterns including monorepo setup, see references/patterns.md**

## Project Setup

### Minimal package.json

```json
{
  "name": "my-agent",
  "type": "module",
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.1.14",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "typescript": "^5.3.3",
    "tsx": "^4.7.0"
  }
}
```

### Directory Structure

```
my-agent/
├── src/
│   ├── index.ts              # Entry point
│   ├── agent.ts              # Agent implementation
│   ├── tools/                # Tool definitions
│   └── prompts/              # System prompts
├── package.json
└── tsconfig.json
```

**For complete project setup including TypeScript config, see references/project-setup.md**

## Common Workflows

### Creating a File Management Agent

1. **Define tools:**
```typescript
const readFile = tool('read_file', 'Read file contents',
  z.object({ path: z.string() }).shape,
  async ({ path }) => ({ content: [{ type: 'text', text: await fs.readFile(path, 'utf-8') }] })
);

const writeFile = tool('write_file', 'Write to file',
  z.object({ path: z.string(), content: z.string() }).shape,
  async ({ path, content }) => { await fs.writeFile(path, content); return { content: [{ type: 'text', text: 'Done' }] }; }
);
```

2. **Create system prompt:**
```typescript
const SYSTEM_PROMPT = `You are a file management agent.

When user asks to edit a file:
1. read_file to see current contents
2. Propose changes
3. write_file to save changes`;
```

3. **Set up agent:**
```typescript
const server = createSdkMcpServer({ name: 'files', version: '1.0.0', tools: [readFile, writeFile] });
const messages = query({ prompt: userRequest, options: { systemPrompt: SYSTEM_PROMPT, permissionMode: 'bypassPermissions', mcpServers: { 'files': server } } });
```

### Adding Context-Aware Tools

Create tool factories that close over session-specific data:

```typescript
function createSessionTools(userId: string) {
  return [
    tool('get_user_data', 'Get user data', {}, async () => {
      const data = await db.getUser(userId);  // Closure over userId
      return { content: [{ type: 'text', text: JSON.stringify(data) }] };
    })
  ];
}

// Per-session tools
app.post('/agent', async (req, res) => {
  const tools = createSessionTools(req.session.userId);
  const server = createSdkMcpServer({ name: 'session', version: '1.0.0', tools });
  // ... rest of agent setup
});
```

## Best Practices

### ✅ DO

- **Use Zod schemas** with detailed descriptions
- **Create servers at query time**, not module level
- **Set `permissionMode: 'bypassPermissions'`** for standalone servers
- **Use tool factories** for context-aware tools
- **Write detailed system prompts** (100+ lines)
- **Handle errors** in tool implementations

### ❌ DON'T

- **Don't skip Zod validation** - schemas help Claude use tools correctly
- **Don't use global state** - use closures instead
- **Don't mix module types** - use `"type": "module"` consistently
- **Don't use `interactive` permission mode** in standalone servers

## Authentication

**No configuration required!** The SDK automatically uses Claude Code's authentication. Your agent works seamlessly within Claude Code without any API key setup.

## Debugging

### Enable Tool Logging

```typescript
const messages = query({
  prompt,
  options: {
    systemPrompt,
    mcpServers,
    onToolCall: (name, params) => console.log(`[CALL] ${name}`, params),
    onToolResult: (name, result) => console.log(`[RESULT] ${name}`, result),
  },
});
```

### Test Tools Independently

```typescript
// Test before integrating
const result = await myTool.execute({ param: 'test' });
console.log('Tool output:', result);
```

### Common Issues

**"Claude Code process exited with code 1"**
- Solution: Use `permissionMode: 'bypassPermissions'` for standalone servers

**Tools not being called**
- Check tool descriptions are clear
- Verify system prompt mentions tools
- Ensure schema validation isn't too restrictive

**Import errors**
- Ensure `"type": "module"` in package.json
- Use `.js` extensions in imports (Node16 resolution)

## Reference Files

This skill includes detailed reference documentation:

- **references/patterns.md** - All 4 architecture patterns with complete examples
- **references/tools.md** - Tool creation, composition, factories, subprocess wrappers
- **references/streaming.md** - Event handling, streaming patterns, UI integration
- **references/system-prompts.md** - How to write effective 100+ line prompts
- **references/project-setup.md** - Complete project configuration, directory structures
- **references/api-reference.md** - Official SDK API documentation
- **references/working-examples.md** - Production implementation examples
- **references/troubleshooting.md** - Common issues and solutions

## Next Steps

1. **Quick prototype:** Use the Quick Start example above
2. **Choose pattern:** Select architecture from references/patterns.md
3. **Set up project:** Follow references/project-setup.md
4. **Create tools:** See references/tools.md for patterns
5. **Write system prompt:** Use references/system-prompts.md template
6. **Handle streaming:** Implement patterns from references/streaming.md
7. **Deploy:** Follow project-setup.md deployment guide

## Resources

- **SDK GitHub:** https://github.com/anthropics/anthropic-sdk-typescript
- **Example Projects:** See assets/project-template/ for starter code
- **Community:** Anthropic Developer Discord
