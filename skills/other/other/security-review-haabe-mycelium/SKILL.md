---
name: security-review
description: "OWASP secure design review for code and architecture. Checks input validation, authentication, authorization, data protection."
instruction_budget: 42
---

# Security Review

Language-agnostic security review based on OWASP Secure by Design.

## Checklist (OWASP Top 10:2025)

*Updated to OWASP Top 10:2025 (released January 2025). Previous 2021 edition had different groupings.*

### A01:2025 — Broken Access Control
- [ ] Least privilege enforced (users get minimum permissions needed)
- [ ] Authorization checked on EVERY request (not just the first)
- [ ] CORS restrictive (not `*`)
- [ ] Directory listing disabled
- [ ] Rate limiting on API/controller access

### A02:2025 — Cryptographic Failures
- [ ] Data encrypted at rest and in transit (TLS 1.2+)
- [ ] No secrets in code, logs, or error messages
- [ ] PII identified and classified in threat model
- [ ] Passwords hashed with bcrypt/argon2 (never MD5/SHA1)
- [ ] Cryptographic algorithms current (no deprecated ciphers)

### A03:2025 — Injection
- [ ] All user input validated (type, length, range, format)
- [ ] Parameterized queries for ALL data access (never string concatenation)
- [ ] Input allowlisting preferred over denylisting
- [ ] Output encoded based on context (HTML, JS, URL, CSS — covers XSS)
- [ ] Content Security Policy configured

### A03b:2025 — Software Supply Chain Failures *(new in 2025)*
- [ ] SBOM (Software Bill of Materials) maintained for critical dependencies
- [ ] Build integrity verified (reproducible builds, signed artifacts)
- [ ] Dependency provenance checked (not just version, but source authenticity)
- [ ] Transitive dependencies audited (not just direct)
- [ ] Lock files committed and verified

### A04:2025 — Insecure Design
- [ ] Threat modeling performed (STRIDE — see /threat-model)
- [ ] Secure design patterns used (defense in depth, fail secure)
- [ ] Business logic abuse cases considered
- [ ] Security requirements defined alongside functional requirements

### A05:2025 — Security Misconfiguration
- [ ] Default credentials changed
- [ ] Unnecessary features/ports disabled
- [ ] Security headers set (CSP, HSTS, X-Frame-Options, X-Content-Type-Options)
- [ ] Error handling does not expose stack traces

### A06:2025 — Vulnerable and Outdated Components
- [ ] Dependency audit run (no known critical vulnerabilities)
- [ ] Dependencies pinned to specific versions
- [ ] Automated scanning in CI
- [ ] Unused dependencies removed

### A07:2025 — Identification and Authentication Failures
- [ ] Session IDs regenerated on login
- [ ] Multi-factor authentication available for sensitive operations
- [ ] Credential stuffing protections (rate limiting, account lockout)
- [ ] Password strength requirements enforced

### A08:2025 — Software and Data Integrity Failures
- [ ] CI/CD pipeline integrity verified (no unsigned code execution)
- [ ] Deserialization inputs validated
- [ ] Software supply chain reviewed (SBOMs for critical dependencies)
- [ ] Auto-update mechanisms use signed packages

### A09:2025 — Security Logging and Monitoring Failures
- [ ] Security events logged (login attempts, auth failures, access denials)
- [ ] No sensitive data in logs
- [ ] Alerting on anomalous patterns
- [ ] Logs tamper-resistant (append-only or forwarded to SIEM)

### A10:2025 — Server-Side Request Forgery (SSRF)
- [ ] URL inputs validated and allowlisted
- [ ] Internal network access restricted from user-supplied URLs
- [ ] Response content not returned directly to users without sanitization

### A10b:2025 — Mishandling of Exceptional Conditions *(new in 2025)*
- [ ] All error paths explicitly handled (no silent failures)
- [ ] Resource exhaustion scenarios addressed (memory, disk, connections)
- [ ] Timeout and retry policies defined for all external calls
- [ ] System fails closed (denies access on error, not grants)

## OWASP Top 10 for LLM Applications (2025)

*Apply for `ai_tool` product types. Source: owasp.org/www-project-top-10-for-large-language-model-applications*

- [ ] **Prompt Injection**: User input cannot override system instructions (direct or indirect)
- [ ] **Data Poisoning**: Training/fine-tuning data sources validated and auditable
- [ ] **Insecure Output Handling**: LLM output sanitized before use in downstream systems (SQL, shell, HTML)
- [ ] **Model Denial of Service**: Rate limiting and resource caps on inference requests
- [ ] **Supply Chain**: Model provenance verified; third-party models/plugins audited
- [ ] **Sensitive Information Disclosure**: PII/secrets not leaked in model responses; training data scrubbed
- [ ] **Insecure Plugin/Tool Design**: Tool permissions follow least privilege; tool outputs validated
- [ ] **Excessive Agency**: Model actions bounded; human-in-the-loop for destructive operations
- [ ] **Overreliance**: Users informed of model limitations; confidence indicators provided
- [ ] **Model Theft**: Model weights and fine-tuning data access-controlled

## Decision Log (MANDATORY per G-P4)
**APPEND** a `### Security Review` entry to `harness/decision-log.md` with: OWASP categories assessed, findings, risk ratings, remediation recommendations.

## Stack-Specific Tools
Consult `.claude/jit-tooling/security-scanning.md` for tool selection per stack.
