---
name: audit-agent
description: "Comprehensive security and code quality audit. Use for thorough security, vulnerability, and code quality analysis. Related: project-health-checker for quick diagnostic checks."
version: 1.0.0
tags:
  - security
  - audit
  - quality
  - scanning
---

# Audit Agent

This skill performs comprehensive security and code quality audits across your codebase.

## Features

- **Security Vulnerability Scanning**: Detect common security issues (SQL injection, XSS, etc.)
- **Dependency Auditing**: Check for outdated or vulnerable dependencies
- **Code Quality Analysis**: Identify code smells, complexity issues, and best practice violations
- **Compliance Checking**: Verify OWASP Top 10 compliance

## When to Use

This skill is automatically invoked when you ask:

- "Run a security audit"
- "Check for vulnerabilities"
- "Audit the codebase"
- "Scan for security issues"
- "Check code quality"

## Audit Process

### 1. Security Scan

- Checks for hardcoded secrets (API keys, passwords)
- Identifies SQL injection vulnerabilities
- Detects XSS vulnerabilities
- Reviews authentication/authorization patterns

### 2. Dependency Audit

- Scans `package.json`, `requirements.txt`, `go.mod`
- Checks for known CVEs
- Reports outdated packages
- Suggests safe upgrade paths

### 3. Code Quality

- Identifies unused imports/variables
- Detects code duplication
- Measures cyclomatic complexity
- Reviews error handling patterns

### 4. Report Generation

- Creates detailed audit report
- Prioritizes findings by severity (Critical, High, Medium, Low)
- Provides remediation steps
- Includes code examples for fixes

## Example Usage

**User Request:**

> "Run a security audit on the backend API"

**Skill Actions:**

1. Scans `backend/` directory for security issues
2. Audits Python dependencies in `requirements.txt`
3. Checks FastAPI endpoints for common vulnerabilities
4. Generates comprehensive report with findings

**Output Format:**

```markdown
# Security Audit Report

## Summary

- 🔴 Critical: 2
- 🟠 High: 5
- 🟡 Medium: 8
- 🟢 Low: 12

## Critical Findings

### 1. Hardcoded API Key Detected

**File:** `backend/app/config.py:23`
**Issue:** API key hardcoded in source code
**Risk:** Credential exposure if code is leaked
**Fix:** Move to environment variable or Secret Manager

### 2. SQL Injection Vulnerability

**File:** `backend/app/api/users.py:45`
**Issue:** Unsanitized user input in SQL query
**Risk:** Database compromise
**Fix:** Use parameterized queries
```

## Configuration

No configuration required. The skill automatically:

- Detects project type (Python, Node.js, Go, etc.)
- Selects appropriate scanners
- Adapts to codebase structure

## Limitations

- Does not execute actual security testing tools (Bandit, OWASP ZAP)
- Provides static analysis recommendations only
- Requires user to run suggested tools for deep scanning

## Related Skills

- `security-analyst` - Deep security architecture review
- `project-health-checker` - Overall project health validation
- `dependency-updater` - Automated dependency updates
