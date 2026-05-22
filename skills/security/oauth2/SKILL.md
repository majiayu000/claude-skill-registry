---
name: OAuth2
description: Expert guidance for OAuth 2.0 protocol including authorization flows, grant types, token management, OpenID Connect, security best practices, and implementation patterns. Use this when implementing authentication/authorization, working with OAuth providers, securing APIs, or integrating with third-party services.
---

# OAuth 2.0

Expert assistance with OAuth 2.0 authorization framework and OpenID Connect.

## Overview

OAuth 2.0 is an authorization framework that enables applications to obtain limited access to user accounts. Key concepts:

- **Resource Owner**: User who owns the data
- **Client**: Application requesting access
- **Authorization Server**: Issues access tokens (e.g., Keycloak, Auth0)
- **Resource Server**: API that holds protected resources
- **Access Token**: Credentials to access protected resources
- **Refresh Token**: Credentials to obtain new access tokens

## OAuth 2.0 Flows

### Authorization Code Flow (Most Secure)

**Best for**: Server-side web apps with backend

**Flow**:
```
1. Client redirects user to authorization server
   GET /authorize?
     response_type=code
     &client_id=CLIENT_ID
     &redirect_uri=REDIRECT_URI
     &scope=read write
     &state=RANDOM_STATE

2. User authenticates and grants permission

3. Authorization server redirects back with code
   REDIRECT_URI?code=AUTH_CODE&state=RANDOM_STATE

4. Client exchanges code for tokens
   POST /token
   Content-Type: application/x-www-form-urlencoded

   grant_type=authorization_code
   &code=AUTH_CODE
   &redirect_uri=REDIRECT_URI
   &client_id=CLIENT_ID
   &client_secret=CLIENT_SECRET

5. Authorization server responds with tokens
   {
     "access_token": "ACCESS_TOKEN",
     "token_type": "Bearer",
     "expires_in": 3600,
     "refresh_token": "REFRESH_TOKEN",
     "scope": "read write"
   }
```

**Implementation (Node.js)**:
```javascript
// Step 1: Redirect to authorization
app.get('/login', (req, res) => {
  const state = crypto.randomBytes(16).toString('hex')
  req.session.oauthState = state

  const authUrl = new URL('https://auth.example.com/authorize')
  authUrl.searchParams.set('response_type', 'code')
  authUrl.searchParams.set('client_id', CLIENT_ID)
  authUrl.searchParams.set('redirect_uri', REDIRECT_URI)
  authUrl.searchParams.set('scope', 'read write')
  authUrl.searchParams.set('state', state)

  res.redirect(authUrl.toString())
})

// Step 3 & 4: Handle callback and exchange code
app.get('/callback', async (req, res) => {
  const { code, state } = req.query

  // Verify state
  if (state !== req.session.oauthState) {
    return res.status(400).send('Invalid state')
  }

  // Exchange code for token
  const tokenResponse = await fetch('https://auth.example.com/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: REDIRECT_URI,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    }),
  })

  const tokens = await tokenResponse.json()

  // Store tokens securely
  req.session.accessToken = tokens.access_token
  req.session.refreshToken = tokens.refresh_token

  res.redirect('/dashboard')
})
```

### Authorization Code Flow with PKCE

**Best for**: Mobile apps, SPAs, any public client

**PKCE adds security for public clients that can't keep secrets**

**Flow**:
```javascript
// Step 1: Generate code verifier and challenge
const codeVerifier = base64URLEncode(crypto.randomBytes(32))
const codeChallenge = base64URLEncode(
  crypto.createHash('sha256').update(codeVerifier).digest()
)

// Step 2: Authorization request
GET /authorize?
  response_type=code
  &client_id=CLIENT_ID
  &redirect_uri=REDIRECT_URI
  &scope=read
  &state=STATE
  &code_challenge=CODE_CHALLENGE
  &code_challenge_method=S256

// Step 3: Token request (no client_secret needed)
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=authorization_code
&code=AUTH_CODE
&redirect_uri=REDIRECT_URI
&client_id=CLIENT_ID
&code_verifier=CODE_VERIFIER
```

**Implementation (React)**:
```typescript
import { useEffect } from 'react'
import { useRouter } from 'next/router'

// Generate PKCE challenge
function generatePKCE() {
  const codeVerifier = generateRandomString(128)
  const codeChallenge = base64URLEncode(
    sha256(codeVerifier)
  )

  return { codeVerifier, codeChallenge }
}

function LoginButton() {
  const router = useRouter()

  const handleLogin = () => {
    const { codeVerifier, codeChallenge } = generatePKCE()
    const state = generateRandomString(32)

    // Store for later use
    sessionStorage.setItem('pkce_verifier', codeVerifier)
    sessionStorage.setItem('oauth_state', state)

    const authUrl = new URL('https://auth.example.com/authorize')
    authUrl.searchParams.set('response_type', 'code')
    authUrl.searchParams.set('client_id', CLIENT_ID)
    authUrl.searchParams.set('redirect_uri', REDIRECT_URI)
    authUrl.searchParams.set('scope', 'openid profile email')
    authUrl.searchParams.set('state', state)
    authUrl.searchParams.set('code_challenge', codeChallenge)
    authUrl.searchParams.set('code_challenge_method', 'S256')

    window.location.href = authUrl.toString()
  }

  return <button onClick={handleLogin}>Login</button>
}

// Callback page
function CallbackPage() {
  const router = useRouter()

  useEffect(() => {
    async function handleCallback() {
      const { code, state } = router.query

      // Verify state
      const savedState = sessionStorage.getItem('oauth_state')
      if (state !== savedState) {
        throw new Error('Invalid state')
      }

      // Get code verifier
      const codeVerifier = sessionStorage.getItem('pkce_verifier')

      // Exchange code for token
      const response = await fetch('https://auth.example.com/token', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: new URLSearchParams({
          grant_type: 'authorization_code',
          code: code as string,
          redirect_uri: REDIRECT_URI,
          client_id: CLIENT_ID,
          code_verifier: codeVerifier!,
        }),
      })

      const tokens = await response.json()

      // Store tokens
      localStorage.setItem('access_token', tokens.access_token)
      localStorage.setItem('refresh_token', tokens.refresh_token)

      // Clean up
      sessionStorage.removeItem('pkce_verifier')
      sessionStorage.removeItem('oauth_state')

      router.push('/dashboard')
    }

    handleCallback()
  }, [router.query])

  return <div>Logging in...</div>
}
```

### Client Credentials Flow

**Best for**: Machine-to-machine, service accounts, server-to-server

**Flow**:
```bash
# Request token
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=client_credentials
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET
&scope=api.read api.write

# Response
{
  "access_token": "ACCESS_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600,
  "scope": "api.read api.write"
}
```

**Implementation**:
```javascript
async function getServiceToken() {
  const response = await fetch('https://auth.example.com/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'client_credentials',
      client_id: process.env.CLIENT_ID,
      client_secret: process.env.CLIENT_SECRET,
      scope: 'api.read api.write',
    }),
  })

  return await response.json()
}

// Use token
async function callProtectedAPI() {
  const { access_token } = await getServiceToken()

  const response = await fetch('https://api.example.com/data', {
    headers: {
      'Authorization': `Bearer ${access_token}`,
    },
  })

  return await response.json()
}
```

### Resource Owner Password Credentials (Legacy)

**⚠️ Not recommended** - Only use when no other flow works

```bash
POST /token
Content-Type: application/x-www-form-urlencoded

grant_type=password
&username=USER
&password=PASSWORD
&client_id=CLIENT_ID
&client_secret=CLIENT_SECRET
&scope=read
```

### Implicit Flow (Deprecated)

**⚠️ Deprecated** - Use Authorization Code Flow with PKCE instead

## Token Management

### Access Tokens

**Characteristics**:
- Short-lived (5-15 minutes typical)
- Used to access protected resources
- Should be treated as opaque strings
- Often JWT format but not required

**Usage**:
```javascript
// Make API request with access token
fetch('https://api.example.com/user/profile', {
  headers: {
    'Authorization': `Bearer ${accessToken}`,
  },
})
```

### Refresh Tokens

**Purpose**: Obtain new access tokens without re-authentication

**Usage**:
```javascript
async function refreshAccessToken(refreshToken) {
  const response = await fetch('https://auth.example.com/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded',
    },
    body: new URLSearchParams({
      grant_type: 'refresh_token',
      refresh_token: refreshToken,
      client_id: CLIENT_ID,
      client_secret: CLIENT_SECRET,
    }),
  })

  const tokens = await response.json()
  return tokens
}

// Automatic token refresh
async function apiCall(url, options = {}) {
  let accessToken = localStorage.getItem('access_token')

  let response = await fetch(url, {
    ...options,
    headers: {
      ...options.headers,
      'Authorization': `Bearer ${accessToken}`,
    },
  })

  // Token expired
  if (response.status === 401) {
    const refreshToken = localStorage.getItem('refresh_token')
    const newTokens = await refreshAccessToken(refreshToken)

    localStorage.setItem('access_token', newTokens.access_token)
    if (newTokens.refresh_token) {
      localStorage.setItem('refresh_token', newTokens.refresh_token)
    }

    // Retry request with new token
    response = await fetch(url, {
      ...options,
      headers: {
        ...options.headers,
        'Authorization': `Bearer ${newTokens.access_token}`,
      },
    })
  }

  return response
}
```

### Token Storage

**Best Practices**:

**Browser (SPA)**:
- ✅ Memory (most secure, lost on refresh)
- ✅ Session storage (cleared on tab close)
- ⚠️ Local storage (XSS risk, but convenient)
- ❌ Cookies without httpOnly (XSS risk)
- ✅ httpOnly cookies (CSRF protection needed)

**Server-side**:
- ✅ Encrypted session storage
- ✅ Secure database with encryption
- ❌ Plain text files
- ❌ Environment variables (for user tokens)

**Implementation**:
```javascript
// Secure token storage (Next.js)
import { serialize, parse } from 'cookie'

// Set token in httpOnly cookie
export function setTokenCookie(res, token) {
  const cookie = serialize('token', token, {
    httpOnly: true,
    secure: process.env.NODE_ENV === 'production',
    sameSite: 'lax',
    maxAge: 3600,
    path: '/',
  })

  res.setHeader('Set-Cookie', cookie)
}

// Get token from cookie
export function getTokenCookie(req) {
  const cookies = parse(req.headers.cookie || '')
  return cookies.token
}
```

## OpenID Connect (OIDC)

OAuth 2.0 extension for authentication

### ID Token

**JWT containing user information**:
```json
{
  "iss": "https://auth.example.com",
  "sub": "user-123",
  "aud": "client-id",
  "exp": 1234567890,
  "iat": 1234567890,
  "name": "John Doe",
  "email": "john@example.com",
  "email_verified": true,
  "picture": "https://example.com/photo.jpg"
}
```

### OIDC Flow
```javascript
// Authorization request with openid scope
GET /authorize?
  response_type=code
  &client_id=CLIENT_ID
  &redirect_uri=REDIRECT_URI
  &scope=openid profile email
  &state=STATE

// Token response includes ID token
{
  "access_token": "ACCESS_TOKEN",
  "id_token": "ID_TOKEN_JWT",
  "refresh_token": "REFRESH_TOKEN",
  "token_type": "Bearer",
  "expires_in": 3600
}

// Validate ID token
import jwt from 'jsonwebtoken'
import jwksClient from 'jwks-rsa'

const client = jwksClient({
  jwksUri: 'https://auth.example.com/.well-known/jwks.json'
})

function getKey(header, callback) {
  client.getSigningKey(header.kid, (err, key) => {
    const signingKey = key.publicKey || key.rsaPublicKey
    callback(null, signingKey)
  })
}

jwt.verify(idToken, getKey, {
  audience: CLIENT_ID,
  issuer: 'https://auth.example.com',
  algorithms: ['RS256']
}, (err, decoded) => {
  if (err) {
    console.error('Invalid token')
  } else {
    console.log('User:', decoded)
  }
})
```

### UserInfo Endpoint
```javascript
// Get additional user info
async function getUserInfo(accessToken) {
  const response = await fetch('https://auth.example.com/userinfo', {
    headers: {
      'Authorization': `Bearer ${accessToken}`,
    },
  })

  return await response.json()
}
```

### Discovery
```bash
# Get provider configuration
GET https://auth.example.com/.well-known/openid-configuration

# Response includes:
{
  "issuer": "https://auth.example.com",
  "authorization_endpoint": "https://auth.example.com/authorize",
  "token_endpoint": "https://auth.example.com/token",
  "userinfo_endpoint": "https://auth.example.com/userinfo",
  "jwks_uri": "https://auth.example.com/.well-known/jwks.json",
  "response_types_supported": ["code", "token", "id_token"],
  "grant_types_supported": ["authorization_code", "refresh_token"],
  "token_endpoint_auth_methods_supported": ["client_secret_post"]
}
```

## Scopes

### Standard Scopes
- `openid` - Required for OIDC
- `profile` - User's profile info (name, picture, etc.)
- `email` - User's email address
- `address` - User's address
- `phone` - User's phone number
- `offline_access` - Request refresh token

### Custom Scopes
```
API-specific permissions:
- api:read - Read access to API
- api:write - Write access to API
- api:delete - Delete access to API
- admin - Admin access
```

### Requesting Scopes
```javascript
// Request multiple scopes
const authUrl = new URL('https://auth.example.com/authorize')
authUrl.searchParams.set('scope', 'openid profile email api:read api:write')
```

## Security Best Practices

### 1. Always Use State Parameter
```javascript
// Generate random state
const state = crypto.randomBytes(32).toString('hex')
sessionStorage.setItem('oauth_state', state)

// Include in authorization request
authUrl.searchParams.set('state', state)

// Verify in callback
if (receivedState !== sessionStorage.getItem('oauth_state')) {
  throw new Error('CSRF attack detected')
}
```

### 2. Use PKCE for Public Clients
Always use PKCE for SPAs and mobile apps - no exceptions.

### 3. Validate Tokens
```javascript
// Validate JWT
- Verify signature using public key
- Check issuer (iss)
- Check audience (aud)
- Check expiration (exp)
- Check not before (nbf)
```

### 4. Short-Lived Access Tokens
```
Access token: 5-15 minutes
Refresh token: Days to months (with rotation)
```

### 5. Token Rotation
```javascript
// Refresh token rotation
When using refresh token:
1. Issue new access token
2. Issue new refresh token
3. Invalidate old refresh token
```

### 6. Secure Token Storage
```javascript
// ✅ Best practices
- httpOnly cookies (server-side)
- Encrypted session storage (server-side)
- Memory only (SPA, lost on refresh)

// ❌ Avoid
- Local storage (XSS vulnerable)
- Session storage without proper sanitization
- URL parameters
- Plain text anywhere
```

### 7. Redirect URI Validation
```javascript
// Server must validate exact match
Registered: https://app.example.com/callback
Valid:     https://app.example.com/callback
Invalid:   https://app.example.com/callback/extra
Invalid:   https://evil.com/callback
```

### 8. HTTPS Only
All OAuth communication must use HTTPS in production.

### 9. Rate Limiting
Implement rate limiting on:
- Token endpoint
- Authorization endpoint
- UserInfo endpoint

### 10. Audit Logging
Log all OAuth events:
- Authorization requests
- Token issuances
- Token refreshes
- Failed attempts

## Common Patterns

### API Protection
```javascript
// Express middleware
function requireAuth(req, res, next) {
  const token = req.headers.authorization?.split(' ')[1]

  if (!token) {
    return res.status(401).json({ error: 'No token provided' })
  }

  try {
    const decoded = jwt.verify(token, PUBLIC_KEY)
    req.user = decoded
    next()
  } catch (error) {
    return res.status(401).json({ error: 'Invalid token' })
  }
}

// Protected route
app.get('/api/protected', requireAuth, (req, res) => {
  res.json({ data: 'Protected data', user: req.user })
})

// Role-based protection
function requireRole(role) {
  return (req, res, next) => {
    if (!req.user?.roles?.includes(role)) {
      return res.status(403).json({ error: 'Insufficient permissions' })
    }
    next()
  }
}

app.delete('/api/users/:id', requireAuth, requireRole('admin'), (req, res) => {
  // Delete user
})
```

### Silent Authentication
```javascript
// Attempt silent authentication in hidden iframe
function silentAuthentication() {
  return new Promise((resolve, reject) => {
    const iframe = document.createElement('iframe')
    iframe.style.display = 'none'

    const authUrl = new URL('https://auth.example.com/authorize')
    authUrl.searchParams.set('prompt', 'none')
    authUrl.searchParams.set('response_type', 'code')
    authUrl.searchParams.set('client_id', CLIENT_ID)
    authUrl.searchParams.set('redirect_uri', SILENT_REDIRECT_URI)

    iframe.src = authUrl.toString()

    window.addEventListener('message', (event) => {
      if (event.origin !== 'https://app.example.com') return

      if (event.data.code) {
        resolve(event.data.code)
      } else {
        reject(new Error('Silent auth failed'))
      }

      document.body.removeChild(iframe)
    })

    document.body.appendChild(iframe)
  })
}
```

## Troubleshooting

### Invalid Grant
- Expired authorization code
- Code already used
- Mismatched redirect URI
- Invalid code verifier (PKCE)

### Invalid Client
- Wrong client credentials
- Client not found
- Client disabled

### Unauthorized Client
- Client not allowed for grant type
- Client not allowed for scope

### Access Denied
- User denied permission
- Invalid scope requested

## Resources

- RFC 6749 (OAuth 2.0): https://tools.ietf.org/html/rfc6749
- RFC 7636 (PKCE): https://tools.ietf.org/html/rfc7636
- OpenID Connect: https://openid.net/connect/
- OAuth 2.0 Security Best Practices: https://tools.ietf.org/html/draft-ietf-oauth-security-topics
