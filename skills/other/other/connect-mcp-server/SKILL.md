---
name: connect-mcp-server
description: Guide for connecting MCP (Model Context Protocol) servers to Claude Code with HTTP, stdio, and SSE transports. Covers installation, configuration, authentication, environment variables, and security. Use when the user wants to connect MCP servers, add integrations, configure external services, or mentions MCP, servers, integrations, or external tools.
---

# Connect MCP Server Guide

This skill helps you connect MCP (Model Context Protocol) servers to Claude Code, enabling integrations with external services like GitHub, Notion, databases, project management tools, and custom APIs.

## Quick Start

When connecting an MCP server, follow this workflow:

1. **Identify the server** - Which service do you want to integrate?
2. **Choose transport** - HTTP (remote), stdio (local), or SSE (deprecated)
3. **Gather credentials** - API keys, tokens, or OAuth requirements
4. **Select scope** - Local (default), project (.mcp.json), or user (cross-project)
5. **Add server** - Use `claude mcp add` command
6. **Authenticate** - Use `/mcp` in Claude Code for OAuth
7. **Test connection** - Verify server status and available tools
8. **Use resources/prompts** - Access via `@` and `/` prefixes

## What is MCP?

**Model Context Protocol (MCP)** is a standard for connecting AI assistants to external services and data sources. MCP servers provide:

- **Tools:** Functions Claude can execute (e.g., create GitHub issue)
- **Resources:** Data Claude can reference (e.g., @github:issue://123)
- **Prompts:** Pre-built commands (e.g., /mcp__github__review-pr)

## Transport Protocols

### 1. HTTP Servers (Recommended)

**Best for:** Remote cloud-based services
**Protocol:** HTTP/HTTPS with JSON-RPC

**Basic syntax:**
```bash
claude mcp add --transport http <name> <url>
```

**Examples:**

**Notion integration:**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**GitHub integration:**
```bash
claude mcp add --transport http github https://mcp.github.com
```

**Custom API with authentication:**
```bash
claude mcp add --transport http secure-api https://api.example.com/mcp \
  --header "Authorization: Bearer your-token-here"
```

**Multiple headers:**
```bash
claude mcp add --transport http api https://api.example.com/mcp \
  --header "Authorization: Bearer token" \
  --header "X-API-Version: v2"
```

**Advantages:**
- No local installation required
- Works across networks
- Managed by service provider
- Automatic updates
- OAuth 2.0 support

### 2. Stdio Servers (Local)

**Best for:** Local tools requiring system access
**Protocol:** Standard input/output (stdin/stdout)

**Basic syntax:**
```bash
claude mcp add --transport stdio <name> <command> [args...]
```

**Examples:**

**Using npx (recommended for Node.js servers):**
```bash
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem /path/to/allowed/directory
```

**With environment variables:**
```bash
claude mcp add --transport stdio airtable \
  --env AIRTABLE_API_KEY=your-key-here \
  -- npx -y airtable-mcp-server
```

**Direct executable:**
```bash
claude mcp add --transport stdio custom-server -- /usr/local/bin/my-server --arg1 value1
```

**Windows-specific (requires cmd /c wrapper):**
```bash
claude mcp add --transport stdio github-local -- cmd /c npx -y @modelcontextprotocol/server-github
```

**Python server:**
```bash
claude mcp add --transport stdio python-server -- python3 /path/to/server.py
```

**Advantages:**
- Direct file system access
- No network latency
- Full control over installation
- Works offline
- Can integrate system utilities

**Important notes:**
- The `--` separator is required before the command
- Use `-y` flag with npx to auto-install
- Windows requires `cmd /c` wrapper for npx

### 3. SSE Servers (Deprecated)

**Status:** Deprecated - use HTTP servers instead

**Syntax (if needed):**
```bash
claude mcp add --transport sse <name> <url>
```

**Note:** SSE (Server-Sent Events) transport is being phased out. Migrate to HTTP servers where available.

## Configuration Scopes

### Local Scope (Default)

**Storage:** User settings (not shared)
**Use for:** Personal project-specific servers

```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

No `--scope` flag means local scope.

### Project Scope

**Storage:** `.mcp.json` in project root (shared via git)
**Use for:** Team-wide integrations

```bash
claude mcp add --transport http github https://mcp.github.com --scope project
```

**Creates:** `.mcp.json` file:
```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com"
    }
  }
}
```

**Important:** Claude Code prompts for approval before using project-scoped servers from `.mcp.json` files for security.

### User Scope

**Storage:** User settings (cross-project)
**Use for:** Servers you use across all projects

```bash
claude mcp add --transport stdio filesystem \
  --scope user \
  -- npx -y @modelcontextprotocol/server-filesystem ~/Documents
```

Available in all projects on your machine.

## Manual Configuration (.mcp.json)

### HTTP Server Configuration

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}",
        "X-Custom-Header": "value"
      }
    },
    "notion": {
      "type": "http",
      "url": "https://mcp.notion.com/mcp"
    }
  }
}
```

### Stdio Server Configuration

```json
{
  "mcpServers": {
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/allowed/directory"
      ]
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL}"
      }
    },
    "custom-python": {
      "type": "stdio",
      "command": "python3",
      "args": ["/path/to/server.py", "--config", "config.json"],
      "env": {
        "PYTHONPATH": "/custom/python/path",
        "API_KEY": "${MY_API_KEY}"
      }
    }
  }
}
```

### Complete Example with Multiple Servers

```json
{
  "mcpServers": {
    "github": {
      "type": "http",
      "url": "https://mcp.github.com",
      "headers": {
        "Authorization": "Bearer ${GITHUB_TOKEN}"
      }
    },
    "filesystem": {
      "type": "stdio",
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${HOME}/projects"
      ]
    },
    "postgres": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "${DATABASE_URL:-postgresql://localhost:5432/mydb}"
      }
    },
    "slack": {
      "type": "http",
      "url": "https://mcp.slack.com",
      "headers": {
        "Authorization": "Bearer ${SLACK_TOKEN}"
      }
    }
  }
}
```

## Environment Variables

### Variable Expansion

Claude Code supports environment variable expansion:

**Syntax:**
- `${VAR}` - Expands to environment variable value
- `${VAR:-default}` - Uses default if variable not set

**Supported locations:**
- Command paths
- Arguments
- Environment settings
- HTTP headers

**Examples:**

```json
{
  "mcpServers": {
    "api": {
      "type": "http",
      "url": "https://api.example.com/mcp",
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}",
        "X-Environment": "${ENVIRONMENT:-production}"
      }
    },
    "local-server": {
      "type": "stdio",
      "command": "${HOME}/bin/my-server",
      "args": ["--config", "${CONFIG_PATH:-/etc/server.conf}"],
      "env": {
        "LOG_LEVEL": "${LOG_LEVEL:-info}",
        "DATA_DIR": "${DATA_DIR}"
      }
    }
  }
}
```

### Setting Environment Variables

**macOS/Linux (.bashrc, .zshrc):**
```bash
export GITHUB_TOKEN="ghp_your_token_here"
export DATABASE_URL="postgresql://user:pass@localhost:5432/db"
export API_KEY="your-api-key"
```

**Windows (PowerShell):**
```powershell
$env:GITHUB_TOKEN = "ghp_your_token_here"
$env:DATABASE_URL = "postgresql://user:pass@localhost:5432/db"
```

**Session-specific:**
```bash
# Set variable before running Claude Code
GITHUB_TOKEN=token DATABASE_URL=url claude
```

## Authentication

### OAuth 2.0 (Recommended)

Many cloud-based MCP servers use OAuth 2.0:

**Process:**
1. Add server (no credentials needed initially)
2. Start Claude Code
3. Type `/mcp` command
4. Follow browser login flow
5. Tokens stored securely and auto-refreshed

**Example:**
```bash
# Add GitHub server
claude mcp add --transport http github https://mcp.github.com

# In Claude Code session
/mcp
# Opens browser for GitHub authentication
```

### API Token Authentication

For services using API tokens:

**Via header:**
```bash
claude mcp add --transport http service https://api.example.com/mcp \
  --header "Authorization: Bearer your-token"
```

**Via environment variable:**
```bash
# Set environment variable
export SERVICE_TOKEN="your-token"

# Add server with variable reference
claude mcp add --transport http service https://api.example.com/mcp \
  --header "Authorization: Bearer ${SERVICE_TOKEN}"
```

### No Authentication

Public or local servers:

```bash
claude mcp add --transport http public https://public-api.example.com/mcp
```

## Server Management Commands

### List All Servers

```bash
claude mcp list
```

**Output:**
```
Configured MCP servers:
  github (http) - https://mcp.github.com
  filesystem (stdio) - npx -y @modelcontextprotocol/server-filesystem
  postgres (stdio) - npx -y @modelcontextprotocol/server-postgres
```

### Get Server Details

```bash
claude mcp get github
```

**Output:**
```json
{
  "type": "http",
  "url": "https://mcp.github.com",
  "headers": {
    "Authorization": "Bearer ..."
  }
}
```

### Remove Server

```bash
claude mcp remove github
```

### Reset Project Approval Choices

```bash
claude mcp reset-project-choices
```

Clears your approval decisions for project-scoped servers.

### Check Server Status (In Claude Code)

```
/mcp
```

Shows:
- Connected servers
- Authentication status
- Available tools and resources

## Using MCP Resources

### Reference Resources with @

Type `@` in Claude Code to see available resources:

**Format:**
```
@server:protocol://resource/path
```

**Examples:**

**GitHub issue:**
```
Review the implementation in @github:issue://123
```

**Notion page:**
```
Summarize @notion:page://abc123def456
```

**File from filesystem server:**
```
Compare @filesystem:file:///project/src/old.js with current implementation
```

**Database table:**
```
Analyze schema for @postgres:table://users
```

## Using MCP Prompts

### Execute Prompts with /

Type `/` to discover MCP prompts:

**Format:**
```
/mcp__servername__promptname [arguments]
```

**Examples:**

**GitHub PR review:**
```
/mcp__github__review-pr 123
```

**Notion page creation:**
```
/mcp__notion__create-page "Project Ideas" "Brainstorming session notes"
```

**Database query:**
```
/mcp__postgres__query "SELECT * FROM users WHERE active = true"
```

## Output Limits

### Default Limits

- **Warning threshold:** 10,000 tokens
- **Default maximum:** 25,000 tokens

### Configure Output Limit

```bash
# Allow larger outputs (50,000 tokens)
export MAX_MCP_OUTPUT_TOKENS=50000
claude

# Or inline
MAX_MCP_OUTPUT_TOKENS=50000 claude
```

**Use when:**
- Server returns large datasets
- Processing extensive documents
- Analyzing comprehensive logs

## Timeout Configuration

### MCP Server Startup Timeout

```bash
# 10-second timeout (default is 5 seconds)
MCP_TIMEOUT=10000 claude
```

**Use when:**
- Server initialization is slow
- Network latency is high
- Complex server setup required

## Popular MCP Servers

### Official MCP Servers

**GitHub:**
```bash
claude mcp add --transport http github https://mcp.github.com
```
Tools: Create issues, review PRs, manage repositories

**Filesystem:**
```bash
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/Documents
```
Tools: Read/write files, search directories

**PostgreSQL:**
```bash
claude mcp add --transport stdio postgres \
  --env POSTGRES_CONNECTION_STRING=postgresql://localhost:5432/db \
  -- npx -y @modelcontextprotocol/server-postgres
```
Tools: Query database, analyze schema

**Slack:**
```bash
claude mcp add --transport http slack https://mcp.slack.com
```
Tools: Send messages, search history, manage channels

**Google Drive:**
```bash
claude mcp add --transport http gdrive https://mcp.google.com/drive
```
Tools: Access files, search documents, manage folders

**Brave Search:**
```bash
claude mcp add --transport stdio brave-search \
  --env BRAVE_API_KEY=your-key \
  -- npx -y @modelcontextprotocol/server-brave-search
```
Tools: Web search, fact-checking

**Git:**
```bash
claude mcp add --transport stdio git -- npx -y @modelcontextprotocol/server-git
```
Tools: Repository operations, commit history, diff analysis

**Sentry:**
```bash
claude mcp add --transport http sentry https://mcp.sentry.io \
  --header "Authorization: Bearer ${SENTRY_TOKEN}"
```
Tools: Error monitoring, stack trace analysis

**Linear:**
```bash
claude mcp add --transport http linear https://mcp.linear.app
```
Tools: Issue tracking, project management

**Notion:**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```
Tools: Page creation, database queries, content search

### Community MCP Servers

**Airtable:**
```bash
claude mcp add --transport stdio airtable \
  --env AIRTABLE_API_KEY=your-key \
  -- npx -y airtable-mcp-server
```

**MongoDB:**
```bash
claude mcp add --transport stdio mongodb \
  --env MONGODB_URI=mongodb://localhost:27017 \
  -- npx -y mongodb-mcp-server
```

**Redis:**
```bash
claude mcp add --transport stdio redis \
  --env REDIS_URL=redis://localhost:6379 \
  -- npx -y redis-mcp-server
```

**AWS:**
```bash
claude mcp add --transport stdio aws \
  --env AWS_PROFILE=default \
  -- npx -y aws-mcp-server
```

## Enterprise MCP Configuration

### Managed MCP Servers

Administrators can deploy centralized configurations:

**macOS:**
```
/Library/Application Support/ClaudeCode/managed-mcp.json
```

**Windows:**
```
C:\ProgramData\ClaudeCode\managed-mcp.json
```

**Linux:**
```
/etc/claude-code/managed-mcp.json
```

### Allowlists/Denylists

**managed-settings.json:**
```json
{
  "mcpServers": {
    "allowlist": ["github", "slack", "notion"],
    "denylist": ["unapproved-server"]
  }
}
```

Controls which servers users can configure.

## Security Considerations

### Trust Verification

**CRITICAL WARNING:** "Use third party MCP servers at your own risk - Anthropic has not verified the correctness or security of all these servers."

**Before installing:**
- Verify server source (official vs community)
- Review server code if open source
- Check reputation and reviews
- Understand data access requirements
- Review authentication requirements

### Prompt Injection Risks

Servers that fetch untrusted content (web search, user input) can expose Claude to prompt injection attacks.

**Mitigation:**
- Use servers from trusted sources
- Limit server permissions
- Review server behavior regularly
- Monitor for unexpected actions

### Credential Management

**Best practices:**
- Use environment variables for secrets
- Never commit tokens to git (.mcp.json with ${VAR})
- Rotate credentials regularly
- Use least-privilege access tokens
- Enable OAuth when available

**Bad practice:**
```json
{
  "mcpServers": {
    "api": {
      "headers": {
        "Authorization": "Bearer hardcoded-token-123"
      }
    }
  }
}
```

**Good practice:**
```json
{
  "mcpServers": {
    "api": {
      "headers": {
        "Authorization": "Bearer ${API_TOKEN}"
      }
    }
  }
}
```

### Project-Scoped Server Approval

Claude Code prompts before using servers from `.mcp.json`:

**Prompt:**
```
This project wants to connect to the following MCP servers:
- github (https://mcp.github.com)
- filesystem (local file access)

Do you trust these servers?
[Allow for this session] [Always allow] [Never allow]
```

**Review before approving:**
- Server purpose and source
- Data access requirements
- Team trustworthiness
- Security implications

## Troubleshooting

### Server Not Appearing

**Check configuration:**
```bash
claude mcp list
claude mcp get server-name
```

**Verify:**
- Server name is correct
- Configuration syntax is valid
- Environment variables are set
- Server is running (stdio)

### Authentication Failing

**For OAuth:**
```
/mcp
```
Re-authenticate through browser

**For API tokens:**
- Verify environment variable is set: `echo $TOKEN_NAME`
- Check token hasn't expired
- Verify token permissions

### Connection Timeout

**Increase timeout:**
```bash
MCP_TIMEOUT=15000 claude
```

**Check:**
- Network connectivity
- Server URL is correct
- Server is running and accessible

### Tools Not Available

**Verify server is connected:**
```
/mcp
```

**Check:**
- Server status shows as connected
- Authentication is complete
- Server supports expected tools

### Large Output Truncated

**Increase output limit:**
```bash
MAX_MCP_OUTPUT_TOKENS=50000 claude
```

**Alternative:**
- Request smaller data chunks
- Use server filtering options
- Paginate results

### Windows npx Issues

**Use cmd /c wrapper:**
```bash
claude mcp add --transport stdio server -- cmd /c npx -y package-name
```

## Testing MCP Servers

### 1. Verify Server Added

```bash
claude mcp list
```

Confirm server appears in the list.

### 2. Check Server Details

```bash
claude mcp get server-name
```

Verify configuration is correct.

### 3. Test in Claude Code

Start Claude Code and run:
```
/mcp
```

Confirm:
- Server shows as connected
- Authentication status is OK
- Tools are available

### 4. Test Resources

Type `@` and verify server resources appear:
```
@server-name:
```

### 5. Test Prompts

Type `/` and verify server prompts appear:
```
/mcp__server-name__
```

### 6. Execute Test Command

Try a simple server operation:
```
/mcp__github__list-repos
```

## Common Use Cases

### Development Workflow

**GitHub + Filesystem + Git:**
```bash
# GitHub for issues and PRs
claude mcp add --transport http github https://mcp.github.com

# Filesystem for project access
claude mcp add --transport stdio filesystem -- npx -y @modelcontextprotocol/server-filesystem ~/projects

# Git for version control
claude mcp add --transport stdio git -- npx -y @modelcontextprotocol/server-git
```

**Usage:**
- Review code from @filesystem:file://
- Reference issues with @github:issue://
- Check git history with /mcp__git__log

### Database Administration

**PostgreSQL + MongoDB:**
```bash
# PostgreSQL
claude mcp add --transport stdio postgres \
  --env POSTGRES_CONNECTION_STRING=${DATABASE_URL} \
  -- npx -y @modelcontextprotocol/server-postgres

# MongoDB
claude mcp add --transport stdio mongodb \
  --env MONGODB_URI=${MONGO_URL} \
  -- npx -y mongodb-mcp-server
```

**Usage:**
- Query data: `/mcp__postgres__query "SELECT ..."`
- Analyze schema: @postgres:schema://table_name
- Monitor collections: @mongodb:collection://users

### Project Management

**Linear + Slack + Notion:**
```bash
# Linear for issues
claude mcp add --transport http linear https://mcp.linear.app

# Slack for communication
claude mcp add --transport http slack https://mcp.slack.com

# Notion for documentation
claude mcp add --transport http notion https://mcp.notion.com/mcp
```

**Usage:**
- Create issues: `/mcp__linear__create-issue`
- Send updates: `/mcp__slack__send-message`
- Reference docs: @notion:page://abc123

### Error Monitoring

**Sentry + Logs:**
```bash
# Sentry for error tracking
claude mcp add --transport http sentry https://mcp.sentry.io \
  --header "Authorization: Bearer ${SENTRY_TOKEN}"

# Custom log server
claude mcp add --transport stdio logs -- python3 ~/mcp-servers/log-analyzer.py
```

**Usage:**
- Analyze errors: @sentry:issue://ERROR-123
- Search logs: `/mcp__logs__search "authentication failed"`

## Best Practices Checklist

When connecting an MCP server:

- [ ] Server source is trusted and verified
- [ ] Transport type matches use case (HTTP for remote, stdio for local)
- [ ] Scope is appropriate (local/project/user)
- [ ] Credentials use environment variables (not hardcoded)
- [ ] Authentication is configured (OAuth or API token)
- [ ] Server name is descriptive and unique
- [ ] Environment variables are set before adding server
- [ ] Configuration is tested (`claude mcp list`, `/mcp`)
- [ ] Resources and prompts are accessible (@ and /)
- [ ] Team is informed (for project-scoped servers)
- [ ] Security implications reviewed
- [ ] .mcp.json is committed to git (project scope)
- [ ] Secrets are NOT committed to git

## Key Principles

1. **Trust first** - Only install servers from verified sources
2. **Environment variables** - Use ${VAR} for secrets, never hardcode
3. **Scope appropriately** - Local for personal, project for team, user for cross-project
4. **OAuth when possible** - Prefer OAuth over API tokens for security
5. **Test thoroughly** - Verify connection and tools before relying on server
6. **Document for team** - Explain server purpose in project README
7. **Monitor access** - Review what data servers can access
8. **Keep updated** - Update servers regularly for security patches
9. **Least privilege** - Grant minimum necessary permissions
10. **Review regularly** - Audit configured servers periodically

## Workflow Summary

When user asks to connect an MCP server:

1. **Identify server** - Which service/integration is needed?
2. **Find installation method** - Official docs, GitHub, or custom
3. **Choose transport** - HTTP (remote) or stdio (local)?
4. **Gather credentials** - API keys, OAuth setup, connection strings
5. **Set environment variables** - Export secrets before adding server
6. **Select scope** - Local (default), project (team), or user (cross-project)
7. **Add server** - Use `claude mcp add` command
8. **Verify configuration** - `claude mcp list` and `claude mcp get`
9. **Test connection** - `/mcp` in Claude Code session
10. **Use server** - Access resources (@) and prompts (/)

Remember: MCP servers extend Claude's capabilities by connecting to external services. Always verify server trust, use environment variables for secrets, and test thoroughly before relying on server integrations.
