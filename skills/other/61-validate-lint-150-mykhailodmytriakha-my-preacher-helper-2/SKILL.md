---
name: 61-validate-lint-150
description: "[61] VALIDATE. Comprehensive code quality check combining ESLint, TypeScript compilation, and unused code detection. Runs full lint suite with detailed error reporting and fix suggestions. Use before commits, after major changes, or when ensuring code quality standards."
---

# Validate-Lint 150 Protocol

**Core Principle:** Code quality is non-negotiable. Run comprehensive checks before any delivery. Catch issues early, fix systematically.

## What This Skill Does

When you invoke this skill, you're asking AI to:
- **Run full lint suite** — ESLint + TypeScript + Unused code detection
- **Report all issues** — Categorized by severity and type
- **Provide fix guidance** — Specific suggestions for each error
- **Verify resolution** — Re-run checks after fixes
- **Quality gate** — Only proceed when all checks pass

## The 150% Lint Rule

| Dimension | 100% Core | +50% Enhancement |
|-----------|-----------|------------------|
| **ESLint** | No lint errors | + Consistent code style |
| **TypeScript** | Compiles cleanly | + Strict type checking |
| **Unused Code** | No unused locals | + Clean imports/exports |
| **Standards** | Follows rules | + Project conventions |

## Quality Check Framework

```
LINT INTEGRITY CHECK (100% Required)
├── ESLint Rules: No violations (style, logic, best practices)
├── TypeScript: Clean compilation, no type errors
├── Unused Code: No unused locals (parameters allowed for interfaces)
└── Import Hygiene: Clean, organized imports

ENHANCED VALIDATION (50% Enhancement)
├── Code Standards: Follows project conventions
├── Complexity: Cognitive complexity within limits
├── Consistency: Matches codebase patterns
└── Future-Proofing: No deprecated patterns
```

## Command Execution

from `my-preacher-helper/`
```bash
npm run lint:full
```

This runs three sequential checks:
1. `npm run lint` — ESLint code quality rules
2. `npm run compile` — TypeScript compilation check
3. `npm run lint:unused` — Unused code detection

## Error Classification

| Error Type | Severity | Action Required |
|------------|----------|----------------|
| **ESLint Error** | High | Must fix before commit |
| **TypeScript Error** | Critical | Blocks compilation |
| **Unused Local** | Medium | Remove or prefix with `_` |
| **Import Issues** | Medium | Clean up imports |

## Common Fix Patterns

### ESLint Fixes
```bash
# Auto-fix what can be auto-fixed
npm run lint -- --fix

# Manual fixes for complex issues
# - Add missing JSDoc
# - Fix import order
# - Remove duplicate code
```

### TypeScript Fixes
```typescript
// Fix common type errors
// 1. Add missing type annotations
// 2. Import missing types
// 3. Fix property access on union types
// 4. Add null/undefined checks
```

### Unused Code Fixes
```typescript
// For intentionally unused parameters (interfaces)
function handler(_unused: string) { /* ... */ }

// For temporarily unused locals
// eslint-disable-next-line @typescript-eslint/no-unused-vars
const tempVar = 'remove later';
```

## Execution Protocol

### Phase 1: Initial Check
```bash
npm run lint:full
```
- Capture all errors
- Categorize by type
- Prioritize critical issues

### Phase 2: Fix Cycle
```
For each error category:
├── Fix critical TypeScript errors first
├── Fix ESLint errors next
├── Clean unused code last
└── Re-run checks after each category
```

### Phase 3: Verification
```bash
npm run lint:full
```
- Confirm all issues resolved
- Document any intentional deviations
- Ready for commit/integration

## Success Criteria

- **All TypeScript errors resolved** (compilation clean)
- **Zero ESLint violations** (or documented exceptions)
- **No unused locals** (unused parameters allowed for interfaces)
- **Clean build** (no warnings that break standards)

## Failure Recovery

| Failure Mode | Detection | Recovery |
|--------------|-----------|----------|
| **Auto-fix breaks logic** | Tests fail after --fix | Revert auto-fixes, manual repair |
| **TypeScript strictness** | Overly complex type fixes | Use `any` with TODO comment |
| **Unused but needed** | Removal breaks functionality | Add `_` prefix or eslint-disable |
| **Import cycles** | Complex dependency issues | Restructure imports or use barrels |

## Integration Points

- **Pre-commit hooks** — Run automatically before commits
- **CI/CD pipeline** — Quality gate in deployment
- **Code review** — Manual verification of complex fixes
- **Refactoring** — Clean up after major changes

## Quality Metrics

| Metric | Target | Current Status |
|--------|--------|----------------|
| **ESLint Violations** | 0 | Check required |
| **TypeScript Errors** | 0 | Check required |
| **Unused Code** | 0 locals | Check required |
| **Build Success** | 100% | Must pass |

---

**Lint 150 ensures code quality standards are maintained at the highest level, preventing technical debt and maintaining codebase health.**
