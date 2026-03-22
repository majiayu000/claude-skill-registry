---
name: mcp-server-creation
description: >
  Guide for creating MCP (Model Context Protocol) servers in TypeScript and Python,
  including scaffolding, transports, lifecycle hooks, and testing. Use when the user
  wants to build an MCP server, add tools/resources/prompts to an MCP server, configure
  stdio or SSE transport, or test MCP server functionality.
---

# MCP Server Creation

How to build MCP servers from scratch in TypeScript and Python. Covers project setup,
transport configuration, tool/resource/prompt registration, lifecycle hooks, and testing.

## When to Use
- User wants to create a new MCP server
- User is adding tools, resources, or prompts to an MCP server
- User needs to configure stdio or SSE transport
- User is testing or debugging an MCP server
- User asks about MCP server architecture or lifecycle

## Core Patterns

### TypeScript MCP Server Scaffold

```bash
# Initialize project
mkdir my-mcp-server && cd my-mcp-server
npm init -y
npm install @modelcontextprotocol/sdk zod
npm install -D typescript @types/node
npx tsc --init
```

```typescript
// src/index.ts - Minimal MCP server with stdio transport
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const server = new McpServer({
  name: "my-server",
  version: "1.0.0",
});

// Register a tool
server.tool(
  "greet",
  "Greet a user by name. Use when the user wants a personalized greeting.",
  { name: z.string().describe("The person's name") },
  async ({ name }) => ({
    content: [{ type: "text", text: `Hello, ${name}!` }],
  })
);

// Start with stdio transport
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP server running on stdio");
}

main().catch(console.error);
```

### Python MCP Server Scaffold

```bash
# Initialize project
mkdir my-mcp-server && cd my-mcp-server
pip install mcp
```

```python
# server.py - Minimal MCP server with stdio transport
import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
import mcp.types as types

server = Server("my-server")

@server.list_tools()
async def list_tools() -> list[types.Tool]:
    return [
        types.Tool(
            name="greet",
            description="Greet a user by name. Use when the user wants a personalized greeting.",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "The person's name"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    if name == "greet":
        return [types.TextContent(type="text", text=f"Hello, {arguments['name']}!")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    asyncio.run(main())
```

### SSE Transport (HTTP)

For remote MCP servers accessible over HTTP.

```typescript
// TypeScript - SSE transport
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { SSEServerTransport } from "@modelcontextprotocol/sdk/server/sse.js";
import express from "express";

const app = express();
const server = new McpServer({ name: "my-server", version: "1.0.0" });

// Register tools on server...

app.get("/sse", async (req, res) => {
  const transport = new SSEServerTransport("/messages", res);
  await server.connect(transport);
});

app.post("/messages", async (req, res) => {
  // Handle incoming messages from the transport
  await transport.handlePostMessage(req, res);
});

app.listen(3001, () => console.error("MCP SSE server on port 3001"));
```

### Lifecycle Hooks

Handle server initialization and shutdown gracefully.

```typescript
const server = new McpServer({ name: "my-server", version: "1.0.0" });

// The server handles lifecycle automatically, but you can add cleanup
process.on("SIGINT", async () => {
  console.error("Shutting down MCP server...");
  await server.close();
  process.exit(0);
});

process.on("SIGTERM", async () => {
  await server.close();
  process.exit(0);
});
```

### Testing MCP Servers

Test your MCP server using the MCP Inspector or programmatically with an in-memory client.

```bash
# Use MCP Inspector for interactive testing
npx @modelcontextprotocol/inspector node dist/index.js
```

```typescript
// Programmatic testing with in-memory transport
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { InMemoryTransport } from "@modelcontextprotocol/sdk/inMemory.js";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";

async function testServer() {
  const server = new McpServer({ name: "test", version: "1.0.0" });
  // Register tools...

  const [clientTransport, serverTransport] = InMemoryTransport.createLinkedPair();
  await server.connect(serverTransport);

  const client = new Client({ name: "test-client", version: "1.0.0" });
  await client.connect(clientTransport);

  // Call a tool
  const result = await client.callTool({ name: "greet", arguments: { name: "World" } });
  console.assert(result.content[0].text === "Hello, World!");

  await client.close();
  await server.close();
}
```

### Claude Desktop Configuration

Register your MCP server in Claude Desktop's config.

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/absolute/path/to/dist/index.js"],
      "env": {
        "API_KEY": "your-key-here"
      }
    }
  }
}
```

## Anti-Patterns
- Using console.log in stdio servers (stdout is the transport channel -- use console.error)
- Not validating tool inputs with a schema (leads to runtime crashes)
- Blocking the event loop in tool handlers (use async operations)
- Hardcoding secrets in server code instead of reading from environment variables
- Not handling unknown tool names in the call_tool handler
- Missing error handling in tool execution (unhandled errors crash the server)
- Creating one massive tool instead of composing multiple focused tools

## Quick Reference

| Component | TypeScript Import |
|-----------|-------------------|
| Server | `@modelcontextprotocol/sdk/server/mcp.js` |
| Stdio | `@modelcontextprotocol/sdk/server/stdio.js` |
| SSE | `@modelcontextprotocol/sdk/server/sse.js` |
| InMemory | `@modelcontextprotocol/sdk/inMemory.js` |
| Client | `@modelcontextprotocol/sdk/client/index.js` |

| Transport | Use Case |
|-----------|----------|
| stdio | Local tools, CLI integration, Claude Desktop |
| SSE | Remote servers, web-accessible tools |
| In-memory | Testing, same-process communication |

MCP Inspector: `npx @modelcontextprotocol/inspector <command> <args>`
