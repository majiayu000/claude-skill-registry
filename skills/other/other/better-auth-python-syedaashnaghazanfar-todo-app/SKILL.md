---
name: better-auth-python
description: Better Auth JWT verification for Python/FastAPI backends. Use when integrating Python APIs with a Better Auth TypeScript server via JWT tokens. Covers JWKS verification, FastAPI dependencies, SQLModel/SQLAlchemy integration, and protected routes.
---

# Better Auth Python Integration Skill

Integrate Python/FastAPI backends with Better Auth (TypeScript) authentication server using JWT verification.

## Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Next.js App   │────▶│  Better Auth    │────▶│   PostgreSQL    │
│   (Frontend)    │     │  (Auth Server)  │     │   (Database)    │
└────────┬────────┘     └────────┬────────┘     └─────────────────┘
         │                       │
         │ JWT Token             │ JWKS Endpoint
         ▼                       ▼
┌─────────────────────────────────────────────────────────────────┐
│                     FastAPI Backend                              │
│                   (Verifies JWT tokens)                          │
└─────────────────────────────────────────────────────────────────┘
```

## Quick Start

### Installation

```bash
# pip
pip install fastapi uvicorn pyjwt cryptography httpx

# poetry
poetry add fastapi uvicorn pyjwt cryptography httpx

# uv
uv add fastapi uvicorn pyjwt cryptography httpx
```

### Environment Variables

```env
DATABASE_URL=postgresql://user:password@localhost:5432/mydb
BETTER_AUTH_URL=http://localhost:3000
```

## ORM Integration (Choose One)

| ORM | Guide |
|-----|-------|
| **SQLModel** | [reference/sqlmodel.md](reference/sqlmodel.md) |
| **SQLAlchemy** | [reference/sqlalchemy.md](reference/sqlalchemy.md) |

## Basic JWT Verification

```python
# app/auth.py
import os
import httpx
import jwt
from dataclasses import dataclass
from typing import Optional
from fastapi import HTTPException, Header, status

BETTER_AUTH_URL = os.getenv("BETTER_AUTH_URL", "http://localhost:3000")

@dataclass
class User:
    id: str
    email: str
    name: Optional[str] = None

_jwks_cache: dict = {}

async def get_jwks() -> dict:
    global _jwks_cache
    if not _jwks_cache:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{BETTER_AUTH_URL}/.well-known/jwks.json")
            response.raise_for_status()
            _jwks_cache = response.json()
    return _jwks_cache

async def verify_token(token: str) -> User:
    if token.startswith("Bearer "):
        token = token[7:]

    jwks = await get_jwks()
    public_keys = {}
    for key in jwks.get("keys", []):
        public_keys[key["kid"]] = jwt.algorithms.RSAAlgorithm.from_jwk(key)

    unverified_header = jwt.get_unverified_header(token)
    kid = unverified_header.get("kid")

    if not kid or kid not in public_keys:
        raise HTTPException(status_code=401, detail="Invalid token key")

    payload = jwt.decode(token, public_keys[kid], algorithms=["RS256"])

    return User(
        id=payload.get("sub"),
        email=payload.get("email"),
        name=payload.get("name"),
    )

async def get_current_user(
    authorization: str = Header(..., alias="Authorization")
) -> User:
    return await verify_token(authorization)
```

### Protected Route

```python
from fastapi import Depends
from app.auth import User, get_current_user

@app.get("/api/me")
async def get_me(user: User = Depends(get_current_user)):
    return {"id": user.id, "email": user.email, "name": user.name}
```

## Examples

| Pattern | Guide |
|---------|-------|
| **Protected Routes** | [examples/protected-routes.md](examples/protected-routes.md) |
| **JWT Verification** | [examples/jwt-verification.md](examples/jwt-verification.md) |

## Templates

| Template | Purpose |
|----------|---------|
| [templates/auth.py](templates/auth.py) | JWT verification module |
| [templates/main.py](templates/main.py) | FastAPI app template |
| [templates/database_sqlmodel.py](templates/database_sqlmodel.py) | SQLModel database setup |
| [templates/models_sqlmodel.py](templates/models_sqlmodel.py) | SQLModel models |

## Quick SQLModel Example

```python
from sqlmodel import SQLModel, Field, Session, select
from typing import Optional
from datetime import datetime

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True)
    completed: bool = Field(default=False)
    user_id: str = Field(index=True)  # From JWT 'sub' claim

@app.get("/api/tasks")
async def get_tasks(
    user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
):
    statement = select(Task).where(Task.user_id == user.id)
    return session.exec(statement).all()
```

## Frontend Integration

### Getting JWT from Better Auth

```typescript
import { authClient } from "./auth-client";

const { data } = await authClient.token();
const jwtToken = data?.token;
```

### Sending to FastAPI

```typescript
async function fetchAPI(endpoint: string) {
  const { data } = await authClient.token();

  return fetch(`${API_URL}${endpoint}`, {
    headers: {
      Authorization: `Bearer ${data?.token}`,
      "Content-Type": "application/json",
    },
  });
}
```

## Security Considerations

1. **Always use HTTPS** in production
2. **Validate issuer and audience** to prevent token substitution
3. **Handle token expiration** gracefully
4. **Refresh JWKS** when encountering unknown key IDs
5. **Don't log tokens** - they contain sensitive data

## Troubleshooting

### JWKS fetch fails
- Ensure Better Auth server is running
- Check JWKS endpoint is accessible
- Verify network connectivity

### Token validation fails
- Check issuer/audience match exactly
- Verify token hasn't expired
- Check algorithm compatibility (RS256)

### CORS errors
- Configure CORS middleware properly
- Allow credentials if using cookies
- Check origin is in allowed list
