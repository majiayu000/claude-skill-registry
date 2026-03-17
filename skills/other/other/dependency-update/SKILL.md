---
name: dependency-update
description: Safely update dependencies with version analysis, breaking change detection, and rollback planning
version: 1.1.0
tags: [dependencies, npm, security, maintenance, updates]
owner: platform
status: active
---

# Dependency Update Skill

## Overview

Safely update dependencies with risk analysis and rollback planning.

## Usage

```
/dependency-update
```

## Documentation Reference

- Use Ref tools to confirm migration guides and breaking changes.

## Identity
**Role**: Dependency Manager
**Objective**: Keep dependencies up-to-date while minimizing risk of breaking changes and security vulnerabilities.

## Update Strategy

### Version Classification

**Semantic Versioning (SemVer)**: `MAJOR.MINOR.PATCH`
- **PATCH** (1.2.3 → 1.2.4): Bug fixes, safe to auto-update
- **MINOR** (1.2.3 → 1.3.0): New features, backward compatible
- **MAJOR** (1.2.3 → 2.0.0): Breaking changes, requires review

### Update Tiers

| Tier | Risk | Automation | Review |
|------|------|------------|--------|
| Security patches | Critical | Auto-merge | Post-merge |
| Patch updates | Low | Auto-merge with tests | Weekly batch |
| Minor updates | Medium | PR with tests | Per-PR review |
| Major updates | High | Draft PR | Dedicated review |

## Workflow

### Step 1: Audit Current State

```bash
# Check for outdated packages
npm outdated

# Check for vulnerabilities
npm audit

# Get detailed dependency tree
npm ls --all
```

**Output Analysis**:
```
Package          Current  Wanted  Latest  Location
react            18.2.0   18.2.0  19.0.0  myapp
lodash           4.17.20  4.17.21 4.17.21 myapp
@types/node      20.8.0   20.11.5 20.11.5 myapp
```

### Step 2: Categorize Updates

**Security Updates** (do first):
```bash
# Find packages with vulnerabilities
npm audit --json | jq '.vulnerabilities | keys[]'

# Auto-fix what's safe
npm audit fix

# Force fix (may have breaking changes)
npm audit fix --force  # Review changes carefully!
```

**Patch Updates** (safe):
```bash
# Update all to latest patch
npm update
```

**Minor Updates**:
```bash
# Check changelogs before updating
npm view <package> versions
npm view <package> repository

# Update specific package
npm install <package>@latest
```

**Major Updates**:
```bash
# Read migration guide first!
npm view <package> readme

# Install specific major version
npm install <package>@^2.0.0
```

### Step 3: Test Updates

**Before committing**:
```bash
# Clean install to verify lock file
rm -rf node_modules
npm ci

# Run all tests
npm test

# Type check
npm run typecheck

# Build
npm run build

# Run E2E tests if available
npm run test:e2e
```

**Smoke Test Checklist**:
- [ ] App starts without errors
- [ ] Core functionality works
- [ ] No console errors/warnings
- [ ] Performance not degraded

### Step 4: Document Changes

**Commit Message**:
```
chore(deps): update dependencies

Security fixes:
- lodash 4.17.20 → 4.17.21 (CVE-2021-23337)

Minor updates:
- react-query 3.34.0 → 3.39.0
- typescript 5.0.0 → 5.3.0

Major updates:
- None

Full test suite passing.
```

**CHANGELOG Entry**:
```markdown
## [Unreleased]

### Security
- Updated lodash to fix prototype pollution (CVE-2021-23337)

### Changed
- Updated TypeScript to 5.3 for improved type inference
```

## Breaking Change Handling

### Detection

Check for breaking changes:
1. Read CHANGELOG/release notes
2. Check GitHub releases page
3. Search for migration guides
4. Look for deprecation warnings

### Common Breaking Changes

**React**:
- Component lifecycle changes
- Hook behavior changes
- Prop type changes

**TypeScript**:
- Stricter type checking
- Removed deprecated features
- New required flags

**Node.js**:
- API changes
- V8 engine updates
- Module system changes

### Migration Process

1. **Create migration branch**
   ```bash
   git checkout -b chore/upgrade-react-19
   ```

2. **Update package**
   ```bash
   npm install react@19 react-dom@19
   ```

3. **Run migration codemod** (if available)
   ```bash
   npx @react-codemod/react-19 .
   ```

4. **Fix compilation errors**
   - Address TypeScript errors
   - Update deprecated APIs

5. **Fix test failures**
   - Update test utilities
   - Fix changed behavior

6. **Manual testing**
   - Critical user paths
   - Edge cases
   - Performance comparison

7. **Create detailed PR**
   - List all changes
   - Document breaking change handling
   - Include before/after metrics

## Automation Setup

### Dependabot Configuration
```yaml
# .github/dependabot.yml
version: 2
updates:
  - package-ecosystem: npm
    directory: "/"
    schedule:
      interval: weekly
      day: monday
    open-pull-requests-limit: 10
    groups:
      dev-dependencies:
        patterns:
          - "@types/*"
          - "eslint*"
          - "prettier"
      production:
        patterns:
          - "react*"
          - "next"

  - package-ecosystem: docker
    directory: "/"
    schedule:
      interval: weekly
```

### Renovate Configuration
```json
{
  "$schema": "https://docs.renovatebot.com/renovate-schema.json",
  "extends": [
    "config:base",
    ":automergeMinor",
    ":automergePatch",
    "security:openssf-scorecard"
  ],
  "packageRules": [
    {
      "matchUpdateTypes": ["patch", "minor"],
      "matchCurrentVersion": "!/^0/",
      "automerge": true
    },
    {
      "matchPackagePatterns": ["^@types/"],
      "automerge": true
    },
    {
      "matchUpdateTypes": ["major"],
      "labels": ["major-update", "needs-review"]
    }
  ],
  "vulnerabilityAlerts": {
    "enabled": true,
    "labels": ["security"]
  }
}
```

### CI Validation
```yaml
# .github/workflows/dependency-check.yml
name: Dependency Check

on:
  pull_request:
    paths:
      - 'package.json'
      - 'package-lock.json'

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Setup Node
        uses: actions/setup-node@v4
        with:
          node-version: 20
          cache: 'npm'

      - name: Clean install
        run: npm ci

      - name: Audit
        run: npm audit --audit-level=high

      - name: Test
        run: npm test

      - name: Build
        run: npm run build
```

## Rollback Plan

If update causes issues in production:

1. **Immediate**: Revert the commit
   ```bash
   git revert <commit-hash>
   ```

2. **Lock versions**: Pin problematic packages
   ```json
   {
     "overrides": {
       "problematic-package": "1.2.3"
     }
   }
   ```

3. **Document**: Create issue tracking the problem

4. **Investigate**: Find root cause before retry

## Output Format

```json
{
  "scan_date": "2026-01-23",
  "outdated_count": 12,
  "vulnerable_count": 2,
  "updates_applied": [
    {
      "package": "lodash",
      "from": "4.17.20",
      "to": "4.17.21",
      "type": "patch",
      "reason": "security"
    }
  ],
  "major_updates_pending": [
    {
      "package": "react",
      "from": "18.2.0",
      "to": "19.0.0",
      "migration_guide": "https://react.dev/blog/react-19-upgrade-guide"
    }
  ],
  "automation_configured": {
    "dependabot": true,
    "renovate": false
  },
  "test_results": "all_passing"
}
```

## Anti-Patterns

**DO NOT**:
- Update all packages blindly (`npm update --save`)
- Ignore deprecation warnings
- Skip testing after updates
- Mix feature work with dependency updates
- Force update past security warnings
- Forget to update lock file
- Update in Friday afternoon deploys

## Outputs

- Dependency update report with risk assessment and test status.

## Related Skills

- `/security-scan` - Scan for dependency vulnerabilities
