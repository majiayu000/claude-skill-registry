---
name: error-handling-rfc9457
description: RFC 9457 Problem Details for standardized HTTP API error responses. Use when implementing problem details format, structured API errors, error registries, or migrating from RFC 7807.
context: fork
agent: backend-system-architect
version: 1.0.0
tags: [error-handling, rfc9457, problem-details, fastapi, api, 2026]
author: SkillForge
user-invocable: false
---

# RFC 9457 Problem Details

Standardize API error responses with machine-readable problem details.

## RFC 9457 vs RFC 7807

| Feature | RFC 7807 (Old) | RFC 9457 (Current) |
|---------|----------------|---------------------|
| Status | Obsolete | Active Standard |
| Multiple problems | Not specified | Explicitly supported |
| Error registry | No | Yes (IANA registry) |
| Extension fields | Implicit | Explicitly allowed |

## Problem Details Schema

```python
from pydantic import BaseModel, Field, HttpUrl
from typing import Any

class ProblemDetail(BaseModel):
    """RFC 9457 Problem Details for HTTP APIs."""

    type: HttpUrl = Field(
        default="about:blank",
        description="URI identifying the problem type"
    )
    title: str = Field(
        description="Short, human-readable summary"
    )
    status: int = Field(
        ge=400, le=599,
        description="HTTP status code"
    )
    detail: str | None = Field(
        default=None,
        description="Human-readable explanation specific to this occurrence"
    )
    instance: str | None = Field(
        default=None,
        description="URI reference identifying the specific occurrence"
    )

    model_config = {"extra": "allow"}  # Allow extension fields
```

## FastAPI Integration

### Exception Classes

```python
from fastapi import HTTPException
from typing import Any

class ProblemException(HTTPException):
    """Base exception for RFC 9457 problem details."""

    def __init__(
        self,
        status_code: int,
        problem_type: str,
        title: str,
        detail: str | None = None,
        instance: str | None = None,
        **extensions: Any,
    ):
        self.problem_type = problem_type
        self.title = title
        self.detail = detail
        self.instance = instance
        self.extensions = extensions
        super().__init__(status_code=status_code, detail=detail)

    def to_problem_detail(self) -> dict[str, Any]:
        result = {
            "type": self.problem_type,
            "title": self.title,
            "status": self.status_code,
        }
        if self.detail:
            result["detail"] = self.detail
        if self.instance:
            result["instance"] = self.instance
        result.update(self.extensions)
        return result
```

### Specific Problem Types

```python
class ValidationProblem(ProblemException):
    def __init__(self, errors: list[dict], instance: str | None = None):
        super().__init__(
            status_code=422,
            problem_type="https://api.example.com/problems/validation-error",
            title="Validation Error",
            detail="One or more fields failed validation",
            instance=instance,
            errors=errors,  # Extension field
        )

class NotFoundProblem(ProblemException):
    def __init__(self, resource: str, resource_id: str, instance: str | None = None):
        super().__init__(
            status_code=404,
            problem_type="https://api.example.com/problems/resource-not-found",
            title="Resource Not Found",
            detail=f"{resource} with ID '{resource_id}' was not found",
            instance=instance,
            resource=resource,
            resource_id=resource_id,
        )

class RateLimitProblem(ProblemException):
    def __init__(self, retry_after: int, instance: str | None = None):
        super().__init__(
            status_code=429,
            problem_type="https://api.example.com/problems/rate-limit-exceeded",
            title="Too Many Requests",
            detail="Rate limit exceeded. Please retry later.",
            instance=instance,
            retry_after=retry_after,
        )
```

### Exception Handler

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

app = FastAPI()

@app.exception_handler(ProblemException)
async def problem_exception_handler(request: Request, exc: ProblemException):
    return JSONResponse(
        status_code=exc.status_code,
        content=exc.to_problem_detail(),
        media_type="application/problem+json",
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = [
        {"field": ".".join(str(loc) for loc in err["loc"]), "message": err["msg"]}
        for err in exc.errors()
    ]
    problem = ValidationProblem(errors=errors, instance=str(request.url))
    return JSONResponse(
        status_code=422,
        content=problem.to_problem_detail(),
        media_type="application/problem+json",
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={
            "type": "https://api.example.com/problems/internal-error",
            "title": "Internal Server Error",
            "status": 500,
            "detail": "An unexpected error occurred",
            "instance": str(request.url),
        },
        media_type="application/problem+json",
    )
```

## Usage in Endpoints

```python
@router.get("/api/v1/analyses/{analysis_id}")
async def get_analysis(
    analysis_id: str,
    request: Request,
    service: AnalysisService = Depends(get_analysis_service),
):
    analysis = await service.get_by_id(analysis_id)
    if not analysis:
        raise NotFoundProblem(
            resource="Analysis",
            resource_id=analysis_id,
            instance=str(request.url),
        )
    return analysis
```

## Response Examples

### 404 Not Found

```json
{
  "type": "https://api.example.com/problems/resource-not-found",
  "title": "Resource Not Found",
  "status": 404,
  "detail": "Analysis with ID 'abc123' was not found",
  "instance": "/api/v1/analyses/abc123",
  "resource": "Analysis",
  "resource_id": "abc123"
}
```

### 422 Validation Error

```json
{
  "type": "https://api.example.com/problems/validation-error",
  "title": "Validation Error",
  "status": 422,
  "detail": "One or more fields failed validation",
  "instance": "/api/v1/analyses",
  "errors": [
    {"field": "source_url", "message": "Invalid URL format"},
    {"field": "depth", "message": "Must be between 1 and 3"}
  ]
}
```

### 429 Rate Limited

```json
{
  "type": "https://api.example.com/problems/rate-limit-exceeded",
  "title": "Too Many Requests",
  "status": 429,
  "detail": "Rate limit exceeded. Please retry later.",
  "instance": "/api/v1/analyses",
  "retry_after": 60
}
```

## Error Type Registry

```python
# app/core/problem_types.py
PROBLEM_TYPES = {
    "validation-error": {
        "uri": "https://api.example.com/problems/validation-error",
        "title": "Validation Error",
        "status": 422,
    },
    "resource-not-found": {
        "uri": "https://api.example.com/problems/resource-not-found",
        "title": "Resource Not Found",
        "status": 404,
    },
    "rate-limit-exceeded": {
        "uri": "https://api.example.com/problems/rate-limit-exceeded",
        "title": "Too Many Requests",
        "status": 429,
    },
    "unauthorized": {
        "uri": "https://api.example.com/problems/unauthorized",
        "title": "Unauthorized",
        "status": 401,
    },
    "forbidden": {
        "uri": "https://api.example.com/problems/forbidden",
        "title": "Forbidden",
        "status": 403,
    },
    "conflict": {
        "uri": "https://api.example.com/problems/conflict",
        "title": "Conflict",
        "status": 409,
    },
    "internal-error": {
        "uri": "https://api.example.com/problems/internal-error",
        "title": "Internal Server Error",
        "status": 500,
    },
}
```

## Anti-Patterns (FORBIDDEN)

```python
# NEVER return plain text errors
return Response("Not found", status_code=404)

# NEVER use inconsistent error formats
return {"error": "Not found"}  # Different from other errors
return {"message": "Validation failed", "errors": [...]}

# NEVER expose internal details in production
return {"detail": str(exc), "traceback": traceback.format_exc()}

# NEVER use generic 500 for everything
except Exception:
    raise HTTPException(500, "Something went wrong")
```

## Key Decisions

| Decision | Recommendation |
|----------|----------------|
| Media type | `application/problem+json` |
| Type URI | Use your API domain + `/problems/` |
| Detail | Include only for user-actionable info |
| Extensions | Use for machine-readable context |
| Logging | Log problem types for monitoring |

## Related Skills

- `api-design-framework` - REST API patterns
- `observability-monitoring` - Error tracking
- `input-validation` - Validation patterns

## Capability Details

### problem-details
**Keywords:** problem details, RFC 9457, RFC 7807, structured error
**Solves:**
- How to standardize API error responses?
- What format for API errors?

### fastapi-errors
**Keywords:** fastapi exception, error handler, HTTPException
**Solves:**
- How to handle errors in FastAPI?
- Custom exception handlers

### error-registry
**Keywords:** error registry, problem types, error catalog
**Solves:**
- How to document all API errors?
- Error type management
