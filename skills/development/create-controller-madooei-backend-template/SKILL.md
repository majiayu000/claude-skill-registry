---
name: create-controller
description: Create a controller for handling HTTP requests. Use when creating a controller to connect routes to services. Triggers on "create controller", "controller for", "HTTP handler".
---

# Create Controller

Creates a controller that handles HTTP requests and responses. Controllers are thin layers that extract data from requests, call services, and return responses.

## Quick Reference

**Location**: `src/controllers/{entity-name}.controller.ts`
**Naming**: Singular, kebab-case (e.g., `note.controller.ts`, `user.controller.ts`)

## Prerequisites

Before creating a controller, ensure you have:

1. Schema created with request/response types (`src/schemas/{entity-name}.schema.ts`)
2. Service created (`src/services/{entity-name}.service.ts`)

## Instructions

### Step 1: Create the Controller File

Create `src/controllers/{entity-name}.controller.ts`

### Step 2: Import Dependencies

```typescript
import type { Context } from "hono";
import { {Entity}Service } from "@/services/{entity-name}.service";
import type { EntityIdParamType } from "@/schemas/shared.schema";
import type {
  Create{Entity}Type,
  {Entity}QueryParamsType,
  Update{Entity}Type,
} from "@/schemas/{entity-name}.schema";
import type { AppEnv } from "@/schemas/app-env.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import { NotFoundError } from "@/errors";
```

### Step 3: Create the Controller Class

```typescript
export class {Entity}Controller {
  private {entity}Service: {Entity}Service;

  constructor({entity}Service?: {Entity}Service) {
    if ({entity}Service) {
      this.{entity}Service = {entity}Service;
    } else {
      this.{entity}Service = new {Entity}Service();
    }
  }

  // Handler methods...
}
```

### Step 4: Implement CRUD Handlers

#### getAll

```typescript
getAll = async (c: Context<AppEnv>): Promise<Response> => {
  const user = c.var.user as AuthenticatedUserContextType;
  const query = c.var.validatedQuery as {Entity}QueryParamsType;
  const {entities} = await this.{entity}Service.getAll(query, user);
  return c.json({entities});
};
```

#### getById

```typescript
getById = async (c: Context<AppEnv>): Promise<Response> => {
  const user = c.var.user as AuthenticatedUserContextType;
  const { id } = c.var.validatedParams as EntityIdParamType;
  const {entity} = await this.{entity}Service.getById(id, user);
  if (!{entity}) throw new NotFoundError();
  return c.json({entity});
};
```

#### create

```typescript
create = async (c: Context<AppEnv>): Promise<Response> => {
  const user = c.var.user as AuthenticatedUserContextType;
  const body = c.var.validatedBody as Create{Entity}Type;
  const {entity} = await this.{entity}Service.create(body, user);
  return c.json({entity});
};
```

#### update

```typescript
update = async (c: Context<AppEnv>): Promise<Response> => {
  const user = c.var.user as AuthenticatedUserContextType;
  const { id } = c.var.validatedParams as EntityIdParamType;
  const body = c.var.validatedBody as Update{Entity}Type;
  const {entity} = await this.{entity}Service.update(id, body, user);
  if (!{entity}) throw new NotFoundError();
  return c.json({entity});
};
```

#### delete

```typescript
delete = async (c: Context<AppEnv>): Promise<Response> => {
  const user = c.var.user as AuthenticatedUserContextType;
  const { id } = c.var.validatedParams as EntityIdParamType;
  const success = await this.{entity}Service.delete(id, user);
  if (!success) throw new NotFoundError();
  return c.json({ message: "{Entity} deleted successfully" });
};
```

## Patterns & Rules

### Handler Method Pattern

Use arrow functions assigned to class properties for handlers:

```typescript
// Correct - arrow function maintains `this` binding
getAll = async (c: Context<AppEnv>): Promise<Response> => {
  // ...
};

// Wrong - regular method loses `this` when passed as callback
async getAll(c: Context<AppEnv>): Promise<Response> {
  // ...
}
```

### Context Variables

Data is pre-validated by middleware and stored in `c.var`:

```typescript
// User from auth middleware
const user = c.var.user as AuthenticatedUserContextType;

// Validated query params from validation middleware
const query = c.var.validatedQuery as {Entity}QueryParamsType;

// Validated request body from validation middleware
const body = c.var.validatedBody as Create{Entity}Type;

// Validated URL params from validation middleware
const { id } = c.var.validatedParams as EntityIdParamType;
```

### Dependency Injection

Allow service injection for testing:

```typescript
constructor({entity}Service?: {Entity}Service) {
  if ({entity}Service) {
    this.{entity}Service = {entity}Service;
  } else {
    this.{entity}Service = new {Entity}Service();
  }
}
```

### Error Handling

Controllers throw domain errors - global error handler converts to HTTP:

```typescript
// Service returns null for not found
const {entity} = await this.{entity}Service.getById(id, user);
if (!{entity}) throw new NotFoundError();

// Service throws UnauthorizedError for permission denied
// Let it propagate - global handler catches it
```

### Response Format

Use `c.json()` for all responses:

```typescript
// Return entity
return c.json({ entity });

// Return paginated result
return c.json({ entities }); // { data: [...], total: n, page: 1, ... }

// Return success message
return c.json({ message: "{Entity} deleted successfully" });
```

### AppEnv Type

Always type Context with `AppEnv`:

```typescript
import type { AppEnv } from "@/schemas/app-env.schema";

getAll = async (c: Context<AppEnv>): Promise<Response> => {
  // c.var is properly typed
};
```

The `AppEnv` interface provides types for:

- `c.var.user` - Authenticated user context
- `c.var.validatedQuery` - Validated query parameters
- `c.var.validatedBody` - Validated request body
- `c.var.validatedParams` - Validated URL parameters

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a complete `NoteController` implementation.

## What NOT to Do

- Do NOT validate input in controllers (use validation middleware)
- Do NOT access `c.req.json()` directly (use `c.var.validatedBody`)
- Do NOT catch errors (let global error handler catch them)
- Do NOT return HTTP status codes manually (use domain errors)
- Do NOT put business logic in controllers (that's for services)
- Do NOT use regular methods (use arrow functions for `this` binding)

## See Also

- `create-routes` - Wire controller handlers to routes with middleware
- `create-middleware` - Create validation and auth middleware
- `test-controller` - Test controller handlers
