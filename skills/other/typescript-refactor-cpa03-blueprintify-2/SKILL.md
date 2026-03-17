---
name: typescript-refactor
description: Safely refactor TypeScript code while maintaining type safety and test coverage. Includes verification steps.
---

# TypeScript Refactor Skill

Safely refactor TypeScript code with full verification.

## Pre-Refactor Checklist

1. Run current tests to establish baseline:

   ```bash
   npm run test
   ```

2. Run type check:

   ```bash
   npm run typecheck
   ```

3. Note current state as baseline

## Refactoring Patterns

### Extract Function

```typescript
// Before
function process(data: Data) {
  // complex validation logic
  if (!data.field1) throw new Error("field1 required");
  if (!data.field2) throw new Error("field2 required");
  // ... more processing
}

// After
function validateData(data: Data): void {
  if (!data.field1) throw new Error("field1 required");
  if (!data.field2) throw new Error("field2 required");
}

function process(data: Data) {
  validateData(data);
  // ... more processing
}
```

### Extract Component (React)

```typescript
// Before: Large component with repeated patterns
// After: Smaller, focused components with clear props
```

### Rename Symbol

```bash
# Find all usages first
grep -r "oldName" --include="*.ts" --include="*.tsx" src/
```

## Post-Refactor Verification

1. Run type check:

   ```bash
   npm run typecheck
   ```

2. Run tests:

   ```bash
   npm run test
   ```

3. Run linter:

   ```bash
   npm run lint
   ```

4. Build project:
   ```bash
   npm run build
   ```

## Rules

- Never change behavior during refactor
- One refactor type at a time
- Commit after each successful refactor
- If tests fail, rollback immediately
