---
name: kpi-code-quality
description: KPI for measuring and improving code quality. Covers lint errors, type safety, test coverage, and verification pass rates. Use to ensure code meets quality standards.
---

# KPI: Code Quality

**Definition**: The degree to which code is correct, maintainable, and follows established patterns.

## Why This Matters

Code quality directly impacts:
- **Velocity** - Clean code is easier to change
- **Reliability** - Quality code has fewer bugs
- **Collaboration** - Consistent patterns reduce friction

## Metrics

### Primary Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Lint Errors | 0 | `npm run lint:check` |
| Type Errors | 0 | `npm run typecheck` |
| Test Pass Rate | 100% | `npm run test` |
| Build Success | Yes | `npm run build` |

### Secondary Metrics

| Metric | Target | Measurement |
|--------|--------|-------------|
| Test Coverage | >80% | Coverage report |
| Cyclomatic Complexity | <10 per function | Static analysis |
| Code Duplication | <5% | Duplicate detection |

## Measurement

### Verification Pipeline

The primary quality gate is:
```bash
./verify.sh --ui=false
```

This runs:
1. Format check
2. Lint check
3. Type check
4. Unit tests
5. Build

All stages must pass.

### Individual Checks

```bash
npm run format:check  # Formatting
npm run lint:check    # Linting
npm run typecheck     # TypeScript
npm run test          # Tests
npm run build         # Build
```

## Improvement Strategies

### 1. Fix Forward

When you encounter an error:
1. Fix it immediately
2. Record the pattern in typescript-coding skill
3. Prevent recurrence through documentation

### 2. Type Everything

Eliminate `any` types. Strong types catch bugs at compile time.

### 3. Test First

Write tests before or alongside implementation. Tests are documentation that runs.

### 4. Follow Patterns

Use established patterns from coding-patterns skill:
- Contract-port architecture
- Explicit dependency injection
- Hermetic primitives

### 5. Review Lint Rules

If a lint rule is consistently violated:
- Either the rule is wrong (propose removing it)
- Or the pattern is wrong (fix the code)

## Quality Checklist

Before creating a PR:

- [ ] `npm run lint:check` passes
- [ ] `npm run typecheck` passes
- [ ] `npm run test` passes
- [ ] `npm run build` passes
- [ ] No `any` types added
- [ ] New code has tests
- [ ] Error handling follows patterns

## Blockers to Watch

| Issue | Detection | Resolution |
|-------|-----------|------------|
| Lint errors | lint:check fails | Run `npm run lint` to auto-fix |
| Type errors | typecheck fails | Fix types, avoid `any` |
| Test failures | test fails | Debug and fix tests |
| Build errors | build fails | Check for missing exports |

## Anti-Patterns

- **Disabling rules** - Don't `// biome-ignore` without good reason
- **Using `any`** - Defeats the purpose of TypeScript
- **Skipping tests** - Untested code is broken code waiting to happen
- **Copy-paste** - Duplicated code diverges and rots
