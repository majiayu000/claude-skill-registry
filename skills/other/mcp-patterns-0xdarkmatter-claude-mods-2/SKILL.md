---
name: mcp-patterns
description: "Model Context Protocol (MCP) server patterns for building integrations with Claude Code. Triggers on: mcp server, model context protocol, tool handler, mcp resource, mcp tool."
compatibility: "Requires Python 3.10+ or Node.js 18+ for MCP server development."
allowed-tools: "Read Write Bash"
depends-on: []
related-skills: [claude-code-hooks, claude-code-debug]
---

# MCP Patterns

Model Context Protocol (MCP) server patterns for building integrations with Claude Code.

## Basic MCP Server (Python)

```python
from mcp.server import Server
from mcp.server.stdio import stdio_server

app = Server("my-server")

@app.list_tools()
async def list_tools():
    return [
        {
            "name": "my_tool",
            "description": "Does something useful",
            "inputSchema": {
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Search query"}
                },
                "required": ["query"]
            }
        }
    ]

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        result = await do_something(arguments["query"])
        return {"content": [{"type": "text", "text": result}]}
    raise ValueError(f"Unknown tool: {name}")

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
```

## Project Layout

```
my-mcp-server/
├── src/
│   └── my_server/
│       ├── __init__.py
│       ├── server.py       # Main server logic
│       ├── tools.py        # Tool handlers
│       └── resources.py    # Resource handlers
├── pyproject.toml
└── README.md
```

## Claude Desktop Configuration

### Basic Configuration

```json
{
  "mcpServers": {
    "my-server": {
      "command": "python",
      "args": ["-m", "my_server"],
      "env": {
        "MY_API_KEY": "your-key-here"
      }
    }
  }
}
```

### With uv (Recommended)

```json
{
  "mcpServers": {
    "my-server": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/my-server", "python", "-m", "my_server"],
      "env": {
        "MY_API_KEY": "your-key-here"
      }
    }
  }
}
```

## Quick Reference

| Pattern | Use Case | Reference |
|---------|----------|-----------|
| Tool validation | Input sanitization with Pydantic | `./references/tool-patterns.md` |
| Error handling | Graceful failure responses | `./references/tool-patterns.md` |
| Multiple tools | CRUD-style tool registration | `./references/tool-patterns.md` |
| Static resources | Config/settings exposure | `./references/resource-patterns.md` |
| Dynamic resources | Database-backed resources | `./references/resource-patterns.md` |
| Environment auth | API key from env vars | `./references/auth-patterns.md` |
| OAuth tokens | Token refresh with TTL | `./references/auth-patterns.md` |
| SQLite cache | Persistent state storage | `./references/state-patterns.md` |
| In-memory cache | TTL-based caching | `./references/state-patterns.md` |
| Manual testing | Quick validation script | `./references/testing-patterns.md` |
| pytest async | Unit tests for tools | `./references/testing-patterns.md` |

## Common Issues

| Issue | Solution |
|-------|----------|
| Server not starting | Check `command` path, ensure dependencies installed |
| Tool not appearing | Verify `list_tools()` returns valid schema |
| Auth failures | Check env vars are set in config, not shell |
| Timeout errors | Add timeout to httpx calls, use async properly |
| JSON parse errors | Ensure `call_tool` returns proper content structure |

## Official Documentation

- https://modelcontextprotocol.io - MCP specification
- https://modelcontextprotocol.io/docs/concepts/tools - Tools reference
- https://modelcontextprotocol.io/docs/concepts/resources - Resources reference
- https://github.com/modelcontextprotocol/python-sdk - Python SDK
- https://github.com/modelcontextprotocol/servers - Official MCP servers

## Additional Resources

For detailed patterns, load:

- `./references/tool-patterns.md` - Validation, error handling, multi-tool registration
- `./references/resource-patterns.md` - Static and dynamic resource exposure
- `./references/auth-patterns.md` - Environment variables, OAuth token refresh
- `./references/state-patterns.md` - SQLite persistence, in-memory caching
- `./references/testing-patterns.md` - Manual test scripts, pytest async patterns
