---
name: mcp-setup
description: Set up and configure MCP (Model Context Protocol) servers with Claude Code. Use when the user wants to connect Claude Code to external tools, databases, APIs, or services via MCP. Handles HTTP, SSE, and stdio server configurations with proper authentication.
---

# MCP Setup Skill

This skill helps configure Model Context Protocol (MCP) servers to connect Claude Code to external tools, databases, and APIs.

## What is MCP?

MCP (Model Context Protocol) is an open-source standard for AI-tool integrations. MCP servers give Claude Code access to:
- Issue trackers (Jira, GitHub Issues)
- Monitoring tools (Sentry, Statsig)
- Databases (PostgreSQL, MySQL)
- Design tools (Figma)
- Communication (Slack, Gmail)
- And hundreds more

## Server Types

### 1. HTTP Servers (Recommended for remote)
Cloud-based services, most widely supported.

```bash
claude mcp add --transport http <name> <url>

# Example: Connect to Notion
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With Bearer token authentication
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

### 2. SSE Servers (Deprecated)
Use HTTP instead where available.

```bash
claude mcp add --transport sse <name> <url>

# Example: Connect to Asana
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

### 3. Stdio Servers (Local processes)
Run as local processes on your machine.

```bash
claude mcp add --transport stdio <name> <command> [args...]

# Example: Airtable server
claude mcp add --transport stdio airtable --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server

# Example: PostgreSQL database
claude mcp add --transport stdio db -- npx -y @bytebase/dbhub \
  --dsn "postgresql://user:pass@localhost:5432/mydb"
```

**Note**: The `--` separates Claude's flags from the server command.

## Configuration Scopes

| Scope | Storage | Use Case |
|-------|---------|----------|
| `local` | `~/.claude.json` (project path) | Personal, project-specific |
| `project` | `.mcp.json` in project root | Team-shared via git |
| `user` | `~/.claude.json` (global) | Personal across all projects |

```bash
# Add to specific scope
claude mcp add --transport http api --scope project https://api.example.com
```

## Management Commands

```bash
# List all configured servers
claude mcp list

# Get details for a specific server
claude mcp get <name>

# Remove a server
claude mcp remove <name>

# Check server status (in Claude Code)
/mcp
```

## Authentication

For OAuth 2.0 authentication:

1. Add the server: `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp`
2. In Claude Code, run: `/mcp`
3. Select "Authenticate" and follow browser prompts

## Plugin MCP Servers

Plugins can bundle MCP servers. Create `.mcp.json` at plugin root:

```json
{
  "mcpServers": {
    "plugin-server": {
      "command": "${CLAUDE_PLUGIN_ROOT}/servers/my-server",
      "args": ["--config", "${CLAUDE_PLUGIN_ROOT}/config.json"],
      "env": {
        "API_KEY": "${API_KEY}"
      }
    }
  }
}
```

Or inline in `plugin.json`:

```json
{
  "name": "my-plugin",
  "mcpServers": {
    "plugin-api": {
      "type": "http",
      "url": "https://api.example.com/mcp"
    }
  }
}
```

## Project Shared Configuration

For team-shared servers, create `.mcp.json` in project root:

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://api.githubcopilot.com/mcp/"
    },
    "database": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@bytebase/dbhub", "--dsn", "${DATABASE_URL}"]
    }
  }
}
```

### Environment Variable Expansion

Supported in `.mcp.json`:
- `${VAR}` - Value of environment variable
- `${VAR:-default}` - Value or default if not set

Works in: `command`, `args`, `env`, `url`, `headers`

## Popular MCP Servers

| Server | Type | Install Command |
|--------|------|-----------------|
| GitHub | HTTP | `claude mcp add --transport http github https://api.githubcopilot.com/mcp/` |
| Sentry | HTTP | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| Notion | HTTP | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| Postgres | stdio | `claude mcp add --transport stdio db -- npx -y @bytebase/dbhub --dsn "..."` |
| Filesystem | stdio | `claude mcp add --transport stdio fs -- npx -y @modelcontextprotocol/server-filesystem /path` |

## Using MCP in Claude Code

### Reference Resources
Type `@` to see available resources from MCP servers:
```
> Analyze @github:issue://123
```

### Execute Prompts
MCP prompts become slash commands:
```
> /mcp__github__list_prs
> /mcp__jira__create_issue "Bug title" high
```

## Troubleshooting

### Windows Users
Use `cmd /c` wrapper for npx:
```bash
claude mcp add --transport stdio my-server -- cmd /c npx -y @some/package
```

### Output Limits
Set `MAX_MCP_OUTPUT_TOKENS` for large outputs:
```bash
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

### Timeout Issues
Increase startup timeout:
```bash
MCP_TIMEOUT=10000 claude
```

## Setup Checklist

When setting up a new MCP server:

- [ ] Choose appropriate transport (HTTP for remote, stdio for local)
- [ ] Select correct scope (local/project/user)
- [ ] Configure authentication if required
- [ ] Set necessary environment variables
- [ ] Test with `/mcp` command
- [ ] Verify tools are available
