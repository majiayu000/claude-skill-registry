---
name: tes-oauth
description: |
  OAuth 2.0 integration and configuration for TES (Takeback Event System). Use this skill when:
  (1) Configuring OAuth 2.0 for a new client application
  (2) Implementing authorization code flow with PKCE
  (3) Setting up client credentials authentication
  (4) Managing OAuth tokens and refresh flows
  (5) Configuring role-based permissions for API access
  (6) Integrating external auth providers (WorkOS) with TES
  (7) Debugging authentication issues in TES
  (8) Implementing password reset flows
  (9) Setting up multi-organization user authentication
---

# TES OAuth 2.0 Integration

Configure and integrate OAuth 2.0 authentication for client applications using the Takeback Event System.

## Quick Reference

| Flow | Use Case | Endpoint |
|------|----------|----------|
| Authorization Code + PKCE | User-facing apps | `/oauth/authorize` → `/oauth/token` |
| Client Credentials | Server-to-server | `/oauth/token` |
| Refresh Token | Token renewal | `/oauth/token` |
| Password Reset | Forgot password | `/oauth/forgot-password` → `/oauth/reset-password` |
| Signup | New user registration | `/oauth/authorize?mode=signup` |

## Architecture Overview

TES uses a layered authentication system:

```
Client App → TES OAuth → Provider (WorkOS) → TES JWT → API Access
```

Key components:
- **OAuth endpoints**: `/oauth/authorize`, `/oauth/token`, `/oauth/forgot-password`, `/oauth/reset-password`
- **Auth endpoints**: `/api/auth/login`, `/api/auth/signup`, `/api/auth/refresh`
- **Client config**: Environment variables per client (`CLIENT_CONFIG_<CLIENT_ID>`)
- **Permissions**: Role-based with `action:entity:scope` format

## Implementation Workflows

### 1. Authorization Code Flow (PKCE)

For browser/mobile apps with user authentication:

```javascript
// 1. Generate PKCE challenge
const codeVerifier = generateRandomString(64);
const codeChallenge = base64url(sha256(codeVerifier));

// 2. Redirect to authorize
window.location = `/oauth/authorize?` +
  `client_id=${clientId}&` +
  `redirect_uri=${encodeURIComponent(redirectUri)}&` +
  `response_type=code&` +
  `code_challenge=${codeChallenge}&` +
  `code_challenge_method=S256&` +
  `state=${state}`;

// 3. Exchange code for tokens (after redirect)
const response = await fetch('/oauth/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Client-Id': clientId
  },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: redirectUri,
    code_verifier: codeVerifier
  })
});
```

### 2. Client Credentials Flow

For server-to-server authentication using TES tokens:

```javascript
const response = await fetch('/oauth/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Client-Id': clientId
  },
  body: new URLSearchParams({
    grant_type: 'client_credentials',
    client_id: clientId,
    client_secret: tesAccessToken  // Valid TES JWT
  })
});
```

### 3. Token Refresh

```javascript
const response = await fetch('/oauth/token', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/x-www-form-urlencoded',
    'X-Client-Id': clientId
  },
  body: new URLSearchParams({
    grant_type: 'refresh_token',
    refresh_token: refreshToken
  })
});
```

### 4. Password Reset Flow

For users who forgot their password:

```javascript
// 1. Request password reset (sends email via WorkOS)
await fetch('/oauth/forgot-password', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({ email: 'user@example.com' })
});

// 2. User clicks link in email, lands on reset page with token
// 3. Submit new password
await fetch('/oauth/reset-password', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    token: resetToken,
    password: newPassword,
    confirmPassword: newPassword
  })
});
```

### 5. User Signup Flow

For new user registration:

```javascript
// Redirect to signup form
window.location = `/oauth/authorize?client_id=${clientId}&mode=signup`;

// Or direct API call
const response = await fetch('/api/auth/signup', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'X-Client-Id': clientId
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'securePassword123',
    firstName: 'John',
    lastName: 'Doe'
  })
});
```

## Token Response Format

```json
{
  "access_token": "tes_clientid_randomstring",
  "token_type": "Bearer",
  "expires_in": 3600,
  "refresh_token": "ref_clientid_randomstring"
}
```

## API Authentication

Use tokens in the Authorization header:

```javascript
fetch('/api/graphql', {
  method: 'POST',
  headers: {
    'Authorization': `Bearer ${accessToken}`,
    'X-Client-Id': clientId,
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({ query, variables })
});
```

## Detailed References

- **OAuth flow details**: See [references/oauth-flows.md](references/oauth-flows.md) for complete flow diagrams and error handling
- **Client configuration**: See [references/client-setup.md](references/client-setup.md) for setting up new clients with WorkOS
- **Permissions system**: See [references/permissions.md](references/permissions.md) for RBAC roles and permission mappings
- **Password reset**: See [references/password-reset.md](references/password-reset.md) for password reset implementation

## Key Files in TES

| Purpose | Location |
|---------|----------|
| OAuth authorize | `functions/oauth/authorize.js` |
| OAuth token | `functions/oauth/token.js` |
| Forgot password | `functions/oauth/forgot-password.js` |
| Reset password | `functions/oauth/reset-password.js` |
| JWT utilities | `functions/api/auth/_services/jwt.js` |
| Client auth registry | `functions/api/auth/_services/index.js` |
| Permission mappings | `functions/api/auth/_services/<client>/permissions.js` |
| Auth middleware | `functions/api/_helpers/handleAuthorization.js` |
| OAuth token model | `functions/api/graphql/domains/oauthToken/` |
| WorkOS integration | `functions/api/auth/_services/<client>/workos.js` |

## Multi-Organization Users

When a user belongs to multiple WorkOS organizations, TES handles this automatically:

1. Initial login attempt returns `organization_selection_required`
2. TES uses the `pending_authentication_token` to complete auth
3. Automatically selects the organization configured for the client

```javascript
// WorkOS returns this for multi-org users
{
  "code": "organization_selection_required",
  "pending_authentication_token": "xxx",
  "organizations": [
    { "id": "org_xxx", "name": "Org 1" },
    { "id": "org_yyy", "name": "Org 2" }
  ]
}

// TES automatically completes with configured org
{
  "grant_type": "urn:workos:oauth:grant-type:organization-selection",
  "pending_authentication_token": "xxx",
  "organization_id": "org_xxx"  // From client config
}
```

## Common Issues

| Issue | Solution |
|-------|----------|
| `invalid_grant` | PKCE code_verifier doesn't match challenge |
| `invalid_client` | Missing or incorrect X-Client-Id header |
| `access_denied` | Token lacks required permissions |
| Missing permissions | Check role-to-permission mapping in client service |
| `organization_selection_required` | User in multiple orgs - ensure WORKOS_ORGANIZATION_ID is set in client config |
| Password reset email not received | Check WorkOS dashboard for email delivery status |
