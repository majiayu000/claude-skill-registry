---
name: dependency-audit
description: Provides dependency management and supply chain security practices for auditing vulnerabilities, checking licenses, assessing dependency health, and managing upgrades safely. Use when auditing packages, reviewing security, managing dependencies, or when user mentions 'audit', 'vulnerability', 'dependency', 'supply chain', 'npm audit', 'license', 'bundle size'.
---

# Dependency Audit

Read-only analysis patterns for dependency security, license compliance, and health assessment. This skill does NOT auto-upgrade packages -- it helps you understand your dependency landscape and make informed decisions.

## Security-First Principles

| Principle | Practice |
|-----------|----------|
| Audit before merge | Run security checks in CI on every PR |
| Understand before upgrading | Read changelogs, check breaking changes |
| Never blindly force-fix | `npm audit fix --force` can introduce breaking changes |
| Pin production dependencies | Use exact versions or lock files |
| Verify publisher identity | Check package ownership, download counts, repo activity |

## Security Audit Workflow

### Step 1: Run the Audit

```bash
# npm (built-in)
npm audit

# npm -- JSON output for parsing
npm audit --json

# Yarn
yarn audit

# pnpm
pnpm audit
```

### Step 2: Read the Report

```
# Example npm audit output
┌───────────────┬──────────────────────────────────────────────┐
│ Severity      │ high                                         │
├───────────────┼──────────────────────────────────────────────┤
│ Package       │ lodash                                       │
│ Dependency of │ my-library                                   │
│ Path          │ my-library > lodash                          │
│ More info     │ https://github.com/advisories/GHSA-xxxx-xxxx │
└───────────────┴──────────────────────────────────────────────┘
```

### Step 3: Assess Each Vulnerability

| Severity | CVSS Score | Action |
|----------|-----------|--------|
| Critical | 9.0-10.0 | Fix immediately, block deployment |
| High | 7.0-8.9 | Fix within 24 hours |
| Moderate | 4.0-6.9 | Fix within 1 week, assess exploitability |
| Low | 0.1-3.9 | Track, fix in next maintenance window |
| Info | 0 | Informational, no action required |

### Step 4: Determine Fix Strategy

```bash
# SAFE: See what non-breaking fixes are available
npm audit fix --dry-run

# SAFE: Apply only semver-compatible fixes
npm audit fix

# DANGEROUS: Never run without understanding consequences
# npm audit fix --force    <-- CAN INTRODUCE BREAKING CHANGES

# INVESTIGATE: When audit fix doesn't resolve
npm ls <vulnerable-package>          # See dependency tree
npm explain <vulnerable-package>     # See why it's installed
```

### Step 5: Handle Unresolvable Vulnerabilities

When a vulnerability exists in a transitive dependency with no fix available:

```bash
# Check if the vulnerable code path is actually used
# Read the advisory -- is it relevant to your usage?

# Option A: Override the transitive dependency (npm)
# In package.json:
{
  "overrides": {
    "vulnerable-package": ">=fixed-version"
  }
}

# Option B: Override the transitive dependency (yarn)
# In package.json:
{
  "resolutions": {
    "vulnerable-package": ">=fixed-version"
  }
}

# Option C: Exclude from audit (document why)
# Create .nsprc or use npm audit --omit=dev for dev-only deps
```

## Third-Party Scanning Tools

| Tool | Type | Best For |
|------|------|----------|
| `npm audit` | Built-in | Quick check, CI integration |
| Snyk | SaaS + CLI | Deep analysis, fix PRs, monitoring |
| Socket.dev | SaaS + CLI | Supply chain attack detection |
| Dependabot | GitHub native | Automated update PRs |
| Renovate | Self-hosted/SaaS | Highly configurable update PRs |
| OSV-Scanner | CLI | Google's vulnerability database |

### Snyk CLI Usage

```bash
# Install
npm install -g snyk

# Authenticate
snyk auth

# Test for vulnerabilities (read-only)
snyk test

# Monitor project (sends to dashboard)
snyk monitor

# Test a specific package before installing
snyk test <package-name>
```

### OSV-Scanner Usage

```bash
# Install
go install github.com/google/osv-scanner/cmd/osv-scanner@latest

# Scan lock file
osv-scanner --lockfile=package-lock.json

# Scan entire directory
osv-scanner -r .
```

## License Compatibility

### Common License Types

| License | Type | Can Use In Commercial | Must Open Source Your Code | Must Include License |
|---------|------|----------------------|--------------------------|---------------------|
| MIT | Permissive | Yes | No | Yes |
| Apache-2.0 | Permissive | Yes | No | Yes (+ NOTICE file) |
| BSD-2-Clause | Permissive | Yes | No | Yes |
| BSD-3-Clause | Permissive | Yes | No | Yes |
| ISC | Permissive | Yes | No | Yes |
| GPL-2.0 | Copyleft | Yes | Yes (if distributed) | Yes |
| GPL-3.0 | Copyleft | Yes | Yes (if distributed) | Yes |
| LGPL-2.1 | Weak Copyleft | Yes | Only modifications to LGPL code | Yes |
| AGPL-3.0 | Strong Copyleft | Yes | Yes (even for network use) | Yes |
| MPL-2.0 | Weak Copyleft | Yes | Only modified MPL files | Yes |
| Unlicense | Public Domain | Yes | No | No |
| SSPL | Source Available | Check terms | Yes (broad scope) | Yes |
| BSL | Source Available | After change date | Before change date, restricted | Yes |

### Compatibility Matrix (Can A Include B?)

| Your Project | MIT | Apache-2.0 | GPL-2.0 | GPL-3.0 | AGPL-3.0 |
|-------------|-----|-----------|---------|---------|----------|
| MIT | Yes | Yes | No | No | No |
| Apache-2.0 | Yes | Yes | No | No | No |
| GPL-2.0 | Yes | No | Yes | No | No |
| GPL-3.0 | Yes | Yes | Yes | Yes | No |
| AGPL-3.0 | Yes | Yes | Yes | Yes | Yes |

### Checking Licenses

```bash
# List all dependency licenses
npx license-checker --summary

# Check for problematic licenses
npx license-checker --failOn "GPL-2.0;GPL-3.0;AGPL-3.0"

# Export full report
npx license-checker --csv --out licenses.csv

# Production only (skip devDependencies)
npx license-checker --production --summary
```

### CI License Check

```yaml
# GitHub Actions step
- name: Check licenses
  run: |
    npx license-checker --production \
      --failOn "GPL-2.0;GPL-3.0;AGPL-3.0;SSPL-1.0" \
      --excludePackages "known-exception@1.0.0"
```

## Dependency Health Indicators

### Red Flags

| Indicator | Risk | Check |
|-----------|------|-------|
| No updates in 2+ years | Unmaintained, unpatched vulns | `npm view <pkg> time` |
| Single maintainer | Bus factor of 1 | Check GitHub contributors |
| No tests or CI | Quality unknown | Check repo for test config |
| Frequent ownership changes | Possible supply chain risk | Check npm ownership history |
| Typosquat name | Malicious package | Verify exact package name |
| Post-install scripts | Can execute arbitrary code | Check `scripts.postinstall` |
| Excessive permissions | Over-scoped access | Review package contents |
| Many open security issues | Known vulnerabilities | Check GitHub issues/advisories |

### Health Check Commands

```bash
# View package metadata
npm view <package-name>

# Check when last published
npm view <package-name> time --json | jq 'to_entries | sort_by(.value) | last'

# See who maintains it
npm view <package-name> maintainers

# Check download counts (popularity signal)
npm view <package-name> --json | jq '.dist-tags, .versions | length'

# List all postinstall scripts in dependencies
npm ls --json | jq '.. | .scripts?.postinstall? // empty'

# Check package size before installing
npx package-phobia <package-name>
```

### Before Adding a New Dependency

Ask these questions before `npm install`:

- [ ] Is this package actively maintained? (Commits in last 6 months)
- [ ] Does it have more than one maintainer?
- [ ] Are there open, unresolved security issues?
- [ ] Is the license compatible with my project?
- [ ] What is the install size and bundle size impact?
- [ ] Does it have post-install scripts? Are they necessary?
- [ ] Could I implement this functionality in <50 lines?
- [ ] Is this a direct dependency or could it be a devDependency?

## Safe Upgrade Strategy

### The Read-Analyze-Test-Upgrade Cycle

Never upgrade blindly. Follow this cycle for each upgrade.

**Step 1: Identify Available Updates**

```bash
# See what's outdated (read-only)
npm outdated

# More detail
npm outdated --long

# Output:
# Package    Current  Wanted  Latest  Location
# express    4.18.2   4.18.3  5.0.0   my-app
# lodash     4.17.20  4.17.21 4.17.21 my-app
```

**Step 2: Categorize Updates**

| Update Type | Version Change | Risk | Example |
|------------|---------------|------|---------|
| Patch | `x.y.Z` | Low | `4.18.2` -> `4.18.3` (bug fixes) |
| Minor | `x.Y.z` | Medium | `4.18.2` -> `4.19.0` (new features) |
| Major | `X.y.z` | High | `4.18.2` -> `5.0.0` (breaking changes) |

**Step 3: Read Changelogs**

```bash
# Check the changelog before upgrading
npm view <package-name> repository.url
# Then visit the repo and read CHANGELOG.md or Releases
```

**Step 4: Upgrade in Isolation**

```bash
# Upgrade one package at a time
npm install <package-name>@<version>

# Run tests immediately
npm test

# Check for type errors (TypeScript)
npx tsc --noEmit

# Check for lint issues
npm run lint
```

**Step 5: Verify and Commit**

```bash
# Verify the lock file changed as expected
git diff package-lock.json | head -50

# Commit the single upgrade
git add package.json package-lock.json
git commit -m "chore(deps): upgrade <package> to <version>"
```

## Lock File Hygiene

### Why Lock Files Matter

| Concern | Without Lock File | With Lock File |
|---------|------------------|---------------|
| Reproducibility | Different versions on each install | Exact same versions every time |
| Security | Can get compromised newer version | Pinned to known-good versions |
| CI reliability | "Works on my machine" | Same everywhere |
| Audit accuracy | Audit results vary | Consistent audit results |

### Lock File Rules

| Rule | Rationale |
|------|-----------|
| Always commit lock files | Ensures reproducible builds |
| Use `npm ci` in CI, not `npm install` | `ci` respects lock file exactly |
| Review lock file diffs in PRs | Catch unexpected transitive changes |
| Regenerate periodically | Clear accumulated cruft |
| Never manually edit lock files | Use npm/yarn commands instead |

```bash
# CORRECT: Clean install from lock file (CI)
npm ci

# CORRECT: Install and update lock file (development)
npm install

# WRONG: Deleting lock file to "fix" issues
# rm package-lock.json && npm install   <-- loses pinned versions
```

## Bundle Size Analysis

### Measuring Impact

```bash
# Check bundle size of a package (before installing)
npx bundlephobia <package-name>

# Analyze your bundle
npx webpack-bundle-analyzer dist/stats.json

# Check what's in node_modules
npx cost-of-modules

# Compare alternatives
npx bundlephobia lodash vs ramda vs lodash-es
```

### Size Budget Rules

| Metric | Budget | Tool |
|--------|--------|------|
| Initial JS bundle | < 200KB gzipped | Webpack/Vite analyzer |
| Single dependency | < 50KB gzipped | bundlephobia |
| Total node_modules | Monitor trend | `du -sh node_modules` |
| Install time | < 30s | `time npm ci` |

### Reducing Bundle Size

| Strategy | Example |
|----------|---------|
| Import specific functions | `import debounce from 'lodash/debounce'` not `import { debounce } from 'lodash'` |
| Use tree-shakeable packages | `lodash-es` instead of `lodash` |
| Check for smaller alternatives | `date-fns` vs `moment` (tree-shakeable) |
| Lazy load heavy dependencies | `const lib = await import('heavy-lib')` |
| Avoid duplicate packages | Check `npm ls <pkg>` for multiple versions |

## CI Integration

### Audit in CI Pipeline

```yaml
name: Dependency Audit
on:
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'
  schedule:
    # Run weekly audit on Monday mornings
    - cron: '0 8 * * 1'

jobs:
  audit:
    runs-on: ubuntu-latest
    permissions:
      contents: read
    steps:
      - uses: actions/checkout@v4

      - uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: npm

      - run: npm ci

      - name: Security audit
        run: npm audit --audit-level=high

      - name: License check
        run: npx license-checker --production --failOn "GPL-2.0;GPL-3.0;AGPL-3.0"

      - name: Check for outdated (informational)
        run: npm outdated || true
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|--------------|---------|-----|
| `npm audit fix --force` | Introduces breaking major version bumps | Use `npm audit fix` (safe) and handle majors manually |
| Ignoring audit warnings | Vulnerabilities accumulate | Triage every audit finding, document accepted risks |
| `"*"` or `""` version ranges | Installs any version, including malicious | Use exact versions or `^` ranges with lock file |
| Not committing lock file | Non-reproducible builds | Always commit `package-lock.json` / `yarn.lock` |
| Deleting lock file to fix issues | Loses all version pins | Diagnose the actual issue, regenerate carefully |
| Installing without reviewing | Supply chain attack vector | Check package health before `npm install` |
| Bulk upgrading all at once | Hard to diagnose breakage | Upgrade one package at a time, test between each |
| Running `npx` with unknown packages | Executes unreviewed code | Verify package before first `npx` usage |
| Ignoring post-install scripts | Arbitrary code execution | Review scripts, use `--ignore-scripts` when cautious |
| No CI audit step | Vulnerabilities ship to production | Add `npm audit` to CI pipeline |
| Using deprecated packages | No security patches | Find maintained alternatives |
| `devDependencies` in production | Larger attack surface, bigger image | Use `npm ci --omit=dev` for production builds |

## Quick Reference: Audit Decision Tree

```
npm audit reports vulnerability
  |
  +--> Is it in a devDependency only?
  |      YES --> Lower priority (not in production)
  |      NO  --> Continue
  |
  +--> Is there a patch/minor fix available?
  |      YES --> npm audit fix (safe)
  |      NO  --> Continue
  |
  +--> Is the vulnerable code path used in your app?
  |      NO  --> Document accepted risk, revisit monthly
  |      YES --> Continue
  |
  +--> Is there a major version fix?
  |      YES --> Read changelog, test upgrade in branch
  |      NO  --> Continue
  |
  +--> Can you use overrides/resolutions?
  |      YES --> Pin transitive dep to fixed version
  |      NO  --> Continue
  |
  +--> Find alternative package or implement inline
```
