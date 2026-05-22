---
name: bun-test-gen
description: Generate Bun test files following x4-mono conventions and patterns
---

# Bun Test Generator

Generate test files for x4-mono source files using Bun's built-in test runner.

## Arguments

The user provides a source file path. If no path given, ask which file to generate tests for.

## Test Patterns by Source Location

### tRPC Router Tests (`apps/api/src/routers/*.ts`)

```typescript
import { describe, test, expect } from 'bun:test';
import { createCallerFactory } from '../trpc';
import { appRouter } from '../routers';
import type { Context } from '../trpc';
import { createMockDb, createTestUser, TEST_USER_ID } from './helpers';

function createTestContext(overrides: Partial<Context> = {}): Context {
  return {
    db: createMockDb(),
    user: null,
    req: new Request('http://localhost:3002'),
    ...overrides,
  };
}

const createCaller = createCallerFactory(appRouter);
```

For each procedure, test:

- Happy path with valid input
- Invalid input (BAD_REQUEST)
- Unauthenticated access (UNAUTHORIZED) for protected procedures
- Authorization/ownership checks (FORBIDDEN)
- NOT_FOUND for missing resources
- Edge cases (empty results, pagination boundaries)

### Middleware Tests (`apps/api/src/middleware/*.ts`)

```typescript
import { describe, test, expect } from 'bun:test';
// Test using app.request()
```

### Zod Schema Tests (`packages/shared/types/*.ts`, `packages/shared/utils/validators.ts`)

```typescript
import { describe, test, expect } from 'bun:test';
// Import schemas directly
// Use .safeParse() for validation tests
// Use .parse() for default value tests
```

For each schema, test:

- Valid input with all required fields
- Valid input with optional fields omitted
- Each required field missing
- Invalid types for each field
- Boundary values (min/max length, min/max number)
- Default values applied correctly
- Enum values accepted/rejected

### Unit Tests (`apps/api/src/lib/*.ts`, `packages/shared/utils/*.ts`)

```typescript
import { describe, test, expect } from 'bun:test';
// Direct function import and test
```

### Component Tests (`apps/web/src/components/*.tsx`)

```typescript
import { describe, test, expect } from 'bun:test';
// Uses @testing-library/react
```

## Test File Placement

- `apps/api/src/routers/foo.ts` → `apps/api/src/__tests__/foo.test.ts`
- `apps/api/src/lib/foo.ts` → `apps/api/src/__tests__/foo.test.ts`
- `apps/api/src/middleware/foo.ts` → `apps/api/src/__tests__/foo.test.ts`
- `packages/shared/utils/foo.ts` → `packages/shared/utils/foo.test.ts` (co-located)
- `packages/shared/types/foo.ts` → `packages/shared/types/foo.test.ts` (co-located)
- `packages/*/src/foo.ts` → `packages/*/src/__tests__/foo.test.ts`

## Conventions

- Always import from `bun:test` (never jest)
- Use `describe` blocks grouped by function/procedure name
- Use descriptive test names: "returns X when Y", "throws Z for invalid input"
- Use section comments: `// --- functionName ---`
- Use `toMatchObject` for partial error matching: `rejects.toMatchObject({ code: "NOT_FOUND" })`
- Use `createMockDb` helper for database mocks in API tests
- Test the tRPC error codes: `NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `BAD_REQUEST`

## Workflow

1. Read the source file to understand exports and logic
2. Determine the test pattern based on file location
3. Check for existing test helpers in `apps/api/src/__tests__/helpers.ts`
4. Generate the test file
5. Run `bun test <test-file-path>` to verify tests pass
