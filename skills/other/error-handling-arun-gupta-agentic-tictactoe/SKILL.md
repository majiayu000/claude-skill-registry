---
name: error-handling
description: Defines error handling patterns using custom error codes, result wrappers, and HTTP status code mapping. Use when implementing error handling in services, business logic, or API endpoints to ensure consistent error responses.
license: MIT
metadata:
  version: "1.0.0"
  error_system: "custom error codes, result wrappers, HTTP mapping"
---

# Error Handling Pattern

This skill defines how to handle errors consistently across the codebase.

## Error Code System

### Error Code Definition

Define error codes in a central location (e.g., `errors.py` or constants module):

```python
# Validation Errors
E_INVALID_INPUT = "E_INVALID_INPUT"
E_OUT_OF_BOUNDS = "E_OUT_OF_BOUNDS"
E_MISSING_REQUIRED_FIELD = "E_MISSING_REQUIRED_FIELD"

# Resource Errors
E_RESOURCE_NOT_FOUND = "E_RESOURCE_NOT_FOUND"
E_RESOURCE_CONFLICT = "E_RESOURCE_CONFLICT"
E_RESOURCE_LOCKED = "E_RESOURCE_LOCKED"

# Service Errors
E_SERVICE_TIMEOUT = "E_SERVICE_TIMEOUT"
E_SERVICE_UNAVAILABLE = "E_SERVICE_UNAVAILABLE"
E_EXTERNAL_SERVICE_ERROR = "E_EXTERNAL_SERVICE_ERROR"

# API Errors
E_INVALID_REQUEST = "E_INVALID_REQUEST"
E_INTERNAL_ERROR = "E_INTERNAL_ERROR"
E_SERVICE_NOT_READY = "E_SERVICE_NOT_READY"
```

### Using Error Codes

```python
from errors import E_OUT_OF_BOUNDS

if not (0 <= value <= max_value):
    raise ValueError(
        f"Value {value} is out of bounds (0-{max_value}). "
        f"Error code: {E_OUT_OF_BOUNDS}"
    )
```

## Result Wrapper Pattern

### Result Wrapper Structure

For operations that can fail, use a result wrapper:

```python
from typing import Generic, TypeVar

T = TypeVar("T")

class Result(Generic[T]):
    """Generic result wrapper for operations that can fail."""
    success: bool
    data: T | None = None
    error_code: str | None = None
    error_message: str | None = None
    metadata: dict | None = None

    @classmethod
    def success_result(cls, data: T) -> "Result[T]":
        """Create successful result."""
        return cls(success=True, data=data)

    @classmethod
    def error_result(
        cls, error_code: str, error_message: str, metadata: dict | None = None
    ) -> "Result[T]":
        """Create error result."""
        return cls(
            success=False,
            error_code=error_code,
            error_message=error_message,
            metadata=metadata
        )
```

### Result Wrapper Usage

```python
def process_data(input_data: InputData) -> Result[OutputData]:
    """Process data with error handling."""
    try:
        output = perform_processing(input_data)
        return Result.success_result(data=output)
    except TimeoutError as e:
        return Result.error_result(
            error_code="E_SERVICE_TIMEOUT",
            error_message=f"Processing exceeded timeout: {e}",
            metadata={"timeout_seconds": 10}
        )
    except Exception as e:
        return Result.error_result(
            error_code="E_INTERNAL_ERROR",
            error_message=f"Processing failed: {e}"
        )
```

### Checking Result

```python
result = service.process(data)

if result.success:
    output = result.data  # Type-safe access
    # Use output
else:
    error_code = result.error_code
    error_message = result.error_message
    # Handle error
```

## API Error Responses

### Standard Error Response Format

Use a consistent error response format:

```python
from fastapi.responses import JSONResponse
from fastapi import status
from datetime import UTC, datetime

def error_response(
    error_code: str,
    message: str,
    status_code: int = 400,
    details: dict | None = None
) -> JSONResponse:
    """Create standard error response."""
    return JSONResponse(
        status_code=status_code,
        content={
            "status": "failure",
            "error_code": error_code,
            "message": message,
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "details": details
        }
    )
```

### HTTP Status Code Mapping

Map error codes to appropriate HTTP status codes:

| Error Code | HTTP Status | Use Case |
|------------|-------------|----------|
| `E_INVALID_REQUEST` | 400 Bad Request | Invalid request format or validation failure |
| `E_OUT_OF_BOUNDS` | 400 Bad Request | Invalid input values |
| `E_RESOURCE_NOT_FOUND` | 404 Not Found | Resource doesn't exist |
| `E_RESOURCE_CONFLICT` | 409 Conflict | Resource already exists or state conflict |
| `E_UNAUTHORIZED` | 401 Unauthorized | Authentication required |
| `E_FORBIDDEN` | 403 Forbidden | Insufficient permissions |
| `E_SERVICE_NOT_READY` | 503 Service Unavailable | Service dependencies not ready |
| `E_SERVICE_TIMEOUT` | 504 Gateway Timeout | Service timeout |
| `E_INTERNAL_ERROR` | 500 Internal Server Error | Unexpected server error |

### Exception Handlers

Register exception handlers in FastAPI app:

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi import status

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError) -> JSONResponse:
    """Handle ValueError exceptions."""
    # Extract error code from message if present
    error_code = "E_INVALID_REQUEST"
    if "Error code:" in str(exc):
        error_code = str(exc).split("Error code:")[-1].strip()

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "status": "failure",
            "error_code": error_code,
            "message": str(exc),
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "details": None
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handle unexpected exceptions."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "status": "failure",
            "error_code": "E_INTERNAL_ERROR",
            "message": "Internal server error",
            "timestamp": datetime.now(UTC).isoformat().replace("+00:00", "Z"),
            "details": None
        }
    )
```

## Service Error Handling

### Input Validation Errors

```python
def validate_input(self, data: InputData) -> None:
    """Validate input and raise ValueError with error code."""
    # Bounds check
    if not (min_value <= data.value <= max_value):
        raise ValueError(
            f"Value {data.value} is out of bounds ({min_value}-{max_value}). "
            f"Error code: {E_OUT_OF_BOUNDS}"
        )

    # Required field check
    if not data.required_field:
        raise ValueError(
            f"Required field 'required_field' is missing. "
            f"Error code: {E_MISSING_REQUIRED_FIELD}"
        )

    # State check
    if data.status != "ACTIVE":
        raise ValueError(
            f"Resource is not in active state (status: {data.status}). "
            f"Error code: {E_RESOURCE_CONFLICT}"
        )
```

### Error Propagation

```python
def process_data(self, data: InputData) -> Result[OutputData]:
    """Process data, handling errors."""
    try:
        self.validate_input(data)
        # Process data
        output = perform_processing(data)
        return Result.success_result(data=output)
    except ValueError as e:
        # Extract error code from exception message
        error_code = extract_error_code(str(e))
        return Result.error_result(
            error_code=error_code,
            error_message=str(e)
        )
```

## Service Error Handling

### Timeout Handling

```python
def execute_with_timeout(self, func, timeout: float) -> Result[T]:
    """Execute function with timeout."""
    try:
        with ThreadPoolExecutor() as executor:
            future = executor.submit(func)
            result = future.result(timeout=timeout)
            return Result.success_result(data=result)
    except TimeoutError:
        return Result.error_result(
            error_code="E_SERVICE_TIMEOUT",
            error_message=f"Operation exceeded timeout of {timeout}s",
            metadata={"timeout_seconds": timeout}
        )
```

### Fallback Strategies

```python
def execute_pipeline(self, input_data: InputData) -> Result[OutputData]:
    """Execute service pipeline with fallbacks."""
    # Try primary service
    primary_result = self.primary_service.process(input_data)
    if not primary_result.success:
        # Fallback to secondary service
        return self._fallback_secondary_service(input_data)

    # Continue pipeline...
```

## Testing Error Handling

### Testing Error Codes

```python
def test_returns_correct_error_code(self) -> None:
    """Test returns correct error code."""
    result = component.operation(invalid_input)

    assert result.success is False
    assert result.error_code == "E_ERROR_CODE"
    assert result.error_message is not None
```

### Testing HTTP Error Responses

```python
def test_endpoint_returns_correct_error_status(self, client: TestClient) -> None:
    """Test endpoint returns correct HTTP status for error."""
    response = client.post("/endpoint", json={"invalid": "data"})

    assert response.status_code == 400
    data = response.json()
    assert data["status"] == "failure"
    assert data["error_code"] == "E_INVALID_REQUEST"
    assert "timestamp" in data
```

### Testing Error Message Format

```python
def test_error_message_includes_error_code(self) -> None:
    """Test error message includes error code."""
    try:
        component.operation(invalid_input)
    except ValueError as e:
        assert "Error code: E_ERROR_CODE" in str(e)
```

## Best Practices

1. **Use error codes**: Always include error codes in error messages
2. **Consistent format**: Follow established error response formats
3. **Log errors**: Log unexpected errors with full context
4. **Type safety**: Use `AgentResult` for type-safe error handling
5. **Map to HTTP**: Map error codes to appropriate HTTP status codes
6. **User-friendly messages**: Provide clear, actionable error messages
7. **Include context**: Add metadata for debugging when appropriate

## Error Code Naming

### Convention

- Prefix: `E_` (Error)
- Format: `E_<CATEGORY>_<DESCRIPTION>`
- Uppercase with underscores

### Categories

- `INVALID_*`: Validation errors
- `RESOURCE_*`: Resource-related errors
- `SERVICE_*`: Service availability/timeout errors
- `AUTH_*`: Authentication/authorization errors
- `EXTERNAL_*`: External service errors
- `INTERNAL_*`: Unexpected errors

## Common Patterns

### Error Aggregation

```python
def validate_multiple_things(self) -> list[str]:
    """Validate multiple things and return all errors."""
    errors = []

    if not condition1:
        errors.append("E_ERROR_1")
    if not condition2:
        errors.append("E_ERROR_2")

    return errors
```

### Error with Details

```python
AgentResult.error(
    error_code="E_VALIDATION_ERROR",
    error_message="Validation failed",
    metadata={
        "field": "row",
        "expected": "0-2",
        "actual": 5
    }
)
```
