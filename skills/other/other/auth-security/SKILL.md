---
name: auth-security
description: OAuth 2.1 + JWT authentication security best practices. Use when implementing auth, API authorization, token management. Follows RFC 9700 (2025).
---
# Auth Security

## Core Principles

- **OAuth 2.1** — Follow RFC 9700 (January 2025)
- **PKCE Required** — All clients must use PKCE
- **Short-lived Tokens** — Access tokens expire in 5-15 minutes
- **Token Rotation** — Refresh tokens are single-use
- **HttpOnly Storage** — Browser tokens in HttpOnly cookies
- **Explicit Algorithm** — Never trust JWT header algorithm
- **No backwards compatibility** — Delete deprecated auth flows

---

## OAuth 2.1 Key Changes

### Deprecated Flows (DO NOT USE)

| Flow | Status | Replacement |
|------|--------|-------------|
| Implicit Grant | Removed | Authorization Code + PKCE |
| Password Grant | Removed | Authorization Code + PKCE |
| Auth Code without PKCE | Removed | Must use PKCE |

### Required: Authorization Code + PKCE

```typescript
import crypto from 'crypto';

// 1. Generate code verifier (43-128 chars)
function generateCodeVerifier(): string {
  return crypto.randomBytes(32).toString('base64url');
}

// 2. Generate code challenge
function generateCodeChallenge(verifier: string): string {
  return crypto
    .createHash('sha256')
    .update(verifier)
    .digest('base64url');
}

// 3. Authorization request
const verifier = generateCodeVerifier();
const challenge = generateCodeChallenge(verifier);

const authUrl = new URL('https://auth.example.com/authorize');
authUrl.searchParams.set('response_type', 'code');
authUrl.searchParams.set('client_id', CLIENT_ID);
authUrl.searchParams.set('redirect_uri', REDIRECT_URI);
authUrl.searchParams.set('code_challenge', challenge);
authUrl.searchParams.set('code_challenge_method', 'S256');
authUrl.searchParams.set('scope', 'openid profile email');
authUrl.searchParams.set('state', generateState());

// 4. Token exchange (after redirect)
const tokenResponse = await fetch('https://auth.example.com/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: new URLSearchParams({
    grant_type: 'authorization_code',
    code: authorizationCode,
    redirect_uri: REDIRECT_URI,
    client_id: CLIENT_ID,
    code_verifier: verifier, // Prove we initiated the request
  }),
});
```

---

## JWT Best Practices

### Algorithm Selection (2025)

| Priority | Algorithm | Notes |
|----------|-----------|-------|
| 1 | EdDSA (Ed25519) | Most secure, quantum-resistant properties |
| 2 | ES256 (ECDSA P-256) | Widely supported, compact signatures |
| 3 | PS256 (RSA-PSS) | More secure than RS256 |
| 4 | RS256 (RSA PKCS#1) | Best compatibility |

```typescript
// Recommended: ES256
import { SignJWT, jwtVerify } from 'jose';

const privateKey = await importPKCS8(PRIVATE_KEY_PEM, 'ES256');
const publicKey = await importSPKI(PUBLIC_KEY_PEM, 'ES256');

// Sign
const token = await new SignJWT({ sub: userId, scope: 'read write' })
  .setProtectedHeader({ alg: 'ES256', typ: 'JWT', kid: keyId })
  .setIssuer('https://auth.example.com')
  .setAudience('https://api.example.com')
  .setExpirationTime('15m')
  .setIssuedAt()
  .setJti(crypto.randomUUID())
  .sign(privateKey);
```

### Token Structure

```typescript
interface AccessTokenPayload {
  // Standard claims
  iss: string;  // Issuer
  sub: string;  // Subject (user ID)
  aud: string;  // Audience
  exp: number;  // Expiration (Unix timestamp)
  iat: number;  // Issued at
  jti: string;  // JWT ID (unique identifier)

  // Custom claims
  scope: string;      // Permissions
  email?: string;     // User email
  roles?: string[];   // User roles
}
```

### Verification (Critical)

```typescript
import { jwtVerify, errors } from 'jose';

async function verifyAccessToken(token: string): Promise<AccessTokenPayload> {
  try {
    const { payload } = await jwtVerify(token, publicKey, {
      // CRITICAL: Explicitly specify allowed algorithms
      algorithms: ['ES256'],

      // Validate standard claims
      issuer: 'https://auth.example.com',
      audience: 'https://api.example.com',

      // Clock tolerance for sync issues
      clockTolerance: 30,
    });

    // Additional validation
    if (!payload.scope?.includes('read')) {
      throw new Error('Insufficient scope');
    }

    return payload as AccessTokenPayload;
  } catch (err) {
    if (err instanceof errors.JWTExpired) {
      throw new AuthError('Token expired', 'TOKEN_EXPIRED');
    }
    if (err instanceof errors.JWTClaimValidationFailed) {
      throw new AuthError('Invalid token claims', 'INVALID_CLAIMS');
    }
    throw new AuthError('Invalid token', 'INVALID_TOKEN');
  }
}
```

---

## Token Storage

### Web Applications

```typescript
// Set token in HttpOnly cookie (server-side)
function setAuthCookie(res: Response, token: string) {
  res.cookie('access_token', token, {
    httpOnly: true,     // Not accessible via JavaScript
    secure: true,       // HTTPS only
    sameSite: 'strict', // CSRF protection
    maxAge: 15 * 60 * 1000, // 15 minutes
    path: '/api',       // Only sent to API routes
  });
}

// Refresh token (longer-lived)
function setRefreshCookie(res: Response, token: string) {
  res.cookie('refresh_token', token, {
    httpOnly: true,
    secure: true,
    sameSite: 'strict',
    maxAge: 7 * 24 * 60 * 60 * 1000, // 7 days
    path: '/api/auth/refresh',  // Only for refresh endpoint
  });
}
```

### Single Page Applications (SPA)

```typescript
// Store in memory (NOT localStorage/sessionStorage)
class TokenManager {
  private accessToken: string | null = null;

  setToken(token: string) {
    this.accessToken = token;
  }

  getToken(): string | null {
    return this.accessToken;
  }

  clearToken() {
    this.accessToken = null;
  }
}

// Use with Refresh Token Rotation
// Refresh token in HttpOnly cookie
// Access token in memory
```

### Storage Comparison

| Storage | XSS Safe | CSRF Safe | Persistence |
|---------|----------|-----------|-------------|
| HttpOnly Cookie | Yes | Needs SameSite | Yes |
| Memory | Yes | Yes | No (lost on reload) |
| localStorage | No | Yes | Yes |
| sessionStorage | No | Yes | Tab only |

---

## Refresh Token Rotation

### Flow

```
1. Client sends refresh_token
2. Server validates refresh_token
3. Server generates NEW access_token + NEW refresh_token
4. Server INVALIDATES old refresh_token
5. Server returns new tokens
6. Client stores new tokens
```

### Implementation

```typescript
async function refreshTokens(refreshToken: string) {
  // Find token in database
  const stored = await db.refreshToken.findUnique({
    where: { token: hashToken(refreshToken) },
    include: { user: true },
  });

  if (!stored) {
    throw new AuthError('Invalid refresh token', 'INVALID_TOKEN');
  }

  // Check if already used (reuse detection)
  if (stored.usedAt) {
    // Potential token theft - revoke ALL user tokens
    await db.refreshToken.deleteMany({
      where: { userId: stored.userId },
    });

    // Alert security team
    await alertSecurityTeam({
      event: 'REFRESH_TOKEN_REUSE',
      userId: stored.userId,
      tokenId: stored.id,
    });

    throw new AuthError('Token reuse detected', 'TOKEN_REUSE');
  }

  // Check expiration
  if (stored.expiresAt < new Date()) {
    throw new AuthError('Refresh token expired', 'TOKEN_EXPIRED');
  }

  // Mark as used (but keep for reuse detection)
  await db.refreshToken.update({
    where: { id: stored.id },
    data: { usedAt: new Date() },
  });

  // Generate new tokens
  const newAccessToken = await generateAccessToken(stored.user);
  const newRefreshToken = await generateRefreshToken(stored.user);

  // Store new refresh token
  await db.refreshToken.create({
    data: {
      token: hashToken(newRefreshToken),
      userId: stored.userId,
      expiresAt: addDays(new Date(), 7),
      previousTokenId: stored.id, // Chain for audit
    },
  });

  return {
    accessToken: newAccessToken,
    refreshToken: newRefreshToken,
  };
}
```

---

## Attack Prevention

### Algorithm Confusion

```typescript
// WRONG: Trusts header algorithm
jwt.verify(token, key); // Uses alg from header

// CORRECT: Explicit algorithm
jwt.verify(token, key, { algorithms: ['ES256'] });
```

### CSRF Protection

```typescript
// Use SameSite cookies
res.cookie('session', token, {
  sameSite: 'strict', // or 'lax' for cross-site links
});

// Or double-submit cookie pattern
const csrfToken = crypto.randomBytes(32).toString('hex');
res.cookie('csrf', csrfToken, { httpOnly: false });
// Client sends csrf token in header
```

### XSS Protection

```typescript
// Content Security Policy
res.setHeader('Content-Security-Policy', [
  "default-src 'self'",
  "script-src 'self'",
  "style-src 'self' 'unsafe-inline'",
].join('; '));

// Use HttpOnly cookies for tokens
// Never store tokens in localStorage
```

### Token Binding (DPoP)

```typescript
// Demonstration of Proof of Possession
// Bind token to client's key pair

const dpopProof = await new SignJWT({
  htm: 'POST',
  htu: 'https://api.example.com/resource',
  ath: await hashAccessToken(accessToken), // Access token hash
})
  .setProtectedHeader({ alg: 'ES256', typ: 'dpop+jwt', jwk: publicKey })
  .setJti(crypto.randomUUID())
  .setIssuedAt()
  .sign(privateKey);

// Send with request
fetch('https://api.example.com/resource', {
  headers: {
    Authorization: `DPoP ${accessToken}`,
    DPoP: dpopProof,
  },
});
```

---

## Token Revocation

```typescript
// Revoke all user tokens (e.g., password change, logout all)
async function revokeAllUserTokens(userId: string) {
  await db.refreshToken.deleteMany({
    where: { userId },
  });

  // If using token blacklist for access tokens
  await redis.sadd(`revoked:${userId}`, Date.now());
  await redis.expire(`revoked:${userId}`, 15 * 60); // 15 min (access token lifetime)
}

// Check blacklist during verification
async function isTokenRevoked(userId: string, iat: number): Promise<boolean> {
  const revokedAt = await redis.get(`revoked:${userId}`);
  return revokedAt && parseInt(revokedAt) > iat * 1000;
}
```

---

## Checklist

```markdown
## OAuth 2.1
- [ ] Using Authorization Code flow
- [ ] PKCE enabled for all clients
- [ ] No implicit or password grants
- [ ] Redirect URI exact matching

## JWT
- [ ] Using ES256 or EdDSA algorithm
- [ ] Explicit algorithm verification
- [ ] Short expiration (≤15 min)
- [ ] Unique jti for each token
- [ ] Issuer and audience validation

## Tokens
- [ ] HttpOnly cookies for web apps
- [ ] Refresh token rotation enabled
- [ ] Reuse detection implemented
- [ ] Token revocation mechanism

## Security
- [ ] HTTPS everywhere
- [ ] SameSite cookies
- [ ] CSP headers configured
- [ ] Rate limiting on auth endpoints
- [ ] Brute force protection
```

---

## See Also

- [reference/oauth2.1.md](reference/oauth2.1.md) — OAuth 2.1 deep dive
- [reference/jwt.md](reference/jwt.md) — JWT patterns
- [reference/attacks.md](reference/attacks.md) — Attack prevention
