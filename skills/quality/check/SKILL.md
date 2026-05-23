---
name: check
description: Run build, lint, and type checking for the Kardashev Network project
disable-model-invocation: true
allowed-tools: Bash, Read
---

# Project Health Check

Run all checks to verify project health.

## Commands to Run

### 1. Type Checking
```bash
cd /Users/tyrelle/Desktop/KardashevNetwork && npx tsc --noEmit
```

### 2. Linting
```bash
cd /Users/tyrelle/Desktop/KardashevNetwork && npm run lint
```

### 3. Build
```bash
cd /Users/tyrelle/Desktop/KardashevNetwork && npm run build
```

## Run All Checks

Execute all checks sequentially and report results:

```bash
cd /Users/tyrelle/Desktop/KardashevNetwork && npm run lint && npx tsc --noEmit && npm run build
```

## Expected Output

### Success
- Lint: No warnings or errors
- TypeScript: No type errors
- Build: "Compiled successfully" with route summary

### Common Issues

| Error | Solution |
|-------|----------|
| "Cannot find module" | Run `npm install` |
| Type error in component | Check prop types match usage |
| ESLint warning | Fix or add disable comment with justification |
| Build fails | Check for syntax errors, missing imports |

## Quick Fixes

### Missing dependencies
```bash
npm install
```

### Clear build cache
```bash
rm -rf .next && npm run build
```

### Fix auto-fixable lint issues
```bash
npm run lint -- --fix
```

## Checklist

- [ ] Run lint - no errors
- [ ] Run type check - no errors
- [ ] Run build - completes successfully
- [ ] Report any issues found
- [ ] Suggest fixes for any failures
