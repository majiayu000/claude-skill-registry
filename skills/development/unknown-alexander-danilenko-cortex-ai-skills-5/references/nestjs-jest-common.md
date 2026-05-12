# Jest Testing Standards — Common (NestJS Backend)

Applies to **all** Jest tests in a NestJS backend. Read before writing or modifying any test. Also read the type-specific file for the test type being written.

## Which Instructions File to Read

- Writing a `.spec.ts` file? → Read `nestjs-jest-unit-tests.md`
- Writing a `.contract-spec.ts` file? → Read `AGENTS.jest.contract-tests.md`
- Writing a `.e2e-spec.ts` file? → Read `AGENTS.jest.e2e-tests.md` (planned)

## Structure & Naming

### File Placement (co-located)

`__tests__/` MUST live as a sibling **inside the same directory** as the source file it tests.

```text
src/core/{module}/service/__tests__/{name}.service.spec.ts
src/core/{module}/service/__tests__/{name}.service--{method}.spec.ts
src/core/{module}/service/strategy/__tests__/{name}.strategy--{method}.spec.ts
src/core/{module}/group/__tests__/{name}.group.spec.ts
src/core/{module}/listener/__tests__/{name}.listener.spec.ts
```

### Per-Method File Splitting

- **MUST** use the `--method-kebab` double-dash convention to separate the service name from the method scope (e.g., `--cancel.spec.ts`).
- **SHOULD** coalesce trivial methods whose tests total fewer than ~40 lines into a single `--queries` file to avoid tiny file proliferation.

```text
{name}.service--{method-kebab}.spec.ts          # per-method
{name}.service--queries.spec.ts                 # coalesced trivial getters/lookups
{name}.service.spec.ts                          # unsplit (under threshold)
```

- **MUST** split when the test file exceeds 400 lines OR the service has 8+ public methods with decisions.
- **SHOULD** keep a single file when fewer than 5 testable methods AND tests are under 300 lines total.

## Shared Setup & Fixtures

- **MUST** extract shared `TestingModule` setup into `__tests__/__setup__/` when splitting across multiple spec files.
- **MUST** place static test data in `__tests__/__fixtures__/`.
- **MUST** define a context interface that types all objects returned from the factory.
- **MUST** call the factory in `beforeEach` (unit tests) or `beforeAll` (contract tests).

```text
__tests__/
  __setup__/
    {name}.service.setup.ts           # module factory
  __fixtures__/
    user.ts                           # static mock data
  {name}.service--verify.spec.ts
  {name}.service--queries.spec.ts
```

**Unit test setup factory** (mock providers via `useValue`):

```typescript
// __tests__/__setup__/{name}.service.setup.ts
import { Test } from "@nestjs/testing";
import { MyService } from "../../my.service";
import { DepService } from "../../../dep/service";

import type { TestingModule } from "@nestjs/testing";

export interface MyServiceTestContext {
  module: TestingModule;
  service: MyService;
  depService: DepService;
}

export async function createMyServiceModule(): Promise<MyServiceTestContext> {
  const module = await Test.createTestingModule({
    providers: [
      MyService,
      { provide: DepService, useValue: { doWork: jest.fn() } },
    ],
  }).compile();

  return {
    module,
    service: module.get(MyService),
    depService: module.get(DepService),
  };
}
```

**Contract test setup factory** (real providers only, no mocks):

```typescript
// __tests__/__setup__/{name}.service.setup.ts
import { Test } from "@nestjs/testing";
import { ExternalApiService } from "../../external-api.service";

import type { TestingModule } from "@nestjs/testing";

export interface ExternalApiTestContext {
  module: TestingModule;
  service: ExternalApiService;
}

export async function createExternalApiModule(): Promise<ExternalApiTestContext> {
  const module = await Test.createTestingModule({
    providers: [ExternalApiService],
  }).compile();

  return {
    module,
    service: module.get(ExternalApiService),
  };
}
```

## Naming Conventions

- **MUST** organize as `describe(ServiceName @tag)` → `describe(method)` → `describe(scenario)`.
- **MUST** name tests as `it("should [outcome] when [condition]")`.
- **MUST** use `@ci` tag for unit tests, `@contract` tag for contract tests, and `@smoke` for critical-path unit tests.

```typescript
// WRONG
describe("tests", () => {
  it("works", () => {
    /* ... */
  });
});

// RIGHT
describe("ExternalApiService @contract", () => {
  describe("search", () => {
    it("should return the matching record when searching by ID alone", () => {
      /* ... */
    });
  });
});
```

## Test Documentation

Every `it()` MUST have a TSDoc block. Use multiline TSDoc format — never single-line.

| Field | Required | Purpose |
| --- | --- | --- |
| `@what` | **yes** | One sentence: what behavior is verified. |
| `@expected` | **yes** | The observable outcome: return value, exception, or side-effect. |
| `@prerequisites` | no | Non-obvious mock setup, data state, or environment. MUST omit when trivial. |
| `@conditions` | no | The action/input that triggers the behavior. MUST omit when obvious from the `it()` name or test body. |

File-level and top-level `describe()` blocks SHOULD have a TSDoc comment with `@remarks` describing the scope of the suite.

```typescript
/** Happy path — prerequisites/conditions obvious from code, omit them. */

/**
 * @what Disconnect resolves for a valid resource deletion.
 * @expected Resolves without throwing.
 */
it("should resolve when resource is deleted successfully", async () => {
  jest
    .spyOn(storageService, "deleteResource")
    .mockResolvedValue(undefined as never);
  await expect(
    strategy.disconnect("usr_123", "res_abc"),
  ).resolves.toBeUndefined();
});

/** Error path — prerequisites explain the non-obvious setup. */

/**
 * @what Disconnect silently succeeds for already-removed resource.
 * @prerequisites deleteResource rejects with resource_missing.
 * @expected Resolves without throwing; error is swallowed.
 */
it("should silently succeed on resource_missing error", async () => {
  jest
    .spyOn(storageService, "deleteResource")
    .mockRejectedValue(
      new ResourceNotFoundError("No such resource: 'res_gone'"),
    );
  await expect(
    strategy.disconnect("usr_123", "res_gone"),
  ).resolves.toBeUndefined();
});
```

## Assertions

- **MUST** assert outputs (return values or thrown exceptions), not wiring.
- **MUST** use `toEqual` for values, `toBe` for identity, and `toThrow(Class)` for errors.
- **MUST NOT** use `toHaveBeenCalledWith` as the sole assertion; use it only to confirm skipped paths or when no output exists.
- **MUST** assert translated/project exceptions, not raw SDK errors.

```typescript
// WRONG — sole assertion is on wiring, not output
it("should call dependency", async () => {
  await service.process(input);
  expect(depService.doWork).toHaveBeenCalledWith(input);
});

// RIGHT — assert output, toHaveBeenCalledWith is secondary
it("should return processed result", async () => {
  jest.spyOn(depService, "doWork").mockResolvedValue(expected);
  const result = await service.process(input);
  expect(result).toEqual(expected);
});
```

## Anti-Patterns

- **MUST NOT** use snapshot assertions for business objects.
- **MUST NOT** chase coverage on branchless code — line coverage for no-branch code is noise.
- **MUST NOT** share mutable state between tests; tests **MUST** be order-independent.
- **MUST NOT** write one-assert-per-line tests; group assertions by decision boundaries.

## Import Ordering

- **MUST** order imports: external libraries first, internal modules second, type-only imports last.

```typescript
// WRONG — type imports mixed with value imports
import type { TestingModule } from "@nestjs/testing";
import { Test } from "@nestjs/testing";
import type { MyService } from "../my.service";
import { DepService } from "../../dep/service";

// RIGHT — type imports grouped at bottom
import { Test } from "@nestjs/testing";
import { DepService } from "../../dep/service";

import type { TestingModule } from "@nestjs/testing";
import type { MyService } from "../my.service";
```

## Type Safety

- **MUST NOT** use `any` — use `unknown`, `as never`, or `as unknown as Type` instead.
- **MUST** add explicit return types on all helper and factory functions.
- **MUST** use `Array<T>` instead of `T[]` for non-simple element types.
- **SHOULD** use `@ts-expect-error` with a justification comment when casting is unavoidable.
- **MUST** use the `satisfies` operator instead of `as` for type assertions where possible.
