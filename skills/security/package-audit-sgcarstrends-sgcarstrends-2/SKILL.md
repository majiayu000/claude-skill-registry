---
name: package-audit
description: Scan for security vulnerabilities using pnpm audit, Snyk, and automated tools. Use when checking security, before deployments, or resolving CVEs.
allowed-tools: Read, Edit, Write, Bash, Grep
---

# Package Audit Skill

This skill helps you scan for and fix security vulnerabilities in npm dependencies.

## When to Use This Skill

- Scanning for security vulnerabilities
- Before production deployments
- Resolving CVE alerts
- Regular security audits
- Dependency health checks
- Compliance requirements
- Pre-commit security checks

## Security Audit Tools

### pnpm audit

Built-in vulnerability scanner:

```bash
# Run audit
pnpm audit

# Output example:
# ┌───────────────┬──────────────────────────────────────────────────────────────┐
# │ moderate      │ Prototype Pollution in lodash                                │
# ├───────────────┼──────────────────────────────────────────────────────────────┤
# │ Package       │ lodash                                                       │
# ├───────────────┼──────────────────────────────────────────────────────────────┤
# │ Vulnerable    │ <4.17.21                                                     │
# ├───────────────┼──────────────────────────────────────────────────────────────┤
# │ Patched in    │ >=4.17.21                                                    │
# ├───────────────┼──────────────────────────────────────────────────────────────┤
# │ Path          │ lodash                                                       │
# └───────────────┴──────────────────────────────────────────────────────────────┘
```

### Snyk

Advanced vulnerability scanning:

```bash
# Install Snyk CLI
pnpm add -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities
snyk test

# Monitor project
snyk monitor

# Fix vulnerabilities
snyk fix
```

## Running Audits

### Basic Audit

```bash
# Audit all packages
pnpm audit

# Audit specific workspace
pnpm -F @sgcarstrends/api audit

# Audit production dependencies only
pnpm audit --prod

# Get JSON output
pnpm audit --json > audit-report.json
```

### Severity Levels

```bash
# Only show high/critical
pnpm audit --audit-level=high

# Audit levels:
# - info
# - low
# - moderate
# - high
# - critical
```

### Automated Fix

```bash
# Automatically fix vulnerabilities
pnpm audit --fix

# Dry run (preview fixes)
pnpm audit --fix --dry-run
```

## Understanding Audit Results

### Vulnerability Report

```
┌───────────────┬──────────────────────────────────────────────────────────────┐
│ High          │ Regular Expression Denial of Service                        │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Package       │ semver                                                       │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Vulnerable    │ <5.7.2 || >=6.0.0 <6.3.1 || >=7.0.0 <7.5.2                  │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ Patched in    │ >=5.7.2 <6.0.0 || >=6.3.1 <7.0.0 || >=7.5.2                 │
├───────────────┼──────────────────────────────────────────────────────────────┤
│ More info     │ https://github.com/advisories/GHSA-c2qf-rxjj-qqgw           │
└───────────────┴──────────────────────────────────────────────────────────────┘
```

**Key Information:**
- **Severity**: critical, high, moderate, low, info
- **Package**: Affected package name
- **Vulnerable**: Vulnerable version range
- **Patched in**: Fixed version range
- **Path**: Dependency path (direct or transitive)

### JSON Report Analysis

```bash
# Generate JSON report
pnpm audit --json > audit.json

# Parse with jq
cat audit.json | jq '.vulnerabilities | length'
cat audit.json | jq '.vulnerabilities | group_by(.severity)'

# Filter critical vulnerabilities
cat audit.json | jq '.vulnerabilities[] | select(.severity == "critical")'
```

## Fixing Vulnerabilities

### Direct Dependencies

```bash
# Step 1: Identify vulnerable package
pnpm audit

# Step 2: Check available versions
pnpm view package-name versions

# Step 3: Update catalog
# pnpm-workspace.yaml
catalog:
  lodash: ^4.17.21  # Updated from ^4.17.19

# Step 4: Install
pnpm install

# Step 5: Verify fix
pnpm audit
```

### Transitive Dependencies

```bash
# Step 1: Identify dependency chain
pnpm why vulnerable-package

# Output:
# parent-package 1.0.0
# └─┬ intermediate-package 2.0.0
#   └── vulnerable-package 3.0.0

# Step 2: Update parent package
catalog:
  parent-package: ^2.0.0  # Newer version with fixed dependency

# Step 3: Or use overrides (last resort)
{
  "pnpm": {
    "overrides": {
      "vulnerable-package": "^3.1.0"
    }
  }
}
```

### Using Overrides

```json
// package.json
{
  "pnpm": {
    "overrides": {
      // Fix specific vulnerability
      "lodash": "^4.17.21",

      // Fix across all dependencies
      "semver@<7.5.2": "^7.5.2",

      // Fix in specific dependency
      "some-package>vulnerable-dep": "^2.0.0"
    }
  }
}
```

## Snyk Integration

### Setup

```bash
# Install Snyk
pnpm add -g snyk

# Authenticate
snyk auth

# Test project
snyk test

# Monitor for new vulnerabilities
snyk monitor
```

### Snyk Commands

```bash
# Test for vulnerabilities
snyk test

# Test with severity threshold
snyk test --severity-threshold=high

# Test specific file
snyk test --file=package.json

# Ignore specific vulnerabilities
snyk ignore --id=SNYK-JS-LODASH-1018905

# Generate HTML report
snyk test --json | snyk-to-html -o snyk-report.html
```

### Snyk Configuration

```yaml
# .snyk
version: v1.25.0
ignore:
  # Ignore low severity
  'SNYK-JS-LODASH-1018905':
    - '*':
        reason: Low severity, no fix available
        expires: 2024-12-31

  # Ignore specific path
  'SNYK-JS-AXIOS-1234567':
    - 'dev-dependency > axios':
        reason: Dev dependency only
        expires: never
```

## CI Integration

### GitHub Actions

```yaml
# .github/workflows/security.yml
name: Security Audit

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  audit:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install
      - run: pnpm audit --audit-level=moderate

      # Fail on high/critical vulnerabilities
      - name: Check for high/critical vulnerabilities
        run: |
          AUDIT_OUTPUT=$(pnpm audit --json)
          HIGH=$(echo $AUDIT_OUTPUT | jq '.metadata.vulnerabilities.high // 0')
          CRITICAL=$(echo $AUDIT_OUTPUT | jq '.metadata.vulnerabilities.critical // 0')

          if [ $HIGH -gt 0 ] || [ $CRITICAL -gt 0 ]; then
            echo "High or critical vulnerabilities found!"
            exit 1
          fi

  snyk:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: snyk/actions/setup@master
      - uses: pnpm/action-setup@v2
      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: "pnpm"

      - run: pnpm install

      - name: Snyk test
        run: snyk test --severity-threshold=high
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}

      - name: Snyk monitor
        run: snyk monitor
        env:
          SNYK_TOKEN: ${{ secrets.SNYK_TOKEN }}
```

## Automated Dependency Updates

### Dependabot

```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: "npm"
    directory: "/"
    schedule:
      interval: "weekly"
    open-pull-requests-limit: 10

    # Auto-merge security patches
    groups:
      security:
        patterns:
          - "*"
        update-types:
          - "patch"

    # Ignore major versions
    ignore:
      - dependency-name: "*"
        update-types: ["version-update:semver-major"]
```

### Renovate

```json
// renovate.json
{
  "extends": ["config:base"],
  "vulnerabilityAlerts": {
    "enabled": true,
    "automerge": true
  },
  "packageRules": [
    {
      "matchUpdateTypes": ["patch"],
      "matchCurrentVersion": "!/^0/",
      "automerge": true,
      "automergeType": "branch"
    },
    {
      "matchDepTypes": ["devDependencies"],
      "matchUpdateTypes": ["minor", "patch"],
      "automerge": true
    }
  ]
}
```

## Best Practices

### 1. Regular Audits

```bash
# ❌ Only audit before deployment
pnpm audit  # Once every few months

# ✅ Regular schedule
# - Daily: Automated CI checks
# - Weekly: Manual review
# - Before deployment: Final check
```

### 2. Prioritize Fixes

```bash
# ❌ Try to fix everything at once
pnpm audit --fix

# ✅ Prioritize by severity
# 1. Critical: Fix immediately
# 2. High: Fix within 1 week
# 3. Moderate: Fix within 1 month
# 4. Low: Fix when convenient
```

### 3. Verify Fixes

```bash
# ❌ Just update and deploy
pnpm audit --fix
git push

# ✅ Test after fixing
pnpm audit --fix
pnpm test          # Run tests
pnpm build         # Build check
pnpm dev           # Manual testing
git commit && git push
```

### 4. Document Decisions

```yaml
# .snyk
ignore:
  'SNYK-JS-LODASH-1018905':
    - '*':
        reason: >
          Low severity prototype pollution.
          Package only used in dev scripts.
          No fix available yet.
          Monitoring for updates.
        expires: 2024-12-31
        created: 2024-01-15
```

## Handling Common Scenarios

### No Fix Available

```bash
# Issue: Vulnerability with no fix

# Options:
# 1. Wait for fix (monitor regularly)
snyk monitor

# 2. Find alternative package
pnpm remove vulnerable-package
pnpm add alternative-package

# 3. Accept risk (document decision)
# Add to .snyk with expiration date
```

### Breaking Changes in Fix

```bash
# Issue: Fix requires major version upgrade

# Solution:
# 1. Review breaking changes
pnpm view package-name changelog

# 2. Create migration branch
git checkout -b upgrade/package-name

# 3. Update and test
catalog:
  package-name: ^2.0.0  # Major version
pnpm install
pnpm test

# 4. Fix breaking changes
# 5. Commit and merge
```

### False Positives

```bash
# Issue: Vulnerability doesn't affect your code

# Solution: Ignore with justification
# .snyk
ignore:
  'SNYK-ID':
    - 'package-name':
        reason: >
          False positive.
          Vulnerable code path not used in our application.
          Only affects feature X which we don't use.
        expires: never
```

## Security Audit Checklist

- [ ] Run `pnpm audit` regularly
- [ ] Fix critical and high vulnerabilities immediately
- [ ] Monitor for new vulnerabilities (Snyk/Dependabot)
- [ ] Document ignored vulnerabilities
- [ ] Review security patches before applying
- [ ] Test thoroughly after fixes
- [ ] Keep audit logs for compliance
- [ ] Update security policy as needed

## References

- pnpm Audit: https://pnpm.io/cli/audit
- Snyk: https://snyk.io
- npm Security Advisories: https://github.com/advisories
- OWASP Dependency Check: https://owasp.org/www-project-dependency-check
- Related files:
  - `.snyk` - Snyk configuration
  - `.github/dependabot.yml` - Dependabot config
  - Root CLAUDE.md - Security guidelines

## Best Practices Summary

1. **Regular Audits**: Run audits daily in CI, weekly manually
2. **Prioritize Severity**: Fix critical/high first, then moderate/low
3. **Automate Security**: Use Dependabot or Renovate
4. **Test Fixes**: Always test after applying security patches
5. **Document Decisions**: Explain ignored vulnerabilities
6. **Monitor Continuously**: Use Snyk monitor for ongoing tracking
7. **Review Dependencies**: Regularly review and remove unused packages
8. **Stay Informed**: Subscribe to security advisories for key packages
