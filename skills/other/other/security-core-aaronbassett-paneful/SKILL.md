---
name: security-core
description: Comprehensive application security expertise covering authentication, authorization, OWASP Top 10, and security best practices. Use when (1) Implementing authentication (JWT, OAuth2, sessions, OAuth for CLI/TUI/desktop apps), (2) Adding authorization (RBAC, ABAC, RLS with Supabase/PostgreSQL), (3) Security auditing code or infrastructure, (4) Setting up security infrastructure (headers, CORS, CSP, rate limiting), (5) Managing secrets and credentials, (6) Preventing OWASP Top 10 vulnerabilities (injection, XSS, CSRF, etc.), (7) Reviewing code for security issues, (8) Configuring secure web applications in TypeScript, Python, or Rust. Automatically triggered when working with authentication/authorization systems, security reviews, or addressing security vulnerabilities.
---

# Security Core

Comprehensive application security guidance for TypeScript, Python, and Rust applications.

## Quick Start

### Common Security Tasks

**Setting up authentication:**
1. Generate JWT keys: `./scripts/generate_jwt_keys.sh RS256`
2. Consult [authentication.md](references/authentication.md) for implementation patterns
3. Use security templates from `assets/configs/`

**Implementing authorization:**
1. Review [authorization.md](references/authorization.md) for RBAC/ABAC/RLS patterns
2. For Supabase: See RLS section with multi-tenant examples
3. Implement permission checking at API and database layers

**Security auditing:**
1. Run: `./scripts/audit_security.sh`
2. Review [code-review.md](references/code-review.md) checklist
3. Check [owasp-top-10.md](references/owasp-top-10.md) for vulnerabilities

**Hardening application:**
1. Apply security headers from [security-headers.md](references/security-headers.md)
2. Implement rate limiting from [rate-limiting.md](references/rate-limiting.md)
3. Configure secrets management per [secrets-management.md](references/secrets-management.md)

## When to Use This Skill

### Authentication Scenarios
- Implementing login/signup flows
- Adding JWT or session-based authentication
- Integrating OAuth 2.0 providers
- **OAuth for CLI, TUI, or desktop applications** (Device Flow)
- Multi-factor authentication (TOTP, SMS/Email OTP)
- Password hashing and validation

### Authorization Scenarios
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- **Row Level Security (RLS) with Supabase/PostgreSQL**
- Multi-tenant data isolation
- Permission-based access control
- Resource ownership validation

### Security Auditing
- Code security reviews
- Dependency vulnerability scanning
- OWASP Top 10 compliance checks
- Secret detection in code
- Security configuration verification

### Infrastructure Security
- Security headers (CSP, HSTS, X-Frame-Options)
- CORS configuration
- Rate limiting implementation
- Secrets management
- API security hardening

## Core Resources

### Scripts (`scripts/`)

**`audit_security.sh`** - Security audit for TypeScript, Python, and Rust projects
- Runs dependency vulnerability scanners (npm audit, pip-audit, cargo-audit)
- Detects hardcoded secrets in code
- Checks for common security misconfigurations
- Usage: `./scripts/audit_security.sh [project-directory]`

**`generate_jwt_keys.sh`** - Generate secure JWT signing keys
- Supports HS256 (symmetric), RS256 (asymmetric), ES256 (elliptic curve)
- Automatically adds keys to .gitignore
- Provides usage examples
- Usage: `./scripts/generate_jwt_keys.sh [ALGORITHM] [OUTPUT_DIR]`

### Reference Documentation (`references/`)

**[authentication.md](references/authentication.md)** - Complete authentication guide
- JWT implementation (TypeScript, Python, Rust)
- Session-based authentication
- OAuth 2.0 Authorization Code Flow
- **OAuth Device Flow for CLI/TUI/desktop apps** ⭐
- Multi-factor authentication (TOTP, SMS)
- Password security and hashing
- Token storage best practices

**[authorization.md](references/authorization.md)** - Authorization patterns and implementations
- Role-Based Access Control (RBAC)
- Attribute-Based Access Control (ABAC)
- **Row Level Security (RLS) with Supabase/PostgreSQL** ⭐
- Multi-tenant RLS patterns
- Permission checking patterns
- Resource-based authorization
- Testing authorization logic

**[owasp-top-10.md](references/owasp-top-10.md)** - OWASP Top 10 prevention guide
- A01: Broken Access Control
- A02: Cryptographic Failures
- A03: Injection (SQL, NoSQL, Command)
- A04: Insecure Design
- A05: Security Misconfiguration
- A06: Vulnerable Components
- A07: Authentication Failures
- A08: Data Integrity Failures
- A09: Logging & Monitoring Failures
- A10: Server-Side Request Forgery (SSRF)

**[secrets-management.md](references/secrets-management.md)** - Secrets and credentials management
- Environment variables best practices
- Secret managers (AWS Secrets Manager, HashiCorp Vault)
- Secret rotation strategies
- CI/CD secrets handling
- Local development with .env files

**[security-headers.md](references/security-headers.md)** - HTTP security headers
- Content-Security-Policy (CSP)
- Strict-Transport-Security (HSTS)
- X-Frame-Options, X-Content-Type-Options
- CORS configuration
- Implementation examples for all frameworks

**[rate-limiting.md](references/rate-limiting.md)** - Rate limiting strategies
- Fixed window, sliding window, token bucket
- Implementation in TypeScript, Python, Rust
- Distributed rate limiting with Redis
- Per-user and per-IP limiting
- Rate limit headers and responses

**[code-review.md](references/code-review.md)** - Security code review checklist
- Authentication & authorization checks
- Input validation & sanitization
- Data protection and encryption
- Security headers & configuration
- Session management
- API security
- Common vulnerabilities (XSS, CSRF, SQL injection)

### Configuration Templates (`assets/configs/`)

Ready-to-use security middleware for all supported languages:

**TypeScript:** `assets/configs/typescript/security-config.ts`
- Express + Helmet configuration
- CORS setup
- Rate limiting
- Security headers

**Python:** `assets/configs/python/security_middleware.py`
- FastAPI middleware
- Security headers
- CORS
- Rate limiting with slowapi

**Rust:** `assets/configs/rust/security_middleware.rs`
- Axum middleware
- tower-http CORS layer
- Security headers

## Decision Guides

### Choosing Authentication Method

| Method | Use When | Complexity | Best For |
|--------|----------|------------|----------|
| JWT | Stateless APIs, microservices | Medium | SPAs, mobile apps, APIs |
| Sessions | Traditional web apps | Low | Server-rendered apps |
| OAuth 2.0 | Third-party auth, SSO | High | Delegated authentication |
| API Keys | Service-to-service | Low | Internal services |

See [authentication.md](references/authentication.md) for detailed implementation patterns.

### Choosing Authorization Model

| Model | Use When | Complexity | Best For |
|-------|----------|------------|----------|
| RBAC | Simple role hierarchies | Low | Standard web apps |
| ABAC | Complex, dynamic policies | High | Enterprise apps |
| RLS | Multi-tenant with data isolation | Medium | SaaS applications |
| Permissions | Fine-grained control | Medium | Admin panels, APIs |

See [authorization.md](references/authorization.md) for implementation patterns and RLS examples.

### OAuth for CLI/TUI/Desktop

For applications without traditional browser redirects:

**Device Authorization Flow (OAuth 2.0):**
1. App requests device code
2. User opens browser and enters code
3. App polls for token
4. Token granted after user approval

Full implementation examples in [authentication.md - OAuth for CLI, TUI, and Desktop Apps](references/authentication.md#oauth-for-cli-tui-and-desktop-apps).

## Common Workflows

### 1. Implementing JWT Authentication

```bash
# Generate keys
./scripts/generate_jwt_keys.sh RS256 ./keys

# Review implementation patterns
# See references/authentication.md#jwt-authentication
```

Then implement using examples for your language (TypeScript/Python/Rust).

### 2. Adding Row Level Security (Supabase)

```bash
# Review RLS patterns
# See references/authorization.md#row-level-security-rls
```

Implement RLS policies for multi-tenant isolation:
- Enable RLS on tables
- Create policies for SELECT, INSERT, UPDATE, DELETE
- Use helper functions for complex rules
- Test with different user contexts

### 3. Security Audit Workflow

```bash
# Run automated audit
./scripts/audit_security.sh

# Manual review
# 1. Check references/code-review.md checklist
# 2. Review references/owasp-top-10.md for vulnerabilities
# 3. Verify security headers with references/security-headers.md
# 4. Test rate limiting per references/rate-limiting.md
```

### 4. Hardening New Application

1. **Apply security templates:**
   - Copy appropriate config from `assets/configs/[language]/`
   - Configure CORS for your domains
   - Set up rate limiting

2. **Implement authentication:**
   - Choose method from [authentication.md](references/authentication.md)
   - Generate secure keys
   - Configure token expiration

3. **Add authorization:**
   - Choose model from [authorization.md](references/authorization.md)
   - Implement permission checks
   - Enable RLS if multi-tenant

4. **Configure security headers:**
   - Follow [security-headers.md](references/security-headers.md)
   - Test with online tools

5. **Set up secrets management:**
   - Follow [secrets-management.md](references/secrets-management.md)
   - Use environment variables or secret manager

6. **Review OWASP Top 10:**
   - Check [owasp-top-10.md](references/owasp-top-10.md)
   - Ensure all risks are mitigated

## Language-Specific Guidance

### TypeScript/Node.js
- Use Helmet for security headers
- Validate inputs with Zod
- Use prepared statements for SQL
- Hash passwords with bcrypt
- See config: `assets/configs/typescript/security-config.ts`

### Python/FastAPI
- Use Pydantic for validation
- Parameterized queries only
- Hash passwords with bcrypt
- Security middleware in startup
- See config: `assets/configs/python/security_middleware.py`

### Rust
- Compiler prevents many issues
- Validate at boundaries
- Use sqlx for type-safe SQL
- Hash passwords with argon2
- See config: `assets/configs/rust/security_middleware.rs`

## Best Practices

1. **Defense in Depth** - Multiple security layers
2. **Least Privilege** - Grant minimum necessary permissions
3. **Fail Securely** - Default to deny
4. **Keep Secrets Secret** - Never commit credentials
5. **Validate Everything** - All inputs at boundaries
6. **Use Strong Crypto** - Modern algorithms only
7. **Log Security Events** - Authentication, authorization failures
8. **Update Dependencies** - Regular security patches
9. **Rate Limit** - Protect against abuse
10. **Test Security** - Automated security tests

## Testing Security

Write tests for security concerns:

```typescript
// Authentication tests
it('should reject invalid credentials');
it('should rate limit login attempts');
it('should require MFA when enabled');

// Authorization tests
it('should deny unauthorized access');
it('should allow access for correct role');
it('should enforce resource ownership');

// Input validation tests
it('should prevent SQL injection');
it('should sanitize HTML input');
it('should validate file uploads');
```

See [code-review.md](references/code-review.md) for complete testing checklist.

## Security Resources

**Primary references in this skill:**
- [authentication.md](references/authentication.md) - Auth patterns and OAuth for CLI/desktop
- [authorization.md](references/authorization.md) - RBAC, ABAC, and RLS
- [owasp-top-10.md](references/owasp-top-10.md) - Top web vulnerabilities
- [secrets-management.md](references/secrets-management.md) - Credential handling
- [security-headers.md](references/security-headers.md) - HTTP security headers
- [rate-limiting.md](references/rate-limiting.md) - API protection
- [code-review.md](references/code-review.md) - Security review checklist

**External resources:**
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
- [Security Headers](https://securityheaders.com/)
- [Mozilla Web Security Guidelines](https://infosec.mozilla.org/guidelines/web_security)

## Getting Started

**For a new secure application:**
1. Review [Best Practices](#best-practices) section
2. Apply security templates from `assets/configs/`
3. Implement authentication from [authentication.md](references/authentication.md)
4. Add authorization from [authorization.md](references/authorization.md)
5. Configure security headers from [security-headers.md](references/security-headers.md)
6. Run `./scripts/audit_security.sh` to verify

**For security review:**
1. Run `./scripts/audit_security.sh`
2. Follow [code-review.md](references/code-review.md) checklist
3. Check [owasp-top-10.md](references/owasp-top-10.md) for vulnerabilities

**For specific security concern:**
- Authentication issue → [authentication.md](references/authentication.md)
- Authorization issue → [authorization.md](references/authorization.md)
- OWASP vulnerability → [owasp-top-10.md](references/owasp-top-10.md)
- Configuration issue → [security-headers.md](references/security-headers.md) or [rate-limiting.md](references/rate-limiting.md)
- Secrets issue → [secrets-management.md](references/secrets-management.md)
