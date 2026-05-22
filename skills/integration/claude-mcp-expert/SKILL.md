---
name: claude-mcp-expert
description: Model Context Protocol (MCP) expert for Claude Code. Install, configure, and troubleshoot MCP servers. Covers HTTP, SSE, and stdio transports, authentication, popular integrations (Sentry, GitHub, Jira, Notion, databases). Triggers on MCP, Model Context Protocol, MCP server, installing MCP, connecting tools, webhooks, remote server.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
license: MIT
metadata:
  author: raintree
  version: "1.0"
---

# Claude Code MCP Expert

Connect Claude Code to external tools, databases, and services using Model Context Protocol (MCP).

## When to Use

- User wants to connect external services (GitHub, Jira, Sentry)
- User needs database access (PostgreSQL, MongoDB)
- User asks about MCP configuration or `.mcp.json`
- User has MCP connection or authentication issues

## What is MCP?

**Model Context Protocol (MCP)** is an open standard that connects AI agents to:
- External APIs (GitHub, Jira, Notion, Slack)
- Databases (PostgreSQL, MongoDB, MySQL)
- File systems (local, Google Drive)
- Custom integrations

## Quick Start

```bash
# Add an HTTP server
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Add an SSE server
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse

# Add a stdio server (npm package)
claude mcp add --transport stdio github -- npx -y @modelcontextprotocol/server-github

# Manage servers interactively
/mcp
```

## Transport Types

### HTTP (Most Common)
For cloud services with REST-like endpoints.

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
claude mcp add --transport http github https://api.github.com/mcp
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

### SSE (Server-Sent Events)
For streaming services.

```bash
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

### stdio (Local/NPM Packages)
For local tools or npm packages.

```bash
claude mcp add --transport stdio postgres \
  --env POSTGRES_CONNECTION_STRING="postgresql://user:pass@localhost:5432/db" \
  -- npx -y @modelcontextprotocol/server-postgres

claude mcp add --transport stdio filesystem \
  --env ALLOWED_DIRECTORIES="/path/to/dir" \
  -- npx -y @modelcontextprotocol/server-filesystem
```

## Popular Integrations

### Development Tools

| Service | Command |
|---------|---------|
| **Sentry** | `claude mcp add --transport http sentry https://mcp.sentry.dev/mcp` |
| **GitHub** | `claude mcp add --transport http github https://api.github.com/mcp` |
| **Socket** | `claude mcp add --transport http socket https://mcp.socket.dev/` |

### Project Management

| Service | Command |
|---------|---------|
| **Jira** | `claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse` |
| **Linear** | `claude mcp add --transport http linear https://mcp.linear.app/mcp` |
| **Notion** | `claude mcp add --transport http notion https://mcp.notion.com/mcp` |
| **Asana** | `claude mcp add --transport sse asana https://mcp.asana.com/sse` |

### Databases

```bash
# PostgreSQL
claude mcp add --transport stdio postgres \
  --env POSTGRES_CONNECTION_STRING="postgresql://localhost:5432/mydb" \
  -- npx -y @modelcontextprotocol/server-postgres

# MongoDB
claude mcp add --transport stdio mongodb \
  --env MONGODB_URI="mongodb://localhost:27017/mydb" \
  -- npx -y @modelcontextprotocol/server-mongodb
```

### Communication

```bash
# Slack
claude mcp add --transport stdio slack \
  --env SLACK_BOT_TOKEN=xoxb-your-token \
  --env SLACK_TEAM_ID=T1234567 \
  -- npx -y @modelcontextprotocol/server-slack

# Gmail
claude mcp add --transport stdio gmail \
  -- npx -y @modelcontextprotocol/server-gmail
```

## Configuration Files

### .mcp.json Structure

```json
{
  "mcpServers": {
    "server-name": {
      "transport": "http",
      "url": "https://mcp.service.com/mcp"
    },
    "database": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://localhost/db"
      }
    }
  }
}
```

### Configuration Scopes

| Scope | Location | Use Case |
|-------|----------|----------|
| **User** | `~/.claude/.mcp.json` | Personal tools, global |
| **Project** | `.claude/.mcp.json` | Team-shared, git committed |
| **Local** | `.claude/.mcp.local.json` | Personal overrides, not committed |

### Add with Scope

```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp --user     # Global
claude mcp add --transport http linear https://mcp.linear.app/mcp --project  # Team
claude mcp add --transport http notion https://mcp.notion.com/mcp --local    # Personal override
```

## Authentication

### OAuth (Recommended)
```bash
# Install server
claude mcp add --transport http github https://api.github.com/mcp

# Authenticate via /mcp command
/mcp
# Select: Authenticate with server
# Browser opens → authorize → done
```

### API Keys (Environment Variables)
```bash
claude mcp add --transport stdio server-name \
  --env API_KEY=your_api_key \
  -- npx -y package-name
```

### Via settings.json
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxx",
    "SENTRY_AUTH_TOKEN": "sntrys_xxxxx"
  }
}
```

## Using MCP Features

### MCP Tools
Once connected, use naturally:
```
"Check Sentry for errors in the last 24 hours"
"Create a PR for this feature on GitHub"
"List my assigned Jira tickets"
"Query the users table for active accounts"
```

### MCP Resources
Reference MCP-provided files:
```
Review @mcp://github/README.md and suggest improvements
```

### MCP Prompts as Commands
MCP prompts become slash commands:
```
/mcp__github__create_issue "Bug in login" high
/mcp__jira__update_status PROJ-123 "In Progress"
```

## Managing Servers

### Interactive Management
```bash
/mcp
# Options:
# - View all servers
# - Add new server
# - Remove server
# - Authenticate
# - View tools/prompts/resources
```

### Command Line
```bash
claude mcp list                    # List servers
claude mcp add ...                 # Add server
claude mcp remove server-name      # Remove server
```

## Troubleshooting

### Server Not Connecting

1. **Verify URL/command** - check for typos
2. **Check auth** - run `/mcp` → Authenticate
3. **Test network** - can you reach the URL?
4. **Debug mode** - run `claude --debug`

### Authentication Failing

1. Re-authenticate: `/mcp` → Clear auth → Re-authenticate
2. Check API key validity
3. Verify OAuth tokens not expired
4. Check permissions/scopes

### stdio Server Errors

```bash
# Test command manually
npx -y @modelcontextprotocol/server-postgres

# Check environment variables are set
echo $POSTGRES_CONNECTION_STRING

# Verify npm package exists
npm info @modelcontextprotocol/server-postgres
```

### Tools Not Available

1. Confirm server is connected: `/mcp`
2. Check authentication completed
3. Restart Claude Code
4. Verify server provides expected tools

## Security Best Practices

**DO:**
- Use OAuth when available
- Store secrets in settings.json, not .mcp.json
- Use project scope for team configs
- Review server permissions regularly

**DON'T:**
- Commit API keys to git
- Install untrusted servers
- Share OAuth tokens
- Use broad permissions unnecessarily

## Example Workflows

### Issue to PR
```bash
# Setup
claude mcp add --transport http github https://api.github.com/mcp
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse

# Usage
"Read JIRA ticket ENG-123, implement the feature, and create a PR on GitHub"
```

### Error Investigation
```bash
# Setup
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp

# Usage
"Check Sentry for errors in the last hour and fix them"
```

### Database Query to Report
```bash
# Setup
claude mcp add --transport stdio postgres \
  --env POSTGRES_CONNECTION_STRING="postgresql://localhost/analytics" \
  -- npx -y @modelcontextprotocol/server-postgres

# Usage
"Find users who signed up this month and summarize their activity"
```

## Resources

- **MCP Website:** https://modelcontextprotocol.io/
- **MCP Servers List:** https://github.com/modelcontextprotocol/servers
- **Claude Code MCP Docs:** https://docs.anthropic.com/en/docs/claude-code/mcp
