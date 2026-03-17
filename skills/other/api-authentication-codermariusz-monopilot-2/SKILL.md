---
name: api-authentication
description: Apply when implementing API authentication: JWT tokens, session management, API keys, and auth middleware. Follows JWT Best Current Practices (RFC 8725).
version: 1.1.0
tokens: ~750
confidence: high
sources:
  - https://datatracker.ietf.org/doc/html/rfc7519
  - https://datatracker.ietf.org/doc/html/rfc8725
  - https://oauth.net/2/
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [api, authentication, jwt, security]
---

## When to Use

Apply when implementing API authentication: JWT tokens, session management, API keys, and auth middleware. Follows JWT Best Current Practices (RFC 8725).

## Patterns

### Pattern 1: JWT Authentication
```typescript
// Source: RFC 7519, RFC 8725 (JWT Best Practices)
import jwt from 'jsonwebtoken';

interface TokenPayload {
  userId: string;
  email: string;
  role: string;
}

function generateToken(payload: TokenPayload): string {
  return jwt.sign(payload, process.env.JWT_SECRET!, {
    expiresIn: '1h',      // RFC 8725: Always set expiration
    issuer: 'myapp',
    algorithm: 'HS256',   // RFC 8725: Explicitly specify algorithm
  });
}

function verifyToken(token: string): TokenPayload {
  return jwt.verify(token, process.env.JWT_SECRET!, {
    algorithms: ['HS256'], // RFC 8725: Prevent algorithm confusion
  }) as TokenPayload;
}
```

### Pattern 2: Auth Middleware
```typescript
// Source: Best practice pattern
async function authMiddleware(
  req: NextRequest
): Promise<TokenPayload | null> {
  const authHeader = req.headers.get('authorization');

  if (!authHeader?.startsWith('Bearer ')) {
    return null;
  }

  const token = authHeader.slice(7);

  try {
    return verifyToken(token);
  } catch {
    return null;
  }
}

// In route handler
export async function GET(req: NextRequest) {
  const user = await authMiddleware(req);

  if (!user) {
    return NextResponse.json(
      { error: { code: 'UNAUTHORIZED', message: 'Invalid token' } },
      { status: 401 }
    );
  }

  // user.userId, user.role available
}
```

### Pattern 3: API Key Authentication
```typescript
// Source: Best practice pattern
async function apiKeyMiddleware(req: NextRequest): Promise<ApiClient | null> {
  const apiKey = req.headers.get('x-api-key');

  if (!apiKey) {
    return null;
  }

  // Hash the key before lookup (keys stored hashed)
  const hashedKey = await hashApiKey(apiKey);
  const client = await db.apiClients.findUnique({
    where: { keyHash: hashedKey },
  });

  if (!client || client.revokedAt) {
    return null;
  }

  // Update last used
  await db.apiClients.update({
    where: { id: client.id },
    data: { lastUsedAt: new Date() },
  });

  return client;
}
```

### Pattern 4: Refresh Token Flow
```typescript
// Source: https://oauth.net/2/refresh-tokens/
async function refreshTokens(refreshToken: string) {
  // Verify refresh token
  const payload = verifyRefreshToken(refreshToken);

  // Check if token is revoked
  const stored = await db.refreshTokens.findUnique({
    where: { token: refreshToken },
  });

  if (!stored || stored.revokedAt) {
    throw new UnauthorizedError('Token revoked');
  }

  // Rotate refresh token (invalidate old)
  await db.refreshTokens.update({
    where: { token: refreshToken },
    data: { revokedAt: new Date() },
  });

  // Generate new tokens
  const newAccessToken = generateToken({ userId: payload.userId });
  const newRefreshToken = generateRefreshToken({ userId: payload.userId });

  await db.refreshTokens.create({
    data: { token: newRefreshToken, userId: payload.userId },
  });

  return { accessToken: newAccessToken, refreshToken: newRefreshToken };
}
```

### Pattern 5: Role-Based Access Control
```typescript
// Source: Best practice pattern
function requireRole(...roles: string[]) {
  return async (req: NextRequest) => {
    const user = await authMiddleware(req);

    if (!user) {
      return NextResponse.json({ error: 'Unauthorized' }, { status: 401 });
    }

    if (!roles.includes(user.role)) {
      return NextResponse.json({ error: 'Forbidden' }, { status: 403 });
    }

    return null; // Authorized
  };
}

// Usage
export async function DELETE(req: NextRequest) {
  const error = await requireRole('admin')(req);
  if (error) return error;

  // Admin-only logic
}
```

## Security Best Practices (RFC 8725)

- **Always set token expiration** - Short-lived access tokens (15m-1h)
- **Explicitly specify algorithm** - Prevent algorithm confusion attacks
- **Validate algorithm on verify** - Pass `algorithms` array to `jwt.verify()`
- **Use strong secrets** - Minimum 256 bits for HS256
- **Rotate refresh tokens** - Invalidate old token when issuing new one

## Anti-Patterns

- **JWT in localStorage** - Use httpOnly cookies for web
- **No token expiration** - Always set expiry
- **Storing plain API keys** - Hash before storing
- **No refresh token rotation** - Rotate on use
- **Missing algorithm validation** - Specify allowed algorithms

## Verification Checklist

- [ ] Tokens have expiration
- [ ] Algorithm explicitly specified
- [ ] Refresh tokens are rotated
- [ ] API keys stored hashed
- [ ] Auth errors don't leak info
- [ ] RBAC for sensitive endpoints
