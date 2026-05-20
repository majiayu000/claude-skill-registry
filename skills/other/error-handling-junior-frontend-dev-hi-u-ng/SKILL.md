---
name: error-handling
description: Implement consistent error handling across the application.
  Use when adding try-catch blocks, error boundaries, or custom error classes.
---

# Error Handling Skill

## Purpose
Ensure consistent, informative error handling.

## Backend Error Handling
Reference: [patterns/backend-errors.md](patterns/backend-errors.md)

### Custom Error Classes
```typescript
// templates/error-class.ts
export class AppError extends Error {
  constructor(
    public code: string,
    message: string,
    public statusCode: number = 500,
    public details?: unknown
  ) {
    super(message);
    this.name = 'AppError';
  }
}

export class ValidationError extends AppError {
  constructor(message: string, details?: unknown) {
    super('VALIDATION_ERROR', message, 400, details);
  }
}

export class NotFoundError extends AppError {
  constructor(resource: string) {
    super('NOT_FOUND', `${resource} not found`, 404);
  }
}
```

### Error Handler Middleware
```typescript
function errorHandler(err, req, res, next) {
  logger.error(err);

  if (err instanceof AppError) {
    return res.status(err.statusCode).json({
      error: {
        code: err.code,
        message: err.message,
        details: err.details
      }
    });
  }

  return res.status(500).json({
    error: {
      code: 'INTERNAL_ERROR',
      message: 'An unexpected error occurred'
    }
  });
}
```

## Frontend Error Handling
Reference: [patterns/frontend-errors.md](patterns/frontend-errors.md)

### Error Boundaries
```tsx
class ErrorBoundary extends React.Component {
  state = { hasError: false };

  static getDerivedStateFromError() {
    return { hasError: true };
  }

  componentDidCatch(error, info) {
    logError(error, info);
  }

  render() {
    if (this.state.hasError) {
      return <ErrorFallback onReset={() => this.setState({ hasError: false })} />;
    }
    return this.props.children;
  }
}
```

### Async Error Handling
```typescript
async function fetchWithError<T>(url: string): Promise<T> {
  const response = await fetch(url);

  if (!response.ok) {
    const error = await response.json();
    throw new ApiError(error.code, error.message);
  }

  return response.json();
}
```

## Logging Guidelines
| Level | Use For |
|-------|---------|
| error | Exceptions, failures |
| warn | Recoverable issues |
| info | Important events |
| debug | Development info |
