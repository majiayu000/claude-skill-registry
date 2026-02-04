---
name: security-scanner
description: Perform security scanning, vulnerability assessment, and code analysis. Use tools like Trivy, Snyk, OWASP ZAP, and static analyzers to identify security issues. Use when auditing container images, scanning dependencies, performing SAST/DAST, or hardening systems. Triggers on security scan, vulnerability, trivy, snyk, owasp, sast, dast, dependency check, container security.
---

# Security Scanner & Vulnerability Assessment

Expert guidance for security scanning and vulnerability management.

## Triggers

Use this skill when:
- Scanning container images for vulnerabilities
- Checking dependencies for security issues
- Performing static application security testing (SAST)
- Performing dynamic application security testing (DAST)
- Auditing infrastructure security
- Running compliance checks
- Keywords: trivy, snyk, owasp zap, semgrep, bandit, security audit, vulnerability scan, CVE

## When to Use This Skill

- Container image vulnerability scanning
- Dependency vulnerability checking
- Static application security testing (SAST)
- Dynamic application security testing (DAST)
- Infrastructure security auditing
- Compliance checking

---

## Container Scanning (Trivy)

### Installation

```bash
# Linux
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin

# macOS
brew install trivy

# Docker
docker pull aquasec/trivy
```

### Image Scanning

```bash
# Scan container image
trivy image nginx:latest

# Scan with severity filter
trivy image --severity HIGH,CRITICAL nginx:latest

# Scan and fail on vulnerabilities
trivy image --exit-code 1 --severity CRITICAL nginx:latest

# Output formats
trivy image -f json -o results.json nginx:latest
trivy image -f table nginx:latest
trivy image -f sarif -o results.sarif nginx:latest

# Scan local image
trivy image --input image.tar

# Ignore unfixed vulnerabilities
trivy image --ignore-unfixed nginx:latest

# Scan specific types
trivy image --scanners vuln,secret,misconfig nginx:latest
```

### Filesystem & Repository Scanning

```bash
# Scan filesystem
trivy fs /path/to/project

# Scan git repository
trivy repo https://github.com/user/repo

# Scan for secrets
trivy fs --scanners secret /path/to/project

# Scan IaC files
trivy config /path/to/terraform
trivy config --severity HIGH,CRITICAL .

# Scan Kubernetes manifests
trivy k8s --report summary cluster
```

### Trivy Configuration

```yaml
# trivy.yaml
severity:
  - HIGH
  - CRITICAL

ignorefile: .trivyignore
cache-dir: /tmp/trivy

db:
  skip-update: false

scan:
  scanners:
    - vuln
    - secret
    - misconfig
```

```bash
# .trivyignore
# Ignore specific CVEs
CVE-2021-44228
CVE-2022-12345

# Ignore by package
npm:lodash
```

---

## Dependency Scanning

### Snyk

```bash
# Install
npm install -g snyk

# Authenticate
snyk auth

# Test dependencies
snyk test

# Test specific manifest
snyk test --file=package.json
snyk test --file=requirements.txt
snyk test --file=go.mod

# Monitor project (continuous scanning)
snyk monitor

# Fix vulnerabilities
snyk fix

# Output formats
snyk test --json > results.json
snyk test --sarif > results.sarif
```

### npm audit

```bash
# Run audit
npm audit

# JSON output
npm audit --json

# Fix automatically
npm audit fix

# Fix with breaking changes
npm audit fix --force

# Only production deps
npm audit --omit=dev
```

### pip-audit (Python)

```bash
# Install
pip install pip-audit

# Scan installed packages
pip-audit

# Scan requirements file
pip-audit -r requirements.txt

# Output formats
pip-audit -f json
pip-audit -f cyclonedx-json

# Fix vulnerabilities
pip-audit --fix
```

### Safety (Python)

```bash
# Install
pip install safety

# Check installed packages
safety check

# Check requirements file
safety check -r requirements.txt

# JSON output
safety check --json

# Ignore specific vulnerabilities
safety check --ignore 12345
```

---

## OWASP Dependency-Check

```bash
# Docker
docker run --rm \
  -v $(pwd):/src \
  -v $(pwd)/report:/report \
  owasp/dependency-check \
  --scan /src \
  --format HTML \
  --out /report

# Output formats
--format HTML
--format JSON
--format XML
--format SARIF
--format CSV

# Fail on CVSS score
--failOnCVSS 7

# Suppress false positives
--suppression suppression.xml
```

```xml
<!-- suppression.xml -->
<?xml version="1.0" encoding="UTF-8"?>
<suppressions xmlns="https://jeremylong.github.io/DependencyCheck/dependency-suppression.1.3.xsd">
   <suppress>
      <notes>False positive</notes>
      <cve>CVE-2021-12345</cve>
   </suppress>
   <suppress>
      <notes>Package not used</notes>
      <packageUrl regex="true">^pkg:npm/example@.*$</packageUrl>
      <cpe>cpe:/a:example:library</cpe>
   </suppress>
</suppressions>
```

---

## Static Analysis (SAST)

### Semgrep

```bash
# Install
pip install semgrep

# Run with default rules
semgrep --config auto .

# OWASP rules
semgrep --config p/owasp-top-ten .

# Language-specific
semgrep --config p/python .
semgrep --config p/javascript .
semgrep --config p/golang .

# Output formats
semgrep --json -o results.json .
semgrep --sarif -o results.sarif .

# CI mode (fails on findings)
semgrep --config auto --error .
```

### Custom Semgrep Rules

```yaml
# .semgrep.yml
rules:
  - id: hardcoded-password
    patterns:
      - pattern: password = "..."
    message: Hardcoded password detected
    languages: [python]
    severity: ERROR

  - id: sql-injection
    patterns:
      - pattern: |
          cursor.execute($QUERY % ...)
    message: Potential SQL injection
    languages: [python]
    severity: ERROR
```

### Bandit (Python)

```bash
# Install
pip install bandit

# Scan directory
bandit -r /path/to/code

# Specific severity
bandit -r . -ll  # Medium and higher
bandit -r . -lll # High only

# Output formats
bandit -r . -f json -o results.json
bandit -r . -f sarif -o results.sarif

# Exclude tests
bandit -r . --exclude tests/

# Skip specific checks
bandit -r . -s B101,B102
```

### ESLint Security (JavaScript)

```bash
# Install plugin
npm install --save-dev eslint-plugin-security
```

```javascript
// .eslintrc.js
module.exports = {
  plugins: ['security'],
  extends: ['plugin:security/recommended'],
  rules: {
    'security/detect-object-injection': 'warn',
    'security/detect-non-literal-fs-filename': 'error',
    'security/detect-eval-with-expression': 'error'
  }
};
```

### GoSec (Go)

```bash
# Install
go install github.com/securego/gosec/v2/cmd/gosec@latest

# Scan
gosec ./...

# Output formats
gosec -fmt json -out results.json ./...
gosec -fmt sarif -out results.sarif ./...

# Exclude rules
gosec -exclude G101,G102 ./...
```

---

## DAST (Dynamic Testing)

### OWASP ZAP

```bash
# Docker baseline scan
docker run -t owasp/zap2docker-stable zap-baseline.py \
  -t https://target.example.com

# Full scan
docker run -t owasp/zap2docker-stable zap-full-scan.py \
  -t https://target.example.com

# API scan
docker run -t owasp/zap2docker-stable zap-api-scan.py \
  -t https://api.example.com/openapi.json \
  -f openapi

# With report
docker run -v $(pwd):/zap/wrk:rw \
  owasp/zap2docker-stable zap-baseline.py \
  -t https://target.example.com \
  -r report.html
```

### Nuclei

```bash
# Install
go install -v github.com/projectdiscovery/nuclei/v3/cmd/nuclei@latest

# Update templates
nuclei -ut

# Basic scan
nuclei -u https://target.example.com

# Specific templates
nuclei -u https://target.example.com -t cves/
nuclei -u https://target.example.com -t exposures/

# Severity filter
nuclei -u https://target.example.com -s critical,high

# Output formats
nuclei -u https://target.example.com -j -o results.json
nuclei -u https://target.example.com -me output/
```

---

## Infrastructure Scanning

### Checkov (IaC Security)

```bash
# Install
pip install checkov

# Scan Terraform
checkov -d /path/to/terraform

# Scan Kubernetes
checkov -d /path/to/k8s/manifests

# Scan Docker
checkov -f Dockerfile

# Output formats
checkov -d . -o json > results.json
checkov -d . -o sarif > results.sarif

# Skip checks
checkov -d . --skip-check CKV_AWS_1,CKV_AWS_2

# Soft fail (exit 0)
checkov -d . --soft-fail
```

### tfsec (Terraform)

```bash
# Install
brew install tfsec

# Scan
tfsec /path/to/terraform

# Severity filter
tfsec --minimum-severity HIGH .

# Output formats
tfsec . --format json > results.json
tfsec . --format sarif > results.sarif

# Exclude checks
tfsec . --exclude-downloaded-modules
```

### kube-bench (Kubernetes CIS)

```bash
# Run on cluster
kubectl apply -f https://raw.githubusercontent.com/aquasecurity/kube-bench/main/job.yaml

# Docker
docker run --pid=host -v /etc:/etc:ro \
  -v /var:/var:ro \
  aquasec/kube-bench

# Specific benchmark
docker run aquasec/kube-bench run --targets master
docker run aquasec/kube-bench run --targets node
```

---

## CI/CD Integration

### GitHub Actions

```yaml
name: Security Scan

on: [push, pull_request]

jobs:
  trivy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: 'fs'
          scan-ref: '.'
          severity: 'CRITICAL,HIGH'
          exit-code: '1'

  semgrep:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Semgrep
        uses: returntocorp/semgrep-action@v1
        with:
          config: p/default

  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Snyk test
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

### GitLab CI

```yaml
include:
  - template: Security/SAST.gitlab-ci.yml
  - template: Security/Dependency-Scanning.gitlab-ci.yml
  - template: Security/Container-Scanning.gitlab-ci.yml

trivy:
  stage: test
  image:
    name: aquasec/trivy
    entrypoint: [""]
  script:
    - trivy fs --exit-code 1 --severity HIGH,CRITICAL .
  allow_failure: true
```

---

## Reporting

### SARIF Format

```bash
# Convert to SARIF for GitHub Security tab
trivy image -f sarif -o results.sarif nginx:latest
semgrep --sarif -o results.sarif .
bandit -r . -f sarif -o results.sarif

# Upload to GitHub
# Uses GitHub Advanced Security
```

### HTML Reports

```bash
# Trivy HTML template
trivy image --format template \
  --template "@contrib/html.tpl" \
  -o report.html nginx:latest

# ZAP HTML report
zap-baseline.py -t https://target.com -r report.html
```

---

## Security Checklist

### Code Level

- [ ] No hardcoded secrets or credentials
- [ ] Input validation on all user inputs
- [ ] Output encoding to prevent XSS
- [ ] Parameterized queries (no SQL injection)
- [ ] Secure password hashing (bcrypt, argon2)
- [ ] CSRF protection on state-changing requests
- [ ] Proper error handling (no stack traces)

### Dependency Level

- [ ] No known vulnerable dependencies
- [ ] Lock files committed (package-lock.json)
- [ ] Regular dependency updates
- [ ] License compliance checked

### Infrastructure Level

- [ ] Container images scanned
- [ ] IaC security checked
- [ ] Secrets in secret manager (not env vars)
- [ ] Network policies defined
- [ ] RBAC properly configured

### Runtime Level

- [ ] TLS/HTTPS everywhere
- [ ] Security headers configured
- [ ] Rate limiting enabled
- [ ] Logging and monitoring active
- [ ] Incident response plan documented

---

## Best Practices

1. **Scan in CI/CD** - Automate scanning in pipelines
2. **Block on critical** - Fail builds on critical vulnerabilities
3. **Update regularly** - Keep vulnerability databases current
4. **Use multiple tools** - Different tools catch different issues
5. **Triage findings** - Review and prioritize vulnerabilities
6. **Track over time** - Monitor security posture trends
7. **Integrate with ticketing** - Create issues for findings
8. **Document exceptions** - Record accepted risks
9. **Scan early** - Shift security left in SDLC
10. **Layer defenses** - Combine SAST, DAST, and SCA
