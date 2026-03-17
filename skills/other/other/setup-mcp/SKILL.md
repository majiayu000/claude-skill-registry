---
name: setup-mcp
description: Find, install, and configure an MCP server for a specific service. Handles discovery, installation, and verification.
disable-model-invocation: true
argument-hint: [service-name e.g. figma, github, postgres]
---

# Setup MCP Server

Find, install, and configure an MCP (Model Context Protocol) server for a specific external service.

## Usage

`/setup-mcp <service-name>`

Examples:
- `/setup-mcp github`
- `/setup-mcp postgres`
- `/setup-mcp figma`
- `/setup-mcp slack`

## Procedure

### Step 1: Identify the Service

Parse `$ARGUMENTS` to determine what service the user wants to connect. Common services:
- **github** — GitHub API (issues, PRs, repos)
- **postgres / mysql / sqlite** — Database access
- **figma** — Design file access
- **slack** — Messaging
- **linear** — Project management
- **notion** — Documentation
- **filesystem** — Local file access with sandboxing
- **brave-search** — Web search
- **memory** — Persistent knowledge graph

### Step 2: Search for MCP Server

Search for an appropriate MCP server:

1. Check the official MCP servers list by searching the web for: `site:github.com modelcontextprotocol/servers [service-name]`
2. Also search for community servers: `mcp server [service-name]`
3. Check npm: `npm search mcp-server-[service-name]`

Evaluate candidates on:
- Stars / downloads (popularity = maintenance likelihood)
- Last updated (stale = risky)
- Official vs community (prefer official)

### Step 3: Present Options

Show the user what was found:

```
Found MCP servers for [service]:

1. [name] (official) — [description]
   Stars: [N] | Last updated: [date]
   Install: [command]

2. [name] (community) — [description]
   Stars: [N] | Last updated: [date]
   Install: [command]

Which would you like to install?
```

### Step 4: Install

Based on the server type, install appropriately:

**For npx-based servers** (most common):
Add to `.claude/settings.json` under `mcpServers`:

```json
{
  "mcpServers": {
    "[service-name]": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-[name]"],
      "env": {
        "API_KEY": "your-api-key-here"
      }
    }
  }
}
```

**For Docker-based servers**:
```json
{
  "mcpServers": {
    "[service-name]": {
      "command": "docker",
      "args": ["run", "-i", "--rm", "[image-name]"]
    }
  }
}
```

### Step 5: Configure Authentication

If the MCP server requires API keys or tokens:

1. Tell the user what credentials are needed
2. Ask them to provide the credentials
3. **Never store credentials directly in settings.json** — use environment variables
4. Show how to set the env var: `export MCP_[SERVICE]_KEY=your-key`

### Step 6: Verify Installation

1. Tell the user to run `/mcp` to check the server status
2. The server should appear in the list with a "connected" status
3. If it fails, check:
   - Is the command/path correct?
   - Are environment variables set?
   - Are network/firewall rules blocking it?

### Step 7: Warn About Token Costs

Important caveat to share with the user:

> "Note: MCP servers add tools to Claude's context, which increases token usage. Each MCP server's tool descriptions are loaded into every message. If you notice higher token consumption, consider disabling MCP servers you're not actively using."
