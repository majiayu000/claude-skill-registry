---
name: error-handling
description: Structured error classes and API error responses for this project. Custom ApiError hierarchy with HTTP status codes, withErrorHandling middleware, Zod validation handling, Convex error pattern detection. Triggers on "ApiError", "error handling", "try catch", "throw", "BadRequestError", "NotFoundError", "UnauthorizedError".
---

# Error Handling

Custom error class hierarchy with HTTP status codes for API routes. Middleware wraps handlers, detects error types, logs structured JSON, returns API envelope format.

## Error Class Hierarchy

Base ApiError with statusCode + code + message:

```typescript
// From apps/web/src/lib/api/errors.ts
export class ApiError extends Error {
  constructor(
    public statusCode: number,
    message: string,
    public code: string,
  ) {
    super(message);
    this.name = "ApiError";
  }
}
```

Specialized subclasses:

```typescript
export class BadRequestError extends ApiError {
  constructor(message: string) {
    super(400, message, "BAD_REQUEST");
  }
}

export class UnauthorizedError extends ApiError {
  constructor(message = "Authentication required") {
    super(401, message, "UNAUTHORIZED");
  }
}

export class ForbiddenError extends ApiError {
  constructor(message = "Access denied") {
    super(403, message, "FORBIDDEN");
  }
}

export class NotFoundError extends ApiError {
  constructor(entity: string, id?: string) {
    super(404, `${entity} not found${id ? `: ${id}` : ""}`, "NOT_FOUND");
  }
}

export class ConflictError extends ApiError {
  constructor(message: string) {
    super(409, message, "CONFLICT");
  }
}

export class InternalServerError extends ApiError {
  constructor(message = "Internal server error") {
    super(500, message, "INTERNAL_ERROR");
  }
}
```

## Throwing Errors in API Routes

```typescript
// NotFoundError with entity name + optional ID
if (!user) {
  throw new NotFoundError("User", userId);
}
// Returns: "User not found: 123" with 404 status

// BadRequestError for validation
if (!args.conversationId) {
  throw new BadRequestError("conversationId is required");
}

// UnauthorizedError (uses default message)
if (!userId) {
  throw new UnauthorizedError();
}
// Returns: "Authentication required" with 401 status
```

## withErrorHandling Middleware

Wrap all API route handlers with `withErrorHandling`:

```typescript
// From apps/web/src/lib/api/middleware/errors.ts
import { withErrorHandling } from "@/lib/api/middleware/errors";

export const GET = withErrorHandling(async (req: NextRequest) => {
  // Your handler logic
  const data = await fetchData();
  return NextResponse.json(formatEntity(data, "user"));
});
```

Middleware handles 4 error types:

### 1. ApiError (Custom Classes)

```typescript
if (error instanceof ApiError) {
  logger.warn(
    { error: error.message, code: error.code, url: req.url },
    "API error",
  );
  return NextResponse.json(
    formatErrorEntity({
      message: error.message,
      code: error.code,
    }),
    { status: error.statusCode },
  );
}
```

### 2. Zod Validation Errors

```typescript
if (error instanceof z.ZodError) {
  logger.warn({ issues: error.issues, url: req.url }, "Validation error");
  return NextResponse.json(
    formatErrorEntity({
      message: "Validation failed",
      code: "VALIDATION_ERROR",
      details: error.issues,
    }),
    { status: 400 },
  );
}
```

### 3. Convex Error Pattern Detection

Convex throws Error with text patterns. Parse message string:

```typescript
if (error instanceof Error) {
  const message = error.message;

  // Not found pattern
  if (message.includes("not found")) {
    logger.warn({ error: message, url: req.url }, "Resource not found");
    return NextResponse.json(formatErrorEntity("Resource not found"), {
      status: 404,
    });
  }

  // Unauthorized pattern
  if (
    message.includes("unauthorized") ||
    message.includes("permission")
  ) {
    logger.warn({ error: message, url: req.url }, "Unauthorized");
    return NextResponse.json(formatErrorEntity("Access denied"), {
      status: 403,
    });
  }
}
```

### 4. Unhandled Errors

```typescript
// Catch-all for unexpected errors
logger.error(
  {
    error: error instanceof Error ? error.message : String(error),
    stack: error instanceof Error ? error.stack : undefined,
    url: req.url,
  },
  "Unhandled error",
);

return NextResponse.json(formatErrorEntity("Internal server error"), {
  status: 500,
});
```

## Convex Error Handling

Convex functions throw errors directly (no status codes):

```typescript
// In Convex queries/mutations
export const getUser = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    const user = await ctx.db.get(args.userId);
    if (!user) {
      throw new Error("User not found");
    }
    return user;
  },
});
```

API middleware detects "not found" in message, returns 404.

## Custom Error Classes for Domain Logic

Create custom errors for specific scenarios:

```typescript
// From packages/backend/convex/lib/budgetTracker.ts
export class TimeoutError extends Error {
  constructor(
    public readonly operation: string,
    public readonly timeoutMs: number,
  ) {
    super(`${operation} timed out after ${timeoutMs}ms`);
    this.name = "TimeoutError";
  }
}
```

Use in async operations:

```typescript
export async function withTimeout<T>(
  promise: Promise<T>,
  timeoutMs: number,
  operation: string,
): Promise<T> {
  let timeoutId: ReturnType<typeof setTimeout>;

  const timeoutPromise = new Promise<never>((_, reject) => {
    timeoutId = setTimeout(() => {
      reject(new TimeoutError(operation, timeoutMs));
    }, timeoutMs);
  });

  try {
    const result = await Promise.race([promise, timeoutPromise]);
    clearTimeout(timeoutId!);
    return result;
  } catch (error) {
    clearTimeout(timeoutId!);
    throw error;
  }
}
```

## Logging Conventions

Always use structured Pino logging:

```typescript
import logger from "@/lib/logger";

// Warn level for expected errors (4xx)
logger.warn({ error: message, code, url }, "API error");

// Error level for unexpected errors (5xx)
logger.error({ error: message, stack, url }, "Unhandled error");
```

Log fields:
- `error`: Error message (string)
- `code`: Error code (e.g., "NOT_FOUND")
- `stack`: Stack trace (for 5xx errors)
- `url`: Request URL
- `issues`: Zod validation issues array

## API Response Format

All errors return envelope format via `formatErrorEntity`:

```typescript
// Single error
formatErrorEntity("User not found")
// Returns:
// {
//   status: "error",
//   sys: { entity: "error" },
//   error: "User not found"
// }

// Error with code and details
formatErrorEntity({
  message: "Validation failed",
  code: "VALIDATION_ERROR",
  details: zodError.issues,
})
// Returns:
// {
//   status: "error",
//   sys: { entity: "error" },
//   error: {
//     message: "Validation failed",
//     code: "VALIDATION_ERROR",
//     details: [...]
//   }
// }
```

## Key Files

- `apps/web/src/lib/api/errors.ts` - Error class definitions
- `apps/web/src/lib/api/middleware/errors.ts` - withErrorHandling middleware
- `apps/web/src/lib/utils/formatEntity.ts` - formatErrorEntity helper
- `apps/web/src/lib/logger.ts` - Pino structured logger
- `packages/backend/convex/lib/budgetTracker.ts` - TimeoutError example

## Error Handling Patterns

### API Route Pattern

```typescript
import { withErrorHandling } from "@/lib/api/middleware/errors";
import { BadRequestError, NotFoundError } from "@/lib/api/errors";
import { formatEntity } from "@/lib/utils/formatEntity";

export const GET = withErrorHandling(async (req: NextRequest) => {
  const userId = req.nextUrl.searchParams.get("userId");
  if (!userId) {
    throw new BadRequestError("userId is required");
  }

  const user = await getUser(userId);
  if (!user) {
    throw new NotFoundError("User", userId);
  }

  return NextResponse.json(formatEntity(user, "user"));
});
```

### Convex Query Pattern

```typescript
export const getUser = query({
  args: { userId: v.id("users") },
  handler: async (ctx, args) => {
    // Throws Error (no status codes in Convex)
    const user = await ctx.db.get(args.userId);
    if (!user) {
      throw new Error("User not found");
    }
    return user;
  },
});
```

### Timeout Wrapper Pattern

```typescript
try {
  const result = await withTimeout(
    expensiveOperation(),
    30000,
    "expensiveOperation",
  );
} catch (error) {
  if (error instanceof TimeoutError) {
    logger.warn({ operation: error.operation, timeout: error.timeoutMs });
    throw new InternalServerError("Operation timed out");
  }
  throw error;
}
```

## Avoid

- Don't throw raw Error in API routes - use ApiError subclasses
- Don't return error responses directly - let middleware handle it
- Don't use console.log - use structured logger
- Don't forget to wrap API handlers with withErrorHandling
- Don't check error.message string in API routes - use instanceof
- Don't include stack traces in production error responses (middleware strips them)
- Don't use HTTP status codes in Convex functions (throw Error only)
