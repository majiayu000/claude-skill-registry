---
name: dependency-scan
description: 'Scans project dependencies for known vulnerabilities, outdated packages,
  and license compliance issues. Trigger keywords: dependency, vulnerability, CVE,
  npm audit, outdated, license, supply chain, SB'
---

---
name: dependency-scan
description: Scans project dependencies for known vulnerabilities, outdated packages, and license compliance issues. Trigger keywords: dependency, vulnerability, CVE, npm audit, outdated, license, supply chain, SBOM.
allowed-tools: Read, Grep, Glob, Bash
---

# Dependency Scan

## Overview

This skill focuses on identifying security vulnerabilities, outdated packages, and license compliance issues in project dependencies. It covers multiple package ecosystems and provides remediation guidance.

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
