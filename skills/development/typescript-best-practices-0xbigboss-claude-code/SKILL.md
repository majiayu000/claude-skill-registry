---
name: typescript-best-practices
description: Provides TypeScript patterns for type-first development, making illegal states unrepresentable, exhaustive handling, and runtime validation. Must use when reading or writing TypeScript/JavaScript files.
---

# TypeScript Best Practices

## Pair with React Best Practices

When working with React components (`.tsx`, `.jsx` files or `@react` imports), always load `react-best-practices` alongside this skill. This skill covers TypeScript fundamentals; React-specific patterns (effects, hooks, refs, component design) are in the dedicated React skill.

## Type-First Development

Types define the contract before implementation. Follow this workflow:

1. **Define the data model** - types, interfaces, and schemas first
2. **Define function signatures** - input/output types before logic
3. **Implement to satisfy types** - let the compiler guide completeness
4. **Validate at boundaries** - runtime checks where data enters the system

### Make Illegal States Unrepresentable

Use the type system to prevent invalid states at compile time.

**Discriminated unions for mutually exclusive states:**
```ts
// Good: only valid combinations possible
type RequestState<T> =
  | { status: 'idle' }
  | { status: 'loading' }
  | { status: 'success'; data: T }
  | { status: 'error'; error: Error };

// Bad: allows invalid combinations like { loading: true, error: Error }
type RequestState<T> = {
  loading: boolean;
  data?: T;
  error?: Error;
};
```

**Branded types for domain primitives:**
```ts
type UserId = string & { readonly __brand: 'UserId' };
type OrderId = string & { readonly __brand: 'OrderId' };

// Compiler prevents passing OrderId where UserId expected
function getUser(id: UserId): Promise<User> { /* ... */ }

function createUserId(id: string): UserId {
  return id as UserId;
}
```

**Const assertions for literal unions:**
```ts
const ROLES = ['admin', 'user', 'guest'] as const;
type Role = typeof ROLES[number]; // 'admin' | 'user' | 'guest'

// Array and type stay in sync automatically
function isValidRole(role: string): role is Role {
  return ROLES.includes(role as Role);
}
```

**Required vs optional fields - be explicit:**
```ts
// Creation: some fields required
type CreateUser = {
  email: string;
  name: string;
};

// Update: all fields optional
type UpdateUser = Partial<CreateUser>;

// Database row: all fields present
type User = CreateUser & {
  id: UserId;
  createdAt: Date;
};
```

## Module Structure

Prefer smaller, focused files: one component, hook, or utility per file. Split when a file handles multiple concerns or exceeds ~200 lines. Colocate tests with implementation (`foo.test.ts` alongside `foo.ts`). Group related files by feature rather than by type.

## Functional Patterns

- Prefer `const` over `let`; use `readonly` and `Readonly<T>` for immutable data.
- Use `array.map/filter/reduce` over `for` loops; chain transformations in pipelines.
- Write pure functions for business logic; isolate side effects in dedicated modules.
- Avoid mutating function parameters; return new objects/arrays instead.

## Instructions

- Enable `strict` mode; model data with interfaces and types. Strong typing catches bugs at compile time.
- Every code path returns a value or throws; use exhaustive `switch` with `never` checks in default. Unhandled cases become compile errors.
- Propagate errors with context; catching requires re-throwing or returning a meaningful result. Hidden failures delay debugging.
- Handle edge cases explicitly: empty arrays, null/undefined inputs, boundary values. Defensive checks prevent runtime surprises.
- Use `await` for async calls; wrap external calls with contextual error messages. Unhandled rejections crash Node processes.
- Add or update focused tests when changing logic; test behavior, not implementation details.

## Examples

Explicit failure for unimplemented logic:
```ts
export function buildWidget(widgetType: string): never {
  throw new Error(`buildWidget not implemented for type: ${widgetType}`);
}
```

Exhaustive switch with never check:
```ts
type Status = "active" | "inactive";

export function processStatus(status: Status): string {
  switch (status) {
    case "active":
      return "processing";
    case "inactive":
      return "skipped";
    default: {
      const _exhaustive: never = status;
      throw new Error(`unhandled status: ${_exhaustive}`);
    }
  }
}
```

Wrap external calls with context:
```ts
export async function fetchWidget(id: string): Promise<Widget> {
  const response = await fetch(`/api/widgets/${id}`);
  if (!response.ok) {
    throw new Error(`fetch widget ${id} failed: ${response.status}`);
  }
  return response.json();
}
```

Debug logging with namespaced logger:
```ts
import debug from "debug";

const log = debug("myapp:widgets");

export function createWidget(name: string): Widget {
  log("creating widget: %s", name);
  const widget = { id: crypto.randomUUID(), name };
  log("created widget: %s", widget.id);
  return widget;
}
```

## Runtime Validation with Zod

- Define schemas as single source of truth; infer TypeScript types with `z.infer<>`. Avoid duplicating types and schemas.
- Use `safeParse` for user input where failure is expected; use `parse` at trust boundaries where invalid data is a bug.
- Compose schemas with `.extend()`, `.pick()`, `.omit()`, `.merge()` for DRY definitions.
- Add `.transform()` for data normalization at parse time (trim strings, parse dates).
- Include descriptive error messages; use `.refine()` for custom validation logic.

### Examples

Schema as source of truth with type inference:
```ts
import { z } from "zod";

const UserSchema = z.object({
  id: z.string().uuid(),
  email: z.string().email(),
  name: z.string().min(1),
  createdAt: z.string().transform((s) => new Date(s)),
});

type User = z.infer<typeof UserSchema>;
```

Return parse results to callers (never swallow errors):
```ts
import { z, SafeParseReturnType } from "zod";

export function parseUserInput(raw: unknown): SafeParseReturnType<unknown, User> {
  return UserSchema.safeParse(raw);
}

// Caller handles both success and error:
const result = parseUserInput(formData);
if (!result.success) {
  setErrors(result.error.flatten().fieldErrors);
  return;
}
await submitUser(result.data);
```

Strict parsing at trust boundaries:
```ts
export async function fetchUser(id: string): Promise<User> {
  const response = await fetch(`/api/users/${id}`);
  if (!response.ok) {
    throw new Error(`fetch user ${id} failed: ${response.status}`);
  }
  const data = await response.json();
  return UserSchema.parse(data); // throws if API contract violated
}
```

Schema composition:
```ts
const CreateUserSchema = UserSchema.omit({ id: true, createdAt: true });
const UpdateUserSchema = CreateUserSchema.partial();
const UserWithPostsSchema = UserSchema.extend({
  posts: z.array(PostSchema),
});
```

## Configuration

- Load config from environment variables at startup; validate with Zod before use. Invalid config should crash immediately.
- Define a typed config object as single source of truth; avoid accessing `process.env` throughout the codebase.
- Use sensible defaults for development; require explicit values for production secrets.

### Examples

Typed config with Zod validation:
```ts
import { z } from "zod";

const ConfigSchema = z.object({
  PORT: z.coerce.number().default(3000),
  DATABASE_URL: z.string().url(),
  API_KEY: z.string().min(1),
  NODE_ENV: z.enum(["development", "production", "test"]).default("development"),
});

export const config = ConfigSchema.parse(process.env);
```

Access config values (not process.env directly):
```ts
import { config } from "./config";

const server = app.listen(config.PORT);
const db = connect(config.DATABASE_URL);
```

## Optional: type-fest

For advanced type utilities beyond TypeScript builtins, consider [type-fest](https://github.com/sindresorhus/type-fest):

- `Opaque<T, Token>` - cleaner branded types than manual `& { __brand }` pattern
- `PartialDeep<T>` - recursive partial for nested objects
- `ReadonlyDeep<T>` - recursive readonly for immutable data
- `LiteralUnion<Literals, Fallback>` - literals with autocomplete + string fallback
- `SetRequired<T, K>` / `SetOptional<T, K>` - targeted field modifications
- `Simplify<T>` - flatten complex intersection types in IDE tooltips

```ts
import type { Opaque, PartialDeep, SetRequired } from 'type-fest';

// Branded type (cleaner than manual approach)
type UserId = Opaque<string, 'UserId'>;

// Deep partial for patch operations
type UserPatch = PartialDeep<User>;

// Make specific fields required
type UserWithEmail = SetRequired<Partial<User>, 'email'>;
```
