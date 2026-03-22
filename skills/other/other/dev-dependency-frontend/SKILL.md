---
version: 1.1.0
name: dev-dependency-frontend
description: >
  Audit and update npm packages for Angular/TypeScript projects. Detects outdated
  packages, security vulnerabilities, and breaking changes. Groups updates by risk
  level, runs verification after each batch, and pauses for user confirmation before
  any major version bump or Angular framework upgrade.
  Invoked via /dev-dependency (unified entry point) — not directly.
disable-model-invocation: true
user-invocable: false
argument-hint: "[--audit | --patch | --minor | --major | --security | --interactive]"
---

# Dependency Update — Frontend (Angular)

Audit and update npm packages safely, with breaking change detection.

> **Stack:** Angular/TypeScript (npm)

## When to Use

- Routine npm dependency maintenance
- Security vulnerability response (`npm audit`)
- Angular framework upgrades (Angular 19→20, TypeScript bumps)
- Before starting a new feature (ensure clean baseline)

## Core Principle

**Never apply major version bumps without user confirmation.** Major versions mean breaking changes — API removals, behavioral changes, migration schematics. Always show what changed and ask before proceeding.

## Workflow

```
1. AUDIT       → npm outdated / npm audit / ng update
2. TRIAGE      → Classify as patch / minor / major / security
3. UPDATE      → Patch → verify → Minor → verify → Major → ASK → verify
4. VERIFY      → ng build && ng test after each batch
```

## Phase 1: Audit

```bash
# Outdated packages (color-coded: red=in-range, yellow=major bump)
npm outdated

# Security audit
npm audit

# Angular-specific update check
ng update
```

### Optional tools

```bash
# npm-check-updates (color-coded risk: red=major, cyan=minor, green=patch)
npx npm-check-updates

# Doctor mode — auto-tests each upgrade to find which ones break
npx npm-check-updates --doctor
```

## Phase 2: Triage

Present a report to the user:

```
DEPENDENCY UPDATE REPORT — Frontend (Angular)
===============================================

Patch (safe):
  rxjs                     7.8.0 → 7.8.1
  zone.js                  0.14.3 → 0.14.4

Minor (review):
  @angular/material       17.2.0 → 17.3.0
  @ngrx/store              17.1.0 → 17.2.0

Major (BREAKING — needs confirmation):
  ⚠ @angular/core          17.3.0 → 18.0.0
  ⚠ typescript              5.3.3 → 5.5.0
  ⚠ rxjs                    7.8.1 → 8.0.0

Security:
  🔒 express               4.18.2 → 4.19.2  (CVE-2024-XXXX)
```

### Risk levels

| Level | SemVer | Risk | Action |
|-------|--------|------|--------|
| **Patch** | `X.Y.Z+` | Minimal — bug fixes | Apply automatically |
| **Minor** | `X.Y+.Z` | Low — backward-compatible | Apply, run tests |
| **Major** | `X+.Y.Z` | High — breaking changes | **ASK the user first** |
| **Security** | Any | Depends on severity | Prioritize |

**Note:** `npm update` respects semver ranges and will never auto-install major versions. Major bumps always require explicit action.

## Phase 3: Update

### Step 1: Security fixes (urgent)

```bash
# Auto-fix what it can (safe updates only)
npm audit fix

# NEVER blindly run this — may install breaking major versions:
# npm audit fix --force
```

**→ Run verification (`ng build && ng test --watch=false`)**

### Step 2: Patch updates (safe)

```bash
# Respects semver ranges, only applies patches
npm update
```

**→ Run verification**

### Step 3: Minor updates (review)

Apply one by one:

```bash
npm install <package>@<latest-minor>
```

**→ Run verification**

### Step 4: Major updates (STOP AND ASK)

**Never auto-apply.** For each major bump:

1. **Show the user what's changing:**
   ```
   ⚠ MAJOR VERSION UPDATE: @angular/core 17.3.0 → 18.0.0

   Breaking changes:
   - New control flow syntax (@if/@for replace *ngIf/*ngFor)
   - Signals become primary reactivity model
   - Karma test runner deprecated (migrate to Jest/Vitest)

   Impact: 47 files import from @angular/core
   Migration guide: https://angular.dev/update-guide

   Files likely needing changes:
   - All component templates (control flow migration)
   - app.config.ts (new providers pattern)
   - karma.conf.js (test runner migration)

   Proceed? (yes/no/skip)
   ```

2. **If user confirms:** use `ng update`, run schematics, check build, run tests

### Impact Analysis

```bash
# How many files import this?
grep -rn "from '<package>'" --include="*.ts" src/ | wc -l

# Which files?
grep -rln "from '<package>'" --include="*.ts" src/
```

## Breaking Change Detection

### How to identify

1. **SemVer major bump** → always assume breaking
2. **Angular update guide** — check `angular.dev/update-guide`
3. **`ng update` schematics** — auto-migrate known patterns
4. **TypeScript wiki** — check `github.com/microsoft/TypeScript/wiki/Breaking-Changes`
5. **Build after update** — compiler errors reveal API changes

### Common breaking changes by package

| Package | Watch for |
|---------|-----------|
| **@angular/core** | Module→standalone, signal APIs, control flow syntax, build system |
| **TypeScript** | Stricter type checks, enum handling, decorator metadata changes |
| **RxJS** | Operator renames, import paths, subscription handling |
| **@angular/material** | MDC migration, theming API changes, component selectors |
| **@ngrx/store** | createFeature API, signal store, action creators |
| **zone.js** | Zoneless Angular (experimental), provideZonelessChangeDetection |
| **Playwright** | API renames, configuration format, assertion changes |

## Angular Framework Upgrade

Angular upgrades have a specific workflow:

```
1. Check angular.dev/update-guide for migration guide
2. ng update @angular/core @angular/cli
3. Run migration schematics (automatic code transforms)
4. ng build → fix compiler errors
5. ng test --watch=false → fix test failures
6. Update third-party Angular packages to compatible versions
7. Check for deprecated APIs (Angular compiler warnings)
```

**Always update @angular/core FIRST, then third-party packages.**

### Version-by-version approach

For multi-version jumps (e.g., Angular 16→19), upgrade one major version at a time:

```bash
ng update @angular/core@17 @angular/cli@17
# test, fix, commit
ng update @angular/core@18 @angular/cli@18
# test, fix, commit
ng update @angular/core@19 @angular/cli@19
# test, fix, commit
```

## Verification

After each batch:

```bash
ng build 2>&1 | tail -20
ng test --watch=false 2>&1 | tail -30
```

## Rollback

```bash
# Restore from lock file
rm -rf node_modules
npm ci

# Revert specific package
npm install <package>@<previous-version>

# Nuclear option
git checkout -- package.json package-lock.json
npm ci
```

## Flags

| Flag | Behavior |
|------|----------|
| `--audit` | Report only, no changes (default) |
| `--patch` | Apply patch updates only |
| `--minor` | Apply patch + minor updates |
| `--major` | Full update including major (always asks) |
| `--security` | Security fixes only |
| `--interactive` | Step through each package one by one |

## Anti-Patterns

- **Updating everything at once** — one major bump breaks, but which one?
- **`npm audit fix --force`** — may install breaking major versions silently
- **Updating Angular packages before @angular/core** — version mismatches cause cryptic errors
- **Skipping migration schematics** — `ng update` schematics fix known patterns automatically
- **Pinning exact versions forever** — security vulnerabilities accumulate
- **Ignoring TypeScript version requirements** — Angular requires specific TypeScript ranges
