---
name: cloudflare-mcp-server
description: Build MCP (Model Context Protocol) servers on Cloudflare Workers with tools, resources, and prompts.
license: MIT
---

# Cloudflare MCP Server

**Last Updated**: 2025-11-21

## Quick Start

```typescript
import { McpServer } from '@modelcontextprotocol/sdk';

const server = new McpServer({
  name: 'my-server',
  version: '1.0.0'
});

server.tool('getTodo', async ({ id }) => ({
  id,
  title: 'Task',
  completed: false
}));

export default server;
```

## Core Concepts

- **Tools**: Functions AI can call
- **Resources**: Data AI can access
- **Prompts**: Reusable templates
- **Transports**: SSE, HTTP, WebSocket

## Example Tool

```typescript
server.tool('searchDocs', {
  description: 'Search documentation',
  parameters: {
    type: 'object',
    properties: {
      query: { type: 'string' }
    }
  },
  handler: async ({ query }) => {
    return { results: [...] };
  }
});
```

## Resources

### Core Documentation
- `references/quick-start-guide.md` (704 lines) - Official Cloudflare templates, complete step-by-step workflow, 5-minute setup
- `references/core-concepts.md` (66 lines) - MCP fundamentals: tools, resources, prompts, transports
- `references/worker-basics.md` (326 lines) - Worker & Durable Objects basics, transport selection, HTTP fundamentals
- `references/stateful-servers.md` (246 lines) - Durable Objects integration, WebSocket hibernation, cost optimization, common patterns
- `references/production-deployment.md` (814 lines) - Deployment & testing, configuration reference, authentication patterns, 22 known errors with solutions

### Templates
- `templates/basic-mcp.ts` - Minimal MCP server
- `templates/tools-example.ts` - Tool definitions
- `templates/durable-object-mcp.ts` - Stateful MCP with DO
- `templates/websocket-mcp.ts` - WebSocket transport

**Official Docs**: https://modelcontextprotocol.io | **Cloudflare**: https://developers.cloudflare.com/workers/runtime-apis/durable-objects/
