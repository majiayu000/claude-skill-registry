---
name: configuring-better-auth
description: |
  Implement OAuth 2.1 / OIDC authentication using Better Auth with MCP assistance. Use when setting
  up a centralized auth server (SSO provider), implementing SSO clients in Next.js apps, configuring
  PKCE flows, or managing tokens with JWKS verification. Uses Better Auth MCP for guided setup.
  NOT when using simple session-only auth without OAuth/OIDC requirements.
---

# Better Auth OAuth/OIDC

Implement centralized authentication with Better Auth - either as an auth server or SSO client.

## MCP Server Setup

Better Auth provides an MCP server powered by Chonkie for guided configuration:

```bash
claude mcp add --transport http better-auth https://mcp.chonkie.ai/better-auth/better-auth-builder/mcp
```

Or in `settings.json`:

```json
{
  "mcpServers": {
    "better-auth": {
      "type": "http",
      "url": "https://mcp.chonkie.ai/better-auth/better-auth-builder/mcp"
    }
  }
}
```

### When to Use the MCP

| Task | Use MCP? |
|------|----------|
| Initial Better Auth setup | Yes - guided configuration |
| Adding OIDC provider plugin | Yes - generates correct config |
| Troubleshooting auth issues | Yes - can analyze setup |
| Understanding auth flow | Yes - explains concepts |
| Writing custom middleware | No - use patterns below |

---

## Architecture Overview

```
┌─────────────────┐
│ Better Auth SSO │ ← Central auth server (auth-server-setup.md)
│  (Auth Server)  │
└────────┬────────┘
         │
    ┌────┴────┐
    ▼         ▼
┌───────┐  ┌───────┐
│ App 1 │  │ App 2 │ ← SSO clients (sso-client-integration.md)
└───────┘  └───────┘
```

---

## Quick Start: Auth Server Setup

```bash
npm install better-auth @better-auth/oidc-provider drizzle-orm
```

### Core Configuration

```typescript
// src/lib/auth.ts
import { betterAuth } from "better-auth";
import { drizzleAdapter } from "better-auth/adapters/drizzle";
import { oidcProvider } from "better-auth/plugins/oidc-provider";

export const auth = betterAuth({
  database: drizzleAdapter(db, { provider: "pg", schema }),
  emailAndPassword: { enabled: true },
  session: {
    expiresIn: 60 * 60 * 24 * 7, // 7 days
    updateAge: 60 * 60 * 24,     // 1 day
  },
  plugins: [
    oidcProvider({
      loginPage: "/sign-in",
      consentPage: "/consent",
      // PKCE for public clients (recommended)
      requirePKCE: true,
    }),
  ],
});
```

### Register OAuth Clients

```typescript
// Register SSO client
await auth.api.createOAuthClient({
  name: "My App",
  redirectUris: ["http://localhost:3000/api/auth/callback"],
  type: "public", // Use 'public' for PKCE
});
```

See [references/auth-server-setup.md](references/auth-server-setup.md) for complete setup with JWKS, email verification, and admin dashboard.

---

## Quick Start: SSO Client Integration

```bash
npm install jose
```

### Environment Variables

```env
NEXT_PUBLIC_SSO_URL=http://localhost:3001
NEXT_PUBLIC_SSO_CLIENT_ID=your-client-id
```

### PKCE Auth Flow

```typescript
// lib/auth-client.ts
import { generateCodeVerifier, generateCodeChallenge } from "./pkce";

export async function startLogin() {
  const verifier = generateCodeVerifier();
  const challenge = await generateCodeChallenge(verifier);

  // Store verifier in cookie
  document.cookie = `pkce_verifier=${verifier}; path=/; SameSite=Lax`;

  const params = new URLSearchParams({
    client_id: process.env.NEXT_PUBLIC_SSO_CLIENT_ID!,
    redirect_uri: `${window.location.origin}/api/auth/callback`,
    response_type: "code",
    scope: "openid profile email",
    code_challenge: challenge,
    code_challenge_method: "S256",
  });

  window.location.href = `${SSO_URL}/oauth2/authorize?${params}`;
}
```

### Token Exchange (API Route)

```typescript
// app/api/auth/callback/route.ts
export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get("code");
  const verifier = cookies().get("pkce_verifier")?.value;

  const response = await fetch(`${SSO_URL}/oauth2/token`, {
    method: "POST",
    headers: { "Content-Type": "application/x-www-form-urlencoded" },
    body: new URLSearchParams({
      grant_type: "authorization_code",
      client_id: process.env.NEXT_PUBLIC_SSO_CLIENT_ID!,
      code: code!,
      redirect_uri: `${process.env.NEXT_PUBLIC_APP_URL}/api/auth/callback`,
      code_verifier: verifier!,
    }),
  });

  const tokens = await response.json();

  // Set httpOnly cookies
  const res = NextResponse.redirect("/dashboard");
  res.cookies.set("access_token", tokens.access_token, { httpOnly: true });
  res.cookies.set("refresh_token", tokens.refresh_token, { httpOnly: true });
  return res;
}
```

See [references/sso-client-integration.md](references/sso-client-integration.md) for JWKS verification, token refresh, and global logout.

---

## PKCE Utilities

```typescript
// lib/pkce.ts
export function generateCodeVerifier(): string {
  const array = new Uint8Array(32);
  crypto.getRandomValues(array);
  return base64UrlEncode(array);
}

export async function generateCodeChallenge(verifier: string): Promise<string> {
  const encoder = new TextEncoder();
  const data = encoder.encode(verifier);
  const hash = await crypto.subtle.digest("SHA-256", data);
  return base64UrlEncode(new Uint8Array(hash));
}

function base64UrlEncode(buffer: Uint8Array): string {
  return btoa(String.fromCharCode(...buffer))
    .replace(/\+/g, "-")
    .replace(/\//g, "_")
    .replace(/=+$/, "");
}
```

---

## Key Patterns

### 1. Token Storage
- Store tokens in **httpOnly cookies** (not localStorage)
- Use SameSite=Lax for CSRF protection

### 2. Token Refresh
```typescript
async function refreshTokens() {
  const response = await fetch(`${SSO_URL}/oauth2/token`, {
    method: "POST",
    body: new URLSearchParams({
      grant_type: "refresh_token",
      client_id: process.env.NEXT_PUBLIC_SSO_CLIENT_ID!,
      refresh_token: currentRefreshToken,
    }),
  });
  return response.json();
}
```

### 3. JWKS Verification
```typescript
import { createRemoteJWKSet, jwtVerify } from "jose";

const JWKS = createRemoteJWKSet(
  new URL(`${SSO_URL}/.well-known/jwks.json`)
);

export async function verifyAccessToken(token: string) {
  const { payload } = await jwtVerify(token, JWKS, {
    issuer: SSO_URL,
    audience: process.env.NEXT_PUBLIC_SSO_CLIENT_ID,
  });
  return payload;
}
```

### 4. Global Logout
```typescript
// Logout from all apps
const logoutUrl = new URL(`${SSO_URL}/oauth2/logout`);
logoutUrl.searchParams.set("post_logout_redirect_uri", window.location.origin);
window.location.href = logoutUrl.toString();
```

---

## Common Pitfalls

| Issue | Solution |
|-------|----------|
| PKCE verifier lost after redirect | Store in httpOnly cookie before redirect |
| Token in localStorage | Use httpOnly cookies instead |
| JWKS fetch fails | Check CORS on auth server |
| Consent screen loops | Ensure consent page saves decision |

---

## Verification

Run: `python3 scripts/verify.py`

Expected: `✓ configuring-better-auth skill ready`

## If Verification Fails

1. Check: references/ folder has both setup files
2. **Stop and report** if still failing

## References

- [references/auth-server-setup.md](references/auth-server-setup.md) - Complete auth server with OIDC provider
- [references/sso-client-integration.md](references/sso-client-integration.md) - Full SSO client implementation