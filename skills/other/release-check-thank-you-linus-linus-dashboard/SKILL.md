---
name: release-check
description: Check if project is ready for release with comprehensive pre-release validation. Use when verifying release readiness, running validation checks, or checking project quality before publishing.
---

# Pre-Release Validation Checks

Run comprehensive pre-release validation checks.

Current version: Check `package.json` for current version.

## Running Validation Checks

Execute the release check command:
```bash
npm run release:check
```

---

## What Will Be Checked (17 Validations)

1. Git status is clean
2. On correct branch (main/master)
3. Up to date with remote
4. RELEASE_NOTES.md exists
5. Dependencies installed
6. Linting passes
7. Type checking passes
8. Build succeeds
9. Version consistency across files
10. No FIXME/TODO comments
11. CHANGELOG.md exists
12. Manifest.json valid
13. HACS.json valid
14. No sensitive data
15. Python syntax valid
16. README files exist
17. LICENSE exists

---

## Additional Pre-Release Checks

**Smoke tests:**
```bash
npm run test:smoke
```
Runs 15 critical smoke tests to ensure basic functionality.

**Release notes validation:**
```bash
npm run release:validate
```
Validates RELEASE_NOTES.md format and content.

---

## If Checks Fail

### Build Errors
- Run: `npm run build` to see detailed errors
- Fix reported issues
- Re-run checks

### Linting Errors
- Run: `npm run lint` to fix automatically
- Or: `npm run lint:check` to see issues
- Fix any remaining manual issues
- Re-run checks

### Type Errors
- Run: `npm run type-check` to see detailed errors
- Fix type issues in TypeScript files
- Re-run checks

### Version Mismatch
All files should have same version:
- [package.json](package.json)
- [custom_components/linus_dashboard/manifest.json](custom_components/linus_dashboard/manifest.json)
- [custom_components/linus_dashboard/const.py](custom_components/linus_dashboard/const.py)
- [src/linus-strategy.ts](src/linus-strategy.ts)

Run appropriate bump command to sync versions.

---

## Quick Fixes

### Missing CHANGELOG.md
```bash
npm run release:changelog
```

### Missing RELEASE_NOTES.md
```bash
npm run release:notes
```

### Dependencies Out of Date
```bash
npm install
```

---

## After All Checks Pass

Choose release type based on changes:
- Use release-beta skill - Pre-release for community testing (recommended)
- Use release-stable skill - Stable production release

---

## Workflow

1. Run validation checks
2. Fix any reported issues
3. Run smoke tests
4. Validate release notes
5. Proceed with release if all checks pass
