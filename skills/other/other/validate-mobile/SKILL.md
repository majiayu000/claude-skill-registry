---
name: validate-mobile
description: Validates mobile app code (TypeScript, ESLint, Jest tests) in the frontend-mobile/ directory
user-invocable: true
---

# Validate Mobile Skill

**CLAUDE: When this skill is invoked with `/validate-mobile`, run these commands in sequence:**
```bash
cd frontend-mobile && bun run typecheck && bun run lint && bun test
```

## Purpose
Validates the mobile app codebase (Expo + React Native + NativeWind) for type safety, lint compliance, and test correctness.

## Usage
```bash
/validate-mobile
```

## What It Validates

### Tier 0: TypeScript (fastest feedback)
```bash
cd frontend-mobile && bun run typecheck
```
- Catches type errors before runtime
- Validates all `.ts` and `.tsx` files
- Uses TypeScript strict mode

### Tier 1: ESLint
```bash
cd frontend-mobile && bun run lint
```
- React hooks rules
- React Native specific rules
- TypeScript ESLint integration

### Tier 2: Unit Tests
```bash
cd frontend-mobile && bun test
```
- Runs Jest with jest-expo preset
- Tests components, hooks, and utilities
- Uses Testing Library for React Native

## Full Validation Command
```bash
cd frontend-mobile && bun run typecheck && bun run lint && bun test
```

## Additional Commands

### E2E Tests (requires iOS Simulator)
```bash
cd frontend-mobile && bun run e2e:build && bun run e2e:test
```

### Integration Tests
```bash
cd frontend-mobile && bun run e2e:integration
```

### Coverage Report
```bash
cd frontend-mobile && bun run test:coverage
```

### Watch Mode
```bash
cd frontend-mobile && bun run test:watch
```

## Port Configuration
**CRITICAL:** Mobile dev server uses port 8082 (port 8081 is reserved for Pierre MCP Server)
```bash
cd frontend-mobile && bun start  # Uses port 8082
```

## Success Criteria
- All TypeScript files compile without errors
- Zero ESLint violations
- All unit tests pass (135+ tests)
- No type regressions

## Related Skills
- `frontend-design` - Design system compliance (shares brand colors)
- `accessibility-check` - Accessibility audit (mobile accessibility)
