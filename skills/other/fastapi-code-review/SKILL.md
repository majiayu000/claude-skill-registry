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

## Gates (FastAPI-specific)

Run **once per FastAPI-related finding**, after you can anchor **`file:line`** for the handler (see [review-verification-protocol](../review-verification-protocol/SKILL.md)) and **before** the finding text ships. If a step’s pass condition is not met, **do not** assert the finding as written—gather evidence, withdraw, downgrade severity, or rephrase as a question.

### Gate 1 — Route decorator and response surface

| Step | Action | **Pass condition** |
|------|--------|---------------------|
| 1a | Open the handler’s route decorator in the repo (not from memory). | **`file:line`** for `@router.*` / `@app.*` (or the site that registers this handler). |
| 1b | Record HTTP method, `response_model=`, and `status_code=` on that decorator (or note they are absent). | **Snippet from that line** or **explicit absent** with the same **`file:line`**. |

### Gate 2 — Blocking or “should be async”

| Step | Action | **Pass condition** |
|------|--------|---------------------|
| 2a | Read the full handler body. | **`file:line` range** covering the body. |
| 2b | If claiming blocking I/O: name each blocking call (e.g. `requests.`, `open(`, `time.sleep`, sync DB/ORM). | **Each** call has **`file:line`**, or withdraw the finding if **none** after the read. |

### Gate 3 — Depends, validation, auth

| Step | Action | **Pass condition** |
|------|--------|---------------------|
| 3a | List parameters: `Depends` / `Annotated[..., Depends]`, Pydantic models, `Body`/`Query`/`Path`, `Request`/`Response`. | **Names + mechanism** tied to **`file:line`** on the signature. |
| 3b | If claiming missing auth: search the handler file (and its `APIRouter` module if separate) for `Depends`, `Security`, `HTTPBearer`, or project auth dependencies. | **Citation** to an existing hook, or **search result**: paths searched + **N matches** (zero is allowed). |
| 3c | If claiming missing validation: confirm the argument is not already a Pydantic model or constrained `Query`/`Path`/`Body`. | **Type/source** with **`file:line`**, or withdraw if validation already applies. |

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

1. For each FastAPI-related finding, complete **Gates (FastAPI-specific)** above.
2. Load and follow [review-verification-protocol](../review-verification-protocol/SKILL.md) (Pre-Report checklist and **Verification by Issue Type**) before reporting any issue.
