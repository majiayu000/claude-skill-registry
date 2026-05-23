---
name: mcp-server-manager
description: Configure and manage MCP (Model Context Protocol) servers in Claude Code CLI. Use this skill when adding, removing, listing, or troubleshooting MCP servers, or when questions arise about MCP configuration, transport types, scopes, or authentication. Essential for connecting Claude Code to external tools, databases, and APIs.
---

# MCP Server Manager

## Overview

MCP (Model Context Protocol) servers connect Claude Code to external tools, databases, and APIs. This skill provides guidance for installing, configuring, and managing MCP servers using the `claude mcp` command-line interface.

## Quick Reference

### Essential Commands

List all configured MCP servers:
```bash
claude mcp list
```

Get details about a specific server:
```bash
claude mcp get <server-name>
```

Remove a server:
```bash
claude mcp remove <server-name>
```

Check server status (from within Claude Code):
```
/mcp
```

## Adding MCP Servers

### Transport Types

MCP servers use one of three transport protocols. Choose the appropriate transport based on the server type:

#### HTTP Transport (Remote Servers)

For cloud-based services providing HTTP endpoints:

```bash
# Basic syntax
claude mcp add --transport http <name> <url>

# Example: Add Notion server
claude mcp add --transport http notion https://mcp.notion.com/mcp

# With authentication header
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer YOUR_TOKEN"
```

#### SSE Transport (Server-Sent Events)

For remote servers using SSE protocol:

```bash
# Basic syntax
claude mcp add --transport sse <name> <url>

# Example: Add Webflow server
claude mcp add --transport sse webflow https://mcp.webflow.com/sse

# With API key header
claude mcp add --transport sse private-api https://api.company.com/sse \
  --header "X-API-Key: YOUR_KEY"
```

#### Stdio Transport (Local Process)

For servers running as local processes with stdio communication:

```bash
# Basic syntax
claude mcp add --transport stdio <name> [--env KEY=VALUE ...] -- <command> [args...]

# Example: Add Airtable server
claude mcp add --transport stdio airtable \
  --env AIRTABLE_API_KEY=YOUR_KEY \
  -- npx -y airtable-mcp-server

# Example: Add local Python server
claude mcp add --transport stdio custom-db \
  --env DB_URL=postgresql://localhost/mydb \
  -- python3 /path/to/server.py
```

**Important**: Use `--` separator before the command to indicate where environment variables end and the command begins.

## Configuration Scopes

MCP servers can be configured at three different scopes:

### Local Scope (Default)

Private to the current project directory only. Ideal for:
- Personal development servers
- Experimental configurations
- Servers with sensitive credentials

```bash
# Local scope (default)
claude mcp add --transport http stripe https://mcp.stripe.com

# Explicitly specify local scope
claude mcp add --transport http stripe --scope local https://mcp.stripe.com
```

### Project Scope

Shared with team members via `.mcp.json` in project root. Ideal for:
- Team-shared servers
- Project-specific tools
- Version-controlled configurations

```bash
# Add project-scoped server
claude mcp add --transport http paypal --scope project https://mcp.paypal.com/mcp
```

Creates/updates `.mcp.json`:
```json
{
  "mcpServers": {
    "paypal": {
      "type": "http",
      "url": "https://mcp.paypal.com/mcp"
    }
  }
}
```

**Security Note**: Claude Code prompts for approval before using project-scoped servers. Reset approvals with:
```bash
claude mcp reset-project-choices
```

### User Scope

Available across all projects on the machine. Ideal for:
- Personal utility servers
- Development tools used across projects
- Frequently-used services

```bash
# Add user-scoped server
claude mcp add --transport http hubspot --scope user https://mcp.hubspot.com/anthropic
```

### Scope Precedence

When servers with the same name exist at multiple scopes:
**Local > Project > User**

## Authentication

### OAuth 2.0 (Remote Servers)

Many remote MCP servers use OAuth. Authentication flow:

1. Add the server using `claude mcp add`
2. First use triggers OAuth browser flow
3. Authorize in browser
4. Credentials stored in `~/.mcp-auth/`

Example with Webflow:
```bash
# Add server
claude mcp add --transport sse webflow https://mcp.webflow.com/sse

# Check status - shows "⚠ Needs authentication"
claude mcp list

# Within Claude Code, trigger OAuth
# Ask: "List my Webflow sites"
# Browser opens for authorization
```

Reset OAuth credentials:
```bash
rm -rf ~/.mcp-auth
```

### API Keys and Headers

For servers requiring API keys or custom headers:

```bash
# Bearer token
claude mcp add --transport http api-server https://api.example.com/mcp \
  --header "Authorization: Bearer YOUR_TOKEN"

# API key header
claude mcp add --transport sse service https://service.com/sse \
  --header "X-API-Key: YOUR_KEY"

# Multiple headers
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer TOKEN" \
  --header "X-Custom-Header: VALUE"
```

### Environment Variables (Stdio Servers)

Pass sensitive credentials via environment variables:

```bash
claude mcp add --transport stdio database \
  --env DB_PASSWORD=secret123 \
  --env API_KEY=key456 \
  -- python3 /path/to/db-server.py
```

## Troubleshooting

### Common Issues

**Server shows "⚠ Needs authentication"**
- Remote server requires OAuth
- Trigger authentication by using the server's tools
- Check `claude mcp get <name>` for authentication status

**Server shows "✗ Connection failed"**
- Verify URL is correct
- Check network connectivity
- Ensure authentication credentials are valid
- For stdio servers, verify command path and permissions

**Server not appearing in list**
- Restart Claude Code CLI if just added
- Check scope - server may be at different scope level
- Verify configuration file syntax

**Project-scoped server requires repeated approval**
- Claude Code asks for approval on first use as security measure
- Select "Approve once" or "Always approve" when prompted
- Reset choices with `claude mcp reset-project-choices`

### Configuration File Locations

**Local scope**: Project-specific settings in `.claude/settings.local.json`
**Project scope**: `.mcp.json` in project root
**User scope**: `~/.claude/settings.json`

### Debugging

Enable MCP debug mode:
```bash
claude --mcp-debug
```

Or use newer debug flag:
```bash
claude --debug
```

Check server details:
```bash
# Get server configuration
claude mcp get <server-name>

# List all servers with status
claude mcp list
```

## Advanced Usage

### Environment Variable Expansion in .mcp.json

Project-scoped configurations support environment variable expansion:

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

Syntax:
- `${VAR}` - Expand environment variable
- `${VAR:-default}` - Use default if not set

### Import from Claude Desktop

If MCP servers are already configured in Claude Desktop:

```bash
claude mcp add-from-claude-desktop
```

Imports servers from Claude Desktop configuration (macOS and WSL only).

### Add from JSON Configuration

Direct JSON configuration import:

```bash
claude mcp add-json <name> '<json-config>'
```

Example:
```bash
claude mcp add-json my-server '{
  "command": "npx",
  "args": ["-y", "server-package"],
  "env": {"API_KEY": "value"}
}'
```

### MCP Output Limits

Control maximum output tokens from MCP tools:

```bash
# Set custom limit (default: 25,000 tokens)
export MAX_MCP_OUTPUT_TOKENS=50000
claude
```

Useful for servers that:
- Query large datasets
- Generate detailed reports
- Process extensive logs

## Common MCP Servers

Reference the [full MCP documentation](references/mcp_documentation.md) for an extensive list of popular MCP servers across categories:

- **Development & Testing**: Sentry, Socket, Hugging Face, Jam
- **Project Management**: Asana, Atlassian, Linear, Notion, Monday
- **Databases**: Airtable, HubSpot, PostgreSQL
- **Payments**: PayPal, Plaid, Square, Stripe
- **Design**: Figma, Canva, InVideo
- **Infrastructure**: Cloudflare, Netlify, Vercel
- **Automation**: Workato, Zapier

## Resources

### references/mcp_documentation.md

Complete MCP documentation including:
- Comprehensive server directory with installation commands
- Detailed transport protocol specifications
- Authentication methods and OAuth flows
- Plugin-based MCP servers
- Enterprise MCP configuration
- Environment variable expansion syntax
- Practical examples and use cases

Consult when:
- Need installation command for specific MCP server
- Troubleshooting complex configuration issues
- Setting up enterprise MCP deployment
- Understanding transport protocol details
