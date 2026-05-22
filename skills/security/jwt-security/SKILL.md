---
name: jwt-security
description: Guidelines for implementing JWT authentication with security best practices for token creation, validation, and storage
---

# JWT Security

You are an expert in JSON Web Token (JWT) security implementation. Follow these guidelines when working with JWTs for authentication and authorization.

## Core Principles

- JWTs are not inherently secure - security depends on implementation
- Always validate tokens server-side, even for internal services
- Use asymmetric signing (RS256, ES256) when possible
- Keep tokens short-lived and implement proper refresh mechanisms
- Never store sensitive data in JWT payloads

## Token Structure

A JWT consists of three parts: Header, Payload, and Signature.

```
header.payload.signature
```

### Header Best Practices

```json
{
  "alg": "RS256",
  "typ": "JWT",
  "kid": "key-identifier-for-rotation"
}
```

- Always include `kid` (key ID) for key rotation support
- Use `typ: "JWT"` explicitly
- Never accept `alg: "none"`

### Payload Best Practices

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-uuid-here",
  "aud": "https://api.example.com",
  "exp": 1704067200,
  "iat": 1704063600,
  "nbf": 1704063600,
  "jti": "unique-token-id"
}
```

Required claims:
- `iss` (issuer): Who created the token
- `sub` (subject): Who the token represents
- `aud` (audience): Who the token is intended for
- `exp` (expiration): When the token expires
- `iat` (issued at): When the token was created

Recommended claims:
- `nbf` (not before): Token not valid before this time
- `jti` (JWT ID): Unique identifier for token revocation

## Signing Algorithm Selection

### Recommended: Asymmetric Algorithms

```javascript
// RS256 - RSA with SHA-256 (most widely supported)
// ES256 - ECDSA with P-256 and SHA-256 (smaller keys)
// EdDSA - Edwards-curve Digital Signature Algorithm (most secure)

const ALLOWED_ALGORITHMS = ['RS256', 'ES256', 'EdDSA'];
```

### When Symmetric is Required

```javascript
// HS256 - HMAC with SHA-256
// Only use with a strong secret (minimum 256 bits / 32 bytes)
const secret = crypto.randomBytes(64).toString('hex');
```

## Token Creation

### Using RS256 (Recommended)

```javascript
const jwt = require('jsonwebtoken');
const fs = require('fs');

const privateKey = fs.readFileSync('private.pem');

function createToken(userId, roles) {
  const payload = {
    sub: userId,
    roles: roles,
    // Keep custom claims minimal
  };

  const options = {
    algorithm: 'RS256',
    expiresIn: '15m', // Short-lived access tokens
    issuer: 'https://auth.example.com',
    audience: 'https://api.example.com',
    keyid: 'current-key-id',
  };

  return jwt.sign(payload, privateKey, options);
}
```

### Token Lifetime Guidelines

```javascript
const TOKEN_LIFETIMES = {
  accessToken: '15m',      // 15 minutes max
  refreshToken: '7d',      // 7 days with rotation
  idToken: '1h',           // 1 hour
  passwordReset: '15m',    // 15 minutes
  emailVerification: '24h', // 24 hours
};
```

## Token Validation

### Complete Validation Example

```javascript
const jwt = require('jsonwebtoken');
const jwksClient = require('jwks-rsa');

// JWKS client for fetching public keys
const client = jwksClient({
  jwksUri: 'https://auth.example.com/.well-known/jwks.json',
  cache: true,
  cacheMaxAge: 600000, // 10 minutes
  rateLimit: true,
  jwksRequestsPerMinute: 10,
});

async function validateToken(token) {
  // 1. Decode header without verification to get kid
  const decoded = jwt.decode(token, { complete: true });

  if (!decoded) {
    throw new Error('Invalid token format');
  }

  // 2. Validate algorithm against whitelist
  if (!ALLOWED_ALGORITHMS.includes(decoded.header.alg)) {
    throw new Error(`Algorithm ${decoded.header.alg} not allowed`);
  }

  // 3. Get signing key
  const key = await client.getSigningKey(decoded.header.kid);
  const publicKey = key.getPublicKey();

  // 4. Verify signature and claims
  const verified = jwt.verify(token, publicKey, {
    algorithms: ALLOWED_ALGORITHMS, // Whitelist algorithms
    issuer: 'https://auth.example.com',
    audience: 'https://api.example.com',
    clockTolerance: 30, // 30 seconds clock skew tolerance
  });

  return verified;
}
```

### Validation Checklist

```javascript
function validateTokenClaims(decoded) {
  const now = Math.floor(Date.now() / 1000);

  // 1. Check expiration
  if (decoded.exp && decoded.exp < now) {
    throw new Error('Token expired');
  }

  // 2. Check not before
  if (decoded.nbf && decoded.nbf > now) {
    throw new Error('Token not yet valid');
  }

  // 3. Check issuer
  if (decoded.iss !== EXPECTED_ISSUER) {
    throw new Error('Invalid issuer');
  }

  // 4. Check audience
  const audiences = Array.isArray(decoded.aud) ? decoded.aud : [decoded.aud];
  if (!audiences.includes(EXPECTED_AUDIENCE)) {
    throw new Error('Invalid audience');
  }

  // 5. Check required claims exist
  if (!decoded.sub) {
    throw new Error('Missing subject claim');
  }

  return true;
}
```

## Security Vulnerabilities to Prevent

### 1. Algorithm Confusion Attack

```javascript
// WRONG: Accepting any algorithm
jwt.verify(token, secret); // Vulnerable!

// CORRECT: Whitelist allowed algorithms
jwt.verify(token, key, { algorithms: ['RS256'] });
```

### 2. None Algorithm Attack

```javascript
// Always reject 'none' algorithm
if (decoded.header.alg === 'none' || decoded.header.alg.toLowerCase() === 'none') {
  throw new Error('Algorithm none is not allowed');
}
```

### 3. Key Confusion (RS256 vs HS256)

```javascript
// When using asymmetric keys, never allow symmetric algorithms
const ASYMMETRIC_ONLY = ['RS256', 'RS384', 'RS512', 'ES256', 'ES384', 'ES512', 'EdDSA'];

jwt.verify(token, publicKey, { algorithms: ASYMMETRIC_ONLY });
```

### 4. Weak HMAC Secrets

```javascript
// Minimum 256-bit (32 byte) secret for HS256
// Minimum 384-bit (48 byte) secret for HS384
// Minimum 512-bit (64 byte) secret for HS512

function generateHmacSecret(algorithm) {
  const bits = parseInt(algorithm.slice(2)); // HS256 -> 256
  const bytes = bits / 8;
  return crypto.randomBytes(Math.max(bytes, 32)).toString('hex');
}
```

## Token Storage

### Browser Storage Security

```javascript
// Best: HttpOnly cookie (requires backend support)
// Server sets:
res.cookie('access_token', token, {
  httpOnly: true,
  secure: true,
  sameSite: 'strict',
  maxAge: 900000, // 15 minutes
});

// Acceptable: In-memory (lost on refresh)
let accessToken = null;
function setToken(token) {
  accessToken = token;
}

// Avoid: localStorage (vulnerable to XSS)
// Avoid: sessionStorage for sensitive tokens
```

### Token Transmission

```javascript
// Always use Authorization header
fetch('/api/resource', {
  headers: {
    Authorization: `Bearer ${accessToken}`,
  },
});

// Never put tokens in URLs (logged, cached, visible in history)
// WRONG: /api/resource?token=eyJ...
```

## Refresh Token Implementation

```javascript
// Refresh tokens should be:
// 1. Stored securely (httpOnly cookie or secure server-side storage)
// 2. Rotated on each use
// 3. Bound to the client (if possible)

async function refreshAccessToken(refreshToken) {
  // Validate refresh token
  const decoded = await validateRefreshToken(refreshToken);

  // Check if token has been revoked
  const isRevoked = await checkTokenRevocation(decoded.jti);
  if (isRevoked) {
    throw new Error('Refresh token has been revoked');
  }

  // Generate new tokens
  const newAccessToken = createAccessToken(decoded.sub);
  const newRefreshToken = createRefreshToken(decoded.sub);

  // Revoke old refresh token (rotation)
  await revokeToken(decoded.jti);

  return { accessToken: newAccessToken, refreshToken: newRefreshToken };
}
```

## Token Revocation

```javascript
// Maintain a revocation list for early token invalidation
const revokedTokens = new Set(); // Use Redis in production

function revokeToken(jti) {
  revokedTokens.add(jti);
}

function isTokenRevoked(jti) {
  return revokedTokens.has(jti);
}

// Include revocation check in validation
async function validateToken(token) {
  const decoded = jwt.verify(token, key, options);

  if (decoded.jti && isTokenRevoked(decoded.jti)) {
    throw new Error('Token has been revoked');
  }

  return decoded;
}
```

## Key Rotation

```javascript
// Support multiple keys during rotation
const keyStore = {
  'key-2024-01': { /* current key */ },
  'key-2023-12': { /* previous key, still valid */ },
};

// JWKS endpoint should expose all valid public keys
app.get('/.well-known/jwks.json', (req, res) => {
  const keys = Object.entries(keyStore).map(([kid, key]) => ({
    kid,
    kty: 'RSA',
    use: 'sig',
    alg: 'RS256',
    n: key.publicKey.n,
    e: key.publicKey.e,
  }));

  res.json({ keys });
});
```

## Express Middleware Example

```javascript
const expressJwt = require('express-jwt');
const jwksRsa = require('jwks-rsa');

const jwtMiddleware = expressJwt({
  secret: jwksRsa.expressJwtSecret({
    cache: true,
    rateLimit: true,
    jwksRequestsPerMinute: 5,
    jwksUri: 'https://auth.example.com/.well-known/jwks.json',
  }),
  audience: 'https://api.example.com',
  issuer: 'https://auth.example.com',
  algorithms: ['RS256'],
});

// Protected route
app.get('/api/protected', jwtMiddleware, (req, res) => {
  // req.auth contains the decoded token
  res.json({ user: req.auth.sub });
});
```

## Testing

```javascript
describe('JWT Validation', () => {
  it('should reject expired tokens', async () => {
    const expiredToken = createToken({ exp: Math.floor(Date.now() / 1000) - 3600 });
    await expect(validateToken(expiredToken)).rejects.toThrow('expired');
  });

  it('should reject tokens with wrong issuer', async () => {
    const wrongIssuer = createToken({ iss: 'https://evil.com' });
    await expect(validateToken(wrongIssuer)).rejects.toThrow('issuer');
  });

  it('should reject none algorithm', async () => {
    const noneAlg = 'eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJzdWIiOiIxMjM0NTY3ODkwIn0.';
    await expect(validateToken(noneAlg)).rejects.toThrow('algorithm');
  });
});
```

## Common Anti-Patterns to Avoid

1. Using JWTs for session management (prefer server-side sessions for web apps)
2. Storing sensitive data in JWT payload (it's only encoded, not encrypted)
3. Not validating all claims
4. Using weak or hardcoded secrets
5. Not implementing token expiration
6. Trusting the algorithm header without validation
7. Not implementing refresh token rotation
8. Logging full tokens
