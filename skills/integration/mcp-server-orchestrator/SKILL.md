---
name: mcp-server-orchestrator
description: Configure, deploy, and troubleshoot Model Context Protocol (MCP) servers for AI agent workflows. Use when setting up MCP servers, debugging connection issues, managing multi-server configurations, integrating with Claude Desktop/Code/Cowork, or designing custom tool servers. Triggers on MCP configuration, tool server development, Claude integration issues, or agent infrastructure setup.
license: MIT
---

# MCP Server Orchestrator

Manage MCP server infrastructure for AI-powered development workflows.

## MCP Architecture Overview

```
┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
│   MCP Client    │────▶│   MCP Server     │────▶│  External APIs  │
│ (Claude, etc.)  │◀────│  (Tool Provider) │◀────│  (Services)     │
└─────────────────┘     └──────────────────┘     └─────────────────┘
         │                       │
         └───── JSON-RPC ────────┘
```

**Key concepts:**
- **Server**: Provides tools, resources, and prompts via MCP protocol
- **Client**: Consumes server capabilities (Claude Desktop, Claude Code, etc.)
- **Transport**: Communication layer (stdio, SSE, WebSocket)

## Configuration Locations

| Client | Config File | Platform |
|--------|------------|----------|
| Claude Desktop | `claude_desktop_config.json` | macOS: `~/Library/Application Support/Claude/` |
| | | Windows: `%APPDATA%\Claude\` |
| Claude Code | `settings.json` or MCP config | Project-level or user settings |
| Cline | `cline_mcp_settings.json` | VS Code extension settings |

## Server Configuration Schema

```json
{
  "mcpServers": {
    "server-name": {
      "command": "executable",
      "args": ["arg1", "arg2"],
      "env": {
        "API_KEY": "value"
      },
      "disabled": false
    }
  }
}
```

### Common Server Types

**Python Server (uvx)**:
```json
{
  "my-python-server": {
    "command": "uvx",
    "args": ["--from", "package-name", "server-command"]
  }
}
```

**Node Server (npx)**:
```json
{
  "my-node-server": {
    "command": "npx",
    "args": ["-y", "@scope/package-name"]
  }
}
```

**Local Development Server**:
```json
{
  "dev-server": {
    "command": "python",
    "args": ["-m", "my_server"],
    "env": {
      "DEBUG": "true"
    }
  }
}
```

## Troubleshooting Workflow

### Connection Issues

1. **Verify server starts independently**:
   ```bash
   # Test Python server
   python -m my_server
   
   # Test Node server
   npx -y @scope/package-name
   ```

2. **Check logs**:
   - Claude Desktop: `~/Library/Logs/Claude/mcp*.log`
   - Look for JSON-RPC errors, connection timeouts

3. **Validate JSON config**:
   ```bash
   python -c "import json; json.load(open('config.json'))"
   ```

4. **Common fixes**:
   - Use absolute paths for commands
   - Ensure dependencies installed in correct environment
   - Check API keys/env vars are set
   - Restart client after config changes

### Authentication Issues

1. **OAuth flows**: Ensure redirect URIs configured correctly
2. **API keys**: Verify env vars accessible to server process
3. **Token refresh**: Check token storage location and permissions

## Building Custom Servers

### Python Server (FastMCP)

```python
from fastmcp import FastMCP

mcp = FastMCP("my-server")

@mcp.tool()
def my_tool(param: str) -> str:
    """Tool description for the AI."""
    return f"Result: {param}"

@mcp.resource("resource://my-data")
def get_data() -> str:
    """Provide data as a resource."""
    return "Resource content"

if __name__ == "__main__":
    mcp.run()
```

### Node Server (MCP SDK)

```typescript
import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";

const server = new Server({ name: "my-server", version: "1.0.0" }, {
  capabilities: { tools: {} }
});

server.setRequestHandler(ListToolsRequestSchema, async () => ({
  tools: [{
    name: "my_tool",
    description: "Tool description",
    inputSchema: { type: "object", properties: { param: { type: "string" } } }
  }]
}));

const transport = new StdioServerTransport();
await server.connect(transport);
```

## Multi-Server Orchestration

### Modular Architecture

Organize servers by domain:

```json
{
  "mcpServers": {
    "filesystem": { "command": "...", "args": ["--allowed-dirs", "/projects"] },
    "database": { "command": "...", "env": { "DB_URL": "..." } },
    "api-integrations": { "command": "...", "env": { "API_KEYS": "..." } },
    "custom-tools": { "command": "python", "args": ["-m", "my_tools"] }
  }
}
```

### Server Selection Strategy

Think of servers as modules in a synthesizer—patch them together based on workflow needs:

- **Development workflow**: filesystem + git + code-analysis servers
- **Research workflow**: web-search + document + note-taking servers
- **Data workflow**: database + visualization + export servers

## Performance Optimization

- **Lazy loading**: Only enable servers needed for current task
- **Caching**: Implement response caching for expensive operations
- **Timeout tuning**: Adjust timeouts for slow external APIs
- **Connection pooling**: Reuse connections in database servers

## References

- `references/server-templates.md` - Boilerplate for common server types
- `references/debugging-guide.md` - Detailed troubleshooting procedures
