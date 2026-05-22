---
name: pre-commit
description: Run code hygiene checks before committing. Use before git commits or when asked to check code quality.
---

# Pre-Commit Checks

Run hygiene checks before committing code.

## Quick Check Commands

```bash
# Type check (don't use pnpm typecheck)
pnpm build

# Lint
pnpm lint

# Tests
pnpm test
```

## Manual Checklist

### Before Every Commit

- [ ] `pnpm build` passes
- [ ] `pnpm lint` passes
- [ ] No `console.log` statements (except in CLI apps)
- [ ] No commented-out code blocks
- [ ] No `// TODO` without issue reference

### For Effect-TS Code

- [ ] No `async/await` - use `Effect.gen`
- [ ] No type casts - use `satisfies`
- [ ] Errors extend `Data.TaggedError`
- [ ] Services have proper Layer

### For Portal Components

- [ ] Pages are minimal
- [ ] Loading states have skeletons
- [ ] `"use client"` only where needed
- [ ] Barrel exports updated

### For New Files

- [ ] Added to barrel exports
- [ ] Types are exported if public API
- [ ] CLAUDE.md updated if new pattern

## Auto-Fix Common Issues

### Unused imports

```bash
pnpm lint --fix
```

### Sort imports/objects

ESLint perfectionist plugin handles this automatically.

## Instructions

1. Run `pnpm build` to check types
2. Run `pnpm lint` to check style
3. Review staged changes with `git diff --staged`
4. Flag any issues from checklist above
5. Suggest fixes for problems found
