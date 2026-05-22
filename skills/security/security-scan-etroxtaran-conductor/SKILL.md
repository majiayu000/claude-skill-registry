---
name: security-scan
description: Run comprehensive security audits including SAST, dependency scanning, and secret detection
version: 1.1.0
tags: [security, audit, sast, sca, secrets, vulnerabilities]
owner: security
status: active
---

# Security Scan Skill

## Overview

Run multi-layer security scans and summarize findings with remediation steps.

## Usage

```
/security-scan
```

## Identity
**Role**: Security Auditor
**Objective**: Identify security vulnerabilities in code, dependencies, containers, and configurations using automated scanning and manual review.

## Security Scanning Types

### 1. SAST (Static Application Security Testing)
Analyzes source code for vulnerabilities without executing it.

**What it finds**:
- SQL injection
- Cross-site scripting (XSS)
- Command injection
- Path traversal
- Insecure deserialization
- Hardcoded secrets

**Tools**:
| Language | Tool | Command |
|----------|------|---------|
| JavaScript/TypeScript | ESLint security plugins | `npm run lint` |
| Python | Bandit | `bandit -r src/` |
| Go | gosec | `gosec ./...` |
| Java | SpotBugs + FindSecBugs | `mvn spotbugs:check` |
| Multi-language | Semgrep | `semgrep --config auto .` |

### 2. SCA (Software Composition Analysis)
Scans dependencies for known vulnerabilities.

**npm/Node.js**:
```bash
# Built-in audit
npm audit

# With fix suggestions
npm audit --json | jq '.vulnerabilities'

# Auto-fix (patch/minor only)
npm audit fix

# See outdated packages
npm outdated
```

**Python**:
```bash
# pip-audit (recommended)
pip install pip-audit
pip-audit

# safety
pip install safety
safety check
```

**Docker Images**:
```bash
# Trivy (recommended)
trivy image myapp:latest

# Snyk
snyk container test myapp:latest

# Grype
grype myapp:latest
```

### 3. Secret Scanning
Detects accidentally committed secrets.

**Tools**:
```bash
# gitleaks (recommended)
gitleaks detect --source . --verbose

# truffleHog
trufflehog git file://. --only-verified

# detect-secrets
detect-secrets scan > .secrets.baseline
```

**Common Secrets to Find**:
- API keys (AWS, GCP, Azure, Stripe, etc.)
- Database connection strings
- JWT signing keys
- OAuth client secrets
- SSH private keys
- Certificates

### 4. Container Security
Scans Docker images and Kubernetes configs.

**Dockerfile Best Practices**:
```dockerfile
# Use specific versions, not :latest
FROM node:20.10.0-alpine

# Run as non-root user
RUN addgroup -g 1001 appgroup && \
    adduser -u 1001 -G appgroup -D appuser
USER appuser

# Don't expose unnecessary ports
EXPOSE 3000

# Use multi-stage builds to reduce attack surface
```

**Kubernetes Security**:
```bash
# kubesec - security risk analysis
kubesec scan deployment.yaml

# kube-bench - CIS benchmark
kube-bench run --targets node

# Check for misconfigurations
kubectl auth can-i --list
```

### 5. Infrastructure as Code (IaC)
Scans Terraform, CloudFormation, etc.

```bash
# tfsec for Terraform
tfsec .

# checkov for multiple IaC formats
checkov -d .

# terrascan
terrascan scan -t aws
```

## Comprehensive Scan Workflow

### Step 1: Run Automated Scans
```bash
#!/bin/bash
# security-scan.sh

echo "=== Dependency Scan ==="
npm audit --json > security-reports/npm-audit.json

echo "=== Secret Scan ==="
gitleaks detect --source . --report-path security-reports/secrets.json --report-format json

echo "=== SAST Scan ==="
semgrep --config auto . --json > security-reports/sast.json

echo "=== Container Scan ==="
trivy image myapp:latest --format json > security-reports/container.json
```

### Step 2: Triage Findings

**Severity Levels**:
| Level | Response Time | Action |
|-------|---------------|--------|
| CRITICAL | Immediate | Block deployment, fix now |
| HIGH | 24 hours | Priority fix in current sprint |
| MEDIUM | 1 week | Schedule in next sprint |
| LOW | 1 month | Add to backlog |

**False Positive Handling**:
```yaml
# .semgrep.yml - ignore false positives
rules:
  - id: my-rule
    patterns:
      - pattern: ...
    paths:
      exclude:
        - tests/
        - "*.test.ts"
```

### Step 3: Generate SBOM (Software Bill of Materials)

```bash
# Generate SBOM in CycloneDX format
npm sbom --sbom-format cyclonedx

# Or using syft
syft . -o cyclonedx-json > sbom.json
```

### Step 4: Report

**Security Report Template**:
```markdown
# Security Scan Report
**Date**: 2026-01-23
**Scanned**: myapp v1.2.3

## Summary
| Severity | Count |
|----------|-------|
| Critical | 0 |
| High | 2 |
| Medium | 5 |
| Low | 12 |

## Critical/High Findings

### HIGH: SQL Injection in user lookup
**File**: src/services/user.ts:45
**Issue**: User input directly interpolated in SQL query
**Fix**: Use parameterized queries
**CVE**: N/A (code issue)

### HIGH: Vulnerable dependency lodash
**Package**: lodash@4.17.20
**Issue**: Prototype pollution (CVE-2021-23337)
**Fix**: Upgrade to lodash@4.17.21
```

## CI/CD Integration

### GitHub Actions Example
```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  security:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run npm audit
        run: npm audit --audit-level=high

      - name: Run Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: auto

      - name: Run Trivy
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

      - name: Secret Scanning
        uses: gitleaks/gitleaks-action@v2
```

### Pre-commit Hook
```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.5
    hooks:
      - id: bandit
        args: ["-r", "src/"]
```

## OWASP Top 10 Checklist

| # | Vulnerability | Check |
|---|--------------|-------|
| 1 | Broken Access Control | Auth on all endpoints, RBAC tests |
| 2 | Cryptographic Failures | TLS everywhere, strong hashing |
| 3 | Injection | Parameterized queries, input validation |
| 4 | Insecure Design | Threat modeling, security requirements |
| 5 | Security Misconfiguration | Hardened configs, no defaults |
| 6 | Vulnerable Components | SCA scanning, update policy |
| 7 | Auth Failures | MFA, secure session management |
| 8 | Data Integrity Failures | Signed updates, CI/CD security |
| 9 | Logging Failures | Security event logging, monitoring |
| 10 | SSRF | URL validation, network segmentation |

## Output Format

```json
{
  "scan_date": "2026-01-23T10:30:00Z",
  "project": "myapp",
  "version": "1.2.3",
  "summary": {
    "critical": 0,
    "high": 2,
    "medium": 5,
    "low": 12,
    "total": 19
  },
  "scans_run": [
    "npm_audit",
    "semgrep",
    "gitleaks",
    "trivy"
  ],
  "blocking_issues": [
    {
      "severity": "HIGH",
      "type": "vulnerability",
      "package": "lodash",
      "cve": "CVE-2021-23337",
      "fix": "Upgrade to 4.17.21"
    }
  ],
  "sbom_generated": true,
  "report_path": "security-reports/scan-2026-01-23.json"
}
```

## Anti-Patterns

**DO NOT**:
- Ignore CRITICAL/HIGH findings
- Suppress warnings without documentation
- Commit secrets (even "test" ones)
- Use `:latest` tags in production
- Run containers as root
- Skip security scans to meet deadlines
- Trust user input without validation

## Outputs

- Security scan report with findings and remediation guidance.

## Related Skills

- `/dependency-update` - Update vulnerable dependencies
