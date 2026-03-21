---
name: oauth-patterns
description: OIDC flows, PKCE implementation, token refresh strategies, social login integration, and secure session management.
---

# OAuth Patterns

Secure authentication and authorization patterns with OAuth 2.0 and OpenID Connect.

## Authorization Code Flow with PKCE

```typescript
// PKCE (Proof Key for Code Exchange): required for public clients (SPA, mobile)
import crypto from 'crypto'

// Step 1: Generate PKCE verifier and challenge
function generatePKCE(): { verifier: string; challenge: string } {
  const verifier = crypto.randomBytes(32).toString('base64url')
  const challenge = crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url')
  return { verifier, challenge }
}

// Step 2: Build authorization URL
function getAuthorizationUrl(config: OAuthConfig): { url: string; state: string; pkce: PKCE } {
  const state = crypto.randomBytes(16).toString('hex')
  const pkce = generatePKCE()

  const params = new URLSearchParams({
    response_type: 'code',
    client_id: config.clientId,
    redirect_uri: config.redirectUri,
    scope: 'openid profile email',
    state,
    code_challenge: pkce.challenge,
    code_challenge_method: 'S256',
    prompt: 'consent',            // Force consent screen
    nonce: crypto.randomUUID(),   // Replay protection
  })

  return {
    url: `${config.authorizationEndpoint}?${params}`,
    state,
    pkce,
  }
}

// Step 3: Exchange code for tokens
async function exchangeCodeForTokens(
  code: string,
  verifier: string,
  config: OAuthConfig
): Promise<TokenSet> {
  const response = await fetch(config.tokenEndpoint, {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({
      grant_type: 'authorization_code',
      code,
      redirect_uri: config.redirectUri,
      client_id: config.clientId,
      code_verifier: verifier,
    }),
  })

  if (!response.ok) {
    const error = await response.json()
    throw new Error(`Token exchange failed: ${error.error_description}`)
  }

  return response.json() as Promise<TokenSet>
}
```

## Token Refresh Strategy

```typescript
interface TokenSet {
  access_token: string
  refresh_token: string
  id_token: string
  expires_in: number        // seconds
  token_type: 'Bearer'
}

class TokenManager {
  private refreshTimer: NodeJS.Timeout | null = null

  async setTokens(tokens: TokenSet): Promise<void> {
    // Store tokens securely (httpOnly cookies or encrypted storage)
    await secureStore.set('access_token', tokens.access_token)
    await secureStore.set('refresh_token', tokens.refresh_token)

    // Schedule refresh before expiry (refresh at 75% of lifetime)
    const refreshIn = tokens.expires_in * 0.75 * 1000
    this.scheduleRefresh(refreshIn)
  }

  private scheduleRefresh(delayMs: number): void {
    if (this.refreshTimer) clearTimeout(this.refreshTimer)
    this.refreshTimer = setTimeout(() => this.refresh(), delayMs)
  }

  private async refresh(): Promise<void> {
    const refreshToken = await secureStore.get('refresh_token')
    if (!refreshToken) {
      this.emit('session_expired')
      return
    }

    try {
      const response = await fetch(config.tokenEndpoint, {
        method: 'POST',
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        body: new URLSearchParams({
          grant_type: 'refresh_token',
          refresh_token: refreshToken,
          client_id: config.clientId,
        }),
      })

      if (!response.ok) throw new Error('Refresh failed')

      const tokens = await response.json() as TokenSet
      await this.setTokens(tokens)
    } catch (err) {
      // Refresh token expired or revoked
      await this.clearTokens()
      this.emit('session_expired')
    }
  }

  async clearTokens(): Promise<void> {
    if (this.refreshTimer) clearTimeout(this.refreshTimer)
    await secureStore.delete('access_token')
    await secureStore.delete('refresh_token')
  }
}
```

## Social Login Integration

```typescript
// Provider-specific configurations
const OAUTH_PROVIDERS: Record<string, OAuthConfig> = {
  google: {
    clientId: process.env.GOOGLE_CLIENT_ID!,
    clientSecret: process.env.GOOGLE_CLIENT_SECRET!,
    authorizationEndpoint: 'https://accounts.google.com/o/oauth2/v2/auth',
    tokenEndpoint: 'https://oauth2.googleapis.com/token',
    userInfoEndpoint: 'https://www.googleapis.com/oauth2/v3/userinfo',
    scopes: ['openid', 'profile', 'email'],
  },
  github: {
    clientId: process.env.GITHUB_CLIENT_ID!,
    clientSecret: process.env.GITHUB_CLIENT_SECRET!,
    authorizationEndpoint: 'https://github.com/login/oauth/authorize',
    tokenEndpoint: 'https://github.com/login/oauth/access_token',
    userInfoEndpoint: 'https://api.github.com/user',
    scopes: ['user:email'],
  },
}

// Callback handler: link social account to internal user
async function handleOAuthCallback(
  provider: string,
  code: string,
  state: string
): Promise<{ user: User; session: Session }> {
  // Verify state matches stored state (CSRF protection)
  const storedState = await sessionStore.get(`oauth_state_${state}`)
  if (!storedState) throw new Error('Invalid state parameter')

  const config = OAUTH_PROVIDERS[provider]
  if (!config) throw new Error(`Unknown provider: ${provider}`)

  // Exchange code for tokens
  const tokens = await exchangeCodeForTokens(code, storedState.verifier, config)

  // Fetch user profile from provider
  const profile = await fetchUserProfile(config.userInfoEndpoint, tokens.access_token)

  // Find or create user (link social identity)
  let user = await db.user.findFirst({
    where: {
      socialAccounts: {
        some: { provider, providerUserId: profile.sub }
      }
    }
  })

  if (!user) {
    user = await db.user.create({
      data: {
        email: profile.email,
        displayName: profile.name,
        socialAccounts: {
          create: {
            provider,
            providerUserId: profile.sub,
            email: profile.email,
          }
        }
      }
    })
  }

  const session = await createSession(user.id)
  return { user, session }
}
```

## Session Management

```typescript
import { SignJWT, jwtVerify } from 'jose'

const SESSION_SECRET = new TextEncoder().encode(process.env.SESSION_SECRET!)

async function createSession(userId: string): Promise<string> {
  const sessionId = crypto.randomUUID()

  // Store session server-side (not just JWT)
  await db.session.create({
    data: {
      id: sessionId,
      userId,
      expiresAt: new Date(Date.now() + 24 * 60 * 60 * 1000),  // 24h
      createdAt: new Date(),
    }
  })

  // Issue signed session token
  const token = await new SignJWT({ sub: userId, sid: sessionId })
    .setProtectedHeader({ alg: 'HS256' })
    .setIssuedAt()
    .setExpirationTime('24h')
    .sign(SESSION_SECRET)

  return token
}

// Set session cookie (httpOnly, secure, sameSite)
function setSessionCookie(res: Response, token: string): void {
  res.cookie('session', token, {
    httpOnly: true,       // Not accessible via JavaScript
    secure: true,         // HTTPS only
    sameSite: 'lax',      // CSRF protection
    maxAge: 24 * 60 * 60 * 1000,
    path: '/',
    domain: '.example.com',
  })
}

// Validate session middleware
async function validateSession(req: Request, res: Response, next: NextFunction) {
  const token = req.cookies.session
  if (!token) return res.status(401).json({ error: 'No session' })

  try {
    const { payload } = await jwtVerify(token, SESSION_SECRET)
    const session = await db.session.findUnique({ where: { id: payload.sid as string } })

    if (!session || session.expiresAt < new Date()) {
      return res.status(401).json({ error: 'Session expired' })
    }

    req.user = { id: payload.sub as string, sessionId: session.id }
    next()
  } catch {
    return res.status(401).json({ error: 'Invalid session' })
  }
}
```

## Checklist

- [ ] PKCE enabled for all public clients (SPA, mobile, CLI)
- [ ] State parameter validated on callback (CSRF protection)
- [ ] Tokens stored in httpOnly secure cookies (not localStorage)
- [ ] Refresh tokens rotated on each use (detect token theft)
- [ ] Session validated server-side (not just JWT expiry)
- [ ] Social login links to internal user account (not provider-dependent)
- [ ] Nonce in OIDC requests for replay protection
- [ ] Logout: revoke tokens + clear session + clear cookies

## Anti-Patterns

- Storing tokens in localStorage (XSS exposes all tokens)
- Implicit grant flow (deprecated, tokens in URL fragment)
- Not validating state parameter: vulnerable to CSRF
- Long-lived access tokens without refresh mechanism
- Trusting JWT without server-side session validation (no revocation)
- Hardcoding client secrets in frontend code (use backend proxy)
