---
name: error-handling-patterns
description: Robust error handling patterns for TypeScript applications
license: MIT
compatibility: typescript 5+, nodejs 18+
allowed-tools: read_file write_file apply_patch search_with_context
---

# Error Handling Patterns

## Core Principles

1. **Fail fast** - Detect and report errors early
2. **Fail safely** - Errors shouldn't crash the application
3. **Fail informatively** - Provide actionable error messages
4. **Recover gracefully** - Handle expected failures

## Custom Error Classes

```typescript
// Base application error
export class AppError extends Error {
  constructor(
    message: string,
    public readonly code: string,
    public readonly statusCode: number = 500,
    public readonly details?: unknown
  ) {
    super(message);
    this.name = this.constructor.name;
    Error.captureStackTrace(this, this.constructor);
  }

  toJSON() {
    return {
      code: this.code,
      message: this.message,
      ...(this.details && { details: this.details }),
    };
  }
}

// Specific error types
export class ValidationError extends AppError {
  constructor(message: string, details?: Record<string, string>) {
    super(message, 'VALIDATION_ERROR', 400, details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string, id: string) {
    super(`${resource} with id '${id}' not found`, 'NOT_FOUND', 404);
  }
}

export class UnauthorizedError extends AppError {
  constructor(message = 'Authentication required') {
    super(message, 'UNAUTHORIZED', 401);
  }
}

export class ForbiddenError extends AppError {
  constructor(message = 'Insufficient permissions') {
    super(message, 'FORBIDDEN', 403);
  }
}
```

## Result Type Pattern

```typescript
type Result<T, E = Error> =
  | { success: true; data: T }
  | { success: false; error: E };

// Helper functions
function ok<T>(data: T): Result<T, never> {
  return { success: true, data };
}

function err<E>(error: E): Result<never, E> {
  return { success: false, error };
}

// Usage
async function findUser(id: string): Promise<Result<User, NotFoundError>> {
  const user = await db.users.findUnique({ where: { id } });
  if (!user) {
    return err(new NotFoundError('User', id));
  }
  return ok(user);
}

// Consuming
const result = await findUser('123');
if (!result.success) {
  console.error(result.error.message);
  return;
}
const user = result.data; // Type-safe User
```

## Error Boundaries (React)

```typescript
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
  onError?: (error: Error, info: ErrorInfo) => void;
}

interface State {
  hasError: boolean;
  error: Error | null;
}

export class ErrorBoundary extends Component<Props, State> {
  state: State = { hasError: false, error: null };

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    this.props.onError?.(error, info);
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback ?? (
        <div role="alert">
          <h2>Something went wrong</h2>
          <pre>{this.state.error?.message}</pre>
        </div>
      );
    }
    return this.props.children;
  }
}
```

## Async Error Handling

```typescript
// Wrapper for async functions
function tryCatch<T>(
  promise: Promise<T>
): Promise<[null, T] | [Error, null]> {
  return promise
    .then((data) => [null, data] as [null, T])
    .catch((error) => [error as Error, null]);
}

// Usage
const [error, user] = await tryCatch(fetchUser(id));
if (error) {
  handleError(error);
  return;
}
// user is guaranteed to be defined here

// Multiple operations
async function processOrder(orderId: string) {
  const [orderError, order] = await tryCatch(getOrder(orderId));
  if (orderError) return err(orderError);

  const [paymentError] = await tryCatch(processPayment(order));
  if (paymentError) {
    await tryCatch(rollbackOrder(order));
    return err(paymentError);
  }

  return ok(order);
}
```

## Retry Pattern

```typescript
interface RetryOptions {
  maxAttempts: number;
  delayMs: number;
  backoff?: 'linear' | 'exponential';
  shouldRetry?: (error: Error) => boolean;
}

async function withRetry<T>(
  fn: () => Promise<T>,
  options: RetryOptions
): Promise<T> {
  const { maxAttempts, delayMs, backoff = 'exponential', shouldRetry } = options;
  let lastError: Error;

  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      return await fn();
    } catch (error) {
      lastError = error as Error;

      if (shouldRetry && !shouldRetry(lastError)) {
        throw lastError;
      }

      if (attempt < maxAttempts) {
        const delay = backoff === 'exponential'
          ? delayMs * Math.pow(2, attempt - 1)
          : delayMs * attempt;
        await sleep(delay);
      }
    }
  }

  throw lastError!;
}

// Usage
const data = await withRetry(() => fetchFromAPI(), {
  maxAttempts: 3,
  delayMs: 1000,
  shouldRetry: (err) => err.message.includes('timeout'),
});
```

## Validation Errors

```typescript
import { z } from 'zod';

function validateInput<T>(schema: z.ZodSchema<T>, input: unknown): Result<T, ValidationError> {
  const result = schema.safeParse(input);

  if (!result.success) {
    const details = result.error.flatten().fieldErrors;
    return err(new ValidationError('Invalid input', details));
  }

  return ok(result.data);
}

// Usage
const userSchema = z.object({
  email: z.string().email(),
  age: z.number().min(18),
});

const result = validateInput(userSchema, req.body);
if (!result.success) {
  return res.status(400).json(result.error.toJSON());
}
```

## Logging Errors

```typescript
interface ErrorContext {
  userId?: string;
  requestId?: string;
  path?: string;
  [key: string]: unknown;
}

function logError(error: Error, context: ErrorContext = {}) {
  const payload = {
    timestamp: new Date().toISOString(),
    name: error.name,
    message: error.message,
    stack: error.stack,
    ...(error instanceof AppError && { code: error.code }),
    ...context,
  };

  console.error(JSON.stringify(payload));

  // Send to error tracking service
  if (process.env.NODE_ENV === 'production') {
    // Sentry.captureException(error, { extra: context });
  }
}
```

## Best Practices

1. **Create specific error types** for different failure modes
2. **Use Result types** for expected failures (validation, not found)
3. **Throw errors** for unexpected failures (bugs, system errors)
4. **Include context** in error messages for debugging
5. **Log at boundaries** - API handlers, event processors
6. **Validate at boundaries** - external input, API responses
7. **Implement retry** for transient failures
8. **Use error boundaries** in React for graceful degradation
