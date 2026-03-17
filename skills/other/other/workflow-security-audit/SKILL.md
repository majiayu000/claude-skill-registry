---
name: workflow-security-audit
description: Comprehensive security assessment and remediation. Use for security reviews, compliance checks, vulnerability assessments.
---

# Security Audit Workflow

Comprehensive security assessment process.

## Phase 1: Threat Assessment
**Agents:** `security-auditor`

Scope:
- Authentication & authorization
- Data protection
- API security
- Dependency vulnerabilities
- Infrastructure security

**Output:** Threat model, risk assessment, priority list

## Phase 2: Automated Scanning
**Agents:** `security-auditor`

Tools to run:
- Dependency check (npm audit, pip-audit, cargo audit)
- Static analysis (semgrep, bandit, etc.)
- Secret scanning (trufflehog, gitleaks)

**Output:** Vulnerability report with severity ratings

## Phase 3: Manual Code Review
**Agents:** `security-auditor`

Focus areas:
- Input validation
- Output encoding
- Authentication logic
- Authorization checks
- Cryptography usage
- Session management

## Phase 4: Penetration Testing
**Agents:** `security-auditor`

Test for:
- SQL injection
- XSS attacks
- CSRF attacks
- Authentication bypass
- Privilege escalation

## Phase 5: Remediation Planning
**Agents:** `requirements-analyst`

- Create fix tasks from vulnerability report
- Prioritize by severity
- Estimate timeline
- Allocate resources

## Phase 6: Fix Implementation

**Blocking:** Validation required before proceeding

## Phase 7: Security Validation
**Agents:** `security-auditor`

- Retest all identified vulnerabilities
- Regression checks
- Verify fixes don't introduce new issues

## Phase 8: Documentation
**Agents:** `technical-writer`

- Security audit report
- Compliance documentation
- Security best practices guide

## Phase 9: Compliance Check
**Agents:** `security-auditor`

Standards:
- OWASP Top 10
- GDPR (if applicable)
- SOC2 (if applicable)
- HIPAA (if applicable)

## Success Criteria
- [ ] All critical vulnerabilities fixed
- [ ] All high vulnerabilities fixed
- [ ] Compliance requirements met
- [ ] Security tests pass

## Severity Levels
| Level | Response Time | Examples |
|-------|---------------|----------|
| Critical | Immediate | RCE, auth bypass, data breach |
| High | 24-48h | SQL injection, privilege escalation |
| Medium | 1 week | XSS, CSRF, information disclosure |
| Low | Next sprint | Best practice violations |
