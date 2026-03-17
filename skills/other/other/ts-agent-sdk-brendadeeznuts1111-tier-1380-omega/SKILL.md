---
name: ts-agent-sdk
description: |
  Generate typed TypeScript SDKs for AI agents to interact with MCP servers. Converts JSON-RPC curl commands to clean function calls. Auto-generates types, client methods, and example scripts from MCP tool definitions.

  Use when building MCP-enabled applications, need typed programmatic access to MCP tools, or creating reusable agent automation scripts.
user-invocable: true
---

# ts-agent-sdk

## Overview

This skill generates typed TypeScript SDKs that allow AI agents (primarily Claude Code) to interact with web applications via MCP servers. It replaces verbose JSON-RPC curl commands with clean function calls.

## Template Location

The core SDK template files are bundled with this skill at:
`templates/`

Copy these files to the target project's `scripts/sdk/` directory as a starting point:

```bash
cp -r ~/.claude/skills/ts-agent-sdk/templates/* ./scripts/sdk/
```

## SDK Generation Workflow

### Step 1: Detect MCP Servers

Scan the project for MCP server modules:
```
src/server/modules/mcp*/server.ts
```

Each server.ts file contains tool definitions using the pattern:
```typescript
server.tool(
  'tool_name',
  'Tool description',
  zodInputSchema,
  async (params) => { ... }
)
```

### Step 2: Extract Tool Definitions

For each tool, extract:
1. **name**: The tool identifier (e.g., 'create_document')
2. **description**: Tool description for JSDoc
3. **inputSchema**: Zod schema defining input parameters
4. **endpoint**: The MCP endpoint path (e.g., '/api/mcp-docs/message')

### Step 3: Generate TypeScript Interfaces

Convert Zod schemas to TypeScript interfaces:

```typescript
// From: z.object({ name: z.string(), email: z.string().email() })
// To:
export interface CreateEnquiryInput {
  name: string;
  email: string;
}
```

### Step 4: Generate Module Client

Create a client class with methods for each tool:

```typescript
// scripts/sdk/docs/client.ts
import { MCPClient, defaultClient } from '../client';
import type { CreateDocumentInput, CreateDocumentOutput } from './types';

const ENDPOINT = '/api/mcp-docs/message';

export class DocsClient {
  private mcp: MCPClient;

  constructor(client?: MCPClient) {
    this.mcp = client || defaultClient;
  }

  async createDocument(input: CreateDocumentInput): Promise<CreateDocumentOutput> {
    return this.mcp.callTool(ENDPOINT, 'create_document', input);
  }

  async listDocuments(input: ListDocumentsInput): Promise<ListDocumentsOutput> {
    return this.mcp.callTool(ENDPOINT, 'list_documents', input);
  }

  // ... one method per tool
}

export const docs = new DocsClient();
```

### Step 5: Generate Example Scripts

Create runnable examples in `scripts/sdk/examples/`:

```typescript
#!/usr/bin/env npx tsx
// scripts/sdk/examples/create-doc.ts
import { docs } from '../';

async function main() {
  const result = await docs.createDocument({
    spaceId: 'wiki',
    title: 'Getting Started',
    content: '# Welcome\n\nThis is the intro.',
  });

  console.log(`Created document: ${result.document.id}`);
}

main().catch(console.error);
```

### Step 6: Update Index Exports

Add module exports to `scripts/sdk/index.ts`:

```typescript
export { docs } from './docs';
export { enquiries } from './enquiries';
```

## Output Structure

```
project/
└── scripts/sdk/
    ├── index.ts           # Main exports
    ├── config.ts          # Environment config
    ├── errors.ts          # Error classes
    ├── client.ts          # MCP client
    │
    ├── docs/              # Generated module
    │   ├── types.ts       # TypeScript interfaces
    │   ├── client.ts      # Typed methods
    │   └── index.ts       # Module exports
    │
    ├── enquiries/         # Another module
    │   ├── types.ts
    │   ├── client.ts
    │   └── index.ts
    │
    └── examples/          # Runnable scripts
        ├── create-doc.ts
        ├── list-spaces.ts
        └── create-enquiry.ts
```

## Environment Variables

The SDK uses these environment variables:

| Variable | Description | Default |
|----------|-------------|---------|
| `SDK_MODE` | Execution mode: 'local', 'remote', 'auto' | 'auto' |
| `SDK_BASE_URL` | Target Worker URL | http://localhost:8787 |
| `SDK_API_TOKEN` | Bearer token for auth | (none) |

## Execution

Run generated scripts with:
```bash
SDK_API_TOKEN="your-token" SDK_BASE_URL="https://app.workers.dev" npx tsx scripts/sdk/examples/create-doc.ts
```

## Naming Conventions

- **Module names**: Lowercase, from MCP server name (e.g., 'mcp-docs' → 'docs')
- **Method names**: camelCase from tool name (e.g., 'create_document' → 'createDocument')
- **Type names**: PascalCase (e.g., 'CreateDocumentInput', 'CreateDocumentOutput')

## Error Handling

The SDK provides typed errors:

- `AuthError` - 401, invalid token
- `ValidationError` - Invalid input
- `NotFoundError` - Resource not found
- `RateLimitError` - 429, too many requests
- `MCPError` - MCP protocol errors
- `NetworkError` - Connection failures

## Regeneration

When MCP tools change, regenerate the SDK:
1. Re-scan `src/server/modules/mcp*/server.ts`
2. Update types.ts with new/changed schemas
3. Update client.ts with new/changed methods
4. Preserve any custom code in examples/
