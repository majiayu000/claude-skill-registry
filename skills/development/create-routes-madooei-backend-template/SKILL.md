---
name: create-routes
description: Create route definitions for HTTP endpoints. Use when wiring controllers and middleware to HTTP routes. Triggers on "create routes", "router for", "route definitions".
---

# Create Routes

Creates Hono route definitions that wire controllers and middleware to HTTP endpoints. Routes use a factory function pattern for dependency injection.

## Quick Reference

**Location**: `src/routes/{entity-name}.router.ts`
**Naming**: Singular for entities (`note.router.ts`), plural for cross-cutting (`events.router.ts`)

## Prerequisites

Before creating routes, ensure you have:

1. Controller created (`src/controllers/{entity-name}.controller.ts`)
2. Schemas for validation (`src/schemas/{entity-name}.schema.ts`)
3. Middleware (auth, validation) available

## Instructions

### Step 1: Create the Router File

Create `src/routes/{entity-name}.router.ts`

### Step 2: Import Dependencies

```typescript
import { Hono } from "hono";
import type { {Entity}Controller } from "@/controllers/{entity-name}.controller";
import type { AppEnv } from "@/schemas/app-env.schema";
import { validate as defaultValidate } from "@/middlewares/validation.middleware";
import { entityIdParamSchema } from "@/schemas/shared.schema";
import {
  create{Entity}Schema,
  {entity}QueryParamsSchema,
} from "@/schemas/{entity-name}.schema";
import { authMiddleware as defaultAuthMiddleware } from "@/middlewares/auth.middleware";
```

### Step 3: Define Dependencies Interface

```typescript
export interface Create{Entity}RoutesDeps {
  {entity}Controller: {Entity}Controller;
  validate?: typeof defaultValidate;
  authMiddleware?: typeof defaultAuthMiddleware;
}
```

### Step 4: Create Factory Function

```typescript
export const create{Entity}Routes = (dependencies: Create{Entity}RoutesDeps) => {
  const {
    {entity}Controller,
    validate = defaultValidate,
    authMiddleware = defaultAuthMiddleware,
  } = dependencies;

  const {entity}Routes = new Hono<AppEnv>();

  // Apply auth middleware to all routes
  {entity}Routes.use("*", authMiddleware);

  // Define routes...

  return {entity}Routes;
};
```

### Step 5: Define CRUD Routes

```typescript
// GET / - List all
{entity}Routes.get(
  "/",
  validate({
    schema: {entity}QueryParamsSchema,
    source: "query",
    varKey: "validatedQuery",
  }),
  {entity}Controller.getAll,
);

// GET /:id - Get by ID
{entity}Routes.get(
  "/:id",
  validate({
    schema: entityIdParamSchema("id"),
    source: "params",
    varKey: "validatedParams",
  }),
  {entity}Controller.getById,
);

// POST / - Create
{entity}Routes.post(
  "/",
  validate({
    schema: create{Entity}Schema,
    source: "body",
    varKey: "validatedBody",
  }),
  {entity}Controller.create,
);

// PUT /:id - Update (full replace)
{entity}Routes.put(
  "/:id",
  validate({
    schema: entityIdParamSchema("id"),
    source: "params",
    varKey: "validatedParams",
  }),
  validate({
    schema: create{Entity}Schema,
    source: "body",
    varKey: "validatedBody",
  }),
  {entity}Controller.update,
);

// DELETE /:id - Delete
{entity}Routes.delete(
  "/:id",
  validate({
    schema: entityIdParamSchema("id"),
    source: "params",
    varKey: "validatedParams",
  }),
  {entity}Controller.delete,
);
```

## Patterns & Rules

### Factory Function Pattern

Always use a factory function with dependency injection:

```typescript
export const create{Entity}Routes = (dependencies: Create{Entity}RoutesDeps) => {
  const { {entity}Controller, validate = defaultValidate } = dependencies;

  const router = new Hono<AppEnv>();
  // ...
  return router;
};
```

This enables:

- Testing with mock dependencies
- Flexible middleware injection
- Consistent instantiation pattern

### Type Controllers in Interface

Use `type` import for controllers to avoid circular dependencies:

```typescript
import type { {Entity}Controller } from "@/controllers/{entity-name}.controller";

export interface Create{Entity}RoutesDeps {
  {entity}Controller: {Entity}Controller;  // Not a class, just the type
}
```

### Default Middleware Imports

Import middleware with aliases and provide as defaults:

```typescript
import { validate as defaultValidate } from "@/middlewares/validation.middleware";
import { authMiddleware as defaultAuthMiddleware } from "@/middlewares/auth.middleware";

// In factory function
const { validate = defaultValidate, authMiddleware = defaultAuthMiddleware } =
  dependencies;
```

### Global vs Per-Route Middleware

Apply shared middleware globally, specific middleware per-route:

```typescript
// Global auth for all routes
{
  entity;
}
Routes.use("*", authMiddleware);

// Per-route validation
{
  entity;
}
Routes.get(
  "/",
  validate({ schema: querySchema, source: "query", varKey: "validatedQuery" }),
  controller.getAll,
);
```

### Validation Middleware Chaining

For routes needing multiple validations, chain middleware:

```typescript
{entity}Routes.put(
  "/:id",
  validate({ schema: entityIdParamSchema("id"), source: "params", varKey: "validatedParams" }),
  validate({ schema: updateSchema, source: "body", varKey: "validatedBody" }),
  {entity}Controller.update,
);
```

### Route Typing

Always type routers with `AppEnv`:

```typescript
const {entity}Routes = new Hono<AppEnv>();
```

## Mounting Routes in App

Routes are mounted in `src/app.ts`:

```typescript
import { createNoteRoutes } from "@/routes/note.router";
import { NoteController } from "@/controllers/note.controller";
import { NoteService } from "@/services/note.service";

// Create dependency chain
const noteService = new NoteService();
const noteController = new NoteController(noteService);

// Mount routes
app.route("/notes", createNoteRoutes({ noteController }));
```

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a complete `note.router.ts` implementation.

## What NOT to Do

- Do NOT instantiate controllers inside route files (inject them)
- Do NOT use untyped `new Hono()` (always use `new Hono<AppEnv>()`)
- Do NOT hardcode middleware (allow injection for testing)
- Do NOT forget to return the router from the factory function
- Do NOT put business logic in routes (that's for controllers/services)

## See Also

- `create-controller` - Create controllers for route handlers
- `create-middleware` - Create validation and auth middleware
- `test-routes` - Test route configurations
