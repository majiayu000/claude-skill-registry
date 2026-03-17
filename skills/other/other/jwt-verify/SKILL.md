---
name: jwt-verify
description: Implement JWT verification middleware in FastAPI for user auth. Use when securing APIs or handling tokens.
---
# JWTVerify Instructions
Input: Request with Authorization header, shared secret.
Output: Verified user claims or 401 error.
Steps:
1. Install dependencies if needed (jose, fastapi-security).
2. Generate middleware code.
Example Code:
from fastapi import Depends, HTTPException
from jose import JWTError, jwt
from fastapi.security import HTTPBearer
security = HTTPBearer()
async def verify_jwt(token: str = Depends(security)):
    try:
        payload = jwt.decode(token.credentials, SECRET_KEY, algorithms=["HS256"])
        return payload
    except JWTError:
        raise HTTPException(401, "Invalid token")