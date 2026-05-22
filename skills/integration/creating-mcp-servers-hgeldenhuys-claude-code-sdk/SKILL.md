---
name: creating-mcp-servers
description: Guide for creating and integrating MCP (Model Context Protocol) servers with Claude Code. Use when building external tool integrations, connecting to databases, creating custom capabilities, or adding API wrappers. Covers transports, OAuth, configuration, and troubleshooting.
allowed-tools: ["Read", "Write", "Bash", "Glob"]
---

# Creating MCP Servers

Build and integrate MCP (Model Context Protocol) servers to extend Claude Code with external tools, databases, and APIs.

## Quick Reference

| Concept | Description |
|---------|-------------|
| **MCP** | Model Context Protocol - open standard for AI-tool integrations |
| **Transport** | How Claude Code connects: HTTP (recommended), SSE (deprecated), stdio (local) |
| **Scope** | Where config lives: `local`, `project`, `user` |
| **Tool Naming** | `mcp__<server>__<tool>` pattern |

## What MCP Provides

MCP servers expose three primitives to Claude Code:

| Primitive | Description | Example |
|-----------|-------------|---------|
| **Tools** | Callable functions | `search_repos`, `query_database`, `send_email` |
| **Resources** | Data sources (@ mentionable) | `@github:issue://123`, `@postgres:schema://users` |
| **Prompts** | Reusable prompt templates | `/mcp__github__pr_review 456` |

## Adding MCP Servers

### HTTP Transport (Recommended)

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Example: Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With authentication header
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### stdio Transport (Local Servers)

```bash
# Basic syntax
claude mcp add --transport stdio <name> -- <command> [args...]

# Example: Database server
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@host:5432/db"

# With environment variables
claude mcp add --transport stdio --env API_KEY=xxx myserver -- npx -y my-package
```

### SSE Transport (Deprecated)

```bash
# Use HTTP instead when available
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

## Configuration Scopes

| Scope | Flag | Storage | Use Case |
|-------|------|---------|----------|
| `local` | (default) | `~/.claude.json` | Personal, per-project |
| `project` | `--scope project` | `.mcp.json` | Team-shared, version controlled |
| `user` | `--scope user` | `~/.claude.json` | Personal, all projects |

### Project Scope Example

```bash
claude mcp add --transport http github --scope project https://api.githubcopilot.com/mcp/
```

Creates `.mcp.json`:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    }
  }
}
```

## Managing Servers

```bash
# List all servers
claude mcp list

# Get server details
claude mcp get <name>

# Remove server
claude mcp remove <name>

# Check status in Claude Code
/mcp

# Import from Claude Desktop
claude mcp add-from-claude-desktop
```

### Enable/Disable Servers (2.1.6+)

Use `/mcp` command to enable or disable servers:

```bash
# In Claude Code
/mcp enable <server-name>
/mcp disable <server-name>
```

**Note:** As of 2.1.6, @-mentioning MCP servers to enable/disable them is no longer supported. Use `/mcp enable <name>` instead.

## OAuth Authentication

Many cloud MCP servers require OAuth:

1. Add the server: `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`
2. In Claude Code, run: `/mcp`
3. Select "Authenticate" and complete browser flow
4. Tokens refresh automatically

## Environment Variables

### In .mcp.json

```json
{
  "mcpServers": {
    "api-server": {
      "type": "http",
      "url": "${API_BASE_URL:-https://api.example.com}/mcp",
      "headers": {
        "Authorization": "Bearer ${API_KEY}"
      }
    }
  }
}
```

Supported syntax:
- `${VAR}` - Required variable
- `${VAR:-default}` - With default value

### Configuration Environment Variables

| Variable | Description |
|----------|-------------|
| `MCP_TIMEOUT` | Startup timeout in ms (e.g., `MCP_TIMEOUT=10000 claude`) |
| `MAX_MCP_OUTPUT_TOKENS` | Max output tokens (default: 25000) |

## Using Claude Code as MCP Server

Expose Claude Code tools to other applications:

```bash
claude mcp serve
```

Claude Desktop configuration:

```json
{
  "mcpServers": {
    "claude-code": {
      "type": "stdio",
      "command": "claude",
      "args": ["mcp", "serve"],
      "env": {}
    }
  }
}
```

## Tool Naming Convention

MCP tools follow the pattern: `mcp__<server>__<tool>`

Examples:
- `mcp__github__search_repositories`
- `mcp__sentry__get_issues`
- `mcp__db__query`

### Wildcard Permissions

```json
{
  "permissions": {
    "allow": ["mcp__github__*"],
    "deny": ["mcp__dangerous__*"]
  }
}
```

## Resources and Prompts

### Using Resources (@ mentions)

```
> Analyze @github:issue://123 and suggest a fix
> Compare @postgres:schema://users with @docs:file://database/user-model
```

### Using Prompts (slash commands)

```
> /mcp__github__list_prs
> /mcp__github__pr_review 456
> /mcp__jira__create_issue "Bug in login" high
```

## Plugin-Bundled MCP Servers

Plugins can include MCP servers:

```json
// plugin.json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/api-server",
      "args": ["--port", "8080"]
    }
  }
}
```

Or in `.mcp.json` at plugin root:

```json
{
  "database-tools": {
    "command": "${CLAUDE_PLUGIN_ROOT}/servers/db-server",
    "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"]
  }
}
```

## list_changed Notifications (2.1.0+)

MCP servers can dynamically update their tools, prompts, and resources without requiring reconnection. Claude Code automatically handles `list_changed` notifications.

## Enterprise: Managed MCP

### Option 1: Exclusive Control

Deploy `managed-mcp.json` to system directory:

- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux/WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\Program Files\ClaudeCode\managed-mcp.json`

### Option 2: Allowlists/Denylists

In managed settings:

```json
{
  "allowedMcpServers": [
    { "serverName": "github" },
    { "serverUrl": "https://mcp.company.com/*" },
    { "serverCommand": ["npx", "-y", "approved-package"] }
  ],
  "deniedMcpServers": [
    { "serverUrl": "https://*.untrusted.com/*" }
  ]
}
```

## Workflow: Add MCP Server

### Prerequisites
- [ ] Identify server type (HTTP, stdio, SSE)
- [ ] Have authentication credentials ready
- [ ] Decide on scope (local, project, user)

### Steps

1. **Add Server**
   - [ ] Run appropriate `claude mcp add` command
   - [ ] Include `--scope project` if team-shared

2. **Authenticate (if OAuth)**
   - [ ] Run `/mcp` in Claude Code
   - [ ] Complete browser authentication flow

3. **Test**
   - [ ] Run `/mcp` to verify connection
   - [ ] Try a simple tool call

### Validation
- [ ] Server appears in `claude mcp list`
- [ ] `/mcp` shows "Connected"
- [ ] Tools visible in autocomplete

## Workflow: Build MCP Server

### Prerequisites
- [ ] Node.js or Python environment
- [ ] MCP SDK installed

### Steps

1. **Choose SDK**
   - [ ] TypeScript: `npm install @modelcontextprotocol/sdk`
   - [ ] Python: `pip install mcp`

2. **Implement Server**
   - [ ] Define tools, resources, or prompts
   - [ ] Handle authentication
   - [ ] Return structured responses

3. **Test Locally**
   - [ ] Add with stdio transport
   - [ ] Verify tools work

4. **Deploy (Optional)**
   - [ ] Host as HTTP endpoint
   - [ ] Configure OAuth if needed

See [EXAMPLES.md](./EXAMPLES.md) for implementation patterns.

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Options after server name | Put `--transport`, `--env`, `--scope` BEFORE name |
| Windows npx issues | Use `cmd /c npx ...` wrapper |
| Server not connecting | Check `/mcp` status, verify URL |
| Tools not appearing | Restart Claude Code after adding server |
| OAuth expired | Re-authenticate via `/mcp` |

## Reference Files

| File | Contents |
|------|----------|
| [TRANSPORTS.md](./TRANSPORTS.md) | Detailed transport documentation |
| [EXAMPLES.md](./EXAMPLES.md) | Example MCP server implementations |
| [TROUBLESHOOTING.md](./TROUBLESHOOTING.md) | Common issues and solutions |

## External Resources

- [MCP Protocol](https://modelcontextprotocol.io/introduction)
- [MCP SDK Quickstart](https://modelcontextprotocol.io/quickstart/server)
- [MCP Server Registry](https://github.com/modelcontextprotocol/servers)
- [Claude Code MCP Docs](https://code.claude.com/docs/en/mcp)
