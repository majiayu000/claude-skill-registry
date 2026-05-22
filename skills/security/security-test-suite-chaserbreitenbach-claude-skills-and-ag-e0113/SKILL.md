---
name: security-test-suite
description: |
  Comprehensive security testing framework aligned with OWASP Top 10 and CWE/SANS Top 25.
  Performs static analysis (SAST), dependency auditing (SCA), secret scanning, and infrastructure
  security checks. Generates actionable remediation reports with CVSS severity scoring.
license: MIT
allowed-tools:
  - Bash
  - Read
  - Write
  - Edit
  - Glob
  - Grep
compatibility:
  claude-code: ">=1.0.0"
metadata:
  version: "1.0.0"
  author: "QuantQuiver AI R&D"
  category: "testing"
  tags:
    - security
    - owasp
    - sast
    - vulnerability-scanning
    - secret-detection
---

# Security Test Suite

## Purpose

Comprehensive security testing framework aligned with OWASP Top 10 and CWE/SANS Top 25. Performs static analysis (SAST), dependency auditing (SCA), secret scanning, and infrastructure security checks. Generates actionable remediation reports.

## Triggers

Use this skill when:

- "security scan"
- "check for vulnerabilities"
- "OWASP compliance test"
- "penetration test preparation"
- "security audit"
- "find security issues"
- "dependency vulnerability check"

## When to Use

- Pre-deployment security review
- Compliance requirements (SOC2, HIPAA, PCI-DSS)
- New third-party integrations
- Authentication/authorization changes
- Handling sensitive data
- Public-facing applications

## When NOT to Use

- Functional testing (use unit-test-generator)
- Performance testing (use performance-benchmark)
- Data quality validation (use data-validation)

---

## Core Instructions

### Security Testing Layers

| Layer | Description |
| ----- | ----------- |
| **SAST** | Code pattern scanning, taint analysis, security linting |
| **SCA** | Known vulnerability scanning (CVE), license compliance |
| **Secrets** | Hardcoded credential detection, entropy analysis |
| **Infrastructure** | Container security, IaC scanning, cloud misconfigurations |

### OWASP Top 10 Coverage

| OWASP Category | Test Types | Severity |
| -------------- | ---------- | -------- |
| A01: Broken Access Control | AuthZ bypass, IDOR, privilege escalation | Critical |
| A02: Cryptographic Failures | Weak crypto, plaintext secrets, bad TLS | Critical |
| A03: Injection | SQLi, XSS, Command, LDAP injection | Critical |
| A04: Insecure Design | Business logic, threat modeling | High |
| A05: Security Misconfiguration | Default creds, verbose errors | High |
| A06: Vulnerable Components | Known CVEs, outdated deps | High |
| A07: Auth Failures | Weak passwords, session fixation | High |
| A08: Data Integrity Failures | Insecure deserialization | High |
| A09: Logging Failures | Missing logs, log injection | Medium |
| A10: SSRF | Server-side request forgery | High |

### Severity Scoring (CVSS 3.1)

| Score | Severity | SLA | Action |
| ----- | -------- | --- | ------ |
| 9.0-10.0 | Critical | 24h | Immediate fix, block deployment |
| 7.0-8.9 | High | 7d | Fix before next release |
| 4.0-6.9 | Medium | 30d | Schedule remediation |
| 0.1-3.9 | Low | 90d | Backlog |

### Detection Patterns

```yaml
patterns:
  sql_injection:
    regex: '\.execute\s*\(\s*f["\']'
    severity: CRITICAL
    cwe: CWE-89
    message: "F-strings in SQL queries lead to injection"

  hardcoded_secret:
    regex: '(password|secret|api_key)\s*=\s*["\'][^"\']+["\']'
    severity: HIGH
    cwe: CWE-798
    message: "Hardcoded credentials detected"

  eval_usage:
    regex: 'eval\s*\([^)]*\)'
    severity: HIGH
    cwe: CWE-95
    message: "eval() can execute arbitrary code"
```

---

## Templates

### Security Report

```markdown
# Security Scan Report

**Timestamp:** {timestamp}
**Repository:** {repository}

## Executive Summary

**Overall Risk Level:** {risk_level}

| Severity | Count | SLA |
| -------- | ----- | --- |
| Critical | {critical} | 24 hours |
| High | {high} | 7 days |
| Medium | {medium} | 30 days |
| Low | {low} | 90 days |

## Critical Findings

### {finding_id}: {title}

**Severity:** {severity} (CVSS: {cvss})
**CWE:** {cwe_id}
**Location:** `{file_path}:{line_number}`

**Code:**

```
{code_snippet}
```

**Remediation:**
{remediation}
```

---

## Example

**Input**: Security scan of Flask application

**Output**:

```markdown
## Executive Summary

**Overall Risk Level:** HIGH

| Severity | Count |
| -------- | ----- |
| Critical | 1 |
| High | 3 |
| Medium | 5 |

## Critical Findings

### SAST-0001: SQL injection via f-string

**Severity:** CRITICAL (CVSS: 9.5)
**Location:** `app/database.py:45`

**Code:**

```python
query = f"SELECT * FROM users WHERE id = {user_id}"
cursor.execute(query)
```

**Remediation:**
Use parameterized queries:

```python
cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
```
```

---

## Validation Checklist

- [ ] All source files scanned
- [ ] Dependency manifests analyzed
- [ ] Git history checked for secrets (if enabled)
- [ ] All CRITICAL issues have specific remediation
- [ ] OWASP coverage mapping complete
- [ ] False positives reviewed and documented

---

## Related Skills

- `api-contract-validator` - For API security testing
- `unit-test-generator` - For testing security fixes
- `test-health-monitor` - For security test coverage
