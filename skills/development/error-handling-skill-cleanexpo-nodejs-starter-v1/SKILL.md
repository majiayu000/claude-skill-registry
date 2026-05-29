---
name: error-handling
category: verification
version: 2.0.0
description: Error handling patterns with Australian user-friendly messages
author: Unite Group
priority: 2
---

# Error Handling Patterns

## Principles

1. **Fail Fast**: Detect errors early and report them immediately
2. **Fail Clearly**: Error messages should be actionable (en-AU friendly)
3. **Fail Safely**: Errors should not corrupt state or leak data
4. **Fail Loudly**: Errors should be logged and observable

## Error Types

### Expected Errors
Errors that can occur during normal operation:
- Validation failures
- Authentication failures
- Resource not found
- Rate limiting

Handle these gracefully with user-friendly messages (Australian English).

### Unexpected Errors
Errors that indicate bugs or system failures:
- Null pointer exceptions
- Database connection failures
- Out of memory errors
- Network timeouts

Log these with full context and return generic error to user.

## Frontend Error Handling

### API Errors
```typescript
interface ApiError extends Error {
  status: number;
  message: string;
  details?: Record<string, any>;
}

async function fetchWithErrorHandling<T>(
  url: string,
  options?: RequestInit
): Promise<T> {
  try {
    const response = await fetch(url, options);

    if (!response.ok) {
      const error = await response.json();
      throw new ApiError(error.message, response.status, error.details);
    }

    return response.json();
  } catch (error) {
    if (error instanceof ApiError) {
      // Handle known API errors with Australian-friendly messages
      const message = getAustralianFriendlyMessage(error);
      toast.error(message);
      throw error;
    } else {
      // Handle unexpected errors
      console.error('Unexpected error:', error);
      toast.error('Something went wrong. Please try again.');
      throw new Error('Unexpected error occurred');
    }
  }
}

function getAustralianFriendlyMessage(error: ApiError): string {
  """Convert error to Australian-friendly message."""
  const messages: Record<number, string> = {
    400: "We couldn't process that request. Please check your input.",
    401: "You'll need to log in to access this.",
    403: "You don't have permission to do that.",
    404: "We couldn't find what you're looking for.",
    422: "Please check your input and try again.",
    429: "You're going a bit too fast. Please wait a moment.",
    500: "Something's gone wrong on our end. We're looking into it.",
    503: "We're experiencing some technical difficulties. Please try again soon."
  };

  return messages[error.status] || "Something went wrong. Please try again.";
}
```

### Error Boundaries
```typescript
import { Component, ErrorInfo, ReactNode } from 'react';

interface Props {
  children: ReactNode;
  fallback?: ReactNode;
}

interface State {
  hasError: boolean;
  error?: Error;
}

export class ErrorBoundary extends Component<Props, State> {
  constructor(props: Props) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(error: Error): State {
    return { hasError: true, error };
  }

  componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error('Error boundary caught:', error, errorInfo);
    // Report to error tracking service
    reportError(error, {
      componentStack: errorInfo.componentStack,
      locale: 'en-AU'
    });
  }

  render() {
    if (this.state.hasError) {
      return this.props.fallback || (
        <div className="error-fallback">
          <h2>Something went wrong</h2>
          <p>We're sorry, but something unexpected happened. Please refresh the page and try again.</p>
          <button onClick={() => window.location.reload()}>
            Refresh Page
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
```

## Backend Error Handling

### FastAPI Exception Handlers
```python
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from pydantic import ValidationError
import structlog

logger = structlog.get_logger()

@app.exception_handler(ValidationError)
async def validation_exception_handler(request: Request, exc: ValidationError):
    """Handle validation errors with Australian-friendly messages."""
    logger.warning(
        "Validation error",
        path=request.url.path,
        errors=exc.errors()
    )

    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "message": "Please check your input and try again.",  # en-AU
            "details": exc.errors()
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.info(
        "HTTP exception",
        status_code=exc.status_code,
        detail=exc.detail,
        path=request.url.path
    )

    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error(
        "Unhandled exception",
        error=str(exc),
        path=request.url.path,
        exc_info=True
    )

    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "message": "Something went wrong on our end. We're looking into it."  # en-AU
        }
    )
```

### Agent Error Handling
```python
from typing import TypeVar, Callable
import asyncio
from functools import wraps

T = TypeVar('T')

class RetryableError(Exception):
    """Error that can be retried."""
    pass

class FatalError(Exception):
    """Error that should not be retried."""
    pass

class MaxRetriesExceeded(Exception):
    """Maximum retries exceeded."""
    pass

async def execute_with_retry(
    task: Callable[[], T],
    max_retries: int = 3,
    backoff_base: float = 2.0
) -> T:
    """Execute task with exponential backoff retry."""
    last_error = None

    for attempt in range(max_retries):
        try:
            return await task()
        except RetryableError as e:
            last_error = e
            logger.warning(
                "Retryable error",
                attempt=attempt + 1,
                max_retries=max_retries,
                error=str(e)
            )
            if attempt < max_retries - 1:
                await asyncio.sleep(backoff_base ** attempt)
        except FatalError as e:
            logger.error("Fatal error", error=str(e))
            raise

    raise MaxRetriesExceeded(
        f"Failed after {max_retries} attempts: {last_error}"
    )

def handle_agent_errors(func: Callable) -> Callable:
    """Decorator for agent error handling."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except ValidationError as e:
            logger.error("Agent validation error", error=str(e))
            raise FatalError(f"Invalid input: {e}")
        except Exception as e:
            logger.error("Agent error", error=str(e), exc_info=True)
            raise RetryableError(f"Agent failed: {e}")

    return wrapper
```

## Error Logging

### What to Log
- Error type and message
- Stack trace
- Request context (URL, method, user ID)
- Timestamp (Australian timezone: AEST/AEDT)
- Relevant state/data (sanitized)
- Australian context (locale, state, regulations)

### What NOT to Log
- Passwords
- API keys
- PII (unless necessary and compliant with Privacy Act 1988)
- Credit card numbers
- ABN/ACN (unless required for compliance audit)

### Structured Logging (Australian Context)
```python
import structlog

logger = structlog.get_logger()

logger.error(
    "Failed to process task",
    error=str(e),
    task_id=task.id,
    user_id=user.id,
    attempt=attempt,
    locale="en-AU",
    state="QLD",
    timezone="Australia/Brisbane",
    timestamp=datetime.now().isoformat()
)
```

## Error Monitoring

```python
from typing import Optional

async def report_error(
    error: Exception,
    context: dict,
    user_id: Optional[str] = None
):
    """Report error to monitoring service."""
    await error_tracking_service.report({
        "error": str(error),
        "type": type(error).__name__,
        "context": context,
        "user_id": user_id,
        "locale": "en-AU",
        "timestamp": datetime.now().isoformat(),
        "environment": os.getenv("ENVIRONMENT", "production")
    })
```

## Australian Compliance

### Privacy Act 1988 Considerations
When handling errors that involve personal data:

```python
def sanitize_error_for_logging(error: Exception, context: dict) -> dict:
    """Remove PII from error context per Privacy Act 1988."""
    sensitive_fields = {"email", "phone", "address", "abn", "acn", "medicare"}

    sanitized = {}
    for key, value in context.items():
        if key.lower() in sensitive_fields:
            sanitized[key] = "[REDACTED]"
        else:
            sanitized[key] = value

    return sanitized
```

## Integration with Verification

This skill integrates with:
- `verification/verification-first.skill.md` - Error handling in verification
- `backend/fastapi.skill.md` - API error handling
- `backend/langgraph.skill.md` - Agent error handling

See: `core/VERIFICATION.md`, `backend/FASTAPI.md`
