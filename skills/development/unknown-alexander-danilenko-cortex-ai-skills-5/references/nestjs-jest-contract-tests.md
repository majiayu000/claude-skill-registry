# Jest Contract Testing Standards (NestJS Backend)

> **PREREQUISITE:** Read `nestjs-jest-common.md` BEFORE this file. Rules from that file apply here and are not repeated.

**Not covered here:** file placement, naming conventions, TSDoc format, import ordering, type safety rules, assertion philosophy, anti-patterns. Those are in `nestjs-jest-common.md`.

## Purpose

- Contract tests verify that an external API behaves as the application expects: response shape, status codes, error format, and pagination behavior.
- Contract tests catch upstream breaking changes before they hit production.
- Contract tests do **NOT** test internal business logic — that is what unit tests are for.

## What to Test

- **MUST** test response envelope shape (fields, types, nullability).
- **MUST** test known-entity lookups — a stable fixture returns expected data.
- **MUST** test error response structure.
- **SHOULD** test input parameter behavior (filters, wildcards, pagination offsets).
- **SHOULD** test edge cases (limit boundaries, empty results, mismatched criteria).

## What NOT to Test

- **MUST NOT** test internal service logic or branching.
- **MUST NOT** assert exact result counts for broad queries — use `toBeGreaterThanOrEqual`.
- **MUST NOT** assert volatile data (addresses, phone numbers).
- **MUST NOT** test performance or latency.

## Lifecycle

- **MUST** use `beforeAll`/`afterAll` (not `beforeEach`/`afterEach`).
- **MUST** follow this pattern: single API call in `beforeAll`, cache the response, multiple `it()` blocks assert against the cached response.
- **MUST** call `await module.close()` in `afterAll`.
- Each `describe` block **MAY** make its own `beforeAll` if it needs a different query.

```typescript
// WRONG — beforeEach makes N API calls (one per test)
beforeEach(async () => {
  result = await service.search(buildInput({ id: KnownRecord.id }));
});

// RIGHT — beforeAll makes 1 API call, all it() blocks share the cached response
beforeAll(async () => {
  const ctx = await createExternalApiModule();
  module = ctx.module;
  service = ctx.service;
  result = await service.search(buildInput({ id: KnownRecord.id }));
}, API_TIMEOUT);

afterAll(async () => {
  await module.close();
});
```

## Timeout Management

- **MUST** export an `API_TIMEOUT` constant from the `__setup__/` file (recommended value: 15,000ms).
- **MUST** pass `API_TIMEOUT` as the second argument to every `it()` block that makes a live API call.
- **MUST** pass `API_TIMEOUT` to `beforeAll` blocks that contain API calls.
- **MUST NOT** set a global Jest timeout.

Constant definition in `__setup__/`:

```typescript
/** Timeout for live external API calls (ms). */
export const API_TIMEOUT = 15_000;
```

Usage in spec files:

```typescript
it(
  "should return the exact record when searching by ID alone",
  async () => {
    const result = await service.search(buildInput({ id: KnownRecord.id }));
    expect(result.result_count).toBe(1);
  },
  API_TIMEOUT,
);
```

Usage in `beforeAll`:

```typescript
beforeAll(async () => {
  const ctx = await createExternalApiModule();
  module = ctx.module;
  service = ctx.service;
  response = await service.search(buildInput({ id: KnownRecord.id }));
}, API_TIMEOUT);
```

## Known Fixture Pattern

- **MUST** use a stable, well-known entity as the test anchor.
- **MUST** store the fixture in `__fixtures__/` as a `const` object literal using `as const`.
- **MUST** include only immutable or stable fields (identifiers, classifications).
- **MUST NOT** include volatile data (addresses, phone numbers, dates).
- **MUST** document the fixture with a comment explaining its stability and how to reverify it.

```typescript
/**
 * Known record fixture for contract test assertions.
 *
 * @remarks
 * Source: https://api.example.com/registry
 * Record ID "ABC-12345" is a stable public entry. Classification and name
 * values were pinned on 2026-03-19 and may change if the record is updated.
 * Re-verify periodically by running: `npm run test:contract`
 */
export const KnownRecord = {
  id: "ABC-12345",
  firstName: "JOHN",
  lastName: "SMITH",
  city: "NEW YORK",
  state: "NY",
  postalCodePrefix: "100",
  classification: "General Practice",
} as const;
```

## No-Mock Policy

| In contract tests... | DO | DO NOT |
| --- | --- | --- |
| Service under test | Provide as real class in `providers` | Mock with `useValue` |
| External API calls | Let them hit the real API | Intercept with `jest.spyOn` |
| Helper utilities | Write as plain functions | Wrap in `jest.fn()` |
| Service import in setup | Use value import (`import { Svc }`) | Use `import type` |
| Service import in spec | **MAY** use `import type` | — |
| `jest.mock()` | — | Never use in contract tests |

## Setup Helpers

- **MUST** create an input builder function with sensible defaults.
- **SHOULD** create index/lookup helpers for O(1) assertions.
- **MUST** export all helpers from the `__setup__/` file.
- **MUST** type `Promise.all` tuples with `satisfies [TypeA, TypeB]` — not `as`.

Full example:

```typescript
import { chain } from "lodash";
import { Test } from "@nestjs/testing";
import { ExternalApiService } from "../../external-api.service";
import { SearchInput } from "../../../dto";
import { RecordType } from "../../../enum";

import type { TestingModule } from "@nestjs/testing";
import type { SearchResult } from "../../../schema";

/** Timeout for live external API calls (ms). */
export const API_TIMEOUT = 15_000;

export interface ExternalApiTestContext {
  module: TestingModule;
  service: ExternalApiService;
}

/**
 * Create a NestJS testing module with the external API service.
 */
export async function createExternalApiModule(): Promise<ExternalApiTestContext> {
  const module = await Test.createTestingModule({
    providers: [ExternalApiService],
  }).compile();

  return {
    module,
    service: module.get(ExternalApiService),
  };
}

/**
 * Build a search input with sensible defaults.
 */
export function buildInput(overrides: Partial<SearchInput>): SearchInput {
  const input = new SearchInput();
  input.record_type = RecordType.Individual;
  input.limit = 10;
  Object.assign(input, overrides);
  return input;
}

/**
 * Index search results by ID for O(1) lookups in assertions.
 */
export function indexById(
  results: SearchResult[],
): Record<string, SearchResult> {
  return chain(results)
    .keyBy((result) => result.id)
    .value();
}
```

`satisfies` usage for `Promise.all` tuples:

```typescript
const [withFilter, withoutFilter] = (await Promise.all([
  service.search(buildInput({ include_aliases: true, limit: 200 })),
  service.search(buildInput({ include_aliases: false, limit: 200 })),
])) satisfies [SearchResponse, SearchResponse];
```

## Assertion Helpers

- **SHOULD** extract small helper functions for repetitive type/shape checks into the test file itself (not into `__setup__/`).
- **MUST** place assertion helpers at the top of the file, before the `describe` block.
- **MUST** add explicit return types (`: void` for assertion helpers, or the appropriate type guard return for predicate helpers).

```typescript
/** Helper: check if a value is null or undefined. */
function isAbsent(value: unknown): value is null | undefined {
  return null === value || undefined === value;
}

/** Helper: assert a field is a string or absent (null/undefined). */
function expectStringOrAbsent(value: unknown): void {
  expect(isAbsent(value) || "string" === typeof value).toBe(true);
}

/** Helper: assert a field is a date string (YYYY-MM-DD) or absent. */
function expectDateOrAbsent(value: unknown): void {
  if (!isAbsent(value)) {
    expect(typeof value).toBe("string");
    expect(value).toMatch(/^\d{4}-\d{2}-\d{2}$/);
  }
}
```

## Resilience & Flaky APIs

- **MUST** use generous timeouts (10–15s) for all live API calls.
- **MUST** tag flaky tests with `@flaky` in the test description and exclude them from CI.
- **MUST NOT** add retry logic inside individual `it()` blocks.
- **MAY** use `jest.retryTimes(2)` at the `describe` level for known-unstable endpoints — include a comment explaining why.

## Checklist (for `.contract-spec.ts` files only)

- [ ] File uses `.contract-spec.ts` suffix.
- [ ] Uses `beforeAll`/`afterAll` lifecycle (not `beforeEach`/`afterEach`).
- [ ] Every live-call `it()` and `beforeAll` has an explicit `API_TIMEOUT` argument.
- [ ] No mocks on the service under test.
- [ ] Known fixture is stable and documented with reverification instructions.
- [ ] Assertion helpers have explicit return types.
- [ ] `npm run test:contract && npm run lint && npm run typecheck` pass.
