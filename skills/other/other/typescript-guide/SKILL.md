---
name: typescript-guide
description: |
  TypeScript/JavaScript guardrails, patterns, and best practices for AI-assisted development.
  Use when working with TypeScript (.ts, .tsx) or JavaScript (.js, .jsx) files, package.json,
  or tsconfig.json. Provides strict mode conventions, async patterns, testing standards,
  and module system guidelines.
license: MIT
metadata:
  author: samuel
  version: "1.0"
  category: language
  language: typescript
  extensions: ".ts,.tsx,.js,.jsx"
---

# TypeScript/JavaScript Guide

> Applies to: TypeScript 5+, Node.js 20+, ES2022+, React, Server-Side JS

## Core Principles

1. **Strict TypeScript**: Enable all strict flags; treat type errors as build failures
2. **Immutability by Default**: Use `const`, `readonly`, `as const`, and spread operators; mutate only when profiling demands it
3. **Explicit Types at Boundaries**: All function signatures, API responses, and public interfaces must have explicit type annotations; infer internally
4. **Functional Patterns**: Prefer pure functions, map/filter/reduce, and composition over classes and mutation
5. **Zero `any`**: Use `unknown` for truly unknown data, Zod/io-ts for runtime narrowing; every `any` requires a code-review comment explaining why

## Guardrails

### TypeScript Configuration

- Enable `"strict": true` (this activates `strictNullChecks`, `noImplicitAny`, `strictFunctionTypes`, etc.)
- Enable `"noUncheckedIndexedAccess": true` (arrays and records return `T | undefined`)
- Enable `"noImplicitReturns": true` and `"noFallthroughCasesInSwitch": true`
- Set `"target": "ES2022"`, `"module": "ESNext"`, `"moduleResolution": "bundler"`
- Never suppress errors with `@ts-ignore`; use `@ts-expect-error` with a justification comment

### Code Style

- `const` over `let`; never use `var`
- Nullish coalescing (`??`) over logical OR (`||`) for defaults (avoids falsy-value bugs with `0`, `""`, `false`)
- Optional chaining (`?.`) over nested null checks
- Template literals over string concatenation
- Destructuring at call sites: `const { id, name } = user`
- Barrel exports (`index.ts`) only at package boundaries, not within internal modules (causes circular imports and tree-shaking failures)
- Enums: prefer `as const` objects over TypeScript `enum` (enums produce runtime code and have surprising behaviors with reverse mappings)

```typescript
// Prefer this
const Status = {
  Active: "active",
  Inactive: "inactive",
} as const;
type Status = (typeof Status)[keyof typeof Status];

// Over this
enum Status {
  Active = "active",
  Inactive = "inactive",
}
```

### Error Handling

- Every `catch` block must type-narrow the error before accessing properties
- Never throw primitive values (strings, numbers); always throw `Error` subclasses
- Use the `cause` option for error chaining: `new AppError("msg", { cause: original })`
- Never swallow errors with empty `catch` blocks
- Async functions must have error handling at the call site or a global boundary handler

### Async/Await

- Always `await` or return promises; never create fire-and-forget promises without explicit `void` annotation
- Use `Promise.all` for independent concurrent operations, not sequential `await` in a loop
- Set timeouts on all external calls (fetch, database, third-party APIs) using `AbortController`
- Use `Promise.allSettled` when partial failure is acceptable
- Never mix `.then()` chains with `await` in the same function

```typescript
// Bad: sequential when order does not matter
const users = await fetchUsers();
const posts = await fetchPosts();

// Good: concurrent
const [users, posts] = await Promise.all([fetchUsers(), fetchPosts()]);

// Good: timeout with AbortController
async function fetchWithTimeout(url: string, ms: number): Promise<Response> {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), ms);
  try {
    return await fetch(url, { signal: controller.signal });
  } finally {
    clearTimeout(timeout);
  }
}
```

### Module System

- Use ES modules (`import`/`export`) exclusively; no `require()` in TypeScript
- One export per concept: prefer named exports over default exports (improves refactoring, grep-ability)
- Side-effect imports (`import "./setup"`) must be documented with a comment explaining why
- Re-export from `index.ts` only at package/feature boundaries
- Keep import order: stdlib/node builtins, external packages, internal modules, relative paths (enforce with ESLint `import/order`)

## Project Structure

```
myproject/
├── src/
│   ├── index.ts              # Application entry point
│   ├── config/               # Environment, feature flags
│   │   └── env.ts            # Validated env vars (Zod schema)
│   ├── domain/               # Business logic (no I/O)
│   │   ├── user.ts
│   │   └── order.ts
│   ├── services/             # Application services (orchestrate domain + I/O)
│   ├── repositories/         # Data access (database, external APIs)
│   ├── routes/               # HTTP handlers / controllers
│   ├── middleware/            # Express/Koa/Hono middleware
│   ├── utils/                # Pure utility functions
│   └── types/                # Shared type definitions
├── tests/
│   ├── unit/                 # Mirror src/ structure
│   ├── integration/          # API and database tests
│   └── fixtures/             # Shared test data
├── tsconfig.json
├── package.json
├── .eslintrc.cjs
├── .prettierrc
└── vitest.config.ts
```

- Domain logic in `domain/` must have zero I/O dependencies (pure functions, easy to test)
- No business logic in route handlers; delegate to services
- Shared types in `types/`; co-locate component-specific types with their module

## Error Handling Patterns

### Custom Application Errors

```typescript
class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    options?: ErrorOptions
  ) {
    super(message, options);
    this.name = "AppError";
  }
}

class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`, "NOT_FOUND", 404);
    this.name = "NotFoundError";
  }
}
```

### Result Pattern (for Expected Failures)

```typescript
type Result<T, E = AppError> =
  | { ok: true; value: T }
  | { ok: false; error: E };

function parseAge(input: string): Result<number> {
  const age = Number(input);
  if (Number.isNaN(age) || age < 0 || age > 150) {
    return { ok: false, error: new AppError("Invalid age", "VALIDATION") };
  }
  return { ok: true, value: age };
}

// Usage: caller must check before accessing value
const result = parseAge(input);
if (!result.ok) {
  return res.status(400).json({ error: result.error.message });
}
console.log(result.value); // Type-safe: number
```

### Typed Catch Blocks

```typescript
try {
  await externalService.call();
} catch (error: unknown) {
  if (error instanceof AppError) {
    logger.warn(error.message, { code: error.code });
    return res.status(error.statusCode).json({ error: error.message });
  }
  // Unknown error: wrap and re-throw
  throw new AppError("Unexpected failure", "INTERNAL", 500, { cause: error });
}
```

## Testing

### Standards

- Test runner: Vitest (preferred) or Jest
- Test files: co-located as `*.test.ts` or under `tests/` mirroring `src/`
- Naming: `describe("ModuleName")` with `it("should [expected behavior] when [condition]")`
- Use `beforeEach` for setup; avoid `beforeAll` for mutable state
- Coverage target: >80% for business logic, >60% overall
- No `any` in test files; test helpers must be typed
- Mock at boundaries (HTTP, database, file system), not internal functions

### Table-Driven Tests

```typescript
import { describe, it, expect } from "vitest";
import { validateEmail } from "./validate";

describe("validateEmail", () => {
  const cases = [
    { input: "user@example.com", expected: true, desc: "valid email" },
    { input: "no-at-sign", expected: false, desc: "missing @ symbol" },
    { input: "", expected: false, desc: "empty string" },
    { input: "a@b.c", expected: true, desc: "minimal valid email" },
  ] as const;

  it.each(cases)("returns $expected for $desc", ({ input, expected }) => {
    expect(validateEmail(input)).toBe(expected);
  });
});
```

### Mocking External Dependencies

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { UserService } from "./user.service";
import type { UserRepository } from "./user.repository";

describe("UserService", () => {
  let service: UserService;
  let repo: UserRepository;

  beforeEach(() => {
    repo = {
      findById: vi.fn(),
      save: vi.fn(),
    } as unknown as UserRepository;
    service = new UserService(repo);
  });

  it("should throw NotFoundError when user does not exist", async () => {
    vi.mocked(repo.findById).mockResolvedValue(null);

    await expect(service.getUser("abc")).rejects.toThrow("not found");
    expect(repo.findById).toHaveBeenCalledWith("abc");
  });
});
```

## Tooling

### Essential Commands

```bash
tsc --noEmit                     # Type check (no output)
eslint . --ext .ts,.tsx          # Lint
prettier --check .               # Format check
prettier --write .               # Format fix
vitest                           # Run tests (watch mode)
vitest run                       # Run tests (CI mode)
vitest run --coverage            # With coverage
```

### ESLint Configuration (Flat Config)

```javascript
// eslint.config.mjs
import tseslint from "typescript-eslint";
import importPlugin from "eslint-plugin-import";

export default tseslint.config(
  ...tseslint.configs.strictTypeChecked,
  {
    rules: {
      "@typescript-eslint/no-explicit-any": "error",
      "@typescript-eslint/explicit-function-return-type": ["warn", {
        allowExpressions: true,
      }],
      "@typescript-eslint/no-floating-promises": "error",
      "@typescript-eslint/no-misused-promises": "error",
      "@typescript-eslint/strict-boolean-expressions": "error",
      "import/order": ["error", {
        groups: ["builtin", "external", "internal", "parent", "sibling"],
        "newlines-between": "always",
      }],
    },
  }
);
```

### Strict tsconfig.json

```json
{
  "compilerOptions": {
    "strict": true,
    "target": "ES2022",
    "module": "ESNext",
    "moduleResolution": "bundler",
    "esModuleInterop": true,
    "skipLibCheck": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "forceConsistentCasingInFileNames": true,
    "exactOptionalPropertyTypes": true,
    "noPropertyAccessFromIndexSignature": true,
    "isolatedModules": true,
    "verbatimModuleSyntax": true
  }
}
```

### Input Validation (Zod)

```typescript
import { z } from "zod";

const CreateUserSchema = z.object({
  email: z.string().email(),
  name: z.string().min(1).max(100),
  age: z.number().int().min(0).max(150),
  role: z.enum(["admin", "user", "viewer"]),
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

// At API boundary
function handleCreateUser(rawBody: unknown): CreateUserInput {
  return CreateUserSchema.parse(rawBody); // throws ZodError on failure
}
```

## Advanced Topics

For detailed patterns and examples, see:

- [references/patterns.md](references/patterns.md) -- Advanced type patterns, Zod validation, async orchestration, module organization, React + TypeScript idioms
- [references/pitfalls.md](references/pitfalls.md) -- Common TypeScript footguns, type narrowing mistakes, async traps
- [references/security.md](references/security.md) -- XSS prevention, CSRF, content security policy, dependency auditing

## External References

- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Strict Mode Explained](https://www.typescriptlang.org/tsconfig#strict)
- [typescript-eslint](https://typescript-eslint.io/)
- [Zod Documentation](https://zod.dev/)
- [Vitest Documentation](https://vitest.dev/)
- [Effective TypeScript (Book)](https://effectivetypescript.com/)
- [Total TypeScript (Matt Pocock)](https://www.totaltypescript.com/)
