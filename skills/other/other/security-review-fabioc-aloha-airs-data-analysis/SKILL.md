---
name: "Security Review Skill"
description: "Defend before attackers find the gaps - OWASP, STRIDE, and Microsoft SFI"
applyTo: "**/*security*,**/*auth*,**/*password*,**/*token*,**/*credential*,**/*vulnerability*,**/*CVE*,**/*secret*"
---

# Security Review Skill

> Defend before attackers find the gaps.

## ⚠️ Staleness Warning

Security practices evolve with new threats, vulnerabilities, and industry standards.

**Refresh triggers:**
- New CVEs affecting our stack
- Microsoft SFI updates
- Major security incidents (industry-wide)
- Dependency security advisories
- Compliance requirement changes

**Last validated:** February 2026

**Check current state:** [Microsoft SFI](https://www.microsoft.com/en-us/trust-center/security/secure-future-initiative), [OWASP](https://owasp.org/), [CVE Database](https://cve.mitre.org/)

---

## Core Principle

Security is not a feature—it's a property. Review code with adversarial thinking.

---

## Microsoft Secure Future Initiative (SFI)

Microsoft's approach to security-first development:

### SFI Core Principles

| Principle | Focus |
| --------- | ----- |
| **Secure by Design** | Security comes first when designing any product or service |
| **Secure by Default** | Protections enabled/enforced by default, require no extra effort, not optional |
| **Secure Operations** | Security controls and monitoring continuously improved for current/future threats |

> **Satya's Mandate (May 2024):** "If you're faced with the tradeoff between security and another priority, your answer is clear: Do security."

### SFI Foundations

Four foundations that underpin successful security operations:

| Foundation | Description |
| ---------- | ----------- |
| **Security-first Culture** | Daily behaviors reinforced through regular meetings between engineering and SFI leaders |
| **Security Governance** | Framework led by CISO, partnering with engineering teams to oversee SFI and manage risks |
| **Continuous Improvement** | Growth mindset integrating feedback and learnings from incidents into standards |
| **Paved Paths & Standards** | Best practices that optimize productivity, compliance, and security at scale |

### SFI Six Pillars

| Pillar | Focus |
| ------ | ----- |
| **Protect Identities & Secrets** | Best-in-class standards for identity/secrets infrastructure, phishing-resistant MFA |
| **Protect Tenants & Isolate Systems** | Tenant isolation and production system protection |
| **Protect Networks** | Network security and segmentation |
| **Protect Engineering Systems** | Secure development infrastructure and CI/CD |
| **Monitor & Detect Cyberthreats** | Continuous threat monitoring and detection |
| **Accelerate Response & Remediation** | Fast incident response and recovery |

### Secure by Design Checklist

Before coding:
- [ ] Authentication method defined
- [ ] Authorization model designed
- [ ] Data classification done
- [ ] Encryption requirements clear
- [ ] Logging requirements defined
- [ ] Third-party dependencies reviewed

### Secure by Default Patterns

```typescript
// Bad: Optional security
createServer({ https: false, cors: '*' });

// Good: Secure by default
createServer({
    https: true,
    cors: ['https://trusted.com'],
    helmet: true
});
```

**Principle of Least Privilege:**

```typescript
// Bad: Admin access by default
const user = { role: 'admin', permissions: ['*'] };

// Good: Minimum permissions
const user = { role: 'viewer', permissions: ['read:own'] };
```

**Input Validation:**

```typescript
// Validate and sanitize ALL input
function processInput(input: unknown) {
    const validated = schema.parse(input); // Zod, Joi, etc.
    const sanitized = sanitize(validated);
    return sanitized;
}
```

---

## OWASP Top 10

| # | Vulnerability | What to Check | Prevention |
|---|---------------|---------------|------------|
| 1 | Broken Access Control | Check permissions on every request | Authorization on all routes |
| 2 | Cryptographic Failures | Use strong, modern crypto | TLS 1.2+, proper key management |
| 3 | Injection | SQL, NoSQL, LDAP, OS commands | Parameterized queries, no string concat |
| 4 | Insecure Design | Threat modeling, secure patterns | STRIDE analysis pre-implementation |
| 5 | Security Misconfiguration | Secure defaults, remove unused features | Hardened configs, no default passwords |
| 6 | Vulnerable Components | Dependency scanning, updates | npm audit, regular updates |
| 7 | Auth Failures | MFA, secure session management | Strong passwords, session timeout |
| 8 | Data Integrity | Signatures, checksums | Tamper detection |
| 9 | Logging Failures | Comprehensive audit logging | Monitor security events |
| 10 | SSRF | Allowlist URLs, validate requests | Input validation, URL allowlisting |

---

## Threat Modeling (STRIDE)

| Threat | Question | Mitigation |
|--------|----------|------------|
| **S**poofing | Can attacker impersonate? | Strong authentication, phishing-resistant MFA |
| **T**ampering | Can data be modified? | Integrity checks, signatures, checksums |
| **R**epudiation | Can actions be denied? | Audit logging, non-repudiation mechanisms |
| **I**nformation Disclosure | Can secrets leak? | Encryption at rest/transit, access control |
| **D**enial of Service | Can system be overwhelmed? | Rate limiting, quotas, redundancy |
| **E**levation of Privilege | Can attacker gain access? | Least privilege, authorization checks |

---

## Code Review Security Lens

### Authentication
```
□ Passwords hashed with bcrypt/argon2 (not MD5/SHA1)
□ No hardcoded credentials
□ Session tokens are random, rotated, and expire
□ Failed login attempts are rate-limited
□ MFA supported where appropriate
```

### Authorization
```
□ Every endpoint has explicit access control
□ No security through obscurity (hidden URLs)
□ Resource ownership verified before access
□ Admin functions require elevated auth
□ Deny by default, allow explicitly
```

### Input Validation
```
□ All input validated on server (not just client)
□ Allowlist validation preferred over blocklist
□ File uploads restricted by type and size
□ URL redirects validated against allowlist
□ JSON/XML parsing has size limits
```

### Data Protection
```
□ Sensitive data encrypted at rest
□ TLS 1.2+ for data in transit
□ API keys/secrets in env vars, not code
□ PII minimized and retention limited
□ Logs don't contain passwords/tokens/PII
```

### Dependencies
```
□ npm audit / pip audit / cargo audit clean
□ No deprecated or unmaintained packages
□ Dependabot or Renovate enabled
□ Lock files committed
□ Known CVE check before release
```

---

## Credential Management

### Never Hardcode

```typescript
// NEVER
const apiKey = 'sk-1234567890abcdef';

// ALWAYS
const apiKey = process.env.API_KEY;
// Or: Azure Key Vault, AWS Secrets Manager, etc.
```

### Rotation Policy

| Credential Type | Rotation Period |
|----------------|-----------------|
| API Keys | 90 days |
| Service Passwords | 90 days |
| Certificates | 1 year |
| User Passwords | User discretion + breach response |

### Secrets in Git

If secrets accidentally committed:

1. **Revoke immediately** — The secret is compromised
2. **Remove from history** — `git filter-branch` or BFG
3. **Rotate** — Generate new credentials
4. **Audit** — Check for unauthorized use

---

## Dependency Security

### Regular Audits

```powershell
# npm
npm audit
npm audit fix

# Check for outdated
npm outdated
```

### Automated Scanning

- Dependabot (GitHub)
- Snyk
- npm audit in CI/CD

### Update Strategy

| Severity | Response Time |
| -------- | ------------- |
| Critical | 24-48 hours |
| High | 1 week |
| Medium | 2 weeks |
| Low | Next release |

---

## Security Code Review Checklist

### Pre-Merge Gate

- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Output encoding for XSS
- [ ] SQL uses parameterized queries
- [ ] Auth checks on all endpoints
- [ ] Sensitive data encrypted
- [ ] Errors don't leak info
- [ ] Dependencies up to date

### Red Flags

```text
🚩 eval(), exec(), dangerouslySetInnerHTML
🚩 String concatenation in queries
🚩 Disabled security features
🚩 Overly permissive CORS
🚩 Secrets in code or config files
🚩 Missing rate limiting
🚩 Verbose error messages
```

---

## Common Vulnerabilities by Language

| Language | Watch For |
|----------|-----------|
| JavaScript | Prototype pollution, eval(), innerHTML |
| TypeScript | Type assertions bypassing validation |
| Python | pickle deserialization, format strings |
| SQL | String concatenation in queries |
| Shell | Command injection, unquoted variables |

---

## Security Headers Checklist

```http
Content-Security-Policy: default-src 'self'
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
Strict-Transport-Security: max-age=31536000
X-XSS-Protection: 0 (deprecated, use CSP)
```

---

## Quick Security Questions

Before shipping, ask:
1. **What's the worst thing an attacker could do?**
2. **What data could leak if this endpoint is exposed?**
3. **Who should NOT have access to this?**
4. **What happens if input is malicious?**
5. **Are we trusting anything we shouldn't?**

---

## Incident Response Connection

When vulnerability found:
1. **Assess**: What's the blast radius?
2. **Contain**: Can we disable the feature?
3. **Fix**: Patch the vulnerability
4. **Verify**: Confirm fix works
5. **Learn**: Update review checklist

See [incident-response](../incident-response/SKILL.md) for full IR workflow.

---

## Synapses

See [synapses.json](synapses.json) for connections.

---

*Consolidated: 2026-02-19*
*Sources: security-review (2026-02-01) + microsoft-sfi*
