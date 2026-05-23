---
name: add-error-type
description: Add a new custom error type for domain-specific errors. Use when creating errors for specific business rules or HTTP status codes. Triggers on "add error", "custom error", "error type".
---

# Add Error Type

Adds a new domain error type that extends `BaseError`. All custom errors are defined in `src/errors.ts` and automatically handled by the global error handler.

## Quick Reference

**File**: `src/errors.ts`
**Base class**: `BaseError`
**Auto HTTP mapping**: `errorCode` number maps to HTTP status

## Existing Error Types

| Error Class               | HTTP Status | Use Case                        |
| ------------------------- | ----------- | ------------------------------- |
| `BadRequestError`         | 400         | Invalid input, validation fails |
| `UnauthenticatedError`    | 401         | Missing or invalid credentials  |
| `UnauthorizedError`       | 403         | Lacks permission for action     |
| `NotFoundError`           | 404         | Resource doesn't exist          |
| `InternalServerError`     | 500         | Unexpected server errors        |
| `ServiceUnavailableError` | 503         | External service down           |

## Instructions

### Step 1: Add Error Class to `src/errors.ts`

```typescript
export class {ErrorName}Error extends BaseError {
  constructor(
    message: string = "Default error message",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: {HTTP_STATUS_CODE} });
  }
}
```

### Step 2: Use in Services/Controllers

```typescript
import { {ErrorName}Error } from "@/errors";

// Throw when condition is met
if (someCondition) {
  throw new {ErrorName}Error("Specific error message");
}

// With cause for debugging
throw new {ErrorName}Error("Error message", { cause: originalError });
```

## Common HTTP Status Codes

| Code | Name                  | When to Use                              |
| ---- | --------------------- | ---------------------------------------- |
| 400  | Bad Request           | Malformed request, validation failure    |
| 401  | Unauthenticated       | No credentials or invalid credentials    |
| 403  | Forbidden             | Valid credentials but lacks permission   |
| 404  | Not Found             | Resource doesn't exist                   |
| 409  | Conflict              | Resource state conflict (duplicate, etc) |
| 422  | Unprocessable Entity  | Semantic errors in valid syntax          |
| 429  | Too Many Requests     | Rate limiting                            |
| 500  | Internal Server Error | Unexpected server-side errors            |
| 502  | Bad Gateway           | Upstream service returned invalid        |
| 503  | Service Unavailable   | Server temporarily unavailable           |
| 504  | Gateway Timeout       | Upstream service timeout                 |

## Examples

### Conflict Error (409)

```typescript
export class ConflictError extends BaseError {
  constructor(
    message: string = "Resource conflict",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 409 });
  }
}

// Usage
if (await repository.findByEmail(email)) {
  throw new ConflictError("User with this email already exists");
}
```

### Rate Limit Error (429)

```typescript
export class RateLimitError extends BaseError {
  constructor(
    message: string = "Too many requests",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 429 });
  }
}

// Usage
if (requestCount > limit) {
  throw new RateLimitError("Rate limit exceeded. Try again later.");
}
```

### Validation Error (422)

```typescript
export class ValidationError extends BaseError {
  constructor(
    message: string = "Validation failed",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 422 });
  }
}

// Usage with cause containing field errors
throw new ValidationError("Invalid input data", {
  cause: { field: "email", message: "Invalid email format" },
});
```

### Gateway Error (502)

```typescript
export class BadGatewayError extends BaseError {
  constructor(
    message: string = "Bad Gateway",
    options?: Omit<BaseErrorOptions, "errorCode">,
  ) {
    super(message, { ...options, errorCode: 502 });
  }
}

// Usage
if (!upstreamResponse.ok) {
  throw new BadGatewayError("Upstream service returned invalid response");
}
```

### Using HttpError for One-off Status Codes

For status codes that don't need a dedicated class:

```typescript
import { HttpError } from "@/errors";

// One-off 451 (Unavailable For Legal Reasons)
throw new HttpError(451, "Content unavailable in your region");

// One-off 507 (Insufficient Storage)
throw new HttpError(507, "Storage quota exceeded");
```

## BaseError Structure

```typescript
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
```

## Global Error Handler

The `globalErrorHandler` in `src/errors.ts` automatically:

1. Logs the error
2. Converts `BaseError` instances to JSON responses
3. Maps `errorCode` to HTTP status
4. Wraps unknown errors in `InternalServerError`

```typescript
export const globalErrorHandler = (err: Error, c: Context<AppEnv>) => {
  console.error(err);

  if (err instanceof BaseError) {
    return createErrorResponse(c, err); // Uses errorCode as HTTP status
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

## What NOT to Do

- Do NOT catch and re-throw as generic Error (loses type info)
- Do NOT return error responses manually (use error classes)
- Do NOT use non-standard HTTP status codes without good reason
- Do NOT forget to set `errorCode` (defaults to 500)
- Do NOT put stack traces in error messages (use `cause` for debugging)

## See Also

- `create-middleware` - Global error handler setup
- `create-utility-service` - Error handling in services
- `create-controller` - Throwing errors from controllers
