---
name: node-to-bun
description: Migrate Node.js projects to Bun with compatibility analysis. Use when converting existing npm/pnpm/yarn projects to Bun or auditing dependencies for Bun compatibility.
compatibility: Requires Bun 1.0+
allowed-tools: ["Bash", "Read", "Grep", "Write"]
metadata:
  author: daleseo
  category: bun-runtime
  tags: [bun, migration, nodejs, node-to-bun, compatibility, dependencies]
---

# Node.js to Bun Migration

You are assisting with migrating an existing Node.js project to Bun. This involves analyzing dependencies, updating configurations, and ensuring compatibility.

## Migration Workflow

### 1. Pre-Migration Analysis

**Check if Bun is installed:**
```bash
bun --version
```

**Analyze current project:**
```bash
# Check Node.js version
node --version

# Check package manager
ls -la | grep -E "package-lock.json|yarn.lock|pnpm-lock.yaml"
```

Read `package.json` to understand the project structure.

### 2. Dependency Compatibility Check

**Read and analyze all dependencies** from `package.json`:

```bash
cat package.json
```

**Check for known incompatible native modules:**

Common problematic packages (check against current dependencies):

- `bcrypt` → Use `bcryptjs` or `@node-rs/bcrypt` instead
- `sharp` → Bun has native support, but may need version check
- `node-canvas` → Limited support, check version compatibility
- `sqlite3` → Use `bun:sqlite` instead
- `node-gyp` dependent packages → May require alternative pure JS versions
- `fsevents` → macOS-specific, usually optional dependency
- `esbuild` → Bun has built-in bundler, may be redundant

**Check workspace configuration** (for monorepos):
```bash
# Check if workspaces are defined
grep -n "workspaces" package.json
```

### 3. Generate Compatibility Report

Create a migration report file `BUN_MIGRATION_REPORT.md`:

```markdown
# Bun Migration Analysis Report

## Project Overview
- **Name**: [project name]
- **Current Node Version**: [version]
- **Package Manager**: [npm/yarn/pnpm]
- **Project Type**: [app/library/monorepo]

## Dependency Analysis

### ✅ Compatible Dependencies
[List dependencies that are Bun-compatible]

### ⚠️ Potentially Incompatible Dependencies
[List dependencies that may have issues]

**Recommended Actions:**
- [Specific migration steps for each incompatible dependency]

### 🔄 Recommended Replacements
[List suggested package replacements]

## Configuration Changes Needed

### package.json
- [ ] Update scripts to use `bun` instead of `npm`/`yarn`
- [ ] Review and update `engines` field
- [ ] Check `type` field (ESM vs CommonJS)

### tsconfig.json
- [ ] Update `moduleResolution` to `"bundler"`
- [ ] Add `bun-types` to types array
- [ ] Set `allowImportingTsExtensions` to `true`

### Build Configuration
- [ ] Review webpack/rollup/esbuild config (may use Bun bundler)
- [ ] Update test runner config (use Bun test instead of Jest)

## Migration Steps

1. Install Bun dependencies
2. Update configuration files
3. Run tests to verify compatibility
4. Update CI/CD pipelines
5. Update documentation

## Risk Assessment

**Low Risk:**
[List low-risk changes]

**Medium Risk:**
[List items needing testing]

**High Risk:**
[List critical compatibility concerns]
```

### 4. Backup Current State

Before making changes:

```bash
# Create backup branch if in git repo
git branch -c backup-before-bun-migration

# Or suggest user commits current state
git add -A
git commit -m "Backup before Bun migration"
```

### 5. Update package.json

**Read current package.json:**
```typescript
// Read and parse package.json
```

**Update scripts** to use Bun:

```json
{
  "scripts": {
    "dev": "bun run --hot src/index.ts",
    "start": "bun run src/index.ts",
    "build": "bun build src/index.ts --outdir=dist",
    "test": "bun test",
    "typecheck": "bun run --bun tsc --noEmit",
    "lint": "bun run --bun eslint ."
  }
}
```

**Update engines field:**
```json
{
  "engines": {
    "bun": ">=1.0.0"
  }
}
```

**For libraries, add exports field** if not present:
```json
{
  "type": "module",
  "exports": {
    ".": {
      "types": "./dist/index.d.ts",
      "import": "./dist/index.js",
      "require": "./dist/index.cjs"
    }
  }
}
```

### 6. Update tsconfig.json

**Read current tsconfig:**
```bash
cat tsconfig.json
```

**Apply Bun-specific updates:**

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "types": ["bun-types"],
    "lib": ["ES2022"],
    "jsx": "react-jsx",
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "resolveJsonModule": true,
    "allowImportingTsExtensions": true,
    "noEmit": true
  }
}
```

**Key changes explained:**
- `moduleResolution: "bundler"` → Uses Bun's module resolution
- `types: ["bun-types"]` → Adds Bun's TypeScript definitions
- `allowImportingTsExtensions: true` → Allows importing `.ts` files directly
- `noEmit: true` → Bun runs TypeScript directly, no compilation needed

### 7. Handle Workspace Configuration

**For monorepos with workspaces:**

Verify workspace configuration is compatible:

```json
{
  "workspaces": [
    "packages/*",
    "apps/*"
  ]
}
```

Bun supports the same workspace syntax as npm/yarn/pnpm.

**Check workspace dependencies:**
```bash
# Verify workspace structure
find . -name "package.json" -not -path "*/node_modules/*"
```

### 8. Install Dependencies with Bun

**Remove old lockfiles:**
```bash
rm -f package-lock.json yarn.lock pnpm-lock.yaml
```

**Install with Bun:**
```bash
bun install
```

This creates `bun.lockb` (Bun's binary lockfile).

**For workspaces:**
```bash
bun install --frozen-lockfile  # Equivalent to npm ci
```

### 9. Update Test Configuration

**If using Jest, migrate to Bun test:**

Create `bunfig.toml` for test configuration:

```toml
[test]
preload = ["./tests/setup.ts"]
coverage = true
coverageThreshold = 0.8
```

**Update test files:**
- Replace `import { test, expect } from '@jest/globals'`
- With `import { test, expect } from 'bun:test'`

**Jest compatibility notes:**
- Most Jest APIs work out of the box
- `jest.mock()` → Use `mock()` from `bun:test`
- Snapshot testing works the same
- Coverage reports may differ slightly

### 10. Update Environment Configuration

**Check .env files:**
```bash
ls -la | grep .env
```

Bun loads `.env` files automatically (same as dotenv package).

**Update environment loading code:**
- Remove `require('dotenv').config()`
- Bun loads `.env` by default

### 11. Update Build Configuration

**If using webpack/rollup/esbuild:**

Consider replacing with Bun's built-in bundler:

```typescript
// bun-build.ts
await Bun.build({
  entrypoints: ['./src/index.ts'],
  outdir: './dist',
  minify: true,
  splitting: true,
  sourcemap: 'external',
  target: 'bun',
});
```

**Update build script in package.json:**
```json
{
  "scripts": {
    "build": "bun run bun-build.ts"
  }
}
```

### 12. Update CI/CD Configuration

**GitHub Actions example:**

```yaml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3

      - name: Setup Bun
        uses: oven-sh/setup-bun@v1
        with:
          bun-version: latest

      - name: Install dependencies
        run: bun install --frozen-lockfile

      - name: Run tests
        run: bun test

      - name: Type check
        run: bun run typecheck

      - name: Build
        run: bun run build
```

### 13. Verification Steps

Run these commands to verify migration:

```bash
# 1. Check dependencies installed correctly
bun install

# 2. Run type checking
bun run --bun tsc --noEmit

# 3. Run tests
bun test

# 4. Try development server
bun run dev

# 5. Test production build
bun run build
```

### 14. Update Documentation

Create or update these documentation sections:

**README.md:**
```markdown
## Prerequisites

- [Bun](https://bun.sh) 1.0 or higher

## Installation

```bash
bun install
```

## Development

```bash
bun run dev
```

## Testing

```bash
bun test
```
```

**CHANGELOG.md entry:**
```markdown
## [Version] - [Date]

### Changed
- Migrated from Node.js/npm to Bun
- Updated all dependencies to Bun-compatible versions
- Replaced [specific packages] with [alternatives]
- Updated TypeScript configuration for Bun
```

## Common Migration Issues & Solutions

### Issue: Native Module Incompatibility

**Symptoms:**
```
error: Cannot find module "bcrypt"
```

**Solution:**
```bash
# Replace with pure JavaScript alternative
bun remove bcrypt
bun add bcryptjs

# Update imports
# Before: import bcrypt from 'bcrypt';
# After: import bcrypt from 'bcryptjs';
```

### Issue: ESM/CommonJS Conflicts

**Symptoms:**
```
error: require() of ES Module not supported
```

**Solution:**

Add to `package.json`:
```json
{
  "type": "module"
}
```

Or use `.mts` extension for ES modules and `.cts` for CommonJS.

### Issue: Path Alias Resolution

**Symptoms:**
```
error: Cannot resolve "@/components"
```

**Solution:**

Verify `tsconfig.json` paths match:
```json
{
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

Bun respects TypeScript path aliases automatically.

### Issue: Test Failures

**Symptoms:**
```
error: jest is not defined
```

**Solution:**

Update test imports:
```typescript
// Before
import { describe, it, expect } from '@jest/globals';

// After
import { describe, it, expect } from 'bun:test';
```

## Migration Checklist

Present this checklist to the user:

- [ ] Bun installed and verified
- [ ] Dependency compatibility analyzed
- [ ] Migration report reviewed
- [ ] Current state backed up (git commit/branch)
- [ ] `package.json` scripts updated
- [ ] `tsconfig.json` configured for Bun
- [ ] Old lockfiles removed
- [ ] Dependencies installed with `bun install`
- [ ] Test configuration migrated
- [ ] Tests passing with `bun test`
- [ ] Build process verified
- [ ] CI/CD updated for Bun
- [ ] Documentation updated
- [ ] Team notified of migration

## Post-Migration Performance Verification

After migration, help user verify performance improvements:

```bash
# Compare install times
time bun install  # Should be 3-10x faster than npm

# Compare test execution
time bun test     # Should be faster than Jest

# Compare startup time
time bun run src/index.ts  # Should be 90% faster than ts-node
```

## Rollback Procedure

If migration encounters critical issues:

```bash
# Return to backup branch
git checkout backup-before-bun-migration

# Or restore original state
git reset --hard HEAD~1

# Reinstall original dependencies
npm install  # or yarn/pnpm
```

## Completion

Once migration is complete, provide summary:
- ✅ Migration status (success/partial/issues)
- ✅ List of changes made
- ✅ Performance improvements observed
- ✅ Any remaining manual steps
- ✅ Links to Bun documentation for ongoing development
