---
name: lint-fixer
description: Expert assistant for analyzing and fixing linting and formatting issues in the KR92 Bible Voice project using Biome and TypeScript. Use when fixing lint errors, resolving TypeScript issues, applying code formatting, or reviewing code quality.
---

# Lint Fixer

## Context Files (Read First)

For project conventions, read from `Docs/context/`:
- `Docs/context/conventions.md` - Code style and patterns
- `Docs/context/repo-structure.md` - File organization

## Quick Commands

```bash
npx @biomejs/biome check --write .  # Auto-fix lint + format
npx tsc --noEmit                    # Type checking
npm run typecheck:ci                # CI type check
```

## Workflow

1. **Assess** - `npx @biomejs/biome lint .`
2. **Auto-fix** - `npx @biomejs/biome check --write .`
3. **Manual fixes** - Priority: errors → warnings → infos
4. **Verify** - `npx tsc --noEmit && npx @biomejs/biome check .`

## Priority Order

1. **TypeScript errors** - Breaks builds
2. **Biome errors** - Critical issues
3. **Biome warnings** - Important
4. **Biome infos** - Nice to have

## References

- **Fix patterns**: See [references/patterns.md](references/patterns.md) for common fixes
- **Biome docs**: https://biomejs.dev/

## Related Skills

| Situation | Delegate To |
|-----------|-------------|
| CI failures after fixes | `ci-doctor` |
| Need refactoring | `code-refactoring` |
| Test failures | `test-writer` |
