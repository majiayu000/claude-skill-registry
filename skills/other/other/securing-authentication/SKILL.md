---
name: securing-authentication
description: Authentication, authorization, and API security implementation. Use when building user systems, protecting APIs, or implementing access control. Covers OAuth 2.1/OIDC, JWT patterns, sessions, Passkeys/WebAuthn, RBAC/ABAC/ReBAC, policy engines (OPA, Casbin, SpiceDB), managed auth (Clerk, Auth0), self-hosted (Keycloak, Ory), and API security best practices.
---

# Authentication & Security

Implement modern authentication, authorization, and API security across Python, Rust, Go, and TypeScript.

## When to Use This Skill

Use this skill when:
- Building user authentication systems (login, signup, SSO)
- Implementing authorization (roles, permissions, access control)
- Securing APIs (JWT validation, rate limiting)
- Adding passwordless auth (Passkeys/WebAuthn)
- Migrating from password-based to modern auth
- Integrating enterprise SSO (SAML, OIDC)
- Implementing fine-grained permissions (RBAC, ABAC, ReBAC)

## OAuth 2.1 Mandatory Requirements (2025 Standard)

```
┌─────────────────────────────────────────────────────────────┐
│           OAuth 2.1 MANDATORY REQUIREMENTS                  │
│                   (RFC 9798 - 2025)                         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ✅ REQUIRED (Breaking Changes from OAuth 2.0)             │
│  ├─ PKCE (Proof Key for Code Exchange) MANDATORY           │
│  │   └─ S256 method (SHA-256), minimum entropy 43 chars   │
│  ├─ Exact redirect URI matching                            │
│  │   └─ No wildcard matching, no substring matching       │
│  ├─ Authorization code flow ONLY for public clients       │
│  │   └─ All other flows require confidential client       │
│  └─ TLS 1.2+ required for all endpoints                   │
│                                                             │
│  ❌ REMOVED (No Longer Supported)                          │
│  ├─ Implicit grant (security vulnerabilities)             │
│  ├─ Resource Owner Password Credentials grant              │
│  │   └─ Use OAuth 2.0 Device Flow (RFC 8628) instead      │
│  └─ Bearer token in query parameters                       │
│      └─ Must use Authorization header or POST body        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

**Critical:** PKCE is now mandatory for ALL OAuth flows, not just public clients.

## JWT Best Practices

### Signing Algorithms (Priority Order)

1. **EdDSA with Ed25519** (Recommended)
   - Fastest performance
   - Smallest signature size
   - Modern cryptography

2. **ES256 (ECDSA with P-256)**
   - Good performance
   - Industry standard
   - Wide compatibility

3. **RS256 (RSA)**
   - Legacy compatibility
   - Larger signatures
   - Slower performance

**NEVER allow `alg: none` or algorithm switching attacks.**

### Token Lifetimes (Concrete Values)

- **Access token:** 5-15 minutes
- **Refresh token:** 1-7 days with rotation
- **ID token:** Same as access token (5-15 minutes)

**Refresh token rotation:** Each refresh generates new access AND refresh tokens, invalidating the old refresh token.

### Token Storage

- **Access token:** Memory only (never localStorage)
- **Refresh token:** HTTP-only cookie + SameSite=Strict
- **CSRF token:** Separate non-HTTP-only cookie
- **Never log tokens:** Redact in application logs

### JWT Claims (Required)

```json
{
  "iss": "https://auth.example.com",
  "sub": "user-id-123",
  "aud": "api.example.com",
  "exp": 1234567890,
  "iat": 1234567890,
  "jti": "unique-token-id",
  "scope": "read:profile write:data"
}
```

## Password Hashing with Argon2id

### OWASP 2025 Parameters

```
Algorithm: Argon2id
Memory cost (m): 64 MB (65536 KiB)
Time cost (t): 3 iterations
Parallelism (p): 4 threads
Salt length: 16 bytes (128 bits)
Target hash time: 150-250ms
```

### Implementation

For concrete implementations, see `references/password-hashing.md`.

**Key Points:**
- Argon2id is hybrid: data-independent timing + memory-hard
- Tune memory cost to achieve 150-250ms on YOUR hardware
- Use timing-safe comparison for verification
- Migrate from bcrypt gradually (verify with old, rehash with new)

## Passkeys / WebAuthn

Passkeys provide phishing-resistant, passwordless authentication using FIDO2/WebAuthn.

### When to Use Passkeys

- User-facing applications prioritizing security
- Reducing password-related support burden
- Mobile-first applications (biometric auth)
- Applications requiring MFA without SMS

### Cross-Device Passkey Sync

- **iCloud Keychain:** Apple ecosystem (iOS 16+, macOS 13+)
- **Google Password Manager:** Android, Chrome
- **1Password, Bitwarden:** Third-party password managers

For implementation guide, see `references/passkeys-webauthn.md`.

## Authorization Models

```
┌─────────────────────────────────────────────────────────────┐
│                Authorization Model Selection                │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  Simple Roles (<20 roles)                                  │
│  └─ RBAC with Casbin (embedded, any language)              │
│      Example: Admin, User, Guest                           │
│                                                             │
│  Complex Attribute Rules                                    │
│  └─ ABAC with OPA or Cerbos                                │
│      Example: "Allow if user.clearance >= doc.level        │
│                AND user.dept == doc.dept"                   │
│                                                             │
│  Relationship-Based (Multi-Tenant, Collaborative)          │
│  └─ ReBAC with SpiceDB (Zanzibar model)                    │
│      Example: "Can edit if member of doc's workspace       │
│                AND workspace.plan includes feature"         │
│      Use cases: Notion-like, GitHub-like permissions       │
│                                                             │
│  Kubernetes / Infrastructure Policies                       │
│  └─ OPA (Gatekeeper for admission control)                 │
│      Example: Enforce pod security policies                │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

For detailed comparison, see `references/authorization-patterns.md`.

## Library Selection by Language

### TypeScript

| Use Case | Library | Context7 ID | Trust | Notes |
|----------|---------|-------------|-------|-------|
| Auth Framework | Auth.js v5 | `/websites/authjs_dev` | 87.4 | Multi-framework (Next, Svelte, Solid) |
| JWT | jose 5.x | - | - | EdDSA, ES256, RS256 support |
| Passkeys | @simplewebauthn/server 11.x | - | - | FIDO2 server |
| Validation | Zod 3.x | `/colinhacks/zod` | 90.4 | Schema validation |
| Policy Engine | Casbin.js 1.x | - | - | RBAC/ABAC embedded |

### Python

| Use Case | Library | Notes |
|----------|---------|-------|
| Auth Framework | Authlib 1.3+ | OAuth/OIDC client + server |
| JWT | joserfc 1.x | Modern, maintained |
| Passkeys | py_webauthn 2.x | WebAuthn server |
| Password Hashing | argon2-cffi 24.x | OWASP parameters |
| Validation | Pydantic 2.x | FastAPI integration |
| Policy Engine | PyCasbin 1.x | RBAC/ABAC embedded |

### Rust

| Use Case | Library | Notes |
|----------|---------|-------|
| JWT | jsonwebtoken 10.x | EdDSA, ES256, RS256 |
| OAuth Client | oauth2 5.x | OAuth 2.1 flows |
| Passkeys | webauthn-rs 0.5.x | WebAuthn + attestation |
| Password Hashing | argon2 0.5.x | Native Argon2id |
| Policy Engine | Casbin-RS 2.x | RBAC/ABAC embedded |

### Go

| Use Case | Library | Notes |
|----------|---------|-------|
| JWT | golang-jwt v5 | Community-maintained |
| OAuth Client | go-oidc v3 | OIDC client only |
| Passkeys | go-webauthn 0.11.x | Duo-maintained |
| Password Hashing | golang.org/x/crypto/argon2 | Standard library |
| Policy Engine | Casbin v2 | Original implementation |

## Managed Auth Services

| Service | Best For | Key Features |
|---------|----------|--------------|
| Clerk | Rapid development, startups | Prebuilt UI, Next.js SDK |
| Auth0 | Enterprise, established | 25+ social providers, SSO |
| WorkOS AuthKit | B2B SaaS, enterprise SSO | SAML/SCIM, admin portal |
| Supabase Auth | Postgres users | Built on Postgres, RLS |

For detailed comparison, see `references/managed-auth-comparison.md`.

## Self-Hosted Solutions

| Solution | Language | Use Case |
|----------|----------|----------|
| Keycloak | Java | Enterprise, on-prem |
| Ory | Go | Cloud-native, microservices |
| Authentik | Python | Modern, developer-friendly |

For setup guides, see `references/self-hosted-auth.md`.

## API Security Best Practices

### Rate Limiting

```typescript
// Tiered rate limiting (per IP + per user)
const rateLimits = {
  anonymous: '10 requests/minute',
  authenticated: '100 requests/minute',
  premium: '1000 requests/minute',
}
```

Use sliding window algorithm (not fixed window) with Redis.

### CORS Configuration

```typescript
// Restrictive CORS (production)
const corsOptions = {
  origin: ['https://app.example.com'],
  credentials: true,
  maxAge: 86400, // 24 hours
  allowedHeaders: ['Content-Type', 'Authorization'],
  methods: ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
}

// NEVER use origin: '*' with credentials: true
```

### Security Headers

```typescript
const securityHeaders = {
  'Strict-Transport-Security': 'max-age=63072000; includeSubDomains; preload',
  'X-Frame-Options': 'DENY',
  'X-Content-Type-Options': 'nosniff',
  'Referrer-Policy': 'strict-origin-when-cross-origin',
  'Permissions-Policy': 'geolocation=(), microphone=(), camera=()',
  'Content-Security-Policy': "default-src 'self'; script-src 'self'",
}
```

For complete API security guide, see `references/api-security.md`.

## Frontend Integration Patterns

### Protected Routes (Next.js)

```typescript
// middleware.ts
import { withAuth } from 'next-auth/middleware'

export default withAuth({
  callbacks: {
    authorized: ({ token, req }) => {
      if (req.nextUrl.pathname.startsWith('/dashboard')) {
        return !!token
      }
      if (req.nextUrl.pathname.startsWith('/admin')) {
        return token?.role === 'admin'
      }
      return true
    },
  },
})

export const config = {
  matcher: ['/dashboard/:path*', '/admin/:path*'],
}
```

### Role-Based UI Rendering

```typescript
import { useSession } from 'next-auth/react'

export function AdminPanel() {
  const { data: session } = useSession()

  if (session?.user?.role !== 'admin') {
    return null
  }

  return <div>Admin Controls</div>
}
```

## Common Workflows

### 1. OAuth 2.1 Integration

1. Generate PKCE challenge
2. Redirect to authorization endpoint
3. Handle callback with authorization code
4. Exchange code for tokens (with code_verifier)
5. Store tokens securely
6. Implement refresh token rotation

See `references/oauth21-guide.md` for complete implementation.

### 2. JWT Implementation

1. Generate signing keys using `scripts/generate_jwt_keys.py`
2. Configure token lifetimes (5-15 min access, 1-7 day refresh)
3. Implement token validation middleware
4. Set up refresh token rotation
5. Configure token storage (memory for access, HTTP-only cookie for refresh)

See `references/jwt-best-practices.md` for detailed patterns.

### 3. Passkeys Setup

1. Register credential during signup/settings
2. Generate challenge for registration
3. Verify attestation
4. Store credential ID and public key
5. Implement authentication flow with assertion

See `examples/passkeys-demo/` for runnable implementation.

### 4. Authorization Engine Setup

1. Choose engine (Casbin for simple RBAC, SpiceDB for ReBAC)
2. Define schema/policies
3. Implement check functions
4. Integrate with route handlers
5. Add audit logging

See `references/authorization-patterns.md` for detailed comparison.

## Integration with Other Skills

### Forms Skill
- Login/register forms with validation
- Error states for auth failures
- Password strength indicators
- Email validation

### API Patterns Skill
- JWT middleware integration
- Error response formats (401, 403)
- OpenAPI security schemas
- CORS configuration

### Dashboards Skill
- Role-based widget visibility
- User profile display
- Permission-based data filtering
- Audit trail visualization

### Observability Skill
- Auth event logging (login, logout, permission denied)
- Failed login tracking
- Token refresh monitoring
- Security incident alerting

## Scripts

### Generate JWT Keys

```bash
python scripts/generate_jwt_keys.py --algorithm EdDSA
```

Generates EdDSA or ES256 key pairs for JWT signing.

### Validate OAuth 2.1 Configuration

```bash
python scripts/validate_oauth_config.py --config oauth.json
```

Validates OAuth 2.1 compliance (PKCE enabled, exact redirect URIs, etc.).

## Examples

### Auth.js + Next.js

Complete implementation with OAuth providers, credentials, and session management.

Location: `examples/authjs-nextjs/`

### Keycloak + FastAPI

Self-hosted Keycloak with FastAPI integration via OIDC.

Location: `examples/keycloak-fastapi/`

### Passkeys Demo

Runnable passkeys implementation with @simplewebauthn.

Location: `examples/passkeys-demo/`

## Reference Documentation

- `references/oauth21-guide.md` - OAuth 2.1 implementation guide
- `references/jwt-best-practices.md` - JWT generation, validation, storage
- `references/passkeys-webauthn.md` - Passkeys/WebAuthn implementation
- `references/authorization-patterns.md` - RBAC, ABAC, ReBAC comparison
- `references/password-hashing.md` - Argon2id parameters, migration
