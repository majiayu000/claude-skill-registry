---
name: MCP Server Generator
description: Expert guidance for creating, configuring, and deploying Model Context Protocol (MCP) servers. Use when building custom MCP servers, integrating external APIs, or extending Claude with new capabilities.
version: 1.0.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Bash
  - Glob
  - Grep
  - WebSearch
---

# MCP Server Generator

Comprehensive system for creating high-quality Model Context Protocol (MCP) servers that integrate external APIs, databases, and services with Claude.

## Core Concepts

### What is MCP?

Model Context Protocol (MCP) is an open standard that enables AI applications to connect to external data sources and tools. MCP servers provide:

- **Resources**: File-like data (documents, logs, database schemas)
- **Tools**: Executable functions (API calls, calculations, searches)
- **Prompts**: Reusable prompt templates
- **Sampling**: LLM completion requests

### MCP Architecture

```
┌─────────────┐         ┌─────────────┐         ┌──────────────┐
│   Claude    │ ◄─────► │ MCP Server  │ ◄─────► │ External API │
│  (Client)   │   MCP   │  (Bridge)   │         │  or Service  │
└─────────────┘         └─────────────┘         └──────────────┘
```

## Implementation Patterns

### 1. TypeScript/Node.js MCP Server

**Basic Structure:**
```typescript
#!/usr/bin/env node
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
  ListResourcesRequestSchema,
  ReadResourceRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

// Initialize server
const server = new Server(
  {
    name: "my-mcp-server",
    version: "1.0.0",
  },
  {
    capabilities: {
      tools: {},
      resources: {},
      prompts: {},
    },
  }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "example_tool",
        description: "An example tool that does something useful",
        inputSchema: {
          type: "object",
          properties: {
            query: {
              type: "string",
              description: "The query parameter",
            },
          },
          required: ["query"],
        },
      },
    ],
  };
});

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "example_tool") {
    const result = await performAction(args.query);
    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// List resources
server.setRequestHandler(ListResourcesRequestSchema, async () => {
  return {
    resources: [
      {
        uri: "example://resource/1",
        name: "Example Resource",
        description: "An example resource",
        mimeType: "application/json",
      },
    ],
  };
});

// Read resource
server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;

  if (uri === "example://resource/1") {
    return {
      contents: [
        {
          uri,
          mimeType: "application/json",
          text: JSON.stringify({ data: "example" }, null, 2),
        },
      ],
    };
  }

  throw new Error(`Resource not found: ${uri}`);
});

// Start server
async function main() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("MCP Server running on stdio");
}

main().catch(console.error);
```

**package.json:**
```json
{
  "name": "my-mcp-server",
  "version": "1.0.0",
  "type": "module",
  "bin": {
    "my-mcp-server": "./dist/index.js"
  },
  "scripts": {
    "build": "tsc && chmod +x dist/index.js",
    "dev": "tsc --watch",
    "prepare": "npm run build"
  },
  "dependencies": {
    "@modelcontextprotocol/sdk": "^0.5.0"
  },
  "devDependencies": {
    "@types/node": "^20.0.0",
    "typescript": "^5.3.0"
  }
}
```

**tsconfig.json:**
```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "Node16",
    "moduleResolution": "Node16",
    "outDir": "./dist",
    "rootDir": "./src",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "resolveJsonModule": true,
    "declaration": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist"]
}
```

### 2. Python MCP Server

**Basic Structure:**
```python
#!/usr/bin/env python3
import asyncio
import logging
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    Tool,
    TextContent,
    Resource,
    INTERNAL_ERROR,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize server
app = Server("my-mcp-server")

@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools."""
    return [
        Tool(
            name="example_tool",
            description="An example tool that does something useful",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The query parameter",
                    },
                },
                "required": ["query"],
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """Handle tool calls."""
    if name == "example_tool":
        query = arguments.get("query")
        result = await perform_action(query)

        return [
            TextContent(
                type="text",
                text=str(result),
            )
        ]

    raise ValueError(f"Unknown tool: {name}")

@app.list_resources()
async def list_resources() -> list[Resource]:
    """List available resources."""
    return [
        Resource(
            uri="example://resource/1",
            name="Example Resource",
            description="An example resource",
            mimeType="application/json",
        ),
    ]

@app.read_resource()
async def read_resource(uri: str) -> str:
    """Read resource content."""
    if uri == "example://resource/1":
        return '{"data": "example"}'

    raise ValueError(f"Resource not found: {uri}")

async def perform_action(query: str) -> dict:
    """Perform the actual action."""
    # Your implementation here
    return {"query": query, "result": "success"}

async def main():
    """Run the MCP server."""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

**pyproject.toml:**
```toml
[project]
name = "my-mcp-server"
version = "1.0.0"
description = "MCP server for..."
requires-python = ">=3.10"
dependencies = [
    "mcp>=0.9.0",
]

[project.scripts]
my-mcp-server = "my_mcp_server:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"
```

### 3. Common MCP Server Patterns

#### API Integration Server

```typescript
// GitHub API MCP Server Example
import { Octokit } from "@octokit/rest";

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_repositories",
        description: "Search GitHub repositories",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "Search query" },
            language: { type: "string", description: "Filter by language" },
            limit: { type: "number", description: "Max results", default: 10 },
          },
          required: ["query"],
        },
      },
      {
        name: "get_repository",
        description: "Get repository details",
        inputSchema: {
          type: "object",
          properties: {
            owner: { type: "string", description: "Repository owner" },
            repo: { type: "string", description: "Repository name" },
          },
          required: ["owner", "repo"],
        },
      },
      {
        name: "create_issue",
        description: "Create a new issue",
        inputSchema: {
          type: "object",
          properties: {
            owner: { type: "string" },
            repo: { type: "string" },
            title: { type: "string" },
            body: { type: "string" },
            labels: { type: "array", items: { type: "string" } },
          },
          required: ["owner", "repo", "title"],
        },
      },
    ],
  };
});

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  switch (name) {
    case "search_repositories": {
      const result = await octokit.search.repos({
        q: `${args.query}${args.language ? ` language:${args.language}` : ""}`,
        per_page: args.limit || 10,
      });
      return {
        content: [
          {
            type: "text",
            text: JSON.stringify(
              result.data.items.map((item) => ({
                name: item.full_name,
                description: item.description,
                stars: item.stargazers_count,
                url: item.html_url,
              })),
              null,
              2
            ),
          },
        ],
      };
    }

    case "get_repository": {
      const result = await octokit.repos.get({
        owner: args.owner,
        repo: args.repo,
      });
      return {
        content: [
          { type: "text", text: JSON.stringify(result.data, null, 2) },
        ],
      };
    }

    case "create_issue": {
      const result = await octokit.issues.create({
        owner: args.owner,
        repo: args.repo,
        title: args.title,
        body: args.body,
        labels: args.labels,
      });
      return {
        content: [
          { type: "text", text: `Issue created: ${result.data.html_url}` },
        ],
      };
    }

    default:
      throw new Error(`Unknown tool: ${name}`);
  }
});
```

#### Database Integration Server

```python
# PostgreSQL MCP Server Example
import asyncpg
from mcp.server import Server
from mcp.types import Tool, TextContent

app = Server("postgres-mcp-server")

# Connection pool
pool = None

async def init_db():
    global pool
    pool = await asyncpg.create_pool(
        host=os.getenv("DB_HOST", "localhost"),
        port=int(os.getenv("DB_PORT", "5432")),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
    )

@app.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="query_database",
            description="Execute a read-only SQL query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "SQL SELECT query to execute",
                    },
                },
                "required": ["query"],
            },
        ),
        Tool(
            name="get_schema",
            description="Get database schema information",
            inputSchema={
                "type": "object",
                "properties": {
                    "table_name": {
                        "type": "string",
                        "description": "Optional table name to filter",
                    },
                },
            },
        ),
    ]

@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    if name == "query_database":
        query = arguments.get("query", "")

        # Security: Only allow SELECT queries
        if not query.strip().upper().startswith("SELECT"):
            raise ValueError("Only SELECT queries are allowed")

        async with pool.acquire() as conn:
            results = await conn.fetch(query)
            return [
                TextContent(
                    type="text",
                    text=json.dumps([dict(row) for row in results], indent=2),
                )
            ]

    elif name == "get_schema":
        table_filter = arguments.get("table_name")

        query = """
            SELECT table_name, column_name, data_type, is_nullable
            FROM information_schema.columns
            WHERE table_schema = 'public'
        """

        if table_filter:
            query += f" AND table_name = '{table_filter}'"

        async with pool.acquire() as conn:
            results = await conn.fetch(query)
            return [
                TextContent(
                    type="text",
                    text=json.dumps([dict(row) for row in results], indent=2),
                )
            ]

    raise ValueError(f"Unknown tool: {name}")
```

#### File System Server

```typescript
// File System MCP Server
import fs from "fs/promises";
import path from "path";

const ALLOWED_DIRECTORIES = [
  process.env.DOCS_PATH || "./docs",
  process.env.DATA_PATH || "./data",
];

function isPathAllowed(filePath: string): boolean {
  const absPath = path.resolve(filePath);
  return ALLOWED_DIRECTORIES.some((dir) =>
    absPath.startsWith(path.resolve(dir))
  );
}

server.setRequestHandler(ListResourcesRequestSchema, async () => {
  const resources = [];

  for (const dir of ALLOWED_DIRECTORIES) {
    const files = await fs.readdir(dir, { recursive: true });
    for (const file of files) {
      const fullPath = path.join(dir, file);
      const stats = await fs.stat(fullPath);

      if (stats.isFile()) {
        resources.push({
          uri: `file://${fullPath}`,
          name: file,
          description: `File at ${fullPath}`,
          mimeType: getMimeType(fullPath),
        });
      }
    }
  }

  return { resources };
});

server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
  const { uri } = request.params;
  const filePath = uri.replace("file://", "");

  if (!isPathAllowed(filePath)) {
    throw new Error("Access denied");
  }

  const content = await fs.readFile(filePath, "utf-8");

  return {
    contents: [
      {
        uri,
        mimeType: getMimeType(filePath),
        text: content,
      },
    ],
  };
});

server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "search_files",
        description: "Search for files by name or content",
        inputSchema: {
          type: "object",
          properties: {
            query: { type: "string", description: "Search query" },
            type: {
              type: "string",
              enum: ["name", "content"],
              description: "Search by filename or content",
            },
          },
          required: ["query", "type"],
        },
      },
      {
        name: "write_file",
        description: "Write content to a file",
        inputSchema: {
          type: "object",
          properties: {
            path: { type: "string", description: "File path" },
            content: { type: "string", description: "File content" },
          },
          required: ["path", "content"],
        },
      },
    ],
  };
});
```

### 4. Configuration & Deployment

**Claude Desktop Configuration:**

On macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
On Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "my-mcp-server": {
      "command": "node",
      "args": ["/path/to/my-mcp-server/dist/index.js"],
      "env": {
        "API_KEY": "your-api-key",
        "LOG_LEVEL": "info"
      }
    },
    "python-mcp-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "DATABASE_URL": "postgresql://localhost/mydb"
      }
    },
    "npx-server": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_..."
      }
    }
  }
}
```

**Environment Variables Best Practices:**

```typescript
// Load from .env file
import dotenv from "dotenv";
dotenv.config();

// Validate required env vars
const requiredEnvVars = ["API_KEY", "DATABASE_URL"];
for (const varName of requiredEnvVars) {
  if (!process.env[varName]) {
    throw new Error(`Missing required environment variable: ${varName}`);
  }
}

// Use with defaults
const config = {
  apiKey: process.env.API_KEY,
  apiUrl: process.env.API_URL || "https://api.example.com",
  timeout: parseInt(process.env.TIMEOUT || "30000"),
  maxRetries: parseInt(process.env.MAX_RETRIES || "3"),
};
```

### 5. Error Handling & Logging

**Comprehensive Error Handling:**

```typescript
import { McpError, ErrorCode } from "@modelcontextprotocol/sdk/types.js";

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    // Validate arguments
    if (!args.query) {
      throw new McpError(
        ErrorCode.InvalidParams,
        "Missing required parameter: query"
      );
    }

    // Perform action
    const result = await performAction(args.query);

    return {
      content: [
        {
          type: "text",
          text: JSON.stringify(result, null, 2),
        },
      ],
    };
  } catch (error) {
    // Log error
    console.error(`Error in tool ${name}:`, error);

    // Return user-friendly error
    if (error instanceof McpError) {
      throw error;
    }

    throw new McpError(
      ErrorCode.InternalError,
      `Failed to execute tool: ${error.message}`
    );
  }
});
```

**Structured Logging:**

```python
import logging
import json
from datetime import datetime

# Configure JSON logging
class JSONFormatter(logging.Formatter):
    def format(self, record):
        log_data = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
        }
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        return json.dumps(log_data)

handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger = logging.getLogger(__name__)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

# Use in code
logger.info("Tool called", extra={"tool_name": name, "args": arguments})
logger.error("API request failed", extra={"status_code": 500, "url": api_url})
```

### 6. Testing Strategies

**Unit Testing:**

```typescript
import { describe, it, expect, beforeAll, afterAll } from "vitest";
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

describe("MCP Server", () => {
  let client: Client;
  let transport: StdioClientTransport;

  beforeAll(async () => {
    transport = new StdioClientTransport({
      command: "node",
      args: ["./dist/index.js"],
    });

    client = new Client(
      {
        name: "test-client",
        version: "1.0.0",
      },
      {
        capabilities: {},
      }
    );

    await client.connect(transport);
  });

  afterAll(async () => {
    await client.close();
  });

  it("should list tools", async () => {
    const response = await client.listTools();
    expect(response.tools).toHaveLength(3);
    expect(response.tools[0].name).toBe("example_tool");
  });

  it("should call tool successfully", async () => {
    const response = await client.callTool({
      name: "example_tool",
      arguments: { query: "test" },
    });
    expect(response.content).toBeDefined();
  });

  it("should handle errors gracefully", async () => {
    await expect(
      client.callTool({
        name: "non_existent_tool",
        arguments: {},
      })
    ).rejects.toThrow();
  });
});
```

**Integration Testing:**

```bash
# Test server manually
node dist/index.js &
SERVER_PID=$!

# Send test requests
echo '{"jsonrpc":"2.0","id":1,"method":"tools/list"}' | node dist/index.js

# Cleanup
kill $SERVER_PID
```

### 7. Performance Optimization

**Caching:**

```typescript
import NodeCache from "node-cache";

const cache = new NodeCache({ stdTTL: 600 }); // 10 minutes

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "expensive_operation") {
    const cacheKey = `${name}:${JSON.stringify(args)}`;

    // Check cache
    const cached = cache.get(cacheKey);
    if (cached) {
      return {
        content: [{ type: "text", text: JSON.stringify(cached) }],
      };
    }

    // Perform operation
    const result = await expensiveOperation(args);

    // Store in cache
    cache.set(cacheKey, result);

    return {
      content: [{ type: "text", text: JSON.stringify(result) }],
    };
  }
});
```

**Rate Limiting:**

```typescript
import rateLimit from "express-rate-limit";

const limiter = new Map();

function checkRateLimit(key: string): boolean {
  const now = Date.now();
  const record = limiter.get(key) || { count: 0, resetAt: now + 60000 };

  if (now > record.resetAt) {
    record.count = 0;
    record.resetAt = now + 60000;
  }

  record.count++;
  limiter.set(key, record);

  return record.count <= 100; // 100 requests per minute
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (!checkRateLimit("global")) {
    throw new McpError(ErrorCode.InternalError, "Rate limit exceeded");
  }

  // Handle request...
});
```

### 8. Security Best Practices

**Input Validation:**

```typescript
import { z } from "zod";

const toolInputSchemas = {
  search_query: z.object({
    query: z.string().min(1).max(500),
    limit: z.number().int().min(1).max(100).optional(),
    filters: z.record(z.string()).optional(),
  }),
};

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  // Validate input
  const schema = toolInputSchemas[name];
  if (!schema) {
    throw new McpError(ErrorCode.InvalidParams, `Unknown tool: ${name}`);
  }

  try {
    const validatedArgs = schema.parse(args);
    // Use validatedArgs...
  } catch (error) {
    throw new McpError(
      ErrorCode.InvalidParams,
      `Invalid arguments: ${error.message}`
    );
  }
});
```

**Access Control:**

```typescript
function checkPermissions(userId: string, action: string): boolean {
  const permissions = {
    admin: ["read", "write", "delete"],
    user: ["read"],
    guest: [],
  };

  const userRole = getUserRole(userId);
  return permissions[userRole]?.includes(action) || false;
}

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const userId = request.params._meta?.userId;
  const action = getActionFromTool(request.params.name);

  if (!checkPermissions(userId, action)) {
    throw new McpError(ErrorCode.InvalidParams, "Permission denied");
  }

  // Proceed with request...
});
```

### 9. Publishing & Distribution

**NPM Package:**

```json
{
  "name": "@company/mcp-server-example",
  "version": "1.0.0",
  "description": "MCP server for...",
  "main": "dist/index.js",
  "bin": {
    "mcp-server-example": "dist/index.js"
  },
  "files": ["dist", "README.md", "LICENSE"],
  "keywords": ["mcp", "claude", "mcp-server"],
  "repository": {
    "type": "git",
    "url": "https://github.com/company/mcp-server-example"
  },
  "publishConfig": {
    "access": "public"
  }
}
```

**Docker Distribution:**

```dockerfile
FROM node:18-alpine
WORKDIR /app
COPY package*.json ./
RUN npm ci --only=production
COPY dist ./dist
USER node
CMD ["node", "dist/index.js"]
```

### 10. Documentation Template

**README.md:**

```markdown
# My MCP Server

> [Brief description of what this server does]

## Features

- Feature 1
- Feature 2
- Feature 3

## Installation

\`\`\`bash
npm install -g my-mcp-server
\`\`\`

## Configuration

Add to your Claude Desktop config:

\`\`\`json
{
  "mcpServers": {
    "my-server": {
      "command": "my-mcp-server",
      "env": {
        "API_KEY": "your-api-key"
      }
    }
  }
}
\`\`\`

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| API_KEY | Yes | Your API key |
| API_URL | No | API endpoint (default: https://api.example.com) |

## Available Tools

### tool_name

Description of what this tool does.

**Parameters:**
- `param1` (string, required): Description
- `param2` (number, optional): Description

**Example:**
\`\`\`
Use the tool_name tool with parameter "value"
\`\`\`

## Available Resources

### resource://example/1

Description of this resource.

## Development

\`\`\`bash
git clone https://github.com/company/my-mcp-server
cd my-mcp-server
npm install
npm run build
npm run dev
\`\`\`

## License

MIT
```

## Quick Start Checklist

- [ ] Choose implementation language (TypeScript/Python)
- [ ] Set up project structure with proper tooling
- [ ] Implement tools with clear input schemas
- [ ] Add comprehensive error handling
- [ ] Implement caching for expensive operations
- [ ] Add input validation and sanitization
- [ ] Set up structured logging
- [ ] Write unit and integration tests
- [ ] Create detailed documentation
- [ ] Configure environment variables properly
- [ ] Add rate limiting if needed
- [ ] Implement access control if needed
- [ ] Test with Claude Desktop
- [ ] Publish to npm/PyPI or Docker

## Common Use Cases

1. **API Integration**: GitHub, Jira, Slack, Linear, Notion
2. **Database Access**: PostgreSQL, MongoDB, Redis, Elasticsearch
3. **File Systems**: Local files, S3, Google Drive, Dropbox
4. **Developer Tools**: Git operations, CI/CD, deployment
5. **Business Tools**: CRM, ERP, analytics platforms
6. **AI/ML**: Vector databases, model APIs, embeddings
7. **Communication**: Email, SMS, webhooks, notifications
8. **Monitoring**: Logs, metrics, alerts, dashboards

---

**When to Use This Skill:**

Invoke when building new MCP servers, troubleshooting existing servers, or integrating external services with Claude.
