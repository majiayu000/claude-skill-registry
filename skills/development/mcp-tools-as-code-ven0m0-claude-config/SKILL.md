---
name: mcp-tools-as-code
description: Convert MCP servers to typed TypeScript APIs for efficient code execution. Reduces token usage by 98%+ by transforming tool calls into programmatic access. Use when building agents that need to interact with multiple MCP servers efficiently, when context window is a concern, or when native control flow (loops, conditionals) would simplify multi-step workflows.
---

# MCP Tools as Code

Transform MCP servers from discrete tool invocations into typed TypeScript APIs that agents interact with programmatically. This approach dramatically reduces token usage and enables native control flow.

## The Problem

Traditional MCP tool usage has two inefficiencies:

1. **Context Overload**: Tool definitions occupy significant context window space. Agents connected to many servers process thousands of tokens before reading requests.

2. **Intermediate Result Duplication**: Data retrieved through tool calls traverses the model multiple times. A meeting transcript fetched, summarized, and stored means processing the transcript tokens repeatedly.

## The Solution

Present MCP servers as filesystem-organized code APIs. Agents discover, load, and use tools via native TypeScript instead of discrete tool calls.

**Before** (150,000+ tokens for a simple workflow):
```
1. Tool call: gdrive.getDocument → Model processes result
2. Tool call: summarize → Model processes result
3. Tool call: salesforce.updateRecord → Model processes result
```

**After** (2,000 tokens):
```typescript
const transcript = (await gdrive.getDocument({ documentId: 'abc123' })).content;
const summary = extractKeyPoints(transcript);
await salesforce.updateRecord({
  objectType: 'SalesMeeting',
  recordId: '00Q5f000001abcXYZ',
  data: { Notes: summary }
});
```

## Architecture

### Directory Structure

```
servers/
├── {server-name}/
│   ├── index.ts          # Re-exports all tools
│   ├── types.ts          # Shared types and interfaces
│   ├── {tool-name}.ts    # Individual tool modules
│   └── README.md         # Server documentation
└── index.ts              # Server discovery/registry
```

### Tool Module Pattern

Each MCP tool becomes a typed TypeScript module:

```typescript
// servers/google-drive/getDocument.ts
import type { DocumentResult } from './types';

export interface GetDocumentInput {
  /** Google Drive document ID */
  documentId: string;
  /** Format to retrieve (default: 'text') */
  format?: 'text' | 'html' | 'markdown';
}

export interface GetDocumentOutput {
  content: string;
  title: string;
  lastModified: string;
  mimeType: string;
}

/**
 * Retrieves a document from Google Drive by ID.
 *
 * @example
 * const doc = await getDocument({ documentId: 'abc123' });
 * console.log(doc.content);
 */
export async function getDocument(input: GetDocumentInput): Promise<GetDocumentOutput> {
  // Implementation calls underlying MCP transport
  return await mcpCall('google-drive', 'getDocument', input);
}
```

### Server Index Pattern

```typescript
// servers/google-drive/index.ts
export { getDocument } from './getDocument';
export { listFiles } from './listFiles';
export { createDocument } from './createDocument';
export { updateDocument } from './updateDocument';

export * from './types';
```

### Root Discovery

```typescript
// servers/index.ts
export * as gdrive from './google-drive';
export * as salesforce from './salesforce';
export * as slack from './slack';
export * as notion from './notion';
```

## Converting MCP Servers

### Step 1: Analyze Server Tools

List available tools from the MCP server:

```typescript
const tools = await mcpClient.listTools();
// Extract: name, description, inputSchema, outputSchema
```

### Step 2: Generate Type Definitions

Convert JSON schemas to TypeScript interfaces:

```typescript
// From JSON Schema
{
  "type": "object",
  "properties": {
    "query": { "type": "string", "description": "Search query" },
    "limit": { "type": "number", "default": 10 }
  },
  "required": ["query"]
}

// To TypeScript
export interface SearchInput {
  /** Search query */
  query: string;
  /** Maximum results (default: 10) */
  limit?: number;
}
```

### Step 3: Create Tool Modules

For each tool, create a module with:

1. Input interface with JSDoc descriptions
2. Output interface
3. Async function wrapping MCP call
4. Usage examples in JSDoc

### Step 4: Generate Index Files

Export all tools from server index, then all servers from root index.

## Benefits

### Progressive Disclosure

Agents navigate the filesystem naturally, loading only needed definitions:

```typescript
// Agent discovers available servers
const servers = await glob('servers/*/index.ts');

// Agent loads specific server when needed
const gdrive = await import('./servers/google-drive');

// Agent uses specific tool
const doc = await gdrive.getDocument({ documentId: 'abc123' });
```

### Data Filtering

Large datasets filter client-side before model exposure:

```typescript
// Fetch 10,000 rows
const allRows = await sheets.getRows({ spreadsheetId: 'xyz' });

// Filter to relevant subset (never exposed to model)
const relevantRows = allRows.filter(row => row.status === 'active');

// Only log/return filtered results
console.log(`Found ${relevantRows.length} active records`);
```

### Native Control Flow

Replace sequential tool calls with native programming:

```typescript
// Process multiple items efficiently
for (const item of items) {
  const data = await source.getData({ id: item.id });

  if (data.needsUpdate) {
    await target.updateRecord({
      id: item.targetId,
      data: transform(data)
    });
  }
}
```

### Error Handling

Native try/catch instead of tool call error parsing:

```typescript
try {
  const result = await api.riskyOperation({ id });
  return { success: true, result };
} catch (error) {
  if (error.code === 'NOT_FOUND') {
    return { success: false, reason: 'Record not found' };
  }
  throw error;
}
```

### State Persistence

Maintain workspace files across executions:

```typescript
// Save reusable functions to skills directory
await fs.writeFile('./skills/summarize.ts', summarizeFunction);

// Load in future executions
const { summarize } = await import('./skills/summarize');
```

## MCP Transport Layer

The typed wrappers call through a transport abstraction:

```typescript
// lib/mcp-transport.ts
import { Client } from '@modelcontextprotocol/sdk/client/index.js';

const clients = new Map<string, Client>();

export async function mcpCall<T>(
  serverName: string,
  toolName: string,
  input: unknown
): Promise<T> {
  const client = await getOrCreateClient(serverName);

  const result = await client.callTool({
    name: toolName,
    arguments: input
  });

  if (result.isError) {
    throw new MCPError(result.content);
  }

  return parseResult<T>(result.content);
}

async function getOrCreateClient(serverName: string): Promise<Client> {
  if (!clients.has(serverName)) {
    const client = await initializeClient(serverName);
    clients.set(serverName, client);
  }
  return clients.get(serverName)!;
}
```

## Code Generation Template

Use this template to generate tool modules:

```typescript
// Template for generating tool modules
function generateToolModule(tool: MCPTool): string {
  const inputInterface = schemaToInterface(tool.inputSchema, `${tool.name}Input`);
  const outputInterface = schemaToInterface(tool.outputSchema, `${tool.name}Output`);

  return `
import { mcpCall } from '../../lib/mcp-transport';

${inputInterface}

${outputInterface}

/**
 * ${tool.description}
 *
 * @example
 * const result = await ${tool.name}(input);
 */
export async function ${tool.name}(input: ${tool.name}Input): Promise<${tool.name}Output> {
  return await mcpCall('${tool.serverName}', '${tool.name}', input);
}
`;
}
```

## Security Considerations

### Sandboxing

Code execution requires secure sandboxing:

- Resource limits (CPU, memory, network)
- Filesystem isolation
- Network egress controls
- Timeout enforcement

### Input Validation

Validate at the typed wrapper layer:

```typescript
export async function updateRecord(input: UpdateRecordInput): Promise<void> {
  // Validate before MCP call
  if (!input.recordId.match(/^[A-Za-z0-9]+$/)) {
    throw new ValidationError('Invalid record ID format');
  }

  await mcpCall('salesforce', 'updateRecord', input);
}
```

### PII Handling

Intermediate results stay in execution environment:

```typescript
// PII never leaves sandbox by default
const userData = await crm.getUser({ id: userId });

// Only sanitized summary returned to model
return {
  summary: `User ${userData.firstName} has ${userData.orderCount} orders`,
  // Raw PII stays in sandbox
};
```

## When to Use This Pattern

**Good fit:**

- Multi-step workflows with intermediate data
- High-volume data processing
- Complex control flow (loops, conditionals, error handling)
- Agents connecting to many MCP servers
- Cost-sensitive applications

**Traditional MCP better for:**

- Simple, single-tool interactions
- When tool definitions fit easily in context
- Quick prototyping without code generation
- When sandboxed execution isn't available

## Conversion Checklist

- [ ] List all tools from target MCP server
- [ ] Generate TypeScript interfaces from JSON schemas
- [ ] Create individual tool modules with types and JSDoc
- [ ] Create server index re-exporting all tools
- [ ] Add server to root index
- [ ] Implement MCP transport layer if not exists
- [ ] Add usage examples to each tool's JSDoc
- [ ] Test type safety with TypeScript compiler
- [ ] Document any server-specific quirks

## Resources

- [Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) - Original Anthropic engineering blog post
- [MCP TypeScript SDK](https://github.com/modelcontextprotocol/typescript-sdk)
- [json-schema-to-typescript](https://github.com/bcherny/json-schema-to-typescript) - Schema conversion utility

## Related Skills

- **mcp-development**: Building MCP servers with fastmcp
- **typescript-expert**: TypeScript patterns and best practices
- **api-design**: Interface design and documentation
