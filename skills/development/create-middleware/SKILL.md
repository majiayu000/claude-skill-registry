---
name: create-middleware
description: Create middleware for cross-cutting concerns. Use when creating authentication, validation, or other request processing middleware. Triggers on "create middleware", "auth middleware", "validation middleware".
---

# Create Middleware

Creates Hono middleware for cross-cutting concerns like authentication, validation, and error handling.

## Quick Reference

**Location**: `src/middlewares/{middleware-name}.middleware.ts`
**Naming**: Descriptive, kebab-case (e.g., `auth.middleware.ts`, `validation.middleware.ts`)

## Middleware Types

Examples of middleware types:

| Type           | Purpose                                    | Example                    |
| -------------- | ------------------------------------------ | -------------------------- |
| Authentication | Verify user identity, set `c.var.user`     | `auth.middleware.ts`       |
| Validation     | Validate request data, set validated vars  | `validation.middleware.ts` |
| Error Handling | Global error handler for consistent errors | In `src/errors.ts`         |

## Creating Authentication Middleware

### Step 1: Create the File

Create `src/middlewares/auth.middleware.ts`

### Step 2: Define Dependencies Interface

```typescript
import { createMiddleware } from "hono/factory";
import type { AppEnv } from "@/schemas/app-env.schema";
import { AuthenticationService } from "@/services/authentication.service";
import { UnauthenticatedError } from "@/errors";

export interface AuthMiddlewareDeps {
  authenticationService: AuthenticationService;
}
```

### Step 3: Create Factory Function

```typescript
export const createAuthMiddleware = (deps: AuthMiddlewareDeps) => {
  const { authenticationService } = deps;

  return createMiddleware<AppEnv>(async (c, next) => {
    const authHeader = c.req.header("Authorization");
    if (!authHeader)
      throw new UnauthenticatedError("Authorization header is missing.");

    const parts = authHeader.split(" ");
    let token: string | undefined;

    if (parts.length === 2 && parts[0].toLowerCase() === "bearer") {
      token = parts[1];
    }
    if (!token) throw new UnauthenticatedError("Invalid authorization format.");

    // Will throw errors if it cannot authenticate
    const user = await authenticationService.authenticateUserByToken(token);

    c.set("user", user);
    await next();
  });
};
```

### Step 4: Export Default Instance

```typescript
const defaultAuthenticationService = new AuthenticationService();
export const authMiddleware = createAuthMiddleware({
  authenticationService: defaultAuthenticationService,
});
```

## Creating Validation Middleware

The validation middleware is generic and validates body, query, or params using Zod schemas.

### Factory Function

```typescript
import type { MiddlewareHandler } from "hono";
import { createMiddleware } from "hono/factory";
import type { ZodTypeAny } from "zod";
import type { AppEnv } from "@/schemas/app-env.schema";
import { BadRequestError, InternalServerError } from "@/errors";

export type ValidationDataSource = "body" | "query" | "params";

interface ValidationOptions {
  schema: ZodTypeAny;
  source: ValidationDataSource;
  varKey: string;
}

export const validate = (
  options: ValidationOptions,
): MiddlewareHandler<AppEnv> => {
  const { schema, source, varKey } = options;

  return createMiddleware<AppEnv>(async (c, next) => {
    let dataToValidate: unknown;

    try {
      switch (source) {
        case "body":
          dataToValidate = await c.req.json();
          break;
        case "query":
          dataToValidate = c.req.query();
          break;
        case "params":
          dataToValidate = c.req.param();
          break;
        default:
          throw new InternalServerError();
      }
    } catch (error) {
      if (error instanceof InternalServerError) throw error;
      throw new BadRequestError(`Invalid request ${source}.`);
    }

    const result = schema.safeParse(dataToValidate);

    if (!result.success) {
      const fieldErrors = result.error.flatten().fieldErrors;
      const fieldErrorMessages = Object.entries(fieldErrors)
        .map(([field, errors]) => `${field}: ${errors?.join(", ")}`)
        .join("; ");
      throw new BadRequestError(
        `Validation failed for ${source}. ${fieldErrorMessages}`,
        { cause: result.error.flatten() },
      );
    }

    c.set(varKey as keyof AppEnv["Variables"], result.data);
    await next();
  });
};
```

## Patterns & Rules

### Use `createMiddleware` Factory

Always use Hono's `createMiddleware` with `AppEnv` type:

```typescript
import { createMiddleware } from "hono/factory";
import type { AppEnv } from "@/schemas/app-env.schema";

return createMiddleware<AppEnv>(async (c, next) => {
  // Middleware logic
  await next();
});
```

### Dependency Injection Pattern

Create a factory function that accepts dependencies:

```typescript
export interface MyMiddlewareDeps {
  someService: SomeService;
}

export const createMyMiddleware = (deps: MyMiddlewareDeps) => {
  return createMiddleware<AppEnv>(async (c, next) => {
    // Use deps.someService
    await next();
  });
};

// Export default instance
export const myMiddleware = createMyMiddleware({
  someService: new SomeService(),
});
```

### Setting Context Variables

Store data for downstream handlers using `c.set()`:

```typescript
// In middleware
c.set("user", authenticatedUser);
c.set("validatedBody", parsedData);

// In controller
const user = c.var.user as AuthenticatedUserContextType;
```

### Error Throwing

Throw domain errors - global handler converts to HTTP responses:

```typescript
import { UnauthenticatedError, BadRequestError } from "@/errors";

// Authentication errors
if (!token) throw new UnauthenticatedError("Missing token");

// Validation errors
if (!result.success) throw new BadRequestError("Invalid data");
```

### Always Call `next()`

After successful processing, always call `await next()`:

```typescript
return createMiddleware<AppEnv>(async (c, next) => {
  // Process request...

  // Pass to next handler
  await next();
});
```

## Global Error Handler

The global error handler converts domain errors to HTTP responses:

```typescript
// In src/errors.ts
export const globalErrorHandler = (err: Error, c: Context<AppEnv>) => {
  console.error(err);

  if (err instanceof BaseError) {
    return createErrorResponse(c, err);
  } else if (err instanceof HTTPException) {
    return c.json({ error: err.message }, err.status);
  } else {
    const internalError = new InternalServerError(
      "An unexpected error occurred",
      { cause: err },
    );
    return createErrorResponse(c, internalError);
  }
};

// Register in app setup
app.onError(globalErrorHandler);
```

## Complete Examples

See [REFERENCE.md](REFERENCE.md) for complete examples:

- `auth.middleware.ts` - Authentication with dependency injection
- `validation.middleware.ts` - Generic validation middleware

## Usage in Routes

```typescript
import { authMiddleware } from "@/middlewares/auth.middleware";
import { validate } from "@/middlewares/validation.middleware";
import { createNoteSchema, noteQueryParamsSchema } from "@/schemas/note.schema";
import { entityIdParamSchema } from "@/schemas/shared.schema";

// Apply to routes
router.get(
  "/",
  authMiddleware,
  validate({
    schema: noteQueryParamsSchema,
    source: "query",
    varKey: "validatedQuery",
  }),
  controller.getAll,
);

router.post(
  "/",
  authMiddleware,
  validate({
    schema: createNoteSchema,
    source: "body",
    varKey: "validatedBody",
  }),
  controller.create,
);

router.get(
  "/:id",
  authMiddleware,
  validate({
    schema: entityIdParamSchema,
    source: "params",
    varKey: "validatedParams",
  }),
  controller.getById,
);
```

## What NOT to Do

- Do NOT use `MiddlewareHandler` type directly (use `createMiddleware` factory)
- Do NOT forget to call `await next()`
- Do NOT catch errors (let global handler catch them)
- Do NOT access `process.env` directly (use `@/env`)
- Do NOT put business logic in middleware (that's for services)

## See Also

- `create-routes` - Wire middleware to routes
- `add-error-type` - Add custom error types
- `test-middleware` - Test middleware handlers
