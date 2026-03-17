---
name: fastapi-code-review
description: Reviews FastAPI code for routing patterns, dependency injection, validation, and async handlers. Use when reviewing FastAPI apps, checking APIRouter setup, Depends() usage, or response models.
---

# FastAPI Code Review

## Quick Reference

| Issue Type | Reference |
|------------|-----------|
| APIRouter setup, response_model, status codes | [references/routes.md](references/routes.md) |
| Depends(), yield deps, cleanup, shared deps | [references/dependencies.md](references/dependencies.md) |
| Pydantic models, HTTPException, 422 handling | [references/validation.md](references/validation.md) |
| Async handlers, blocking I/O, background tasks | [references/async.md](references/async.md) |

## Review Checklist

- [ ] APIRouter with proper prefix and tags
- [ ] All routes specify `response_model` for type safety
- [ ] Correct HTTP methods (GET, POST, PUT, DELETE, PATCH)
- [ ] Proper status codes (200, 201, 204, 404, etc.)
- [ ] Dependencies use `Depends()` not manual calls
- [ ] Yield dependencies have proper cleanup
- [ ] Request/Response models use Pydantic
- [ ] HTTPException with status code and detail
- [ ] All route handlers are `async def`
- [ ] No blocking I/O (`requests`, `time.sleep`, `open()`)
- [ ] Background tasks for non-blocking operations
- [ ] No bare `except` in route handlers

## Valid Patterns (Do NOT Flag)

These are idiomatic FastAPI patterns that may appear problematic but are correct:

- **Pydantic validates request body automatically** - No manual validation needed when using typed Pydantic models as parameters
- **Dependency injection for database sessions** - Sessions come from `Depends()`, not passed as function arguments
- **HTTPException for all HTTP errors** - FastAPI handles conversion to proper HTTP responses
- **Async def endpoint without await** - May be using sync dependencies or simple operations; FastAPI handles this
- **Type annotation on Depends()** - This is documentation/IDE support, not a type assertion
- **Query/Path/Body defaults** - FastAPI processes these at runtime, not traditional Python defaults
- **Returning dict from endpoint** - Pydantic converts automatically if `response_model` is set

## Context-Sensitive Rules

Only flag issues when the context warrants it:

- **Flag missing validation** ONLY IF the field isn't already in a Pydantic model with validators
- **Flag missing auth** ONLY IF the endpoint isn't using `Depends()` with an auth dependency
- **Flag missing error handling** ONLY IF HTTPException isn't raised appropriately for error cases
- **Flag sync in async** ONLY IF the operation is actually blocking (file I/O, network calls, CPU-bound), not just non-async

## FastAPI Framework Behaviors

FastAPI + Pydantic handle many concerns automatically:
- Request validation via Pydantic models
- Response serialization via response_model
- Dependency injection for cross-cutting concerns
- Exception handling via exception handlers

Before flagging "missing" functionality, verify FastAPI isn't handling it.

## When to Load References

- Reviewing route definitions → routes.md
- Reviewing dependency injection → dependencies.md
- Reviewing Pydantic models/validation → validation.md
- Reviewing async route handlers → async.md

## Review Questions

1. Do all routes have explicit response models and status codes?
2. Are dependencies injected via Depends() with proper cleanup?
3. Do all Pydantic models validate inputs correctly?
4. Are all route handlers async and non-blocking?

## Before Submitting Findings

Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) before reporting any issue.
