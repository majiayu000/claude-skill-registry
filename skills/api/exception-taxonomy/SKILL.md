---
name: exception-taxonomy
description: Hierarchical exception system with HTTP status codes, machine-readable error codes, and structured responses for consistent API error handling across all endpoints.
license: MIT
compatibility: TypeScript/JavaScript, Python
metadata:
  category: errors
  time: 3h
  source: drift-masterguide
---

# Exception Taxonomy

Hierarchical exception system with HTTP status codes, error codes, and structured responses for consistent API error handling.

## When to Use This Skill

- Building APIs that need consistent error responses
- Creating machine-readable error codes for client handling
- Implementing retry logic based on error types
- Standardizing error handling across a large codebase

## Core Concepts

A well-designed exception taxonomy provides:
- Consistent error responses across all endpoints
- Machine-readable error codes for client handling
- Human-readable messages for debugging
- HTTP status code mapping
- Retry hints for transient failures

The hierarchy typically follows:
```
BaseAppError (abstract)
├── AuthenticationError (401)
├── AuthorizationError (403)
├── ResourceError (404/409)
├── ValidationError (422)
├── RateLimitError (429)
├── ExternalServiceError (502/503)
└── PaymentError (402)
```

## Implementation

### Python

```python
from dataclasses import dataclass, field
from typing import Optional, Dict, Any
from enum import Enum


class ErrorCode(str, Enum):
    """Standardized error codes for API responses."""
    # Authentication
    AUTH_INVALID_CREDENTIALS = "AUTH_INVALID_CREDENTIALS"
    AUTH_TOKEN_EXPIRED = "AUTH_TOKEN_EXPIRED"
    AUTH_TOKEN_INVALID = "AUTH_TOKEN_INVALID"
    AUTH_EMAIL_EXISTS = "AUTH_EMAIL_EXISTS"
    
    # Authorization
    FORBIDDEN = "FORBIDDEN"
    
    # Resources
    RESOURCE_NOT_FOUND = "RESOURCE_NOT_FOUND"
    RESOURCE_CONFLICT = "RESOURCE_CONFLICT"
    
    # Rate Limiting
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"
    
    # External Services
    GENERATION_FAILED = "GENERATION_FAILED"
    GENERATION_TIMEOUT = "GENERATION_TIMEOUT"
    
    # Validation
    VALIDATION_ERROR = "VALIDATION_ERROR"
    INVALID_STATE_TRANSITION = "INVALID_STATE_TRANSITION"


@dataclass
class BaseAppError(Exception):
    """Base exception for all application errors."""
    message: str
    code: ErrorCode
    status_code: int = 500
    details: Optional[Dict[str, Any]] = field(default_factory=dict)
    retry_after: Optional[int] = None
    
    def __post_init__(self):
        super().__init__(self.message)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to API response format."""
        error_dict = {
            "error": {
                "message": self.message,
                "code": self.code.value,
            }
        }
        if self.details:
            error_dict["error"]["details"] = self.details
        if self.retry_after is not None:
            error_dict["error"]["retry_after"] = self.retry_after
        return error_dict


@dataclass
class NotFoundError(BaseAppError):
    """Resource not found error."""
    resource_type: str = "resource"
    resource_id: str = ""
    message: str = field(init=False)
    code: ErrorCode = field(default=ErrorCode.RESOURCE_NOT_FOUND)
    status_code: int = 404
    
    def __post_init__(self):
        self.message = f"{self.resource_type.title()} not found"
        self.details = {
            "resource_type": self.resource_type,
            "resource_id": self.resource_id,
        }
        super().__post_init__()


@dataclass
class RateLimitError(BaseAppError):
    """Rate limit exceeded error."""
    retry_after: int = 60
    message: str = "Rate limit exceeded"
    code: ErrorCode = field(default=ErrorCode.RATE_LIMIT_EXCEEDED)
    status_code: int = 429
    
    def __post_init__(self):
        self.details = {"retry_after": self.retry_after}
        super().__post_init__()


@dataclass
class InvalidStateTransitionError(BaseAppError):
    """Invalid state transition error."""
    current_status: str = ""
    target_status: str = ""
    message: str = field(init=False)
    code: ErrorCode = field(default=ErrorCode.INVALID_STATE_TRANSITION)
    status_code: int = 409
    
    def __post_init__(self):
        self.message = f"Cannot transition from '{self.current_status}' to '{self.target_status}'"
        self.details = {
            "current_status": self.current_status,
            "target_status": self.target_status,
        }
        super().__post_init__()
```

### TypeScript

```typescript
export enum ErrorCode {
  AUTH_INVALID_CREDENTIALS = 'AUTH_INVALID_CREDENTIALS',
  AUTH_TOKEN_EXPIRED = 'AUTH_TOKEN_EXPIRED',
  AUTH_TOKEN_INVALID = 'AUTH_TOKEN_INVALID',
  FORBIDDEN = 'FORBIDDEN',
  RESOURCE_NOT_FOUND = 'RESOURCE_NOT_FOUND',
  RESOURCE_CONFLICT = 'RESOURCE_CONFLICT',
  RATE_LIMIT_EXCEEDED = 'RATE_LIMIT_EXCEEDED',
  VALIDATION_ERROR = 'VALIDATION_ERROR',
  INVALID_STATE_TRANSITION = 'INVALID_STATE_TRANSITION',
}

interface ErrorDetails {
  [key: string]: unknown;
}

export class BaseAppError extends Error {
  constructor(
    public readonly message: string,
    public readonly code: ErrorCode,
    public readonly statusCode: number = 500,
    public readonly details: ErrorDetails = {},
    public readonly retryAfter?: number
  ) {
    super(message);
    this.name = this.constructor.name;
  }

  toJSON() {
    const error: Record<string, unknown> = {
      message: this.message,
      code: this.code,
    };
    if (Object.keys(this.details).length > 0) {
      error.details = this.details;
    }
    if (this.retryAfter !== undefined) {
      error.retry_after = this.retryAfter;
    }
    return { error };
  }
}

export class NotFoundError extends BaseAppError {
  constructor(resourceType: string, resourceId: string) {
    super(
      `${resourceType.charAt(0).toUpperCase() + resourceType.slice(1)} not found`,
      ErrorCode.RESOURCE_NOT_FOUND,
      404,
      { resource_type: resourceType, resource_id: resourceId }
    );
  }
}

export class RateLimitError extends BaseAppError {
  constructor(retryAfter: number = 60) {
    super(
      'Rate limit exceeded',
      ErrorCode.RATE_LIMIT_EXCEEDED,
      429,
      { retry_after: retryAfter },
      retryAfter
    );
  }
}

export class InvalidStateTransitionError extends BaseAppError {
  constructor(currentStatus: string, targetStatus: string) {
    super(
      `Cannot transition from '${currentStatus}' to '${targetStatus}'`,
      ErrorCode.INVALID_STATE_TRANSITION,
      409,
      { current_status: currentStatus, target_status: targetStatus }
    );
  }
}
```

## Usage Examples

### FastAPI Exception Handlers

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(BaseAppError)
async def app_error_handler(request: Request, exc: BaseAppError) -> JSONResponse:
    headers = {"Retry-After": str(exc.retry_after)} if exc.retry_after else None
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict(),
        headers=headers,
    )

@app.exception_handler(Exception)
async def generic_error_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.exception(f"Unexpected error: {exc}")
    return JSONResponse(
        status_code=500,
        content={"error": {"message": "An unexpected error occurred", "code": "INTERNAL_ERROR"}},
    )
```

### Route Usage

```python
@router.get("/jobs/{job_id}")
async def get_job(job_id: str, user_id: str = Depends(get_current_user)):
    job = await job_service.get(job_id)
    
    if not job:
        raise NotFoundError(resource_type="job", resource_id=job_id)
    
    if job.user_id != user_id:
        raise AuthorizationError(resource_type="job")
    
    return job
```

### Client-Side Handling (TypeScript)

```typescript
interface APIError {
  error: {
    message: string;
    code: string;
    details?: Record<string, unknown>;
    retry_after?: number;
  };
}

function handleAPIError(error: APIError): void {
  switch (error.error.code) {
    case 'AUTH_TOKEN_EXPIRED':
      authStore.refreshToken();
      break;
    case 'RATE_LIMIT_EXCEEDED':
      const retryAfter = error.error.retry_after || 60;
      toast.error(`Rate limited. Try again in ${retryAfter}s`);
      break;
    default:
      toast.error(error.error.message);
  }
}
```

## Best Practices

1. Use specific exceptions - Create domain-specific exceptions rather than generic ones
2. Include context - Always include relevant IDs and state in error details
3. Map to HTTP codes - Each exception should have a clear HTTP status code
4. Provide retry hints - For transient failures, include `retry_after`
5. Use error codes - Machine-readable codes enable client-side handling logic
6. Log appropriately - Log full details server-side, return safe messages to clients

## Common Mistakes

- Using generic exceptions instead of domain-specific ones
- Forgetting to include resource IDs in error details
- Not providing retry hints for rate limit errors
- Exposing internal error details in production responses
- Inconsistent error response formats across endpoints

## Related Patterns

- error-sanitization - Sanitize errors before returning to users
- error-handling - General error handling patterns
- rate-limiting - Rate limiting implementation
