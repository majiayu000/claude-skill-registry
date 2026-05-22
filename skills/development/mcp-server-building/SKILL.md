---
name: mcp-server-building
description: Building MCP (Model Context Protocol) servers for Claude extensibility. Use when creating MCP servers, building custom Claude tools, extending Claude with external integrations, or developing tool packages for Claude Desktop.
context: fork
agent: backend-system-architect
version: 1.0.0
author: SkillForge
user-invocable: false
---
# MCP Server Building
Build custom MCP servers to extend Claude with tools, resources, and prompts.

## When to Use

- Extending Claude with custom tools and capabilities
- Integrating external APIs and services with Claude
- Building domain-specific Claude extensions
- Creating reusable tool packages for Claude Desktop

## Core Concepts

### MCP Architecture
```
+-------------+     JSON-RPC      +-------------+
|   Claude    |<----------------->| MCP Server  |
|   (Host)    |   stdio/SSE/WS    |  (Tools)    |
+-------------+                   +-------------+
```

**Three Primitives**:
- **Tools**: Functions Claude can call (with user approval)
- **Resources**: Data Claude can read (files, API responses)
- **Prompts**: Pre-defined prompt templates

## Quick Start

### Minimal Python Server (stdio)
```python
# server.py
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

server = Server("my-tools")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="greet",
            description="Greet a user by name",
            inputSchema={
                "type": "object",
                "properties": {
                    "name": {"type": "string", "description": "Name to greet"}
                },
                "required": ["name"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "greet":
        return [TextContent(type="text", text=f"Hello, {arguments['name']}!")]
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read, write):
        await server.run(read, write, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### TypeScript Server (recommended for production)
```typescript
// src/index.ts
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import {
  CallToolRequestSchema,
  ListToolsRequestSchema,
} from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "my-tools", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "fetch_url",
      description: "Fetch content from a URL",
      inputSchema: {
        type: "object",
        properties: {
          url: { type: "string", description: "URL to fetch" },
        },
        required: ["url"],
      },
    },
  ],
}));

server.setRequestHandler(CallToolRequestSchema, async (request) => {
  if (request.params.name === "fetch_url") {
    const { url } = request.params.arguments as { url: string };
    const response = await fetch(url);
    const text = await response.text();
    return { content: [{ type: "text", text }] };
  }
  throw new Error("Unknown tool: " + request.params.name);
});

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Tool Definition Patterns

### Input Schema Best Practices
```python
Tool(
    name="search_database",
    description="Search the product database. Returns up to 10 results.",
    inputSchema={
        "type": "object",
        "properties": {
            "query": {
                "type": "string",
                "description": "Search query (supports wildcards with *)"
            },
            "category": {
                "type": "string",
                "enum": ["electronics", "clothing", "books"],
                "description": "Filter by category"
            },
            "max_results": {
                "type": "integer",
                "minimum": 1,
                "maximum": 50,
                "default": 10,
                "description": "Maximum results to return"
            }
        },
        "required": ["query"]
    }
)
```

**Guidelines**:
- Always include `description` for each property
- Use `enum` for fixed option sets
- Set `minimum`/`maximum` for numbers
- Mark `required` fields explicitly
- Provide `default` values where sensible

### Error Handling
```python
@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    try:
        if name == "query_api":
            result = await external_api.query(arguments["query"])
            return [TextContent(type="text", text=json.dumps(result))]
    except ExternalAPIError as e:
        # Return error as text - Claude will see and handle it
        return [TextContent(
            type="text",
            text=f"Error: API returned {e.status_code}: {e.message}"
        )]
    except Exception as e:
        # Log internally, return user-friendly message
        logger.exception("Tool execution failed")
        return [TextContent(
            type="text",
            text=f"Error: {type(e).__name__}: {str(e)}"
        )]
```

## Resource Patterns

### File Resources
```python
@server.list_resources()
async def list_resources() -> list[Resource]:
    return [
        Resource(
            uri="file:///config/settings.json",
            name="Settings",
            mimeType="application/json",
            description="Application configuration"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri == "file:///config/settings.json":
        return Path("settings.json").read_text()
    raise ValueError(f"Unknown resource: {uri}")
```

### Dynamic Resources (API data)
```python
@server.list_resources()
async def list_resources() -> list[Resource]:
    # List available data sources
    return [
        Resource(
            uri="api://users/current",
            name="Current User",
            mimeType="application/json"
        ),
        Resource(
            uri="api://metrics/today",
            name="Today's Metrics",
            mimeType="application/json"
        )
    ]

@server.read_resource()
async def read_resource(uri: str) -> str:
    if uri.startswith("api://"):
        endpoint = uri.replace("api://", "")
        data = await api_client.get(endpoint)
        return json.dumps(data, indent=2)
```

## Transport Options

### stdio (recommended for CLI)
```json
// claude_desktop_config.json
{
  "mcpServers": {
    "my-tools": {
      "command": "python",
      "args": ["/path/to/server.py"],
      "env": {
        "API_KEY": "xxx"
      }
    }
  }
}
```

### SSE (for web deployments)
```python
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route

sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(
            streams[0], streams[1],
            server.create_initialization_options()
        )

app = Starlette(routes=[
    Route("/sse", endpoint=handle_sse),
    Route("/messages", endpoint=sse.handle_post_message, methods=["POST"]),
])
```

## Configuration in Claude Desktop

```json
// ~/Library/Application Support/Claude/claude_desktop_config.json (macOS)
// %APPDATA%\Claude\claude_desktop_config.json (Windows)
{
  "mcpServers": {
    "database": {
      "command": "npx",
      "args": ["-y", "@myorg/db-tools"],
      "env": {
        "DATABASE_URL": "postgres://..."
      }
    },
    "python-tools": {
      "command": "uv",
      "args": ["run", "python", "-m", "my_mcp_server"],
      "cwd": "/path/to/project"
    }
  }
}
```

## Testing

### Manual Testing
```bash
# Test with MCP Inspector
npx @modelcontextprotocol/inspector python server.py
```

### Automated Testing
```python
import pytest
from mcp.client import Client
from mcp.client.stdio import stdio_client

@pytest.mark.asyncio
async def test_greet_tool():
    async with stdio_client("python", ["server.py"]) as (read, write):
        client = Client("test", "1.0.0")
        await client.connect(read, write)

        # List tools
        tools = await client.list_tools()
        assert any(t.name == "greet" for t in tools.tools)

        # Call tool
        result = await client.call_tool("greet", {"name": "World"})
        assert "Hello, World!" in result.content[0].text
```

## Common Patterns

### Caching Expensive Operations
```python
from functools import lru_cache
from datetime import datetime, timedelta

_cache = {}
_cache_ttl = timedelta(minutes=5)

async def get_cached_data(key: str) -> dict:
    now = datetime.now()
    if key in _cache:
        data, timestamp = _cache[key]
        if now - timestamp < _cache_ttl:
            return data

    data = await expensive_fetch(key)
    _cache[key] = (data, now)
    return data
```

### Rate Limiting
```python
import asyncio
from collections import defaultdict

_request_times = defaultdict(list)
MAX_REQUESTS_PER_MINUTE = 60

async def rate_limited_call(user_id: str, func, *args):
    now = asyncio.get_event_loop().time()
    _request_times[user_id] = [
        t for t in _request_times[user_id]
        if now - t < 60
    ]

    if len(_request_times[user_id]) >= MAX_REQUESTS_PER_MINUTE:
        raise Exception("Rate limit exceeded. Try again in a minute.")

    _request_times[user_id].append(now)
    return await func(*args)
```

## Anti-Patterns

1. **Stateful tools without cleanup**: Always clean up connections/resources
2. **Blocking synchronous code**: Use `asyncio.to_thread()` for blocking ops
3. **Missing input validation**: Always validate before processing
4. **Secrets in tool output**: Never return API keys or credentials
5. **Unbounded responses**: Limit response sizes (Claude has context limits)


---

## CC 2.1.7: Auto-Discovery Optimization

### MCP Search Discovery

CC 2.1.7 introduces automatic MCP discovery via `MCPSearch`. When context exceeds 10%, your MCP tools are still available but discovered on-demand rather than pre-loaded.

### Optimizing for Auto-Discovery

Make your tools easily discoverable by using descriptive names and keywords:

```python
# GOOD: Descriptive, searchable
Tool(
    name="query_product_database",
    description="""
    Search the product catalog database.

    KEYWORDS: products, catalog, inventory, SKU, search
    USE WHEN: User needs product info, pricing, availability
    """,
    inputSchema={...}
)

# BAD: Generic, hard to discover
Tool(
    name="search",
    description="Search things",
    inputSchema={...}
)
```

### Token-Efficient Tool Definitions

Since tool definitions consume context when loaded, optimize for size:

```python
# Verbose: ~200 tokens
Tool(
    name="search_database",
    description="This tool allows you to search our comprehensive database...",
    inputSchema={...}  # detailed descriptions
)

# Concise: ~80 tokens
Tool(
    name="search_database",
    description="Search database. Supports: full-text, filters. Returns: {id, title, snippet}",
    inputSchema={...}  # brief descriptions
)
```

### Discovery Metadata Pattern

Add discovery hints to improve MCPSearch matching:

```python
Tool(
    name="analyze_logs",
    description="""
    Analyze application logs for errors.

    Category: Observability
    Keywords: logs, errors, debugging, monitoring
    Triggers: "check logs", "find errors", "debug issue"
    """,
    inputSchema={...}
)
```

## Related Skills

- `function-calling` - LLM function calling patterns that MCP tools implement
- `agent-loops` - Agentic patterns that leverage MCP tools for actions
- `input-validation` - Input validation for MCP tool arguments
- `llm-safety-patterns` - Security patterns for MCP tool implementations

## Key Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Transport protocol | stdio for CLI, SSE for web | stdio is simplest, SSE for browser deployments |
| Language choice | TypeScript for production | Better SDK support, type safety |
| Tool descriptions | Concise with keywords | Optimize for CC 2.1.7 auto-discovery |
| Error handling | Return errors as text content | Claude can interpret and retry |

## Resources
- MCP Specification: https://modelcontextprotocol.io/docs
- Python SDK: https://github.com/modelcontextprotocol/python-sdk
- TypeScript SDK: https://github.com/modelcontextprotocol/typescript-sdk
- Example Servers: https://github.com/modelcontextprotocol/servers