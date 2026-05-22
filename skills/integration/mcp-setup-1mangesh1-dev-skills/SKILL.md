---
name: mcp-setup
description: Model Context Protocol (MCP) server setup and integration for Claude and AI agents. Use when user asks to "setup MCP", "configure MCP server", "add MCP tools", "connect to MCP", "create MCP server", or integrate external tools via MCP protocol.
---

# MCP Setup

Configure Model Context Protocol servers for Claude and AI agent integrations.

## Claude Desktop Configuration

### Config Location

```
macOS: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
Linux: ~/.config/Claude/claude_desktop_config.json
```

### Basic Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/allowed/dir"]
    },
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxx"
      }
    }
  }
}
```

## Popular MCP Servers

### Filesystem

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem", "/Users/me/projects"]
  }
}
```

### GitHub

```json
{
  "github": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-github"],
    "env": {
      "GITHUB_PERSONAL_ACCESS_TOKEN": "ghp_xxxx"
    }
  }
}
```

### PostgreSQL

```json
{
  "postgres": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-postgres", "postgresql://user:pass@localhost/db"]
  }
}
```

### SQLite

```json
{
  "sqlite": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-sqlite", "--db-path", "/path/to/db.sqlite"]
  }
}
```

### Brave Search

```json
{
  "brave-search": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-brave-search"],
    "env": {
      "BRAVE_API_KEY": "your-api-key"
    }
  }
}
```

### Slack

```json
{
  "slack": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-slack"],
    "env": {
      "SLACK_BOT_TOKEN": "xoxb-xxxx",
      "SLACK_TEAM_ID": "T12345"
    }
  }
}
```

## Custom MCP Server (Python)

### Basic Structure

```python
#!/usr/bin/env python3
from mcp.server import Server
from mcp.types import Tool, TextContent

server = Server("my-server")

@server.list_tools()
async def list_tools():
    return [
        Tool(
            name="my_tool",
            description="Does something useful",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {"type": "string", "description": "Input query"}
                },
                "required": ["query"]
            }
        )
    ]

@server.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "my_tool":
        result = process(arguments["query"])
        return [TextContent(type="text", text=result)]

if __name__ == "__main__":
    import asyncio
    asyncio.run(server.run())
```

### Config for Custom Server

```json
{
  "my-custom-server": {
    "command": "python",
    "args": ["/path/to/my_server.py"]
  }
}
```

## Custom MCP Server (TypeScript)

### Setup

```bash
npm init -y
npm install @modelcontextprotocol/sdk
```

### Basic Server

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({
  name: "my-server",
  version: "1.0.0"
}, {
  capabilities: { tools: {} }
});

server.setRequestHandler("tools/list", async () => ({
  tools: [{
    name: "my_tool",
    description: "Does something",
    inputSchema: {
      type: "object",
      properties: { query: { type: "string" } },
      required: ["query"]
    }
  }]
}));

server.setRequestHandler("tools/call", async (request) => {
  if (request.params.name === "my_tool") {
    return { content: [{ type: "text", text: "Result" }] };
  }
});

new StdioServerTransport().connect(server);
```

## Debugging

### Test Server Manually

```bash
# Run server directly
npx -y @modelcontextprotocol/server-filesystem /tmp

# Check logs (Claude Desktop)
tail -f ~/Library/Logs/Claude/mcp*.log
```

### Common Issues

1. **Server not starting**: Check command path and permissions
2. **Auth errors**: Verify env variables are set
3. **Timeout**: Server may be slow to initialize
4. **Path issues**: Use absolute paths

## Reference

Full server list and advanced configuration: `references/servers.md`
