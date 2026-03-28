---
name: jwt-auth
description: |
  Use when implementing JWT authentication in FastAPI or Python projects.
  Triggers for: token generation, verification middleware, current user extraction,
  access token creation, token decoding, or role-based auth.
  NOT for: OAuth2 provider setup, OpenID Connect, or non-Python backends.
---

# JWT Authentication Skill

Expert implementation of JWT token generation, verification, and user extraction for FastAPI and Python applications.

## Quick Reference

| Operation | Function | Location |
|-----------|----------|----------|
| Generate token | `create_access_token(data, expires_delta=None)` | `auth/jwt.py` |
| Verify token | `verify_token(token: str)` | `auth/dependencies.py` |
| Get current user | `get_current_user(token: str)` | `auth/dependencies.py` |
| User from payload | `User.from_payload(payload)` | `auth/dependencies.py` |

## Core Workflows

### 1. Generate Access Token

```python
from auth.jwt import create_access_token

# Basic token with subject
token = create_access_token(data={"sub": "user@example.com"})

# Token with custom expiry (minutes)
from datetime import timedelta
token = create_access_token(
    data={"sub": "user@example.com", "roles": ["admin"]},
    expires_delta=timedelta(minutes=15)
)

# Token with roles for RBAC
token = create_access_token(data={"sub": "user@corp.com", "roles": ["editor", "viewer"]})
```

**Claims structure:**
- `sub` (required): User identifier (email, ID, or username)
- `exp` (auto): Expiration time
- `roles` (optional): List of role strings for authorization
- Custom claims: Add any extra data as needed

### 2. Protect Endpoint with Dependency

```python
from fastapi import APIRouter, Depends
from auth.dependencies import get_current_user

router = APIRouter()

@router.get("/protected")
def protected_route(user = Depends(get_current_user)):
    return {"message": f"Hello, {user.email}"}
```

### 3. Role-Based Access Control

```python
from auth.dependencies import get_current_user, RoleChecker

# Define role checker
admin_only = RoleChecker(allowed_roles=["admin"])

@router.delete("/admin-only")
def admin_endpoint(user = Depends(admin_only)):
    return {"message": "Admin access granted"}
```

### 4. Extract User from JWT Payload

```python
from auth.dependencies import get_current_user

# User model automatically extracted from JWT claims
@router.get("/me")
def get_me(user = Depends(get_current_user)):
    return {
        "email": user.email,
        "roles": user.roles,
        "is_active": user.is_active
    }
```

## Security Checklist

- [ ] **Short expiry + refresh**: Access tokens expire in 15-30 minutes; implement refresh token flow for long sessions
- [ ] **No sensitive data**: Never put passwords, PII, or secrets in JWT claims
- [ ] **Blacklist invalid**: Implement token blacklist for logout (see `revoked_tokens` set)
- [ ] **HS256 algorithm**: Use HMAC-SHA256; never use `algorithm="none"`
- [ ] **Verify expiration**: Always check `exp` claim; reject expired tokens

## Token Structure

```
Header:
{
  "alg": "HS256",
  "typ": "JWT"
}

Payload:
{
  "sub": "user@example.com",
  "roles": ["user", "editor"],
  "exp": 1704067200,
  "iat": 1704063600
}

Signature: HMAC-SHA256(secret, header.payload)
```

## User Model

```python
class User:
    email: str
    roles: List[str]
    is_active: bool = True

    @classmethod
    def from_payload(cls, payload: dict) -> "User":
        """Extract User from decoded JWT payload."""
        return cls(
            email=payload.get("sub", ""),
            roles=payload.get("roles", []),
            is_active=payload.get("is_active", True)
        )
```

## Integration with @auth-integration Frontend

The backend JWT implementation pairs with the frontend auth integration skill:

1. **Backend**: `auth/jwt.py` and `auth/dependencies.py`
2. **Frontend**: Use `auth-integration` skill for React/Next.js auth context
3. **Token flow**:
   - Frontend stores token in memory/storage after login
   - Frontend includes `Authorization: Bearer <token>` header
   - Backend `HTTPBearer()` dependency validates and extracts user
   - Failed verification returns 401 Unauthorized

## File Outputs

| File | Purpose |
|------|---------|
| `auth/jwt.py` | Token creation, encoding, secret config |
| `auth/dependencies.py` | FastAPI dependencies for verification and user extraction |

## Configuration

Set these environment variables:
- `JWT_SECRET_KEY`: Long random string (at least 32 chars)
- `JWT_ALGORITHM`: "HS256" (default)
- `JWT_EXPIRATION_MINUTES`: 15 (recommended)

## Quality Gates

Before marking complete:
- [ ] Tokens use HS256 algorithm
- [ ] Expiration set to 15-30 minutes
- [ ] No sensitive data in claims
- [ ] Blacklist mechanism implemented for logout
- [ ] Integration with `auth-integration` frontend skill documented
