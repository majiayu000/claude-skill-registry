---
name: install-agentpmt-mcp
description: Install and configure the AgentPMT MCP server for any AI agent. Use this skill when the user wants to connect Claude Desktop, Claude Code, Cursor, Windsurf, VS Code, Zed, OpenAI Codex CLI, Gemini CLI, or any MCP-compatible client to the AgentPMT tool marketplace. Also use when the user mentions AgentPMT setup, MCP server configuration, agent tool marketplace, or connecting an AI agent to paid tools and APIs.
---

# Install AgentPMT MCP Server

Connect any MCP-compatible AI agent to the AgentPMT tool marketplace. AgentPMT gives agents access to a dynamic catalog of tools, APIs, and services -- all controlled by budgets and spending limits.

## Prerequisites

The user needs an AgentPMT account with:
1. An **API Key** -- generated from Dashboard > Account > API Keys
2. A **Budget Key** -- generated from Dashboard > Budgets > [Select Budget] > Budget Keys

If the user does not have these, direct them to create an account at https://www.agentpmt.com and set up a budget first.

## Choose Installation Method

There are two ways to connect. Use the STDIO connector for desktop AI clients. Use the direct HTTPS endpoint for programmatic or web-based agents.

---

## Method 1: STDIO Connector (Recommended for Desktop Clients)

This method uses the `@agentpmt/mcp-router` package, a lightweight local connector that routes MCP traffic to the AgentPMT cloud. It does not access local files or execute anything on the user's machine.

### Automatic Setup

Run the interactive setup tool:

```bash
npm install -g @agentpmt/mcp-router
agentpmt-setup
```

The setup tool auto-detects installed AI platforms, prompts for credentials, writes the configuration files, and restarts the AI tools.

### Manual Setup

If automatic setup is not available or the user prefers manual configuration, follow the platform-specific instructions below.

#### Step 1: Generate the Bearer Token

Combine the API key and budget key, then base64-encode them:

```bash
echo -n "YOUR_API_KEY:YOUR_BUDGET_KEY" | base64
```

This produces the Bearer token used in all configurations below.

#### Step 2: Configure the AI Client

**Claude Desktop**

Edit the config file:
- macOS: `~/.config/Claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`

```json
{
  "mcpServers": {
    "agentpmt": {
      "command": "npx",
      "args": ["--package=@agentpmt/mcp-router@latest", "agentpmt-router"],
      "env": {
        "AGENTPMT_BEARER_TOKEN": "<your-base64-token>"
      }
    }
  }
}
```

**Claude Code**

Add to the project's `.mcp.json` or the global `~/.claude/mcp.json`:

```json
{
  "mcpServers": {
    "agentpmt": {
      "command": "npx",
      "args": ["--package=@agentpmt/mcp-router@latest", "agentpmt-router"],
      "env": {
        "AGENTPMT_BEARER_TOKEN": "<your-base64-token>"
      }
    }
  }
}
```

**Cursor**

Add to Cursor's MCP settings (Settings > MCP Servers):

```json
{
  "mcpServers": {
    "agentpmt": {
      "command": "npx",
      "args": ["--package=@agentpmt/mcp-router@latest", "agentpmt-router"],
      "env": {
        "AGENTPMT_BEARER_TOKEN": "<your-base64-token>"
      }
    }
  }
}
```

**Windsurf, VS Code, Zed, and Other MCP Clients**

Use the same universal configuration block. The only difference is where the config file lives for each client. The structure is always:

```json
{
  "command": "npx",
  "args": ["--package=@agentpmt/mcp-router@latest", "agentpmt-router"],
  "env": {
    "AGENTPMT_BEARER_TOKEN": "<your-base64-token>"
  }
}
```

#### Step 3: Restart the AI Client

After saving the configuration, restart the AI client. The AgentPMT tools should appear in the tool list within a few seconds.

---

## Method 2: Direct HTTPS Endpoint (For Programmatic Agents)

For agents that support remote MCP servers over HTTP, connect directly without the local connector.

**Endpoint:** `https://api.agentpmt.com/mcp`

**Protocol:** MCP 2.0 (JSON-RPC over streamable HTTP)

**Authentication:** Bearer token in the Authorization header.

```
Authorization: Bearer <base64-encoded-api_key:budget_key>
```

### Example: Initialize Connection

```bash
curl -X POST https://api.agentpmt.com/mcp \
  -H "Authorization: Bearer <your-base64-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 1,
    "method": "initialize",
    "params": {
      "protocolVersion": "2025-03-26",
      "clientInfo": { "name": "my-agent", "version": "1.0" },
      "capabilities": {}
    }
  }'
```

### Example: List Available Tools

```bash
curl -X POST https://api.agentpmt.com/mcp \
  -H "Authorization: Bearer <your-base64-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 2,
    "method": "tools/list",
    "params": {}
  }'
```

### Example: Call a Tool

```bash
curl -X POST https://api.agentpmt.com/mcp \
  -H "Authorization: Bearer <your-base64-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "jsonrpc": "2.0",
    "id": 3,
    "method": "tools/call",
    "params": {
      "name": "tool-name",
      "arguments": { "param1": "value1" }
    }
  }'
```

### For Clients Supporting Remote MCP URLs

Some clients (Claude Code, OpenAI agents) support remote MCP servers directly:

```json
{
  "mcpServers": {
    "agentpmt": {
      "url": "https://api.agentpmt.com/mcp",
      "headers": {
        "Authorization": "Bearer <your-base64-token>"
      }
    }
  }
}
```

---

## Verifying the Connection

After setup, verify the connection works:

1. Ask the agent to list its available tools. AgentPMT tools should appear alongside any other configured tools.
2. Look for built-in tools: `AgentPMT-Refresh-Tools` and `AgentPMT-Report-Tool-Issue` confirm the connection is active.
3. Check the AgentPMT dashboard at https://www.agentpmt.com/dashboard -- active connections appear in real time.

## Troubleshooting

**No tools appearing:**
- Verify the Bearer token is correctly base64-encoded (no trailing newlines)
- Confirm the budget has approved products -- tools only appear if the budget has vendors/products enabled
- Restart the AI client after saving config changes

**Authentication errors (401):**
- Regenerate the API key from the dashboard
- Ensure the budget key matches an active budget
- Check that the base64 encoding uses the format `api_key:budget_key` with a colon separator

**Tools listed but calls fail:**
- Check that the budget has sufficient credit balance
- Verify the specific product is approved for the budget
- Review the budget spending cap -- the agent cannot spend beyond the configured limit

## How It Works

The AgentPMT MCP server dynamically assembles a tool catalog based on the budget's permissions. Each tool includes pricing metadata so the agent knows the cost before calling. Budget limits are enforced server-side. Every tool call is logged with a full audit trail visible in the dashboard.

The local STDIO connector (`@agentpmt/mcp-router`) is a thin relay. It does not access local files, does not execute code on the user's machine, and does not cache credentials beyond the current session. All tool execution happens on AgentPMT's cloud infrastructure.

Sessions expire after 2 hours of inactivity and are automatically refreshed on each request during active use.
