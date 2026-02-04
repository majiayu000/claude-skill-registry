---
name: git-hooks
description: Manage pre-commit hooks, performance optimization, and temp commits. Use when asked about "pre-commit slow", "commit taking forever", "skip hooks", "bypass pre-commit", "optimize commits", or multi-agent workflows. Covers fast Prettier-only hook, ESLint performance issues, and CI delegation strategy.
---

# Git Hooks Management

## Overview

This monorepo uses a **fast pre-commit hook** that only runs Prettier (~1-2 seconds). ESLint, typecheck, and tests run in CI.

**Why?** ESLint with TypeScript type-aware rules takes ~2 minutes per file due to project-wide type loading.

## Quick Reference

### Normal Commit (~1-2 seconds)

```bash
git commit -m "feat: add feature"
```

### Bypass All Checks (instant)

```bash
git commit --no-verify -m "message"
# or
TEMP_COMMIT=1 git commit -m "[temp] message"
```

### Auto-bypass Prefixes

Commits starting with these bypass the hook:

- `[temp]` - temporary, will squash
- `[wip]` - work in progress
- `[skip-ci]` - skip CI
- `[no-verify]` - explicit bypass

## What Runs Where

| Check      | Pre-commit    | CI  | Editor |
| ---------- | ------------- | --- | ------ |
| Prettier   | ✅ ~1s        | ✅  | ✅     |
| ESLint     | ❌ (too slow) | ✅  | ✅     |
| TypeScript | ❌ (too slow) | ✅  | ✅     |
| Tests      | ❌            | ✅  | manual |

## Performance History

Original hook: **~3-5 minutes**

- lint-staged (ESLint): ~2 minutes
- Turbo typecheck: ~2 minutes
- Vitest tests: ~90 seconds

Optimized hook: **~1-2 seconds**

- Prettier only on staged files

## Before Optimizing Your Hook

Benchmark each step to identify the bottleneck:

```bash
# Benchmark lint-staged
time npx lint-staged

# Benchmark ESLint directly on a single file
time pnpm exec eslint packages/core/src/index.ts --fix

# Benchmark Prettier directly
time pnpm exec prettier packages/core/src/index.ts --write

# Benchmark typecheck
time pnpm turbo run typecheck --filter='[HEAD]'
```

## Performance Comparison (This Repo)

| Approach                             | Time  | Notes                   |
| ------------------------------------ | ----- | ----------------------- |
| Full lint-staged (ESLint + Prettier) | ~2:05 | ESLint type-aware rules |
| ESLint alone on 1 file               | ~2:00 | Type loading dominates  |
| Prettier alone on 1 file             | ~0.3s | No type loading         |
| Prettier-only hook                   | ~1-2s | **Current approach**    |

## Why ESLint is Slow

The `.eslintrc.js` has type-aware linting enabled:

```javascript
parserOptions: {
  project: './tsconfig.eslint.json',  // This loads entire TS project
}
```

This makes ESLint load and parse the entire TypeScript project for every file. In a monorepo with many packages, this can take 2+ minutes even for a single file.

### Diagnosing Slow ESLint Rules

```bash
# Show timing for each rule
TIMING=1 pnpm exec eslint packages/core/src/index.ts

# Output shows which rules are slowest:
# Rule                          | Time (ms)
# @typescript-eslint/no-unsafe* | 45000ms  <- type-aware rules
```

### Options to Fix

1. **Remove `project` option** - disables type-aware rules, fastest
2. **Use `TIMING=1`** - identify and disable specific slow rules
3. **Skip ESLint in pre-commit** - run in CI only (current approach)
4. **Switch to Biome** - faster Rust-based linter

## Manual Checks Before PR

Run full validation before creating PRs:

```bash
# Full CI-equivalent check
pnpm turbo run typecheck lint test

# Or individually
pnpm exec eslint .
pnpm turbo run typecheck
pnpm test
```

## Hook Configuration

**Location:** `.husky/pre-commit`

Current hook does:

1. Get staged `.ts`, `.tsx`, `.json`, `.md`, `.yml` files
2. Run Prettier on them
3. Re-stage formatted files

## Troubleshooting

### Hook still slow?

Check if someone re-added lint-staged:

```bash
grep -n "lint-staged\|eslint" .husky/pre-commit
```

### Need ESLint locally?

Run it manually on specific files:

```bash
pnpm exec eslint packages/core/src/myfile.ts
```

### CI failing but local passes?

The hook doesn't run ESLint/typecheck. Run locally:

```bash
pnpm turbo run typecheck lint
```

### Common ESLint Errors in CI

**no-case-declarations**: Lexical declarations (`const`, `let`, `class`, `function`) in `switch` case blocks must be wrapped in braces:

```typescript
// ❌ Bad - ESLint error
switch (method) {
  case 'storage.get':
    const value = await db.get(key); // Error: Unexpected lexical declaration
    return res.json({ data: value });
}

// ✅ Good - wrap case block in braces
switch (method) {
  case 'storage.get': {
    const value = await db.get(key);
    return res.json({ data: value });
  }
}
```

This pattern is common in route handlers and bridge API implementations.
