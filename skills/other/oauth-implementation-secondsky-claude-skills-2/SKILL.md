---
name: oauth-implementation
description: OAuth 2.0 and OpenID Connect authentication with secure flows. Use for third-party integrations, SSO systems, token-based API access, or encountering authorization code flow, PKCE, token refresh, scope management errors.
---

# OAuth Implementation

Implement OAuth 2.0 and OpenID Connect for secure authentication.

## OAuth 2.0 Flows

| Flow | Use Case |
|------|----------|
| Authorization Code | Web apps (most secure) |
| Authorization Code + PKCE | SPAs, mobile apps |
| Client Credentials | Service-to-service |
| Refresh Token | Session renewal |

## Authorization Code Flow (Express)

```javascript
const express = require('express');
const jwt = require('jsonwebtoken');

// Step 1: Redirect to authorization
app.get('/auth/login', (req, res) => {
  const state = crypto.randomBytes(16).toString('hex');
  req.session.oauthState = state;

  const params = new URLSearchParams({
    client_id: process.env.CLIENT_ID,
    redirect_uri: process.env.REDIRECT_URI,
    response_type: 'code',
    scope: 'openid profile email',
    state
  });

  res.redirect(`${PROVIDER_URL}/authorize?${params}`);
});

// Step 2: Handle callback
app.get('/auth/callback', async (req, res) => {
  if (req.query.state !== req.session.oauthState) {
    return res.status(400).json({ error: 'Invalid state' });
  }

  const tokenResponse = await fetch(`${PROVIDER_URL}/token`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code: req.query.code,
      redirect_uri: process.env.REDIRECT_URI,
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET
    })
  });

  const tokens = await tokenResponse.json();
  // Store tokens securely and create session
});
```

## PKCE for Public Clients

```javascript
function generatePKCE() {
  const verifier = crypto.randomBytes(32).toString('base64url');
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
  return { verifier, challenge };
}
```

## Security Requirements

- Always use HTTPS
- Validate redirect URIs strictly
- Use PKCE for public clients
- Store tokens in HttpOnly cookies
- Implement token rotation
- Use short-lived access tokens (15 min)

## Additional Implementations

See [references/python-java.md](references/python-java.md) for:
- Python Flask with Authlib OIDC provider
- OpenID Connect discovery and JWKS endpoints
- Java Spring Security OAuth2 server
- Token introspection and revocation

## Never Do

- Store tokens in localStorage
- Use implicit flow
- Skip state parameter validation
- Expose client secrets in frontend
- Use long-lived access tokens
