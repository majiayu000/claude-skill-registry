---
name: structured-errors
description: Automatically applies when writing error handling in APIs and tools. Ensures errors are returned as structured JSON with error, request_id, and timestamp (not plain strings).
---

# Structured Error Response Enforcer

When writing error handling in API endpoints, tools, or services, always return structured JSON errors.

## ✅ Correct Pattern

```python
import uuid
from datetime import datetime
import json

def create_error_response(
    error_message: str,
    status_code: int = 500,
    details: dict = None
) -> dict:
    """Create structured error response."""
    response = {
        "error": error_message,
        "request_id": str(uuid.uuid4()),
        "timestamp": datetime.now().isoformat(),
        "status_code": status_code
    }
    if details:
        response["details"] = details
    return response

# In API endpoint
@app.get("/users/{user_id}")
async def get_user(user_id: str):
    if not user_id:
        raise HTTPException(
            status_code=400,
            detail=create_error_response(
                "User ID is required",
                status_code=400
            )
        )

    try:
        user = await fetch_user(user_id)
        return user
    except UserNotFoundError:
        raise HTTPException(
            status_code=404,
            detail=create_error_response(
                "User not found",
                status_code=404,
                details={"user_id": user_id}
            )
        )

# In tool function
def process_data(data: str) -> str:
    if not data:
        return json.dumps(create_error_response(
            "Data is required",
            status_code=400
        ))

    try:
        result = parse_data(data)
        return json.dumps({"result": result})
    except Exception as e:
        return json.dumps(create_error_response(
            "Failed to process data",
            status_code=500,
            details={"error_type": type(e).__name__}
        ))
```

## ❌ Incorrect Pattern

```python
# ❌ Plain string
if not user_id:
    return "Error: user ID is required"

# ❌ Exposing sensitive data
except httpx.HTTPStatusError as e:
    return f"Error: {e.response.text}"  # ❌ Leaks API response

# ❌ No request ID for tracing
return {"error": "Something went wrong"}

# ❌ Inconsistent error format
return "Error: failed"  # Sometimes string
return {"message": "failed"}  # Sometimes object
```

## Required Fields

**All error responses must include:**
1. **error** (string) - Human-readable error message
2. **request_id** (uuid) - For tracing/debugging
3. **timestamp** (ISO string) - When error occurred
4. **status_code** (int) - HTTP status code

**Optional but recommended:**
5. **details** (object) - Additional context (safe data only)
6. **error_code** (string) - Application-specific error code
7. **field** (string) - Which field caused the error (validation)

## Custom Exception Classes

```python
class APIError(Exception):
    """Base exception for API errors."""

    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        self.message = message
        self.status_code = status_code
        self.details = details or {}
        self.request_id = str(uuid.uuid4())
        self.timestamp = datetime.now().isoformat()
        super().__init__(self.message)

    def to_dict(self) -> dict:
        """Convert to structured error response."""
        return {
            "error": self.message,
            "status_code": self.status_code,
            "request_id": self.request_id,
            "timestamp": self.timestamp,
            "details": self.details
        }

class ValidationError(APIError):
    """Validation error."""
    def __init__(self, message: str, field: str = None):
        details = {"field": field} if field else {}
        super().__init__(message, status_code=400, details=details)

class NotFoundError(APIError):
    """Resource not found."""
    def __init__(self, resource: str, resource_id: str):
        super().__init__(
            f"{resource} not found",
            status_code=404,
            details={"resource": resource, "id": resource_id}
        )

# Usage
try:
    user = await get_user(user_id)
except UserNotFoundError:
    raise NotFoundError("User", user_id)
```

## FastAPI Integration

```python
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse

app = FastAPI()

@app.exception_handler(APIError)
async def api_error_handler(request: Request, exc: APIError):
    """Global exception handler for APIError."""
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_dict()
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """Catch-all for unexpected errors."""
    error_response = create_error_response(
        "Internal server error",
        status_code=500,
        details={"type": type(exc).__name__}
    )
    # Log full error but don't expose to client
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(status_code=500, content=error_response)
```

## Security Note

**Never include in errors:**
- Raw API response text
- Stack traces (log them, don't return them)
- Internal IDs or tokens
- Database query details
- Full exception messages from external APIs
- Authentication credentials
- File paths or system information

**Safe to include:**
- User-facing error messages
- Validation field names
- Request IDs for support
- Status codes
- Generic error types

## Logging Errors

```python
import logging

logger = logging.getLogger(__name__)

def handle_error(error: Exception, context: dict = None) -> dict:
    """Handle error with proper logging and structured response."""
    request_id = str(uuid.uuid4())

    # Log with context
    logger.error(
        f"Error occurred | request_id={request_id} | "
        f"error={type(error).__name__}",
        extra=context,
        exc_info=True
    )

    # Return safe error response
    return create_error_response(
        "An error occurred processing your request",
        status_code=500,
        details={"request_id": request_id}
    )
```

## ❌ Anti-Patterns

```python
# ❌ Leaking internal errors
return {"error": str(exception)}

# ❌ Inconsistent format across endpoints
def endpoint1(): return "Error"
def endpoint2(): return {"error": "Error"}

# ❌ No context for debugging
return {"error": "Failed"}

# ❌ Returning 200 with error in body
return {"success": False, "error": "..."}  # Should use proper status code

# ❌ Too much information
return {
    "error": f"Database query failed: {full_sql_query}",
    "stacktrace": traceback.format_exc()
}
```

## Best Practices Checklist

- ✅ Use consistent error structure across application
- ✅ Include request_id for tracing
- ✅ Include timestamp for debugging
- ✅ Use proper HTTP status codes
- ✅ Create custom exception classes for common errors
- ✅ Add global exception handlers
- ✅ Log full error details (with context)
- ✅ Return safe, user-friendly messages
- ✅ Never expose sensitive data in errors
- ✅ Document error responses in API docs

## Auto-Apply

When you write error handling:
1. Create helper `create_error_response()`
2. Use it for all error returns
3. Include request_id and timestamp
4. Remove any sensitive data
5. Use proper status codes

## Related Skills

- docstring-format - Document Raises section
- pii-redaction - Redact PII in error logs
- pydantic-models - For error response models
