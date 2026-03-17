---
name: heartwood-auth
description: Integrate Heartwood (GroveAuth) authentication into Grove applications. Use when adding sign-in, protecting routes, or validating sessions in any Grove property.
---

# Heartwood Auth Integration Skill

## When to Activate

Activate this skill when:
- Adding authentication to a Grove application
- Protecting admin routes
- Validating user sessions
- Setting up OAuth sign-in
- Integrating with Heartwood (GroveAuth)

## Overview

**Heartwood** is Grove's centralized authentication service powered by Better Auth.

| Domain | Purpose |
|--------|---------|
| `heartwood.grove.place` | Frontend (login UI) |
| `auth-api.grove.place` | Backend API |

### Key Features

- **OAuth Providers**: Google
- **Magic Links**: Click-to-login emails via Resend
- **Passkeys**: WebAuthn passwordless authentication
- **KV-Cached Sessions**: Sub-100ms validation
- **Cross-Subdomain SSO**: Single session across all .grove.place

## Integration Approaches

### Option A: Better Auth Client (Recommended)

For new integrations, use Better Auth's client library:

```typescript
// src/lib/auth/client.ts
import { createAuthClient } from 'better-auth/client';

export const auth = createAuthClient({
  baseURL: 'https://auth-api.grove.place'
});

// Sign in with Google
await auth.signIn.social({ provider: 'google' });

// Get current session
const session = await auth.getSession();

// Sign out
await auth.signOut();
```

### Option B: Cookie-Based SSO (*.grove.place apps)

For apps on `.grove.place` subdomains, sessions work automatically via cookies:

```typescript
// src/hooks.server.ts
import type { Handle } from '@sveltejs/kit';

export const handle: Handle = async ({ event, resolve }) => {
  // Check session via Heartwood API
  const sessionCookie = event.cookies.get('better-auth.session_token');

  if (sessionCookie) {
    try {
      const response = await fetch('https://auth-api.grove.place/api/auth/session', {
        headers: {
          Cookie: `better-auth.session_token=${sessionCookie}`
        }
      });

      if (response.ok) {
        const data = await response.json();
        event.locals.user = data.user;
        event.locals.session = data.session;
      }
    } catch {
      // Session invalid or expired
    }
  }

  return resolve(event);
};
```

### Option C: Legacy Token Flow (Backwards Compatible)

For existing integrations using the legacy OAuth flow:

```typescript
// 1. Redirect to Heartwood login
const params = new URLSearchParams({
  client_id: 'your-client-id',
  redirect_uri: 'https://yourapp.grove.place/auth/callback',
  state: crypto.randomUUID(),
  code_challenge: await generateCodeChallenge(verifier),
  code_challenge_method: 'S256'
});
redirect(302, `https://auth-api.grove.place/login?${params}`);

// 2. Exchange code for tokens (in callback route)
const tokens = await fetch('https://auth-api.grove.place/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: code,
    redirect_uri: 'https://yourapp.grove.place/auth/callback',
    client_id: 'your-client-id',
    client_secret: env.HEARTWOOD_CLIENT_SECRET,
    code_verifier: verifier
  })
}).then(r => r.json());

// 3. Verify token on protected routes
const user = await fetch('https://auth-api.grove.place/verify', {
  headers: { Authorization: `Bearer ${tokens.access_token}` }
}).then(r => r.json());
```

## Protected Routes Pattern

### SvelteKit Layout Protection

```typescript
// src/routes/admin/+layout.server.ts
import { redirect } from '@sveltejs/kit';
import type { LayoutServerLoad } from './$types';

export const load: LayoutServerLoad = async ({ locals }) => {
  if (!locals.user) {
    throw redirect(302, '/auth/login');
  }

  return {
    user: locals.user
  };
};
```

### API Route Protection

```typescript
// src/routes/api/protected/+server.ts
import { json, error } from '@sveltejs/kit';
import type { RequestHandler } from './$types';

export const GET: RequestHandler = async ({ locals }) => {
  if (!locals.user) {
    throw error(401, 'Unauthorized');
  }

  return json({ message: 'Protected data', user: locals.user });
};
```

## Session Validation

### Via Better Auth Session Endpoint

```typescript
async function validateSession(sessionToken: string) {
  const response = await fetch('https://auth-api.grove.place/api/auth/session', {
    headers: {
      Cookie: `better-auth.session_token=${sessionToken}`
    }
  });

  if (!response.ok) return null;

  const data = await response.json();
  return data.session ? data : null;
}
```

### Via Legacy Verify Endpoint

```typescript
async function validateToken(accessToken: string) {
  const response = await fetch('https://auth-api.grove.place/verify', {
    headers: {
      Authorization: `Bearer ${accessToken}`
    }
  });

  const data = await response.json();
  return data.active ? data : null;
}
```

## Client Registration

To integrate a new app with Heartwood, you need to register it as a client.

### 1. Generate Client Credentials

```bash
# Generate a secure client secret
openssl rand -base64 32
# Example: YKzJChC3RPjZvd1f/OD5zUGAvcouOTXG7maQP1ernCg=

# Hash it for storage (base64url encoding)
echo -n "YOUR_SECRET" | openssl dgst -sha256 -binary | base64 | tr '+/' '-_' | tr -d '='
```

### 2. Register in Heartwood Database

```sql
INSERT INTO clients (id, name, client_id, client_secret_hash, redirect_uris, allowed_origins)
VALUES (
  lower(hex(randomblob(16))),
  'Your App Name',
  'your-app-id',
  'BASE64URL_HASHED_SECRET',
  '["https://yourapp.grove.place/auth/callback"]',
  '["https://yourapp.grove.place"]'
);
```

### 3. Set Secrets on Your App

```bash
# Set the client secret on your app
wrangler secret put HEARTWOOD_CLIENT_SECRET
# Paste: YKzJChC3RPjZvd1f/OD5zUGAvcouOTXG7maQP1ernCg=
```

## Environment Variables

| Variable | Description |
|----------|-------------|
| `HEARTWOOD_CLIENT_ID` | Your registered client ID |
| `HEARTWOOD_CLIENT_SECRET` | Your client secret (never commit!) |

## API Endpoints Reference

### Better Auth Endpoints (Recommended)

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/auth/sign-in/social` | OAuth sign-in |
| POST | `/api/auth/sign-in/magic-link` | Magic link sign-in |
| POST | `/api/auth/sign-in/passkey` | Passkey sign-in |
| GET | `/api/auth/session` | Get current session |
| POST | `/api/auth/sign-out` | Sign out |

### Legacy Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/login` | Login page |
| POST | `/token` | Exchange code for tokens |
| GET | `/verify` | Validate access token |
| GET | `/userinfo` | Get user info |

## Best Practices

### DO
- Use Better Auth client for new integrations
- Validate sessions on every protected request
- Use `httpOnly` cookies for token storage
- Implement proper error handling for auth failures
- Log out users gracefully when sessions expire

### DON'T
- Store tokens in localStorage (XSS vulnerable)
- Skip session validation on API routes
- Hardcode client secrets
- Ignore token expiration

## Cross-Subdomain SSO

All `.grove.place` apps share the same session cookie automatically:

```
better-auth.session_token (domain=.grove.place)
```

Once a user signs in on any Grove property, they're signed in everywhere.

## Troubleshooting

### "Session not found" errors
- Check cookie domain is `.grove.place`
- Verify SESSION_KV namespace is accessible
- Check session hasn't expired

### OAuth callback errors
- Verify redirect_uri matches registered client
- Check client_id is correct
- Ensure client_secret_hash uses base64url encoding

### Slow authentication
- Ensure KV caching is enabled (SESSION_KV binding)
- Check for cold start issues (Workers may sleep)

## Error Codes (HW-AUTH Catalog)

Heartwood has its own Signpost error catalog with 16 codes:

```typescript
import {
  AUTH_ERRORS, getAuthError, logAuthError, buildErrorParams,
} from '@autumnsgrove/groveengine/heartwood';
```

**Key error codes:**

| Code | Key | When |
|------|-----|------|
| `HW-AUTH-001` | `ACCESS_DENIED` | User lacks permission |
| `HW-AUTH-002` | `PROVIDER_ERROR` | OAuth provider failed |
| `HW-AUTH-004` | `REDIRECT_URI_MISMATCH` | Callback URL doesn't match registered client |
| `HW-AUTH-020` | `NO_SESSION` | No session cookie found |
| `HW-AUTH-021` | `SESSION_EXPIRED` | Session timed out |
| `HW-AUTH-022` | `INVALID_TOKEN` | Token verification failed |
| `HW-AUTH-023` | `TOKEN_EXCHANGE_FAILED` | Code-for-token exchange failed |

**Mapping OAuth errors to Signpost codes:**
```typescript
// In callback handler — map OAuth error param to structured error
const authError = getAuthError(errorParam); // e.g. "access_denied" → AUTH_ERRORS.ACCESS_DENIED
logAuthError(authError, { path: '/auth/callback', ip });
redirect(302, `/login?${buildErrorParams(authError)}`);
```

**Number ranges:** 001-019 infrastructure, 020-039 session/token, 040+ reserved.

See `AgentUsage/error_handling.md` for the full Signpost reference.

## Related Resources

- **Heartwood Spec**: `/Users/autumn/Documents/Projects/GroveAuth/GROVEAUTH_SPEC.md`
- **Better Auth Docs**: https://better-auth.com
- **Client Setup Guide**: `/Users/autumn/Documents/Projects/GroveAuth/docs/OAUTH_CLIENT_SETUP.md`
