---
name: shared-deps-safety
description: Universal safety rules, workflow structure, and update priority for dependency management across all platforms.
---

## Purpose

Define safe dependency management practices. Platform deps skills reference this for safety rules and workflow structure, then add platform-specific commands and procedures.

## Safety rules

- Never auto-update major versions
- Always run tests after updates
- Always build after updates
- Rollback on test or build failure
- Commit lockfile changes atomically with updated packages
- Report breaking change warnings

## Workflow structure

### Check

1. List outdated packages
2. Categorize by semver: patch, minor, major
3. Report packages with updates available
4. Flag packages with known issues

### Audit

1. Run security audit
2. Report vulnerabilities by severity (critical, high, moderate, low)
3. Suggest fixes for critical/high
4. Check for patches available

### Update (patch + minor only)

1. Show packages to update
2. **Ask for approval**
3. Update packages
4. Run tests and build
5. If tests pass, commit changes
6. If tests fail, rollback and report

### Major updates (report only)

1. List packages with major updates
2. Show changelogs/breaking changes if available
3. Recommend update order (dependencies first)
4. Do not auto-update — requires manual review

## Update priority order

1. Type packages (`@types/*`, type stubs)
2. Build tools (TypeScript, ESLint, Prettier, SwiftLint)
3. Testing tools (Vitest, Jest, Playwright, Swift Testing)
4. Framework packages (Next.js, Angular, NestJS, SwiftUI dependencies)
5. Application dependencies
