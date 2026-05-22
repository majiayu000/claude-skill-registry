---
name: security-assessment
description: Execute threat modeling, vulnerability scanning, and security control validation. Use when relevant to the task.
---

# security-assessment

Execute threat modeling, vulnerability scanning, and security control validation.

## Triggers

- "run security review"
- "security assessment"
- "threat model [component]"
- "validate security controls"
- "security scan"
- "check vulnerabilities"

## Purpose

This skill orchestrates comprehensive security assessment through:
- STRIDE threat modeling
- Vulnerability pattern detection
- Security control validation
- Compliance verification
- Risk scoring and prioritization

## Behavior

When triggered, this skill:

1. **Determines scope**:
   - Component-level, system-level, or full assessment
   - Identify assets and trust boundaries
   - Load existing threat model if available

2. **Executes threat modeling**:
   - Dispatch Security Architect for STRIDE analysis
   - Enumerate threats per component
   - Identify attack vectors

3. **Runs vulnerability patterns**:
   - Dispatch Security Auditor for pattern scanning
   - Check OWASP Top 10
   - Identify secrets exposure risks
   - Review dependency vulnerabilities

4. **Validates controls**:
   - Dispatch Security Gatekeeper
   - Map controls to threats
   - Verify implementation
   - Check coverage gaps

5. **Assesses privacy**:
   - Dispatch Privacy Officer (if PII involved)
   - Check data handling
   - Verify consent mechanisms

6. **Generates report**:
   - Risk-ranked findings
   - CVSS scores where applicable
   - Remediation guidance
   - Compliance status

## STRIDE Threat Categories

| Category | Description | Example |
|----------|-------------|---------|
| **S**poofing | Impersonating something/someone | Fake user credentials |
| **T**ampering | Modifying data or code | SQL injection |
| **R**epudiation | Denying actions | Missing audit logs |
| **I**nformation Disclosure | Exposing information | Data leakage |
| **D**enial of Service | Disrupting availability | Resource exhaustion |
| **E**levation of Privilege | Gaining unauthorized access | Broken access control |

## Assessment Flow

```
┌─────────────────────────────────────────────────────────┐
│ 1. SCOPE IDENTIFICATION                                 │
│    • Define assessment boundary                         │
│    • Identify assets (data, services, infrastructure)   │
│    • Map trust boundaries                               │
│    • Load existing threat model (if any)                │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 2. THREAT MODELING (Security Architect)                 │
│    • Data flow analysis                                 │
│    • STRIDE enumeration per component                   │
│    • Attack vector identification                       │
│    • Trust boundary crossing analysis                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 3. VULNERABILITY SCANNING (Security Auditor)            │
│    • OWASP Top 10 pattern check                         │
│    • Secrets exposure scan                              │
│    • Dependency vulnerability check                     │
│    • Configuration review                               │
│    • Code pattern analysis                              │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 4. CONTROL VALIDATION (Security Gatekeeper)             │
│    • Map security requirements to controls              │
│    • Verify control implementation                      │
│    • Check control effectiveness                        │
│    • Identify coverage gaps                             │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 5. PRIVACY ASSESSMENT (Privacy Officer) [if PII]        │
│    • Data inventory review                              │
│    • Consent mechanism validation                       │
│    • Data retention compliance                          │
│    • Cross-border transfer assessment                   │
└─────────────────────────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────┐
│ 6. RISK SCORING & REPORTING                             │
│    • Calculate CVSS scores                              │
│    • Prioritize by risk (likelihood × impact)           │
│    • Generate remediation guidance                      │
│    • Produce assessment report                          │
└─────────────────────────────────────────────────────────┘
```

## OWASP Top 10 Checks

| # | Category | Patterns Checked |
|---|----------|-----------------|
| A01 | Broken Access Control | RBAC, ABAC, path traversal, CORS |
| A02 | Cryptographic Failures | Weak algorithms, key management, TLS |
| A03 | Injection | SQL, NoSQL, LDAP, OS command, XSS |
| A04 | Insecure Design | Threat modeling gaps, missing controls |
| A05 | Security Misconfiguration | Defaults, unnecessary features, verbose errors |
| A06 | Vulnerable Components | Outdated dependencies, known CVEs |
| A07 | Auth Failures | Password policies, MFA, session management |
| A08 | Data Integrity Failures | CI/CD security, unsigned updates |
| A09 | Logging Failures | Missing logs, sensitive data in logs |
| A10 | SSRF | Internal resource access, URL validation |

## Severity Scoring

### CVSS Base Metrics

```yaml
severity_levels:
  critical:
    cvss_range: [9.0, 10.0]
    description: Immediate remediation required
    sla: 24 hours

  high:
    cvss_range: [7.0, 8.9]
    description: Remediation within sprint
    sla: 7 days

  medium:
    cvss_range: [4.0, 6.9]
    description: Plan remediation
    sla: 30 days

  low:
    cvss_range: [0.1, 3.9]
    description: Address as time permits
    sla: 90 days

  informational:
    cvss_range: [0.0, 0.0]
    description: Awareness only
    sla: none
```

## Assessment Report Format

```markdown
# Security Assessment Report

**Date**: 2025-12-08
**Scope**: Full System Assessment
**Assessors**: security-architect, security-auditor, security-gatekeeper

## Executive Summary

| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 5 |
| Low | 8 |
| Informational | 3 |

**Overall Risk Level**: MEDIUM
**Recommendation**: Address high-severity findings before production deployment

## Threat Model Summary

### Trust Boundaries
1. External → API Gateway
2. API Gateway → Internal Services
3. Services → Database

### STRIDE Analysis

| Component | S | T | R | I | D | E | Total |
|-----------|---|---|---|---|---|---|-------|
| API Gateway | 2 | 1 | 0 | 1 | 1 | 1 | 6 |
| Auth Service | 3 | 1 | 1 | 2 | 0 | 2 | 9 |
| Data Service | 1 | 2 | 1 | 3 | 1 | 1 | 9 |

## Findings

### HIGH-001: Insufficient Input Validation
- **Severity**: High (CVSS 7.5)
- **Component**: API Gateway
- **Category**: A03 Injection
- **Description**: User input not sanitized before database query
- **Impact**: SQL injection possible, data exfiltration risk
- **Remediation**: Implement parameterized queries, add input validation
- **Status**: Open

### HIGH-002: Missing Rate Limiting
- **Severity**: High (CVSS 7.2)
- **Component**: API Gateway
- **Category**: A05 Denial of Service
- **Description**: No rate limiting on authentication endpoints
- **Impact**: Brute force attacks, credential stuffing
- **Remediation**: Implement rate limiting, add account lockout
- **Status**: Open

### MEDIUM-001: Verbose Error Messages
...

## Control Assessment

| Control | Requirement | Status | Gap |
|---------|-------------|--------|-----|
| Authentication | MFA for privileged users | ✅ Implemented | None |
| Authorization | RBAC with least privilege | ⚠️ Partial | Admin role too broad |
| Encryption | TLS 1.2+ for transit | ✅ Implemented | None |
| Encryption | AES-256 at rest | ⚠️ Partial | Logs not encrypted |
| Logging | Security event logging | ✅ Implemented | None |
| Monitoring | Real-time alerting | ❌ Missing | Not configured |

## Compliance Status

| Framework | Status | Gaps |
|-----------|--------|------|
| OWASP Top 10 | 7/10 compliant | A03, A05, A09 |
| SOC 2 | Partial | Monitoring, encryption |
| GDPR | Compliant | None identified |

## Remediation Roadmap

### Immediate (24-48 hours)
- [ ] Fix SQL injection vulnerability (HIGH-001)
- [ ] Implement rate limiting (HIGH-002)

### Short-term (1-2 weeks)
- [ ] Reduce admin role permissions
- [ ] Encrypt log storage
- [ ] Configure monitoring alerts

### Medium-term (1 month)
- [ ] Address medium-severity findings
- [ ] Complete SOC 2 gap remediation

## Next Assessment

Recommended: 30 days or after major changes
```

## Usage Examples

### Full Assessment

```
User: "Run security review"

Skill orchestrates:
1. Load current architecture
2. Run STRIDE analysis
3. Scan for OWASP patterns
4. Validate controls
5. Generate report

Output:
"Security Assessment Complete

Findings: 0 Critical, 2 High, 5 Medium, 8 Low
Risk Level: MEDIUM

Blocking Issues:
- HIGH-001: SQL injection risk
- HIGH-002: Missing rate limiting

Report: .aiwg/security/assessment-20251208.md"
```

### Component Assessment

```
User: "Threat model the authentication service"

Skill focuses on:
- Auth service components only
- STRIDE for auth flows
- Auth-specific vulnerabilities
- Control validation for auth

Output: Targeted threat model and findings
```

### Control Validation Only

```
User: "Validate security controls"

Skill runs:
- Control mapping
- Implementation verification
- Gap analysis

Output: Control assessment summary
```

## Integration

This skill uses:
- `parallel-dispatch`: Launch security agents concurrently
- `project-awareness`: Get architecture and component info
- `artifact-metadata`: Track assessment artifacts

## Agent Orchestration

```yaml
agents:
  threat_modeling:
    agent: security-architect
    focus: STRIDE analysis, attack vectors, trust boundaries

  vulnerability_scanning:
    agent: security-auditor
    focus: OWASP patterns, secrets, dependencies, configuration

  control_validation:
    agent: security-gatekeeper
    focus: Control mapping, implementation, effectiveness

  privacy_assessment:
    agent: privacy-officer
    focus: PII handling, consent, retention, transfers
    condition: has_pii == true
```

## Output Locations

- Assessment report: `.aiwg/security/assessment-{date}.md`
- Threat model: `.aiwg/security/threat-model.md`
- Control matrix: `.aiwg/security/control-matrix.md`
- Findings tracker: `.aiwg/security/findings/`

## References

- STRIDE methodology: Microsoft Threat Modeling
- OWASP Top 10: https://owasp.org/Top10/
- CVSS Calculator: https://www.first.org/cvss/calculator/3.1
- Security templates: templates/security/
