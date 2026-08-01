---
name: fastapi-jwt
description: This skill provides implementation details for secure JWT verification
  middleware in FastAPI, specifically integrated with Better Auth secrets.
---

# FastAPI JWT Middleware Skill

## Purpose
This skill provides implementation details for secure JWT verification middleware in FastAPI, specifically integrated with Better Auth secrets.

## Capabilities
- Secure JWT extraction from Bearer headers
- Signature verification using `BETTER_AUTH_SECRET`
- Decoding and extraction of `user_id` and `email`
- Route-level ownership validation (matching `user_id` to route paths)
- Dependency injection patterns for FastAPI routes
- Standardized error handling (401/403 HTTPExceptions)

## Implementation Details

### JWT Extraction & Verification
Extract the token from the `Authorization` header and verify it against the `BETTER_AUTH_SECRET` environment variable.

### Data Model
Ensure the decoded payload contains:
- `user_id`: The unique identifier for the user.
- `email`: The user's email address.

### Permissions
Implement a check to ensure that if a `user_id` is present in the route path, it matches the `user_id` in the JWT payload.

### Error Handling
- Raise `401 Unauthorized` if the token is missing, invalid, or expired.
- Raise `403 Forbidden` if the `user_id` validation fails.

## Usage
Include the middleware as a dependency in FastAPI routes:

```python
@app.get("/users/{user_id}/profile")
async def get_profile(user_id: str, user: User = Depends(get_current_user)):
    # get_current_user logic handles JWT and user_id matching
    ...
```
