---
name: mcp-setup
description: MCP server configuration and management. Use when setting up MCP servers, troubleshooting MCP issues, or adding new integrations. Keywords: MCP, model context protocol, supabase, posthog, playwright, gtm, analytics, mcp.json, environment variables, oauth
compatibility: Claude Code
metadata:
  version: "1.0"
  project: "stepleague"
  last_updated: "2026-01-24"
---

# MCP Setup Skill

## Overview

This skill handles Model Context Protocol (MCP) server configuration, troubleshooting, and integration for StepCountLeague v3. Use this when:
- Setting up new MCP servers
- Debugging MCP connection issues
- Managing authentication for MCP services
- Updating MCP configurations

## Key Files

| File | Purpose |
|------|---------|
| `.mcp.json` | Primary Claude Code MCP configuration |
| `.vscode/mcp.json` | VS Code MCP extension compatibility |
| `.env.local` | Environment variables for MCP authentication |
| `.agent/MCP.md` | Comprehensive MCP documentation |

## Configured MCP Servers

### Active Servers (5 total)

1. **Supabase MCP** - Database access
   - Type: HTTP Remote
   - Auth: Project reference in URL
   - Config: `.mcp.json`, `.vscode/mcp.json`

2. **PostHog MCP** - Analytics querying
   - Type: HTTP with Bearer token
   - Auth: `POSTHOG_MCP_TOKEN` environment variable
   - Config: `.mcp.json`, `.vscode/mcp.json`

3. **Google Tag Manager MCP** - GTM management
   - Type: stdio via mcp-remote
   - Auth: Google OAuth (browser popup)
   - Config: `.mcp.json`, `.vscode/mcp.json`

4. **Google Analytics 4 MCP** - GA4 reporting
   - Type: stdio via mcp-remote
   - Auth: Google OAuth (browser popup)
   - Config: `.mcp.json`, `.vscode/mcp.json`

5. **Playwright MCP** - Browser automation
   - Type: stdio via npx
   - Auth: None (local tool)
   - Config: `.mcp.json`, `.vscode/mcp.json`

## Critical Rules

> [!WARNING]
> **Always follow these rules when working with MCP servers:**

### 1. Never Hardcode Tokens

**❌ WRONG:**
```json
{
  "posthog": {
    "headers": {
      "Authorization": "Bearer phx_hardcoded_token_here"
    }
  }
}
```

**✅ CORRECT:**
```json
{
  "posthog": {
    "headers": {
      "Authorization": "Bearer ${POSTHOG_MCP_TOKEN}"
    }
  }
}
```

### 2. Keep Both Config Files in Sync

When adding/updating MCP servers:
1. Update `.mcp.json` (Claude Code)
2. Update `.vscode/mcp.json` (VS Code MCP extension)
3. Keep server names and configurations consistent

### 3. Document New Servers

When adding a new MCP server:
1. Add configuration to `.mcp.json`
2. Add environment variables to `.env.local` (if needed)
3. Document in `.agent/MCP.md`
4. Test with `/mcp` command in Claude Code

### 4. Use Environment Variables

All sensitive tokens must be in `.env.local`:
```env
# ❌ Never in .mcp.json
# ✅ Always in .env.local
POSTHOG_MCP_TOKEN=phx_xxx...
SUPABASE_MCP_ACCESS_TOKEN=sbp_xxx...
```

## Common Tasks

### Adding a New MCP Server

**Step 1:** Choose the server type

**HTTP Server with Bearer Token:**
```json
{
  "server-name": {
    "type": "http",
    "url": "https://api.example.com/mcp",
    "headers": {
      "Authorization": "Bearer ${SERVER_TOKEN}"
    },
    "description": "Brief description of what this server does"
  }
}
```

**stdio Server via npx:**
```json
{
  "server-name": {
    "type": "stdio",
    "command": "npx",
    "args": ["-y", "package-name@version"],
    "description": "Brief description of what this server does"
  }
}
```

**Step 2:** Add to `.mcp.json`

Edit: `D:\Vasso\coding projects\SCL v3 AG\scl-v3\.mcp.json`

**Step 3:** Add environment variables (if needed)

Edit: `D:\Vasso\coding projects\SCL v3 AG\scl-v3\.env.local`
```env
# New MCP Server
# Get from: [URL to token generation]
# Description of what the token is for
SERVER_TOKEN=xxx...
```

**Step 4:** Document the server

Edit: `D:\Vasso\coding projects\SCL v3 AG\scl-v3\.agent\MCP.md`

Add a new section describing:
- Purpose and capabilities
- Authentication method
- Environment variables used
- Official documentation links

**Step 5:** Test the connection

In Claude Code CLI:
```bash
/mcp
# Verify the server appears in the list with status
```

### Troubleshooting MCP Connection Issues

#### Issue: Server Not Listed in `/mcp`

**Diagnostic Steps:**
1. Check `.mcp.json` syntax:
   ```bash
   # Validate JSON syntax
   node -e "JSON.parse(require('fs').readFileSync('.mcp.json', 'utf8'))"
   ```

2. Verify environment variables:
   ```bash
   # Check if token is set (Windows)
   echo %POSTHOG_MCP_TOKEN%
   ```

3. Restart Claude Code CLI completely

4. Check for typos in server name

**Fix:**
- Ensure `.mcp.json` is valid JSON
- Verify environment variable names match exactly (case-sensitive)
- Check for trailing commas in JSON

#### Issue: Authentication Failed (HTTP Servers)

**Diagnostic Steps:**
1. Verify environment variable is set and loaded
2. Check token format (e.g., PostHog uses `phx_` not `phc_`)
3. Test token manually with curl:
   ```bash
   curl -H "Authorization: Bearer $POSTHOG_MCP_TOKEN" https://mcp.posthog.com/mcp
   ```

**Fix:**
- Generate new token from service provider
- Update `.env.local` with correct token
- Restart Claude Code to reload environment variables

#### Issue: OAuth Popup Blocked (GTM/GA4)

**Diagnostic Steps:**
1. Check browser popup blocker settings
2. Verify default browser is set correctly
3. Check if OAuth redirect URL is allowed

**Fix:**
- Disable popup blocker for localhost/Claude Code
- Use a different browser as default temporarily
- Clear browser cache and try again

#### Issue: npx Command Fails (Playwright)

**Diagnostic Steps:**
1. Verify npx is in PATH:
   ```bash
   where npx
   # Should return: C:\Program Files\nodejs\npx.cmd
   ```

2. Test manual execution:
   ```bash
   npx -y @executeautomation/playwright-mcp-server
   ```

3. Check internet connection (first run downloads package)

**Fix:**
- Reinstall Node.js if npx not found
- Clear npx cache: `npx clear-npx-cache`
- Check Windows Firewall settings

### Updating MCP Server Configurations

**Scenario:** Update PostHog MCP endpoint or token

**Step 1:** Update `.mcp.json`:
```json
{
  "posthog": {
    "type": "http",
    "url": "https://new-endpoint.posthog.com/mcp",
    "headers": {
      "Authorization": "Bearer ${POSTHOG_MCP_TOKEN}"
    }
  }
}
```

**Step 2:** Update `.vscode/mcp.json` to match (if needed)

**Step 3:** Update environment variable:
```env
# .env.local
POSTHOG_MCP_TOKEN=phx_new_token_here
```

**Step 4:** Restart Claude Code CLI

**Step 5:** Verify with `/mcp`

### Rotating MCP Tokens

**Best Practice:** Rotate tokens every 90 days

**Step 1:** Generate new token from service provider:
- PostHog: https://app.posthog.com/settings/user-api-keys
- Supabase: https://supabase.com/dashboard/account/tokens

**Step 2:** Update `.env.local`:
```env
# Old token (keep temporarily for rollback)
# POSTHOG_MCP_TOKEN=phx_old_token

# New token
POSTHOG_MCP_TOKEN=phx_new_token
```

**Step 3:** Test connection

**Step 4:** Delete old token from provider once confirmed working

**Step 5:** Remove old token comment from `.env.local`

## Verification Checklist

After any MCP configuration changes:

- [ ] `.mcp.json` is valid JSON
- [ ] Environment variables set in `.env.local`
- [ ] Both `.mcp.json` and `.vscode/mcp.json` updated (if applicable)
- [ ] Documentation updated in `.agent/MCP.md`
- [ ] Claude Code CLI restarted
- [ ] `/mcp` command shows server with ✅ status
- [ ] Server tools loadable via ToolSearch
- [ ] Test query/command executed successfully

## Environment Variable Reference

Current MCP-related environment variables:

```env
# Supabase MCP (optional - project_ref provides read-only)
SUPABASE_MCP_ACCESS_TOKEN=sbp_xxx...

# PostHog MCP (required for MCP server)
# NOTE: Different from app token (phc_ prefix)
POSTHOG_MCP_TOKEN=phx_xxx...

# No environment variables needed for:
# - Google Tag Manager MCP (OAuth)
# - Google Analytics 4 MCP (OAuth)
# - Playwright MCP (local tool)
```

## Server Configuration Template

Use this template when adding new MCP servers:

```json
{
  "mcpServers": {
    "existing-servers": "...",

    "new-server-name": {
      "type": "http|stdio",
      "url": "https://api.example.com/mcp",
      "command": "npx",
      "args": ["-y", "package-name"],
      "headers": {
        "Authorization": "Bearer ${ENV_VAR_NAME}"
      },
      "env": {
        "CUSTOM_ENV": "${CUSTOM_ENV_VAR}"
      },
      "description": "Clear description of server purpose"
    }
  }
}
```

**Choose type:**
- `http` - For HTTP/HTTPS MCP servers
- `stdio` - For command-line MCP servers (npx, python, etc.)

**HTTP servers need:**
- `url` - The MCP endpoint URL
- `headers` (optional) - Authentication headers
- `description` - Brief purpose description

**stdio servers need:**
- `command` - The executable (e.g., "npx", "python")
- `args` - Command arguments
- `env` (optional) - Environment variables for the command
- `description` - Brief purpose description

## Windows-Specific Notes

### Path Handling
- Use forward slashes: `/` not `\`
- Environment variables: `${VAR_NAME}`
- User profile: `${USERPROFILE}` or `%USERPROFILE%`

### Command Execution
- npx commands run via Git Bash (if available)
- Claude Code handles Windows/Unix path translation
- No need for `cmd /c` prefix

### OAuth Flows
- Default browser must be set in Windows
- OAuth redirects to localhost
- Check Windows Firewall for localhost blocking

### Debugging
```bash
# Check environment variable (PowerShell)
$env:POSTHOG_MCP_TOKEN

# Check environment variable (Git Bash)
echo $POSTHOG_MCP_TOKEN

# List environment variables
env | grep MCP
```

## Related Skills

- **supabase-patterns** - Using Supabase MCP for database operations
- **analytics-tracking** - Integrating PostHog/GA4 MCP for analytics queries
- **testing-patterns** - Using Playwright MCP for E2E testing

## References

**Documentation:**
- `.agent/MCP.md` - Comprehensive MCP documentation
- `CLAUDE.md` - Project context including MCP servers

**External Resources:**
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [Claude Code MCP Docs](https://docs.anthropic.com/en/docs/claude-code/mcp)
- [MCP Registry](https://mcp.directory/)

**Configured Servers:**
- [Supabase MCP](https://supabase.com/docs/guides/getting-started/mcp)
- [PostHog MCP](https://posthog.com/docs/model-context-protocol)
- [Stape GTM MCP](https://stape.io/helpdesk/documentation/how-to-set-up-mcp-server-for-gtm)
- [Stape GA4 MCP](https://stape.io/helpdesk/documentation/how-to-set-up-mcp-server-for-ga4)
- [Playwright MCP](https://github.com/executeautomation/mcp-playwright)

---

**Version:** 1.0
**Last Updated:** 2026-01-24
**Compatibility:** Claude Code
**Project:** StepCountLeague v3
