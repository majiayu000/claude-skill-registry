---
name: mcp-server-scaffolding-asyncio
version: "1.0"
description: >
  Use asyncio.TaskGroup() instead of asyncio.gather() for Python 3.13 MCP servers.
  PROACTIVELY activate for: (1) creating new MCP servers, (2) async server patterns, (3) Python 3.13 asyncio.
  Triggers: "mcp server", "asyncio taskgroup", "server scaffolding"
core-integration:
  techniques:
    primary: ["structured_decomposition"]
    secondary: []
  contracts:
    input: "none"
    output: "none"
  patterns: "none"
  rubrics: "none"
---

# MCP Server Scaffolding with Asyncio Skill

## Metadata (Tier 1)

**Keywords**: mcp server, asyncio, taskgroup, async server, python 3.13

**File Patterns**: **/server.py, **/main.py

**Modes**: backend_python

---

## Instructions (Tier 2)

### Python 3.13 Asyncio Patterns

**CRITICAL**: Use `asyncio.TaskGroup()` instead of `asyncio.gather()` for Python 3.13.

```python
# ❌ OLD PATTERN (Python 3.10)
results = await asyncio.gather(task1(), task2())

# ✅ NEW PATTERN (Python 3.13)
async with asyncio.TaskGroup() as tg:
    t1 = tg.create_task(task1())
    t2 = tg.create_task(task2())
results = [t1.result(), t2.result()]
```

### Server Scaffolding Template

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server
import asyncio
from typing import Any

# Initialize server
server = Server("my-mcp-server")

@server.list_tools()
async def list_tools() -> list[dict[str, Any]]:
    """Return available tools with schemas."""
    return [
        {
            "name": "example_tool",
            "description": "Example tool description",
            "inputSchema": ExampleInput.model_json_schema()
        }
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict) -> dict[str, Any]:
    """Execute requested tool."""
    if name == "example_tool":
        # Pydantic validates input
        input_data = ExampleInput(**arguments)
        result = await execute_example(input_data)
        return result.model_dump()

    raise ValueError(f"Unknown tool: {name}")

async def main():
    """Run MCP server via stdio transport."""
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### Project Structure

```
mcp_server_project/
├── pyproject.toml           # Dependencies
├── server.py                # Main server
├── tools/
│   ├── __init__.py
│   ├── schemas.py          # Pydantic models
│   └── handlers.py         # Tool implementations
├── resources/
│   ├── __init__.py
│   └── providers.py        # Resource handlers
└── tests/
    ├── test_protocol.py
    └── test_tools.py
```

### Dependencies (pyproject.toml)

```toml
[project]
name = "my-mcp-server"
version = "1.0.0"
requires-python = ">=3.13"

dependencies = [
    "mcp>=1.0.0",
    "pydantic>=2.0.0",
    "aiofiles>=24.0.0"
]

[project.optional-dependencies]
dev = [
    "pytest>=8.0.0",
    "pytest-asyncio>=0.23.0",
    "pytest-cov>=4.0.0",
    "ruff>=0.1.0",
    "mypy>=1.8.0"
]
```

### Async Context Managers

```python
class DatabaseConnection:
    """Async context manager for database."""

    async def __aenter__(self):
        self.conn = await connect_db()
        return self.conn

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.conn.close()

# Usage in tool
async def execute_query_tool(query: str):
    async with DatabaseConnection() as db:
        result = await db.execute(query)
        return result
```

### Error Handling

```python
from mcp.types import McpError

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    try:
        if name == "risky_operation":
            input_data = RiskyInput(**arguments)
            return await risky_operation(input_data)
    except ValidationError as e:
        # Pydantic validation failed
        raise McpError(
            code=-32602,  # Invalid params
            message=f"Validation error: {str(e)}"
        )
    except Exception as e:
        # Unexpected error
        raise McpError(
            code=-32603,  # Internal error
            message=f"Tool execution failed: {str(e)}"
        )
```

### Async Resource Reading

```python
import aiofiles

@server.read_resource()
async def read_resource(uri: str) -> dict[str, Any]:
    """Read resource content asynchronously."""
    if not uri.startswith("file:///"):
        raise ValueError(f"Unsupported URI: {uri}")

    path = uri.removeprefix("file://")

    # Async file reading
    async with aiofiles.open(path, "r") as f:
        content = await f.read()

    return {
        "contents": [
            {
                "uri": uri,
                "text": content,
                "mimeType": "text/plain"
            }
        ]
    }
```

### Running the Server

**Development**:
```bash
python server.py
```

**Claude Desktop Integration** (claude_desktop_config.json):
```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["/path/to/server.py"]
    }
  }
}
```

### Anti-Patterns

❌ Using `asyncio.gather()` (outdated for Python 3.13)
❌ Blocking I/O in async functions (use aiofiles, httpx, etc.)
❌ Missing async context manager cleanup
❌ No error handling in tool execution

---

## Resources (Tier 3)

**Python Asyncio Docs**: https://docs.python.org/3.13/library/asyncio.html
**MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
**TaskGroup Guide**: https://docs.python.org/3.13/library/asyncio-task.html#task-groups
