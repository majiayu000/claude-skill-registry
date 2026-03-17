---
name: validate-frontend
description: Validates web frontend code (TypeScript, ESLint, unit tests) in the frontend/ directory
user-invocable: true
---

# Validate Frontend Skill

**CLAUDE: When this skill is invoked with `/validate-frontend`, run these commands in sequence:**
```bash
cd frontend && bun run type-check && bun run lint && bun run test -- --run
```

## Purpose
Validates the web frontend codebase (Vite + React + TypeScript) for type safety, lint compliance, and test correctness.

## Usage
```bash
/validate-frontend
```

## What It Validates

### Tier 0: TypeScript (fastest feedback)
```bash
cd frontend && bun run type-check
```
- Catches type errors before runtime
- Validates all `.ts` and `.tsx` files
- Uses `tsconfig.json` configuration

### Tier 1: ESLint
```bash
cd frontend && bun run lint
```
- React hooks rules
- React refresh compliance
- Import ordering
- Code style consistency

### Tier 2: Unit Tests
```bash
cd frontend && bun run test -- --run
```
- Runs Vitest in single-run mode
- Tests components, hooks, and utilities
- Uses Testing Library for React

## Full Validation Command
```bash
cd frontend && bun run type-check && bun run lint && bun run test -- --run
```

## Additional Commands

### E2E Tests (requires browser, run before PR)
```bash
cd frontend && bun run test:e2e
```

### Integration Tests
```bash
cd frontend && bun run test:integration
```

### Coverage Report
```bash
cd frontend && bun run test:coverage
```

### Interactive Test UI
```bash
cd frontend && bun run test:ui
```

## Success Criteria
- All TypeScript files compile without errors
- Zero ESLint violations
- All unit tests pass
- No type regressions

## Related Skills
- `frontend-design` - Design system compliance
- `accessibility-check` - WCAG compliance audit
- `design-review` - Visual consistency review
