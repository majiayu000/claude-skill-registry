---
name: claude-agent-ts-sdk
description: Build Claude agents using TypeScript with the @anthropic-ai/claude-agent-sdk. Use this skill when implementing conversational agents, building tools for agents, setting up streaming responses, or debugging agent implementations. Covers the tool wrapping pattern, SDK initialization, agent architecture, and best practices.
license: MIT
category: development-tools
---

# Claude Agent TypeScript SDK

## Overview

Build production-ready Claude agents using TypeScript and the `@anthropic-ai/claude-agent-sdk`. This skill provides battle-tested patterns from successful implementations, focusing on the tool wrapping approach (not full MCP servers) for creating modular, composable agent tools.

## When to Use This Skill

Use this skill when:
- Implementing a new Claude agent in TypeScript
- Creating tools for agent use
- Setting up streaming agent responses
- Debugging agent SDK implementations
- Converting between MCP server and tool wrapping approaches
- Building CLI agents, web server agents, or plugin-based agents
- Working with subprocess tools, file system tools, or API wrappers

## Authentication

The SDK automatically uses Claude Code's authentication - no setup required. Your agent works seamlessly within Claude Code without any authentication configuration.

## Core Architecture Patterns

### Pattern 1: CLI/Specialized Agent

**Best for:** Command-line tools, specialized workflows, batch processing

```typescript
// src/agent.ts
import { query, createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';
import { myTools } from './tools/index.js';

const SYSTEM_PROMPT = `You are a specialized agent that...
[Detailed instructions about capabilities and tools]`;

export async function runAgent(userPrompt: string) {
  // Create MCP server at query time (not module level)
  const server = createSdkMcpServer({
    name: 'my-agent',
    version: '1.0.0',
    tools: myTools,
  });

  // Query with streaming
  const messages = query({
    prompt: userPrompt,
    options: {
      systemPrompt: SYSTEM_PROMPT,
      permissionMode: 'bypassPermissions',
      mcpServers: {
        'my-agent': server,
      },
    },
  });

  // Process stream
  for await (const event of messages) {
    if (event.type === 'assistant') {
      for (const content of event.message.content) {
        if (content.type === 'text') {
          process.stdout.write(content.text);
        }
      }
    }
  }
}
```

### Pattern 2: Web Server Agent with SSE

**Best for:** Web applications, API servers, real-time UIs

```typescript
// src/routes/agent.ts
import { query, createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';

app.post('/agent/stream', async (req, res) => {
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  const server = createSdkMcpServer({
    name: 'web-agent',
    version: '1.0.0',
    tools: createContextualTools(req.session),
  });

  const messages = query({
    prompt: req.body.prompt,
    options: {
      systemPrompt: SYSTEM_PROMPT,
      mcpServers: { 'web-agent': server },
    },
  });

  for await (const event of messages) {
    res.write(`data: ${JSON.stringify(event)}\n\n`);
  }

  res.end();
});
```

### Pattern 3: Plugin/Framework Agent

**Best for:** Extensible systems, plugin architectures, reusable frameworks

```typescript
// src/engine.ts
export class AgentEngine {
  constructor(private plugin: Plugin) {}

  async stream(prompt: string): Promise<void> {
    const mcpServers: Record<string, any> = {};

    if (this.plugin.tools.length > 0) {
      const serverName = `${this.plugin.name}-tools`;
      mcpServers[serverName] = createSdkMcpServer({
        name: serverName,
        version: this.plugin.version ?? '1.0.0',
        tools: this.plugin.tools,
      });
    }

    const messages = query({
      prompt,
      options: {
        systemPrompt: this.plugin.systemPrompt,
        permissionMode: 'bypassPermissions',
        allowedTools: this.plugin.allowedTools,
        mcpServers,
      },
    });

    for await (const event of messages) {
      await this.plugin.handleEvent(event);
    }
  }
}
```

### Pattern 4: Monorepo Full-Stack Application

**Best for:** Full-stack apps with frontend + backend, complex web applications

Site Studio is an example of this pattern using npm workspaces.

**Project Structure:**
```
my-app/
├── package.json           # Root workspace config
├── packages/
│   ├── backend/
│   │   ├── package.json
│   │   ├── src/
│   │   │   ├── index.ts   # Express server
│   │   │   ├── agent.ts   # Agent logic
│   │   │   └── tools/     # Tool definitions
│   │   └── dist/          # Build output
│   └── frontend/
│       ├── package.json
│       ├── src/
│       └── dist/
```

**Root package.json:**
```json
{
  "name": "my-app",
  "private": true,
  "workspaces": ["packages/*"],
  "scripts": {
    "dev": "concurrently \"npm run dev:backend\" \"npm run dev:frontend\"",
    "dev:backend": "npm run dev --workspace=packages/backend",
    "dev:frontend": "npm run dev --workspace=packages/frontend",
    "build": "npm run build --workspace=packages/backend && npm run build --workspace=packages/frontend"
  },
  "devDependencies": {
    "concurrently": "^9.1.2"
  }
}
```

**Backend package.json:**
```json
{
  "name": "@my-app/backend",
  "type": "module",
  "scripts": {
    "dev": "tsc && node dist/index.js",
    "build": "tsc"
  },
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.1.14",
    "express": "^4.21.2",
    "zod": "^3.24.1"
  }
}
```

**Backend agent.ts:**
```typescript
import { query, createSdkMcpServer } from '@anthropic-ai/claude-agent-sdk';
import { createFileTools } from './tools/file-tools.js';

export async function runAgent(
  prompt: string,
  projectPath: string,
  sessionId?: string
): Promise<AsyncIterable<any>> {
  const tools = createFileTools(projectPath);

  const server = createSdkMcpServer({
    name: 'my-app',
    version: '1.0.0',
    tools,
  });

  const queryOptions: any = {
    permissionMode: 'bypassPermissions',  // Required for standalone servers!
    systemPrompt: SYSTEM_PROMPT,
    mcpServers: { 'my-app': server },
  };

  if (sessionId) {
    queryOptions.resume = sessionId;
  }

  return query({ prompt, options: queryOptions });
}
```

**Backend index.ts (Express):**
```typescript
import express from 'express';
import { runAgent } from './agent.js';

const app = express();
app.use(express.json());

app.post('/api/query', async (req, res) => {
  const { prompt, projectId, sessionId } = req.body;
  const projectPath = path.join(PROJECTS_DIR, projectId);

  // Set up SSE
  res.setHeader('Content-Type', 'text/event-stream');
  res.setHeader('Cache-Control', 'no-cache');
  res.setHeader('Connection', 'keep-alive');

  try {
    const stream = await runAgent(prompt, projectPath, sessionId);

    for await (const event of stream) {
      res.write(`data: ${JSON.stringify(event)}\n\n`);
    }

    res.write('data: [DONE]\n\n');
    res.end();
  } catch (error: any) {
    res.write(`data: ${JSON.stringify({ error: error.message })}\n\n`);
    res.end();
  }
});

app.listen(3001, () => {
  console.log('Backend running on http://localhost:3001');
});
```

**Benefits of Monorepo Pattern:**
- Share TypeScript configurations
- Single `npm install` for all dependencies
- Coordinated development with `concurrently`
- Type safety across packages
- Unified build and deploy processes

## Tool Wrapping Pattern (Preferred)

**Philosophy:** Create portable, composable tools as modules. Only wrap in MCP servers when needed for query execution.

### Basic Tool Definition

```typescript
// src/tools/my-tool.ts
import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

export const myTool = tool(
  'my_tool_name',
  'Clear description of what this tool does',
  z.object({
    param1: z.string().describe('What param1 is for'),
    param2: z.number().optional().describe('Optional parameter'),
  }).shape,
  async (params) => {
    // Implementation
    const result = await doSomething(params.param1, params.param2);

    return {
      content: [{
        type: 'text',
        text: JSON.stringify(result, null, 2),
      }],
    };
  }
);
```

### Tool Composition Pattern

```typescript
// src/tools/index.ts
import { fileTools } from './file-tools.js';
import { apiTools } from './api-tools.js';
import { searchTool } from './search-tool.js';

// Export individual tools for selective use
export { fileTools, apiTools, searchTool };

// Export combined array for convenience
export const allTools = [
  ...fileTools,
  ...apiTools,
  searchTool,
];
```

### Tool Factories (Context-Aware Tools)

```typescript
// src/tools/file-tools.ts
import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

export function createFileTools(projectPath: string) {
  const readFile = tool(
    'read_file',
    'Read a file from the project',
    z.object({
      path: z.string().describe('Relative path from project root'),
    }).shape,
    async ({ path }) => {
      const fullPath = join(projectPath, path);
      const content = await fs.readFile(fullPath, 'utf-8');
      return {
        content: [{ type: 'text', text: content }],
      };
    }
  );

  const writeFile = tool(
    'write_file',
    'Write content to a file',
    z.object({
      path: z.string().describe('Relative path from project root'),
      content: z.string().describe('File content'),
    }).shape,
    async ({ path, content }) => {
      const fullPath = join(projectPath, path);
      await fs.writeFile(fullPath, content, 'utf-8');
      return {
        content: [{ type: 'text', text: `Wrote to ${path}` }],
      };
    }
  );

  return [readFile, writeFile];
}

// Usage in agent:
const tools = createFileTools('/path/to/project');
const server = createSdkMcpServer({ name: 'files', version: '1.0.0', tools });
```

### Subprocess Wrapper Tools

```typescript
// src/tools/python-tools.ts
import { tool } from '@anthropic-ai/claude-agent-sdk';
import { spawn } from 'child_process';
import { z } from 'zod';

export const runPythonScript = tool(
  'run_python_analysis',
  'Run Python data analysis script',
  z.object({
    query: z.string().describe('Search query for analysis'),
    limit: z.number().optional().describe('Max results'),
  }).shape,
  async ({ query, limit = 10 }) => {
    return new Promise((resolve, reject) => {
      const pythonProcess = spawn('python3', [
        'scripts/analyze.py',
        '--query', query,
        '--limit', String(limit),
      ]);

      let stdout = '';
      let stderr = '';

      pythonProcess.stdout.on('data', (data) => {
        stdout += data.toString();
      });

      pythonProcess.stderr.on('data', (data) => {
        stderr += data.toString();
      });

      pythonProcess.on('close', (code) => {
        if (code !== 0) {
          reject(new Error(`Python script failed: ${stderr}`));
          return;
        }

        try {
          const result = JSON.parse(stdout);
          resolve({
            content: [{
              type: 'text',
              text: JSON.stringify(result, null, 2),
            }],
          });
        } catch (e) {
          reject(new Error(`Failed to parse output: ${stdout}`));
        }
      });
    });
  }
);
```

### Dynamic Tool Creation

```typescript
// src/tools/dynamic-tools.ts
import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';

export function createDynamicTools(config: ToolConfig[]) {
  return config.map((toolConfig) => {
    // Build Zod schema from config
    const schemaShape: Record<string, z.ZodType> = {};
    for (const param of toolConfig.parameters) {
      let zodType: z.ZodType = z.string();

      if (param.type === 'number') zodType = z.number();
      if (param.type === 'boolean') zodType = z.boolean();
      if (param.optional) zodType = zodType.optional();

      zodType = zodType.describe(param.description);
      schemaShape[param.name] = zodType;
    }

    return tool(
      toolConfig.name,
      toolConfig.description,
      z.object(schemaShape).shape,
      async (params) => {
        // Execute configured command
        const result = await executeCommand(toolConfig.command, params);
        return {
          content: [{ type: 'text', text: JSON.stringify(result) }],
        };
      }
    );
  });
}
```

## Project Setup Checklist

### 1. Package Configuration

```json
// package.json
{
  "name": "my-agent",
  "version": "1.0.0",
  "type": "module",
  "engines": {
    "node": ">=18.0.0"
  },
  "scripts": {
    "build": "tsc",
    "start": "node dist/index.js",
    "dev": "tsx watch src/index.ts",
    "typecheck": "tsc --noEmit"
  },
  "dependencies": {
    "@anthropic-ai/claude-agent-sdk": "^0.1.14",
    "zod": "^3.23.8"
  },
  "devDependencies": {
    "@types/node": "^20.11.0",
    "tsx": "^4.7.0",
    "typescript": "^5.3.3"
  }
}
```

### 2. TypeScript Configuration

```json
// tsconfig.json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "lib": ["ES2022"],
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 3. Environment Setup

```bash
# .env.example (optional - for your own environment variables)
NODE_ENV=development
```

```typescript
// .gitignore
node_modules/
dist/
.env
*.log
.DS_Store
```

### 4. Directory Structure

```
my-agent/
├── src/
│   ├── index.ts              # Entry point
│   ├── agent.ts              # Agent implementation
│   ├── tools/
│   │   ├── index.ts          # Tool exports
│   │   ├── file-tools.ts     # File operations
│   │   └── api-tools.ts      # API calls
│   ├── prompts/
│   │   └── system.ts         # System prompts
│   └── types/
│       └── index.ts          # Type definitions
├── scripts/                   # Python/shell scripts called by tools
├── package.json
├── tsconfig.json
├── .env
└── .env.example
```

## System Prompts

### Structure

System prompts should be 100-170+ lines with:
1. Role and capabilities
2. Detailed tool descriptions and when to use them
3. Workflow instructions
4. Output formatting requirements
5. Error handling guidelines

```typescript
// src/prompts/system.ts
export const SYSTEM_PROMPT = `You are a specialized agent with the following capabilities:

## Role
[Clear description of the agent's purpose and responsibilities]

## Available Tools

### tool_name_1
**Purpose:** [What it does]
**When to use:** [Specific scenarios]
**Parameters:**
- param1: [Description]
- param2: [Description]
**Example usage:** [Concrete example]

### tool_name_2
[Same structure...]

## Workflow

1. First, [initial step with tool usage]
2. Then, [subsequent steps]
3. Finally, [completion steps]

## Output Format

Always structure your responses as:
- [Format specification]
- [Examples]

## Error Handling

If a tool fails:
- [Recovery strategies]
- [Alternative approaches]

## Important Notes

- [Critical constraints]
- [Edge cases to handle]
`;
```

## Streaming and Event Handling

### Tool Execution Event Flow

When tools are executed, events follow this specific pattern that mirrors the Anthropic Messages API:

**1. `assistant` event with `tool_use` block:**

Claude requests to use a tool. The event contains:

```typescript
{
  type: 'assistant',
  message: {
    role: 'assistant',
    content: [{
      type: 'tool_use',
      id: 'toolu_01AvhNWuX3aeWaaouT5t6D73',  // Unique ID for this tool call
      name: 'mcp__server__tool_name',
      input: { param1: 'value' }
    }]
  }
}
```

**2. `user` event with `tool_result` block:**

The system/environment provides the tool result. **Note: This is a `user` event, not an `assistant` event!**

```typescript
{
  type: 'user',
  message: {
    role: 'user',
    content: [{
      type: 'tool_result',
      tool_use_id: 'toolu_01AvhNWuX3aeWaaouT5t6D73',  // References the tool_use.id
      content: [
        { type: 'text', text: '{"result": "data"}' }
      ],
      is_error: false
    }]
  }
}
```

**3. `assistant` event with text response:**

Claude processes the result and responds to the user.

```typescript
{
  type: 'assistant',
  message: {
    role: 'assistant',
    content: [{
      type: 'text',
      text: 'Based on the results...'
    }]
  }
}
```

**Key Points:**
- **Tool results come in `user` events**, not `assistant` events
- Match results using `tool_result.tool_use_id` ↔ `tool_use.id`
- Tool output is in the `content` array (usually `content[0].text`)
- This structure mirrors how you'd interact with the Anthropic API directly
- From Claude's perspective: it requests a tool (`assistant`), the world responds (`user`), then it continues (`assistant`)

**Example: Tracking Tool Execution**

```typescript
const toolExecutions = new Map();

for await (const event of messages) {
  if (event.type === 'assistant' && event.message?.content) {
    for (const block of event.message.content) {
      if (block.type === 'tool_use') {
        // Store tool execution with its ID
        toolExecutions.set(block.id, {
          name: block.name,
          input: block.input,
          status: 'running'
        });
      }
    }
  }

  if (event.type === 'user' && event.message?.content) {
    for (const block of event.message.content) {
      if (block.type === 'tool_result') {
        // Match result with the tool call
        const tool = toolExecutions.get(block.tool_use_id);
        if (tool) {
          tool.status = block.is_error ? 'error' : 'success';
          tool.output = block.content.map(c => c.text).join('\n');
        }
      }
    }
  }
}
```

### Pattern 1: Simple Text Streaming

```typescript
for await (const event of messages) {
  if (event.type === 'assistant') {
    for (const content of event.message.content) {
      if (content.type === 'text') {
        process.stdout.write(content.text);
      }
    }
  }
}
```

### Pattern 2: Structured Event Processing

```typescript
for await (const event of messages) {
  switch (event.type) {
    case 'assistant':
      // Handle assistant messages (including tool_use blocks)
      for (const block of event.message.content) {
        if (block.type === 'text') {
          await handleTextContent(block.text);
        } else if (block.type === 'tool_use') {
          await handleToolUse(block);
        }
      }
      break;

    case 'user':
      // Handle tool results
      for (const block of event.message.content) {
        if (block.type === 'tool_result') {
          await handleToolResult(block);
        }
      }
      break;

    case 'error':
      await handleError(event.error);
      break;
  }
}
```

### Pattern 3: Web SSE Streaming

```typescript
for await (const event of messages) {
  res.write(`data: ${JSON.stringify(event)}\n\n`);

  if (event.type === 'assistant') {
    // Optionally send custom events
    res.write(`event: message\ndata: ${JSON.stringify({
      role: 'assistant',
      content: event.message.content
    })}\n\n`);
  }
}
```

### Pattern 4: Web UI with Separate Text Sections (CRITICAL)

**Problem:** When building web UIs that display conversation with interleaved text and tools, a common mistake is accumulating ALL text into one string. This causes text from different conversation sections to merge incorrectly.

**❌ WRONG - Text accumulates forever:**
```typescript
let fullTextResponse = '';  // DON'T DO THIS

for await (const event of messages) {
  if (event.type === 'assistant' && event.message?.content) {
    for (const block of event.message.content) {
      if (block.type === 'text') {
        fullTextResponse += block.text;  // ❌ Never resets!
        // Display fullTextResponse
      }
    }
  }
}
```

This creates: `"Text1 Text2 Text3"` all merged together, even when tools appear between them.

**✅ CORRECT - Section-based text management:**
```typescript
let currentSectionText = '';  // Resets after each tool group
let contentBlocks = [];  // Structured: [text, tools, text, tools, text]
let processedToolIds = new Set();

for await (const event of messages) {
  if (event.type === 'assistant' && event.message?.content) {
    for (const block of event.message.content) {
      if (block.type === 'text') {
        // Accumulate text for CURRENT section only
        currentSectionText += block.text;

        // Update or create text block for this section
        let textBlockIndex = contentBlocks.findIndex((b, i) => {
          if (b.type === 'text') {
            // Find last text block (no tools after it)
            const hasToolsAfter = contentBlocks.slice(i + 1).some(cb => cb.type === 'tools');
            return !hasToolsAfter;
          }
          return false;
        });

        if (textBlockIndex >= 0) {
          contentBlocks[textBlockIndex].text = currentSectionText;
        } else {
          contentBlocks.push({ type: 'text', text: currentSectionText });
        }

      } else if (block.type === 'tool_use') {
        // Only process if not duplicate
        if (!processedToolIds.has(block.id)) {
          processedToolIds.add(block.id);

          // Finalize current text section
          if (currentSectionText.trim()) {
            const lastBlock = contentBlocks[contentBlocks.length - 1];
            if (lastBlock?.type === 'text') {
              lastBlock.text = currentSectionText;
            }
          }

          // RESET for next section - this is the key!
          currentSectionText = '';

          // Add tool to tools block
          // (implementation depends on your UI structure)
        }
      }
    }
  }
}
```

**Result:** Properly separated structure:
```javascript
contentBlocks = [
  { type: 'text', text: 'I will scaffold your site...' },
  { type: 'tools', tools: [scaffoldTool] },
  { type: 'text', text: 'Now I will read the files...' },
  { type: 'tools', tools: [readTool1, readTool2] },
  { type: 'text', text: 'I have updated your files...' }
]
```

**Key Principles:**
1. **Reset `currentSectionText` after tools** - Don't accumulate across tool boundaries
2. **Deduplicate tools** - Use a Set to track processed tool IDs
3. **Separate text and tool blocks** - Create structured sections, not one giant text blob
4. **Update the current text block** - Don't create a new text block on every streaming chunk

**Reference:** See `/home/zweb/apps/obsidian-agent-plugin/src/main.ts` lines 915-1010 for a working implementation of this pattern.

## Error Handling

### Tool Error Handling

```typescript
export const myTool = tool(
  'my_tool',
  'Description',
  schema,
  async (params) => {
    try {
      const result = await riskyOperation(params);
      return {
        content: [{ type: 'text', text: JSON.stringify(result) }],
      };
    } catch (error) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({
            error: true,
            message: error.message,
            suggestion: 'Try adjusting parameters or check prerequisites',
          }),
        }],
        isError: true,
      };
    }
  }
);
```

### Stream Error Handling

```typescript
try {
  for await (const event of messages) {
    // Process events
  }
} catch (error) {
  if (error.name === 'AbortError') {
    console.log('Stream aborted by user');
  } else if (error.status === 429) {
    console.error('Rate limit exceeded. Please wait and retry.');
  } else {
    console.error('Agent error:', error.message);
  }
}
```

## Best Practices

### DO

✅ **Export tools as both individual exports and arrays**
```typescript
export const tool1 = tool(...);
export const tool2 = tool(...);
export const myTools = [tool1, tool2];
```

✅ **Use Zod schemas with detailed descriptions**
```typescript
z.object({
  query: z.string().describe('The search query to execute'),
  limit: z.number().optional().describe('Maximum number of results (default: 10)'),
})
```

✅ **Create MCP servers at query time, not module level**
```typescript
// GOOD: In function scope
async function runAgent() {
  const server = createSdkMcpServer({ tools });
  const messages = query({ options: { mcpServers: { 'name': server } } });
}
```

✅ **Use closures for context-aware tools**
```typescript
export function createTools(context: Context) {
  return [
    tool('name', 'desc', schema, async (params) => {
      // Has access to context via closure
      return processWithContext(context, params);
    })
  ];
}
```

✅ **Include detailed system prompts (100+ lines)**

✅ **Set `type: "module"` in package.json**

✅ **Authentication handled automatically by Claude Code**

### DON'T

❌ **Don't create full MCP servers for simple tools**
```typescript
// AVOID: Creating MCP server infrastructure
const server = new MCPServer(...);
server.registerTool(...);
// Use tool() wrapper instead
```

❌ **Don't use global state in tools**
```typescript
// BAD
let globalContext;
export const tool = tool('name', 'desc', schema, async () => {
  return useGlobalContext(globalContext); // Brittle!
});
```

❌ **Don't mix module types**
```typescript
// package.json should have "type": "module"
// Don't mix require() and import
```

❌ **Don't skip Zod validation**
```typescript
// BAD: No schema validation
tool('name', 'desc', {}, async (params: any) => { ... });
```

### Permission Modes

**CRITICAL: Standalone servers must use `bypassPermissions`**

When building standalone applications (Express servers, CLI tools), always use `'bypassPermissions'`:

```typescript
// ✅ CORRECT for standalone servers
const messages = query({
  prompt,
  options: {
    permissionMode: 'bypassPermissions',  // Always use this!
    systemPrompt,
    mcpServers,
  },
});
```

**Why?** The `'interactive'` mode requires Claude Code to be running to show permission prompts. Standalone servers run independently and cannot display interactive prompts, leading to "Claude Code process exited with code 1" errors.

```typescript
// ❌ WRONG for standalone servers
permissionMode: mode === 'execute' ? 'bypassPermissions' : 'interactive',
// This will crash when mode is 'plan'!
```

**When to use each mode:**
- `'bypassPermissions'` - Standalone servers, CLI tools, background agents
- `'interactive'` - Only when running inside Claude Code with UI for approvals
- `'allowedTools'` - When you want to restrict tool access programmatically

## Common Patterns

### CSV Processing Agent

```typescript
import { tool } from '@anthropic-ai/claude-agent-sdk';
import { z } from 'zod';
import { parse } from 'csv-parse/sync';
import { stringify } from 'csv-stringify/sync';

export const readCsv = tool(
  'read_csv',
  'Read and parse CSV file',
  z.object({
    path: z.string(),
  }).shape,
  async ({ path }) => {
    const content = await fs.readFile(path, 'utf-8');
    const records = parse(content, { columns: true });
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(records, null, 2),
      }],
    };
  }
);

export const writeCsv = tool(
  'write_csv',
  'Write data to CSV file',
  z.object({
    path: z.string(),
    data: z.array(z.record(z.any())),
  }).shape,
  async ({ path, data }) => {
    const csv = stringify(data, { header: true });
    await fs.writeFile(path, csv, 'utf-8');
    return {
      content: [{
        type: 'text',
        text: `Wrote ${data.length} records to ${path}`,
      }],
    };
  }
);
```

### API Integration Tools

```typescript
export const searchApi = tool(
  'search_api',
  'Search external API',
  z.object({
    query: z.string(),
    filters: z.record(z.string()).optional(),
  }).shape,
  async ({ query, filters }) => {
    const params = new URLSearchParams({ q: query, ...filters });
    const response = await fetch(`https://api.example.com/search?${params}`);

    if (!response.ok) {
      return {
        content: [{
          type: 'text',
          text: JSON.stringify({ error: `API error: ${response.statusText}` }),
        }],
        isError: true,
      };
    }

    const data = await response.json();
    return {
      content: [{
        type: 'text',
        text: JSON.stringify(data, null, 2),
      }],
    };
  }
);
```

## Debugging Tips

### 1. Enable Verbose Logging

```typescript
const messages = query({
  prompt,
  options: {
    systemPrompt,
    mcpServers,
    // Add debugging
    onToolCall: (toolName, params) => {
      console.log(`[TOOL CALL] ${toolName}`, params);
    },
    onToolResult: (toolName, result) => {
      console.log(`[TOOL RESULT] ${toolName}`, result);
    },
  },
});
```

### 2. Validate Tool Definitions

```typescript
// Add validation helper
function validateTools(tools: any[]) {
  for (const t of tools) {
    if (!t.name) console.error('Tool missing name:', t);
    if (!t.description) console.error('Tool missing description:', t);
    if (!t.inputSchema) console.error('Tool missing schema:', t);
  }
}
```

### 3. Test Tools Independently

```typescript
// Test tools before using in agent
async function testTool() {
  const result = await myTool.execute({ param1: 'test' });
  console.log('Tool result:', result);
}
```

## Resources

This skill references the following bundled resources:

### references/
- `api-reference.md` - Official SDK API documentation
- `working-examples.md` - Complete examples from production implementations
- `troubleshooting.md` - Common issues and solutions

### assets/
- `project-template/` - Starter template for new agent projects
- `tsconfig-template.json` - Recommended TypeScript configuration
