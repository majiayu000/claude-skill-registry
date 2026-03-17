---
name: api-error-handling
description: Implements standardized API error responses with proper status codes, logging, and user-friendly messages. Use when building production APIs, implementing error recovery patterns, or integrating error monitoring services.
---

# API Error Handling

Implement robust error handling with standardized responses and proper logging.

## Standard Error Response Format

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request parameters",
    "status": 400,
    "requestId": "req_abc123",
    "timestamp": "2025-01-15T10:30:00Z",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

## Error Class (Node.js)

```javascript
class ApiError extends Error {
  constructor(code, message, status = 500, details = null) {
    super(message);
    this.code = code;
    this.status = status;
    this.details = details;
  }

  static badRequest(message, details) {
    return new ApiError('BAD_REQUEST', message, 400, details);
  }

  static notFound(resource) {
    return new ApiError('NOT_FOUND', `${resource} not found`, 404);
  }

  static unauthorized() {
    return new ApiError('UNAUTHORIZED', 'Authentication required', 401);
  }
}

// Global error handler
app.use((err, req, res, next) => {
  const status = err.status || 500;
  const response = {
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: status === 500 ? 'Internal server error' : err.message,
      status,
      requestId: req.id
    }
  };

  if (err.details) response.error.details = err.details;
  if (status >= 500) logger.error(err);

  res.status(status).json(response);
});
```

## Circuit Breaker Pattern

```javascript
class CircuitBreaker {
  constructor(threshold = 5, timeout = 30000) {
    this.failures = 0;
    this.threshold = threshold;
    this.timeout = timeout;
    this.state = 'CLOSED';
  }

  async call(fn) {
    if (this.state === 'OPEN') throw new Error('Circuit open');
    try {
      const result = await fn();
      this.failures = 0;
      return result;
    } catch (err) {
      this.failures++;
      if (this.failures >= this.threshold) {
        this.state = 'OPEN';
        setTimeout(() => this.state = 'HALF_OPEN', this.timeout);
      }
      throw err;
    }
  }
}
```

## Additional Implementations

See [references/python-flask.md](references/python-flask.md) for:
- Python Flask error handling with custom exceptions
- Circuit breaker with automatic recovery
- Retry with exponential backoff
- Sentry integration

## Best Practices

- Use consistent error format across all endpoints
- Include request IDs for traceability
- Log errors at appropriate severity levels
- Never expose stack traces to clients
- Distinguish client errors (4xx) from server errors (5xx)
- Provide actionable error messages
