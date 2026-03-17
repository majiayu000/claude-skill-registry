---
name: security-audit
description: "Comprehensive security audit of codebase using multiple security-auditor agents. Use before production deployments or after major features."
model: claude-sonnet-4-20250514
allowed-tools: Read, Write, Glob, Grep, Task
---

# /security-audit

Multi-agent security audit with findings saved to timestamped report.

## Usage

```bash
/security-audit yourbench           # Full security review
/security-audit coordinatr          # Audit specific project
```

## Audit Dimensions

Five security-auditor agents run in parallel:

| Agent | Focus Area | Checks |
|-------|------------|--------|
| **Agent 1: Auth & Access** | Authentication, Authorization | JWT handling, session management, RBAC, privilege escalation |
| **Agent 2: Input & Data** | Injection, Validation | SQL injection, XSS, command injection, input sanitization |
| **Agent 3: Crypto & Secrets** | Cryptography, Secrets | Hardcoded credentials, weak crypto, key management, PII |
| **Agent 4: Config & Deploy** | Configuration, Infrastructure | CORS, CSRF, security headers, exposed endpoints, debug mode |
| **Agent 5: Dependencies** | Supply Chain, Libraries | Vulnerable packages, outdated deps, license issues |

## OWASP Top 10 Coverage

| OWASP Risk | Coverage |
|------------|----------|
| A01 Broken Access Control | Agent 1 |
| A02 Cryptographic Failures | Agent 3 |
| A03 Injection | Agent 2 |
| A04 Insecure Design | Agents 1, 4 |
| A05 Security Misconfiguration | Agent 4 |
| A06 Vulnerable Components | Agent 5 |
| A07 Auth Failures | Agent 1 |
| A08 Data Integrity Failures | Agents 2, 3 |
| A09 Logging Failures | Agent 4 |
| A10 SSRF | Agent 2 |

## Execution Flow

### 1. Validate Project
```bash
ls spaces/[project]/
```

### 2. Launch Parallel Audits
5 security-auditor agents run concurrently with focused prompts.

### 3. Consolidate Findings
Aggregate by:
- **Severity**: Critical, High, Medium, Low, Info
- **Category**: OWASP classification
- **Location**: File path + line number
- **Remediation**: Specific fix guidance

### 4. Generate Report
```bash
Write: .claude/temp/security-audit-[project]-[timestamp].md
```

## Report Structure

```markdown
# Security Audit: [Project Name]
**Date**: YYYY-MM-DD HH:MM:SS

## Executive Summary
- Critical issues: X
- High severity: Y
- Total findings: Z

## Critical Issues
### [Issue Title]
- **Severity**: Critical
- **Category**: SQL Injection (CWE-89)
- **Location**: src/api/users.py:42
- **Description**: [What's wrong]
- **Impact**: [What could happen]
- **Remediation**: [How to fix]

## High Severity Issues
[...]

## Recommendations
- Priority actions
- Long-term improvements

## Scan Coverage
- Files scanned: X
- Technologies: Z
```

## When to Use

- Before production deployments
- After major feature additions
- Monthly security reviews
- Before external security audits
- After dependency updates

## Output Location

```
.claude/temp/security-audit-yourbench-2026-01-08-143022.md
```

Reports saved to `.claude/temp/` (gitignored) for review.

## Notes

- **Read-only**: No code changes made
- **Non-blocking**: Doesn't prevent commits
- **Parallel execution**: Agents run concurrently
- **False positives possible**: Manual review recommended

## Integration

```
Implement security feature → /security-audit → Fix issues → /commit
```
