---
name: mcp-setup
description: MCP server configuration, troubleshooting, and Todoist REST API workarounds
---

# MCP Server Configuration

## Configuration Locations
- **User-level config**: `~/.claude/settings.json` (required for VSCode extension)
- **Project-level config**: `.mcp.json` (may not be loaded by VSCode extension)
- **Environment file**: `~/.claude/.env` (copy from project `.env`)

## Important Setup Notes

1. **Node.js Required**: Install via `brew install node` (needed for all MCP servers using npx)

2. **Use Full Paths**: VSCode may not have Homebrew in PATH, so use `/opt/homebrew/bin/npx` instead of just `npx`

3. **No Variable Interpolation**: The `${VAR}` syntax does NOT work in `~/.claude/settings.json`. You must hardcode actual token values.

4. **Restart Required**: After changing `~/.claude/settings.json`, fully quit VSCode (Cmd+Q) and reopen. A simple reload may not pick up changes.

5. **OAuth for Google Services**: First run of gdrive/gcal will open browser for authentication. Tokens cached in `~/.mcp-gdrive/` or similar.

## MCP Server Packages

| Server | Package | Env Variable |
|--------|---------|--------------|
| todoist | `@abhiz123/todoist-mcp-server` | `TODOIST_API_TOKEN` |
| notion | `@notionhq/notion-mcp-server` | `NOTION_TOKEN` |
| ccg-bot | `@modelcontextprotocol/server-slack` | `SLACK_BOT_TOKEN` |
| astra-bot | `@modelcontextprotocol/server-slack` | `ASTRA_SLACK_BOT_TOKEN` |
| gdrive | `@isaacphi/mcp-gdrive` | `GOOGLE_OAUTH_CREDENTIALS` (path to OAuth keys) |
| gcal | `@anthropic/mcp-gcal` | `GCAL_OAUTH_PATH` (path to OAuth keys) |
| github | `@modelcontextprotocol/server-github` | `GITHUB_TOKEN` |

**Note**: The gdrive package is `@isaacphi/mcp-gdrive`, NOT `@anthropic/mcp-gdrive` (that one doesn't exist on npm).

## Example ~/.claude/settings.json

```json
{
  "mcpServers": {
    "gdrive": {
      "command": "/opt/homebrew/bin/npx",
      "args": ["-y", "@isaacphi/mcp-gdrive"],
      "env": {
        "GOOGLE_OAUTH_CREDENTIALS": "/Users/terrytong/Documents/CCG/ToolProj/gcp-oauth.keys.json"
      }
    },
    "todoist": {
      "command": "/opt/homebrew/bin/npx",
      "args": ["-y", "@abhiz123/todoist-mcp-server"],
      "env": {
        "TODOIST_API_TOKEN": "your-actual-token-here"
      }
    },
    "notion": {
      "command": "/opt/homebrew/bin/npx",
      "args": ["-y", "@notionhq/notion-mcp-server"],
      "env": {
        "NOTION_TOKEN": "your-actual-token-here"
      }
    }
  }
}
```

## Troubleshooting MCP

| Error | Solution |
|-------|----------|
| "Failed to connect" | Check Node.js: `/opt/homebrew/bin/node --version` |
| 401 Unauthorized | Tokens cached from old config. Fully restart VSCode |
| Package not found | Search npm: `/opt/homebrew/bin/npm search mcp <service>` |
| OAuth issues | Run manually: `GOOGLE_OAUTH_CREDENTIALS=<path> /opt/homebrew/bin/npx -y @isaacphi/mcp-gdrive` |

Pre-install packages globally: `/opt/homebrew/bin/npm install -g @isaacphi/mcp-gdrive @abhiz123/todoist-mcp-server`

## Todoist REST API Workaround

The Todoist MCP tool often returns 401 errors. **Use the REST API directly via curl instead**:

```bash
# Create a task (source .env first to get TODOIST_API_TOKEN)
source /Users/terrytong/Documents/CCG/ToolProj/.env && curl -s -X POST "https://api.todoist.com/rest/v2/tasks" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "content": "Task title here",
    "project_id": "2363714490",
    "due_string": "today"
  }'

# Delete a task
source /Users/terrytong/Documents/CCG/ToolProj/.env && curl -s -X DELETE "https://api.todoist.com/rest/v2/tasks/{task_id}" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"

# Get tasks
source /Users/terrytong/Documents/CCG/ToolProj/.env && curl -s "https://api.todoist.com/rest/v2/tasks?project_id=2363714490" \
  -H "Authorization: Bearer $TODOIST_API_TOKEN"
```

**Key**: Always `source .env` before curl commands since MCP servers don't pick up bash exports.
