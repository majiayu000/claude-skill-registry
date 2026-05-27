---
name: dependency-management
description: This skill should be used when managing project dependencies including safe updates, security audits, and compatibility analysis.
---

# Dependency Management Skill

Safely manage and update project dependencies.

## When to Use

- Updating outdated dependencies
- Auditing for security vulnerabilities
- Analyzing dependency compatibility
- Planning major version upgrades
- Reducing dependency bloat

## Reference Documents

- [Update Strategies](./references/update-strategies.md) - Safe update approaches
- [Security Audit](./references/security-audit.md) - Vulnerability scanning
- [Compatibility Matrix](./references/compatibility-matrix.md) - Tracking constraints
- [Changelog Analysis](./references/changelog-analysis.md) - Reading changelogs

## Core Workflow

### 1. Audit Current State

```bash
# Node.js
npm outdated
npm audit

# Python
pip list --outdated
pip-audit

# Ruby
bundle outdated
bundle audit

# Go
go list -m -u all
govulncheck ./...
```

### 2. Categorize Updates

| Category | Risk | Approach |
|----------|------|----------|
| Patch (0.0.x) | Low | Usually safe to batch |
| Minor (0.x.0) | Medium | Review changelog, test |
| Major (x.0.0) | High | Plan migration, extensive test |
| Security | Critical | Prioritize immediately |

### 3. Update Strategy

```markdown
## Update Plan

### Immediate (Security)
- lodash: 4.17.15 → 4.17.21 (CVE-2021-23337)
- axios: 0.21.0 → 1.6.0 (CVE-2023-45857)

### This Sprint (Patch/Minor)
- jest: 29.5.0 → 29.7.0
- typescript: 5.0.4 → 5.3.0
- prettier: 3.0.0 → 3.1.0

### Planned (Major)
- react: 17.0.2 → 18.2.0 (requires migration)
- webpack: 4.x → 5.x (requires config changes)
```

### 4. Safe Update Process

```bash
# 1. Create update branch
git checkout -b deps/update-YYYY-MM-DD

# 2. Update one package at a time (for major updates)
npm install package@version

# 3. Run tests
npm test

# 4. Check for breaking changes
npm run build
npm run lint

# 5. Commit if passing
git commit -m "Update package to version"

# 6. Repeat or batch
```

## Risk Assessment

### Low Risk Updates

Safe to batch together:

```bash
# Update all patch versions
npm update

# Update specific minor versions
npm install package1@^2.1.0 package2@^3.2.0
```

### Medium Risk Updates

Update individually with testing:

```markdown
## Update: typescript 5.0 → 5.3

### Changelog Review
- New decorator syntax
- Improved type inference
- Breaking: stricter null checks

### Testing Plan
1. Run type checker
2. Run full test suite
3. Build production bundle
4. Test critical flows

### Rollback Plan
```bash
npm install typescript@5.0.4
```
```

### High Risk Updates

Require dedicated migration:

```markdown
## Migration: React 17 → 18

### Breaking Changes
- New root API (createRoot)
- Automatic batching
- Strict mode behavior changes

### Migration Steps
1. Update react and react-dom
2. Update to new root API
3. Fix strict mode warnings
4. Update testing library
5. Run full test suite
6. Manual QA of critical flows

### Timeline
- Sprint 1: Core migration
- Sprint 2: Fix deprecation warnings
- Sprint 3: Adopt new features
```

## Security Prioritization

### Severity Levels

| Level | Response Time | Action |
|-------|---------------|--------|
| Critical | Immediate | Emergency patch |
| High | 24-48 hours | Priority update |
| Medium | This sprint | Scheduled update |
| Low | Next sprint | Normal priority |

### Vulnerability Response

```markdown
## CVE Response Checklist

- [ ] Identify affected package and version
- [ ] Check if exploitable in our usage
- [ ] Find patched version
- [ ] Test update locally
- [ ] Deploy to staging
- [ ] Verify fix with security scan
- [ ] Deploy to production
- [ ] Document in security log
```

## Dependency Hygiene

### Regular Maintenance

```markdown
## Weekly
- [ ] Check for security advisories
- [ ] Review critical dependency updates

## Monthly
- [ ] Run full dependency audit
- [ ] Update patch versions
- [ ] Review minor version updates

## Quarterly
- [ ] Plan major version migrations
- [ ] Assess unused dependencies
- [ ] Review dependency size impact
```

### Removing Unused Dependencies

```bash
# Node.js - Find unused
npx depcheck

# Python - Find unused
pip-autoremove --list

# Review and remove
npm uninstall unused-package
```
