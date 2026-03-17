---
name: trivy
description: >-
  Security vulnerability scanner using Trivy for container images, filesystems, and IaC.
  Blocks CRITICAL and HIGH severity vulnerabilities before commit. Triggers on "trivy",
  "vulnerability scan", "security scan", "container scan", "image scan", "sbom", "cve",
  "dependency scan", "supply chain security", "docker scan", "scan image", "scan container",
  "check vulnerabilities", "security check", "license scan", "secret scan", "misconfig scan",
  "iac scan", "terraform scan", "kubernetes scan", "helm scan", "dockerfile scan",
  "package vulnerabilities", "npm audit", "pip audit", "go mod vulnerabilities",
  "scan dependencies", "security gate", "compliance scan", "aqua trivy".
  PROACTIVE: MUST invoke before committing code with new dependencies or container images.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# ABOUTME: Security vulnerability scanning skill using Trivy for pre-commit validation
# ABOUTME: Enforces blocking of CRITICAL and HIGH severity vulnerabilities across all scan targets

# Trivy Security Scanning Skill

**Tool**: [Trivy](https://trivy.dev/)

## Overview

This skill enforces security vulnerability scanning using Trivy before code is committed.
**CRITICAL and HIGH severity vulnerabilities MUST be resolved before commit.**

## When to Use

| Trigger | Action |
|---------|--------|
| New dependency added | Scan filesystem for vulnerabilities |
| Dockerfile modified | Scan container image |
| go.mod/go.sum changed | Scan Go dependencies |
| requirements.txt/pyproject.toml changed | Scan Python dependencies |
| package.json/package-lock.json changed | Scan Node.js dependencies |
| Terraform files changed | Scan IaC misconfigurations |
| Before commit with dependency changes | **MANDATORY** full scan |

## Quick Reference

```bash
# Filesystem scan (most common)
trivy fs --severity CRITICAL,HIGH --exit-code 1 .

# Container image scan
trivy image --severity CRITICAL,HIGH --exit-code 1 IMAGE_NAME

# IaC scan (Terraform, CloudFormation, etc.)
trivy config --severity CRITICAL,HIGH --exit-code 1 .

# Generate SBOM
trivy fs --format spdx-json --output sbom.json .
```

## Severity Policy

| Severity | Action | Commit Allowed |
|----------|--------|----------------|
| CRITICAL | **BLOCK** - Must fix immediately | NO |
| HIGH | **BLOCK** - Must fix or upgrade | NO |
| MEDIUM | WARN - Review and plan remediation | YES (with warning) |
| LOW | INFO - Document in backlog | YES |

## Workflow: Pre-Commit Security Scan

### Step 1: Identify Scan Targets

Check what changed to determine scan type:

```bash
# Check for dependency file changes
git diff --cached --name-only | grep -E "(go\.(mod|sum)|requirements.*\.txt|pyproject\.toml|package.*\.json|Gemfile|Cargo\.(toml|lock)|pom\.xml|build\.gradle)"

# Check for Dockerfile changes
git diff --cached --name-only | grep -iE "(Dockerfile|\.dockerfile|docker-compose)"

# Check for IaC changes
git diff --cached --name-only | grep -E "\.(tf|hcl|yaml|yml)$"
```

### Step 2: Run Appropriate Scan

**Filesystem Scan (Dependencies)**

```bash
trivy fs \
    --severity CRITICAL,HIGH \
    --exit-code 1 \
    --ignore-unfixed \
    --format table \
    .
```

**Container Image Scan**

```bash
# Build the image first if needed
docker build -t local-scan:latest .

# Scan the image
trivy image \
    --severity CRITICAL,HIGH \
    --exit-code 1 \
    --ignore-unfixed \
    --format table \
    local-scan:latest
```

**IaC Configuration Scan**

```bash
trivy config \
    --severity CRITICAL,HIGH \
    --exit-code 1 \
    --format table \
    .
```

### Step 3: Handle Results

**If scan passes (exit code 0):**
- Proceed with commit

**If scan fails (exit code 1):**
1. Review the vulnerability report
2. Identify affected packages
3. Apply remediation (see below)
4. Re-scan to verify fix
5. Only then proceed with commit

## Remediation Strategies

### Strategy 1: Upgrade Dependency

The preferred approach; upgrade to a patched version.

```bash
# Go
go get package@latest
go mod tidy

# Python (uv)
uv pip install --upgrade package

# Python (pip)
pip install --upgrade package

# Node.js
npm update package
# or
npm install package@latest

# Rust
cargo update -p package
```

### Strategy 2: Use Trivy to Find Fixed Version

```bash
# Show which version fixes the vulnerability
trivy fs --severity CRITICAL,HIGH --format json . | jq '.Results[].Vulnerabilities[] | {pkg: .PkgName, installed: .InstalledVersion, fixed: .FixedVersion}'
```

### Strategy 3: Exclude False Positives (With Justification)

**Only when vulnerability is confirmed false positive or not applicable.**

Create `.trivyignore` file:

```
# Vulnerability ID with justification comment
# CVE-2023-XXXXX: Not applicable - we don't use affected feature (code path X)
CVE-2023-XXXXX
```

**WARNING**: Every exclusion MUST have a documented justification.

### Strategy 4: Vendor Override (Last Resort)

For transitive dependencies that cannot be directly upgraded:

```bash
# Go: Use replace directive in go.mod
replace vulnerable/package => vulnerable/package vX.Y.Z-fixed

# Node.js: Use overrides in package.json
{
  "overrides": {
    "vulnerable-package": "^X.Y.Z"
  }
}
```

## Scan Output Examples

### Clean Scan

```
2024-01-09T10:00:00.000Z  INFO  Vulnerability scanning enabled
2024-01-09T10:00:01.000Z  INFO  Detected OS: alpine
2024-01-09T10:00:02.000Z  INFO  Number of PL managers: 1
2024-01-09T10:00:03.000Z  INFO  No vulnerabilities found

Total: 0 (CRITICAL: 0, HIGH: 0)
```

### Failed Scan (Blocking)

```
package-lock.json (npm)
=======================
Total: 2 (CRITICAL: 1, HIGH: 1)

+-----------+------------------+----------+-------------------+---------------+
|  LIBRARY  | VULNERABILITY ID | SEVERITY | INSTALLED VERSION | FIXED VERSION |
+-----------+------------------+----------+-------------------+---------------+
| lodash    | CVE-2021-23337   | CRITICAL | 4.17.15           | 4.17.21       |
| minimist  | CVE-2021-44906   | HIGH     | 1.2.5             | 1.2.6         |
+-----------+------------------+----------+-------------------+---------------+
```

## Integration with Pre-Commit Hook

Add to `.pre-commit-config.yaml`:

```yaml
repos:
  - repo: local
    hooks:
      - id: trivy-fs
        name: Trivy Filesystem Scan
        entry: trivy fs --severity CRITICAL,HIGH --exit-code 1 --ignore-unfixed .
        language: system
        pass_filenames: false
        stages: [commit]
```

Or create a Git hook directly at `.git/hooks/pre-commit`:

```bash
#!/bin/bash
set -euo pipefail

echo "[SECURITY] Running Trivy vulnerability scan..."

if ! command -v trivy &> /dev/null; then
    echo "[ERROR] Trivy is not installed. Install with: brew install trivy"
    exit 1
fi

# Check for dependency file changes
DEPS_CHANGED=$(git diff --cached --name-only | grep -E "(go\.(mod|sum)|requirements.*\.txt|pyproject\.toml|package.*\.json|Gemfile|Cargo\.(toml|lock))" || true)

if [[ -n "${DEPS_CHANGED}" ]]; then
    echo "[SECURITY] Dependency files changed, scanning for vulnerabilities..."

    if ! trivy fs --severity CRITICAL,HIGH --exit-code 1 --ignore-unfixed .; then
        echo ""
        echo "=========================================="
        echo "[BLOCKED] CRITICAL or HIGH vulnerabilities found!"
        echo "Fix vulnerabilities before committing."
        echo "=========================================="
        exit 1
    fi
fi

# Check for Dockerfile changes
DOCKER_CHANGED=$(git diff --cached --name-only | grep -iE "(Dockerfile|\.dockerfile)" || true)

if [[ -n "${DOCKER_CHANGED}" ]]; then
    echo "[SECURITY] Dockerfile changed, building and scanning image..."

    # Build image for scanning (adjust tag as needed)
    docker build -t pre-commit-scan:latest . 2>/dev/null || true

    if docker image inspect pre-commit-scan:latest &>/dev/null; then
        if ! trivy image --severity CRITICAL,HIGH --exit-code 1 --ignore-unfixed pre-commit-scan:latest; then
            echo ""
            echo "=========================================="
            echo "[BLOCKED] Container image has vulnerabilities!"
            echo "Fix vulnerabilities before committing."
            echo "=========================================="
            docker rmi pre-commit-scan:latest 2>/dev/null || true
            exit 1
        fi
        docker rmi pre-commit-scan:latest 2>/dev/null || true
    fi
fi

echo "[SECURITY] Vulnerability scan passed."
```

## Advanced Options

### JSON Output for CI/CD

```bash
trivy fs \
    --severity CRITICAL,HIGH \
    --exit-code 1 \
    --format json \
    --output trivy-report.json \
    .
```

### SARIF Output for GitHub Security

```bash
trivy fs \
    --severity CRITICAL,HIGH \
    --format sarif \
    --output trivy-results.sarif \
    .
```

### Scan Specific Language

```bash
# Only scan Go dependencies
trivy fs --scanners vuln --pkg-types library --file-patterns "go.mod" .

# Only scan Python dependencies
trivy fs --scanners vuln --pkg-types library --file-patterns "requirements.txt,pyproject.toml" .
```

### Offline Scanning

```bash
# Download vulnerability database
trivy --download-db-only

# Scan offline
trivy fs --skip-update --offline-scan .
```

## Trivy Installation

```bash
# macOS
brew install trivy

# Linux (Debian/Ubuntu)
sudo apt-get install trivy

# Linux (RHEL/CentOS)
sudo yum install trivy

# Docker
docker pull aquasec/trivy

# Binary download
curl -sfL https://raw.githubusercontent.com/aquasecurity/trivy/main/contrib/install.sh | sh -s -- -b /usr/local/bin
```

## Checklist

Before committing code with dependency or container changes:

- [ ] Trivy is installed and accessible
- [ ] Ran `trivy fs --severity CRITICAL,HIGH --exit-code 1 .`
- [ ] No CRITICAL vulnerabilities present
- [ ] No HIGH vulnerabilities present (or documented exception)
- [ ] Any `.trivyignore` entries have documented justification
- [ ] Container images (if applicable) scanned and clean
- [ ] IaC configurations (if applicable) scanned and clean

## Claude Code Integration

This skill integrates with Claude Code's commit workflow. See `scm/references/commit-workflow.md` for the full workflow.

### Automatic Invocation

Claude Code automatically invokes Trivy scanning when committing changes to:

| File Pattern | Scan Type |
|--------------|-----------|
| `go.mod`, `go.sum` | `trivy fs` |
| `requirements*.txt`, `pyproject.toml` | `trivy fs` |
| `package*.json`, `yarn.lock` | `trivy fs` |
| `Dockerfile*`, `docker-compose*.yml` | `trivy config` + `trivy image` |
| `*.tf`, `*.hcl` | `trivy config` |

### Workflow Integration

```
User: "/commit-push" or "/commit-push-pr"
           │
           ▼
┌─────────────────────────────┐
│ Detect security-relevant    │
│ files in staged changes     │
└──────────────┬──────────────┘
               │
    ┌──────────┴──────────┐
    ▼                     ▼
[Triggers found]    [No triggers]
    │                     │
    ▼                     │
┌─────────────────┐       │
│ Run Trivy scans │       │
└────────┬────────┘       │
         │                │
  ┌──────┴──────┐         │
  ▼             ▼         │
[VULN]       [CLEAN]      │
  │             │         │
  ▼             └────┬────┘
┌──────────────┐     │
│ Generate     │     │
│ Remediation  │     │
│ Plan         │     │
└──────────────┘     │
                     ▼
              ┌────────────┐
              │ Proceed to │
              │ commit     │
              └────────────┘
```

### Remediation Plan Format

When vulnerabilities are found, Claude Code generates a remediation plan:

```markdown
# Vulnerability Remediation Plan

## Summary
- **Total**: X vulnerabilities (CRITICAL: Y, HIGH: Z)
- **Scan Type**: filesystem / config / image

## Findings

| Severity | Package | CVE | Installed | Fixed |
|----------|---------|-----|-----------|-------|
| CRITICAL | example | CVE-XXXX-YYYY | 1.0.0 | 1.0.1 |

## Remediation Steps

1. Upgrade `example` to version 1.0.1:
   ```bash
   npm install example@1.0.1
   ```

2. Verify fix:
   ```bash
   trivy fs --severity CRITICAL,HIGH --exit-code 1 .
   ```
```

### Related Skills

| Skill | Purpose |
|-------|---------|
| `scm/SKILL.md` | Git workflow, Conventional Commits |
| `scm/references/commit-workflow.md` | Full secure commit workflow |
| `gemini-review/SKILL.md` | Code review (after security scan) |

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `trivy: command not found` | Install Trivy: `brew install trivy` |
| Slow scan | Use `--skip-update` after initial DB download |
| False positive | Add to `.trivyignore` with justification |
| Transitive dependency | Use package manager override mechanism |
| Old vulnerability DB | Run `trivy --download-db-only` to update |

## Additional Resources

- [Trivy Documentation](https://trivy.dev/latest/)
- [Trivy GitHub](https://github.com/aquasecurity/trivy)
- [CVE Database](https://cve.mitre.org/)
- [NVD - National Vulnerability Database](https://nvd.nist.gov/)
