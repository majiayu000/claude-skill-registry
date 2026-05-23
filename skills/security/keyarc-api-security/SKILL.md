---
name: keyarc-api-security
description: Use when creating FastAPI endpoints, implementing JWT authentication, handling encrypted payloads, adding audit logging, or applying OWASP security patterns to KeyArc API endpoints.
---

# KeyArc API Security Patterns

## Overview

Security patterns for KeyArc's zero-knowledge FastAPI backend services. Covers JWT authentication, encrypted payload validation, audit logging, and OWASP top 10 prevention.

## Service Architecture Context

KeyArc uses a multi-service architecture:

| Service | Visibility | Security Responsibility |
|---------|------------|------------------------|
| **Auth Service** | Public | Issues JWTs, validates authHash, rate limits login |
| **Gateway** | Public | Validates JWTs, routes to private services |
| **Account Service** | Private | Trusts Gateway, uses RBAC for team permissions |
| **Key Service** | Private | Trusts Gateway, uses RBAC, validates encrypted payloads |

**Key security boundaries:**
- Gateway handles JWT validation - private services trust user context headers from Gateway
- Auth Service is the only service that validates authHash (never passwords)
- RBAC checks happen in Account Service and Key Service using shared RBAC module
- Audit logging is a shared module used by all services

## When to Use

✅ **Apply this skill when:**
- Creating new API endpoints in any service
- Implementing authentication/authorization
- Handling secrets or encrypted data
- Adding audit logging
- Reviewing security of existing endpoints
- Implementing rate limiting
- Handling errors that might leak data

## Core Security Principles

1. **Validate encrypted payloads** - Never accept plaintext secrets
2. **JWT token authentication** - Validate using authHash, not passwords
3. **Audit everything** - Log all secret access (not values)
4. **Fail securely** - Errors don't leak sensitive data
5. **Rate limit auth** - Prevent brute force attacks
6. **RBAC enforcement** - Check permissions at API level

## Endpoint Security Checklist

Before merging any new endpoint:

**Auth Service endpoints:**
- [ ] Rate limiting applied (5/minute for login)
- [ ] authHash validated (never password)
- [ ] Audit log entry created
- [ ] Error responses don't leak data

**Gateway:**
- [ ] JWT token validated
- [ ] User context headers added for downstream
- [ ] Invalid tokens rejected with 401

**Account/Key Service endpoints (private):**
- [ ] User context from Gateway headers (use `Depends(get_current_user_from_gateway)`)
- [ ] RBAC permissions checked for team operations (use shared RBAC module)
- [ ] Encrypted payloads validated - no plaintext secrets (Key Service)
- [ ] Audit log entry created
- [ ] Error responses don't leak secrets
- [ ] Input validation with Pydantic
- [ ] SQL injection prevented (use ORM)

## JWT Authentication Pattern

```python
# dependencies.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.ext.asyncio import AsyncSession

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Validate JWT token and return current user."""
    token = credentials.credentials

    try:
        payload = jwt.decode(
            token,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials"
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials"
        )

    # Get user from database
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found"
        )

    return user
```

## Creating Tokens (Auth Service Only)

```python
# src/services/auth/app/utils/security.py
from datetime import datetime, timedelta
from jose import jwt

SECRET_KEY = os.getenv("JWT_SECRET")  # From environment
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 120  # 2 hours

def create_access_token(data: dict) -> str:
    """Create JWT access token. Auth Service only."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
```

## Gateway User Context

The Gateway validates JWTs and passes user context to private services via headers:

```python
# Gateway adds these headers after JWT validation:
# X-User-ID: <user_id>
# X-User-Email: <email>

# Private services (Account, Key) read user from headers:
# src/services/account/app/dependencies.py or src/services/keys/app/dependencies.py

from fastapi import Header, HTTPException

async def get_current_user_from_gateway(
    x_user_id: str = Header(..., alias="X-User-ID"),
    x_user_email: str = Header(None, alias="X-User-Email"),
) -> dict:
    """Get user context from Gateway headers. For private services only."""
    if not x_user_id:
        raise HTTPException(401, "Missing user context")

    return {
        "id": int(x_user_id),
        "email": x_user_email
    }
```

**Important:** Private services should only be accessible via Gateway (Fly.io private networking). They trust Gateway headers because external traffic cannot reach them directly.

## Secure Endpoint Example

```python
@router.post("/secrets", response_model=SecretResponse, status_code=201)
async def create_secret(
    secret_data: SecretCreate,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new encrypted secret."""

    # Validate encrypted payload format
    if not is_valid_ciphertext(secret_data.encrypted_value):
        raise HTTPException(400, "Invalid encrypted format")

    # Create secret (store ciphertext only)
    secret = Secret(
        user_id=current_user.id,
        name=secret_data.name,
        encrypted_value=secret_data.encrypted_value,
        folder_id=secret_data.folder_id,
        tags=secret_data.tags
    )

    db.add(secret)
    await db.commit()
    await db.refresh(secret)

    # Audit log (NO secret value!)
    await create_audit_log(
        db=db,
        user_id=current_user.id,
        action="secret.create",
        resource_type="secret",
        resource_id=secret.id,
        ip_address=request.client.host  # From request context
    )

    return secret
```

## Pydantic Schemas for Security

```python
from pydantic import BaseModel, EmailStr, Field, validator

class SecretCreate(BaseModel):
    """Schema for creating a secret."""
    name: str = Field(min_length=1, max_length=255)
    encrypted_value: str = Field(min_length=1)
    folder_id: int | None = None
    tags: list[str] = Field(default_factory=list)

    @validator('encrypted_value')
    def validate_encrypted(cls, v):
        """Ensure value is actually encrypted (base64)."""
        try:
            import base64
            base64.b64decode(v)
            return v
        except Exception:
            raise ValueError('encrypted_value must be base64-encoded ciphertext')

class LoginRequest(BaseModel):
    """Login request with auth hash (NOT password)."""
    email: EmailStr
    auth_hash: str = Field(min_length=1)

    # NO password field! Only authHash!
```

## Audit Logging

```python
async def create_audit_log(
    db: AsyncSession,
    user_id: int,
    action: str,
    resource_type: str,
    resource_id: int,
    ip_address: str,
    metadata: dict | None = None
) -> AuditLog:
    """Create audit log entry."""
    log = AuditLog(
        user_id=user_id,
        action=action,  # 'secret.view', 'secret.create', 'secret.delete', etc.
        resource_type=resource_type,
        resource_id=resource_id,
        ip_address=ip_address,
        metadata=metadata,  # Never include secret values!
        timestamp=datetime.utcnow()
    )

    db.add(log)
    await db.flush()  # Don't commit yet (part of larger transaction)

    return log

# Usage in endpoint:
await create_audit_log(
    db=db,
    user_id=current_user.id,
    action="secret.view",
    resource_type="secret",
    resource_id=secret_id,
    ip_address=request.client.host
)
```

## RBAC Permission Checking

```python
async def check_team_permission(
    user_id: int,
    team_id: int,
    required_role: str,  # 'owner', 'admin', 'member'
    db: AsyncSession
) -> TeamMembership:
    """Check if user has required role in team."""
    result = await db.execute(
        select(TeamMembership).where(
            TeamMembership.user_id == user_id,
            TeamMembership.team_id == team_id
        )
    )
    membership = result.scalar_one_or_none()

    if not membership:
        raise HTTPException(403, "Not a team member")

    role_hierarchy = {'member': 0, 'admin': 1, 'owner': 2}
    if role_hierarchy.get(membership.role, -1) < role_hierarchy.get(required_role, 999):
        raise HTTPException(403, "Insufficient permissions")

    return membership
```

## Rate Limiting

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

@router.post("/auth/login")
@limiter.limit("5/minute")  # 5 attempts per minute per IP
async def login(
    request: Request,
    login_data: LoginRequest,
    db: AsyncSession = Depends(get_db)
):
    # ... login logic
```

## Error Handling (Secure)

```python
# ❌ BAD: Leaks sensitive data
@router.get("/secrets/{secret_id}")
async def get_secret(secret_id: int):
    secret = await db.get(Secret, secret_id)
    if not secret:
        raise HTTPException(404, f"Secret {secret.encrypted_value} not found")  # LEAK!

# ✅ GOOD: Generic errors
@router.get("/secrets/{secret_id}")
async def get_secret(
    secret_id: int,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    secret = await db.get(Secret, secret_id)

    if not secret:
        raise HTTPException(404, "Secret not found")

    # Check ownership
    if secret.user_id != current_user.id:
        # Same error (don't reveal if secret exists)
        raise HTTPException(404, "Secret not found")

    # Audit log
    await create_audit_log(
        db=db,
        user_id=current_user.id,
        action="secret.view",
        resource_type="secret",
        resource_id=secret_id,
        ip_address=request.client.host
    )

    await db.commit()

    return secret
```

## OWASP Top 10 Quick Reference

See `owasp-checklist.md` for detailed prevention patterns.

| Vulnerability | Prevention |
|--------------|------------|
| Injection | SQLAlchemy ORM, parameterized queries |
| Broken Auth | JWT tokens, rate limiting, authHash validation |
| Sensitive Data Exposure | All secrets encrypted, HTTPS only |
| XXE | Validate XML inputs |
| Broken Access Control | RBAC enforced at API level |
| Security Misconfiguration | Secure defaults, no debug in production |
| XSS | Angular handles this, validate API responses |
| Insecure Deserialization | Validate Pydantic models |
| Known Vulnerabilities | Dependabot enabled |
| Insufficient Logging | Comprehensive audit logs |

## See Also

- `jwt-patterns.md` - Detailed JWT implementation
- `audit-logging.md` - Comprehensive audit logging requirements
- `owasp-checklist.md` - Detailed OWASP top 10 prevention

## Key Principles

1. **Validate encrypted payloads**: Never accept plaintext secrets
2. **Auth with JWT**: Token-based, stateless authentication
3. **Audit everything**: Log access, not values
4. **RBAC at API layer**: Enforce permissions in endpoints
5. **Rate limit sensitive endpoints**: Prevent brute force
6. **Secure error handling**: Generic errors, no leaks
7. **Input validation**: Always use Pydantic schemas

**Security is not optional - apply these patterns to every endpoint.**
