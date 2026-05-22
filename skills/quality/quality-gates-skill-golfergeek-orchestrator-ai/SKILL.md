---
name: Quality Gates
description: Ensure code quality before commits. Run lint, format, test, build. Use npm scripts: npm run lint, npm run format, npm test, npm run build. CRITICAL: All tests must pass, no lint errors, code must be formatted before committing.
allowed-tools: Read, Write, Edit, Bash, Grep, Glob
---

# Quality Gates Skill

**CRITICAL**: Code must pass all quality gates before committing: lint, format, test, build.

## When to Use This Skill

Use this skill when:
- Before committing code
- Setting up quality checks
- Verifying code quality
- Running tests
- Checking lint/format compliance

## Quality Gate Commands

From `package.json`:

```6:27:package.json
  "scripts": {
    "contracts:generate": "turbo run generate --filter=@orchestrator-ai/shared-contracts",
    "dev": "./start-dev-local.sh",
    "dev:api": "cd apps/api && ./start-dev.sh",
    "dev:observability": "cd apps/observability/server && npm run dev",
    "dev:observability:client": "cd apps/observability/client && npm run dev",
    "dev:observability:all": "concurrently \"npm run dev:observability\" \"npm run dev:observability:client\"",
    "n8n:up": "./apps/n8n/manage.sh up",
    "n8n:down": "./apps/n8n/manage.sh down",
    "n8n:logs": "./apps/n8n/manage.sh logs -f",
    "build:transport-types": "cd apps/transport-types && npm run build",
    "dev:web": "cd apps/web && npm run dev",
    "dev:start": "./start-dev-local.sh",
    "dev:ports": "./scripts/dev-ports.sh",
    "dev:supabase": "cd apps/api && supabase status",
    "dev:supabase:start": "cd apps/api && supabase start",
    "dev:supabase:stop": "cd apps/api && supabase stop",
    "dev:supabase:reset": "cd apps/api && supabase db reset",
    "build": "turbo run build",
    "test": "turbo run test",
    "lint": "turbo run lint --filter=nestjs",
    "format": "turbo run format",
```

### Core Quality Gates

```bash
# 1. Format code
npm run format

# 2. Lint code
npm run lint

# 3. Run tests
npm test

# 4. Build (verify compilation)
npm run build
```

## Complete Quality Gate Checklist

Before committing, run:

```bash
# Step 1: Format code
npm run format

# Step 2: Lint code (must pass with no errors)
npm run lint

# Step 3: Run tests (all must pass)
npm test

# Step 4: Build (verify compilation succeeds)
npm run build

# Step 5: Commit only if all gates pass
git add .
git commit -m "feat(module): your commit message"
```

## Quality Gate Failures

### ❌ Format Failure

```bash
$ npm run format
# Errors: files need formatting
```

**Fix:**
```bash
npm run format
# Re-run until no changes
```

### ❌ Lint Failure

```bash
$ npm run lint
# Errors: unused imports, type errors, etc.
```

**Fix:**
```bash
# Fix lint errors manually or run auto-fix if available
npm run lint -- --fix
```

### ❌ Test Failure

```bash
$ npm test
# Errors: tests failing
```

**Fix:**
```bash
# Fix failing tests
# Re-run tests until all pass
npm test
```

### ❌ Build Failure

```bash
$ npm run build
# Errors: TypeScript compilation errors
```

**Fix:**
```bash
# Fix TypeScript errors
# Re-run build until successful
npm run build
```

## Pre-Commit Workflow

### Recommended Workflow

```bash
# 1. Make your changes
# ... edit files ...

# 2. Stage files
git add .

# 3. Run quality gates
npm run format && npm run lint && npm test && npm run build

# 4. If all pass, commit
git commit -m "feat(module): description"
```

### One-Line Quality Gate

```bash
npm run format && npm run lint && npm test && npm run build && git commit -m "feat(module): description"
```

## Per-Workspace Quality Gates

### API Workspace

```bash
cd apps/api
npm run lint
npm test
npm run build
```

### Web Workspace

```bash
cd apps/web
npm run lint
npm test:unit
npm run build
```

## Quality Gate Examples

### Example 1: Before Feature Commit

```bash
# Edit feature code
vim apps/api/src/feature/feature.service.ts

# Run quality gates
npm run format
npm run lint
npm test
npm run build

# All pass - commit
git add .
git commit -m "feat(feature): add new feature service"
```

### Example 2: Before Bug Fix Commit

```bash
# Fix bug
vim apps/api/src/bug/bug.service.ts

# Run quality gates
npm run format && npm run lint && npm test && npm run build

# All pass - commit
git add .
git commit -m "fix(bug): resolve service bug"
```

## CI/CD Integration

Quality gates should also run in CI/CD:

```yaml
# .github/workflows/quality.yml
name: Quality Gates

on: [push, pull_request]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
      - run: npm ci
      - run: npm run format -- --check
      - run: npm run lint
      - run: npm test
      - run: npm run build
```

## Common Quality Issues

### Unused Imports

```typescript
// ❌ WRONG
import { UnusedService } from './unused.service';

// ✅ CORRECT - Remove unused imports
```

### Type Errors

```typescript
// ❌ WRONG
const result: string = await service.getNumber();

// ✅ CORRECT
const result: number = await service.getNumber();
```

### Formatting Issues

```typescript
// ❌ WRONG - Inconsistent spacing
if(condition){
  doSomething();
}

// ✅ CORRECT - Formatted
if (condition) {
  doSomething();
}
```

## Checklist for Quality Gates

Before committing:

- [ ] `npm run format` - Code formatted
- [ ] `npm run lint` - No lint errors
- [ ] `npm test` - All tests pass
- [ ] `npm run build` - Build succeeds
- [ ] All quality gates pass before commit

## Related Documentation

- **Conventional Commits**: See Conventional Commits Skill for commit message format
- **Git Standards**: See Orchestrator Git Standards Skill for git workflow

