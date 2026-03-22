---
name: api-framework-elysia
description: Bun-native HTTP framework — routing, TypeBox validation, Eden Treaty, plugins, lifecycle hooks
---

# API Development with Elysia

> **Quick Guide:** Elysia is a Bun-native HTTP framework with end-to-end type safety. Use method chaining (not separate statements) so TypeScript infers the full route tree. Import `t` from `elysia` for TypeBox validation. Export the app type (`export type App = typeof app`) for Eden Treaty clients. Use `status()` (not the deprecated `error()` function) for error responses with type narrowing.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use method chaining on the Elysia instance -- separate `.get()` calls break type inference for Eden Treaty)**

**(You MUST use `status()` for error responses -- `error()` is deprecated since 1.3, prefer `status()`)**

**(You MUST export the app type (`export type App = typeof app`) for Eden Treaty client generation)**

</critical_requirements>

---

**Auto-detection:** Elysia, elysia, ElysiaJS, Eden Treaty, @elysiajs/eden, @elysiajs/openapi, t.Object, t.String, t.Number, t.File, TypeBox, .derive(), .decorate(), .guard(), .macro(), .ws(), onBeforeHandle, onAfterHandle, onRequest, treaty, bun:test

**When to use:**

- Building APIs on Bun runtime with end-to-end type safety
- Need RPC-style client with zero code generation (Eden Treaty)
- TypeBox validation with AOT compilation (~18x faster than Zod on Bun)
- Plugin-based architecture with automatic type propagation
- WebSocket support with schema validation

**When NOT to use:**

- Deploying to Node.js-only environments without Bun (use a Node-first framework)
- Need OpenAPI-first design with `createRoute` patterns (other frameworks with Zod-OpenAPI integration are more mature for this)
- Team already committed to Express/Fastify ecosystem

**Key patterns covered:**

- Route definitions with method chaining and TypeBox validation
- Plugin architecture with `.use()`, `.derive()`, `.decorate()`, `.macro()`
- Scoping rules (local, scoped, global) and `.guard()`
- End-to-end type safety with Eden Treaty
- Lifecycle hooks (onRequest, onBeforeHandle, onAfterHandle, onError)
- Error handling with custom error classes and `status()`
- WebSocket with schema validation
- Testing with `bun:test` and `.handle()` or Eden Treaty

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Route setup, method chaining, validation, plugins
- [examples/eden-treaty.md](examples/eden-treaty.md) - End-to-end type-safe client
- [examples/lifecycle-errors.md](examples/lifecycle-errors.md) - Lifecycle hooks, error handling, custom errors
- [examples/websocket-testing.md](examples/websocket-testing.md) - WebSocket patterns and unit testing
- [reference.md](reference.md) - Decision frameworks, anti-patterns, production checklist

---

<philosophy>

## Philosophy

**Method chaining IS the type system.** Elysia infers the entire route tree through chained calls. Breaking the chain (separate `app.get()` statements) loses type information for Eden Treaty clients. This is the single most important architectural constraint.

**TypeBox over Zod for Bun.** While Elysia 1.4+ supports Standard Schema (Zod, Valibot, etc.), TypeBox (`t` from `elysia`) uses AOT compilation inside Bun for ~18x faster validation. Use TypeBox as default; use Zod only when sharing schemas with a non-Bun codebase.

**Plugins are Elysia instances.** Every `new Elysia()` is a plugin. There is no separate plugin API -- you compose by chaining `.use()`. The `name` property deduplicates plugins across the tree.

**Use Elysia when:**

- Building on Bun runtime with type safety as a priority
- Want RPC-style client without code generation (Eden Treaty)
- Need high-performance validation (TypeBox AOT)
- Building real-time features (native WebSocket support)

**Use a different framework when:**

- Need OpenAPI-first design workflow (Zod-OpenAPI integration is more mature in other frameworks)
- Deploying exclusively to Node.js
- Team needs framework with larger ecosystem/community

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Route Setup with Method Chaining

Chain route definitions on the Elysia instance. Each `.get()`, `.post()`, etc. returns the instance with updated type information.

```typescript
import { Elysia, t } from "elysia";

const app = new Elysia()
  .get("/", () => "hello")
  .get("/user/:id", ({ params: { id } }) => id, {
    params: t.Object({
      id: t.Number(),
    }),
  })
  .post("/user", ({ body }) => body, {
    body: t.Object({
      name: t.String(),
      email: t.String({ format: "email" }),
    }),
  })
  .listen(3000);

export type App = typeof app;
```

**Why good:** method chaining preserves type inference across the entire route tree, `export type App` enables Eden Treaty, TypeBox validates at runtime with AOT compilation

See [examples/core.md](examples/core.md) for complete route setup with modular plugins.

---

### Pattern 2: Plugin Architecture

Every Elysia instance is a plugin. Use `.use()` to compose, `name` to deduplicate.

```typescript
import { Elysia } from "elysia";

const userPlugin = new Elysia({ name: "user", prefix: "/user" })
  .get("/", () => "list users")
  .get("/:id", ({ params: { id } }) => `user ${id}`);

const app = new Elysia().use(userPlugin).listen(3000);
```

**Why good:** `name` prevents duplicate registration when a plugin is `.use()`-d multiple times, `prefix` scopes routes cleanly

See [examples/core.md](examples/core.md) for `.derive()`, `.decorate()`, and `.macro()` patterns.

---

### Pattern 3: Scoping with Guard

Apply validation schemas and lifecycle hooks to groups of routes.

```typescript
import { Elysia, t } from "elysia";

const app = new Elysia()
  .guard(
    {
      headers: t.Object({
        authorization: t.String(),
      }),
    },
    (app) =>
      app
        .get("/protected", ({ headers }) => headers.authorization)
        .post("/admin", ({ body }) => body, {
          body: t.Object({ action: t.String() }),
        }),
  )
  .get("/public", () => "no auth needed");
```

**Why good:** guard encapsulates validation for route groups without repeating schema definitions, public routes outside the guard are unaffected

---

### Pattern 4: Error Handling with status()

Use `status()` for typed error responses. Register custom error classes with `.error()`.

```typescript
import { Elysia } from "elysia";

const HTTP_UNAUTHORIZED = 401;
const HTTP_NOT_FOUND = 404;

class NotFoundError extends Error {
  status = HTTP_NOT_FOUND;
  constructor(public resource: string) {
    super(`${resource} not found`);
  }
}

const app = new Elysia()
  .error({ NotFoundError })
  .onError(({ code, error, status }) => {
    if (code === "NotFoundError") {
      return status(HTTP_NOT_FOUND, { error: error.message });
    }
    if (code === "VALIDATION") {
      return status(HTTP_UNAUTHORIZED, { error: "Validation failed" });
    }
  })
  .get("/user/:id", ({ params: { id }, status }) => {
    const user = findUser(id);
    if (!user) throw new NotFoundError("User");
    return user;
  });
```

**Why good:** `status()` provides type narrowing for error responses, custom error classes with `.error()` enable `code`-based type narrowing in `onError`, named constants avoid magic status numbers

See [examples/lifecycle-errors.md](examples/lifecycle-errors.md) for all lifecycle hooks and error patterns.

---

### Pattern 5: Eden Treaty Client

Export the app type and use `treaty()` for a fully type-safe client with no code generation.

```typescript
// server.ts
import { Elysia, t } from "elysia";

const app = new Elysia()
  .get("/user/:id", ({ params: { id } }) => ({ id, name: "Alice" }), {
    params: t.Object({ id: t.Number() }),
  })
  .post("/user", ({ body }) => body, {
    body: t.Object({ name: t.String() }),
  });

export type App = typeof app;
```

```typescript
// client.ts
import { treaty } from "@elysiajs/eden";
import type { App } from "./server";

const api = treaty<App>("localhost:3000");

const { data, error } = await api.user({ id: 1 }).get();
// data is typed as { id: number; name: string } | null
// error is typed based on error responses
```

**Why good:** zero code generation, full autocomplete on paths and methods, error/data destructuring with type narrowing

See [examples/eden-treaty.md](examples/eden-treaty.md) for response handling, file uploads, and WebSocket via Treaty.

</patterns>

---

<red_flags>

## RED FLAGS

**High Priority:**

- Separate `app.get()` / `app.post()` calls instead of chaining -- breaks Eden Treaty type inference entirely
- Using deprecated `error()` function instead of `status()` -- deprecated since Elysia 1.3
- Not exporting `type App = typeof app` -- Eden Treaty client has no type information
- Using `as('plugin')` -- removed in 1.3+, use `as('scoped')` instead

**Medium Priority:**

- Importing patterns from other HTTP frameworks -- Elysia has its own routing API and conventions
- Using `t.Object()` without named constants for limits/lengths -- magic numbers in validation schemas
- Not providing `name` on plugin instances -- causes duplicate registration in complex app trees
- `.derive()` or lifecycle hooks without `{ as: 'scoped' }` or `{ as: 'global' }` when parent routes need them -- hooks are local-scoped by default

**Gotchas & Edge Cases:**

- `params` are strings by default -- use `t.Number()` in the schema to coerce path params to numbers
- `.handle()` in tests requires a fully qualified URL (`http://localhost/path`), NOT a path fragment (`/path`)
- `.guard()` group standalone mode is default in 1.4+ -- guard schemas merge with route schemas instead of overwriting
- TypeBox `t.File()` auto-detects `multipart/form-data` content type -- no need to set headers manually
- `t.Files()` (plural) for multiple file uploads, `t.File()` for single
- Eden Treaty dynamic path params use function syntax: `api.user({ id: 1 }).get()` not `api.user[1].get()`
- When Eden Treaty response has status >= 300, `data` is always `null` and `error` has the value
- Lifecycle hooks only apply to routes registered AFTER the hook -- order of `.on*()` and route definitions matters
- `onError` receives a `code` string, not a status number -- switch on `code` for type narrowing
- Cookies parse as JSON automatically if the value looks like JSON (1.3+ behavior)
- `await app.modules` is required in tests when using lazy-loaded plugins (`import('./plugin')`)

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use method chaining on the Elysia instance -- separate `.get()` calls break type inference for Eden Treaty)**

**(You MUST use `status()` for error responses -- `error()` is deprecated since 1.3, prefer `status()`)**

**(You MUST export the app type (`export type App = typeof app`) for Eden Treaty client generation)**

**Failure to follow these rules will break end-to-end type safety and Eden Treaty client generation.**

</critical_reminders>
