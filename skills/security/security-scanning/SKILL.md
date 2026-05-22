---
name: security-scanning
description: Automated security scanning for dependencies and code. Use when running npm audit, pip-audit, Semgrep, secret detection, or integrating security checks into CI/CD.
context: fork
agent: security-auditor
allowed-tools:
  - Read
  - Grep
  - Glob
  - Bash  # For running security scanners only
version: 1.0.0
author: SkillForge
user-invocable: false
---

# Security Scanning

Automate vulnerability detection in code and dependencies.

## When to Use

- Before code review completion
- After dependency updates
- In CI/CD pipelines
- Before production deployments

## Dependency Scanning

### JavaScript (npm)

```bash
# Run audit
npm audit --json > security-audit.json

# Check severity counts
CRITICAL=$(npm audit --json | jq '.metadata.vulnerabilities.critical')
HIGH=$(npm audit --json | jq '.metadata.vulnerabilities.high')

if [ "$CRITICAL" -gt 0 ] || [ "$HIGH" -gt 0 ]; then
  echo "🚨 $CRITICAL critical, $HIGH high vulnerabilities"
fi

# Auto-fix
npm audit fix
```

### Python (pip-audit)

```bash
pip-audit --format=json > security-audit.json

# Using safety
safety check --json > security-audit.json
```

## Static Analysis (SAST)

### Semgrep

```bash
# Run with security rules
semgrep --config=auto --json > semgrep-results.json

# Count findings
CRITICAL=$(cat semgrep-results.json | jq '[.results[] | select(.extra.severity == "ERROR")] | length')
```

### Bandit (Python)

```bash
bandit -r . -f json -o bandit-report.json

HIGH=$(cat bandit-report.json | jq '[.results[] | select(.issue_severity == "HIGH")] | length')
```

## Secret Detection

```bash
# TruffleHog
trufflehog git file://. --json > secrets-scan.json

# Gitleaks
gitleaks detect --source . --report-format json

# Check results
SECRET_COUNT=$(cat secrets-scan.json | jq '. | length')
if [ "$SECRET_COUNT" -gt 0 ]; then
  echo "🚨 $SECRET_COUNT secrets detected!"
fi
```

## Container Scanning

```bash
# Trivy
trivy image myapp:latest --format json > trivy-scan.json

CRITICAL=$(cat trivy-scan.json | jq '[.Results[].Vulnerabilities[]? | select(.Severity == "CRITICAL")] | length')
```

## Pre-commit Hooks (2026 Best Practice)

Shift-left security by catching issues before commit:

```yaml
# .pre-commit-config.yaml
repos:
  # Secret detection - MUST HAVE
  - repo: https://github.com/gitleaks/gitleaks
    rev: v8.18.0
    hooks:
      - id: gitleaks

  # Python security
  - repo: https://github.com/PyCQA/bandit
    rev: 1.7.7
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml", "-r", "."]
        exclude: ^tests/

  # Semgrep for SAST
  - repo: https://github.com/semgrep/semgrep
    rev: v1.52.0
    hooks:
      - id: semgrep
        args: ["--config", "auto", "--error"]

  # Detect AWS credentials, private keys
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ["--baseline", ".secrets.baseline"]
```

```bash
# Install and setup
pip install pre-commit
pre-commit install

# Run on all files (first time)
pre-commit run --all-files

# Update hooks to latest versions
pre-commit autoupdate
```

**Baseline for detect-secrets (ignore false positives):**
```bash
# Generate baseline
detect-secrets scan > .secrets.baseline

# Audit false positives
detect-secrets audit .secrets.baseline
```

## CI Integration

```yaml
# GitHub Actions
- name: Security scan
  run: |
    npm audit --json > audit.json
    CRITICAL=$(jq '.metadata.vulnerabilities.critical' audit.json)
    if [ "$CRITICAL" -gt 0 ]; then
      echo "::error::Critical vulnerabilities found"
      exit 1
    fi
```

## Escalation Thresholds

| Severity | Threshold | Action |
|----------|-----------|--------|
| Critical | Any | BLOCK |
| High | > 5 | BLOCK |
| Moderate | > 20 | WARNING |
| Low | > 50 | WARNING |

## Evidence Recording

```typescript
context.quality_evidence.security_scan = {
  executed: true,
  tool: 'npm audit',
  critical: 2,
  high: 5,
  moderate: 10,
  timestamp: new Date().toISOString()
};
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| JS dependencies | npm audit |
| Python dependencies | pip-audit |
| Code analysis | Semgrep |
| Secrets | TruffleHog or Gitleaks |
| Pre-commit | gitleaks + detect-secrets |
| Shift-left | Always use pre-commit hooks |

## Common Mistakes

- Ignoring audit warnings
- No CI integration
- Not blocking on critical
- Missing secret scanning

## Related Skills

- `owasp-top-10` - Vulnerability context
- `devops-deployment` - CI/CD integration
- `code-review-playbook` - Review process

## Capability Details

### dependency-scanning
**Keywords:** npm audit, pip-audit, dependency, vulnerability
**Solves:**
- Scan npm dependencies
- Audit Python packages
- Find vulnerable dependencies

### secret-detection
**Keywords:** secret, credential, api key, trufflehog, gitleaks
**Solves:**
- Detect secrets in code
- Scan for API keys
- Find exposed credentials

### api-security-audit
**Keywords:** api, audit, security, example
**Solves:**
- API security audit example
- Security review checklist
- Real audit walkthrough

### audit-template
**Keywords:** template, audit, report, security
**Solves:**
- Security audit template
- Audit report structure
- Copy-paste audit format
