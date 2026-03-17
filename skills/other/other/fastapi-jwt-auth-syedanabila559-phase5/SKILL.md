---
name: fastapi-jwt-auth
description: This skill should be used when implementing secure, reusable JWT verification dependency for FastAPI routes. It ensures strict user isolation and identity verification using Better Auth secrets.
---

# FastAPI JWT Auth Middleware

This skill provides a secure, reusable JWT verification dependency for FastAPI routes.

## Purpose
Implementing a secure, reusable JWT verification dependency for FastAPI routes to ensure strict user isolation and identity verification.

## Capabilities
- Extracting `Authorization: Bearer <token>` from request headers.
- Verifying token signature using the `BETTER_AUTH_SECRET` environment variable.
- Decoding JWT payloads to extract authenticated `user_id` and `email`.
- Performing path-level validation to ensure the authenticated `user_id` matches the `{user_id}` variable in the route path.
- Standardized error handling with `HTTPException`:
  - `401 Unauthorized`: Token missing, invalid signature, or expired.
  - `403 Forbidden`: Authenticated user ID does not match the requested path resource.
- Providing a `current_user` object injectable directly into route functions.

## Implementation Details

### Security Pattern
Using `python-jose[cryptography]` or `PyJWT` to handle verification.
```python
from fastapi import Depends, HTTPException, status, Request
from jose import jwt

async def get_current_user(user_id: str, request: Request):
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Invalid auth header")

    token = auth_header.split(" ")[1]
    payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
    token_user_id = payload.get("user_id")

    if token_user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized for this resource")

    return payload
```

## Best Practices
- Loading `BETTER_AUTH_SECRET` only once at startup.
- Always validating the `user_id` against the path to prevent ID enumeration/access bypass.
- Using dependency injection to keep route logic clean and testable.
