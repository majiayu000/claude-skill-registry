# Jest Unit Testing Standards (NestJS Backend)

> **PREREQUISITE:** Read `nestjs-jest-common.md` BEFORE this file. Rules from that file apply here and are not repeated.

**Not covered here:** file placement, naming conventions, TSDoc format, import ordering, type safety rules, assertion philosophy, anti-patterns. Those are in `nestjs-jest-common.md`.

## What to Test

- **MUST** test methods with decisions: branching (`if`/`switch`/ternary), error translation, conditional data transforms, state transitions, pagination/aggregation, prefix/type dispatch.

**Rule:** No `if`/`else`/`switch`/`throw`/`catch` in source method → no test needed.

## What NOT to Test

- **MUST NOT** test pass-through delegation: `detach(id) { await this.$dep.detach(id) }`
- **MUST NOT** test simple field mapping without conditional logic.
- **MUST NOT** test one-liner builders, getter/setter wrappers.
- **MUST NOT** test constructor-only services, `*.module.ts`, DTOs, barrel files, config files.
- **MUST NOT** test DTO validation decorators (`@IsString`, `@IsEnum`, `@Matches`, etc.) — these test the `class-validator` library, not application code.

Zero tests is correct when a service contains only delegation and mapping.

## Setup & Lifecycle

- **MUST** use `Test.createTestingModule()` for NestJS services.
- **MAY** instantiate pure utility classes with zero DI dependencies directly with `new`. Add a comment explaining why DI is not used.
- **MUST** make `beforeEach`/`afterEach` async when using `TestingModule`.
- **MUST** call `jest.clearAllMocks()` in `afterEach`.
- **MUST** call `await module.close()` in `afterEach` when a `TestingModule` was created.
- **MUST** set mock return values inside each `it()`, not in `beforeEach`.
- **MUST** declare `let module`, `let service`, and all mock variables inside the top-level `describe()` block — never at file scope. Node.js CJS has a global `module`; shadowing it at file scope crashes Jest.

```typescript
// WRONG — variables at file scope, mock returns in beforeEach
let module: TestingModule;
let service: MyService;

beforeEach(async () => {
  // ...
  jest.spyOn(depService, "doWork").mockResolvedValue(result); // WRONG: mock in beforeEach
});

// RIGHT — variables inside describe, mock returns inside it()
describe("MyService @ci", () => {
  let module: TestingModule;
  let service: MyService;

  beforeEach(async () => {
    /* compile module only */
  });
  afterEach(async () => {
    jest.clearAllMocks();
    await module.close();
  });

  it("should do something", async () => {
    jest.spyOn(depService, "doWork").mockResolvedValue(result); // RIGHT: mock in it()
    // ...
  });
});
```

## Module Setup Template

```typescript
// WRONG — imports array pulls real modules (integration, not unit)
const module = await Test.createTestingModule({
  imports: [DepModule],
  providers: [MyService],
}).compile();

// RIGHT — providers only, all deps mocked
const module = await Test.createTestingModule({
  providers: [
    MyService,
    { provide: DepService, useValue: { doWork: jest.fn() } },
  ],
}).compile();
```

- **MUST** use only the `providers` array (no `imports` array) in `createTestingModule()` — using `imports` pulls real modules and makes the test an integration test.
- **MUST** import dependency classes with value imports (`import { Dep }`), not type-only (`import type { Dep }`). NestJS needs the class reference at runtime for DI token resolution.

```typescript
import { Test } from "@nestjs/testing";
import { MyService } from "../service/my.service";
import { DepService } from "../../dep/service";

import type { TestingModule } from "@nestjs/testing";

describe("MyService @ci", () => {
  let module: TestingModule;
  let service: MyService;
  let depService: DepService;

  beforeEach(async () => {
    module = await Test.createTestingModule({
      providers: [
        MyService,
        { provide: DepService, useValue: { doWork: jest.fn() } },
      ],
    }).compile();

    service = module.get(MyService);
    depService = module.get(DepService);
  });

  afterEach(async () => {
    jest.clearAllMocks();
    await module.close();
  });

  // tests …
});
```

## Mocking & DI

- **MUST** mock all dependencies via DI (`useValue`); no real DB/API/HTTP.
- **MUST** only mock methods that are actually called — not every method on the dependency "for completeness."
- **SHOULD** use typed mock factories for reused mocks; inline object literals are OK for single-use.
- **MUST** use `jest.spyOn(...).mockResolvedValue(...)` / `mockRejectedValue(...)` for per-test overrides.
- **MUST** provide repositories via `{ provide: getRepositoryToken(Entity), useValue: { ... } }`.
- **MUST** provide custom tokens via `{ provide: "TOKEN", useValue: mock }`.
- **MUST** provide `forwardRef` dependencies directly (no `forwardRef` in tests).
- **MUST NOT** access private/protected members. If unavoidable, cast through `unknown` (never `any`) or use `@ts-expect-error` with a justification comment.
- **MUST NOT** use `any`; prefer `unknown`, `as never`, or `as unknown as Type`.
- Top-level `jest.mock()` is acceptable **only** for modules with side effects on import (e.g., error-tracking SDKs, auth libraries, HTTP clients, static JSON data). **MUST** prefer DI mocking for everything else.

## Common Patterns

- Pagination: chain `mockResolvedValueOnce` for each page.
- Private/protected access: `jest.spyOn(service as unknown as { client: () => Promise<T> }, "client")`.

## Special Cases

### Feature Flag Services

- Mock config/secret providers to return flag service credentials.
- Mock environment and timer services.
- Mock HTTP client factories (e.g., `Axios.create()`) to return a stub; never hit the network.
- Validate caching: second call uses cached client/data.

### Webhook Handlers

- Use minimal event stubs (id, type, data payload, request metadata).
- Mock all downstream services the handler dispatches to.
- Assert handler return values and event emission calls.
- In production mode with no event: expect a domain-specific exception.

### Query Builder Utilities

- Assert generated SQL and parameters separately; avoid snapshots.
- Never execute real queries in unit tests.

## Checklist (for `.spec.ts` files only)

- [ ] Each `it()` covers a real decision branch.
- [ ] The concrete bug it prevents can be named.
- [ ] Assertions on outputs, not mocks.
- [ ] Names follow `should [outcome] when [condition]`.
- [ ] TSDoc block with `@what` and `@expected` on every `it()`.
- [ ] No `any` types.
- [ ] Tests are independent — no shared mutable state.
- [ ] `afterEach` clears mocks and closes module.
- [ ] `npm run test && npm run lint && npm run typecheck` pass.

## Best Practices

- **SHOULD** prefer public behavior over implementation details; avoid private/protected access unless unavoidable.
- **MUST** keep Arrange → Act → Assert clear and minimal.
- **SHOULD** cover success + error + boundary cases for each decision branch.
- **MUST** control time/randomness/env/feature flags; tests must be deterministic.
- **SHOULD** use small, representative inputs; avoid huge fixtures.
- If a test needs multiple modules or real IO, it is integration/e2e, not unit.
