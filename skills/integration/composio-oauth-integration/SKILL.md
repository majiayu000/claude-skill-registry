---
name: composio-oauth-integration
description: Composio OAuth integration for external service connections. CSRF-protected flow with state management, connection lifecycle transitions (pending→initiated→active), dynamic tool building from active connections, token expiration handling. Triggers on "composio", "oauth", "integration", "connection", "external service", "third-party".
---

# Composio OAuth Integration

Connect external services (GitHub, Slack, etc.) via Composio OAuth with CSRF protection and dynamic tool registration.

## OAuth Flow

### Initiate Connection

```typescript
// From convex/composio/oauth.ts
export const initiateConnection = action({
  args: { integrationId: v.string(), redirectUrl: v.string() },
  handler: async (ctx, { integrationId, redirectUrl }) => {
    // 1. Get user
    const user = await ctx.runQuery(api.users.getUserByClerkId, { clerkId });

    // 2. Check integration limit (before creating new connection)
    const existingConnection = await ctx.runQuery(
      api.composio.connections.getConnectionByIntegration,
      { integrationId }
    );

    if (!existingConnection) {
      const activeConnections = await ctx.runQuery(
        api.composio.connections.getActiveConnections
      );
      if (activeConnections.length >= maxIntegrations) {
        throw new Error("Integration limit reached");
      }
    }

    // 3. Generate CSRF state (32 bytes)
    const oauthState = randomBytes(32).toString("hex");

    // 4. Create unique entity ID
    const composioUserId = `blahchat_${user._id}`;

    // 5. Initiate with Composio
    const connectionRequest = await composio.connectedAccounts.initiate(
      composioUserId,
      authConfigId,
      { callbackUrl: redirectUrl, allowMultiple: true }
    );

    // 6. Store in DB with state (expires in 10 min)
    await ctx.runMutation(internal.composio.connections.createConnection, {
      userId: user._id,
      composioConnectionId: connectionRequest.id,
      integrationId,
      oauthState,
      // stateExpiresAt: now + 10min (set in mutation)
    });

    return {
      redirectUrl: connectionRequest.redirectUrl,
      state: oauthState // Return to frontend for verification
    };
  }
});
```

**Key patterns:**
- CSRF state: 32-byte hex (not UUID), expires 10 min
- Entity ID format: `blahchat_${userId}` (matches across flows)
- `allowMultiple: true` enables re-auth without losing active status
- Check limit BEFORE creating new connection, skip for re-auth

### Verify Connection (Callback)

```typescript
// From convex/composio/oauth.ts
export const verifyConnection = action({
  args: { composioConnectionId: v.string(), state: v.optional(v.string()) },
  handler: async (ctx, { composioConnectionId, state }) => {
    // 1. Get connection from DB
    const existingConnection = await ctx.runQuery(
      internal.composio.connections.getConnectionByComposioId,
      { composioConnectionId }
    );

    // 2. SECURITY: Verify ownership
    if (existingConnection.userId !== user._id) {
      throw new Error("Unauthorized: Connection belongs to another user");
    }

    // 3. SECURITY: Validate CSRF state
    if (existingConnection.oauthState) {
      if (!state) throw new Error("Missing state parameter");
      if (state !== existingConnection.oauthState) {
        throw new Error("Invalid state parameter - possible CSRF attack");
      }
      if (Date.now() > existingConnection.oauthStateExpiresAt) {
        throw new Error("OAuth state expired - please try again");
      }
    }

    // 4. Check status with Composio
    const connection = await composio.connectedAccounts.get(composioConnectionId);

    if (connection.status === "ACTIVE") {
      await ctx.runMutation(
        internal.composio.connections.updateConnectionStatus,
        { composioConnectionId, status: "active" }
      );
      return { status: "active" };
    }

    // Handle pending/failed states
    const status = connection.status === "INITIATED" ? "initiated" : "failed";
    await ctx.runMutation(
      internal.composio.connections.updateConnectionStatus,
      { composioConnectionId, status, error: ... }
    );

    return { status };
  }
});
```

**CSRF validation:**
- Check `oauthState` field exists in DB
- Verify state matches callback parameter
- Enforce 10-minute expiration
- Backwards compatible (optional state for old connections)

## Connection Status Lifecycle

**States:** `pending` | `initiated` | `active` | `expired` | `failed`

**Transitions:**
```
pending → initiated (OAuth flow starts)
initiated → active (OAuth completes successfully)
active → expired (token refresh fails during tool execution)
initiated → failed (OAuth flow fails)
active → active (re-auth preserves status if user cancels popup)
```

**Status preservation during re-auth:**
```typescript
// From convex/composio/connections.ts (createConnection mutation)
if (existing) {
  await ctx.db.patch(existing._id, {
    composioConnectionId: args.composioConnectionId,
    status: existing.status === "active" ? "active" : "initiated",
    // ^ Preserve active status during re-auth
    oauthState: args.oauthState,
    oauthStateExpiresAt: stateExpiresAt,
    lastError: undefined, // Clear previous error
  });
  return existing._id;
}
```

**Why preserve:** User clicks "Manage" button → popup opens → popup canceled → connection still works. Don't break tools during re-auth attempt.

## Dynamic Tool Building

```typescript
// From convex/composio/tools.ts
export async function createComposioTools(
  ctx: ActionCtx,
  config: { userId: Id<"users">; connections: Doc<"composioConnections">[] }
) {
  // 1. Filter to active connections only
  const activeConnections = config.connections.filter(c => c.status === "active");

  if (activeConnections.length === 0) {
    return { tools: {}, connectedApps: [] };
  }

  // 2. Initialize Composio with Vercel provider
  const composio = new Composio({
    apiKey: process.env.COMPOSIO_API_KEY,
    provider: new VercelProvider() // Vercel AI SDK compatible
  });

  // 3. Create entity ID (must match OAuth flow)
  const entityId = `blahchat_${userId}`;

  // 4. Get toolkits (lowercase integration IDs)
  const connectedToolkits = activeConnections.map(c => c.integrationId.toLowerCase());

  // 5. Fetch tools from Composio
  const tools = await composio.tools.get(entityId, {
    toolkits: connectedToolkits,
    limit: 100
  });

  // 6. Wrap tools to track usage and handle errors
  const wrappedTools: Record<string, unknown> = {};

  for (const [name, originalTool] of Object.entries(tools)) {
    wrappedTools[name] = {
      ...tool,
      execute: async (...args: unknown[]) => {
        // Update lastUsedAt timestamp
        const appName = name.split("_")[0]; // "GITHUB_CREATE_ISSUE" → "GITHUB"
        const connection = activeConnections.find(
          c => c.integrationId.toUpperCase() === appName.toUpperCase()
        );

        if (connection) {
          await ctx.runMutation(
            internal.composio.connections.markConnectionUsed,
            { connectionId: connection._id }
          );
        }

        try {
          return await tool.execute!(...args);
        } catch (error) {
          // Handle expired tokens
          if (error.message.includes("expired") ||
              error.message.includes("401") ||
              error.message.includes("unauthorized")) {

            // Mark connection as expired
            await ctx.runMutation(
              internal.composio.connections.updateConnectionStatus,
              {
                composioConnectionId: connection.composioConnectionId,
                status: "expired",
                error: "Token expired - please reconnect"
              }
            );

            throw new Error(
              `${appName} connection expired. Please reconnect in Settings > Integrations.`
            );
          }
          throw error;
        }
      }
    };
  }

  return {
    tools: wrappedTools,
    connectedApps: activeConnections.map(c => c.integrationName)
  };
}
```

**Integration with generation:**
```typescript
// From convex/generation/tools.ts
export async function buildToolsAsync(config: BuildToolsConfig) {
  const tools = buildTools(config); // Base tools (Tavily, calculator, etc.)
  let connectedApps: string[] = [];

  // Add Composio tools if not incognito and connections exist
  if (!isIncognito && composioConnections?.length > 0) {
    const composioResult = await createComposioTools(ctx, {
      userId,
      connections: composioConnections.filter(c => c.status === "active")
    });

    Object.assign(tools, composioResult.tools); // Merge into tools object
    connectedApps = composioResult.connectedApps; // For system prompt
  }

  return { tools, connectedApps };
}
```

## Auth Config Management

```typescript
// From convex/composio/oauth.ts
const authConfigCache = new Map<string, string>();

async function getOrCreateAuthConfig(composio: Composio, integrationId: string) {
  // 1. Check cache
  const cached = authConfigCache.get(integrationId);
  if (cached) return cached;

  // 2. Normalize to lowercase (Composio SDK requirement)
  const normalizedToolkit = integrationId.toLowerCase();

  // 3. Try to list existing configs
  try {
    const configs = await composio.authConfigs.list({ toolkit: normalizedToolkit });
    if (configs?.items?.length > 0) {
      const configId = configs.items[0].id;
      authConfigCache.set(integrationId, configId);
      return configId;
    }
  } catch {
    // Config doesn't exist, create one
  }

  // 4. Create auth config (Composio managed)
  const config = await composio.authConfigs.create(normalizedToolkit, {
    name: `blahchat_${normalizedToolkit}`,
    type: "use_composio_managed_auth" // Use Composio's OAuth credentials
  });

  const configId = config.id;
  authConfigCache.set(integrationId, configId);
  return configId;
}
```

**Cache strategy:** In-memory Map, no expiration. Auth config IDs stable across restarts. If Composio changes config ID, cache miss creates new config (idempotent).

## Integration Limits

```typescript
// From convex/composio/connections.ts
export const getIntegrationLimits = query({
  handler: async (ctx) => {
    const connections = await ctx.db
      .query("composioConnections")
      .withIndex("by_user", q => q.eq("userId", user._id))
      .collect();

    const activeCount = connections.filter(c => c.status === "active").length;

    // Get max from admin settings (default: 5)
    const adminSettings = await ctx.db.query("adminSettings").first();
    const maxIntegrations = adminSettings?.maxActiveIntegrations ?? 5;

    return {
      current: activeCount,
      max: maxIntegrations,
      canAddMore: activeCount < maxIntegrations
    };
  }
});
```

**Enforcement:** Check limit in `initiateConnection` action BEFORE creating new connection. Skip check for re-auth (existing connection found).

## Disconnect Flow

```typescript
// From convex/composio/oauth.ts
export const revokeConnection = action({
  handler: async (ctx, { integrationId }) => {
    const connection = await ctx.runQuery(
      api.composio.connections.getConnectionByIntegration,
      { integrationId }
    );

    // 1. Delete from Composio (best effort)
    if (process.env.COMPOSIO_API_KEY) {
      try {
        await composio.connectedAccounts.delete(connection.composioConnectionId);
      } catch {
        console.warn(`Failed to delete Composio connection for ${integrationId}`);
        // Continue - still clean up locally
      }
    }

    // 2. Delete local record (always happens)
    await ctx.runMutation(
      api.composio.connections.disconnectIntegration,
      { integrationId }
    );

    return { success: true };
  }
});
```

**Best effort deletion:** If Composio API fails, still delete local record. User can re-auth if needed.

## Key Files

- `packages/backend/convex/composio/oauth.ts` - OAuth flow actions (initiate, verify, refresh, revoke)
- `packages/backend/convex/composio/connections.ts` - Connection CRUD queries/mutations
- `packages/backend/convex/composio/tools.ts` - Dynamic tool building from active connections
- `packages/backend/convex/generation/tools.ts` - Integration with main tool builder

## Error Patterns

**Expired tokens during tool execution:**
```typescript
// Catch 401/expired errors, mark connection as expired
if (error.message.includes("expired") || error.message.includes("401")) {
  await ctx.runMutation(updateConnectionStatus, {
    composioConnectionId: connection.composioConnectionId,
    status: "expired",
    error: "Token expired - please reconnect"
  });
  throw new Error(`${appName} connection expired. Please reconnect in Settings > Integrations.`);
}
```

**OAuth flow failures:**
```typescript
// Check Composio status, update local status
const connection = await composio.connectedAccounts.get(composioConnectionId);
if (connection.status === "FAILED") {
  await ctx.runMutation(updateConnectionStatus, {
    composioConnectionId,
    status: "failed",
    error: "OAuth flow failed"
  });
}
```

## Avoid

- Don't skip CSRF state validation (critical security)
- Don't use UUID for state (use randomBytes for crypto randomness)
- Don't forget entity ID format: `blahchat_${userId}` (must match OAuth and tools)
- Don't lowercase integration ID in DB (only for Composio SDK calls)
- Don't check limit during re-auth (breaks "Manage" button workflow)
- Don't fail disconnect if Composio API fails (local cleanup always happens)
- Don't create tools from non-active connections (status must be "active")
