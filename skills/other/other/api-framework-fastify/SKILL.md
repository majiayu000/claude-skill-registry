---
name: api-framework-fastify
description: Fastify routes, JSON Schema validation, plugin system, TypeScript type providers
---

# API Development with Fastify

> **Quick Guide:** Use Fastify for high-performance Node.js REST APIs with built-in JSON Schema validation and powerful plugin encapsulation. Choose TypeBox or Zod type providers for end-to-end type safety. Plugin system enables modular, testable architecture.

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

**Auto-detection:** Fastify, fastify.register, fastify.decorate, fastify-plugin, TypeBox, @fastify/type-provider-typebox, @fastify/type-provider-json-schema-to-ts, fastify-type-provider-zod, preHandler, onRequest, preSerialization, JSON Schema validation, fast-json-stringify

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
- Response serialization for performance
- Async handler patterns

**Detailed Resources:**

- For code examples:
  - [plugins.md](examples/plugins.md) - Plugin system, encapsulation, decorators
  - [schemas.md](examples/schemas.md) - TypeBox schemas, validation, type-safe routes
  - [hooks.md](examples/hooks.md) - Lifecycle hooks and cross-cutting concerns
- For decision frameworks and anti-patterns, see [reference.md](reference.md)

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

Configure Fastify with TypeBox for compile-time AND runtime type safety.

#### Constants

```typescript
const SERVER_PORT = 3000;
const SERVER_HOST = "0.0.0.0";
```

#### Implementation

```typescript
// src/server.ts
import Fastify from "fastify";
import { TypeBoxTypeProvider } from "@fastify/type-provider-typebox";

import { errorHandler } from "./plugins/error-handler";
import { userRoutes } from "./routes/users";

const buildServer = () => {
  const server = Fastify({
    logger: {
      level: process.env.LOG_LEVEL ?? "info",
    },
  }).withTypeProvider<TypeBoxTypeProvider>();

  // Register global error handler
  server.setErrorHandler(errorHandler);

  // Register route plugins with prefixes
  server.register(userRoutes, { prefix: "/api/users" });

  return server;
};

const start = async () => {
  const server = buildServer();

  try {
    await server.listen({ port: SERVER_PORT, host: SERVER_HOST });
  } catch (error) {
    server.log.error(error);
    process.exit(1);
  }
};

// Named exports
export { buildServer, start };
```

**Why good:** TypeBox provider enables type inference from schemas, factory function enables testing, logger configured from environment

```typescript
// WRONG: No type provider, inline configuration
import Fastify from "fastify";

const server = Fastify();

server.get("/users", async (req, reply) => {
  const limit = req.query.limit; // any type!
  return { users: [] };
});

server.listen({ port: 3000 });
```

**Why bad:** No type safety on request/response, magic number for port, no error handling for startup

---

### Pattern 2: Schema Definition with TypeBox

Define schemas that provide both TypeScript types AND runtime validation.

```typescript
// src/schemas/user.ts
import { Type, Static } from "@sinclair/typebox";

const MIN_USERNAME_LENGTH = 3;
const MAX_USERNAME_LENGTH = 50;
const MIN_AGE = 0;
const MAX_AGE = 150;

export const UserSchema = Type.Object({
  id: Type.String({ format: "uuid" }),
  username: Type.String({
    minLength: MIN_USERNAME_LENGTH,
    maxLength: MAX_USERNAME_LENGTH,
  }),
  email: Type.String({ format: "email" }),
  age: Type.Optional(Type.Integer({ minimum: MIN_AGE, maximum: MAX_AGE })),
  createdAt: Type.String({ format: "date-time" }),
});

export const CreateUserSchema = Type.Object({
  username: Type.String({
    minLength: MIN_USERNAME_LENGTH,
    maxLength: MAX_USERNAME_LENGTH,
  }),
  email: Type.String({ format: "email" }),
  age: Type.Optional(Type.Integer({ minimum: MIN_AGE, maximum: MAX_AGE })),
});

export const UserParamsSchema = Type.Object({
  id: Type.String({ format: "uuid" }),
});

export const UsersQuerySchema = Type.Object({
  limit: Type.Optional(Type.Integer({ minimum: 1, maximum: 100, default: 20 })),
  offset: Type.Optional(Type.Integer({ minimum: 0, default: 0 })),
});

// Derive TypeScript types from schemas
export type User = Static<typeof UserSchema>;
export type CreateUser = Static<typeof CreateUserSchema>;
export type UserParams = Static<typeof UserParamsSchema>;
export type UsersQuery = Static<typeof UsersQuerySchema>;
```

**Why good:** Single source of truth for types and validation, named constants for constraints, Static<> derives TS types automatically

```typescript
// WRONG: Separate types and validation
interface User {
  id: string;
  username: string;
}

const validateUser = (data: unknown) => {
  if (typeof data.username !== "string") throw new Error("Invalid");
  if (data.username.length < 3) throw new Error("Too short");
  // Manual validation...
};
```

**Why bad:** Types and validation can drift apart, no JSON Schema for documentation, manual validation is error-prone

---

### Pattern 3: Route Definition with Full Schema

Define routes with request AND response schemas for complete type safety and serialization optimization.

```typescript
// src/routes/users.ts
import type { FastifyPluginAsync } from "fastify";
import { Type } from "@sinclair/typebox";

import {
  UserSchema,
  CreateUserSchema,
  UserParamsSchema,
  UsersQuerySchema,
} from "../schemas/user";

const HTTP_OK = 200;
const HTTP_CREATED = 201;
const HTTP_NOT_FOUND = 404;

const ErrorSchema = Type.Object({
  statusCode: Type.Integer(),
  error: Type.String(),
  message: Type.String(),
});

export const userRoutes: FastifyPluginAsync = async (fastify) => {
  // GET /api/users
  fastify.get(
    "/",
    {
      schema: {
        querystring: UsersQuerySchema,
        response: {
          [HTTP_OK]: Type.Object({
            users: Type.Array(UserSchema),
            total: Type.Integer(),
          }),
        },
      },
    },
    async (request, reply) => {
      const { limit, offset } = request.query;
      // request.query is typed as UsersQuery

      const users = await fastify.userService.list({ limit, offset });

      return reply.status(HTTP_OK).send({
        users,
        total: users.length,
      });
    },
  );

  // GET /api/users/:id
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
      const { id } = request.params;
      // request.params is typed as UserParams

      const user = await fastify.userService.findById(id);

      if (!user) {
        return reply.status(HTTP_NOT_FOUND).send({
          statusCode: HTTP_NOT_FOUND,
          error: "Not Found",
          message: `User ${id} not found`,
        });
      }

      return reply.status(HTTP_OK).send(user);
    },
  );

  // POST /api/users
  fastify.post(
    "/",
    {
      schema: {
        body: CreateUserSchema,
        response: {
          [HTTP_CREATED]: UserSchema,
        },
      },
    },
    async (request, reply) => {
      const userData = request.body;
      // request.body is typed as CreateUser

      const user = await fastify.userService.create(userData);

      return reply.status(HTTP_CREATED).send(user);
    },
  );
};
```

**Why good:** Response schemas enable fast-json-stringify optimization (2-3x faster), full type inference on request objects, HTTP constants prevent magic numbers

---

### Pattern 4: Plugin System with Encapsulation

Create encapsulated plugins for domain isolation, use fastify-plugin for shared utilities.

#### Encapsulated Domain Plugin

```typescript
// src/plugins/auth-routes.ts
import type { FastifyPluginAsync } from "fastify";

// This plugin is ENCAPSULATED - decorators stay within this scope
export const authRoutes: FastifyPluginAsync = async (fastify) => {
  // This decorator is only available within authRoutes
  fastify.decorate("authConfig", {
    tokenExpiry: 3600,
    refreshExpiry: 86400,
  });

  fastify.post("/login", async (request, reply) => {
    // fastify.authConfig available here
    return { token: "..." };
  });

  fastify.post("/refresh", async (request, reply) => {
    return { token: "..." };
  });
};
```

#### Shared Plugin with fastify-plugin

```typescript
// src/plugins/config.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";

type AppConfig = {
  apiVersion: string;
  environment: string;
};

// Augment Fastify types
declare module "fastify" {
  interface FastifyInstance {
    config: AppConfig;
  }
}

const configPlugin: FastifyPluginAsync = async (fastify) => {
  const config: AppConfig = {
    apiVersion: process.env.API_VERSION ?? "v1",
    environment: process.env.NODE_ENV ?? "development",
  };

  // This decorator is exposed to PARENT scope due to fastify-plugin
  fastify.decorate("config", config);
};

// Wrap with fastify-plugin to break encapsulation
export const appConfig = fp(configPlugin, {
  name: "app-config",
  dependencies: [], // Declare plugin dependencies
});
```

**Why good:** Domain plugins stay isolated (encapsulated), shared utilities use fastify-plugin to expose decorators upward, TypeScript augmentation provides type safety

```typescript
// WRONG: Shared decorator without fastify-plugin
import type { FastifyPluginAsync } from "fastify";

export const configPlugin: FastifyPluginAsync = async (fastify) => {
  fastify.decorate("config", { apiVersion: "v1" });
};

// In another file:
server.register(configPlugin);
server.register(async (fastify) => {
  // fastify.config is undefined! Encapsulation blocks access
});
```

**Why bad:** Without fastify-plugin, decorators are encapsulated and invisible to sibling/parent contexts

---

### Pattern 5: Lifecycle Hooks

Use hooks for cross-cutting concerns at appropriate lifecycle points.

```typescript
// src/plugins/request-context.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";
import { randomUUID } from "node:crypto";

const REQUEST_ID_HEADER = "x-request-id";

declare module "fastify" {
  interface FastifyRequest {
    requestId: string;
    startTime: bigint;
  }
}

const requestContextPlugin: FastifyPluginAsync = async (fastify) => {
  // onRequest: First hook, before parsing
  fastify.addHook("onRequest", async (request) => {
    request.requestId =
      request.headers[REQUEST_ID_HEADER]?.toString() ?? randomUUID();
    request.startTime = process.hrtime.bigint();

    request.log.info({ requestId: request.requestId }, "Request started");
  });

  // preHandler: After validation, before handler
  fastify.addHook("preHandler", async (request) => {
    // Add request ID to all log entries
    request.log = request.log.child({ requestId: request.requestId });
  });

  // onResponse: After response sent (for metrics/logging)
  fastify.addHook("onResponse", async (request, reply) => {
    const duration = process.hrtime.bigint() - request.startTime;
    const durationMs = Number(duration) / 1e6;

    request.log.info(
      {
        requestId: request.requestId,
        statusCode: reply.statusCode,
        durationMs,
      },
      "Request completed",
    );
  });

  // onError: Custom error logging
  fastify.addHook("onError", async (request, reply, error) => {
    request.log.error(
      {
        requestId: request.requestId,
        error: error.message,
        stack: error.stack,
      },
      "Request error",
    );
  });
};

export const requestContext = fp(requestContextPlugin, {
  name: "request-context",
});
```

**Why good:** onRequest for early setup, preHandler for validation-dependent logic, onResponse for metrics (non-blocking), onError for centralized error logging

**Hook execution order:**

1. `onRequest` - First, before body parsing
2. `preParsing` - Transform request stream
3. `preValidation` - Before schema validation
4. `preHandler` - After validation, before handler
5. `preSerialization` - Transform response before stringify
6. `onSend` - Final payload modification
7. `onResponse` - After response sent (async, non-blocking)

---

### Pattern 6: Error Handling

Implement centralized error handling with proper status codes and logging.

```typescript
// src/plugins/error-handler.ts
import type { FastifyError, FastifyReply, FastifyRequest } from "fastify";

const HTTP_BAD_REQUEST = 400;
const HTTP_NOT_FOUND = 404;
const HTTP_INTERNAL_ERROR = 500;

// Custom error classes
export class NotFoundError extends Error {
  statusCode = HTTP_NOT_FOUND;

  constructor(resource: string, id: string) {
    super(`${resource} with id ${id} not found`);
    this.name = "NotFoundError";
  }
}

export class ValidationError extends Error {
  statusCode = HTTP_BAD_REQUEST;
  details: unknown;

  constructor(message: string, details?: unknown) {
    super(message);
    this.name = "ValidationError";
    this.details = details;
  }
}

export const errorHandler = (
  error: FastifyError,
  request: FastifyRequest,
  reply: FastifyReply,
) => {
  const requestId = (request as { requestId?: string }).requestId;

  // Fastify validation errors
  if (error.validation) {
    request.log.warn(
      { requestId, validation: error.validation },
      "Validation failed",
    );

    return reply.status(HTTP_BAD_REQUEST).send({
      statusCode: HTTP_BAD_REQUEST,
      error: "Bad Request",
      message: "Validation failed",
      details: error.validation,
    });
  }

  // Custom application errors
  if ("statusCode" in error && typeof error.statusCode === "number") {
    request.log.warn({ requestId, error: error.message }, "Application error");

    return reply.status(error.statusCode).send({
      statusCode: error.statusCode,
      error: error.name,
      message: error.message,
      ...("details" in error ? { details: error.details } : {}),
    });
  }

  // Unexpected errors - log full details but send generic response
  request.log.error(
    { requestId, error: error.message, stack: error.stack },
    "Unexpected error",
  );

  return reply.status(HTTP_INTERNAL_ERROR).send({
    statusCode: HTTP_INTERNAL_ERROR,
    error: "Internal Server Error",
    message: "An unexpected error occurred",
  });
};
```

**Why good:** Fastify validation errors handled specially (expose details), custom errors with statusCode, unexpected errors logged with stack but hidden from client

---

### Pattern 7: Decorators for Service Layer

Use decorators to inject services and utilities into the Fastify instance.

```typescript
// src/plugins/services.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";

// Service interface - implement according to your domain
interface ServiceDependencies {
  // Your service dependencies here
}

// Augment Fastify types with your services
declare module "fastify" {
  interface FastifyInstance {
    // Add your service decorators here
    myService: ServiceDependencies;
  }
}

const servicesPlugin: FastifyPluginAsync = async (fastify) => {
  // Initialize your services
  const myService: ServiceDependencies = {
    // Your service implementation
  };

  // Expose via decorator
  fastify.decorate("myService", myService);
};

export const services = fp(servicesPlugin, {
  name: "services",
  dependencies: [], // List any plugin dependencies
});
```

```typescript
// src/server.ts - Registration order matters!
import { appConfig } from "./plugins/config";
import { services } from "./plugins/services";
import { userRoutes } from "./routes/users";

const buildServer = () => {
  const server = Fastify().withTypeProvider<TypeBoxTypeProvider>();

  // Register in dependency order
  server.register(appConfig);
  server.register(services);

  server.register(userRoutes, { prefix: "/api/users" });

  return server;
};
```

**Why good:** Dependencies declared explicitly, TypeScript augmentation provides type safety, fastify-plugin exposes to all routes

---

### Pattern 8: Request/Reply Decorators

Extend Request and Reply with per-request utilities.

```typescript
// src/plugins/request-utilities.ts
import fp from "fastify-plugin";
import type { FastifyPluginAsync } from "fastify";

declare module "fastify" {
  interface FastifyRequest {
    userId: string | null;
    hasPermission: (permission: string) => boolean;
  }

  interface FastifyReply {
    notFound: (message: string) => void;
    badRequest: (message: string, details?: unknown) => void;
  }
}

const HTTP_BAD_REQUEST = 400;
const HTTP_NOT_FOUND = 404;

const requestUtilitiesPlugin: FastifyPluginAsync = async (fastify) => {
  // Request decorators - use getter for per-request state
  fastify.decorateRequest("userId", null);

  // Use getter for methods that need access to request state
  fastify.decorateRequest("hasPermission", function (permission: string) {
    // 'this' is the FastifyRequest instance
    const permissions = (this as { permissions?: string[] }).permissions ?? [];
    return permissions.includes(permission);
  });

  // Reply decorators - use getter pattern for methods
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

  fastify.decorateReply(
    "badRequest",
    function (this: FastifyReply, message: string, details?: unknown) {
      this.status(HTTP_BAD_REQUEST).send({
        statusCode: HTTP_BAD_REQUEST,
        error: "Bad Request",
        message,
        ...(details ? { details } : {}),
      });
    },
  );
};

export const requestUtilities = fp(requestUtilitiesPlugin, {
  name: "request-utilities",
});
```

**Usage in routes:**

```typescript
fastify.get("/:id", async (request, reply) => {
  if (!request.hasPermission("users:read")) {
    return reply.badRequest("Insufficient permissions");
  }

  const user = await fastify.userService.findById(request.params.id);

  if (!user) {
    return reply.notFound(`User ${request.params.id} not found`);
  }

  return user;
});
```

**Why good:** Reply helpers reduce boilerplate, permission check uses request context, TypeScript augmentation provides autocomplete

---

### Pattern 9: Route-Level Hooks

Apply hooks to specific routes for authentication, authorization, or validation.

```typescript
// src/routes/admin.ts
import type { FastifyPluginAsync } from "fastify";
import type { FastifyRequest, FastifyReply } from "fastify";

const HTTP_UNAUTHORIZED = 401;
const HTTP_FORBIDDEN = 403;

// Route-level preHandler for authentication
const requireAuth = async (request: FastifyRequest, reply: FastifyReply) => {
  const token = request.headers.authorization?.replace("Bearer ", "");

  if (!token) {
    return reply.status(HTTP_UNAUTHORIZED).send({
      statusCode: HTTP_UNAUTHORIZED,
      error: "Unauthorized",
      message: "Authentication required",
    });
  }

  const user = await request.server.authService.validateToken(token);

  if (!user) {
    return reply.status(HTTP_UNAUTHORIZED).send({
      statusCode: HTTP_UNAUTHORIZED,
      error: "Unauthorized",
      message: "Invalid token",
    });
  }

  request.userId = user.id;
};

// Route-level preHandler for authorization
const requireAdmin = async (request: FastifyRequest, reply: FastifyReply) => {
  const user = await request.server.userService.findById(request.userId!);

  if (user?.role !== "admin") {
    return reply.status(HTTP_FORBIDDEN).send({
      statusCode: HTTP_FORBIDDEN,
      error: "Forbidden",
      message: "Admin access required",
    });
  }
};

export const adminRoutes: FastifyPluginAsync = async (fastify) => {
  // Apply auth to all routes in this plugin
  fastify.addHook("preHandler", requireAuth);

  // GET /admin/users - requires auth only
  fastify.get("/users", async () => {
    return fastify.userService.listAll();
  });

  // DELETE /admin/users/:id - requires auth AND admin
  fastify.delete(
    "/users/:id",
    {
      preHandler: [requireAdmin], // Additional route-level hook
    },
    async (request) => {
      const { id } = request.params as { id: string };
      await fastify.userService.delete(id);
      return { success: true };
    },
  );
};
```

**Why good:** Plugin-level hook applies to all routes, route-specific hooks for additional checks, hooks can short-circuit with reply

---

### Pattern 10: Testing Patterns

Structure tests using the buildServer factory pattern.

```typescript
// src/server.test.ts
import { describe, it, expect, beforeEach, afterEach } from "vitest";

import { buildServer } from "./server";

describe("User API", () => {
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

    const body = response.json();
    expect(body).toHaveProperty("users");
    expect(body).toHaveProperty("total");
  });

  it("should validate query parameters", async () => {
    const response = await server.inject({
      method: "GET",
      url: "/api/users",
      query: { limit: "-1" }, // Invalid: below minimum
    });

    expect(response.statusCode).toBe(400);

    const body = response.json();
    expect(body.message).toContain("Validation failed");
  });

  it("should create user with valid data", async () => {
    const response = await server.inject({
      method: "POST",
      url: "/api/users",
      payload: {
        username: "testuser",
        email: "test@example.com",
      },
    });

    expect(response.statusCode).toBe(201);

    const body = response.json();
    expect(body.username).toBe("testuser");
    expect(body.id).toBeDefined();
  });

  it("should reject invalid email format", async () => {
    const response = await server.inject({
      method: "POST",
      url: "/api/users",
      payload: {
        username: "testuser",
        email: "not-an-email",
      },
    });

    expect(response.statusCode).toBe(400);
  });
});
```

**Why good:** server.inject() tests without network overhead, beforeEach/afterEach ensures clean state, tests validation and success paths

</patterns>

---

<integration>

## Integration Guide

Fastify integrates with your existing infrastructure through its plugin system.

**External Resources:**

- Create plugins that decorate `fastify` with external clients
- Use `onClose` hook for connection cleanup
- Wrap with `fastify-plugin` to expose to all routes

**Authentication:**

- Implement auth logic in `preHandler` hooks
- Use request decorators for user state (`request.userId`)
- Plugin-level hooks for route groups, route-level for specific endpoints

**Logging:**

- Fastify's built-in logger provides high-performance JSON logging
- Configure via server options: `logger: { level: 'info' }`
- Use `request.log` for request-scoped logging with automatic request ID

**Caching:**

- Use `onSend` hook to add Cache-Control headers
- Implement ETag support in `preSerialization`
- Response schemas enable efficient serialization

**API Documentation:**

- Use `@fastify/swagger` with `@fastify/swagger-ui`
- Schemas are automatically extracted from route definitions
- TypeBox schemas generate OpenAPI-compatible JSON Schema

</integration>

---

<critical_reminders>

## CRITICAL REMINDERS

**Before implementing Fastify routes, verify:**

> **All code must follow project conventions in CLAUDE.md**

**(You MUST use `withTypeProvider<>()` for type-safe request/response handling)**

**(You MUST wrap shared plugins with `fastify-plugin` to expose decorators to parent scope)**

**(You MUST define response schemas to enable fast-json-stringify optimization)**

**(You MUST use named constants for HTTP status codes - never raw numbers)**

**Failure to follow these rules will break type safety and lose performance benefits.**

</critical_reminders>
