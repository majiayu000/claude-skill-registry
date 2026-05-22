---
name: api-security
description: Use when implementing API authentication, authorization, or security patterns. Covers OAuth 2.0, OIDC, JWT, API keys, rate limiting, and common API security vulnerabilities.
allowed-tools: Read, Glob, Grep
---

# API Security

Comprehensive guide to securing APIs - authentication, authorization, and protection against common vulnerabilities.

## When to Use This Skill

- Implementing API authentication (OAuth, OIDC, JWT)
- Designing authorization models for APIs
- Securing API endpoints
- Understanding API security vulnerabilities
- Implementing rate limiting and abuse prevention
- API key management

## Authentication Patterns

### OAuth 2.0 Flows

```text
OAuth 2.0 Grant Types:

1. Authorization Code (with PKCE)
   └── Best for: Web apps, mobile apps, SPAs
   └── Most secure for user authentication

   User ──► Auth Server ──► Authorization Code ──► Token

2. Client Credentials
   └── Best for: Service-to-service (M2M)
   └── No user context, server-to-server

   Service ──► Auth Server ──► Access Token

3. Device Authorization (Device Flow)
   └── Best for: Smart TVs, IoT, limited input devices
   └── User authorizes on separate device

   Device ──► Show Code ──► User enters on phone ──► Token

Deprecated (avoid):
- Implicit flow (security issues)
- Resource Owner Password Credentials (anti-pattern)
```

### Authorization Code Flow with PKCE

```text
┌──────────┐                              ┌───────────────┐
│  Client  │                              │  Auth Server  │
└────┬─────┘                              └───────┬───────┘
     │                                            │
     │  1. Generate code_verifier (random)        │
     │  2. Compute code_challenge = SHA256(verifier)
     │                                            │
     │──3. Authorization Request ───────────────►│
     │     (client_id, redirect_uri,             │
     │      code_challenge, challenge_method)     │
     │                                            │
     │◄──4. Authorization Code ──────────────────│
     │     (after user authentication/consent)    │
     │                                            │
     │──5. Token Request ───────────────────────►│
     │     (code, code_verifier)                 │
     │                                            │
     │◄──6. Access Token + Refresh Token ────────│
     │                                            │

Why PKCE?
- Prevents authorization code interception attacks
- Required for mobile apps and SPAs
- Recommended for all OAuth flows
```

### OpenID Connect (OIDC)

```text
OIDC = OAuth 2.0 + Identity Layer

OIDC adds:
├── ID Token (JWT with user claims)
├── UserInfo endpoint
├── Standardized claims (sub, name, email, etc.)
└── Discovery and metadata

Token Types:
┌─────────────────────────────────────────────────┐
│ ID Token                                        │
│ - User identity (who they are)                  │
│ - Contains claims about authentication          │
│ - For the CLIENT to consume                     │
├─────────────────────────────────────────────────┤
│ Access Token                                    │
│ - Authorization (what they can do)              │
│ - For the API/resource server to validate       │
│ - Should NOT be parsed by client                │
├─────────────────────────────────────────────────┤
│ Refresh Token                                   │
│ - Long-lived credential                         │
│ - Used to obtain new access tokens              │
│ - Store securely, never expose to browser       │
└─────────────────────────────────────────────────┘
```

### JWT (JSON Web Tokens)

```text
JWT Structure:

Header.Payload.Signature

Header (Base64URL):
{
  "alg": "RS256",     // Algorithm
  "typ": "JWT",       // Type
  "kid": "key-123"    // Key ID for rotation
}

Payload (Base64URL):
{
  "iss": "https://auth.example.com",  // Issuer
  "sub": "user-12345",                 // Subject
  "aud": "https://api.example.com",   // Audience
  "exp": 1735689600,                   // Expiration
  "iat": 1735686000,                   // Issued at
  "scope": "read write"                // Scopes/permissions
}

Signature:
RSASHA256(
  base64UrlEncode(header) + "." + base64UrlEncode(payload),
  privateKey
)
```

### JWT Validation

```text
JWT Validation Checklist:

1. Signature Verification
   □ Verify using correct public key (from JWKS)
   □ Reject if signature invalid

2. Claims Validation
   □ iss (issuer): Matches expected issuer
   □ aud (audience): Contains your API identifier
   □ exp (expiration): Token not expired
   □ iat (issued at): Not issued in the future
   □ nbf (not before): Token is active

3. Additional Checks
   □ Token not in revocation list (if applicable)
   □ Required scopes present
   □ Token type is access_token (not id_token)

Common Mistakes:
❌ Trusting "alg": "none"
❌ Not validating audience
❌ Using symmetric keys for public APIs
❌ Storing sensitive data in JWT payload
```

## Authorization Patterns

### Role-Based Access Control (RBAC)

```text
RBAC Model:

Users ──► Roles ──► Permissions

Example:
┌──────────────────────────────────────┐
│ Role: editor                         │
├──────────────────────────────────────┤
│ Permissions:                         │
│ - articles:read                      │
│ - articles:create                    │
│ - articles:update                    │
│ - comments:moderate                  │
└──────────────────────────────────────┘

API Implementation:
GET /articles        ← Requires: articles:read
POST /articles       ← Requires: articles:create
PUT /articles/{id}   ← Requires: articles:update
DELETE /articles/{id} ← Requires: articles:delete

Token includes:
{
  "scope": "articles:read articles:create articles:update"
}
```

### Attribute-Based Access Control (ABAC)

```text
ABAC Model:

Access = f(Subject, Resource, Action, Environment)

Subject Attributes:
- Role, department, clearance level
- User ID, group membership

Resource Attributes:
- Owner, classification, type
- Created date, sensitivity

Action Attributes:
- Read, write, delete, approve

Environment Attributes:
- Time of day, IP address, device type

Example Policy:
"Allow if user.department == resource.department
 AND user.role == 'manager'
 AND action == 'approve'
 AND environment.time.isBusinessHours"
```

### Resource-Based Authorization

```text
Check ownership/access at resource level:

GET /documents/{id}

Authorization Check:
1. Validate token (authentication)
2. Extract user from token
3. Query: Can this user access this document?
   - Is user the owner?
   - Does user have explicit permission?
   - Is document in a shared folder user can access?
   - Is user in a group with access?
4. Return 403 if not authorized

Implementation Pattern:
async function authorize(userId, resourceId, action) {
  // Check direct ownership
  if (await isOwner(userId, resourceId)) return true;

  // Check explicit permissions
  if (await hasPermission(userId, resourceId, action)) return true;

  // Check group permissions
  if (await hasGroupPermission(userId, resourceId, action)) return true;

  return false;
}
```

## API Key Security

### API Key Best Practices

```text
API Key Design:

Format: prefix_randomBytes
Example: sk_live_a1b2c3d4e5f6...

Prefix Benefits:
- sk_ = secret key (server-side only)
- pk_ = public key (can be exposed)
- test_ = test environment
- live_ = production

Security Requirements:
□ Sufficient entropy (32+ bytes random)
□ Secure storage (hashed, not plaintext)
□ Scoped permissions (not all-or-nothing)
□ Rotation capability
□ Audit logging
□ Rate limiting per key
```

### API Key vs OAuth

```text
When to Use Each:

API Keys:
✓ Service-to-service integration
✓ Simple use cases
✓ Developer-facing APIs
✓ Stateless, simple auth
✗ Not for user context
✗ Hard to revoke in real-time

OAuth 2.0:
✓ User-delegated access
✓ Fine-grained scopes
✓ Short-lived tokens
✓ Revocation support
✓ Standard compliance
✗ More complex to implement
✗ Requires authorization server
```

## Common Vulnerabilities

### OWASP API Security Top 10

```text
1. Broken Object Level Authorization (BOLA)
   Problem: Accessing other users' resources by changing IDs
   Fix: Always verify user has access to specific resource

   ❌ GET /users/123/orders (any user can change 123)
   ✓ Verify requesting user can access user 123's orders

2. Broken Authentication
   Problem: Weak authentication mechanisms
   Fix: Use proven auth protocols, implement properly

   ❌ Custom token schemes, weak passwords
   ✓ OAuth 2.0/OIDC with MFA

3. Broken Object Property Level Authorization
   Problem: Exposing sensitive properties
   Fix: Filter response based on authorization

   ❌ Returning user.password_hash in API response
   ✓ Explicitly select fields to return

4. Unrestricted Resource Consumption
   Problem: No limits on requests/data
   Fix: Rate limiting, pagination, resource quotas

   ❌ GET /users returns 10 million records
   ✓ Pagination, query limits, rate limiting

5. Broken Function Level Authorization
   Problem: Missing authorization on endpoints
   Fix: Verify authorization for every function

   ❌ Admin endpoints accessible to regular users
   ✓ Role checks on all endpoints

6. Unrestricted Access to Sensitive Business Flows
   Problem: Business logic abuse
   Fix: Detect and limit abuse patterns

   ❌ Unlimited password reset attempts
   ✓ Rate limit + CAPTCHA on sensitive flows

7. Server Side Request Forgery (SSRF)
   Problem: API fetches attacker-controlled URLs
   Fix: Validate and sanitize URLs, allowlist

   ❌ POST /fetch { "url": "http://internal-service" }
   ✓ Validate against allowlist, block internal IPs

8. Security Misconfiguration
   Problem: Default configs, exposed errors
   Fix: Harden configuration, minimal errors

   ❌ Detailed stack traces in production
   ✓ Generic error messages, proper headers

9. Improper Inventory Management
   Problem: Untracked API versions, shadow APIs
   Fix: API inventory, version management

   ❌ Old API versions still accessible
   ✓ Inventory, lifecycle management, deprecation

10. Unsafe Consumption of APIs
    Problem: Trusting third-party API responses
    Fix: Validate all external data

    ❌ Directly using third-party response data
    ✓ Validate, sanitize, treat as untrusted
```

### Input Validation

```text
Validation Layers:

1. Syntax Validation
   - Is it valid JSON/XML?
   - Are required fields present?
   - Are field types correct?

2. Semantic Validation
   - Is email format valid?
   - Is date in valid range?
   - Does ID reference exist?

3. Business Rule Validation
   - Is quantity within limits?
   - Is user authorized for this action?
   - Does the state transition make sense?

Validation Patterns:
- Allowlist over blocklist
- Validate on input AND output
- Fail safely with clear errors
- Log validation failures for monitoring
```

## Transport Security

### TLS Requirements

```text
TLS Configuration:

Minimum: TLS 1.2
Preferred: TLS 1.3

Required Settings:
□ Strong cipher suites only
□ Perfect forward secrecy (ECDHE)
□ Valid certificates from trusted CA
□ HSTS header enabled
□ Certificate transparency

Headers:
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

### Certificate Pinning

```text
Certificate Pinning (Mobile/Embedded):

Purpose: Prevent MITM attacks even with compromised CAs

Options:
1. Pin certificate
   - Requires update for certificate rotation

2. Pin public key
   - Survives certificate renewal
   - More flexible

3. Pin intermediate CA
   - Balance of security and flexibility

Considerations:
- Always have backup pins
- Plan for rotation
- Handle failures gracefully
- Consider using dynamic pinning
```

## Rate Limiting and Abuse Prevention

```text
Rate Limiting Strategies:

By Identity:
- Per API key
- Per user ID
- Per client ID

By Resource:
- Per endpoint
- Per operation type
- Per resource ID

Headers (draft standard):
RateLimit-Limit: 100
RateLimit-Remaining: 95
RateLimit-Reset: 1735689600
Retry-After: 60

Response Codes:
429 Too Many Requests - Rate limit exceeded
503 Service Unavailable - Server overloaded

Abuse Prevention:
□ Rate limiting
□ Request size limits
□ CAPTCHA for sensitive operations
□ Behavioral analysis
□ IP reputation
□ Anomaly detection
```

## Security Headers

```text
Essential API Security Headers:

# Prevent MIME type sniffing
X-Content-Type-Options: nosniff

# Control caching of sensitive data
Cache-Control: no-store, private

# CORS configuration (be restrictive)
Access-Control-Allow-Origin: https://trusted.example.com
Access-Control-Allow-Methods: GET, POST
Access-Control-Allow-Headers: Authorization, Content-Type

# Frame protection (if serving HTML)
X-Frame-Options: DENY

# Content Security Policy (if serving HTML)
Content-Security-Policy: default-src 'none'
```

## Related Skills

- `zero-trust-architecture` - Overall security architecture
- `mtls-service-mesh` - Service-to-service security
- `rate-limiting-patterns` - Detailed rate limiting strategies
- `secrets-management` - Managing API keys and secrets
