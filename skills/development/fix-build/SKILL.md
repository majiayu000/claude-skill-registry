---
skill: fix-build
description: Diagnose and fix build or type errors
arguments: optional error message or file path
---

# Fix Build Errors

Systematically diagnose and fix build, TypeScript, or compilation errors.

## Process

### 1. Identify the Problem

If no specific error provided, run:
```bash
npm run build 2>&1
```

Capture and parse error output.

### 2. Categorize Errors

| Type | Pattern | Common Fix |
|------|---------|------------|
| Type error | `Type 'X' is not assignable` | Fix type mismatch |
| Missing module | `Cannot find module` | Install dep or fix import path |
| Missing export | `has no exported member` | Check export statement |
| Syntax error | `Unexpected token` | Fix syntax |
| JSX error | `Cannot use JSX` | Check tsconfig jsx setting |

### 3. Analyze Each Error

For each error:
1. Read the file at the specified line
2. Understand the context (what the code is trying to do)
3. Identify root cause (not just symptom)

### 4. Apply Fixes

Fix errors in dependency order:
1. Import/module errors first (they cause cascading errors)
2. Type definition errors
3. Implementation errors

### 5. Verify

```bash
npm run build
```

If new errors appear, repeat. Continue until build passes.

### 6. Run Full Validation

```bash
npm run lint
npm test
```

Ensure fixes didn't break anything else.

## Common Fixes

**Missing types:**
```bash
npm install -D @types/[package]
```

**Path alias issues:**
Check `tsconfig.json` paths configuration.

**React component type errors:**
```tsx
// Add proper typing
const Component: React.FC<Props> = ({ prop }) => { ... }
```

**Async/await issues:**
Ensure function is marked `async` and return type includes `Promise`.
