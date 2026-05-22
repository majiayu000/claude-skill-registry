---
name: google-oauth-integration
description: 'Complete Google OAuth integration architecture including token storage and debugging'
---

# Google OAuth Integration

This skill documents the complete Google OAuth integration architecture in Orient, including token storage, tool registration, and debugging procedures.

## Triggers

Use this skill when:

- Setting up Google OAuth for a new package or service
- Debugging "Unknown tool" errors for Google tools (Calendar, Gmail, Tasks)
- Understanding token storage and refresh mechanics
- Adding new Google service tools to the ToolExecutorRegistry

## Token Storage Architecture

### Token File Location

Google OAuth tokens are stored in JSON files at:

```
{cwd}/data/oauth-tokens/google-oauth.json
```

**CRITICAL**: The path is resolved using `process.cwd()`, meaning different packages look in different locations:

- Dashboard: `packages/dashboard/data/oauth-tokens/google-oauth.json`
- Slack bot: `packages/bot-slack/data/oauth-tokens/google-oauth.json`
- WhatsApp bot: `packages/bot-whatsapp/data/oauth-tokens/google-oauth.json`
- Project root: `data/oauth-tokens/google-oauth.json`

### Symlink Setup (Required for Multi-Package Access)

Since the dashboard is typically where users connect their Google accounts, other packages need symlinks to access the same tokens:

```bash
# For bot-slack
mkdir -p packages/bot-slack/data/oauth-tokens
ln -sf $(pwd)/packages/dashboard/data/oauth-tokens/google-oauth.json \
       packages/bot-slack/data/oauth-tokens/google-oauth.json

# For bot-whatsapp
mkdir -p packages/bot-whatsapp/data/oauth-tokens
ln -sf $(pwd)/packages/dashboard/data/oauth-tokens/google-oauth.json \
       packages/bot-whatsapp/data/oauth-tokens/google-oauth.json

# For project root (used by MCP servers)
mkdir -p data/oauth-tokens
ln -sf $(pwd)/packages/dashboard/data/oauth-tokens/google-oauth.json \
       data/oauth-tokens/google-oauth.json
```

### Token File Structure

```json
{
  "accounts": {
    "user@gmail.com": {
      "email": "user@gmail.com",
      "displayName": "User Name",
      "accessToken": "ya29...",
      "refreshToken": "1//...",
      "expiresAt": 1768578677699,
      "scopes": [
        "https://www.googleapis.com/auth/calendar",
        "https://www.googleapis.com/auth/gmail.modify"
      ],
      "connectedAt": 1768552923717,
      "lastRefreshAt": 1768575078699
    }
  },
  "pendingStates": {}
}
```

## Environment Variables

Required environment variables in `.env`:

```bash
# OAuth Client Credentials (from Google Cloud Console)
GOOGLE_OAUTH_CLIENT_ID=<your-client-id>.apps.googleusercontent.com
GOOGLE_OAUTH_CLIENT_SECRET=GOCSPX-<your-secret>

# Callback URL (must match Google Cloud Console)
GOOGLE_OAUTH_CALLBACK_URL=http://localhost/api/auth/google/callback
```

The OAuth service loads credentials in this priority order:

1. Secrets database (`GOOGLE_OAUTH_CLIENT_ID`, `GOOGLE_OAUTH_CLIENT_SECRET`)
2. Environment variables
3. Credentials file: `credentials/client_secret_*.json`

## Tool Registration Architecture

### Two Registration Systems

Orient has two tool registration systems:

1. **ToolRegistry** (Discovery only)
   - Location: `packages/agents/src/services/toolRegistry.ts`
   - Used by: `discover_tools` for listing available tools
   - Does NOT execute tools

2. **ToolExecutorRegistry** (Execution)
   - Location: `packages/agents/src/services/toolRegistry.ts`
   - Used by: `executeToolCallFromRegistry()` in `packages/mcp-servers/src/tool-executor.ts`
   - Actually runs the tool code

### Registering New Google Tools

To add a new Google tool, register it in the `registerGoogleToolHandlers()` function:

```typescript
// In packages/agents/src/services/toolRegistry.ts

function registerGoogleToolHandlers(registry: ToolExecutorRegistry): void {
  const registerHandlers = async () => {
    const { getCalendarService, getGoogleOAuthService } =
      await import('@orientbot/integrations/google');

    // Register handler
    registry.registerHandler('google_calendar_list_events', async (args) => {
      const calendar = getCalendarService();
      const events = await calendar.listEvents(options, accountEmail);
      return createToolResult(JSON.stringify(events, null, 2));
    });
  };

  void registerHandlers();
}
```

### Legacy vs Modern Registration

| Aspect   | Legacy (mcp-server.ts)                   | Modern (ToolExecutorRegistry)                  |
| -------- | ---------------------------------------- | ---------------------------------------------- |
| Location | `packages/mcp-servers/src/mcp-server.ts` | `packages/agents/src/services/toolRegistry.ts` |
| Pattern  | Giant switch statement                   | Handler registration                           |
| Used by  | Direct MCP server                        | assistant-server via base-server               |
| Status   | Deprecated                               | Preferred                                      |

**Important**: The assistant-server (used by Slack/WhatsApp bots) uses `base-server.ts` which ONLY uses `ToolExecutorRegistry`. It does NOT fall back to the legacy switch statement unless `setLegacyExecutor()` is called.

## Token Refresh Mechanics

The OAuth service in `packages/integrations/src/google/oauth.ts` handles automatic token refresh:

```typescript
async getAuthClient(email: string): Promise<Auth.OAuth2Client> {
  const account = this.data.accounts[email];

  // Check if token needs refresh (expired or expiring in < 5 min)
  if (Date.now() > account.expiresAt - 5 * 60 * 1000) {
    const { credentials } = await client.refreshAccessToken();
    account.accessToken = credentials.access_token;
    account.expiresAt = credentials.expiry_date;
    this.saveData();
  }

  return client;
}
```

Key points:

- Tokens are refreshed automatically 5 minutes before expiration
- Requires valid `refresh_token` from initial OAuth consent
- Requires OAuth credentials (client ID/secret) to be accessible

## Debugging "Unknown Tool" Errors

When Google tools return `{"error":"Unknown tool: google_calendar_list_events"}`:

### Step 1: Check Tool Discovery

```bash
# Tool should appear in discover_tools output
curl -X POST http://localhost:4099/... -d '{"tool":"discover_tools","args":{"mode":"search","query":"calendar"}}'
```

If tool appears in discovery but not execution, it's registered in ToolRegistry but not ToolExecutorRegistry.

### Step 2: Check ToolExecutorRegistry Registration

Look for the tool in `packages/agents/src/services/toolRegistry.ts`:

```typescript
// Should see this in registerGoogleToolHandlers():
registry.registerHandler('google_calendar_list_events', async (args) => { ... });
```

### Step 3: Verify Build and Restart

```bash
# Rebuild affected packages
pnpm --filter @orientbot/agents build
pnpm --filter @orientbot/mcp-servers build

# Copy to root dist (used by OpenCode)
cp packages/mcp-servers/dist/*.js dist/mcp-servers/

# Kill existing MCP server processes
ps aux | grep "assistant-server\|coding-server" | grep -v grep | awk '{print $2}' | xargs kill

# OpenCode will spawn fresh processes on next tool call
```

### Step 4: Check MCP Server Logs

```bash
tail -f logs/mcp-debug-*.log | grep -i "calendar\|google\|unknown"
```

Look for:

- `"Registered tool"` - Tool was registered
- `"Unknown tool"` - Tool not found in any executor
- Error messages during handler registration

## Common Issues

### Issue: Tokens not found

**Symptom**: "No Google account connected"
**Cause**: Token file not found at CWD path
**Fix**: Create symlinks as documented above

### Issue: Token refresh fails

**Symptom**: "Failed to refresh token"
**Cause**: OAuth credentials not accessible
**Fix**: Ensure GOOGLE_OAUTH_CLIENT_ID and GOOGLE_OAUTH_CLIENT_SECRET are set

### Issue: Tool returns "Unknown tool"

**Symptom**: `{"error":"Unknown tool: google_calendar_list_events"}`
**Cause**: Tool not registered in ToolExecutorRegistry
**Fix**: Add handler in `registerGoogleToolHandlers()` and rebuild

### Issue: Stale MCP server

**Symptom**: Changes not taking effect
**Cause**: Old MCP server process still running
**Fix**: Kill old processes, OpenCode will spawn new ones

## Files Reference

| File                                           | Purpose                                 |
| ---------------------------------------------- | --------------------------------------- |
| `packages/integrations/src/google/oauth.ts`    | OAuth service, token storage            |
| `packages/integrations/src/google/calendar.ts` | Calendar service implementation         |
| `packages/agents/src/services/toolRegistry.ts` | Tool discovery + executor registration  |
| `packages/mcp-servers/src/tool-executor.ts`    | Tool execution entry point              |
| `packages/mcp-servers/src/base-server.ts`      | MCP server using executor registry      |
| `packages/mcp-servers/src/mcp-server.ts`       | Legacy MCP server with switch statement |
