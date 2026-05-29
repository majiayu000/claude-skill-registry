---
name: nean-deps
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
1. Run `npm outdated`
2. Categorize: patch, minor, major
3. Report packages with updates available
4. Flag packages with known issues

### Audit (`--audit`)
1. Run `npm audit`
2. Report vulnerabilities by severity (critical, high, moderate, low)
3. Suggest fixes for critical/high
4. Check for patches available

### Update (`--update`)
1. Show packages to update (patch + minor only)
2. **Ask for approval**
3. Update packages: `npm update`
4. Run tests: `npm test`
5. Run build: `npm run build`
6. If tests pass, commit changes
7. If tests fail, rollback and report

### Major updates (`--update-major`)
1. List packages with major updates
2. Show changelogs/breaking changes (if available)
3. Recommend update order (dependencies first)
4. Do not auto-update — requires manual review

For universal safety rules and update priority order, see `/shared-deps-safety`.

## NEAN-specific considerations

### Angular updates
```bash
# Use Angular CLI for framework updates
ng update @angular/core @angular/cli
ng update @angular/material  # If using
```

### NestJS updates
- Check migration guides for major versions
- Update @nestjs/* packages together
- Test all modules after update

### Nx updates
```bash
# Use Nx migrate for workspace updates
npx nx migrate latest
npx nx migrate --run-migrations
```

### TypeORM updates
- Check migration compatibility
- Test all database operations
- Review breaking changes in query builder

## Output

### Check output
```
Outdated packages:

Patch updates (safe):
  - @types/node: 20.10.0 → 20.10.5
  - class-validator: 0.14.0 → 0.14.1

Minor updates (usually safe):
  - @nestjs/core: 10.3.0 → 10.4.1
  - primeng: 17.15.0 → 17.18.0

Major updates (review required):
  - typescript: 5.4.0 → 5.5.0 ⚠️ Check compatibility
  - @angular/core: 17.3.0 → 18.0.0 ⚠️ Major version
```

### Audit output
```
Security audit:

Critical: 0
High: 1
  - axios <1.6.0 (SSRF vulnerability)
    Fix: npm update axios
Moderate: 2
Low: 3

Run `npm audit fix` to auto-fix where possible.
```

## Reference
For update strategies and common issues, see `reference/nean-deps-reference.md`
