---
name: setup-errors
description: Configure error handling infrastructure with custom error types and global handler. Use when adding error handling to a project. Triggers on "setup errors", "add errors", "error handling", "error infrastructure".
---

# Setup Errors

Configures error handling infrastructure with a base error class, common HTTP error types, and a global error handler for Hono.

## Quick Reference

**Files created**:

- `src/errors.ts` - Base error class, HTTP error types, global handler

**When to use**: After bootstrapping a project, before creating services or controllers

## Prerequisites

- Project bootstrapped with `bootstrap-project`
- Hono installed as a dependency

## Instructions

### Phase 1: Create Error Infrastructure

#### Step 1: Create Error File

Create `src/errors.ts`:

```typescript
import type { Context } from "hono";
import { HTTPException } from "hono/http-exception";
import type { AppEnv } from "@/schemas/app-env.schema";

type ErrorCode = number;

interface BaseErrorOptions {
  cause?: unknown;
  errorCode?: ErrorCode;
}

export class BaseError extends Error {
  public readonly cause?: unknown;
  public readonly errorCode?: ErrorCode;

  constructor(message: string, options?: BaseErrorOptions) {
    super(message);
    this.name = this.constructor.name;
    this.cause = options?.cause;
    this.errorCode = options?.errorCode;
    Object.setPrototypeOf(this, new.target.prototype);
  }

  public toJSON(): { error: string; code?: ErrorCode; cause?: string } {
    const json: { error: string; code?: ErrorCode; cause?: string } = {
      error: this.message,
    };
    if (this.errorCode !== undefined) {
      json.code = this.errorCode;
    }
    if (this.cause instanceof Error && this.cause.message) {
      json.cause = this.cause.message;
    }
    return json;
  }
}

export class BadRequestError extends BaseError {
  constructor(
    message: string = "Bad Request",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 400 });
  }
}

export class UnauthenticatedError extends BaseError {
  constructor(
    message: string = "Authentication required",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 401 });
  }
}

export class UnauthorizedError extends BaseError {
  constructor(
    message: string = "Access denied",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 403 });
  }
}

export class NotFoundError extends BaseError {
  constructor(
    message: string = "Resource not found",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 404 });
  }
}

export class ConflictError extends BaseError {
  constructor(
    message: string = "Resource conflict",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 409 });
  }
}

export class InternalServerError extends BaseError {
  constructor(
    message: string = "Internal server error",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 500 });
  }
}

export class ServiceUnavailableError extends BaseError {
  constructor(
    message: string = "Service temporarily unavailable",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 503 });
  }
}

function createErrorResponse(c: Context<AppEnv>, error: BaseError) {
  const statusCode = error.errorCode || 500;
  return c.json(error.toJSON(), statusCode as any);
}

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
```

### Phase 2: Integrate with App

#### Step 2: Update App to Use Error Handler

Update `src/app.ts` to use the global error handler:

```typescript
import { Hono } from "hono";
import type { AppEnv } from "@/schemas/app-env.schema";
import { globalErrorHandler } from "@/errors";

const app = new Hono<AppEnv>();

app.get("/", (c) => c.text("Hello Hono!"));

// Error handler (add at the end)
app.onError(globalErrorHandler);

export { app };
```

## Usage Patterns

### Throwing Errors in Services

```typescript
import { NotFoundError, UnauthorizedError } from "@/errors";

export class NoteService {
  async findById(id: string, user: AuthenticatedUserContextType) {
    const note = await this.repository.findById(id);

    if (!note) {
      throw new NotFoundError(`Note with id ${id} not found`);
    }

    if (note.createdBy !== user.userId && user.globalRole !== "admin") {
      throw new UnauthorizedError("You do not have access to this note");
    }

    return note;
  }
}
```

### Throwing Errors with Cause

```typescript
import { InternalServerError } from "@/errors";

try {
  await externalService.call();
} catch (error) {
  throw new InternalServerError("External service failed", { cause: error });
}
```

### Error Response Format

All errors return JSON in this format:

```json
{
  "error": "Error message here",
  "code": 404,
  "cause": "Original error message (if provided)"
}
```

## Available Error Types

| Error Class               | HTTP Status | Default Message                   |
| ------------------------- | ----------- | --------------------------------- |
| `BadRequestError`         | 400         | "Bad Request"                     |
| `UnauthenticatedError`    | 401         | "Authentication required"         |
| `UnauthorizedError`       | 403         | "Access denied"                   |
| `NotFoundError`           | 404         | "Resource not found"              |
| `ConflictError`           | 409         | "Resource conflict"               |
| `InternalServerError`     | 500         | "Internal server error"           |
| `ServiceUnavailableError` | 503         | "Service temporarily unavailable" |

## Files Created Summary

```plaintext
src/
└── errors.ts    # Base error class, HTTP error types, global handler
```

## Adding Custom Error Types

To add a new error type, extend `BaseError`:

```typescript
export class RateLimitError extends BaseError {
  constructor(
    message: string = "Too many requests",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 429 });
  }
}
```

See the `add-error-type` skill for detailed instructions.

## What NOT to Do

- Do NOT throw plain `Error` objects in services/controllers (use typed errors)
- Do NOT catch errors in controllers unless you need to transform them
- Do NOT include sensitive information in error messages
- Do NOT forget to add `app.onError(globalErrorHandler)` to your app

## See Also

- `add-error-type` - Add custom domain-specific error types
- `create-middleware` - Create validation middleware that throws BadRequestError
- `create-resource-service` - Services that use these error types
