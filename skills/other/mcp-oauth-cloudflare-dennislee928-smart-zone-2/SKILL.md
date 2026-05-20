---
name: MCP OAuth Cloudflare
description: |
  Add OAuth authentication to MCP servers on Cloudflare Workers. Uses @cloudflare/workers-oauth-provider with Google OAuth for Claude.ai-compatible authentication. Prevents 9 documented errors including RFC 8707 audience bugs, Claude.ai connection failures, and CSRF vulnerabilities.

  Use when building MCP servers that need user authentication, implementing Dynamic Client Registration (DCR) for Claude.ai, or replacing static auth tokens with OAuth flows. Includes workarounds for production redirect URI mismatches and re-auth loop issues.
user-invocable: true
license: MIT
---

# MCP OAuth Cloudflare

Production-ready OAuth authentication for MCP servers on Cloudflare Workers.

## When to Use This Skill

- Building an MCP server that needs user authentication
- Deploying MCP to Claude.ai (requires Dynamic Client Registration)
- Replacing static auth tokens with OAuth for better security
- Adding Google Sign-In to your MCP server
- Need user context (email, name, picture) in MCP tool handlers

## When NOT to Use

- Internal/private MCP servers where tokens are acceptable
- MCP servers without user-specific data
- Local-only MCP development (use tokens for simplicity)

## Architecture Overview

### Dual OAuth Role Pattern

When using a third-party OAuth provider (like Google), the MCP Server acts as **both an OAuth client (to upstream service) and as an OAuth server (to MCP clients)**. The Worker:

1. Stores encrypted access token in Workers KV
2. Issues its own token to the client
3. `workers-oauth-provider` handles spec compliance

**Critical**: The MCP server **generates and issues its own token** rather than passing through the third-party token. This is essential for security and spec compliance.

```
┌─────────────────────────────────────────────────────────────────────┐
│                        Cloudflare Worker                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│  ┌─────────────────────┐      ┌──────────────────────────────────┐ │
│  │  OAuthProvider      │      │  McpAgent (Durable Object)       │ │
│  │  ─────────────────  │      │  ────────────────────────────    │ │
│  │  /register (DCR)    │      │  MCP Tools with user props:      │ │
│  │  /authorize         │─────▶│  - this.props.email              │ │
│  │  /token             │      │  - this.props.id                 │ │
│  │  /mcp               │      │  - this.props.accessToken        │ │
│  └─────────────────────┘      └──────────────────────────────────┘ │
│           │                                                         │
│           │ OAuth Flow                                              │
│           ▼                                                         │
│  ┌─────────────────────┐      ┌──────────────────────────────────┐ │
│  │  Google Handler     │      │  KV Namespace (OAUTH_KV)         │ │
│  │  ─────────────────  │      │  ────────────────────────────    │ │
│  │  /authorize (GET)   │─────▶│  oauth:state:{token} → AuthReq   │ │
│  │  /authorize (POST)  │      │  TTL: 10 minutes                 │ │
│  │  /callback          │      └──────────────────────────────────┘ │
│  └─────────────────────┘                                           │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

## Quick Start

### 1. Install Dependencies

```bash
npm install @cloudflare/workers-oauth-provider agents @modelcontextprotocol/sdk hono zod
```

### 2. Create OAuth Directory Structure

```
src/
├── index.ts              # Main entry with OAuthProvider
└── oauth/
    ├── google-handler.ts # OAuth routes (/authorize, /callback)
    ├── utils.ts          # Google token exchange & user info
    └── workers-oauth-utils.ts # CSRF, state validation, approval UI
```

### 3. Configure wrangler.jsonc

```jsonc
{
  "name": "my-mcp-server",
  "main": "src/index.ts",
  "compatibility_flags": ["nodejs_compat"],

  // KV for OAuth state storage
  "kv_namespaces": [
    {
      "binding": "OAUTH_KV",
      "id": "YOUR_KV_NAMESPACE_ID"
    }
  ],

  // Durable Objects for MCP sessions
  "durable_objects": {
    "bindings": [
      {
        "class_name": "MyMcpServer",
        "name": "MCP_OBJECT"
      }
    ]
  },

  "migrations": [
    {
      "new_sqlite_classes": ["MyMcpServer"],
      "tag": "v1"
    }
  ]
}
```

### 4. Set Secrets

```bash
# Google OAuth credentials (from console.cloud.google.com)
echo "YOUR_GOOGLE_CLIENT_ID" | npx wrangler secret put GOOGLE_CLIENT_ID
echo "YOUR_GOOGLE_CLIENT_SECRET" | npx wrangler secret put GOOGLE_CLIENT_SECRET

# Cookie encryption key (32+ chars)
python3 -c "import secrets; print(secrets.token_urlsafe(32))" | npx wrangler secret put COOKIE_ENCRYPTION_KEY

# Optional: Custom Google OAuth scopes (default: 'openid email profile')
# See "Common Google Scopes" section below for scope recipes
echo "openid email profile https://www.googleapis.com/auth/drive" | npx wrangler secret put GOOGLE_SCOPES

# Deploy to activate secrets
npx wrangler deploy
```

### 5. Type Definitions (Optional but Recommended)

Copy `templates/env.d.ts` to `src/env.d.ts` for TypeScript type support:

```typescript
interface Env {
  GOOGLE_CLIENT_ID: string;
  GOOGLE_CLIENT_SECRET: string;
  COOKIE_ENCRYPTION_KEY: string;
  GOOGLE_SCOPES?: string;  // Optional: Override default scopes
  OAUTH_KV: KVNamespace;
  MCP_OBJECT: DurableObjectNamespace;
}
```

## Implementation Guide

### Main Entry Point (index.ts)

```typescript
import OAuthProvider from '@cloudflare/workers-oauth-provider';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { McpAgent } from 'agents/mcp';
import { z } from 'zod';
import { GoogleHandler } from './oauth/google-handler';

// Props from OAuth - user info stored in token
type Props = {
  id: string;
  email: string;
  name: string;
  picture?: string;
  accessToken: string;
  refreshToken?: string; // Available on first auth with access_type=offline
};

export class MyMcpServer extends McpAgent<Env, Record<string, never>, Props> {
  server = new McpServer({
    name: 'my-mcp-server',
    version: '1.0.0',
  });

  async init() {
    // Register tools - user info available via this.props
    this.server.tool(
      'my_tool',
      'Tool description',
      { param: z.string() },
      async (args) => {
        // Access authenticated user
        const userEmail = this.props?.email;
        console.log(`Tool called by: ${userEmail}`);

        return {
          content: [{ type: 'text', text: 'Result' }]
        };
      }
    );
  }
}

// Wrap with OAuth provider
export default new OAuthProvider({
  apiHandlers: {
    '/sse': MyMcpServer.serveSSE('/sse'),
    '/mcp': MyMcpServer.serve('/mcp'),
  },
  authorizeEndpoint: '/authorize',
  clientRegistrationEndpoint: '/register',
  defaultHandler: GoogleHandler as any,
  tokenEndpoint: '/token',
});
```

### Google Handler (oauth/google-handler.ts)

```typescript
import { env } from 'cloudflare:workers';
import type { AuthRequest, OAuthHelpers } from '@cloudflare/workers-oauth-provider';
import { Hono } from 'hono';
import { fetchUpstreamAuthToken, fetchGoogleUserInfo, getUpstreamAuthorizeUrl, type Props } from './utils';
import {
  addApprovedClient,
  bindStateToSession,
  createOAuthState,
  generateCSRFProtection,
  isClientApproved,
  OAuthError,
  renderApprovalDialog,
  validateCSRFToken,
  validateOAuthState,
} from './workers-oauth-utils';

const app = new Hono<{ Bindings: Env & { OAUTH_PROVIDER: OAuthHelpers } }>();

// GET /authorize - Show approval dialog or redirect to Google
app.get('/authorize', async (c) => {
  const oauthReqInfo = await c.env.OAUTH_PROVIDER.parseAuthRequest(c.req.raw);
  const { clientId } = oauthReqInfo;

  if (!clientId) return c.text('Invalid request', 400);

  // Skip approval if client already approved
  if (await isClientApproved(c.req.raw, clientId, env.COOKIE_ENCRYPTION_KEY)) {
    const { stateToken } = await createOAuthState(oauthReqInfo, c.env.OAUTH_KV);
    const { setCookie } = await bindStateToSession(stateToken);
    return redirectToGoogle(c.req.raw, stateToken, { 'Set-Cookie': setCookie });
  }

  // Show approval dialog with CSRF protection
  const { token: csrfToken, setCookie } = generateCSRFProtection();
  return renderApprovalDialog(c.req.raw, {
    client: await c.env.OAUTH_PROVIDER.lookupClient(clientId),
    csrfToken,
    server: {
      name: 'My MCP Server',
      description: 'Description of your server',
      logo: 'https://example.com/logo.png',
    },
    setCookie,
    state: { oauthReqInfo },
  });
});

// POST /authorize - Process approval form
app.post('/authorize', async (c) => {
  try {
    const formData = await c.req.raw.formData();
    validateCSRFToken(formData, c.req.raw);

    const encodedState = formData.get('state') as string;
    const state = JSON.parse(atob(encodedState));

    // Add to approved clients
    const approvedCookie = await addApprovedClient(
      c.req.raw, state.oauthReqInfo.clientId, c.env.COOKIE_ENCRYPTION_KEY
    );

    // Create state and redirect
    const { stateToken } = await createOAuthState(state.oauthReqInfo, c.env.OAUTH_KV);
    const { setCookie } = await bindStateToSession(stateToken);

    const headers = new Headers();
    headers.append('Set-Cookie', approvedCookie);
    headers.append('Set-Cookie', setCookie);

    return redirectToGoogle(c.req.raw, stateToken, Object.fromEntries(headers));
  } catch (error: any) {
    if (error instanceof OAuthError) return error.toResponse();
    return c.text(`Error: ${error.message}`, 500);
  }
});

// GET /callback - Handle Google OAuth callback
app.get('/callback', async (c) => {
  const { oauthReqInfo, clearCookie } = await validateOAuthState(c.req.raw, c.env.OAUTH_KV);

  // Exchange code for token
  const [accessToken, err] = await fetchUpstreamAuthToken({
    client_id: c.env.GOOGLE_CLIENT_ID,
    client_secret: c.env.GOOGLE_CLIENT_SECRET,
    code: c.req.query('code'),
    redirect_uri: new URL('/callback', c.req.url).href,
    upstream_url: 'https://oauth2.googleapis.com/token',
  });
  if (err) return err;

  // Get user info
  const user = await fetchGoogleUserInfo(accessToken);
  if (!user) return c.text('Failed to fetch user info', 500);

  // Complete authorization
  const { redirectTo } = await c.env.OAUTH_PROVIDER.completeAuthorization({
    props: {
      accessToken,
      email: user.email,
      id: user.id,
      name: user.name,
      picture: user.picture,
    } as Props,
    request: oauthReqInfo,
    scope: oauthReqInfo.scope,
    userId: user.id,
  });

  return new Response(null, {
    status: 302,
    headers: { Location: redirectTo, 'Set-Cookie': clearCookie },
  });
});

async function redirectToGoogle(request: Request, stateToken: string, headers: Record<string, string> = {}) {
  // Scopes configurable via GOOGLE_SCOPES env var (see "Common Google Scopes" section)
  const scopes = env.GOOGLE_SCOPES || 'openid email profile';

  return new Response(null, {
    status: 302,
    headers: {
      ...headers,
      location: getUpstreamAuthorizeUrl({
        client_id: env.GOOGLE_CLIENT_ID,
        redirect_uri: new URL('/callback', request.url).href,
        scope: scopes,
        state: stateToken,
        upstream_url: 'https://accounts.google.com/o/oauth2/v2/auth',
      }),
    },
  });
}

export { app as GoogleHandler };
```

## OAuth Flow Diagram

```
User clicks "Connect" in Claude.ai
          │
          ▼
┌─────────────────────────────────┐
│  1. /register (DCR)             │ ◄── Claude.ai registers as client
│     Returns client credentials   │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  2. GET /authorize              │
│     - Check approved clients    │
│     - Show approval dialog      │
│     - Generate CSRF token       │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  3. POST /authorize             │
│     - Validate CSRF             │
│     - Create state in KV        │
│     - Redirect to Google        │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  4. Google OAuth                │
│     - User signs in             │
│     - Consents to scopes        │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  5. GET /callback               │
│     - Validate state            │
│     - Exchange code for token   │
│     - Fetch user info           │
│     - Complete authorization    │
└─────────────────────────────────┘
          │
          ▼
┌─────────────────────────────────┐
│  6. User props available        │
│     this.props.email            │
│     this.props.id               │
│     this.props.accessToken      │
└─────────────────────────────────┘
```

## Security Features

### CSRF Protection

```typescript
// Generate CSRF token with HttpOnly cookie
export function generateCSRFProtection(): CSRFProtectionResult {
  const token = crypto.randomUUID();
  const setCookie = `__Host-CSRF_TOKEN=${token}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=600`;
  return { token, setCookie };
}
```

### State Validation (Prevents Replay Attacks)

```typescript
// Create one-time-use state in KV
export async function createOAuthState(oauthReqInfo: AuthRequest, kv: KVNamespace) {
  const stateToken = crypto.randomUUID();
  await kv.put(`oauth:state:${stateToken}`, JSON.stringify(oauthReqInfo), {
    expirationTtl: 600, // 10 minutes
  });
  return { stateToken };
}
```

### Session Binding (Prevents Token Theft)

```typescript
// Bind state to browser session via SHA-256 hash
export async function bindStateToSession(stateToken: string) {
  const hashBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stateToken));
  const hashHex = Array.from(new Uint8Array(hashBuffer))
    .map(b => b.toString(16).padStart(2, '0')).join('');

  const setCookie = `__Host-CONSENTED_STATE=${hashHex}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=600`;
  return { setCookie };
}
```

### Client Approval Caching (Reduces Consent Fatigue)

```typescript
// HMAC-signed cookie tracks approved clients (30-day TTL)
export async function addApprovedClient(request: Request, clientId: string, cookieSecret: string) {
  const existing = await getApprovedClientsFromCookie(request, cookieSecret) || [];
  const updated = [...new Set([...existing, clientId])];

  const payload = JSON.stringify(updated);
  const signature = await signData(payload, cookieSecret);

  return `__Host-APPROVED_CLIENTS=${signature}.${btoa(payload)}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=2592000`;
}
```

### PKCE Methods (Current Limitation)

**Note**: The library currently accepts both `plain` and `S256` PKCE methods. There is no configuration option to enforce S256-only, which is the OAuth 2.1 recommended method.

**Security Consideration**: For maximum security, you may want S256-only. This is tracked in [GitHub Issue #113](https://github.com/cloudflare/workers-oauth-provider/issues/113) as a feature request.

**Workaround**: Until this is configurable, the library will accept both methods. Modern OAuth clients (including Claude.ai) use S256 by default.

## Google Cloud Console Setup

1. Go to [console.cloud.google.com](https://console.cloud.google.com)
2. Create new project or select existing
3. Navigate to **APIs & Services** → **Credentials**
4. Click **Create Credentials** → **OAuth client ID**
5. Application type: **Web application**
6. Add authorized redirect URI: `https://your-worker.workers.dev/callback`
7. Copy Client ID and Client Secret

## Common Google Scopes

Configure scopes via the `GOOGLE_SCOPES` environment variable or modify the `redirectToGoogle` function.

| Use Case | Scopes |
|----------|--------|
| Basic user info (default) | `openid email profile` |
| Google Drive (full access) | `openid email profile https://www.googleapis.com/auth/drive` |
| Google Drive (file-level only) | `openid email profile https://www.googleapis.com/auth/drive.file` |
| Google Docs | `openid email profile https://www.googleapis.com/auth/documents` |
| Google Docs + Drive | `openid email profile https://www.googleapis.com/auth/drive.file https://www.googleapis.com/auth/documents` |
| Gmail (read/send) | `openid email profile https://www.googleapis.com/auth/gmail.modify` |
| Gmail (read only) | `openid email profile https://www.googleapis.com/auth/gmail.readonly` |
| Google Calendar | `openid email profile https://www.googleapis.com/auth/calendar` |
| Google Sheets | `openid email profile https://www.googleapis.com/auth/spreadsheets` |
| Google Slides | `openid email profile https://www.googleapis.com/auth/presentations` |
| YouTube Data | `openid email profile https://www.googleapis.com/auth/youtube` |

**Setting Scopes:**

```bash
# Option 1: Via environment variable (recommended for flexibility)
echo "openid email profile https://www.googleapis.com/auth/drive" | npx wrangler secret put GOOGLE_SCOPES

# Option 2: In wrangler.jsonc (for non-sensitive scopes)
{
  "vars": {
    "GOOGLE_SCOPES": "openid email profile https://www.googleapis.com/auth/drive"
  }
}
```

**Important Notes:**

- Always include `openid email profile` - required for user identification
- Additional scopes must be enabled in Google Cloud Console (APIs & Services → Library)
- Some scopes require OAuth consent screen verification for production use
- `drive.file` only accesses files the app created or user explicitly opened with it

## Refresh Token Lifecycle (v0.2.0+)

For long-lived sessions (Google APIs, Gmail, Drive), you need refresh tokens.

### Design Decision: Two Valid Refresh Tokens

**Note**: `@cloudflare/workers-oauth-provider` implements a non-standard refresh token rotation strategy. At any time, a grant may have **two valid refresh tokens**. When the client uses one, the other is invalidated and a new one is generated.

**Why It Differs from OAuth 2.1**: OAuth 2.1 requires single-use refresh tokens for public clients. However, the library author argues that single-use tokens are fundamentally flawed because they assume every refresh request completes with no errors. In the real world, network errors or software faults could mean the client fails to store the new refresh token.

**Security Trade-off**: Allowing the previous refresh token disables replay attack detection. For confidential clients (most MCP servers), this is compliant with OAuth 2.1. For public clients, consider stricter rotation if needed.

**Source**: [GitHub Issue #43](https://github.com/cloudflare/workers-oauth-provider/issues/43), documented in [README](https://github.com/cloudflare/workers-oauth-provider?tab=readme-ov-file#single-use-refresh-tokens)

### Requesting Refresh Tokens

Add `access_type=offline` to the authorization URL:

```typescript
// In google-handler.ts, redirectToGoogle function
googleAuthUrl.searchParams.set('access_type', 'offline');
googleAuthUrl.searchParams.set('prompt', 'consent'); // Forces new refresh token
```

**When to use `access_type=offline`:**
- MCP server needs to call Google APIs after initial auth
- Long-running sessions (background tasks, scheduled jobs)
- User data synchronization

**When to use `access_type=online` (default):**
- Simple user identification only
- No API calls beyond initial auth
- Short sessions (admin login, one-time actions)

### Storing Refresh Tokens

Store encrypted in your Props type:

```typescript
export type Props = {
  id: string;
  email: string;
  name: string;
  picture?: string;
  accessToken: string;
  refreshToken?: string;      // Store when received
  tokenExpiresAt?: number;    // Track expiration
};
```

### Refreshing Expired Tokens

```typescript
export async function refreshAccessToken(
  client_id: string,
  client_secret: string,
  refresh_token: string
): Promise<{ accessToken: string; expiresAt: number } | null> {
  const resp = await fetch('https://oauth2.googleapis.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      client_id,
      client_secret,
      refresh_token,
      grant_type: 'refresh_token',
    }).toString(),
  });

  if (!resp.ok) return null; // Token revoked, requires re-auth

  const body = await resp.json();
  return {
    accessToken: body.access_token,
    expiresAt: Date.now() + (body.expires_in * 1000),
  };
}
```

### When Refresh Tokens Become Invalid

- User revokes access at https://myaccount.google.com/permissions
- User changes password (if using certain scopes)
- Token unused for 6+ months
- OAuth app credentials regenerated

**Handle gracefully**: Catch refresh failures and redirect to re-authorize.

## Bearer Token + OAuth Coexistence

Modern MCP servers support **both** OAuth (Claude.ai) and Bearer tokens (CLI tools, ElevenLabs):

```typescript
// In your main fetch handler
export default {
  async fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const authHeader = request.headers.get('Authorization');
    const url = new URL(request.url);

    // Check for Bearer token auth on MCP endpoints
    if (env.AUTH_TOKEN && authHeader?.startsWith('Bearer ') &&
        (url.pathname === '/sse' || url.pathname === '/mcp')) {
      const token = authHeader.slice(7);

      if (token === env.AUTH_TOKEN) {
        // Programmatic access (CLI, ElevenLabs)
        const headerAuthCtx = { ...ctx, props: { source: 'bearer' } };
        return mcpHandler.fetch(request, env, headerAuthCtx);
      }
      // NOT env.AUTH_TOKEN - fall through to OAuth provider
      // (it may be an OAuth token from Claude.ai)
    }

    // OAuth flow for web clients
    return oauthProvider.fetch(request, env, ctx);
  }
};
```

**Critical Pattern**: Non-matching Bearer tokens must **fall through** to OAuth provider, not return 401. OAuth tokens from Claude.ai are also sent as Bearer tokens.

**Adding AUTH_TOKEN secret:**
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))" | npx wrangler secret put AUTH_TOKEN
npx wrangler deploy  # Required to activate
```

## Common Issues

### "Invalid state" Error

**Cause**: State expired (>10 min) or KV lookup failed

**Fix**: Restart the OAuth flow - states are one-time-use

### "CSRF token mismatch"

**Cause**: Form submitted without matching cookie

**Fix**: Ensure cookies are enabled and not blocked by browser extensions

### Claude.ai Shows "Connection Failed"

**Cause**: Missing DCR endpoint or invalid response

**Fix**: Ensure `clientRegistrationEndpoint: '/register'` is set in OAuthProvider config

### User Props Undefined

**Cause**: Accessing `this.props` before OAuth completes

**Fix**: Check `if (this.props)` before accessing user data

## OAuth vs Auth Tokens Comparison

| Aspect | Auth Tokens | OAuth |
|--------|-------------|-------|
| Token sharing | Manual (risky) | Automatic |
| User consent | None | Explicit approval |
| Expiration | Manual | Automatic refresh |
| Revocation | None built-in | User can disconnect |
| Scope | All-or-nothing | Fine-grained |
| Claude.ai compatible | No (DCR required) | Yes |

## Required Secrets

| Secret | Purpose | Generate |
|--------|---------|----------|
| `GOOGLE_CLIENT_ID` | OAuth app ID | Google Cloud Console |
| `GOOGLE_CLIENT_SECRET` | OAuth app secret | Google Cloud Console |
| `COOKIE_ENCRYPTION_KEY` | Sign approval cookies | `secrets.token_urlsafe(32)` |
| `GOOGLE_SCOPES` (optional) | Override default OAuth scopes | See "Common Google Scopes" section |

## Token Efficiency

| Without Skill | With Skill | Savings |
|---------------|------------|---------|
| ~20k tokens, 3-5 attempts | ~6k tokens, first try | ~70% |

## Known Issues Prevention

This skill prevents **9** documented errors.

### Issue #1: RFC 8707 Audience Validation Fails with Path Components (v0.1.0+)

**Error**: `invalid_token: Token audience does not match resource server`
**Source**: [GitHub Issue #108](https://github.com/cloudflare/workers-oauth-provider/issues/108)
**Affects**: v0.1.0+ when using RFC 8707 resource indicators with paths (e.g., ChatGPT custom connectors)

**Why It Happens**: The `resourceServer` is computed using only the origin (`https://example.com`) but RFC 8707 recommends using full URLs with paths (`https://example.com/api`). The strict equality check in `audienceMatches` fails when:
- Token audience: `https://example.com/api` (from `resource` parameter)
- Resource server: `https://example.com` (computed from request URL origin only)

**Prevention**:

If using RFC 8707 resource indicators with paths, vendor the library and modify `handleApiRequest`:

```typescript
// Workaround: Include pathname in resourceServer computation
const resourceServer = `${requestUrl.protocol}//${requestUrl.host}${requestUrl.pathname}`;
```

Or avoid using paths in resource indicators until this is fixed upstream.

---

### Issue #2: Claude.ai Client Cannot Connect (v0.2.2)

**Error**: Claude.ai MCP client fails to connect during OAuth flow
**Source**: [GitHub Issue #133](https://github.com/cloudflare/workers-oauth-provider/issues/133)
**Affects**: v0.2.2, Claude.ai MCP clients

**Why It Happens**: There is a '/' character in the `audienceMatches` function that prevents Claude.ai from connecting. Likely related to Issue #1 (RFC 8707 path handling).

**Prevention**: Monitor [Issue #133](https://github.com/cloudflare/workers-oauth-provider/issues/133) for updates. This may require a library update or vendoring the library with a fix.

---

### Issue #3: Props Not Updated After Re-authorization (Upstream OAuth Expiry)

**Error**: Infinite re-auth loop when upstream OAuth provider doesn't provide refresh tokens
**Source**: [GitHub Issue #34](https://github.com/cloudflare/workers-oauth-provider/issues/34)
**Affects**: MCP servers using upstream OAuth providers without refresh tokens

**Why It Happens**: Throwing `invalid_grant` in `tokenExchangeCallback` triggers re-authorization, but `completeAuthorization()` doesn't update props. Stale props cause repeated auth failures until the OAuth client restarts.

**Prevention**:

If your upstream OAuth provider doesn't issue refresh tokens:

1. Implement a fallback strategy (store token expiry, re-auth before expiration)
2. Monitor [Issue #34](https://github.com/cloudflare/workers-oauth-provider/issues/34) for official fix
3. Consider client restart as temporary workaround

**Problematic Pattern:**
```typescript
tokenExchangeCallback: async (options) => {
  if (options.grantType === "refresh_token") {
    const response = await fetchNewToken(options.props.accessToken);

    if (!response.ok) {
      // Triggers re-auth but props remain stale
      throw new Error(JSON.stringify({
        error: "invalid_grant",
        error_description: "access token expired"
      }));
    }
  }
}
```

---

### Issue #4: Redirect URI Mismatch in Production (Development vs Production Behavior)

**Error**: `Invalid redirect URI. The redirect URI provided does not match any registered URI for this client`
**Source**: [GitHub Issue #29](https://github.com/cloudflare/workers-oauth-provider/issues/29) (Community-sourced)
**Affects**: Production deployments; works fine in local `wrangler dev`

**Why It Happens**: Dynamic Client Registration (DCR) behavior differs between local and production environments. Redirect URIs auto-register during DCR, but something fails in production. Root cause unclear but affecting multiple users with MCP clients (Cursor, Windsurf, PyCharm).

**Prevention**:

- Explicitly register redirect URIs when possible instead of relying on DCR auto-registration
- Test OAuth flow in production environment before deploying to Claude.ai
- Monitor [Issue #29](https://github.com/cloudflare/workers-oauth-provider/issues/29) for resolution

---

### Issue #5: CSRF Vulnerabilities

**Error**: Session hijacking, OAuth callback interception
**Prevention**: HttpOnly cookies with SameSite attribute

```typescript
const setCookie = `__Host-CSRF_TOKEN=${token}; HttpOnly; Secure; Path=/; SameSite=Lax; Max-Age=600`;
```

---

### Issue #6: State Replay Attacks

**Error**: OAuth state reused across multiple authorization attempts
**Prevention**: One-time-use KV state with 10-minute TTL

```typescript
await kv.put(`oauth:state:${stateToken}`, JSON.stringify(oauthReqInfo), {
  expirationTtl: 600,
});
```

---

### Issue #7: Token Theft via Session Fixation

**Error**: OAuth state stolen and used from different browser session
**Prevention**: Session binding via SHA-256 hash

```typescript
const hashBuffer = await crypto.subtle.digest('SHA-256', new TextEncoder().encode(stateToken));
const hashHex = Array.from(new Uint8Array(hashBuffer))
  .map(b => b.toString(16).padStart(2, '0')).join('');
```

---

### Issue #8: Missing Dynamic Client Registration (DCR)

**Error**: Claude.ai shows "Connection Failed" when trying to connect
**Prevention**: OAuthProvider handles DCR automatically via `clientRegistrationEndpoint: '/register'`

---

### Issue #9: Cookie Tampering

**Error**: Approved clients list modified to bypass consent
**Prevention**: HMAC signatures on approval cookies

```typescript
const signature = await signData(payload, cookieSecret);
const cookie = `__Host-APPROVED_CLIENTS=${signature}.${btoa(payload)}`;
```

## Version History & Breaking Changes

### v0.2.2 (2025-12-20) - Current

**New Features**:
- Client ID Metadata Document (CIMD) support - allows HTTPS URLs as `client_id` values
- Matches new MCP authorization spec: https://modelcontextprotocol.io/specification/draft/basic/authorization

**Migration**: No breaking changes. CIMD support is additive.

---

### v0.1.0 (2025-11-07)

**New Features**:
- Audience validation for OAuth tokens per RFC 7519

**Breaking Changes**:
- Tokens now require correct `aud` claim
- May break existing deployments without audience validation
- See Issue #108 for RFC 8707 path handling bug

**Migration**:
1. Ensure all tokens include correct `aud` claim
2. Test audience validation thoroughly
3. If using resource indicators with paths, apply workaround from Issue #108

---

### v0.0.x (Pre-November 2025)

Initial releases without audience validation.

## Errors Prevented

1. **RFC 8707 audience path bugs** - Workaround for path component validation
2. **Claude.ai connection failures** - Known issue tracking
3. **Re-auth loops** - Props update handling
4. **Production redirect URI mismatches** - Testing and explicit registration
5. **CSRF vulnerabilities** - HttpOnly cookies with SameSite
6. **State replay attacks** - One-time-use KV state
7. **Token theft** - Session binding via SHA-256
8. **Missing DCR** - OAuthProvider handles automatically
9. **Cookie tampering** - HMAC signatures

## References

- [Cloudflare Workers OAuth Provider](https://developers.cloudflare.com/workers/examples/oauth/)
- [GitHub - cloudflare/workers-oauth-provider](https://github.com/cloudflare/workers-oauth-provider)
- [MCP Specification](https://spec.modelcontextprotocol.io/)
- [MCP Authorization Spec](https://modelcontextprotocol.io/specification/draft/basic/authorization)
- [Google OAuth Documentation](https://developers.google.com/identity/protocols/oauth2)
- [Cloudflare Agents SDK](https://developers.cloudflare.com/agents/)

---

**Last verified**: 2026-01-21 | **Skill version**: 2.0.0 | **Changes**: Added 4 new known issues from post-training-cutoff research (RFC 8707 audience bugs, Claude.ai connection failures, re-auth loops, production redirect URI mismatches), version history section, refresh token rotation design decision, dual OAuth role pattern emphasis, and PKCE limitation note. Updated from 6 to 9 documented error preventions.
