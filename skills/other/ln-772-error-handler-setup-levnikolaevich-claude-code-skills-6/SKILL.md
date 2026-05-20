---
name: ln-772-error-handler-setup
description: Configures global exception handling middleware
---

# ln-772-error-handler-setup

**Type:** L3 Worker
**Category:** 7XX Project Bootstrap
**Parent:** ln-770-crosscutting-setup

Configures global error handling for .NET and Python backend applications.

---

## Overview

| Aspect | Details |
|--------|---------|
| **Input** | Context Store from ln-770 |
| **Output** | Exception handling middleware and custom exceptions |
| **Stacks** | .NET (ASP.NET Core Middleware), Python (FastAPI exception handlers) |

---

## Phase 1: Receive Context

Accept Context Store from coordinator.

**Required Context:**
- `STACK`: .NET or Python
- `FRAMEWORK`: ASP.NET Core or FastAPI
- `PROJECT_ROOT`: Project directory path
- `ENVIRONMENT`: Development or Production

**Idempotency Check:**
- .NET: Grep for `GlobalExceptionMiddleware` or `UseExceptionHandler`
- Python: Grep for `@app.exception_handler` or `exception_handlers.py`
- If found: Return `{ "status": "skipped" }`

---

## Phase 2: Research Error Handling Patterns

Use MCP tools to get up-to-date documentation.

**For .NET:**
```
MCP ref: "ASP.NET Core global exception handling middleware"
Context7: /dotnet/aspnetcore
```

**For Python:**
```
MCP ref: "FastAPI exception handlers custom exceptions"
Context7: /tiangolo/fastapi
```

**Key Patterns to Research:**
1. Middleware pipeline positioning
2. Exception type mapping to HTTP status codes
3. ProblemDetails (RFC 7807) format
4. Development vs Production error details
5. Logging integration

---

## Phase 3: Decision Points

### Q1: Error Response Format

| Option | Description |
|--------|-------------|
| **ProblemDetails (RFC 7807)** (Recommended) | Standardized format, widely adopted |
| **Custom Format** | Project-specific requirements |

### Q2: Error Detail Level

| Environment | Stack Trace | Inner Exceptions | Request Details |
|-------------|-------------|------------------|-----------------|
| Development | ✓ Show | ✓ Show | ✓ Show |
| Production | ✗ Hide | ✗ Hide | ✗ Hide |

### Q3: Error Taxonomy

Define standard error codes:

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `VALIDATION_ERROR` | 400 | Invalid input data |
| `UNAUTHORIZED` | 401 | Authentication required |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `CONFLICT` | 409 | Resource state conflict |
| `INTERNAL_ERROR` | 500 | Unexpected server error |

---

## Phase 4: Generate Configuration

### .NET Output Files

| File | Purpose |
|------|---------|
| `Middleware/GlobalExceptionMiddleware.cs` | Exception handling middleware |
| `Exceptions/AppException.cs` | Base exception class |
| `Exceptions/ValidationException.cs` | Validation errors |
| `Exceptions/NotFoundException.cs` | Not found errors |
| `Models/ErrorResponse.cs` | Error response model |

**Generation Process:**
1. Use MCP ref to get current ASP.NET Core exception handling patterns
2. Generate GlobalExceptionMiddleware with:
   - Exception type to HTTP status mapping
   - Logging of exceptions
   - ProblemDetails response format
   - Environment-aware detail level
3. Generate custom exception classes

**Registration Code:**
```csharp
app.UseMiddleware<GlobalExceptionMiddleware>();
```

### Python Output Files

| File | Purpose |
|------|---------|
| `exceptions/app_exceptions.py` | Custom exception classes |
| `exceptions/handlers.py` | FastAPI exception handlers |
| `models/error_response.py` | Pydantic error models |

**Generation Process:**
1. Use MCP ref to get current FastAPI exception handling patterns
2. Generate exception handlers with:
   - HTTPException handling
   - Custom AppException handling
   - Validation error handling
   - Request validation error handling
3. Generate custom exception classes

**Registration Code:**
```python
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
```

---

## Phase 5: Validate

**Validation Steps:**

1. **Syntax check:**
   - .NET: `dotnet build --no-restore`
   - Python: `python -m py_compile exceptions/handlers.py`

2. **Test error handling:**
   - Create test endpoint that throws exception
   - Verify error response format
   - Check that stack trace hidden in Production

**Expected Error Response (ProblemDetails):**
```json
{
  "type": "https://tools.ietf.org/html/rfc7231#section-6.5.1",
  "title": "Validation Error",
  "status": 400,
  "detail": "Invalid input data",
  "instance": "/api/users",
  "errors": [
    { "field": "email", "message": "Invalid email format" }
  ],
  "traceId": "abc-123-def-456"
}
```

---

## Return to Coordinator

```json
{
  "status": "success",
  "files_created": [
    "Middleware/GlobalExceptionMiddleware.cs",
    "Exceptions/AppException.cs",
    "Models/ErrorResponse.cs"
  ],
  "packages_added": [],
  "registration_code": "app.UseMiddleware<GlobalExceptionMiddleware>();",
  "message": "Configured global exception handling"
}
```

---

## Reference Links

- [ASP.NET Core Error Handling](https://learn.microsoft.com/aspnet/core/web-api/handle-errors)
- [FastAPI Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/)
- [RFC 7807 Problem Details](https://tools.ietf.org/html/rfc7807)

---

## Critical Rules

- **Use ProblemDetails (RFC 7807) by default** — standardized error response format
- **Hide stack traces in Production** — environment-aware detail level is mandatory
- **Use MCP ref for current patterns** — do not hardcode middleware from memory
- **Idempotent** — if `GlobalExceptionMiddleware` or `exception_handlers.py` exists, return `status: "skipped"`
- **Map all custom exceptions to HTTP status codes** — no unhandled exception types reaching the client

## Definition of Done

- Context Store received (stack, framework, environment)
- Error handling patterns researched via MCP tools
- GlobalExceptionMiddleware generated (.NET) or exception handlers generated (Python)
- Custom exception classes created (AppException, ValidationException, NotFoundException)
- Error response model created (ProblemDetails format)
- Syntax validated (`dotnet build` or `py_compile`)
- Structured JSON response returned to ln-770 coordinator

---

**Version:** 2.0.0
**Last Updated:** 2026-01-10
