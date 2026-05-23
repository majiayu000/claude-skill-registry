---
name: error-sanitization
description: Production-safe error handling that logs full details server-side while exposing only generic, safe messages to users. Prevents information leakage of database strings, file paths, stack traces, and API keys.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: security
  time: 2h
  source: drift-masterguide
---

# Error Sanitization

Production-safe error handling: log everything server-side, expose nothing sensitive to users.

## When to Use This Skill

- Building APIs that return error messages to clients
- Handling exceptions in production environments
- Processing batch operations with partial failures
- Any system where error messages could leak sensitive information

## Core Concepts

Error messages can leak sensitive information including database connection strings, internal file paths, stack traces, API keys, and business logic details. The solution is to always log full error details server-side for debugging while returning only generic, safe messages to users.

The flow is:
1. Exception occurs
2. Log FULL error server-side with context
3. Classify error type
4. Return GENERIC message to user
5. Only expose safe, actionable errors (like validation)

## Implementation

### Python

```python
import os
import logging
from typing import Optional
from fastapi import HTTPException
from pydantic import ValidationError

logger = logging.getLogger(__name__)


class ErrorSanitizer:
    """
    Sanitizes error messages to prevent information leakage.
    """
    
    SENSITIVE_PATTERNS = [
        "password", "secret", "key", "token", "credential",
        "postgresql://", "mysql://", "mongodb://", "redis://",
        "localhost", "127.0.0.1", "internal", "0.0.0.0",
        "traceback", "exception", "error at", "line ",
        "/home/", "/var/", "/etc/", "C:\\",
        "SUPABASE", "AWS", "STRIPE", "SENDGRID",
    ]
    
    @staticmethod
    def is_production() -> bool:
        return os.getenv("ENVIRONMENT", "development").lower() == "production"
    
    @staticmethod
    def sanitize_error(
        e: Exception,
        user_message: str = "Operation failed",
        log_context: Optional[dict] = None
    ) -> str:
        """Sanitize error message for user display."""
        # ALWAYS log full error server-side
        logger.error(
            f"Error occurred: {type(e).__name__}: {str(e)}",
            exc_info=True,
            extra=log_context or {}
        )
        
        # In development, show more details
        if not ErrorSanitizer.is_production():
            return f"{user_message}: {str(e)}"
        
        # Validation errors are safe (user input issues)
        if isinstance(e, ValidationError):
            return f"Validation error: {str(e)}"
        
        # HTTPException with client error (4xx) is safe
        if isinstance(e, HTTPException):
            if 400 <= e.status_code < 500:
                return e.detail
            return user_message
        
        # Check for sensitive patterns
        error_str = str(e).lower()
        for pattern in ErrorSanitizer.SENSITIVE_PATTERNS:
            if pattern in error_str:
                return user_message
        
        # Short, simple errors without sensitive patterns might be safe
        if len(str(e)) < 100 and not any(c in str(e) for c in ['/', '\\', '@', ':']):
            return str(e)
        
        return user_message
    
    @staticmethod
    def create_http_exception(
        e: Exception,
        status_code: int = 500,
        user_message: str = "Operation failed",
        log_context: Optional[dict] = None
    ) -> HTTPException:
        """Create HTTPException with sanitized error message."""
        safe_message = ErrorSanitizer.sanitize_error(e, user_message, log_context)
        return HTTPException(status_code=status_code, detail=safe_message)
```

### TypeScript

```typescript
import { Logger } from './logger';

const SENSITIVE_PATTERNS = [
  'password', 'secret', 'key', 'token', 'credential',
  'postgresql://', 'mysql://', 'mongodb://', 'redis://',
  'localhost', '127.0.0.1', 'internal', '0.0.0.0',
  '/home/', '/var/', '/etc/', 'C:\\',
];

interface SanitizeOptions {
  userMessage?: string;
  logContext?: Record<string, unknown>;
}

export class ErrorSanitizer {
  private static isProduction(): boolean {
    return process.env.NODE_ENV === 'production';
  }

  static sanitize(
    error: Error,
    options: SanitizeOptions = {}
  ): string {
    const { userMessage = 'Operation failed', logContext = {} } = options;

    // Always log full error server-side
    Logger.error('Error occurred', {
      name: error.name,
      message: error.message,
      stack: error.stack,
      ...logContext,
    });

    // In development, show more details
    if (!this.isProduction()) {
      return `${userMessage}: ${error.message}`;
    }

    // Check for sensitive patterns
    const errorStr = error.message.toLowerCase();
    for (const pattern of SENSITIVE_PATTERNS) {
      if (errorStr.includes(pattern)) {
        return userMessage;
      }
    }

    // Short, simple errors might be safe
    if (error.message.length < 100 && !/[\/\\@:]/.test(error.message)) {
      return error.message;
    }

    return userMessage;
  }

  static createHttpError(
    error: Error,
    statusCode: number = 500,
    options: SanitizeOptions = {}
  ): { statusCode: number; message: string } {
    return {
      statusCode,
      message: this.sanitize(error, options),
    };
  }
}
```

## Usage Examples

### Route Handler

```python
@router.post("/process")
async def process_invoice(invoice_id: str):
    try:
        result = await processor.process(invoice_id)
        return result
    except ValidationError as e:
        # Validation errors are safe to expose
        raise HTTPException(status_code=400, detail=str(e))
    except HTTPException:
        raise  # Re-raise as-is
    except Exception as e:
        # All other errors get sanitized
        raise ErrorSanitizer.create_http_exception(
            e,
            status_code=500,
            user_message="Failed to process invoice",
            log_context={"invoice_id": invoice_id}
        )
```

### Domain-Specific Sanitizers

```python
def sanitize_database_error(e: Exception) -> str:
    return ErrorSanitizer.sanitize_error(
        e,
        user_message="Database operation failed. Please try again.",
        log_context={"error_type": "database"}
    )

def sanitize_api_error(e: Exception, service_name: str = "external service") -> str:
    return ErrorSanitizer.sanitize_error(
        e,
        user_message=f"Failed to communicate with {service_name}.",
        log_context={"error_type": "external_api", "service": service_name}
    )
```

### Batch Operations with Partial Failures

```python
def process_items(items: list[dict]) -> dict:
    failed_items = []
    
    for idx, item in enumerate(items):
        try:
            process_item(item)
        except Exception as e:
            error_type = classify_error(e)
            failed_items.append({
                "line": idx,
                "description": item['description'][:50],  # Truncate
                "error_type": error_type,
                "message": get_user_friendly_message(error_type)
                # NOTE: Don't include str(e) - might be sensitive
            })
    
    return {
        "status": "partial_success" if failed_items else "success",
        "failed_items": failed_items
    }
```

## Best Practices

1. Always log full error details server-side with `exc_info=True`
2. Include correlation IDs (request_id, session_id) in logs for tracing
3. Truncate user input in error messages to prevent log injection
4. Test error handling in production mode - errors look different in dev vs prod
5. Monitor "unknown" error rates - high rates indicate missing classification

## Common Mistakes

- Exposing raw exception messages to users in production
- Forgetting to log the full error before sanitizing
- Including sensitive data in log messages (passwords, connection strings)
- Not testing error responses in production mode
- Trusting that "safe" errors don't contain injected content

## Related Patterns

- exception-taxonomy - Hierarchical exception system with error codes
- circuit-breaker - Prevent cascading failures
- error-handling - General error handling patterns
