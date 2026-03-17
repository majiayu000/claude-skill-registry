---
name: "MCP Development Skill"
description: "**Domain**: AI Infrastructure"
---

# MCP Development Skill

> **Domain**: AI Infrastructure
> **Inheritance**: inheritable
> **Version**: 1.1.0
> **Last Updated**: 2026-02-19

> ⚠️ **Staleness Watch**: MCP spec is actively versioned. Streamable HTTP replaced HTTP+SSE for remote servers (spec 2025-03-26). Check [MCP Changelog](https://modelcontextprotocol.io/changelog) when advising on transport selection.

---

## Overview

Complete guide to the Model Context Protocol (MCP)—an open standard for connecting AI assistants to external data sources and tools. Covers architecture, server development, client integration, and production deployment patterns.

---

## What Is MCP?

### The Problem MCP Solves

```text
Before MCP:
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Claude  │     │ ChatGPT │     │ Copilot │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     ▼               ▼               ▼
┌─────────┐     ┌─────────┐     ┌─────────┐
│Custom   │     │Custom   │     │Custom   │
│Plugin A │     │Plugin A'│     │Plugin A"│
└─────────┘     └─────────┘     └─────────┘
  (3 different implementations for same data source)

After MCP:
┌─────────┐     ┌─────────┐     ┌─────────┐
│ Claude  │     │ ChatGPT │     │ Copilot │
└────┬────┘     └────┬────┘     └────┬────┘
     │               │               │
     └───────────────┼───────────────┘
                     ▼
              ┌────────────┐
              │ MCP Server │  (One implementation, many clients)
              └────────────┘
```

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Host** | AI application (Claude Desktop, VS Code, etc.) |
| **Client** | MCP client within the host, manages server connections |
| **Server** | Provides tools, resources, and prompts via MCP |
| **Transport** | Communication layer (stdio, Streamable HTTP) |

### MCP Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                        MCP Host                             │
│  (Claude Desktop, VS Code, IDE, Custom App)                 │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────┐                                            │
│  │ MCP Client  │  Manages protocol, routing, lifecycle      │
│  └──────┬──────┘                                            │
│         │                                                   │
│    Transport Layer (stdio / Streamable HTTP)                │
│         │                                                   │
└─────────┼───────────────────────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────────────────────────────────┐
│                      MCP Server                             │
├─────────────────────────────────────────────────────────────┤
│  ┌───────────┐  ┌───────────┐  ┌───────────┐               │
│  │  Tools    │  │ Resources │  │  Prompts  │               │
│  │           │  │           │  │           │               │
│  │ Functions │  │ Data/Files│  │ Templates │               │
│  │ AI calls  │  │ AI reads  │  │ AI uses   │               │
│  └───────────┘  └───────────┘  └───────────┘               │
└─────────────────────────────────────────────────────────────┘
```

---

## MCP Primitives

### Tools

Functions the AI can execute:

```typescript
// Tool definition
{
  name: "search_issues",
  description: "Search GitHub issues in a repository",
  inputSchema: {
    type: "object",
    properties: {
      repo: { type: "string", description: "owner/repo format" },
      query: { type: "string", description: "Search query" },
      state: {
        type: "string",
        enum: ["open", "closed", "all"],
        default: "open"
      }
    },
    required: ["repo", "query"]
  }
}
```

**Tool Design Principles:**
- Clear, action-oriented names
- Comprehensive descriptions (when to use, what it returns)
- Strict input schemas with validation
- Idempotent when possible
- Return structured results

### Resources

Data the AI can read:

```typescript
// Resource definition
{
  uri: "github://repo/owner/repo-name/issues",
  name: "Repository Issues",
  description: "All issues in the repository",
  mimeType: "application/json"
}

// Resource template (dynamic)
{
  uriTemplate: "github://repo/{owner}/{repo}/issues/{id}",
  name: "GitHub Issue",
  description: "A specific GitHub issue",
  mimeType: "application/json"
}
```

**Resource Patterns:**
- Static: Fixed URIs for known data
- Template: Dynamic URIs with parameters
- Subscription: Real-time updates (notifications)

### Prompts

Reusable prompt templates:

```typescript
{
  name: "code_review",
  description: "Generate a code review for changes",
  arguments: [
    {
      name: "diff",
      description: "The code diff to review",
      required: true
    },
    {
      name: "focus",
      description: "Areas to focus on (security, performance, style)",
      required: false
    }
  ]
}
```

---

## Building MCP Servers

### TypeScript Server (Recommended)

```typescript
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new McpServer({
  name: "my-mcp-server",
  version: "1.0.0"
});

// Register a tool
server.tool(
  "get_weather",
  "Get current weather for a location",
  {
    location: {
      type: "string",
      description: "City name or coordinates"
    }
  },
  async ({ location }) => {
    const weather = await fetchWeather(location);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(weather, null, 2)
        }
      ]
    };
  }
);

// Register a resource
server.resource(
  "weather://current",
  "Current weather data",
  "application/json",
  async () => ({
    contents: [
      {
        uri: "weather://current",
        mimeType: "application/json",
        text: JSON.stringify(await getCurrentWeather())
      }
    ]
  })
);

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

### Python Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-mcp-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="get_weather",
            description="Get current weather for a location",
            inputSchema={
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "City name"
                    }
                },
                "required": ["location"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "get_weather":
        weather = await fetch_weather(arguments["location"])
        return [TextContent(type="text", text=str(weather))]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)
```

### Server Project Structure

```text
my-mcp-server/
├── package.json
├── tsconfig.json
├── src/
│   ├── index.ts          # Entry point
│   ├── server.ts         # Server setup
│   ├── tools/
│   │   ├── index.ts      # Tool registry
│   │   ├── search.ts     # Search tool
│   │   └── create.ts     # Create tool
│   ├── resources/
│   │   ├── index.ts      # Resource registry
│   │   └── data.ts       # Data resources
│   └── utils/
│       ├── auth.ts       # Authentication
│       └── cache.ts      # Caching
└── tests/
    └── tools.test.ts
```

---

## Transport Protocols

### stdio (Local)

Default for local servers:

```json
// Claude Desktop config
{
  "mcpServers": {
    "my-server": {
      "command": "node",
      "args": ["/path/to/server/dist/index.js"],
      "env": {
        "API_KEY": "xxx"
      }
    }
  }
}
```

**Characteristics:**
- Process-based communication
- Secure (no network exposure)
- Simple deployment
- Best for local tools

### Streamable HTTP (Remote) — Current Standard

For remote/shared servers (replaces deprecated HTTP+SSE as of MCP spec 2025-03-26):

```text
┌────────────┐         HTTPS          ┌────────────┐
│   Client   │ ◄─────────────────────► │   Server   │
│            │    POST /mcp            │            │
│            │    (streaming response) │            │
└────────────┘                         └────────────┘
```

**Characteristics:**
- Single HTTP endpoint handles both request and streaming response
- Network-accessible
- Supports authentication (Bearer tokens)
- Scalable (multiple clients)
- Requires security hardening

> ⚠️ **HTTP+SSE is deprecated.** Old servers used `POST /message` + `GET /sse`. If you encounter an HTTP+SSE server, it is using the legacy transport. Prefer Streamable HTTP for all new remote servers.

```typescript
import { StreamableHTTPServerTransport } from "@modelcontextprotocol/sdk/server/streamableHttp.js";

const transport = new StreamableHTTPServerTransport({ path: "/mcp" });
await server.connect(transport);
```

---

## Client Integration

### VS Code Integration

```typescript
// Using MCP in VS Code extension
import { McpClient } from "@modelcontextprotocol/sdk/client/mcp.js";

const client = new McpClient({
  name: "vscode-client",
  version: "1.0.0"
});

// Connect to server
await client.connect(transport);

// List available tools
const { tools } = await client.listTools();

// Call a tool
const result = await client.callTool({
  name: "search_issues",
  arguments: { repo: "owner/repo", query: "bug" }
});

// Read a resource
const { contents } = await client.readResource({
  uri: "github://repo/owner/repo/readme"
});
```

### Configuration Patterns

**Per-User Config** (Claude Desktop):
```json
// ~/Library/Application Support/Claude/claude_desktop_config.json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**Workspace Config** (VS Code):
```json
// .vscode/mcp.json
{
  "servers": {
    "project-tools": {
      "command": "node",
      "args": ["./tools/mcp-server.js"]
    }
  }
}
```

---

## Security Best Practices

### Authentication

```typescript
// API key from environment
const apiKey = process.env.SERVICE_API_KEY;
if (!apiKey) {
  throw new Error("SERVICE_API_KEY required");
}

// OAuth token refresh
async function getValidToken(): Promise<string> {
  if (tokenExpired()) {
    token = await refreshToken();
  }
  return token;
}
```

### Input Validation

```typescript
import { z } from "zod";

const SearchSchema = z.object({
  query: z.string().min(1).max(500),
  limit: z.number().int().min(1).max(100).default(10),
  filters: z.object({
    dateFrom: z.string().datetime().optional(),
    dateTo: z.string().datetime().optional()
  }).optional()
});

server.tool("search", "Search documents", SearchSchema, async (args) => {
  const validated = SearchSchema.parse(args);
  // Safe to use validated.query, validated.limit, etc.
});
```

### Rate Limiting

```typescript
import { RateLimiter } from "./utils/rate-limiter";

const limiter = new RateLimiter({
  maxRequests: 100,
  windowMs: 60 * 1000  // 1 minute
});

server.tool("expensive_operation", schema, async (args) => {
  if (!limiter.tryAcquire()) {
    return {
      content: [{
        type: "text",
        text: "Rate limit exceeded. Please try again later."
      }],
      isError: true
    };
  }
  // Proceed with operation
});
```

### Sandboxing

```typescript
// Restrict file system access
const ALLOWED_PATHS = ["/data", "/tmp"];

function validatePath(requestedPath: string): boolean {
  const resolved = path.resolve(requestedPath);
  return ALLOWED_PATHS.some(allowed =>
    resolved.startsWith(path.resolve(allowed))
  );
}

// Restrict network access
const ALLOWED_HOSTS = ["api.example.com", "data.example.com"];

function validateUrl(url: string): boolean {
  const parsed = new URL(url);
  return ALLOWED_HOSTS.includes(parsed.hostname);
}
```

---

## Production Patterns

### Error Handling

```typescript
server.tool("risky_operation", schema, async (args) => {
  try {
    const result = await performOperation(args);
    return {
      content: [{ type: "text", text: JSON.stringify(result) }]
    };
  } catch (error) {
    // Log for debugging
    console.error("Operation failed:", error);

    // Return user-friendly error
    return {
      content: [{
        type: "text",
        text: `Operation failed: ${getUserFriendlyMessage(error)}`
      }],
      isError: true
    };
  }
});

function getUserFriendlyMessage(error: unknown): string {
  if (error instanceof AuthError) {
    return "Authentication failed. Please check your credentials.";
  }
  if (error instanceof RateLimitError) {
    return "Rate limit exceeded. Please try again in a few minutes.";
  }
  if (error instanceof ValidationError) {
    return `Invalid input: ${error.message}`;
  }
  return "An unexpected error occurred. Please try again.";
}
```

### Logging & Observability

```typescript
import { Logger } from "./utils/logger";

const logger = new Logger("mcp-server");

server.tool("search", schema, async (args, context) => {
  const requestId = context.requestId || crypto.randomUUID();

  logger.info("Tool called", {
    requestId,
    tool: "search",
    args: sanitizeForLogging(args)
  });

  const startTime = Date.now();
  try {
    const result = await performSearch(args);

    logger.info("Tool completed", {
      requestId,
      tool: "search",
      durationMs: Date.now() - startTime,
      resultCount: result.items.length
    });

    return { content: [{ type: "text", text: JSON.stringify(result) }] };
  } catch (error) {
    logger.error("Tool failed", {
      requestId,
      tool: "search",
      durationMs: Date.now() - startTime,
      error: error.message
    });
    throw error;
  }
});
```

### Caching

```typescript
import { LRUCache } from "lru-cache";

const cache = new LRUCache<string, any>({
  max: 1000,
  ttl: 5 * 60 * 1000  // 5 minutes
});

server.tool("fetch_data", schema, async ({ id }) => {
  const cacheKey = `data:${id}`;

  // Check cache
  const cached = cache.get(cacheKey);
  if (cached) {
    return { content: [{ type: "text", text: JSON.stringify(cached) }] };
  }

  // Fetch fresh
  const data = await fetchFromAPI(id);
  cache.set(cacheKey, data);

  return { content: [{ type: "text", text: JSON.stringify(data) }] };
});
```

---

## Testing MCP Servers

### Unit Testing Tools

```typescript
import { describe, it, expect } from "vitest";
import { createTestServer } from "./test-utils";

describe("search tool", () => {
  it("returns results for valid query", async () => {
    const server = createTestServer();

    const result = await server.callTool({
      name: "search",
      arguments: { query: "test", limit: 5 }
    });

    expect(result.content).toHaveLength(1);
    expect(result.isError).toBeFalsy();

    const data = JSON.parse(result.content[0].text);
    expect(data.items).toHaveLength(5);
  });

  it("handles invalid input gracefully", async () => {
    const server = createTestServer();

    const result = await server.callTool({
      name: "search",
      arguments: { query: "", limit: -1 }
    });

    expect(result.isError).toBe(true);
    expect(result.content[0].text).toContain("Invalid");
  });
});
```

### Integration Testing

```typescript
import { spawn } from "child_process";
import { McpClient } from "@modelcontextprotocol/sdk/client/mcp.js";

describe("MCP Server Integration", () => {
  let serverProcess: ChildProcess;
  let client: McpClient;

  beforeAll(async () => {
    // Start server process
    serverProcess = spawn("node", ["dist/index.js"]);

    // Connect client
    client = new McpClient({ name: "test", version: "1.0.0" });
    await client.connect(new StdioClientTransport(serverProcess));
  });

  afterAll(() => {
    serverProcess.kill();
  });

  it("lists tools correctly", async () => {
    const { tools } = await client.listTools();
    expect(tools.map(t => t.name)).toContain("search");
  });
});
```

---

## Common MCP Servers

| Server | Purpose | Install |
|--------|---------|---------|
| filesystem | Local file access | `@modelcontextprotocol/server-filesystem` |
| github | GitHub API | `@modelcontextprotocol/server-github` |
| postgres | Database queries | `@modelcontextprotocol/server-postgres` |
| puppeteer | Web scraping | `@modelcontextprotocol/server-puppeteer` |
| memory | Persistent memory | `@modelcontextprotocol/server-memory` |

---

## Activation Triggers

- "MCP", "Model Context Protocol"
- "MCP server", "MCP client"
- "tool server", "resource server"
- "Claude Desktop config", "mcp.json"
- "stdio transport", "SSE transport"
- "@modelcontextprotocol"

---

## Quick Reference

### MCP Server Checklist

- [ ] Define clear tool/resource purposes
- [ ] Implement comprehensive input validation
- [ ] Add proper error handling with user-friendly messages
- [ ] Set up logging for debugging
- [ ] Implement rate limiting for expensive operations
- [ ] Add caching where appropriate
- [ ] Write unit and integration tests
- [ ] Document configuration requirements
- [ ] Consider security (auth, sandboxing)

### Tool vs Resource Decision

| Use Tool When | Use Resource When |
|---------------|-------------------|
| Action with side effects | Read-only data access |
| Requires input parameters | Static or template URI |
| Returns computed result | Returns stored content |
| May fail or have errors | Generally stable data |

---

*MCP Development skill — Building AI-accessible tools and data sources*
