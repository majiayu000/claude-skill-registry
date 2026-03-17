---
name: NestJS Security
description: Authentication, RBAC, and Hardening standards.
metadata:
  labels: [nestjs, security, auth, jwt]
  triggers:
    files: ['**/*.guard.ts', '**/*.strategy.ts', '**/auth/**']
    keywords: [Passport, JWT, AuthGuard, CSRF, Helmet]
---

# NestJS Security Standards

## **Priority: P0 (CRITICAL)**

## Authentication (JWT)

- **Strategy**: Use `@nestjs/passport` with `passport-jwt`.
- **Algorithm**: Enforce `RS256` (preferred) or `HS256`. **Reject `none`**.
- **Claims**: Validate `iss` and `aud`.
- **Tokens**: Short access (15m), Long httponly refresh (7d).
- **MFA**: Require 2FA for admin panels.

## Authorization (RBAC)

- **Deny by default**: Bind `AuthGuard` globally (APP_GUARD).
- **Bypass**: Create `@Public()` decorator for open routes.
- **Roles**: Use `Reflector.getAllAndOverride` for Method/Class merge.

## Cryptography

- **Hashing**: Use **Argon2id**, not Bcrypt. See [implementation](references/implementation.md).
- **Encryption**: Use **AES-256-GCM** with KMS rotation. See [implementation](references/implementation.md).

## Hardening

- **Helmet**: Mandatory. Enable HSTS, CSP.
- **CORS**: Explicit origins only. No `*`.
- **Throttling**: Use Redis-backed `@nestjs/throttler` in production.
- **CSRF**: Required for cookie-based auth. See [implementation](references/implementation.md).

## Data Protection

- **Sanitization**: Use `ClassSerializerInterceptor` + `@Exclude()`.
- **Validation**: `ValidationPipe({ whitelist: true })` to prevent mass assignment.
- **Audit**: Log mutations (Who, What, When). See [implementation](references/implementation.md).

## Secrets Management

- **CI/CD**: Run `npm audit --prod` in pipelines.
- **Runtime**: Inject via vault (AWS Secrets Manager / HashiCorp Vault), not `.env`.

## Anti-Patterns

- **No Shadow APIs**: Audit routes regularly; disable `/docs` in production.
- **No SSRF**: Allowlist domains for all outgoing HTTP requests.
- **No SQLi**: Use ORM; avoid raw `query()` with string concatenation.
- **No XSS**: Sanitize HTML input with `dompurify`.

## Related Topics

common/security-standards | architecture | database
