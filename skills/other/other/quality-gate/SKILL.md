---
name: quality-gate
description: Automates quality checks (typecheck, lint, tests, build) and blocks commits that don't pass. Use before any commit to validate code quality.
allowed-tools: Bash, Read, Grep
---

# Quality Gate - Quality Verification System

## Purpose

This skill automates quality checks:

- **Typecheck** - TypeScript errors
- **Lint** - Code patterns (ESLint)
- **Build** - Build verification
- **Tests** - Unit and E2E tests
- **Blocks** commits that don't pass

---

## Commands

### 1. TypeScript Check

```bash
bun run typecheck
# or
bunx tsc --noEmit
```

### 2. ESLint Check

```bash
bun run lint
# or
bunx eslint . --ext .ts,.tsx
```

### 3. Build Check

```bash
bun run build
```

### 4. Unit Tests

```bash
bun run test
# or
bunx vitest run
```

### 5. E2E Tests

```bash
bun run test:e2e
# or
bunx playwright test
```

### 6. All Checks (RECOMMENDED)

```bash
bun run typecheck && bun run lint && bun run test && bun run test:e2e && bun run build
```

---

## Execution Flow

```
1. TYPECHECK → If fail: STOP and list errors
        ↓
2. LINT → If fail: STOP and list errors
        ↓
3. UNIT TESTS → If fail: STOP and list failures
        ↓
4. E2E TESTS → If fail: STOP and list failures
        ↓
5. BUILD → If fail: STOP and list errors
        ↓
RESULT: ✅ APPROVED or ❌ REJECTED
```

---

## Common TypeScript Errors

### Type 'X' is not assignable to type 'Y'

```typescript
// ERROR
const value: string = 123;

// FIX
const value: number = 123;
```

### Object is possibly 'undefined'

```typescript
// ERROR
const name = user.name.toUpperCase();

// FIX
const name = user?.name?.toUpperCase() ?? '';
```

### Property 'X' does not exist on type 'Y'

```typescript
// ERROR
const age = user.age; // age doesn't exist

// FIX
interface User {
	name: string;
	age?: number;
}
```

---

## Common ESLint Errors

### @typescript-eslint/no-explicit-any

```typescript
// ERROR
function parse(data: any) {}

// FIX
function parse(data: unknown) {}
```

### @typescript-eslint/no-unused-vars

```typescript
// ERROR
const unused = 'value';

// FIX - remove or prefix with _
const _unused = 'value';
```

### react-hooks/exhaustive-deps

```typescript
// ERROR
useEffect(() => {
	fetchData(userId);
}, []); // missing userId

// FIX
useEffect(() => {
	fetchData(userId);
}, [userId]);
```

---

## Output Format

### Approved

```markdown
## QUALITY GATE - APPROVED

### Checks Executed

| Check      | Status        | Time  |
| ---------- | ------------- | ----- |
| TypeScript | ✅ Pass       | 3.2s  |
| ESLint     | ✅ Pass       | 5.1s  |
| Unit Tests | ✅ 42/42 Pass | 8.3s  |
| E2E Tests  | ✅ 15/15 Pass | 45.2s |
| Build      | ✅ Pass       | 32.1s |

**STATUS: APPROVED** - Ready to commit
```

### Rejected

```markdown
## QUALITY GATE - REJECTED

### Checks Executed

| Check      | Status      |
| ---------- | ----------- |
| TypeScript | ❌ 3 errors |

### TypeScript Errors

#### Error 1: server/routers/example.ts:45
```

Type 'string | undefined' is not assignable to type 'string'.

````

**Suggested fix:**
```typescript
const name: string = input.name ?? "";
````

**STATUS: REJECTED** - Fix 3 errors before commit

````

---

## Quick Checks

### Fast Check (typecheck + lint only)
```bash
bun run typecheck && bun run lint
````

### Full Check (everything)

```bash
bun run typecheck && bun run lint && bun run test && bun run test:e2e && bun run build
```

### Modified Files Only

```bash
git diff --name-only | grep -E "\.(ts|tsx)$" | xargs bunx eslint
```

---

## Pre-Commit Checklist

- [ ] `bun run typecheck` passes?
- [ ] `bun run lint` passes?
- [ ] `bun run test` passes?
- [ ] `bun run test:e2e` passes?
- [ ] `bun run build` passes?
- [ ] No `any` in code?
- [ ] No unused variables?
- [ ] No debug console.log?

---

## Scripts (package.json)

```json
{
	"scripts": {
		"typecheck": "tsc --noEmit",
		"lint": "eslint . --ext .ts,.tsx",
		"lint:fix": "eslint . --ext .ts,.tsx --fix",
		"test": "vitest run",
		"test:watch": "vitest",
		"test:e2e": "playwright test",
		"test:e2e:ui": "playwright test --ui",
		"test:all": "bun run typecheck && bun run lint && bun run test && bun run test:e2e",
		"build": "next build"
	}
}
```

---

## Critical Rules

1. **NEVER commit with errors** - All checks must pass
2. **RUN IN ORDER** - typecheck → lint → test → e2e → build
3. **FIX IMMEDIATELY** - Errors cannot accumulate
4. **DON'T USE --force** - Solve problems, don't ignore

---

## Progressive Disclosure

For automated quality checks:

- **[scripts/check-all.sh](scripts/check-all.sh)** - Run all quality gates in sequence

### Quick Command

```bash
# Run all quality gates
bash .claude/skills/quality-gate/scripts/check-all.sh
```

---

## Version

- **v2.1.0** - Added progressive disclosure with check-all script
- **v2.0.0** - Generic template
