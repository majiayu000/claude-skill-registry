---
name: auth-security
description: JWT authentication with Better Auth, token verification, user isolation, and security middleware. Use when implementing auth, protecting endpoints, or verifying tokens.
---

# JWT Authentication & Security

## JWT Verification Middleware
```python
from fastapi import Header, HTTPException
import jwt
import os

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

async def verify_jwt(authorization: str = Header(None)) -> str:
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization")
    
    token = authorization.replace("Bearer ", "")
    try:
        payload = jwt.decode(token, BETTER_AUTH_SECRET, algorithms=["HS256"])
        user_id = payload.get("sub") or payload.get("user_id")
        if not user_id:
            raise HTTPException(status_code=401, detail="Invalid token payload")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token expired")
    except jwt.InvalidTokenError:
        raise HTTPException(status_code=401, detail="Invalid token")
```

## Protected Endpoint
```python
@app.post("/api/{user_id}/resource")
async def endpoint(user_id: str, current_user: str = Depends(verify_jwt)):
    # Enforce user_id matching
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    # Proceed with authenticated user_id
```

## Security Checklist
- BETTER_AUTH_SECRET in .env (never in code)
- JWT verification on all protected endpoints
- User ID from token matches URL parameter
- All DB queries filtered by authenticated user_id
- CORS origins whitelist (no wildcard in production)

## Testing
```python
import jwt
from datetime import datetime, timedelta

def generate_test_token(user_id: str):
    payload = {"sub": user_id, "exp": datetime.utcnow() + timedelta(hours=1)}
    return jwt.encode(payload, BETTER_AUTH_SECRET, algorithm="HS256")

def test_protected():
    token = generate_test_token("user123")
    response = client.post(
        "/api/user123/resource",
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
```