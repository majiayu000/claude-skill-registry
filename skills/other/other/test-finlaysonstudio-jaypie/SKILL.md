---
name: test
description: Run and write Vitest tests, mock Jaypie with testkit, CI matrix
---

# Test

How to run and write tests in this monorepo.

## Running Tests

```bash
npm test                                   # Run ALL tests across all packages (vitest run)
npm test -w packages/<name>                # Run tests for a specific package
npm test -w workspaces/<name>              # Run tests for a specific workspace
```

Never run bare `vitest` -- it defaults to watch mode and won't terminate. Always use `npm test` or `vitest run`.

### Specific Test Shortcuts

```bash
npm run test:jaypie                        # packages/jaypie
npm run test:llm                           # packages/llm
npm run test:testkit                       # packages/testkit
npm run test:express                       # packages/express
npm run test:errors                        # packages/errors
# ... etc (test:<package-name> for each package)
```

### LLM Client Tests (Integration)

Require API keys. Run locally or in CI when `packages/llm/**` changes:

```bash
npm run test:llm:client                    # Basic client tests
npm run test:llm:all                       # All LLM tests (client, document, image, joke, reasoning, structured)
npm run test:llm:joke                      # Individual test suite
```

## Test Framework

- **Vitest** with workspace configuration
- `vitest.workspace.ts` at root discovers `packages/*/vitest.config.{ts,js}`
- Each package with tests has its own `vitest.config.ts` and optional `vitest.setup.ts`
- Tests run across Node.js 22, 24, 25 in CI

## Writing Tests

### File Location

Tests live alongside source or in `__tests__/` directories:

```
src/
├── services/
│   └── user.ts
└── __tests__/
    └── user.spec.ts

# Or co-located:
src/
└── services/
    ├── user.ts
    └── user.spec.ts
```

### Test Structure

```typescript
import { describe, expect, it, vi, beforeEach } from "vitest";

describe("MyFunction", () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it("does the expected thing", async () => {
    // Arrange
    const input = { key: "value" };

    // Act
    const result = await myFunction(input);

    // Assert
    expect(result).toBeDefined();
  });
});
```

## Mocking Jaypie

Most packages mock `jaypie` in their `vitest.setup.ts`:

```typescript
// vitest.setup.ts
import { vi } from "vitest";

vi.mock("jaypie", async () => {
  const { mockJaypie } = await import("@jaypie/testkit");
  return mockJaypie(vi);
});
```

This mocks `log`, `getSecret`, `sendMessage`, and other Jaypie exports as `vi.fn()`.

### Using Mocks in Tests

```typescript
import { log, getSecret } from "jaypie";

it("logs the operation", async () => {
  await myFunction();
  expect(log.info).toHaveBeenCalledWith("message");
});

it("reads a secret", async () => {
  vi.mocked(getSecret).mockResolvedValue("mock-value");
  await myFunction();
  expect(getSecret).toHaveBeenCalledWith("secret-name");
});
```

### Other Available Mocks

```typescript
// @jaypie/logger
vi.mock("@jaypie/logger", async () => {
  const { mockLogger } = await import("@jaypie/testkit");
  return mockLogger(vi);
});

// @jaypie/aws
vi.mock("@jaypie/aws", async () => {
  const { mockAws } = await import("@jaypie/testkit");
  return mockAws(vi);
});
```

## Testing Errors

```typescript
import { NotFoundError } from "jaypie";

it("throws NotFoundError when missing", async () => {
  await expect(myFunction("bad-id")).rejects.toThrow(NotFoundError);
});
```

### Custom Matchers

```typescript
import { matchers } from "@jaypie/testkit";

expect.extend(matchers);

it("throws a Jaypie error", async () => {
  await expect(myFunction()).rejects.toBeJaypieError();
});
```

## Vitest Config Template

```typescript
// vitest.config.ts
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    coverage: {
      reporter: ["text", "json", "html"],
    },
    globals: true,
    setupFiles: ["./vitest.setup.ts"],
  },
});
```

## Build Before Test

Tests often depend on built artifacts. In CI, `npm run build` runs before `npm test`. Locally, if tests fail on import errors, rebuild first:

```bash
npm run build && npm test -w packages/<name>
```

## Testkit Export Requirement

When adding a new export to any package, update `packages/testkit` to mock it -- otherwise tests across the monorepo will fail.

## CI Testing Matrix

Tests run on Node.js 22, 24, 25 in `npm-check.yml` and on 22, 24 in stack deployment workflows. The `continue-on-error` typecheck job won't block merges but lint and test must pass.
