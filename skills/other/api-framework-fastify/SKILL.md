---
name: api-framework-fastify
description: Fastify routes, JSON Schema validation, plugin system, TypeScript type providers
---

# API Development with Fastify

> **Quick Guide:** Use Fastify for high-performance Node.js REST APIs with built-in JSON Schema validation and powerful plugin encapsulation. Use `@fastify/type-provider-typebox` for end-to-end type safety (both `Type` and `TypeBoxTypeProvider` re-exported from it). Wrap shared plugins with `fastify-plugin` to expose decorators. Always define response schemas for serialization performance and data leak prevention.

---

<critical_requirements>

## CRITICAL: Before Using This Skill

> **All code must follow project conventions in CLAUDE.md** (kebab-case, named exports, import ordering, `import type`, named constants)

**(You MUST use `withTypeProvider<>()` for type-safe request/response handling)**

**(You MUST wrap shared plugins with `fastify-plugin` to expose decorators to parent scope)**

**(You MUST define response schemas to enable fast-json-stringify optimization)**

**(You MUST use named constants for HTTP status codes - never raw numbers)**

</critical_requirements>

---

**Auto-detection:** Fastify, fastify.register, fastify.decorate, fastify-plugin, TypeBox, @fastify/type-provider-typebox, @fastify/type-provider-json-schema-to-ts, fastify-type-provider-zod, preHandler, onRequest, preSerialization, JSON Schema validation, fast-json-stringify, FastifyPluginAsyncTypebox

**When to use:**

- Building high-performance REST APIs (45k+ req/sec benchmarks)
- Need schema-based validation with automatic coercion
- Want plugin encapsulation for modular architecture
- Require lifecycle hooks for cross-cutting concerns
- Building APIs with strict TypeScript type safety requirements

**When NOT to use:**

- Simple internal APIs without performance requirements (consider your existing solution)
- GraphQL APIs (use dedicated GraphQL servers)
- Edge/serverless with size constraints (Fastify has larger footprint than minimal frameworks)
- When middleware ecosystem compatibility with Express is required

**Key patterns covered:**

- Server setup with TypeScript type providers
- Plugin system and encapsulation patterns
- JSON Schema validation for request/response
- Lifecycle hooks (onRequest, preHandler, onSend, etc.)
- Decorators for extending Fastify/Request/Reply
- Error handling with setErrorHandler
- Route organization with prefix patterns

---

**Detailed Resources:**

- [examples/core.md](examples/core.md) - Server setup, routes, schemas, error handling, testing
- [examples/plugins.md](examples/plugins.md) - Plugin system, encapsulation, decorators
- [examples/schemas.md](examples/schemas.md) - TypeBox schemas, validation, type-safe routes
- [examples/hooks.md](examples/hooks.md) - Lifecycle hooks and cross-cutting concerns
- [reference.md](reference.md) - Decision frameworks, anti-patterns, quick reference

---

<philosophy>

## Philosophy

**Schema-first, compiled validation.** Fastify compiles JSON schemas at startup into highly optimized validator functions. This provides both runtime safety and documentation from a single source of truth.

**Plugin encapsulation creates microservices in a monolith.** Each plugin has its own scope for decorators and hooks. Child plugins inherit from parents, but parents cannot access child resources - enabling clean separation of concerns.

**Performance without sacrifice.** Fastify achieves 2-3x throughput over Express while maintaining developer ergonomics through TypeScript integration and comprehensive hook system.

**Use Fastify when:**

- Building production APIs requiring high throughput
- Need schema validation at the framework level
- Want plugin architecture for large codebases
- Require fine-grained lifecycle control

**Use alternatives when:**

- Simple internal endpoints (your existing patterns)
- Edge deployments with bundle size constraints
- Need Express middleware ecosystem compatibility

</philosophy>

---

<patterns>

## Core Patterns

### Pattern 1: Server Setup with Type Provider

Configure Fastify with TypeBox for compile-time AND runtime type safety. `Type` is re-exported from `@fastify/type-provider-typebox`.

```typescript
import Fastify from "fastify";
import { Type, TypeBoxTypeProvider } from "@fastify/type-provider-typebox";

const SERVER_PORT = 3000;
const SERVER_HOST = "0.0.0.0";

const buildServer = () => {
  const server = Fastify({
    logger: { level: process.env.LOG_LEVEL ?? "info" },
  }).withTypeProvider<TypeBoxTypeProvider>();

  server.setErrorHandler(errorHandler);
  server.register(userRoutes, { prefix: "/api/users" });

  return server;
};

export { buildServer };
```

**Why good:** TypeBox provider enables type inference from schemas, factory function enables testing, `Type` imported from same package

> Full example with startup, error handling, and testing: [examples/core.md](examples/core.md)

---

### Pattern 2: Schema Definition with TypeBox

Define schemas that provide both TypeScript types AND runtime validation from a single source.

```typescript
import { Type, Static } from "@fastify/type-provider-typebox";

const MIN_USERNAME_LENGTH = 3;
const MAX_USERNAME_LENGTH = 50;

export const UserSchema = Type.Object({
  id: Type.String({ format: "uuid" }),
  username: Type.String({
    minLength: MIN_USERNAME_LENGTH,
    maxLength: MAX_USERNAME_LENGTH,
  }),
  email: Type.String({ format: "email" }),
});

// Derive TypeScript types from schemas
export type User = Static<typeof UserSchema>;
```

**Why good:** Single source of truth for types and validation, `Static<>` derives TS types automatically

> Full schema patterns (composition, partial updates, reusable components): [examples/schemas.md](examples/schemas.md)

---

### Pattern 3: Route Definition with Full Schema

Define routes with request AND response schemas for complete type safety and serialization optimization.

```typescript
import type { FastifyPluginAsync } from "fastify";
import { Type } from "@fastify/type-provider-typebox";

const HTTP_OK = 200;
const HTTP_NOT_FOUND = 404;

export const userRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.get(
    "/:id",
    {
      schema: {
        params: UserParamsSchema,
        response: {
          [HTTP_OK]: UserSchema,
          [HTTP_NOT_FOUND]: ErrorSchema,
        },
      },
    },
    async (request, reply) => {
      const user = await fastify.userService.findById(request.params.id);
      if (!user) {
        return reply.status(HTTP_NOT_FOUND).send({
          statusCode: HTTP_NOT_FOUND,
          error: "Not Found",
          message: `User ${request.params.id} not found`,
        });
      }
      return reply.status(HTTP_OK).send(user);
    },
  );
};
```

**Why good:** Response schemas enable fast-json-stringify (2-3x faster), full type inference on request objects, HTTP constants prevent magic numbers

> Complete CRUD routes with pagination: [examples/core.md](examples/core.md)

---

### Pattern 4: Plugin Encapsulation

Default plugins are **encapsulated** - decorators stay within scope. Use `fastify-plugin` (`fp`) to break encapsulation for shared infrastructure.

```typescript
// ENCAPSULATED - decorators only available within this plugin
export const authRoutes: FastifyPluginAsync = async (fastify) => {
  fastify.decorate("authConfig", { tokenExpiry: 3600 });
  // authConfig only accessible in this plugin
};

// SHARED - decorators exposed to parent scope
import fp from "fastify-plugin";

declare module "fastify" {
  interface FastifyInstance {
    config: AppConfig;
  }
}

const configPlugin: FastifyPluginAsync = async (fastify) => {
  fastify.decorate("config", { apiVersion: "v1" });
};

export const appConfig = fp(configPlugin, {
  name: "app-config",
  dependencies: [],
});
```

**Why good:** Domain plugins stay isolated, shared utilities use `fp()` to expose decorators, TypeScript augmentation provides type safety

> Full plugin examples with dependencies, registration order: [examples/plugins.md](examples/plugins.md)

---

### Pattern 5: Lifecycle Hooks

Use hooks for cross-cutting concerns at specific lifecycle points.

**Hook execution order:**

1. `onRequest` - Before parsing (request ID, timing)
2. `preParsing` - Transform request stream
3. `preValidation` - Before schema validation
4. `preHandler` - After validation (auth, authorization)
5. `preSerialization` - Transform response object
6. `onSend` - Final payload modification
7. `onResponse` - After response sent (metrics, logging)
8. `onError` - On error (error logging)

```typescript
// Plugin-level: applies to ALL routes in this plugin
fastify.addHook("preHandler", requireAuth);

// Route-level: applies to single route
fastify.delete(
  "/users/:id",
  {
    preHandler: [requireAuth, requireAdmin],
  },
  async (request) => {
    /* ... */
  },
);
```

**Why good:** Plugin-level for consistent protection, route-level for selective application, hooks execute in array order

> Full hook examples (request timing, auth, response headers, error logging): [examples/hooks.md](examples/hooks.md)

---

### Pattern 6: Error Handling

Implement centralized error handling with `setErrorHandler`. Fastify validation errors have a `.validation` array (not `.message`).

```typescript
import type { FastifyError, FastifyReply, FastifyRequest } from "fastify";

const HTTP_BAD_REQUEST = 400;
const HTTP_INTERNAL_ERROR = 500;

export const errorHandler = (
  error: FastifyError,
  request: FastifyRequest,
  reply: FastifyReply,
) => {
  if (error.validation) {
    return reply.status(HTTP_BAD_REQUEST).send({
      statusCode: HTTP_BAD_REQUEST,
      error: "Bad Request",
      message: "Validation failed",
      details: error.validation,
    });
  }

  request.log.error(
    { error: error.message, stack: error.stack },
    "Unexpected error",
  );
  return reply.status(HTTP_INTERNAL_ERROR).send({
    statusCode: HTTP_INTERNAL_ERROR,
    error: "Internal Server Error",
    message: "An unexpected error occurred",
  });
};
```

**Why good:** Validation errors expose details, unexpected errors logged with stack but hidden from client

> Full error handler with custom error classes: [examples/core.md](examples/core.md)

---

### Pattern 7: Decorators

Extend Fastify instance, Request, and Reply with decorators.

```typescript
// Instance decorator - services/utilities
fastify.decorate("myService", serviceInstance);

// Request decorator - per-request state (initialize with null, set in hook)
fastify.decorateRequest("userId", null);
fastify.addHook("preHandler", async (request) => {
  request.userId = decoded.userId;
});

// Reply decorator - response helpers (use function for `this` binding)
fastify.decorateReply(
  "notFound",
  function (this: FastifyReply, message: string) {
    this.status(HTTP_NOT_FOUND).send({
      statusCode: HTTP_NOT_FOUND,
      error: "Not Found",
      message,
    });
  },
);
```

**CRITICAL:** Never use reference types (objects, arrays) as initial decorator values - they are **shared across ALL requests**. Use `null` and set per-request in hooks.

> Full decorator examples: [examples/plugins.md](examples/plugins.md)

---

### Pattern 8: Testing with server.inject()

Use the factory pattern for test isolation and `server.inject()` for zero-network-overhead testing.

```typescript
import { buildServer } from "./server";

let server: ReturnType<typeof buildServer>;

beforeEach(async () => {
  server = buildServer();
  await server.ready();
});

afterEach(async () => {
  await server.close();
});

it("should list users", async () => {
  const response = await server.inject({
    method: "GET",
    url: "/api/users",
    query: { limit: "10" },
  });

  expect(response.statusCode).toBe(200);
  expect(response.json()).toHaveProperty("users");
});
```

**Why good:** `server.inject()` tests without network, `beforeEach`/`afterEach` ensures clean state, tests validation and success paths

</patterns>

---

<red_flags>

## RED FLAGS

### High Priority Issues

- **No type provider configured** - Loses compile-time type safety on request/response
- **Shared plugins without `fastify-plugin`** - Decorators invisible to other plugins
- **Missing response schemas** - Loses 2-3x serialization performance AND risks data leaks
- **Raw status code numbers** - Use named constants (`HTTP_OK`, `HTTP_NOT_FOUND`)
- **Reference types in `decorateRequest`/`decorateReply`** - Shared mutable state across ALL requests (security risk)

### Medium Priority Issues

- **No error handler configured** - Stack traces exposed to clients in production
- **Missing `dependencies` in plugin options** - Race conditions on decorator access
- **No schema for query/params** - No validation, types are `unknown`
- **Inline route handlers in god files** - Use modular route plugins with prefix

### Common Mistakes

- **Forgetting `await server.ready()`** - Plugins may not be fully loaded
- **Not cleaning up in `onClose`** - Connection leaks on shutdown
- **Mixing async/await with `done` callback** - Pick one pattern per hook (causes double-completion)
- **Using Express patterns** - `res.send()` vs `reply.send()`, `next()` vs returning

### Gotchas & Edge Cases

- **Hook return values:** Returning a value from hooks sends response immediately (short-circuits)
- **Plugin registration order:** Later plugins can't access earlier encapsulated decorators
- **Validation error shape:** Fastify validation errors have `.validation` array, not `.message`
- **Route specificity:** More specific routes must be registered before wildcards
- **preHandler order:** Route-level runs AFTER plugin-level hooks
- **onResponse timing:** Runs after response sent, cannot modify response
- **Schema compilation:** Happens at startup, errors surface during `server.ready()`
- **v5 redirect order:** `reply.redirect(url, statusCode)` not `reply.redirect(statusCode, url)` (reversed from v4)
- **v5 reply.sent:** Use `reply.hijack()` instead of setting `reply.sent = true`

</red_flags>

---

<critical_reminders>

## CRITICAL REMINDERS

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `withTypeProvider<>()` for type-safe request/response handling)**

**(You MUST wrap shared plugins with `fastify-plugin` to expose decorators to parent scope)**

**(You MUST define response schemas to enable fast-json-stringify optimization)**

**(You MUST use named constants for HTTP status codes - never raw numbers)**

**Failure to follow these rules will break type safety and lose performance benefits.**

</critical_reminders>
