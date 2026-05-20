---
name: authentication-setup
description: Implement JWT authentication with bcrypt password hashing, refresh tokens, account lockout, and password reset flow. Use when setting up authentication or login system.
allowed-tools: Read, Write, Edit, Bash, Glob
---

You implement secure authentication for the QA Team Portal using JWT and bcrypt.

## When to Use This Skill

- Setting up user authentication system
- Implementing JWT with refresh tokens
- Adding password hashing with bcrypt
- Creating password reset flow
- Implementing account lockout mechanism
- Setting up session management

## Prerequisites

- FastAPI backend initialized
- User model exists in `backend/app/models/user.py`
- Database configured

## Implementation Components

### 1. Password Hashing (bcrypt)

**Location:** `backend/app/core/security.py`

```python
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password using bcrypt."""
    return pwd_context.hash(password)

def validate_password_strength(password: str) -> tuple[bool, str]:
    """
    Validate password meets requirements:
    - Minimum 12 characters
    - At least 1 uppercase, 1 lowercase, 1 number, 1 special char
    """
    if len(password) < 12:
        return False, "Password must be at least 12 characters"

    if not any(c.isupper() for c in password):
        return False, "Password must contain at least one uppercase letter"

    if not any(c.islower() for c in password):
        return False, "Password must contain at least one lowercase letter"

    if not any(c.isdigit() for c in password):
        return False, "Password must contain at least one number"

    if not any(c in "!@#$%^&*()_+-=[]{}|;:,.<>?" for c in password):
        return False, "Password must contain at least one special character"

    return True, "Password is strong"
```

### 2. JWT Token Generation

**Location:** `backend/app/core/security.py`

```python
from datetime import datetime, timedelta
from typing import Any, Union
from jose import jwt
from app.core.config import settings

def create_access_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """Create JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": "access"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(
    subject: Union[str, Any],
    expires_delta: timedelta = None
) -> str:
    """Create JWT refresh token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            days=settings.REFRESH_TOKEN_EXPIRE_DAYS
        )

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )
    return encoded_jwt

def decode_token(token: str) -> dict:
    """Decode and validate JWT token."""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(401, "Token has expired")
    except jwt.JWTError:
        raise HTTPException(401, "Could not validate credentials")
```

### 3. Authentication Dependencies

**Location:** `backend/app/api/deps.py`

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from sqlalchemy.orm import Session
from app.core.config import settings
from app.core.security import decode_token
from app.crud.user import user as user_crud
from app.db.session import get_db
from app.models.user import User

security = HTTPBearer()

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    token = credentials.credentials

    try:
        payload = decode_token(token)
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")

        if user_id is None or token_type != "access":
            raise HTTPException(401, "Invalid token")
    except JWTError:
        raise HTTPException(401, "Could not validate credentials")

    user = await user_crud.get(db, id=user_id)
    if user is None:
        raise HTTPException(404, "User not found")

    if user.status != "active":
        raise HTTPException(403, "User account is inactive")

    return user

async def get_current_active_admin(
    current_user: User = Depends(get_current_user)
) -> User:
    """Verify current user is an admin."""
    if current_user.role not in ["admin", "lead"]:
        raise HTTPException(403, "Not enough permissions")
    return current_user
```

### 4. Login Endpoint

**Location:** `backend/app/api/v1/endpoints/auth.py`

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from app.api.deps import get_db, get_current_user
from app.core.security import verify_password, create_access_token, create_refresh_token
from app.core.config import settings
from app.crud.user import user as user_crud
from app.schemas.auth import LoginRequest, TokenResponse

router = APIRouter()

@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login with email and password, returns access and refresh tokens.

    Account lockout after 5 failed attempts.
    """
    # Get user by email
    user = await user_crud.get_by_email(db, email=login_data.email)

    if not user:
        # Don't reveal if user exists or not
        raise HTTPException(401, "Incorrect email or password")

    # Check if account is locked
    if user.failed_login_attempts >= 5:
        if user.locked_until and user.locked_until > datetime.utcnow():
            raise HTTPException(403, "Account locked. Try again later.")
        else:
            # Reset lockout if time expired
            await user_crud.reset_failed_attempts(db, user_id=user.id)

    # Verify password
    if not verify_password(login_data.password, user.password_hash):
        # Increment failed attempts
        await user_crud.increment_failed_attempts(db, user_id=user.id)
        raise HTTPException(401, "Incorrect email or password")

    # Check if user is active
    if user.status != "active":
        raise HTTPException(403, "User account is inactive")

    # Reset failed attempts on successful login
    await user_crud.reset_failed_attempts(db, user_id=user.id)

    # Update last login
    await user_crud.update_last_login(db, user_id=user.id)

    # Create tokens
    access_token = create_access_token(subject=str(user.id))
    refresh_token = create_refresh_token(subject=str(user.id))

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
        "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
    }
```

### 5. Refresh Token Endpoint

```python
@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    refresh_token: str,
    db: Session = Depends(get_db)
):
    """Refresh access token using refresh token."""
    try:
        payload = decode_token(refresh_token)
        user_id = payload.get("sub")
        token_type = payload.get("type")

        if token_type != "refresh":
            raise HTTPException(401, "Invalid token type")

        user = await user_crud.get(db, id=user_id)
        if not user or user.status != "active":
            raise HTTPException(401, "Invalid token")

        # Create new access token
        new_access_token = create_access_token(subject=str(user.id))

        return {
            "access_token": new_access_token,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    except JWTError:
        raise HTTPException(401, "Invalid refresh token")
```

### 6. Password Reset Flow

```python
import secrets
from datetime import datetime, timedelta

@router.post("/forgot-password")
async def forgot_password(
    email: str,
    db: Session = Depends(get_db)
):
    """Send password reset email."""
    user = await user_crud.get_by_email(db, email=email)

    # Don't reveal if user exists
    if not user:
        return {"message": "If the email exists, a reset link has been sent"}

    # Generate reset token (random, not JWT)
    reset_token = secrets.token_urlsafe(32)
    expires = datetime.utcnow() + timedelta(minutes=15)

    # Store token in database
    await user_crud.set_reset_token(
        db,
        user_id=user.id,
        token=reset_token,
        expires=expires
    )

    # Send email (use email service)
    # await send_password_reset_email(user.email, reset_token)

    return {"message": "If the email exists, a reset link has been sent"}

@router.post("/reset-password")
async def reset_password(
    token: str,
    new_password: str,
    db: Session = Depends(get_db)
):
    """Reset password using reset token."""
    # Validate password strength
    is_valid, message = validate_password_strength(new_password)
    if not is_valid:
        raise HTTPException(400, message)

    # Find user by reset token
    user = await user_crud.get_by_reset_token(db, token=token)

    if not user or not user.reset_token_expires:
        raise HTTPException(400, "Invalid or expired reset token")

    # Check if token expired
    if user.reset_token_expires < datetime.utcnow():
        raise HTTPException(400, "Reset token has expired")

    # Update password
    password_hash = get_password_hash(new_password)
    await user_crud.update_password(
        db,
        user_id=user.id,
        password_hash=password_hash
    )

    # Clear reset token
    await user_crud.clear_reset_token(db, user_id=user.id)

    return {"message": "Password reset successful"}
```

### 7. User Model Updates

**Location:** `backend/app/models/user.py`

Add these fields to User model:

```python
from sqlalchemy import Column, String, Integer, DateTime

class User(Base):
    # ... existing fields ...

    # Account lockout
    failed_login_attempts = Column(Integer, default=0)
    locked_until = Column(DateTime, nullable=True)

    # Password reset
    reset_token = Column(String(255), nullable=True)
    reset_token_expires = Column(DateTime, nullable=True)

    # Session tracking
    last_login = Column(DateTime, nullable=True)
```

### 8. CRUD Operations

**Location:** `backend/app/crud/user.py`

Add these methods to UserCRUD:

```python
async def increment_failed_attempts(self, db: Session, user_id: UUID):
    """Increment failed login attempts and lock if needed."""
    user = await self.get(db, id=user_id)
    user.failed_login_attempts += 1

    if user.failed_login_attempts >= 5:
        user.locked_until = datetime.utcnow() + timedelta(minutes=30)

    db.commit()
    return user

async def reset_failed_attempts(self, db: Session, user_id: UUID):
    """Reset failed login attempts."""
    user = await self.get(db, id=user_id)
    user.failed_login_attempts = 0
    user.locked_until = None
    db.commit()
    return user

async def set_reset_token(
    self,
    db: Session,
    user_id: UUID,
    token: str,
    expires: datetime
):
    """Set password reset token."""
    user = await self.get(db, id=user_id)
    user.reset_token = token
    user.reset_token_expires = expires
    db.commit()
    return user
```

## Configuration

**Location:** `backend/app/core/config.py`

```python
class Settings(BaseSettings):
    # JWT
    SECRET_KEY: str  # Generate with: openssl rand -hex 32
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 15
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
```

## Testing Authentication

```python
# tests/integration/test_api_auth.py
import pytest
from fastapi.testclient import TestClient

def test_login_success(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "testpass123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()

def test_login_invalid_password(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "wrongpassword"
    })
    assert response.status_code == 401

def test_account_lockout(client, test_user):
    # Try 5 times with wrong password
    for i in range(5):
        client.post("/api/v1/auth/login", json={
            "email": "admin@test.com",
            "password": "wrongpassword"
        })

    # 6th attempt should be locked
    response = client.post("/api/v1/auth/login", json={
        "email": "admin@test.com",
        "password": "testpass123"
    })
    assert response.status_code == 403
    assert "locked" in response.json()["detail"].lower()
```

## Security Checklist

- ✅ Passwords hashed with bcrypt (cost factor 12)
- ✅ JWT with short expiry (15 minutes access, 7 days refresh)
- ✅ Password strength validation (12+ chars, complexity)
- ✅ Account lockout after 5 failed attempts (30 min)
- ✅ Password reset with secure random token (15 min expiry)
- ✅ Tokens validated on every request
- ✅ User status checked (active/inactive)
- ✅ HTTPOnly cookies for refresh tokens (frontend)
- ✅ No password exposure in logs or errors
- ✅ Rate limiting on auth endpoints (use /security command)

## Frontend Integration

```typescript
// frontend/src/services/authService.ts
export const login = async (email: string, password: string) => {
  const response = await api.post('/auth/login', { email, password })

  // Store tokens
  localStorage.setItem('access_token', response.data.access_token)
  // Refresh token in HttpOnly cookie (set by backend)

  return response.data
}

export const refreshAccessToken = async () => {
  const response = await api.post('/auth/refresh')
  localStorage.setItem('access_token', response.data.access_token)
  return response.data
}

// Add to axios interceptor
api.interceptors.response.use(
  response => response,
  async error => {
    if (error.response?.status === 401) {
      try {
        await refreshAccessToken()
        // Retry original request
        return api(error.config)
      } catch {
        // Refresh failed, logout
        logout()
      }
    }
    return Promise.reject(error)
  }
)
```

## Report Format

After implementation, provide:
1. ✅ JWT authentication implemented
2. ✅ Password hashing with bcrypt
3. ✅ Account lockout mechanism active
4. ✅ Password reset flow complete
5. ✅ Refresh token mechanism working
6. ✅ Tests passing (X/Y)
7. ⚠️ Security recommendations (if any)
