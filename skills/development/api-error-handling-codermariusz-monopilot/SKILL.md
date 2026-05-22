---
name: api-error-handling
description: Apply when designing error responses, implementing error handlers, and ensuring consistent error format across APIs.
version: 1.1.0
tokens: ~650
confidence: high
sources:
  - https://www.rfc-editor.org/rfc/rfc9457
  - https://datatracker.ietf.org/doc/html/rfc9110#section-6
last_validated: 2025-12-10
next_review: 2025-12-24
tags: [api, error-handling, backend, rest]
---

## When to Use

Apply when designing error responses, implementing error handlers, and ensuring consistent error format across APIs.

## Patterns

### Pattern 1: Standard Error Response Format
```typescript
// Source: https://www.rfc-editor.org/rfc/rfc9457 (Problem Details)
interface ApiError {
  error: {
    code: string;           // Machine-readable code
    message: string;        // Human-readable message
    details?: ErrorDetail[];// Field-level errors
    requestId?: string;     // For debugging
  };
}

interface ErrorDetail {
  field: string;
  message: string;
  code?: string;
}

// Example response
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Request validation failed",
    "details": [
      { "field": "email", "message": "Invalid email format", "code": "INVALID_FORMAT" },
      { "field": "age", "message": "Must be positive", "code": "INVALID_RANGE" }
    ],
    "requestId": "req_abc123"
  }
}
```

### Pattern 2: Error Class Hierarchy
```typescript
// Source: Best practice pattern
class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number,
    public details?: ErrorDetail[]
  ) {
    super(message);
    this.name = 'AppError';
  }
}

class ValidationError extends AppError {
  constructor(details: ErrorDetail[]) {
    super('VALIDATION_ERROR', 'Validation failed', 400, details);
  }
}

class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}

class UnauthorizedError extends AppError {
  constructor() {
    super('UNAUTHORIZED', 'Authentication required', 401);
  }
}
```

### Pattern 3: Global Error Handler (Express/Next.js)
```typescript
// Source: Best practice pattern
function errorHandler(
  err: Error,
  req: Request,
  res: Response,
  next: NextFunction
) {
  // Log for debugging
  console.error('Error:', {
    message: err.message,
    stack: err.stack,
    requestId: req.headers['x-request-id'],
  });

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details,
        requestId: req.headers['x-request-id'],
      },
    });
  }

  // Unknown error - don't leak details
  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred',
      requestId: req.headers['x-request-id'],
    },
  });
}
```

### Pattern 4: Frontend Error Handling
```typescript
// Source: Best practice pattern
async function apiCall<T>(url: string, options?: RequestInit): Promise<T> {
  const response = await fetch(url, options);

  if (!response.ok) {
    const error = await response.json();
    throw new ApiError(error.error.code, error.error.message, error.error.details);
  }

  return response.json();
}

// Usage with error handling
try {
  const user = await apiCall<User>('/api/users/123');
} catch (error) {
  if (error instanceof ApiError) {
    if (error.code === 'NOT_FOUND') {
      showNotification('User not found');
    } else if (error.code === 'VALIDATION_ERROR') {
      setFormErrors(error.details);
    }
  }
}
```

### Pattern 5: Error Code Constants
```typescript
// Source: Best practice pattern
export const ErrorCodes = {
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  CONFLICT: 'CONFLICT',
  RATE_LIMITED: 'RATE_LIMITED',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
} as const;

type ErrorCode = typeof ErrorCodes[keyof typeof ErrorCodes];
```

## Anti-Patterns

- **Exposing stack traces** - Never in production
- **Generic "Error occurred"** - Provide actionable messages
- **200 for errors** - Use appropriate HTTP status codes
- **Inconsistent format** - Same structure for all errors

## Verification Checklist

- [ ] All errors have code + message
- [ ] Status codes match error type
- [ ] Validation errors include field details
- [ ] Stack traces hidden in production
- [ ] Request ID for debugging correlation
