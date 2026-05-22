---
name: mcp-integration-patterns
description: Builds MCP (Model Context Protocol) servers and clients for extending AI assistants with custom tools, resources, and prompts.
license: MIT
---

# MCP Integration Patterns

This skill provides guidance for building Model Context Protocol (MCP) servers and clients that extend AI assistants with custom capabilities.

## Core Competencies

- **MCP Server Development**: Exposing tools, resources, and prompts
- **MCP Client Integration**: Connecting to MCP servers
- **Transport Protocols**: stdio, HTTP/SSE, WebSocket
- **Security**: Authentication, authorization, sandboxing

## MCP Fundamentals

### What MCP Provides

```
┌─────────────────────────────────────────────────────────────────────┐
│                         AI Assistant (Claude)                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐                 │
│  │   Tools     │  │  Resources  │  │   Prompts   │                 │
│  │  (Actions)  │  │   (Data)    │  │ (Templates) │                 │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘                 │
│         │                │                │                         │
│         └────────────────┼────────────────┘                         │
│                          │                                          │
│                    MCP Protocol                                     │
│                          │                                          │
├──────────────────────────┼──────────────────────────────────────────┤
│                          │                                          │
│  ┌───────────────────────┼───────────────────────────────────────┐ │
│  │                   MCP Servers                                  │ │
│  │                                                                │ │
│  │  ┌─────────┐   ┌─────────┐   ┌─────────┐   ┌─────────┐       │ │
│  │  │Database │   │   Git   │   │  Slack  │   │ Custom  │       │ │
│  │  │ Server  │   │ Server  │   │ Server  │   │ Server  │       │ │
│  │  └─────────┘   └─────────┘   └─────────┘   └─────────┘       │ │
│  └────────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────────┘
```

### MCP Primitives

| Primitive | Purpose | Direction |
|-----------|---------|-----------|
| Tools | Execute actions | Client → Server |
| Resources | Expose data | Client ← Server |
| Prompts | Template interactions | Client ← Server |
| Sampling | Request completions | Client ← Server |

## Building an MCP Server

### Python SDK Server

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Resource

# Initialize server
server = Server("my-custom-server")

# Define tools
@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="search_documents",
            description="Search internal documents by query",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "limit": {
                        "type": "integer",
                        "description": "Max results",
                        "default": 10
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="create_ticket",
            description="Create a support ticket",
            inputSchema={
                "type": "object",
                "properties": {
                    "title": {"type": "string"},
                    "description": {"type": "string"},
                    "priority": {
                        "type": "string",
                        "enum": ["low", "medium", "high"]
                    }
                },
                "required": ["title", "description"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search_documents":
        results = await search_documents(
            arguments["query"],
            arguments.get("limit", 10)
        )
        return [TextContent(
            type="text",
            text=format_results(results)
        )]

    elif name == "create_ticket":
        ticket = await create_ticket(
            arguments["title"],
            arguments["description"],
            arguments.get("priority", "medium")
        )
        return [TextContent(
            type="text",
            text=f"Created ticket #{ticket.id}"
        )]

    raise ValueError(f"Unknown tool: {name}")

# Run server
async def main():
    async with stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream)

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

### TypeScript SDK Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { ListToolsRequestSchema, CallToolRequestSchema } from "@modelcontextprotocol/sdk/types.js";

const server = new Server(
  { name: "my-custom-server", version: "1.0.0" },
  { capabilities: { tools: {} } }
);

// List available tools
server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [
    {
      name: "execute_query",
      description: "Execute a SQL query against the database",
      inputSchema: {
        type: "object",
        properties: {
          query: { type: "string", description: "SQL query to execute" },
          database: { type: "string", description: "Target database" }
        },
        required: ["query"]
      }
    }
  ]
}));

// Handle tool calls
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  if (name === "execute_query") {
    const results = await executeQuery(args.query, args.database);
    return {
      content: [{ type: "text", text: JSON.stringify(results, null, 2) }]
    };
  }

  throw new Error(`Unknown tool: ${name}`);
});

// Start server
const transport = new StdioServerTransport();
await server.connect(transport);
```

## Resources

Expose data that the AI can read.

```python
from mcp.types import Resource, ResourceTemplate

@server.list_resources()
async def list_resources():
    return [
        Resource(
            uri="file:///config/settings.json",
            name="Application Settings",
            description="Current application configuration",
            mimeType="application/json"
        ),
        Resource(
            uri="db://users/schema",
            name="Users Table Schema",
            description="Database schema for users table",
            mimeType="text/plain"
        )
    ]

@server.list_resource_templates()
async def list_resource_templates():
    return [
        ResourceTemplate(
            uriTemplate="file:///logs/{date}.log",
            name="Daily Logs",
            description="Application logs for a specific date"
        ),
        ResourceTemplate(
            uriTemplate="db://tables/{table_name}/schema",
            name="Table Schema",
            description="Schema for any database table"
        )
    ]

@server.read_resource()
async def read_resource(uri: str):
    if uri == "file:///config/settings.json":
        settings = await load_settings()
        return settings

    if uri.startswith("db://"):
        # Parse URI and fetch from database
        return await fetch_db_resource(uri)

    if uri.startswith("file:///logs/"):
        date = uri.split("/")[-1].replace(".log", "")
        return await read_log_file(date)

    raise ValueError(f"Unknown resource: {uri}")
```

## Prompts

Provide reusable prompt templates.

```python
from mcp.types import Prompt, PromptArgument, PromptMessage

@server.list_prompts()
async def list_prompts():
    return [
        Prompt(
            name="code_review",
            description="Review code for best practices and bugs",
            arguments=[
                PromptArgument(
                    name="code",
                    description="The code to review",
                    required=True
                ),
                PromptArgument(
                    name="language",
                    description="Programming language",
                    required=False
                )
            ]
        ),
        Prompt(
            name="summarize_document",
            description="Summarize a document with key points",
            arguments=[
                PromptArgument(
                    name="document_uri",
                    description="URI of document to summarize",
                    required=True
                ),
                PromptArgument(
                    name="max_points",
                    description="Maximum key points to extract",
                    required=False
                )
            ]
        )
    ]

@server.get_prompt()
async def get_prompt(name: str, arguments: dict):
    if name == "code_review":
        code = arguments["code"]
        language = arguments.get("language", "unknown")

        return {
            "description": f"Code review for {language}",
            "messages": [
                PromptMessage(
                    role="user",
                    content={
                        "type": "text",
                        "text": f"""Review this {language} code for:
1. Bugs and potential issues
2. Security vulnerabilities
3. Performance concerns
4. Best practice violations

Code:
```{language}
{code}
```

Provide specific, actionable feedback."""
                    }
                )
            ]
        }

    raise ValueError(f"Unknown prompt: {name}")
```

## Transport Protocols

### stdio (Default)

Used when the MCP server runs as a subprocess.

```json
// claude_desktop_config.json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_mcp_server"],
      "env": {
        "DATABASE_URL": "postgresql://..."
      }
    }
  }
}
```

### HTTP with SSE

For remote servers:

```python
from mcp.server.sse import SseServerTransport
from starlette.applications import Starlette
from starlette.routing import Route

sse = SseServerTransport("/messages")

async def handle_sse(request):
    async with sse.connect_sse(
        request.scope, request.receive, request._send
    ) as streams:
        await server.run(streams[0], streams[1])

app = Starlette(routes=[
    Route("/sse", endpoint=handle_sse),
    Route("/messages", endpoint=sse.handle_post_message, methods=["POST"])
])
```

## Server Patterns

### Database Integration

```python
import asyncpg

class DatabaseMCPServer:
    def __init__(self, database_url):
        self.database_url = database_url
        self.pool = None

    async def initialize(self):
        self.pool = await asyncpg.create_pool(self.database_url)

    @server.call_tool()
    async def call_tool(self, name: str, arguments: dict):
        if name == "query":
            # Validate query (prevent dangerous operations)
            query = arguments["query"]
            if self._is_dangerous_query(query):
                return [TextContent(
                    type="text",
                    text="Error: Query contains disallowed operations"
                )]

            async with self.pool.acquire() as conn:
                results = await conn.fetch(query)
                return [TextContent(
                    type="text",
                    text=self._format_results(results)
                )]

    def _is_dangerous_query(self, query):
        """Block destructive queries"""
        dangerous = ['DROP', 'DELETE', 'TRUNCATE', 'UPDATE', 'INSERT']
        query_upper = query.upper()
        return any(d in query_upper for d in dangerous)
```

### File System Access

```python
import os
from pathlib import Path

class FileSystemMCPServer:
    def __init__(self, allowed_paths):
        self.allowed_paths = [Path(p).resolve() for p in allowed_paths]

    def _validate_path(self, path_str):
        """Ensure path is within allowed directories"""
        path = Path(path_str).resolve()
        for allowed in self.allowed_paths:
            try:
                path.relative_to(allowed)
                return path
            except ValueError:
                continue
        raise PermissionError(f"Access denied: {path_str}")

    @server.list_resources()
    async def list_resources(self):
        resources = []
        for allowed_path in self.allowed_paths:
            for file in allowed_path.rglob("*"):
                if file.is_file():
                    resources.append(Resource(
                        uri=f"file://{file}",
                        name=file.name,
                        mimeType=self._get_mimetype(file)
                    ))
        return resources

    @server.read_resource()
    async def read_resource(self, uri: str):
        if uri.startswith("file://"):
            path = self._validate_path(uri[7:])
            return path.read_text()
        raise ValueError(f"Unknown URI scheme: {uri}")
```

### External API Integration

```python
import httpx

class APIIntegrationServer:
    def __init__(self, api_key):
        self.api_key = api_key  # allow-secret
        self.client = httpx.AsyncClient()

    @server.call_tool()
    async def call_tool(self, name: str, arguments: dict):
        if name == "fetch_weather":
            response = await self.client.get(
                "https://api.weather.com/current",
                params={"city": arguments["city"]},
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return [TextContent(type="text", text=response.text)]

        if name == "send_notification":
            response = await self.client.post(
                "https://api.notifications.com/send",
                json={
                    "to": arguments["recipient"],
                    "message": arguments["message"]
                },
                headers={"Authorization": f"Bearer {self.api_key}"}
            )
            return [TextContent(
                type="text",
                text=f"Notification sent: {response.json()['id']}"
            )]
```

## Security Considerations

### Input Validation

```python
from pydantic import BaseModel, validator

class QueryInput(BaseModel):
    query: str
    limit: int = 10

    @validator('query')
    def validate_query(cls, v):
        # Prevent SQL injection
        dangerous = [';', '--', '/*', '*/', 'DROP', 'DELETE']
        for d in dangerous:
            if d.lower() in v.lower():
                raise ValueError(f"Query contains disallowed pattern: {d}")
        return v

    @validator('limit')
    def validate_limit(cls, v):
        if v < 1 or v > 100:
            raise ValueError("Limit must be between 1 and 100")
        return v

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "search":
        # Validate input
        validated = QueryInput(**arguments)
        return await execute_search(validated.query, validated.limit)
```

### Rate Limiting

```python
from datetime import datetime, timedelta
from collections import defaultdict

class RateLimiter:
    def __init__(self, requests_per_minute=60):
        self.requests_per_minute = requests_per_minute
        self.requests = defaultdict(list)

    def check(self, client_id: str):
        now = datetime.now()
        cutoff = now - timedelta(minutes=1)

        # Clean old requests
        self.requests[client_id] = [
            t for t in self.requests[client_id] if t > cutoff
        ]

        if len(self.requests[client_id]) >= self.requests_per_minute:
            raise RateLimitError("Too many requests")

        self.requests[client_id].append(now)

rate_limiter = RateLimiter()

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    rate_limiter.check("default")  # Or use actual client ID
    # ... process request
```

### Authentication

```python
import os

class AuthenticatedServer:
    def __init__(self):
        self.api_key = os.environ.get("MCP_API_KEY")  # allow-secret
        if not self.api_key:
            raise ValueError("MCP_API_KEY not set")

    def authenticate(self, request_headers: dict):
        provided_key = request_headers.get("Authorization", "").replace("Bearer ", "")
        if not provided_key or provided_key != self.api_key:
            raise AuthenticationError("Invalid API key")
```

## Testing MCP Servers

```python
import pytest
from mcp.client import Client
from mcp.client.stdio import stdio_client

@pytest.fixture
async def mcp_client():
    """Create test client connected to server"""
    async with stdio_client(
        command="python",
        args=["-m", "my_mcp_server"]
    ) as (read, write):
        client = Client("test-client", "1.0.0")
        await client.connect(read, write)
        yield client

@pytest.mark.asyncio
async def test_list_tools(mcp_client):
    tools = await mcp_client.list_tools()
    assert len(tools) > 0
    assert any(t.name == "search_documents" for t in tools)

@pytest.mark.asyncio
async def test_call_tool(mcp_client):
    result = await mcp_client.call_tool(
        "search_documents",
        {"query": "test", "limit": 5}
    )
    assert result.content
    assert result.content[0].type == "text"
```

## References

- `references/mcp-specification.md` - Full MCP protocol specification
- `references/server-examples.md` - Complete server implementations
- `references/deployment-patterns.md` - Production deployment strategies
