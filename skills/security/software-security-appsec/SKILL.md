---
name: software-security-appsec
description: Modern application security patterns aligned with OWASP Top 10 (2021) and OWASP Top 10:2025 Release Candidate, OWASP API Security Top 10 (2023), NIST SSDF, zero trust, supply chain security, authentication, authorization, input validation, and cryptography.
---

# Software Security & AppSec — Quick Reference

Production-grade security patterns for building secure applications in Dec 2025. Covers OWASP Top 10 (stable 2021) https://owasp.org/www-project-top-ten/ and OWASP Top 10:2025 Release Candidate (preview) https://owasp.org/Top10/2025/, plus OWASP API Security Top 10 (2023) https://owasp.org/API-Security/ and secure SDLC baselines (NIST SSDF) https://csrc.nist.gov/publications/detail/sp/800-218/final.

---

## When to Use This Skill

Activate this skill when:

- Implementing authentication or authorization systems
- Handling user input that could lead to injection attacks (SQL, XSS, command injection)
- Designing secure APIs or web applications
- Working with cryptographic operations or sensitive data storage
- Conducting security reviews, threat modeling, or vulnerability assessments
- Responding to security incidents or compliance audit requirements
- Building systems that must comply with OWASP, NIST, PCI DSS, GDPR, HIPAA, or SOC 2
- Integrating third-party dependencies (supply chain security review)
- Implementing zero trust architecture or modern cloud-native security patterns
- Establishing or improving secure SDLC gates (threat modeling, SAST/DAST, dependency scanning)

---

## Quick Reference Table

| Security Task | Tool/Pattern | Implementation | When to Use |
|---------------|--------------|----------------|-------------|
| Password Storage | bcrypt/Argon2 | `bcrypt.hash(password, 12)` | Always hash passwords (never store plaintext) |
| Input Validation | Allowlist regex | `/^[a-zA-Z0-9_]{3,20}$/` | All user input (SQL, XSS, command injection prevention) |
| SQL Queries | Parameterized queries | `db.execute(query, [userId])` | All database operations (prevent SQL injection) |
| API Authentication | JWT + OAuth2 | `jwt.sign(payload, secret, options)` | Stateless auth with short-lived tokens (15-30 min) |
| Data Encryption | AES-256-GCM | `crypto.createCipheriv('aes-256-gcm')` | Sensitive data at rest (PII, financial, health) |
| HTTPS/TLS | TLS 1.3 | Force HTTPS redirects | All production traffic (data in transit) |
| Access Control | RBAC/ABAC | `requireRole('admin', 'moderator')` | Resource authorization (APIs, admin panels) |
| Rate Limiting | express-rate-limit | `limiter({ windowMs: 15min, max: 100 })` | Public APIs, auth endpoints (DoS prevention) |

## Decision Tree: Security Implementation

```text
Security requirement: [Feature Type]
    ├─ User Authentication?
    │   ├─ Session-based? → Cookie sessions + CSRF tokens
    │   ├─ Token-based? → JWT with refresh tokens (resources/authentication-authorization.md)
    │   └─ Third-party? → OAuth2/OIDC integration
    │
    ├─ User Input?
    │   ├─ Database query? → Parameterized queries (NEVER string concatenation)
    │   ├─ HTML output? → DOMPurify sanitization + CSP headers
    │   ├─ File upload? → Content validation, size limits, virus scanning
    │   └─ API parameters? → Allowlist validation (resources/input-validation.md)
    │
    ├─ Sensitive Data?
    │   ├─ Passwords? → bcrypt/Argon2 (cost factor 12+)
    │   ├─ PII/financial? → AES-256-GCM encryption + key rotation
    │   ├─ API keys/tokens? → Environment variables + secrets manager
    │   └─ In transit? → TLS 1.3 only
    │
    ├─ Access Control?
    │   ├─ Simple roles? → RBAC (templates/web-application/template-authorization.md)
    │   ├─ Complex rules? → ABAC with policy engine
    │   └─ Relationship-based? → ReBAC (owner, collaborator, viewer)
    │
    └─ API Security?
        ├─ Public API? → Rate limiting + API keys
        ├─ CORS needed? → Strict origin allowlist (never *)
        └─ Headers? → Helmet.js (CSP, HSTS, X-Frame-Options)
```

---

## Incident Response Patterns (Dec 2025)

### Security Incident Playbook

| Phase | Actions |
|-------|---------|
| **Detect** | Alert fires, user report, automated scan |
| **Contain** | Isolate affected systems, revoke compromised credentials |
| **Investigate** | Collect logs, determine scope, identify root cause |
| **Remediate** | Patch vulnerability, rotate secrets, update defenses |
| **Recover** | Restore services, verify fixes, update monitoring |
| **Learn** | Post-mortem, update playbooks, share lessons |

### Security Logging Requirements

| What to Log | Format | Retention |
|-------------|--------|-----------|
| Authentication events | JSON with correlation ID | 90 days minimum |
| Authorization failures | JSON with user context | 90 days minimum |
| Data access (sensitive) | JSON with resource ID | 1 year minimum |
| Security scan results | SARIF format | 1 year minimum |

**Do:**

- Include correlation IDs across services
- Log to SIEM (Splunk, Datadog, ELK)
- Mask PII in logs

**Avoid:**

- Logging passwords, tokens, or keys
- Unstructured log formats
- Missing timestamps or context

---

### Optional: AI/Automation Extensions

> **Note**: Security considerations for AI systems. Skip if not building AI features.

#### LLM Security Patterns

| Threat | Mitigation |
|--------|------------|
| Prompt injection | Input validation, output filtering, sandboxed execution |
| Data exfiltration | Output scanning, PII detection |
| Model theft | API rate limiting, watermarking |
| Jailbreaking | Constitutional AI, guardrails |

#### AI-Assisted Security Tools

| Tool | Use Case |
|------|----------|
| Semgrep | Static analysis with AI rules |
| Snyk Code | AI-powered vulnerability detection |
| GitHub CodeQL | Semantic code analysis |

---

## .NET/EF Core Crypto Integration Security

For C#/.NET crypto/fintech services using Entity Framework Core, see:

- [resources/dotnet-efcore-crypto-security.md](resources/dotnet-efcore-crypto-security.md) — Security rules and C# patterns

**Key rules summary:**

- No secrets in code — use configuration/environment variables
- No sensitive data in logs (tokens, keys, PII)
- Use `decimal` for financial values, never `double`/`float`
- EF Core or parameterized queries only — no dynamic SQL
- Generic error messages to users, detailed logging server-side

## Navigation

### Core Resources (Updated 2024-2025)

#### 2025 Updates & Modern Architecture

- [resources/supply-chain-security.md](resources/supply-chain-security.md) — Dependency, build, and artifact integrity (SLSA, provenance, signing)
- [resources/zero-trust-architecture.md](resources/zero-trust-architecture.md) — NIST SP 800-207, service identity, policy-based access
- [resources/owasp-top-10.md](resources/owasp-top-10.md) — OWASP Top 10 mapping (2021 stable + 2025 RC preview)
- [resources/advanced-xss-techniques.md](resources/advanced-xss-techniques.md) — 2024-2025 XSS: mutation XSS, polyglots, SVG attacks, context-aware encoding

#### Foundation Security Patterns

- [resources/secure-design-principles.md](resources/secure-design-principles.md) — Defense in depth, least privilege, secure defaults
- [resources/authentication-authorization.md](resources/authentication-authorization.md) — AuthN/AuthZ flows, OAuth 2.1, JWT best practices, RBAC/ABAC
- [resources/input-validation.md](resources/input-validation.md) — Allowlist validation, SQL injection, XSS, CSRF prevention, file upload security
- [resources/cryptography-standards.md](resources/cryptography-standards.md) — AES-256-GCM, Argon2, TLS 1.3, key management
- [resources/common-vulnerabilities.md](resources/common-vulnerabilities.md) — Path traversal, command injection, deserialization, SSRF

#### External References

- [data/sources.json](data/sources.json) — 70+ curated security resources (OWASP 2025, supply chain, zero trust, API security, compliance)
- Shared checklists: [../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md](../software-clean-code-standard/templates/checklists/secure-code-review-checklist.md), [../software-clean-code-standard/templates/checklists/backend-api-review-checklist.md](../software-clean-code-standard/templates/checklists/backend-api-review-checklist.md)

### Templates by Domain

#### Web Application Security

- [templates/web-application/template-authentication.md](templates/web-application/template-authentication.md) — Secure authentication flows (JWT, OAuth2, sessions, MFA)
- [templates/web-application/template-authorization.md](templates/web-application/template-authorization.md) — RBAC/ABAC/ReBAC policy patterns

#### API Security

- [templates/api/template-secure-api.md](templates/api/template-secure-api.md) — Secure API gateway, rate limiting, CORS, security headers

#### Cloud-Native Security

- [templates/cloud-native/crypto-security.md](templates/cloud-native/crypto-security.md) — Cryptography usage, key management, HSM integration

#### Blockchain & Web3 Security

- [resources/smart-contract-security-auditing.md](resources/smart-contract-security-auditing.md) — **NEW**: Smart contract auditing, vulnerability patterns, formal verification, Solidity security

### Related Skills

#### Security Ecosystem

- [../software-backend/SKILL.md](../software-backend/SKILL.md) — API implementation patterns and error handling
- [../software-architecture-design/SKILL.md](../software-architecture-design/SKILL.md) — Secure system decomposition and dependency design
- [../ops-devops-platform/SKILL.md](../ops-devops-platform/SKILL.md) — DevSecOps pipelines, secrets management, infrastructure hardening
- [../software-crypto-web3/SKILL.md](../software-crypto-web3/SKILL.md) — Smart contract security, blockchain vulnerabilities, DeFi patterns
- [../qa-testing-strategy/SKILL.md](../qa-testing-strategy/SKILL.md) — Security testing, SAST/DAST integration, penetration testing

#### AI/LLM Security

- [../ai-llm/SKILL.md](../ai-llm/SKILL.md) — LLM security patterns including prompt injection prevention
- [../ai-mlops/SKILL.md](../ai-mlops/SKILL.md) — ML model security, adversarial attacks, privacy-preserving ML

#### Quality & Resilience

- [../qa-resilience/SKILL.md](../qa-resilience/SKILL.md) — Resilience, safeguards, failure handling, chaos engineering
- [../qa-refactoring/SKILL.md](../qa-refactoring/SKILL.md) — Security-focused refactoring patterns

## Operational Playbooks
- [resources/operational-playbook.md](resources/operational-playbook.md) — Core security principles, OWASP summaries, authentication patterns, and detailed code examples
