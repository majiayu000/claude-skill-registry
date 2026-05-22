---
name: dependency-audit
description: Audit npm dependencies for security vulnerabilities, outdated packages, and license compliance.
---

# Dependency Audit Skill

Comprehensive npm dependency security and health check.

## Security Audit

1. Run npm audit:

   ```bash
   npm audit
   ```

2. For detailed JSON output:

   ```bash
   npm audit --json
   ```

3. Fix automatically if safe:

   ```bash
   npm audit fix
   ```

4. For breaking changes (be careful):
   ```bash
   npm audit fix --force
   ```

## Outdated Packages

1. Check for outdated:

   ```bash
   npm outdated
   ```

2. Update specific package:

   ```bash
   npm update <package-name>
   ```

3. Update to latest (major versions):
   ```bash
   npx npm-check-updates -u
   npm install
   ```

## License Check

1. List all licenses:

   ```bash
   npx license-checker --summary
   ```

2. Check for problematic licenses:
   ```bash
   npx license-checker --onlyAllow "MIT;Apache-2.0;BSD-2-Clause;BSD-3-Clause;ISC"
   ```

## Bundle Analysis

1. Analyze bundle size:

   ```bash
   npx source-map-explorer dist/**/*.js
   ```

2. Find duplicate dependencies:
   ```bash
   npx npm-dedupe
   ```

## Output Report

```markdown
## Dependency Audit Report

### Security

- Critical: X
- High: X
- Medium: X
- Low: X

### Outdated Packages

| Package | Current | Wanted | Latest |
| ------- | ------- | ------ | ------ |
| ...     | ...     | ...    | ...    |

### Actions Required

1. [Action with priority]
2. [Action with priority]
```
