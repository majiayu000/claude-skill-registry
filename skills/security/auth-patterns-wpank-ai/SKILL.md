---
name: auth-patterns
model: standard
description: Authentication and authorization patterns — JWT, OAuth 2.0, sessions, RBAC/ABAC, password security, MFA, and vulnerability prevention. Use when implementing login flows, protecting routes, managing tokens, or auditing auth security.
---

# Auth Patterns — Authentication & Authorization

> **SECURITY-CRITICAL SKILL** — Auth is the front door. Get it wrong and nothing else matters.

## Authentication Methods

| Method | How It Works | Best For |
|--------|-------------|----------|
| **JWT** | Signed token sent with each request | SPAs, microservices, mobile APIs |
| **Session-based** | Server stores session, client holds cookie | Traditional web apps, SSR |
| **OAuth 2.0** | Delegated auth via authorization server | "Login with Google/GitHub", API access |
| **API Keys** | Static key sent in header | Internal services, public APIs |
| **Magic Links** | One-time login link via email | Low-friction onboarding, B2C |
| **Passkeys/WebAuthn** | Hardware/biometric challenge-response | High-security apps, passwordless |


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install auth-patterns
```


---

## JWT Patterns

### Dual-Token Strategy

Short-lived access token + long-lived refresh token:

```
Client → POST /auth/login → Server
Client ← { access_token, refresh_token }

Client → GET /api/data (Authorization: Bearer <access>) → Server
Client ← 401 Expired

Client → POST /auth/refresh { refresh_token } → Server
Client ← { new_access_token, rotated_refresh_token }
```

### Token Structure

```json
{
  "header": { "alg": "RS256", "typ": "JWT", "kid": "key-2024-01" },
  "payload": {
    "sub": "user_abc123",
    "iss": "https://auth.example.com",
    "aud": "https://api.example.com",
    "exp": 1700000900,
    "iat": 1700000000,
    "jti": "unique-token-id",
    "roles": ["user"],
    "scope": "read:profile write:profile"
  }
}
```

### Signing Algorithms

| Algorithm | Type | When to Use |
|-----------|------|-------------|
| **RS256** | Asymmetric (RSA) | Microservices — only auth server holds private key |
| **ES256** | Asymmetric (ECDSA) | Same as RS256, smaller keys and signatures |
| **HS256** | Symmetric | Single-server apps — all verifiers share secret |

Prefer RS256/ES256 in distributed systems.

### Token Storage

| Storage | XSS Safe | CSRF Safe | Recommendation |
|---------|----------|-----------|----------------|
| **httpOnly cookie** | Yes | No (add CSRF token) | **Best for web apps** |
| **localStorage** | No | Yes | Avoid — XSS exposes tokens |
| **In-memory** | Yes | Yes | Good for SPAs, lost on refresh |

```
Set-Cookie: access_token=eyJ...; HttpOnly; Secure; SameSite=Strict; Path=/; Max-Age=900
```

### Expiration Strategy

| Token | Lifetime | Rotation |
|-------|----------|----------|
| **Access token** | 5–15 minutes | Issued on refresh |
| **Refresh token** | 7–30 days | Rotate on every use |
| **ID token** | Match access token | Not refreshed |

---

## OAuth 2.0 Flows

| Flow | Client Type | When to Use |
|------|-------------|-------------|
| **Authorization Code + PKCE** | Public (SPA, mobile) | **Default for all public clients** |
| **Authorization Code** | Confidential (server) | Server-rendered web apps with backend |
| **Client Credentials** | Machine-to-machine | Service-to-service, cron jobs |
| **Device Code** | Input-constrained | Smart TVs, IoT, CLI on headless servers |

> **Implicit flow is deprecated.** Always use Authorization Code + PKCE for public clients.

### PKCE Flow

```
1. Client generates code_verifier (random 43-128 chars)
2. Client computes code_challenge = BASE64URL(SHA256(code_verifier))
3. Redirect to /authorize?code_challenge=...&code_challenge_method=S256
4. User authenticates, server redirects back with authorization code
5. Client exchanges code + code_verifier for tokens at /token
6. Server verifies SHA256(code_verifier) == code_challenge
```

---

## Session Management

### Server-Side Sessions

```
Client Cookie:  session_id=a1b2c3d4 (opaque, random, no user data)
Server Store:   { "a1b2c3d4": { userId: 123, roles: ["admin"], expiresAt: ... } }
```

| Store | Speed | When to Use |
|-------|-------|-------------|
| **Redis** | Fast | Production default — TTL support, horizontal scaling |
| **PostgreSQL** | Moderate | When Redis is overkill, need audit trail |
| **In-memory** | Fastest | Development only |

### Session Security

| Threat | Prevention |
|--------|------------|
| Session fixation | Regenerate session ID after login |
| Session hijacking | httpOnly + Secure cookies, bind to IP/user-agent |
| CSRF | SameSite cookies + CSRF tokens |
| Idle timeout | Expire after 15–30 min inactivity |
| Absolute timeout | Force re-auth after 8–24 hours |

---

## Authorization Patterns

| Pattern | Granularity | When to Use |
|---------|-------------|-------------|
| **RBAC** | Coarse (admin, editor, viewer) | Most apps — simple role hierarchy |
| **ABAC** | Fine (attributes: dept, time, location) | Enterprise — context-dependent access |
| **Permission-based** | Medium (post:create, user:delete) | APIs — decouple permissions from roles |
| **Policy-based (OPA/Cedar)** | Fine | Microservices — externalized, auditable rules |
| **ReBAC** | Fine (owner, member, shared-with) | Social apps, Google Drive-style sharing |

### RBAC Implementation

```typescript
const ROLE_PERMISSIONS: Record<string, string[]> = {
  admin:  ["user:read", "user:write", "user:delete", "post:read", "post:write", "post:delete"],
  editor: ["user:read", "post:read", "post:write"],
  viewer: ["user:read", "post:read"],
};

function requirePermission(permission: string) {
  return (req: Request, res: Response, next: NextFunction) => {
    const permissions = ROLE_PERMISSIONS[req.user.role] ?? [];
    if (!permissions.includes(permission)) {
      return res.status(403).json({ error: "Forbidden" });
    }
    next();
  };
}

app.delete("/api/users/:id", requirePermission("user:delete"), deleteUser);
```

---

## Password Security

| Algorithm | Recommended | Memory-Hard | Notes |
|-----------|------------|-------------|-------|
| **Argon2id** | **First choice** | Yes | Resists GPU/ASIC attacks |
| **bcrypt** | Yes | No | Battle-tested, 72-byte limit |
| **scrypt** | Yes | Yes | Good alternative |
| **PBKDF2** | Acceptable | No | NIST approved, weaker vs GPU |
| **SHA-256/MD5** | **Never** | No | Not password hashing |

**NIST 800-63B:** Favor length (12+ chars) over complexity rules. Check against breached password lists. Don't force periodic rotation unless breach suspected.

---

## Multi-Factor Authentication

| Factor | Security | Notes |
|--------|----------|-------|
| **TOTP (Authenticator app)** | High | Offline-capable, Google Authenticator / Authy |
| **WebAuthn/Passkeys** | Highest | Phishing-resistant, hardware-backed |
| **SMS OTP** | Medium | Vulnerable to SIM swap — avoid for high-security |
| **Hardware keys (FIDO2)** | Highest | YubiKey — best for admin accounts |
| **Backup codes** | Low (fallback) | One-time use, generate 10, store hashed |

---

## Security Headers

| Header | Value |
|--------|-------|
| **Strict-Transport-Security** | `max-age=63072000; includeSubDomains; preload` |
| **Content-Security-Policy** | Restrict script sources, no inline scripts |
| **X-Content-Type-Options** | `nosniff` |
| **X-Frame-Options** | `DENY` |
| **Referrer-Policy** | `strict-origin-when-cross-origin` |
| **CORS** | Whitelist specific origins, never `*` with credentials |

---

## Common Vulnerabilities

| # | Vulnerability | Prevention |
|---|--------------|------------|
| 1 | Broken authentication | MFA, strong password policy, breach detection |
| 2 | Session fixation | Regenerate session ID on login |
| 3 | JWT `alg:none` attack | Reject `none`, validate `alg` against allowlist |
| 4 | JWT secret brute force | Use RS256/ES256, strong secrets (256+ bits) |
| 5 | CSRF | SameSite cookies, CSRF tokens |
| 6 | Credential stuffing | Rate limiting, breached password check, MFA |
| 7 | Insecure password storage | Argon2id/bcrypt, never encrypt (hash instead) |
| 8 | Insecure password reset | Signed time-limited tokens, invalidate after use |
| 9 | Open redirect | Validate redirect URIs against allowlist |
| 10 | Token leakage in URL | Send tokens in headers or httpOnly cookies only |
| 11 | Privilege escalation | Server-side role checks on every request |
| 12 | OAuth redirect_uri mismatch | Exact match redirect URI validation, no wildcards |
| 13 | Timing attacks | Constant-time comparison for secrets |

---

## NEVER Do

| # | Rule | Why |
|---|------|-----|
| 1 | **NEVER store passwords in plaintext or reversible encryption** | One breach exposes every user |
| 2 | **NEVER put tokens in URLs or query parameters** | Logged by servers, proxies, referrer headers |
| 3 | **NEVER use `alg: none` or allow algorithm switching in JWTs** | Attacker forges tokens |
| 4 | **NEVER trust client-side role/permission claims** | Users can modify any client-side value |
| 5 | **NEVER use MD5, SHA-1, or plain SHA-256 for password hashing** | No salt, no work factor — cracked in seconds |
| 6 | **NEVER skip HTTPS in production** | Tokens and credentials sent in cleartext |
| 7 | **NEVER log tokens, passwords, or secrets** | Logs are broadly accessible and retained |
| 8 | **NEVER use long-lived tokens without rotation** | A single leak grants indefinite access |
| 9 | **NEVER implement your own crypto** | Use established libraries — jose, bcrypt, passport |
| 10 | **NEVER return different errors for "user not found" vs "wrong password"** | Enables user enumeration |
