---
name: typescript-security-review
description: Provides security review capability for TypeScript/Node.js applications, validates code against XSS, injection, CSRF, JWT/OAuth2 flaws, dependency CVEs, and secrets exposure. Use when performing security audits, before deployment, reviewing authentication/authorization implementations, or ensuring OWASP compliance for Express, NestJS, and Next.js. Triggers on "security review", "check for security issues", "TypeScript security audit".
allowed-tools: Read, Edit, Grep, Glob, Bash
---

# TypeScript Security Review

## Overview

Security review for TypeScript/Node.js applications. Evaluates code against OWASP Top 10, framework-specific patterns, and production-readiness criteria. Findings are classified by severity (Critical, High, Medium, Low) with remediation examples. Delegates to the `typescript-security-expert` agent for deep analysis.

## When to Use

- Performing security audits on TypeScript/Node.js codebases
- Reviewing authentication and authorization implementations (JWT, OAuth2, Passport.js)
- Checking for common vulnerabilities (XSS, injection, CSRF, path traversal)
- Validating input validation and sanitization logic
- Reviewing dependency security (npm audit, known CVEs)
- Checking secrets management and environment variable handling
- Assessing API security (rate limiting, CORS, security headers)
- Reviewing Express, NestJS, or Next.js security configurations
- Before deploying to production or after significant code changes
- Compliance checks (GDPR, HIPAA, SOC2 data handling requirements)

## Instructions

1. **Identify Scope**: Determine which files and modules are under review. Prioritize authentication, authorization, data handling, API endpoints, and configuration files. Use `grep` to find security-sensitive patterns (`eval`, `exec`, `innerHTML`, password handling, JWT operations).

   **Checkpoint**: Verify at least 3 security-sensitive files/modules identified before proceeding.

2. **Check Authentication & Authorization**: Review JWT implementation (signing algorithm, expiration, refresh tokens), OAuth2/OIDC integration, session management, password hashing (bcrypt/argon2), and multi-factor authentication. Verify protected routes enforce authentication.

   **Checkpoint**: Use `grep` to confirm all route handlers have auth guards or middleware applied.

3. **Scan for Injection Vulnerabilities**: Check for SQL/NoSQL injection in database queries, command injection in `exec`/`spawn`, template injection, and LDAP injection. Verify parameterized queries and input validation.

   **Checkpoint**: Use `grep` to confirm all database queries use parameterization — no string concatenation with user input.

4. **Review Input Validation**: Check API inputs validated with Zod, Joi, or class-validator. Verify schema completeness — proper type constraints, length limits, format validation. Check for validation bypass paths.

   **Checkpoint**: Verify all public API endpoints have corresponding validation schemas.

5. **Assess XSS Prevention**: Review React components for `dangerouslySetInnerHTML` usage, check Content Security Policy headers, verify HTML sanitization for user-generated content. See `references/xss-prevention.md` for detailed patterns.

   **Checkpoint**: Use `grep` to confirm any `dangerouslySetInnerHTML` usage has sanitization via DOMPurify or equivalent.

6. **Check Secrets Management**: Scan for hardcoded credentials, API keys, secrets in source code. Verify `.env` files are gitignored, secrets accessed through proper management services.

   **Checkpoint**: Run `grep -r "password\|secret\|api.*key\|token" --include="*.ts"` to identify potential secrets in code.

7. **Review Dependency Security**: Run `npm audit` or check `package-lock.json` for known vulnerabilities. Identify outdated dependencies with CVEs. Check for unnecessary dependencies.

   **Checkpoint**: Verify `npm audit` results are reviewed and critical vulnerabilities addressed.

8. **Evaluate Security Headers & Configuration**: Check helmet.js or manual security header configuration. Review CORS policy, rate limiting, HTTPS enforcement, cookie security flags (HttpOnly, Secure, SameSite), and CSP. See `references/security-headers.md` for configuration examples.

   **Checkpoint**: Use `grep` to confirm helmet or equivalent security headers are applied globally.

9. **Produce Security Report**: Generate structured report with severity-classified findings, remediation guidance with code examples, and security posture summary.

   **Feedback Loop**: If Critical or High vulnerabilities found, re-scan related modules for similar patterns before finalizing. Use `grep` to identify if the same vulnerability pattern exists elsewhere.

## Examples

### JWT Security Review

```typescript
// ❌ Critical: Weak JWT configuration
import jwt from 'jsonwebtoken';

const SECRET = 'mysecret123'; // Hardcoded weak secret

function generateToken(user: User) {
  return jwt.sign({ id: user.id, role: user.role }, SECRET);
  // Missing expiration, weak secret, no algorithm specification
}

// ✅ Secure: Proper JWT configuration
import jwt from 'jsonwebtoken';

const JWT_SECRET = process.env.JWT_SECRET;
if (!JWT_SECRET || JWT_SECRET.length < 32) {
  throw new Error('JWT_SECRET must be set and at least 32 characters');
}

function generateToken(user: User): string {
  return jwt.sign(
    { sub: user.id }, // Minimal claims, no sensitive data
    JWT_SECRET,
    {
      algorithm: 'HS256',
      expiresIn: '15m',
      issuer: 'my-app',
      audience: 'my-app-client',
    }
  );
}

function verifyToken(token: string): JwtPayload {
  return jwt.verify(token, JWT_SECRET, {
    algorithms: ['HS256'], // Restrict accepted algorithms
    issuer: 'my-app',
    audience: 'my-app-client',
  }) as JwtPayload;
}
```

### SQL Injection Prevention

```typescript
// ❌ Critical: SQL injection vulnerability
async function findUser(email: string) {
  const result = await db.query(
    `SELECT * FROM users WHERE email = '${email}'`
  );
  return result.rows[0];
}

// ✅ Secure: Parameterized query
async function findUser(email: string) {
  const result = await db.query(
    'SELECT id, name, email FROM users WHERE email = $1',
    [email]
  );
  return result.rows[0];
}

// ✅ Secure: ORM with type-safe queries (Drizzle example)
async function findUser(email: string) {
  return db.select({
    id: users.id,
    name: users.name,
    email: users.email,
  })
  .from(users)
  .where(eq(users.email, email))
  .limit(1);
}
```

See `references/xss-prevention.md` for XSS patterns and `references/security-headers.md` for security headers configuration.

## Review Output Format

Structure all security review findings as follows:

### 1. Security Posture Summary
Overall security assessment score (1-10) with key observations and risk level.

### 2. Critical Vulnerabilities (Immediate Action)
Issues that can be exploited to compromise the system, steal data, or cause unauthorized access.

### 3. High Priority (Address Within 30 Days)
Security misconfigurations, missing protections, or vulnerabilities requiring near-term remediation.

### 4. Medium Priority (Address Within 90 Days)
Issues that reduce security posture but have mitigating factors or limited exploitability.

### 5. Low Priority (Next Cycle)
Security improvements, hardening recommendations, and defense-in-depth enhancements.

### 6. Positive Security Observations
Well-implemented security patterns and practices to acknowledge.

### 7. Remediation Roadmap
Prioritized action items with code examples for the most critical fixes.

## Best Practices

- Validate all inputs at the API boundary — never trust client-side validation alone
- Use parameterized queries or ORMs — never concatenate user input into queries
- Store secrets in environment variables or secret managers — never in source code
- Apply the principle of least privilege for database accounts, API keys, and IAM roles
- Enable security headers (helmet.js) and restrict CORS to known origins
- Implement rate limiting on all public-facing endpoints
- Hash passwords with bcrypt or argon2 — never use MD5/SHA for passwords
- Set cookie flags: `HttpOnly`, `Secure`, `SameSite=Strict`
- Use `npm audit` in CI pipelines to catch dependency vulnerabilities
- Log security events (failed logins, permission denials) without logging sensitive data

## Constraints and Warnings

- Security review is not a substitute for professional penetration testing
- Focus on code-level vulnerabilities — infrastructure security is out of scope
- Respect the project's framework — provide framework-specific remediation guidance
- Do not log, print, or expose discovered secrets — report their location only
- Dependency vulnerabilities should be assessed for actual exploitability, not just presence
- Security recommendations must be practical — consider implementation effort vs risk reduction

## References

See the `references/` directory for detailed security documentation:
- `references/owasp-typescript.md` — OWASP Top 10 mapped to TypeScript/Node.js patterns
- `references/common-vulnerabilities.md` — Common vulnerability patterns and remediation
- `references/dependency-security.md` — Dependency scanning and supply chain security
- `references/xss-prevention.md` — XSS prevention patterns for React and server-side
- `references/security-headers.md` — Security headers and CORS configuration examples
- `references/input-validation.md` — Input validation patterns with Zod and class-validator
