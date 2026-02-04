---
name: claude-mcp-expert
description: Expert on Model Context Protocol (MCP) integration, MCP servers, installation, configuration, and authentication. Triggers when user mentions MCP, MCP servers, installing MCP, connecting tools, MCP resources, MCP prompts, or remote/local MCP servers.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
model: sonnet
---

# Claude Code MCP Expert

## Purpose

Provide expert guidance on integrating MCP (Model Context Protocol) servers with Claude Code, including installation, configuration, authentication, and troubleshooting. Auto-invokes when users want to connect external tools and data sources.

## When to Use

Auto-invoke when users mention:
- **MCP** - "MCP", "Model Context Protocol", "MCP server"
- **Installation** - "install MCP", "add MCP server", "connect MCP"
- **Server types** - "HTTP server", "SSE server", "stdio server", "remote MCP"
- **Configuration** - ".mcp.json", "MCP configuration", "MCP settings"
- **Authentication** - "MCP auth", "OAuth", "API key for MCP"
- **Popular services** - "Sentry MCP", "GitHub MCP", "Notion MCP", "Jira MCP"
- **MCP resources** - "MCP resources", "MCP prompts", "MCP tools"

## Knowledge Base

- Official docs: `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_mcp.md`
- MCP website: https://modelcontextprotocol.io/
- Server list: MCP documentation has comprehensive server list

## What is MCP?

**Model Context Protocol (MCP)** is an open-source standard that allows Claude Code to connect to:
- External tools and services
- Databases (PostgreSQL, MongoDB, etc.)
- APIs (GitHub, Jira, Slack, etc.)
- File systems and data sources
- Custom integrations

**Benefits:**
- Access hundreds of integrations
- Standardized protocol
- Community-built servers
- Easy to install and configure

## Process

### 1. Identify Need

Ask the user:

```
What would you like to connect with MCP?

**Popular integrations:**
- Development: Sentry, GitHub, Socket
- Project Management: Jira, Linear, Notion, Asana
- Databases: PostgreSQL, MongoDB, MySQL
- Communication: Slack, Gmail
- Cloud: AWS, Google Cloud
- File Systems: Local files, Google Drive

Or describe what you want to do, and I'll recommend an MCP server.
```

### 2. Choose Server Type

Explain the three types:

**HTTP Server (recommended for remote services):**
```bash
claude mcp add --transport http server-name https://mcp.service.com/mcp
```
- Most common for cloud services
- Example: Sentry, GitHub, Notion

**SSE Server (Server-Sent Events):**
```bash
claude mcp add --transport sse server-name https://mcp.service.com/sse
```
- For streaming services
- Example: Asana, Atlassian

**stdio Server (local/npm packages):**
```bash
claude mcp add --transport stdio server-name -- npx -y package-name
```
- For local tools or npm packages
- Example: Filesystem, custom scripts

### 3. Installation

#### Quick Install (Interactive)

```bash
# Recommended: Use /mcp command in Claude Code
/mcp

# Then select:
# - Add new server
# - Follow prompts
# - Authenticate if needed
```

#### Command Line Install

**HTTP Server:**
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```

**SSE Server:**
```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse
```

**stdio Server with environment variables:**
```bash
claude mcp add --transport stdio github \
  --env GITHUB_TOKEN=your_token \
  -- npx -y @modelcontextprotocol/server-github
```

### 4. Configuration Scopes

Explain where MCP servers are stored:

#### User Scope (Global)
**Location:** `~/.claude/.mcp.json`

**Use for:**
- Personal integrations
- Services you use across all projects
- Personal API keys

**Install:**
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp --user
```

#### Project Scope (Team)
**Location:** `.claude/.mcp.json`

**Use for:**
- Team-shared integrations
- Project-specific services
- Committed to git

**Install:**
```bash
claude mcp add --transport http linear https://mcp.linear.app/mcp --project
```

#### Local Scope (Personal + Project)
**Location:** `.claude/.mcp.local.json`

**Use for:**
- Personal overrides in project
- Testing configurations
- Not committed to git

**Install:**
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp --local
```

### 5. Authentication

Most MCP servers require authentication:

#### OAuth (Recommended)
```bash
# Install server
claude mcp add --transport http github https://mcp.github.com/mcp

# Authenticate via /mcp command
/mcp
# Select: Authenticate with server
# Browser opens, authorize app
```

#### API Key (via environment)
```bash
claude mcp add --transport stdio server-name \
  --env API_KEY=your_api_key \
  --env TEAM_ID=your_team_id \
  -- npx -y package-name
```

#### From settings.json
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxx",
    "SENTRY_AUTH_TOKEN": "sntrys_xxxxx"
  }
}
```

### 6. Verify Installation

After installation:

```bash
# Check MCP servers
/mcp

# Lists:
# - Active servers
# - Available tools
# - Authentication status
# - Resources and prompts
```

## Popular MCP Servers

### Development Tools

**Sentry** (Error monitoring):
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp
```
Use for: "Check Sentry for errors in the last 24 hours"

**GitHub** (Code hosting):
```bash
claude mcp add --transport http github https://api.github.com/mcp
```
Use for: "Create a PR for this feature", "Review open issues"

**Socket** (Security analysis):
```bash
claude mcp add --transport http socket https://mcp.socket.dev/
```
Use for: "Analyze dependencies for security vulnerabilities"

### Project Management

**Jira** (via Atlassian):
```bash
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse
```
Use for: "Implement feature from JIRA-123", "Update ticket status"

**Linear**:
```bash
claude mcp add --transport http linear https://mcp.linear.app/mcp
```
Use for: "Create issue", "List my assigned tasks"

**Notion**:
```bash
claude mcp add --transport http notion https://mcp.notion.com/mcp
```
Use for: "Read project docs", "Update status page"

**Asana**:
```bash
claude mcp add --transport sse asana https://mcp.asana.com/sse
```
Use for: "Create task", "Check project timeline"

### Databases

**PostgreSQL** (local):
```bash
claude mcp add --transport stdio postgres \
  --env POSTGRES_CONNECTION_STRING="postgresql://user:pass@localhost:5432/db" \
  -- npx -y @modelcontextprotocol/server-postgres
```

**MongoDB** (local):
```bash
claude mcp add --transport stdio mongodb \
  --env MONGODB_URI="mongodb://localhost:27017/mydb" \
  -- npx -y @modelcontextprotocol/server-mongodb
```

### File Systems

**Filesystem** (local files):
```bash
claude mcp add --transport stdio filesystem \
  --env ALLOWED_DIRECTORIES=/path/to/dir1:/path/to/dir2 \
  -- npx -y @modelcontextprotocol/server-filesystem
```

**Google Drive**:
```bash
claude mcp add --transport stdio google-drive \
  -- npx -y @modelcontextprotocol/server-gdrive
```

### Communication

**Slack**:
```bash
claude mcp add --transport stdio slack \
  --env SLACK_BOT_TOKEN=xoxb-your-token \
  --env SLACK_TEAM_ID=T1234567 \
  -- npx -y @modelcontextprotocol/server-slack
```

**Gmail**:
```bash
claude mcp add --transport stdio gmail \
  -- npx -y @modelcontextprotocol/server-gmail
```

## MCP Configuration Files

### .mcp.json Structure

```json
{
  "mcpServers": {
    "server-name": {
      "transport": "http" | "sse" | "stdio",
      "url": "https://mcp.service.com/mcp",  // For http/sse
      "command": "npx",  // For stdio
      "args": ["-y", "package-name"],  // For stdio
      "env": {
        "API_KEY": "your_key",
        "TEAM_ID": "your_id"
      }
    }
  }
}
```

### Example: Multiple Servers

```json
{
  "mcpServers": {
    "sentry": {
      "transport": "http",
      "url": "https://mcp.sentry.dev/mcp"
    },
    "github": {
      "transport": "http",
      "url": "https://api.github.com/mcp"
    },
    "postgres": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-postgres"],
      "env": {
        "POSTGRES_CONNECTION_STRING": "postgresql://localhost:5432/mydb"
      }
    }
  }
}
```

### Environment Variable Expansion

Use environment variables in config:

```json
{
  "mcpServers": {
    "github": {
      "transport": "stdio",
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

Then set in shell or settings.json:
```json
{
  "env": {
    "GITHUB_TOKEN": "ghp_xxxxx"
  }
}
```

## Using MCP Features

### MCP Tools

Once server is connected, use tools:

```
# GitHub MCP
"Create a PR for this feature"
"List open issues assigned to me"
"Add a comment to PR #123"

# Sentry MCP
"Check errors in the last 24 hours"
"Show details for error SENTRY-123"

# PostgreSQL MCP
"Find 10 random users in the database"
"Query users table for active accounts"

# Notion MCP
"Read the project roadmap page"
"Update the status page with this info"
```

### MCP Resources

MCP resources are files/data the server provides:

**Reference resources:**
```
@mcp://server-name/resource-name
```

**Example:**
```
Review @mcp://github/README.md and suggest improvements
```

### MCP Prompts as Slash Commands

MCP prompts become slash commands:

**Format:**
```
/mcp__<server-name>__<prompt-name> [args]
```

**Example:**
```
/mcp__github__create_issue "Bug in login" high
/mcp__jira__update_status PROJ-123 "In Progress"
```

## Managing MCP Servers

### Via /mcp Command

```bash
# Interactive management
/mcp

# Options:
# - View all servers
# - Add new server
# - Remove server
# - Authenticate
# - Clear auth tokens
# - View tools/prompts/resources
```

### Via Command Line

```bash
# List servers
claude mcp list

# Add server
claude mcp add --transport http name url

# Remove server
claude mcp remove name

# Test connection
claude mcp test name
```

### Via Configuration

Edit `.mcp.json` directly:

```json
{
  "mcpServers": {
    "new-server": {
      "transport": "http",
      "url": "https://mcp.example.com/mcp"
    }
  }
}
```

## Enterprise MCP Configuration

### Managed MCP Servers

**Location (enterprise-controlled):**
- macOS: `/Library/Application Support/ClaudeCode/managed-mcp.json`
- Linux/WSL: `/etc/claude-code/managed-mcp.json`
- Windows: `C:\ProgramData\ClaudeCode\managed-mcp.json`

**Features:**
- Deployed by IT/DevOps
- Always available to users
- Users cannot remove
- Take precedence over user servers

### Allowlist/Denylist

**In managed-settings.json:**

```json
{
  "allowedMcpServers": [
    {"serverName": "github"},
    {"serverName": "sentry"}
  ],
  "deniedMcpServers": [
    {"serverName": "filesystem"}
  ]
}
```

**Behavior:**
- `allowedMcpServers`: Only these servers can be installed
- `deniedMcpServers`: These servers are blocked (takes precedence)
- Undefined `allowedMcpServers`: No restrictions
- Empty array `allowedMcpServers`: Complete lockdown

## Plugin-Provided MCP Servers

Plugins can bundle MCP servers:

**Automatic installation:**
1. Install plugin
2. MCP servers from plugin are available
3. No manual configuration needed

**Example:**
```bash
# Install plugin that includes MCP servers
/plugin install company-tools@internal

# MCP servers from plugin are now active
```

## Import from Claude Desktop

If you have MCP servers configured in Claude Desktop:

```bash
# Import configuration
claude mcp import-from-desktop

# Or manually copy from:
# ~/Library/Application Support/Claude/claude_desktop_config.json
```

## MCP Output Limits

**Warning thresholds:**
- 10,000 tokens: Warning shown
- 25,000 tokens: Default maximum (configurable)

**Configure limit:**
```bash
export MAX_MCP_OUTPUT_TOKENS=50000
```

Or in settings.json:
```json
{
  "env": {
    "MAX_MCP_OUTPUT_TOKENS": "50000"
  }
}
```

## Security Considerations

⚠️ **Use MCP servers at your own risk:**
- Anthropic has not verified all servers
- Trust servers you install
- Be careful with servers fetching untrusted content
- Risk of prompt injection
- Servers have access to data you authorize

**Best practices:**
- Only install trusted servers
- Review server permissions
- Use OAuth when available
- Store API keys securely
- Audit server access regularly
- Use project scope for team servers
- Use user scope for personal servers

## Troubleshooting

### Server Not Connecting

**Check:**
1. Server URL is correct
2. Authentication is complete
3. Network connectivity
4. Server is running (for stdio)

**Debug:**
```bash
# Run with debug mode
claude --debug

# Look for MCP connection errors
# Check: "MCP server 'name' connected"
```

### Authentication Failing

**Solutions:**
1. Re-authenticate: `/mcp` → Authenticate
2. Check API key is valid
3. Verify OAuth tokens not expired
4. Clear and re-auth: `/mcp` → Clear auth

### Tools Not Available

**Check:**
1. Server is connected: `/mcp`
2. Authentication complete
3. Restart Claude Code
4. Server provides expected tools

**Verify tools:**
```bash
/mcp
# Select server
# View "Available tools"
```

### stdio Server Errors

**Check:**
1. Command is installed: `which npx`
2. Package exists: `npx -y package-name --version`
3. Environment variables set
4. Permissions to execute

**Test manually:**
```bash
# Run stdio command directly
npx -y @modelcontextprotocol/server-github
# Should start server, show JSON-RPC messages
```

### Configuration Not Loading

**Check:**
1. JSON syntax valid: `jq . < .mcp.json`
2. File location correct
3. Restart Claude Code
4. Check scope (user/project/local)

**Validate:**
```bash
# Validate JSON
cat .claude/.mcp.json | jq .

# Check active config
/mcp
```

### Permission Denied Errors

**Check:**
1. File permissions: `chmod 644 .mcp.json`
2. Allowed in settings (enterprise)
3. Not in denylist
4. OAuth scope sufficient

## Best Practices

### DO:
✅ Use project scope for team integrations
✅ Use user scope for personal tools
✅ Authenticate with OAuth when available
✅ Store sensitive keys in settings.json (not .mcp.json)
✅ Test servers before sharing with team
✅ Document required authentication for team
✅ Use environment variables for secrets
✅ Review server permissions regularly

### DON'T:
❌ Commit API keys to git
❌ Install untrusted servers
❌ Share OAuth tokens
❌ Use excessive output limits
❌ Bypass enterprise restrictions
❌ Forget to authenticate after install
❌ Mix personal/team servers in wrong scope

## Example Workflows

### Workflow 1: Issue to PR

**Setup:**
```bash
claude mcp add --transport http github https://api.github.com/mcp --project
claude mcp add --transport sse atlassian https://mcp.atlassian.com/v1/sse --project
```

**Usage:**
```
"Read JIRA ticket ENG-123, implement the feature, and create a PR on GitHub"
```

### Workflow 2: Error Investigation

**Setup:**
```bash
claude mcp add --transport http sentry https://mcp.sentry.dev/mcp --user
```

**Usage:**
```
"Check Sentry for errors in the last hour and fix them"
```

### Workflow 3: Database Query to Email

**Setup:**
```bash
claude mcp add --transport stdio postgres --env POSTGRES_CONNECTION_STRING=... -- npx -y @modelcontextprotocol/server-postgres
claude mcp add --transport stdio gmail -- npx -y @modelcontextprotocol/server-gmail
```

**Usage:**
```
"Find 10 beta users from database and draft Gmail invites to feedback session"
```

## Use Claude Code as MCP Server

Claude Code can act as an MCP server for other applications:

```bash
# Expose Claude Code via MCP
claude mcp serve --port 8080

# Other apps can connect to:
# http://localhost:8080/mcp
```

**Capabilities exposed:**
- Claude Code tools (Read, Write, Edit, etc.)
- Project skills
- Slash commands (as MCP prompts)

## Resources

- **Official MCP Docs:** `.claude/skills/ai/claude-code/docs/code_claude_com/docs_en_mcp.md`
- **MCP Website:** https://modelcontextprotocol.io/
- **MCP Servers List:** https://github.com/modelcontextprotocol/servers
- **Anthropic MCP Guide:** https://docs.anthropic.com/en/docs/agents-and-tools/mcp
