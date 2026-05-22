---
name: error-handling
model: standard
description: Error handling patterns across languages and layers — operational vs programmer errors, retry strategies, circuit breakers, error boundaries, HTTP responses, graceful degradation, and structured logging. Use when designing error strategies, building resilient APIs, or reviewing error management.
---

# Error Handling Patterns

> Ship resilient software. Handle errors at boundaries, fail fast and loud, never swallow exceptions silently.

## Error Handling Philosophy

| Principle | Description |
|-----------|-------------|
| **Fail Fast** | Detect errors early — validate inputs at the boundary, not deep in business logic |
| **Fail Loud** | Errors must be visible — log them, surface them, alert on them |
| **Handle at Boundaries** | Catch and translate errors at layer boundaries (controller, middleware, gateway) |
| **Let It Crash** | For unrecoverable state, crash and restart (Erlang/OTP philosophy) |
| **Be Specific** | Catch specific error types, never bare `catch` or `except` |
| **Provide Context** | Every error carries enough context to diagnose without reproducing |


## Installation

### OpenClaw / Moltbot / Clawbot

```bash
npx clawhub@latest install error-handling
```


---

## Error Types

**Operational errors** — network timeouts, invalid user input, file not found, DB connection lost. Handle gracefully.

**Programmer errors** — `TypeError`, null dereference, assertion failures. Fix the code — don't catch and suppress.

```javascript
// Operational — handle gracefully
try {
  const data = await fetch('/api/users');
} catch (err) {
  if (err.code === 'ECONNREFUSED') return fallbackData;
  throw err; // re-throw unexpected errors
}

// Programmer — let it crash, fix the bug
const user = null;
user.name; // TypeError — don't try/catch this
```

---

## Language Patterns

| Language | Mechanism | Anti-Pattern |
|----------|-----------|-------------|
| **JavaScript** | `try/catch`, `Promise.catch`, Error subclasses | `.catch(() => {})` swallowing errors |
| **Python** | Exceptions, context managers (`with`) | Bare `except:` catching everything |
| **Go** | `error` returns, `errors.Is/As`, `fmt.Errorf` wrapping | `_ = riskyFunction()` ignoring error |
| **Rust** | `Result<T, E>`, `Option<T>`, `?` operator | `.unwrap()` in production code |

### JavaScript — Error Subclasses

```javascript
class AppError extends Error {
  constructor(message, code, statusCode, details = {}) {
    super(message);
    this.name = this.constructor.name;
    this.code = code;
    this.statusCode = statusCode;
    this.details = details;
    this.isOperational = true;
  }
}

class NotFoundError extends AppError {
  constructor(resource, id) {
    super(`${resource} not found`, 'NOT_FOUND', 404, { resource, id });
  }
}

class ValidationError extends AppError {
  constructor(errors) {
    super('Validation failed', 'VALIDATION_ERROR', 422, { errors });
  }
}
```

### Go — Error Wrapping

```go
func GetUser(id string) (*User, error) {
    row := db.QueryRow("SELECT * FROM users WHERE id = $1", id)
    var user User
    if err := row.Scan(&user.ID, &user.Name); err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            return nil, fmt.Errorf("user %s: %w", id, ErrNotFound)
        }
        return nil, fmt.Errorf("querying user %s: %w", id, err)
    }
    return &user, nil
}
```

---

## Error Boundaries

### Express Error Middleware

```javascript
app.use((err, req, res, next) => {
  const statusCode = err.statusCode || 500;
  const response = {
    error: {
      code: err.code || 'INTERNAL_ERROR',
      message: err.isOperational ? err.message : 'Something went wrong',
      ...(process.env.NODE_ENV === 'development' && { stack: err.stack }),
      requestId: req.id,
    },
  };

  logger.error('Request failed', {
    err, requestId: req.id, method: req.method, path: req.path,
  });

  res.status(statusCode).json(response);
});
```

### React Error Boundary

```tsx
import { ErrorBoundary } from 'react-error-boundary';

function ErrorFallback({ error, resetErrorBoundary }) {
  return (
    <div role="alert">
      <h2>Something went wrong</h2>
      <pre>{error.message}</pre>
      <button onClick={resetErrorBoundary}>Try again</button>
    </div>
  );
}

<ErrorBoundary FallbackComponent={ErrorFallback} onReset={() => queryClient.clear()}>
  <App />
</ErrorBoundary>
```

---

## Retry Patterns

| Pattern | When to Use | Config |
|---------|-------------|--------|
| **Exponential Backoff** | Transient failures (network, 503) | Base 1s, max 30s, factor 2x |
| **Backoff + Jitter** | Multiple clients retrying | Random ±30% on each delay |
| **Circuit Breaker** | Downstream service failing repeatedly | Open after 5 failures, half-open after 30s |
| **Bulkhead** | Isolate failures to prevent cascade | Limit concurrent calls per service |
| **Timeout** | Prevent indefinite hangs | Connect 5s, read 30s, total 60s |

### Exponential Backoff with Jitter

```javascript
async function withRetry(fn, { maxRetries = 3, baseDelay = 1000, maxDelay = 30000 } = {}) {
  for (let attempt = 0; attempt <= maxRetries; attempt++) {
    try {
      return await fn();
    } catch (err) {
      if (attempt === maxRetries || !isRetryable(err)) throw err;
      const delay = Math.min(baseDelay * 2 ** attempt, maxDelay);
      const jitter = delay * (0.7 + Math.random() * 0.6);
      await new Promise((r) => setTimeout(r, jitter));
    }
  }
}

function isRetryable(err) {
  return [408, 429, 500, 502, 503, 504].includes(err.statusCode) || err.code === 'ECONNRESET';
}
```

### Circuit Breaker

```javascript
class CircuitBreaker {
  constructor({ threshold = 5, resetTimeout = 30000 } = {}) {
    this.state = 'CLOSED';       // CLOSED → OPEN → HALF_OPEN → CLOSED
    this.failureCount = 0;
    this.threshold = threshold;
    this.resetTimeout = resetTimeout;
    this.nextAttempt = 0;
  }

  async call(fn) {
    if (this.state === 'OPEN') {
      if (Date.now() < this.nextAttempt) throw new Error('Circuit is OPEN');
      this.state = 'HALF_OPEN';
    }
    try {
      const result = await fn();
      this.onSuccess();
      return result;
    } catch (err) {
      this.onFailure();
      throw err;
    }
  }

  onSuccess() { this.failureCount = 0; this.state = 'CLOSED'; }
  onFailure() {
    this.failureCount++;
    if (this.failureCount >= this.threshold) {
      this.state = 'OPEN';
      this.nextAttempt = Date.now() + this.resetTimeout;
    }
  }
}
```

---

## HTTP Error Responses

| Status | Name | When to Use |
|--------|------|-------------|
| **400** | Bad Request | Malformed syntax, invalid JSON |
| **401** | Unauthorized | Missing or invalid authentication |
| **403** | Forbidden | Authenticated but insufficient permissions |
| **404** | Not Found | Resource does not exist |
| **409** | Conflict | Request conflicts with current state |
| **422** | Unprocessable Entity | Valid syntax but semantic errors |
| **429** | Too Many Requests | Rate limit exceeded (include `Retry-After`) |
| **500** | Internal Server Error | Unexpected server failure |
| **502** | Bad Gateway | Upstream returned invalid response |
| **503** | Service Unavailable | Temporarily overloaded or maintenance |

### Standard Error Envelope

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "The request body contains invalid fields.",
    "details": [
      { "field": "email", "message": "Must be a valid email address" }
    ],
    "requestId": "req_abc123xyz"
  }
}
```

---

## Graceful Degradation

| Strategy | Example |
|----------|---------|
| **Fallback values** | Show cached avatar when image service is down |
| **Feature flags** | Disable unstable recommendation engine |
| **Cached responses** | Serve stale data with `X-Cache: STALE` header |
| **Partial response** | Return available data with `warnings` array |

```javascript
async function getProductPage(productId) {
  const product = await productService.get(productId); // critical — propagate errors

  const [reviews, recommendations] = await Promise.allSettled([
    reviewService.getForProduct(productId),
    recommendationService.getForProduct(productId),
  ]);

  return {
    product,
    reviews: reviews.status === 'fulfilled' ? reviews.value : [],
    recommendations: recommendations.status === 'fulfilled' ? recommendations.value : [],
    warnings: [reviews, recommendations]
      .filter((r) => r.status === 'rejected')
      .map((r) => ({ service: 'degraded', reason: r.reason.message })),
  };
}
```

---

## Logging & Monitoring

| Practice | Implementation |
|----------|---------------|
| **Structured logging** | JSON: `level`, `message`, `error`, `requestId`, `userId`, `timestamp` |
| **Error tracking** | Sentry, Datadog, Bugsnag — automatic capture with source maps |
| **Alert thresholds** | Error rate > 1%, P99 latency > 2s, 5xx spike |
| **Correlation IDs** | Pass `requestId` through all service calls |
| **Log levels** | `error` = needs attention, `warn` = degraded, `info` = normal, `debug` = dev |

---

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| **Swallowing errors** `catch (e) {}` | Log and re-throw, or handle explicitly |
| **Generic catch-all** at every level | Catch specific types, let unexpected errors bubble |
| **Error as control flow** | Use conditionals, return values, or option types |
| **Stringly-typed errors** `throw "wrong"` | Throw `Error` objects with codes and context |
| **Logging and throwing** | Log at the boundary only, or wrap and re-throw |
| **Catch-and-return-null** | Return `Result` type, throw, or return error object |
| **Ignoring Promise rejections** | Always `await` or attach `.catch()` |
| **Exposing internals** | Sanitize responses; log details server-side only |

---

## NEVER Do

1. **NEVER swallow errors silently** — `catch (e) {}` hides bugs and causes silent data corruption
2. **NEVER expose stack traces, SQL errors, or file paths in API responses** — log details server-side only
3. **NEVER use string throws** — `throw 'error'` has no stack trace, no type, no context
4. **NEVER catch and return null without explanation** — callers have no idea why the operation failed
5. **NEVER ignore unhandled Promise rejections** — always `await` or attach `.catch()`
6. **NEVER cache error responses** — 5xx and transient errors must not be cached and re-served
7. **NEVER use exceptions for normal control flow** — exceptions are for exceptional conditions
8. **NEVER return generic "Something went wrong" without logging the real error** — always log the full error server-side with request context
