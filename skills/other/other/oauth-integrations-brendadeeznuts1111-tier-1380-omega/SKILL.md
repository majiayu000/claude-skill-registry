---
name: oauth-integrations
description: |
  Implement OAuth 2.0 authentication with GitHub and Microsoft Entra (Azure AD) in Cloudflare Workers
  and other edge environments. Covers provider-specific quirks, required headers, scope requirements,
  and token handling without MSAL.

  Use when: implementing GitHub OAuth, Microsoft/Azure AD authentication, handling OAuth callbacks,
  or troubleshooting 403 errors in OAuth flows.
license: MIT
---

# OAuth Integrations for Edge Environments

Implement GitHub and Microsoft OAuth in Cloudflare Workers and other edge runtimes.

## GitHub OAuth

### Required Headers

GitHub API has strict requirements that differ from other providers.

| Header | Requirement |
|--------|-------------|
| `User-Agent` | **REQUIRED** - Returns 403 without it |
| `Accept` | `application/vnd.github+json` recommended |

```typescript
const resp = await fetch('https://api.github.com/user', {
  headers: {
    Authorization: `Bearer ${accessToken}`,
    'User-Agent': 'MyApp/1.0',  // Required!
    'Accept': 'application/vnd.github+json',
  },
});
```

### Private Email Handling

GitHub users can set email to private (`/user` returns `email: null`).

```typescript
if (!userData.email) {
  const emails = await fetch('https://api.github.com/user/emails', { headers })
    .then(r => r.json());
  userData.email = emails.find(e => e.primary && e.verified)?.email;
}
```

Requires `user:email` scope.

### Token Exchange

Token exchange returns form-encoded by default. Add Accept header for JSON:

```typescript
const tokenResponse = await fetch('https://github.com/login/oauth/access_token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Accept': 'application/json',  // Get JSON response
  },
  body: new URLSearchParams({ code, client_id, client_secret, redirect_uri }),
});
```

### GitHub OAuth Notes

| Issue | Solution |
|-------|----------|
| Callback URL | Must be EXACT - no wildcards, no subdirectory matching |
| Token exchange returns form-encoded | Add `'Accept': 'application/json'` header |
| Tokens don't expire | No refresh flow needed, but revoked = full re-auth |

## Microsoft Entra (Azure AD) OAuth

### Why MSAL Doesn't Work in Workers

MSAL.js depends on:
- Browser APIs (localStorage, sessionStorage, DOM)
- Node.js crypto module

Cloudflare's V8 isolate runtime has neither. Use manual OAuth instead:
1. Manual OAuth URL construction
2. Direct token exchange via fetch
3. JWT validation with `jose` library

### Required Scopes

```typescript
// For user identity (email, name, profile picture)
const scope = 'openid email profile User.Read';

// For refresh tokens (long-lived sessions)
const scope = 'openid email profile User.Read offline_access';
```

**Critical**: `User.Read` is required for Microsoft Graph `/me` endpoint. Without it, token exchange succeeds but user info fetch returns 403.

### User Info Endpoint

```typescript
// Microsoft Graph /me endpoint
const resp = await fetch('https://graph.microsoft.com/v1.0/me', {
  headers: { Authorization: `Bearer ${accessToken}` },
});

// Email may be in different fields
const email = data.mail || data.userPrincipalName;
```

### Tenant Configuration

| Tenant Value | Who Can Sign In |
|--------------|-----------------|
| `common` | Any Microsoft account (personal + work) |
| `organizations` | Work/school accounts only |
| `consumers` | Personal Microsoft accounts only |
| `{tenant-id}` | Specific organization only |

### Azure Portal Setup

1. App Registration → New registration
2. Platform: **Web** (not SPA) for server-side OAuth
3. Redirect URIs: Add both `/callback` and `/admin/callback`
4. Certificates & secrets → New client secret

### Token Lifetimes

| Token Type | Default Lifetime | Notes |
|------------|------------------|-------|
| Access token | 60-90 minutes | Configurable via token lifetime policies |
| Refresh token | 90 days | Revoked on password change |
| ID token | 60 minutes | Same as access token |

**Best Practice**: Always request `offline_access` scope and implement refresh token flow for sessions longer than 1 hour.

## Common Corrections

| If Claude suggests... | Use instead... |
|----------------------|----------------|
| GitHub fetch without User-Agent | Add `'User-Agent': 'AppName/1.0'` (REQUIRED) |
| Using MSAL.js in Workers | Manual OAuth + jose for JWT validation |
| Microsoft scope without User.Read | Add `User.Read` scope |
| Fetching email from token claims only | Use Graph `/me` endpoint |

## Error Reference

### GitHub Errors

| Error | Cause | Fix |
|-------|-------|-----|
| 403 Forbidden | Missing User-Agent header | Add User-Agent header |
| `email: null` | User has private email | Fetch `/user/emails` with `user:email` scope |

### Microsoft Errors

| Error | Cause | Fix |
|-------|-------|-----|
| AADSTS50058 | Silent auth failed | Use interactive flow |
| AADSTS700084 | Refresh token expired | Re-authenticate user |
| 403 on Graph /me | Missing User.Read scope | Add User.Read to scopes |

## Reference

- GitHub API: https://docs.github.com/en/rest
- GitHub OAuth: https://docs.github.com/en/apps/oauth-apps
- Microsoft Graph permissions: https://learn.microsoft.com/en-us/graph/permissions-reference
- AADSTS error codes: https://learn.microsoft.com/en-us/entra/identity-platform/reference-error-codes
