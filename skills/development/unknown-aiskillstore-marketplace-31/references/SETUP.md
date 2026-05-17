# Raindrop.io MCP Server Setup Guide

This guide will help you configure the official Raindrop.io MCP server to work with your AI client.

## Prerequisites

Before starting, ensure you have:

1. **Raindrop.io Pro Subscription**
   - The official MCP server requires a Pro account ($28/year)
   - Check your subscription at https://app.raindrop.io/settings/account
   - Upgrade if needed at https://raindrop.io/pro

2. **Compatible AI Client**
   - Claude.ai (web version)
   - Claude Desktop
   - Claude Code
   - Chat GPT (Plus, Pro, Business, or Enterprise)
   - Cursor
   - Windsurf
   - VS Code (with MCP extension)
   - Zed
   - Or any other MCP-compatible client

## Quick Start

The fastest way to get started depends on your client:

- **Claude.ai users**: Go directly to step 1 below
- **Claude Desktop/Code users**: Skip to step 2
- **ChatGPT users**: Skip to step 3
- **Other clients**: Skip to step 4

## Step 1: Claude.ai Setup

If you're using Claude.ai (the web version):

1. Open https://claude.ai
2. Click on your profile icon (bottom left)
3. Select **Settings**
4. Navigate to **Connectors** section
5. Click **Add connector**
6. Paste this URL:
   ```
   https://api.raindrop.io/rest/v2/ai/mcp
   ```
7. Click **Continue**
8. You'll be redirected to Raindrop.io to authorize access
9. Log in to your Raindrop.io account
10. Click **Authorize** to grant permission
11. You'll be redirected back to Claude.ai
12. The connector should now show as **Connected**

### Verification
To verify the connection:
- Start a new conversation
- Type: "List my available tools"
- You should see Raindrop.io MCP tools in the list

## Step 2: Claude Desktop / Claude Code Setup

For Claude Desktop or Claude Code (VS Code extension):

### Option A: Using `mcp-remote` (Recommended)

1. Ensure you have Node.js installed (v18 or later)
2. Open your MCP configuration file:
   - **macOS**: `~/.config/claude/claude_desktop_config.json`
   - **Windows**: `%APPDATA%\Claude\claude_desktop_config.json`
   - **Linux**: `~/.config/claude/claude_desktop_config.json`

3. Add the Raindrop.io server configuration:
   ```json
   {
     "mcpServers": {
       "raindrop": {
         "command": "npx",
         "args": ["-y", "mcp-remote", "https://api.raindrop.io/rest/v2/ai/mcp"]
       }
     }
   }
   ```

4. Save the file
5. Restart Claude Desktop/Code
6. On first use, your browser will open for OAuth authorization
7. Log in to Raindrop.io and authorize access

### Option B: Alternative Configuration

If you prefer a different approach, you can also use:

```json
{
  "mcpServers": {
    "raindrop": {
      "command": "node",
      "args": [
        "-e",
        "require('mcp-remote')('https://api.raindrop.io/rest/v2/ai/mcp')"
      ]
    }
  }
}
```

### Verification
1. Open Claude Desktop/Code
2. Start a new conversation
3. Commands/Tools menu should show Raindrop.io tools
4. Try listing your collections to verify connection

## Step 3: ChatGPT Setup

For ChatGPT (requires Plus, Pro, Business, or Enterprise subscription):

1. Open https://chat.openai.com
2. Go to **Settings** (bottom left)
3. Navigate to **Apps** section
4. Click **Advanced**
5. Enable **Developer mode**
6. Click **Create new app**
7. Choose **Create manually**
8. Fill in the details:
   - **Name**: Raindrop.io
   - **Description**: Bookmark management
   - **Server URL**: `https://api.raindrop.io/rest/v2/ai/mcp`
   - **Transport**: SSE (Server-Sent Events)
9. Click **Create**
10. Click **Connect** on the new app
11. Your browser will open for OAuth authorization
12. Log in to Raindrop.io and authorize access
13. Return to ChatGPT

### Verification
- Start a new chat
- Tools menu should show Raindrop.io capabilities
- Try a simple operation like listing collections

## Step 4: Other Clients (Cursor, Windsurf, VS Code, Zed)

For other MCP-compatible clients, you'll need to add configuration. The exact format varies by client.

### Cursor

Edit your Cursor settings:

```json
{
  "mcpServers": {
    "raindrop": {
      "type": "sse",
      "url": "https://api.raindrop.io/rest/v2/ai/mcp"
    }
  }
}
```

### Windsurf

Similar to Cursor, add to your settings:

```json
{
  "mcp": {
    "servers": {
      "raindrop": {
        "url": "https://api.raindrop.io/rest/v2/ai/mcp",
        "transport": "sse"
      }
    }
  }
}
```

### VS Code (with MCP extension)

Install the MCP extension, then add to settings.json:

```json
{
  "mcp.servers": {
    "raindrop": {
      "url": "https://api.raindrop.io/rest/v2/ai/mcp",
      "type": "sse"
    }
  }
}
```

### Zed

Edit your Zed configuration:

```json
{
  "extensions": {
    "mcp": {
      "servers": {
        "raindrop": {
          "url": "https://api.raindrop.io/rest/v2/ai/mcp",
          "transport": "sse"
        }
      }
    }
  }
}
```

**Note**: Exact configuration may vary by client version. Consult your client's MCP documentation for the latest format.

## Alternative: API Token Authentication

If OAuth doesn't work for your setup, you can use a personal API token:

### Getting Your API Token

1. Go to https://app.raindrop.io/settings/integrations
2. Click **Create new app**
3. Give it a name (e.g., "MCP Access")
4. Click **Create**
5. Copy the **Test token** shown
6. Keep this token secure!

### Using the Token

Add the token to your MCP configuration as an environment variable:

**Claude Desktop (macOS/Linux)**:
```json
{
  "mcpServers": {
    "raindrop": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://api.raindrop.io/rest/v2/ai/mcp"],
      "env": {
        "RAINDROP_TOKEN": "your-token-here"
      }
    }
  }
}
```

**Important**: Never commit configuration files with tokens to version control!

## Troubleshooting

### "MCP server not found"

**Cause**: Configuration file not in the correct location or format invalid

**Solutions**:
- Double-check the file path for your OS
- Validate JSON syntax (use a JSON validator)
- Ensure no trailing commas in JSON
- Restart your client after changes

### "Authorization failed"

**Cause**: OAuth flow didn't complete or token invalid

**Solutions**:
- Clear your browser cookies for raindrop.io
- Try the authorization flow again
- Check that you're logged into the correct Raindrop.io account
- Verify your Pro subscription is active
- Try using API token authentication instead

### "Node.js not found"

**Cause**: Node.js not installed or not in PATH

**Solutions**:
- Install Node.js from https://nodejs.org (LTS version recommended)
- Restart your terminal/client after installing
- Verify with: `node --version` (should show v18+)

### "Tools not appearing"

**Cause**: Server not properly connected or configured

**Solutions**:
- Check your client's logs for error messages
- Verify the MCP server URL is correct
- Try removing and re-adding the configuration
- Restart your client completely
- Check that your Pro subscription is active

### "Rate limiting errors"

**Cause**: Too many requests to Raindrop.io API

**Solutions**:
- The official MCP server should handle rate limiting automatically
- If you see errors, wait a few minutes before trying again
- Raindrop.io API limits are 120 requests per minute per user
- Contact Raindrop.io support if problems persist

### "Connection timeout"

**Cause**: Network issues or server unavailable

**Solutions**:
- Check your internet connection
- Verify https://api.raindrop.io is accessible
- Check Raindrop.io status page for outages
- Try again in a few minutes
- Check firewall/proxy settings

## Beta Limitations

The official Raindrop.io MCP server is currently in **beta**. This means:

- Features may change or be added over time
- Some operations might not work as expected
- Documentation may be updated frequently
- Report issues to info@raindrop.io

## Security Best Practices

1. **OAuth is recommended** over API tokens when possible
2. **Never share** your API token or commit it to repositories
3. **Use environment variables** for tokens in configuration
4. **Review permissions** granted during OAuth authorization
5. **Revoke access** at https://app.raindrop.io/settings/integrations if needed

## Getting Help

- **Raindrop.io MCP documentation**: https://help.raindrop.io/mcp
- **Raindrop.io support**: info@raindrop.io
- **Model Context Protocol docs**: https://modelcontextprotocol.io
- **Claude Desktop config help**: https://docs.anthropic.com/claude/docs

## Next Steps

Once your MCP server is configured:

1. Return to [SKILL.md](../SKILL.md) to learn how to use the skill
2. Check [API-REFERENCE.md](API-REFERENCE.md) for tool details
3. Explore [WORKFLOWS.md](WORKFLOWS.md) for advanced examples

---

**Last updated**: 2025-02-18
**Raindrop.io MCP Server**: Beta
**Minimum Pro subscription**: Required