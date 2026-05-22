# Skill: JWT Middleware for FastAPI

**Purpose**: Generate JWT verification middleware for FastAPI that validates Better Auth tokens.

## Trigger Conditions

Invoke this skill when:
- Setting up authentication in FastAPI backend
- User mentions "JWT", "token verification", or "auth middleware"
- Phase II requires protected API endpoints

## Capabilities

### 1. Generate JWT Middleware

Creates `backend/app/middleware/auth.py`:

```python
from fastapi import HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import jwt, JWTError
from typing import Optional
from ..config import settings

security = HTTPBearer()

class TokenPayload:
    """Decoded JWT token payload"""
    def __init__(self, user_id: str, email: str, exp: int):
        self.user_id = user_id
        self.email = email
        self.exp = exp

async def verify_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> TokenPayload:
    """
    Verify JWT token from Authorization header.
    Returns decoded payload with user_id.
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            settings.BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )

        user_id = payload.get("sub") or payload.get("user_id")
        email = payload.get("email", "")
        exp = payload.get("exp", 0)

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )

        return TokenPayload(user_id=user_id, email=email, exp=exp)

    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Invalid or expired token: {str(e)}"
        )

async def verify_user_access(
    user_id_param: str,
    token: TokenPayload = Depends(verify_token)
) -> TokenPayload:
    """
    Verify that the authenticated user matches the user_id in the URL.
    Prevents users from accessing other users' resources.
    """
    if token.user_id != user_id_param:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied: You can only access your own resources"
        )
    return token

# Convenience dependency for routes
def get_current_user(
    token: TokenPayload = Depends(verify_token)
) -> str:
    """Returns the current user's ID"""
    return token.user_id
```

### 2. Usage in Routes

```python
from fastapi import APIRouter, Depends
from ..middleware.auth import verify_token, verify_user_access, TokenPayload

router = APIRouter()

@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    token: TokenPayload = Depends(verify_token)
):
    # Verify user can only access their own tasks
    if token.user_id != user_id:
        raise HTTPException(status_code=403, detail="Access denied")

    # ... fetch tasks for user_id
```

### 3. Route-Level Protection Pattern

```python
# For routes that need user_id validation
@router.get("/api/{user_id}/tasks")
async def list_tasks(
    user_id: str,
    _: TokenPayload = Depends(lambda: verify_user_access(user_id))
):
    pass

# For routes that just need authentication
@router.get("/api/profile")
async def get_profile(
    current_user: str = Depends(get_current_user)
):
    pass
```

## Dependencies

Add to `requirements.txt`:
```
python-jose[cryptography]>=3.3.0
```

## Token Structure Expected

Better Auth JWT payload format:
```json
{
  "sub": "user-uuid-here",
  "email": "user@example.com",
  "exp": 1735344000,
  "iat": 1734739200
}
```

## Common Errors & Solutions

| Error | Cause | Solution |
|-------|-------|----------|
| "Invalid token" | Wrong secret | Ensure BETTER_AUTH_SECRET matches frontend |
| "Token expired" | JWT expired | Re-authenticate user |
| "Access denied" | user_id mismatch | User trying to access another user's data |

## Integration Checklist

- [ ] Add `python-jose[cryptography]` to requirements
- [ ] Create `middleware/auth.py` with verify functions
- [ ] Add `BETTER_AUTH_SECRET` to `.env`
- [ ] Import and use `Depends(verify_token)` in protected routes
- [ ] Test with valid/invalid/expired tokens
