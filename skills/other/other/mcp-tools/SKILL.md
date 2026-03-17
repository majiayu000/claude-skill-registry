---
name: mcp-tools
description: Create MCP server tools with Official Python MCP SDK for AI agents. Use when building MCP tools, registering tool schemas, or creating AI-accessible functions.
---

# MCP Tools Development (Official SDK)

## Tool Registration
```python
from mcp.server import Server
from mcp.types import Tool, TextContent
import mcp.server.stdio

server = Server("mcp-server")

@server.list_tools()
async def list_tools() -> list[Tool]:
    return [
        Tool(
            name="tool_name",
            description="What this tool does",
            inputSchema={
                "type": "object",
                "properties": {
                    "user_id": {"type": "string"},
                    "param": {"type": "string", "maxLength": 200}
                },
                "required": ["user_id", "param"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    if name == "tool_name":
        # Validate inputs
        if not arguments.get("user_id"):
            return [TextContent(type="text", text='{"error": "user_id required"}')]
        
        # Stateless: create DB session per call
        async with get_db_session() as session:
            # Do work
            result = {"status": "success", "data": {}}
            return [TextContent(type="text", text=json.dumps(result))]
```

## Server Startup
```python
async def main():
    async with mcp.server.stdio.stdio_server() as (read_stream, write_stream):
        await server.run(read_stream, write_stream, server.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Key Rules
- Stateless tools (no global state)
- DB session per tool call
- Return exact JSON schemas
- Input validation before operations
- User isolation (filter by user_id)