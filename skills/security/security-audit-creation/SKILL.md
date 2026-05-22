---
name: security-audit-creation
description: "Generate security audit documentation following the SECURITY-AUDIT template. Use when performing security reviews, checking for vulnerabilities, or when the user asks for a security audit."
event: security-review
auto_trigger: false
version: "1.0.0"
last_updated: "2026-01-26"

# Inputs/Outputs
inputs:
  - audit_scope
  - threat_model
  - vulnerabilities_found
  - compliance_requirements
  - remediation_priority
output: security_audit_document
output_format: "Markdown audit report (09-SECURITY-AUDIT-TEMPLATE.md)"
output_path: "docs/technical/security/"

# Auto-Trigger Rules
auto_invoke:
  events:
    - "security-review"
    - "pre-deployment"
    - "compliance-audit"
  conditions:
    - "user requests security audit"
    - "pre-production review"
    - "compliance requirement"

# Validation
validation_rules:
  - "OWASP Top 10 addressed"
  - "all vulnerabilities have severity"
  - "remediation timeline defined"
  - "compliance checklist completed"

# Chaining
chain_after: []
chain_before: [doc-index-update]

# Agent Association
called_by: ["@Security"]
mcp_tools:
  - mcp_payment-syste_search_full_text
  - read_file
  - grep_search
---

# Security Audit Creation Skill

> **Purpose:** Generate comprehensive security audit documentation. Ensures security reviews are thorough and remediation is tracked.

## Trigger

**When:** Pre-deployment review OR compliance audit OR security concern raised
**Context Needed:** Code to review, threat model, compliance requirements
**MCP Tools:** `mcp_payment-syste_search_full_text`, `read_file`, `grep_search`

## Required Sections

```markdown
# [Feature/System] - Security Audit

## Audit Metadata

- Date: YYYY-MM-DD
- Auditor: @username
- Scope: [description]
- Classification: internal | confidential

## Executive Summary

[High-level findings]

## Threat Model

### Assets

- [asset]: [classification]

### Threat Actors

- [actor]: [capability]

### Attack Vectors

- [vector]: [mitigation]

## Findings

### Critical

| ID  | Title | Status | Remediation |
| :-- | :---- | :----- | :---------- |

### High

...

### Medium

...

### Low

...

## Compliance Status

- [ ] OWASP Top 10
- [ ] PCI-DSS (if applicable)
- [ ] GDPR (if applicable)
```

## OWASP Top 10 Checklist

```markdown
## OWASP Top 10 (2021)

| #   | Category                  | Status   | Notes |
| :-- | :------------------------ | :------- | :---- |
| A01 | Broken Access Control     | ✅/⚠️/❌ |       |
| A02 | Cryptographic Failures    | ✅/⚠️/❌ |       |
| A03 | Injection                 | ✅/⚠️/❌ |       |
| A04 | Insecure Design           | ✅/⚠️/❌ |       |
| A05 | Security Misconfiguration | ✅/⚠️/❌ |       |
| A06 | Vulnerable Components     | ✅/⚠️/❌ |       |
| A07 | Auth Failures             | ✅/⚠️/❌ |       |
| A08 | Software/Data Integrity   | ✅/⚠️/❌ |       |
| A09 | Security Logging          | ✅/⚠️/❌ |       |
| A10 | SSRF                      | ✅/⚠️/❌ |       |
```

## Finding Format

```markdown
### FINDING-001: [Title]

**Severity:** Critical | High | Medium | Low
**Category:** OWASP A0X
**Status:** Open | In Progress | Resolved

**Description:**
[What was found]

**Impact:**
[Potential damage]

**Reproduction:**

1. [step]
2. [step]

**Recommendation:**
[How to fix]

**Remediation Timeline:**

- Target: YYYY-MM-DD
- Owner: @username
```

## Reference

- [09-SECURITY-AUDIT-TEMPLATE.md](/docs/templates/09-SECURITY-AUDIT-TEMPLATE.md)
- [SECURITY-ARCHITECTURE.md](/docs/technical/architecture/SECURITY-ARCHITECTURE.md)
