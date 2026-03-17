---
name: add-test
description: Generate tests for an existing source file using Bun test runner
---

# Add Test Skill

Generate a test file for an existing source file in x4-mono using Bun's built-in test runner.

## Arguments

The user provides a source file path. If no path given, ask which file to generate tests for.

## Test Patterns by Source Location

| Source                          | Test Location                      | Pattern                  |
| ------------------------------- | ---------------------------------- | ------------------------ |
| `apps/api/src/routers/*.ts`     | `apps/api/src/__tests__/*.test.ts` | tRPC caller              |
| `apps/api/src/middleware/*.ts`  | `apps/api/src/__tests__/*.test.ts` | `app.request()`          |
| `apps/api/src/lib/*.ts`         | `apps/api/src/__tests__/*.test.ts` | Direct function calls    |
| `packages/shared/utils/*.ts`    | Co-located `*.test.ts`             | Direct function calls    |
| `packages/shared/types/*.ts`    | Co-located `*.test.ts`             | Zod `.safeParse()`       |
| `apps/web/src/components/*.tsx` | Co-located `*.test.tsx`            | `@testing-library/react` |

## tRPC Router Test Template

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

describe('routerName', () => {
  describe('list', () => {
    test('returns items', async () => {
      const caller = createCaller(createTestContext());
      const result = await caller.routerName.list({ limit: 20, offset: 0 });
      expect(result.items).toBeArray();
    });
  });

  describe('create', () => {
    test('throws UNAUTHORIZED for unauthenticated user', async () => {
      const caller = createCaller(createTestContext({ user: null }));
      await expect(caller.routerName.create({ name: 'test' })).rejects.toMatchObject({
        code: 'UNAUTHORIZED',
      });
    });
  });
});
```

## What to Test per Procedure/Function

For tRPC routers:

- Happy path with valid input
- Invalid input → `BAD_REQUEST`
- Unauthenticated → `UNAUTHORIZED` (protected procedures)
- Wrong owner → `FORBIDDEN`
- Missing resource → `NOT_FOUND`
- Edge cases (empty results, pagination boundaries)

For Zod schemas:

- Valid input with all required fields
- Valid input with optional fields omitted
- Each required field missing
- Invalid types for each field
- Boundary values (min/max length, min/max number)
- Default values applied correctly

For utility functions:

- Normal inputs → expected outputs
- Edge cases (empty strings, zero, null)
- Error conditions

## Mock Patterns

### Database Mock

Use `createMockDb()` from `apps/api/src/__tests__/helpers.ts`.

### Module Mock

```typescript
import { mock } from 'bun:test';
mock.module('@x4/database', () => ({ db: createMockDb() }));
```

**CRITICAL**: `bun mock.module` runs ALL test files in the same process. First call wins. Extract shared mocks into a single helper file.

### Environment Variables

`env.ts` validates eagerly at import time — set env vars BEFORE importing:

```typescript
process.env.DATABASE_URL ??= 'postgres://test:test@localhost/test';
```

## Conventions

- Always import from `bun:test` (never jest)
- Use `describe` blocks grouped by function/procedure name
- Use descriptive test names: "returns X when Y", "throws Z for invalid input"
- Use `toMatchObject` for partial error matching
- Test tRPC error codes: `NOT_FOUND`, `UNAUTHORIZED`, `FORBIDDEN`, `BAD_REQUEST`

## Workflow

1. Read the source file to understand exports and logic
2. Determine the test pattern based on file location
3. Check for existing test helpers in `apps/api/src/__tests__/helpers.ts`
4. Generate the test file at the correct location
5. Run `bun test <test-file-path>` to verify tests pass
