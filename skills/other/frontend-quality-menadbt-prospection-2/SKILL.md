---
name: frontend-quality
description: Runs frontend quality checks including TypeScript, ESLint, and tests. Use before commits, PRs, or when the user says "check frontend", "run frontend tests", "lint frontend".
allowed-tools: Bash(pnpm type-check), Bash(pnpm lint:*), Bash(pnpm lint), Bash(pnpm test:*), Bash(pnpm test), Bash(pnpm build)
---

# Frontend Quality Checks

Runs TypeScript type checking, ESLint, and tests for the frontend.

## Quick Check

```bash
cd front && pnpm type-check && pnpm lint
```

## 1. TypeScript Type Check

```bash
cd front && pnpm type-check
```

Checks all TypeScript files without emitting output.

### Common Type Errors

**Missing null check in page**:
```typescript
// Error: Build fails
export default function Page() {
  const { user } = useUser();
  return <Content userId={user.id} />; // user might be undefined!
}

// Fix: Add null check
export default function Page() {
  const { user } = useUser();
  if (!user) return null; // Required!
  return <Content userId={user.id} />;
}
```

**API type mismatch**:
```bash
# Regenerate types from backend
pnpm run generate:api
```

## 2. ESLint

Check:
```bash
cd front && pnpm lint
```

Auto-fix:
```bash
cd front && pnpm lint:fix
```

### Common Lint Issues

**Unused imports**: Auto-fixed by `lint:fix`

**Missing dependencies in useEffect**:
```typescript
// Warning: Missing dependency
useEffect(() => {
  fetchData(userId);
}, []); // userId missing

// Fix: Add all dependencies
useEffect(() => {
  fetchData(userId);
}, [userId]);
```

## 3. Tests (Vitest)

All tests:
```bash
cd front && pnpm test
```

Watch mode:
```bash
cd front && pnpm test:watch
```

Specific file:
```bash
cd front && pnpm test src/lib/utils.test.ts
```

## 4. Build Check

Full production build (catches more errors):
```bash
cd front && pnpm build
```

### Common Build Errors

**Dynamic import issues**:
- Ensure client components have `'use client'` directive
- Check for server-only code in client components

**Environment variables**:
- `NEXT_PUBLIC_*` for client-side
- Non-prefixed for server-side only

## Pre-commit Checklist

```bash
cd front

# 1. Type check
pnpm type-check

# 2. Lint
pnpm lint

# 3. Run tests
pnpm test

# 4. (Optional) Full build
pnpm build
```

## Configuration Files

| File | Purpose |
|------|---------|
| `tsconfig.json` | TypeScript configuration |
| `eslint.config.mjs` | ESLint rules |
| `vitest.config.ts` | Test configuration |
| `next.config.ts` | Next.js configuration |
