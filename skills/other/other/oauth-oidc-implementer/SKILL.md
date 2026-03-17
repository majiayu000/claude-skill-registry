---
name: oauth-oidc-implementer
description: Expert in implementing OAuth 2.0 and OpenID Connect (OIDC) authentication flows. Specializes in secure token handling, social login integration, API authorization, and identity provider configuration. Handles both client-side and server-side flows with security best practices.
version: 1.0.0
category: security
tags: [oauth, oidc, authentication, authorization, jwt, security]
---

# OAuth/OIDC Implementer

## Overview

Expert in implementing OAuth 2.0 and OpenID Connect (OIDC) authentication flows. Specializes in secure token handling, social login integration, API authorization, and identity provider configuration. Handles both client-side and server-side flows with security best practices.

## When to Use

- Implementing "Login with Google/GitHub/etc." social login
- Setting up OAuth 2.0 for API authorization
- Configuring OIDC for enterprise SSO
- Designing token refresh and session management
- Implementing PKCE for mobile/SPA applications
- Securing API endpoints with JWT validation
- Integrating with identity providers (Auth0, Okta, Keycloak)
- Troubleshooting OAuth flow failures

## Capabilities

### OAuth 2.0 Flows
- Authorization Code flow (with PKCE)
- Client Credentials flow for service-to-service
- Implicit flow (legacy, understand why to avoid)
- Device Authorization flow for IoT
- Refresh token rotation

### OpenID Connect
- ID token validation and claims
- UserInfo endpoint usage
- Discovery document (`.well-known/openid-configuration`)
- Session management (front-channel/back-channel logout)
- PKCE for public clients

### Token Management
- JWT structure (header, payload, signature)
- Access token vs ID token vs refresh token
- Token storage strategies (httpOnly cookies vs localStorage)
- Token refresh patterns
- Revocation and logout

### Security Best Practices
- PKCE (Proof Key for Code Exchange)
- State parameter for CSRF protection
- Nonce for replay protection
- Secure token storage
- Short-lived access tokens

### Identity Providers
- Auth0 integration
- Okta configuration
- Keycloak self-hosted
- Google/GitHub/Microsoft social login
- SAML to OIDC bridge

## Dependencies

Works well with:
- `nextjs-app-router-expert` - Full-stack auth implementation
- `api-architect` - API authorization design
- `cloudflare-worker-dev` - Edge authentication
- `site-reliability-engineer` - Auth monitoring

## Examples

### Authorization Code Flow with PKCE (SPA)
```typescript
// 1. Generate PKCE challenge
function generatePKCE() {
  const verifier = base64URLEncode(crypto.getRandomValues(new Uint8Array(32)));
  const challenge = base64URLEncode(
    await crypto.subtle.digest('SHA-256', new TextEncoder().encode(verifier))
  );
  return { verifier, challenge };
}

// 2. Redirect to authorization endpoint
function initiateLogin() {
  const { verifier, challenge } = generatePKCE();
  const state = crypto.randomUUID();

  // Store verifier and state for later validation
  sessionStorage.setItem('pkce_verifier', verifier);
  sessionStorage.setItem('oauth_state', state);

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: 'your-client-id',
    redirect_uri: 'https://yourapp.com/callback',
    scope: 'openid profile email',
    state: state,
    code_challenge: challenge,
    code_challenge_method: 'S256',
  });

  window.location.href = `https://auth.example.com/authorize?${params}`;
}

// 3. Handle callback and exchange code for tokens
async function handleCallback(code: string, state: string) {
  // Validate state
  if (state !== sessionStorage.getItem('oauth_state')) {
    throw new Error('State mismatch - possible CSRF attack');
  }

  const verifier = sessionStorage.getItem('pkce_verifier');

  const response = await fetch('https://auth.example.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: 'https://yourapp.com/callback',
      client_id: 'your-client-id',
      code_verifier: verifier,
    }),
  });

  const tokens = await response.json();
  // { access_token, id_token, refresh_token, expires_in }

  // Clean up
  sessionStorage.removeItem('pkce_verifier');
  sessionStorage.removeItem('oauth_state');

  return tokens;
}
```

### Next.js API Route Token Handler
```typescript
// app/api/auth/callback/route.ts
import { cookies } from 'next/headers';
import { NextResponse } from 'next/server';

export async function GET(request: Request) {
  const { searchParams } = new URL(request.url);
  const code = searchParams.get('code');
  const state = searchParams.get('state');

  // Validate state from cookie
  const cookieStore = cookies();
  const storedState = cookieStore.get('oauth_state')?.value;

  if (state !== storedState) {
    return NextResponse.redirect('/auth/error?reason=state_mismatch');
  }

  // Exchange code for tokens (server-side, can use client_secret)
  const tokenResponse = await fetch('https://auth.example.com/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code: code!,
      redirect_uri: process.env.REDIRECT_URI!,
      client_id: process.env.CLIENT_ID!,
      client_secret: process.env.CLIENT_SECRET!,
    }),
  });

  const tokens = await tokenResponse.json();

  // Store refresh token in httpOnly cookie
  const response = NextResponse.redirect('/dashboard');

  response.cookies.set('refresh_token', tokens.refresh_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 60 * 60 * 24 * 30, // 30 days
    path: '/',
  });

  // Access token can go to client or httpOnly cookie
  response.cookies.set('access_token', tokens.access_token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: tokens.expires_in,
    path: '/',
  });

  return response;
}
```

### JWT Validation (Node.js)
```typescript
import jwt from 'jsonwebtoken';
import jwksClient from 'jwks-rsa';

const client = jwksClient({
  jwksUri: 'https://auth.example.com/.well-known/jwks.json',
  cache: true,
  rateLimit: true,
});

function getKey(header: jwt.JwtHeader, callback: jwt.SigningKeyCallback) {
  client.getSigningKey(header.kid, (err, key) => {
    const signingKey = key?.getPublicKey();
    callback(err, signingKey);
  });
}

export async function validateToken(token: string): Promise<JWTPayload> {
  return new Promise((resolve, reject) => {
    jwt.verify(
      token,
      getKey,
      {
        algorithms: ['RS256'],
        issuer: 'https://auth.example.com/',
        audience: 'your-client-id',
      },
      (err, decoded) => {
        if (err) reject(err);
        else resolve(decoded as JWTPayload);
      }
    );
  });
}

// Middleware usage
export async function authMiddleware(req: Request) {
  const token = req.headers.get('Authorization')?.replace('Bearer ', '');

  if (!token) {
    return new Response('Unauthorized', { status: 401 });
  }

  try {
    const payload = await validateToken(token);
    // Attach user to request context
    return { user: payload };
  } catch (error) {
    return new Response('Invalid token', { status: 401 });
  }
}
```

### Token Refresh Pattern
```typescript
// Client-side token refresh with race condition handling
let refreshPromise: Promise<string> | null = null;

async function getAccessToken(): Promise<string> {
  const accessToken = localStorage.getItem('access_token');
  const expiresAt = localStorage.getItem('token_expires_at');

  // Check if token is still valid (with 60s buffer)
  if (accessToken && expiresAt && Date.now() < parseInt(expiresAt) - 60000) {
    return accessToken;
  }

  // Deduplicate concurrent refresh requests
  if (refreshPromise) {
    return refreshPromise;
  }

  refreshPromise = refreshAccessToken();

  try {
    return await refreshPromise;
  } finally {
    refreshPromise = null;
  }
}

async function refreshAccessToken(): Promise<string> {
  const response = await fetch('/api/auth/refresh', {
    method: 'POST',
    credentials: 'include', // Send httpOnly refresh token cookie
  });

  if (!response.ok) {
    // Refresh failed, redirect to login
    window.location.href = '/login';
    throw new Error('Token refresh failed');
  }

  const { access_token, expires_in } = await response.json();

  localStorage.setItem('access_token', access_token);
  localStorage.setItem('token_expires_at', String(Date.now() + expires_in * 1000));

  return access_token;
}
```

### Social Login Setup (Auth0)
```typescript
// auth0.config.ts
export const auth0Config = {
  domain: process.env.AUTH0_DOMAIN!,
  clientId: process.env.AUTH0_CLIENT_ID!,
  clientSecret: process.env.AUTH0_CLIENT_SECRET!,
  redirectUri: process.env.AUTH0_REDIRECT_URI!,
  scope: 'openid profile email',
  audience: process.env.AUTH0_AUDIENCE, // For API access
};

// Login URL builder
export function getLoginUrl(connection?: string) {
  const params = new URLSearchParams({
    response_type: 'code',
    client_id: auth0Config.clientId,
    redirect_uri: auth0Config.redirectUri,
    scope: auth0Config.scope,
    state: generateState(),
    ...(auth0Config.audience && { audience: auth0Config.audience }),
    ...(connection && { connection }), // 'google-oauth2', 'github', etc.
  });

  return `https://${auth0Config.domain}/authorize?${params}`;
}
```

### OIDC Discovery
```typescript
// Fetch and cache OIDC configuration
interface OIDCConfig {
  authorization_endpoint: string;
  token_endpoint: string;
  userinfo_endpoint: string;
  jwks_uri: string;
  issuer: string;
}

let oidcConfig: OIDCConfig | null = null;

export async function getOIDCConfig(issuer: string): Promise<OIDCConfig> {
  if (oidcConfig) return oidcConfig;

  const response = await fetch(`${issuer}/.well-known/openid-configuration`);
  oidcConfig = await response.json();

  return oidcConfig;
}
```

## Best Practices

1. **Always use PKCE** - Even for confidential clients, it adds security
2. **Validate state parameter** - Prevents CSRF attacks
3. **Use httpOnly cookies** - For refresh tokens, never localStorage
4. **Short-lived access tokens** - 15 minutes is common, refresh as needed
5. **Validate tokens server-side** - Don't trust client-side validation alone
6. **Use the nonce claim** - Prevents replay attacks with ID tokens
7. **Implement proper logout** - Revoke tokens and clear sessions
8. **Validate audience and issuer** - Ensure tokens are for your app
9. **Rotate refresh tokens** - Issue new refresh token on each use

## Common Pitfalls

- **Storing tokens in localStorage** - Vulnerable to XSS attacks
- **Not validating state** - Opens CSRF vulnerability
- **Implicit flow for SPAs** - Deprecated, use Authorization Code + PKCE
- **Long-lived access tokens** - Increases risk if compromised
- **Not validating JWT signature** - Anyone can forge unsigned tokens
- **Hardcoded client secrets** - Use environment variables
- **Missing token revocation** - Users can't properly log out
- **Not handling token expiry** - Silent refresh failures cause bad UX
