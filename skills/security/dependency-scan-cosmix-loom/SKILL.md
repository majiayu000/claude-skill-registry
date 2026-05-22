---
name: dependency-scan
description: Scans project dependencies for known vulnerabilities, outdated packages, and license compliance issues. Supports vulnerability scanning (CVE detection), SBOM generation, license compliance checking, and supply chain security analysis across multiple ecosystems (npm, pip, cargo, go, maven, etc.). Trigger keywords: dependency scan, vulnerability, CVE, Snyk, Dependabot, Renovate, npm audit, cargo audit, pip-audit, safety, outdated packages, SBOM, software bill of materials, license compliance, supply chain, security advisory, transitive dependency, lock file.
allowed-tools: Read, Grep, Glob, Bash
---

# Dependency Scan

## Overview

This skill focuses on identifying security vulnerabilities, outdated packages, and license compliance issues in project dependencies. It covers multiple package ecosystems (JavaScript/Node.js, Python, Rust, Go, Ruby, Java, .NET, PHP) and provides remediation guidance, SBOM generation, and supply chain security analysis.

## When to Use

- Scanning dependencies for CVEs and security advisories
- Checking for outdated or unmaintained packages
- Generating Software Bill of Materials (SBOM)
- Verifying license compliance and compatibility
- Analyzing supply chain risks and transitive dependencies
- Setting up automated dependency updates (Dependabot, Renovate, Snyk)
- Investigating security alerts from GitHub/GitLab
- Auditing dependencies before production deployment

## Instructions

### 1. Identify Dependencies

- Parse manifest files (package.json, requirements.txt, etc.)
- Build complete dependency tree
- Identify direct vs transitive dependencies
- Check for phantom dependencies

### 2. Vulnerability Scanning

- Check against CVE databases
- Identify severity levels
- Find affected versions
- Check for available patches

### 3. Assess Risks

- Evaluate exploitability
- Check for active exploitation
- Assess impact on application
- Prioritize remediations

### 4. Report and Remediate

- Document all findings
- Provide upgrade paths
- Suggest alternatives
- Create remediation plan

### 5. Language-Specific Scanning

**JavaScript/Node.js:**
- Use `npm audit` or `yarn audit` for vulnerability scanning
- Check `package-lock.json` or `yarn.lock` for reproducibility
- Consider `npm-check-updates` for upgrade analysis
- Use `license-checker` for license compliance

**Python:**
- Use `pip-audit` or `safety` for CVE scanning
- Check `requirements.txt` and `Pipfile.lock`
- Use `pip-compile` with `--generate-hashes` for integrity
- Consider `pipdeptree` for dependency visualization

**Rust:**
- Use `cargo audit` for RustSec advisories
- Check `Cargo.lock` for reproducible builds
- Use `cargo outdated` for version analysis
- Consider `cargo deny` for policy enforcement

**Go:**
- Use `govulncheck` for vulnerability scanning
- Check `go.sum` for module integrity
- Use `go list -m all` to enumerate dependencies
- Consider `nancy` for OSS Index checking

### 6. SBOM Generation

Generate Software Bill of Materials for supply chain transparency:

**CycloneDX:**
- `npm install -g @cyclonedx/cyclonedx-npm && cyclonedx-npm --output-file sbom.json`
- `cargo install cargo-cyclonedx && cargo cyclonedx`
- `pip install cyclonedx-bom && cyclonedx-py`

**SPDX:**
- Use `syft` (universal tool): `syft . -o spdx-json > sbom.spdx.json`
- Use `trivy` for container images: `trivy image --format spdx-json myimage:tag`

**Purpose:** Track all components for vulnerability management, license compliance, and incident response.

### 7. License Compliance Checking

Ensure all dependencies have compatible licenses:

**Automated Tools:**
- Node.js: `npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC'`
- Rust: `cargo deny check licenses`
- Python: `pip-licenses`
- Universal: `fossology`, `scancode-toolkit`

**License Categories:**
- Permissive: MIT, Apache-2.0, BSD (generally safe)
- Weak Copyleft: MPL, LGPL (check linking requirements)
- Strong Copyleft: GPL, AGPL (may require source disclosure)
- Unknown/Missing: Investigate before use

## Best Practices

1. **Regular Scanning**: Automate daily/weekly scans
2. **Lock Files**: Use lockfiles for reproducibility
3. **Minimal Dependencies**: Only include what's needed
4. **Verify Sources**: Use trusted registries
5. **Review Updates**: Don't blindly update
6. **License Compliance**: Ensure compatible licenses
7. **SBOM**: Maintain software bill of materials

## Examples

### Example 1: Scanning Commands by Ecosystem

```bash
# JavaScript/Node.js
npm audit
npm audit --json > audit-report.json
npm outdated
npx npm-check-updates

# Python
pip-audit
safety check
pip list --outdated
pip-compile --generate-hashes

# Rust
cargo audit
cargo outdated
cargo deny check

# Go
go list -m all | nancy sleuth
govulncheck ./...

# Ruby
bundle audit
bundle outdated

# Java/Maven
mvn dependency-check:check
mvn versions:display-dependency-updates

# .NET
dotnet list package --vulnerable
dotnet list package --outdated

# PHP
composer audit
composer outdated
```

### Example 2: GitHub Actions Dependency Scanning

```yaml
name: Dependency Scanning

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: "0 6 * * *" # Daily at 6 AM

jobs:
  dependency-scan:
    runs-on: ubuntu-latest

    steps:
      - uses: actions/checkout@v4

      - name: Run Trivy vulnerability scanner
        uses: aquasecurity/trivy-action@master
        with:
          scan-type: "fs"
          scan-ref: "."
          format: "sarif"
          output: "trivy-results.sarif"
          severity: "CRITICAL,HIGH"

      - name: Upload Trivy scan results
        uses: github/codeql-action/upload-sarif@v2
        with:
          sarif_file: "trivy-results.sarif"

      - name: Setup Node.js
        uses: actions/setup-node@v4
        with:
          node-version: "20"

      - name: Run npm audit
        run: |
          npm ci
          npm audit --audit-level=high

      - name: Check for outdated packages
        run: npm outdated || true

      - name: License check
        run: npx license-checker --onlyAllow 'MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC'

  snyk-scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Run Snyk to check for vulnerabilities
        uses: snyk/actions/node@master
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
        with:
          args: --severity-threshold=high
```

### Example 3: Dependency Analysis Report Template

```markdown
# Dependency Security Report

**Generated:** 2024-01-15
**Project:** my-application
**Total Dependencies:** 245 (42 direct, 203 transitive)

## Summary

| Severity | Count | Status             |
| -------- | ----- | ------------------ |
| Critical | 2     | Action Required    |
| High     | 5     | Action Required    |
| Medium   | 12    | Review Recommended |
| Low      | 8     | Monitor            |

## Critical Vulnerabilities

### CVE-2024-1234 - Remote Code Execution in lodash

- **Package:** lodash@4.17.20
- **Severity:** Critical (CVSS 9.8)
- **Affected Versions:** < 4.17.21
- **Fixed Version:** 4.17.21
- **Path:** my-app > express > lodash
- **Description:** Prototype pollution vulnerability allowing RCE
- **Remediation:** `npm update lodash`

### CVE-2024-5678 - SQL Injection in sequelize

- **Package:** sequelize@6.28.0
- **Severity:** Critical (CVSS 9.1)
- **Affected Versions:** < 6.29.0
- **Fixed Version:** 6.29.0
- **Path:** my-app > sequelize
- **Description:** SQL injection via raw query methods
- **Remediation:** `npm update sequelize`

## License Compliance

| License      | Count | Compliance           |
| ------------ | ----- | -------------------- |
| MIT          | 180   | Approved             |
| Apache-2.0   | 45    | Approved             |
| BSD-3-Clause | 15    | Approved             |
| GPL-3.0      | 3     | Review Required      |
| Unknown      | 2     | Investigation Needed |

## Recommendations

1. **Immediate:** Update lodash and sequelize to fix critical vulnerabilities
2. **Short-term:** Review GPL-licensed dependencies for compatibility
3. **Ongoing:** Enable Dependabot/Renovate for automated updates
```

### Example 4: Renovate Configuration

```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": ["config:base", ":semanticCommits", ":preserveSemverRanges"],
  "schedule": ["before 6am on Monday"],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  },
  "packageRules": [
    {
      "matchUpdateTypes": ["major"],
      "labels": ["major-update"],
      "automerge": false
    },
    {
      "matchUpdateTypes": ["minor", "patch"],
      "matchCurrentVersion": "!/^0/",
      "automerge": true,
      "automergeType": "pr",
      "platformAutomerge": true
    },
    {
      "matchPackagePatterns": ["^@types/"],
      "automerge": true,
      "groupName": "type definitions"
    },
    {
      "matchDepTypes": ["devDependencies"],
      "automerge": true,
      "groupName": "dev dependencies"
    }
  ],
  "prConcurrentLimit": 5,
  "prHourlyLimit": 2
}
```
