---
name: mern-deps
description: Check and update dependencies safely with security audits and test verification.
argument-hint: "[--check] [--audit] [--update] [--update-major]"
allowed-tools: Bash, Write, Read, Glob, Grep
---

## Purpose
Manage dependencies safely: audit for vulnerabilities, check for updates, and update with test verification.

## Arguments
- `--check` — Check for outdated packages (default if no args)
- `--audit` — Run security audit
- `--update` — Update patch/minor versions with test verification
- `--update-major` — Show available major updates (requires manual review)

## Workflow

### Check (`--check`)
1. Run `pnpm outdated`
2. Categorize: patch, minor, major
3. Report packages with updates available
4. Flag packages with known issues

### Audit (`--audit`)
1. Run `pnpm audit`
2. Report vulnerabilities by severity (critical, high, moderate, low)
3. Suggest fixes for critical/high
4. Check for patches available

### Update (`--update`)
1. Show packages to update (patch + minor only)
2. **Ask for approval**
3. Update packages: `pnpm update`
4. Run tests: `pnpm test`
5. Run build: `pnpm build`
6. If tests pass, commit changes
7. If tests fail, rollback and report

### Major updates (`--update-major`)
1. List packages with major updates
2. Show changelogs/breaking changes (if available)
3. Recommend update order (dependencies first)
4. Do not auto-update — requires manual review

For universal safety rules and update priority order, see `/shared-deps-safety`.

## Output

### Check output
```
Outdated packages:

Patch updates (safe):
  - zod: 3.22.4 → 3.22.5
  - mongoose: 8.0.1 → 8.0.3

Minor updates (usually safe):
  - next: 14.1.0 → 14.2.1
  - @types/node: 20.10.0 → 20.11.0

Major updates (review required):
  - eslint: 8.56.0 → 9.0.0 ⚠️ Breaking changes
```

### Audit output
```
Security audit:

Critical: 0
High: 1
  - lodash <4.17.21 (Prototype Pollution)
    Fix: pnpm update lodash
Moderate: 2
Low: 3

Run `pnpm audit fix` to auto-fix where possible.
```

## Reference
For update strategies and common issues, see `reference/mern-deps-reference.md`
