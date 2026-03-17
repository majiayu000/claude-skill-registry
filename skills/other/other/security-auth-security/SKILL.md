---
name: security-auth-security
description: Authentication, authorization, secrets management, XSS prevention, CSRF protection, Dependabot configuration, vulnerability scanning, DOMPurify sanitization, CSP headers, CODEOWNERS, HttpOnly cookies
---

# Security Patterns

> **Quick Guide:** Managing secrets? Use .env.local (gitignored), CI secrets (GitHub/Vercel), rotate quarterly. Dependency security? Enable Dependabot, audit weekly, patch critical vulns within 24hrs. XSS prevention? React escapes by default - never use dangerouslySetInnerHTML with user input. Sanitize with DOMPurify if needed. Set CSP headers. CODEOWNERS? Require security team review for auth/, .env.example, workflows.

**Detailed Resources:**

- For code examples, see [examples/core.md](examples/core.md) (essential patterns)
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

**Additional Examples:**

- [examples/xss-prevention.md](examples/xss-prevention.md) - XSS protection, DOMPurify, CSP headers
- [examples/dependency-security.md](examples/dependency-security.md) - Dependabot, CI security checks
- [examples/access-control.md](examples/access-control.md) - CODEOWNERS, rate limiting, branch protection

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST NEVER commit secrets to the repository - use .env.local and CI secrets only)**

**(You MUST sanitize ALL user input before rendering HTML - use DOMPurify with dangerouslySetInnerHTML)**

**(You MUST patch critical/high vulnerabilities within 24 hours - use Dependabot for automated scanning)**

**(You MUST use HttpOnly cookies for authentication tokens - NEVER localStorage or sessionStorage)**

**(You MUST configure CODEOWNERS for security-sensitive files - require security team approval)**

</critical_requirements>

---

**Auto-detection:** security, secrets management, XSS prevention, CSRF protection, Dependabot, vulnerability scanning, authentication, DOMPurify, CSP headers, CODEOWNERS, HttpOnly cookies

**When to use:**

- Managing secrets securely (never commit, use .env.local and CI secrets)
- Setting up Dependabot for automated vulnerability scanning
- Preventing XSS attacks (React escaping, DOMPurify, CSP headers)
- Configuring CODEOWNERS for security-sensitive code
- Implementing secure authentication and token storage

**When NOT to use:**

- For general code quality (use reviewing skill instead)
- For performance optimization (use performance skills)
- For CI/CD pipeline setup (use ci-cd skill - security patterns here are for code, not pipelines)
- When security review would delay critical hotfixes (document for follow-up)

**Key patterns covered:**

- Never commit secrets (.gitignore, CI secrets, rotation policies quarterly)
- Automated dependency scanning with Dependabot (critical within 24h)
- XSS prevention (React's built-in escaping, DOMPurify for HTML, CSP headers)
- CSRF protection with tokens and SameSite cookies
- CODEOWNERS for security-sensitive areas (.env.example, auth code, workflows)
- Secure token storage (HttpOnly cookies, in-memory access tokens)

---

<philosophy>

## Philosophy

Security is not a feature - it's a foundation. Every line of code must be written with security in mind. Defense in depth means multiple layers of protection, so if one fails, others catch the attack.

**When to use security patterns:**

- Always - security is not optional
- When handling user input (sanitize and validate)
- When managing secrets (environment variables, rotation)
- When storing authentication tokens (HttpOnly cookies)
- When setting up CI/CD (vulnerability scanning, CODEOWNERS)

**When NOT to compromise:**

- Never skip HTTPS in production
- Never trust client-side validation alone
- Never commit secrets to repository
- Never use localStorage for sensitive tokens
- Never bypass security reviews for critical code

**Core principles:**

- **Least privilege**: Grant minimum necessary access
- **Defense in depth**: Multiple layers of security
- **Fail securely**: Default to deny, not allow
- **Don't trust user input**: Always validate and sanitize
- **Assume breach**: Plan for when (not if) attacks happen

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Secret Management

Never commit secrets to the repository. Use environment variables in .env.local (gitignored) for development, and CI/CD secret managers for production. Rotate secrets quarterly or on team member departure.

#### What Are Secrets

Secrets include: API keys, tokens, passwords, database credentials, private keys, certificates, OAuth client secrets, encryption keys, JWT secrets.

#### Where to Store Secrets

**Development:**

- `.env.local` (gitignored)
- Per-developer local overrides
- Never committed to repository

**CI/CD:**

- GitHub Secrets
- Vercel Environment Variables
- GitLab CI/CD Variables
- Other platform secret managers

**Production:**

- Environment variables (injected by platform)
- Secret management services (AWS Secrets Manager, HashiCorp Vault)
- Never hardcoded in code

#### Rotation Policies

**Note:** NIST SP 800-63-4 (2025) recommends against mandatory periodic password rotation for users. Instead, use event-based rotation (on compromise, team member departure, or security incident). Periodic rotation is still recommended for service accounts and privileged access.

| Secret Type                  | Rotation Frequency                      |
| ---------------------------- | --------------------------------------- |
| Service account credentials  | 90 days (quarterly)                     |
| API keys                     | 365 days (annually) or on compromise    |
| User passwords               | On compromise only (NIST 2025 guidance) |
| Privileged account passwords | 90 days (quarterly)                     |
| Certificates                 | 30 days warning before expiry           |
| All secrets                  | Immediately on team member departure    |

**See [examples/core.md](examples/core.md#pattern-1-secret-management) for code examples.**

---

### Pattern 2: Dependency Security

Enable automated vulnerability scanning with Dependabot to catch security issues in dependencies. Patch critical vulnerabilities within 24 hours, high within 1 week, medium within 1 month.

#### Update Policies

**Security updates:**

- **Critical vulnerabilities** - Immediate (within 24 hours)
- **High vulnerabilities** - Within 1 week
- **Medium vulnerabilities** - Within 1 month
- **Low vulnerabilities** - Next regular update cycle

**Regular updates:**

- **Patch updates** (1.2.3 -> 1.2.4) - Auto-merge if tests pass
- **Minor updates** (1.2.0 -> 1.3.0) - Review changes, test, merge
- **Major updates** (1.0.0 -> 2.0.0) - Plan migration, test thoroughly

**See [examples/dependency-security.md](examples/dependency-security.md) for Dependabot configuration and CI security check scripts.**

---

### Pattern 3: XSS Prevention

React automatically escapes user input by default. Never use `dangerouslySetInnerHTML` with user input unless sanitized with DOMPurify. Configure Content Security Policy (CSP) headers to block unauthorized scripts.

#### React's Built-in Protection

React escapes all text content automatically. Only `dangerouslySetInnerHTML` bypasses this protection.

#### DOMPurify Sanitization

When HTML rendering is required, use DOMPurify with a whitelist of allowed tags and attributes.

#### Content Security Policy

Configure CSP headers to prevent unauthorized script execution even if XSS occurs.

**See [examples/xss-prevention.md](examples/xss-prevention.md) for React, DOMPurify, and CSP code examples.**

---

### OWASP Top 10 2025 Coverage

This skill addresses the following OWASP Top 10:2025 categories:

| OWASP Category                                | Coverage                                          |
| --------------------------------------------- | ------------------------------------------------- |
| A01: Broken Access Control                    | CODEOWNERS, branch protection, rate limiting      |
| A02: Security Misconfiguration                | CSP headers, security headers, Dependabot         |
| A03: Software Supply Chain Failures (NEW)     | Dependabot, CI security audits, dependency review |
| A04: Cryptographic Failures                   | HttpOnly/Secure cookies, HTTPS enforcement        |
| A05: Injection (includes XSS)                 | DOMPurify, React auto-escaping, CSP               |
| A07: Identification & Auth Failures           | HttpOnly cookies, session management              |
| A09: Security Logging & Alerting              | (See observability skill)                         |
| A10: Mishandling Exceptional Conditions (NEW) | Fail securely principle, error handling           |

</patterns>

---

<integration>

## Integration Guide

**Works with:**

- **React**: Built-in XSS protection via auto-escaping, use DOMPurify for rich HTML
- **Next.js**: Configure security headers in middleware or next.config.js
- **GitHub**: Dependabot for automated vulnerability scanning, CODEOWNERS for code review
- **Vercel/CI**: Store secrets in environment variables, never commit
- **axios**: Interceptors for automatic CSRF token injection
- **DOMPurify**: Sanitize user HTML before rendering with dangerouslySetInnerHTML

**Security layers:**

- **Secrets**: .env.local (dev) -> CI secrets (GitHub/Vercel) -> Environment variables (production)
- **XSS**: React auto-escaping -> DOMPurify sanitization -> CSP headers
- **CSRF**: Tokens -> SameSite cookies -> Server-side validation
- **Dependencies**: Dependabot -> CI security audit -> Manual review

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST NEVER commit secrets to the repository - use .env.local and CI secrets only)**

**(You MUST sanitize ALL user input before rendering HTML - use DOMPurify with dangerouslySetInnerHTML)**

**(You MUST patch critical/high vulnerabilities within 24 hours - use Dependabot for automated scanning)**

**(You MUST use HttpOnly cookies for authentication tokens - NEVER localStorage or sessionStorage)**

**(You MUST configure CODEOWNERS for security-sensitive files - require security team approval)**

**Failure to follow these rules will create security vulnerabilities enabling XSS attacks, token theft, CSRF attacks, and data breaches.**

</critical_reminders>
