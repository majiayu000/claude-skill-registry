---
name: mcp-tools
description: "Expert guidance for the Model Context Protocol (MCP) - connect AI agents to external tools, services, and data sources. Use when working with: (1) Building MCP servers to expose tools, resources, and prompts, (2) Integrating MCP clients with AI applications, (3) Protocol transports (stdio, HTTP SSE), (4) Tool execution and resource management, (5) JSON-RPC message handling, (6) Server-client architecture, (7) Production deployments. Supports Python SDK with async patterns."
---

# Model Context Protocol (MCP)

Connect AI agents to external tools, services, and data sources using the open Model Context Protocol.

## What is MCP?

Model Context Protocol is an **open protocol** that standardizes how AI applications connect to external data sources and tools. It provides a uniform way to:

- **Expose Tools** - Functions that AI agents can call
- **Share Resources** - Data and context for LLMs (files, databases, APIs)
- **Provide Prompts** - Reusable prompt templates
- **Enable Integration** - Connect any data source or service to any AI application

### Architecture

```
┌─────────────────┐        MCP Protocol         ┌─────────────────┐
│                 │◄──────────────────────────►│                 │
│  MCP Client     │     JSON-RPC Messages       │   MCP Server    │
│  (AI App/LLM)   │                             │  (Tools/Data)   │
│                 │                             │                 │
└─────────────────┘                             └─────────────────┘
        │                                                │
        │                                                │
    Uses tools,                                    Exposes:
    reads resources,                               - Tools
    gets prompts                                   - Resources
                                                   - Prompts
```

**Client** - AI application that needs tools and context (Claude Desktop, custom apps)
**Server** - Provides specific capabilities (filesystem access, database queries, API integration)
**Protocol** - JSON-RPC 2.0 messages over stdio or HTTP

## Quick Start

### Install MCP Python SDK

```bash
pip install mcp
```

### Build Your First MCP Server

```python
from mcp.server.mcpserver import MCPServer

# Create server
mcp = MCPServer("My First Server")

# Add a tool
@mcp.tool()
def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

# Add a resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"

# Add a prompt
@mcp.prompt()
def code_review(code: str) -> str:
    """Generate code review prompt"""
    return f"Please review this code:\n{code}"

# Run server
if __name__ == "__main__":
    mcp.run(transport="stdio")
```

### Connect a Client

```python
import asyncio
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

async def main():
    server_params = StdioServerParameters(
        command="python",
        args=["my_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # Call a tool
            result = await session.call_tool("add", {"a": 5, "b": 3})
            print(result.content[0].text)  # "8"

            # Read a resource
            content = await session.read_resource("greeting://Alice")
            print(content.contents[0].text)  # "Hello, Alice!"

asyncio.run(main())
```

## Core Concepts

### 1. Tools

Functions that AI agents can execute:

```python
@mcp.tool()
def search_database(query: str, limit: int = 10) -> list[dict]:
    """Search the database.

    Args:
        query: Search query string
        limit: Maximum results to return
    """
    # Implementation
    results = db.search(query, limit=limit)
    return results
```

**Features:**
- Auto-generated JSON Schema from type hints
- Structured input/output
- Async support
- Progress reporting

### 2. Resources

Data and context for LLMs:

```python
@mcp.resource("file://{path}")
def read_file(path: str) -> str:
    """Read file contents."""
    with open(path) as f:
        return f.read()

# Dynamic resources with URI templates
@mcp.resource("user://{user_id}/profile")
def get_user_profile(user_id: str) -> dict:
    """Get user profile data."""
    return db.get_user(user_id)
```

**Use cases:**
- File contents
- Database schemas
- API documentation
- Application state

### 3. Prompts

Reusable prompt templates:

```python
@mcp.prompt()
def analyze_logs(log_file: str, error_type: str = "all") -> str:
    """Generate log analysis prompt.

    Args:
        log_file: Path to log file
        error_type: Type of errors to focus on
    """
    return f"""Analyze the logs in {log_file}.
Focus on: {error_type}
Provide:
1. Error summary
2. Root causes
3. Recommendations"""
```

## Transport Mechanisms

MCP supports multiple transport layers:

### stdio (Standard Input/Output)

**Best for:** Local processes, development, Claude Desktop integration

**Server:**
```python
mcp.run(transport="stdio")
```

**Client:**
```python
server_params = StdioServerParameters(
    command="python",
    args=["server.py"],
    env={"DEBUG": "true"}
)

async with stdio_client(server_params) as (read, write):
    async with ClientSession(read, write) as session:
        # Use session...
```

### HTTP with Server-Sent Events (SSE)

**Best for:** Remote servers, web applications, production deployments

**Server:**
```python
mcp.run(
    transport="streamable-http",
    stateless_http=True,
    json_response=True
)
```

**Features:**
- Bidirectional communication
- Server-to-client notifications
- Resumable connections
- Multiple concurrent clients

For detailed transport patterns, see [references/transports.md](references/transports.md).

## Server Development

### High-Level API (Recommended)

Use `MCPServer` with decorators:

```python
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("Demo Server", version="1.0.0")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description"""
    return f"Result: {param}"

@mcp.resource("resource://uri")
def my_resource() -> str:
    """Resource description"""
    return "Resource content"

@mcp.prompt()
def my_prompt(arg: str) -> str:
    """Prompt description"""
    return f"Prompt: {arg}"

mcp.run(transport="stdio")
```

For comprehensive server patterns, see [references/servers.md](references/servers.md).

## Client Integration

```python
import asyncio
from mcp import ClientSession, StdioServerParameters, types
from mcp.client.stdio import stdio_client

async def use_mcp_server():
    server_params = StdioServerParameters(
        command="python",
        args=["my_server.py"]
    )

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize
            await session.initialize()

            # List available tools
            tools = await session.list_tools()

            # Call a tool
            result = await session.call_tool("add", {"a": 5, "b": 3})

            # Read resource
            content = await session.read_resource("greeting://World")
```

For detailed client patterns, see [references/clients.md](references/clients.md).

## Advanced Features

### Progress Reporting

```python
from mcp.server.mcpserver import Context

@mcp.tool()
async def long_task(ctx: Context, steps: int = 10) -> str:
    """Long running task with progress."""
    for i in range(steps):
        await ctx.report_progress(
            progress=(i + 1) / steps,
            total=1.0,
            message=f"Step {i + 1}/{steps}"
        )
    return "Complete"
```

### Logging

```python
@mcp.tool()
async def process_data(data: str, ctx: Context) -> str:
    """Process data with logging."""
    await ctx.debug(f"Processing: {data}")
    await ctx.info("Starting processing")
    await ctx.warning("This is experimental")
    return f"Processed: {data}"
```

### Error Handling

```python
from mcp.shared.exceptions import MCPError

try:
    result = await session.call_tool("my_tool", args)
except MCPError as e:
    print(f"MCP error: {e.message}")
```

## Reference Documentation

- **[servers.md](references/servers.md)** - Comprehensive server development guide
- **[clients.md](references/clients.md)** - Client integration patterns
- **[transports.md](references/transports.md)** - Transport mechanisms
- **[core-concepts.md](references/core-concepts.md)** - Protocol architecture

## Starter Templates

Ready-to-use templates in `assets/`:
- **hello-world-server/** - Minimal MCP server
- **full-server/** - Complete server with all features
- **client-integration/** - Client examples

## Best Practices

1. **Use type hints** - Enables automatic JSON Schema generation
2. **Write clear descriptions** - Docstrings become tool descriptions
3. **Start with stdio** - Easier development and debugging
4. **Handle errors gracefully** - Use MCPError
5. **Report progress** - For long-running operations
6. **Log appropriately** - Use debug/info/warning/error
7. **Test thoroughly** - Test tools, resources, prompts independently
8. **Version your server** - Include version in constructor
