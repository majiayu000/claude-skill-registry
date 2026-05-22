# Backend JWT Authentication Skill

**Purpose**: Guidance for implementing JWT authentication middleware, token verification, and user isolation using Better Auth shared secret.

## Overview

JWT authentication MUST verify tokens on every API request, extract user information, validate user_id matches URL path, and use Better Auth shared secret (BETTER_AUTH_SECRET) for consistency with frontend.

## Key Patterns

### 1. JWT Token Verification Middleware

**File Location**: `/backend/middleware/jwt.py`

**Pattern**: Create dependency function for JWT verification

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
import os
from typing import Dict

# Get shared secret from environment
BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

# HTTP Bearer token scheme
security = HTTPBearer()

def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    """
    Verify JWT token and extract user information.
    
    Returns:
        dict: {"user_id": str, "email": str}
    
    Raises:
        HTTPException: 401 if token is invalid or missing
    """
    token = credentials.credentials
    
    try:
        # Decode and verify JWT token
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]  # HMAC SHA-256
        )
        
        # Extract user information
        user_id: str = payload.get("sub") or payload.get("user_id")
        email: str = payload.get("email")
        
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: missing user_id"
            )
        
        return {
            "user_id": user_id,
            "email": email or ""
        }
    
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Token verification failed: {str(e)}"
        )
```

**Pattern Rules**:
- Use `HTTPBearer()` for extracting token from Authorization header
- Use `jwt.decode()` with shared secret and HS256 algorithm
- Extract `user_id` from `sub` or `user_id` claim
- Return dict with user information
- Raise 401 Unauthorized for invalid tokens
- Use BETTER_AUTH_SECRET from environment

### 2. User ID Validation in Routes

**Pattern**: Verify user_id from JWT matches URL path user_id

```python
from fastapi import Depends, HTTPException, status
from backend.middleware.jwt import verify_jwt_token

@router.get("/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, str] = Depends(verify_jwt_token)
):
    # CRITICAL: Verify user_id matches JWT token
    if current_user["user_id"] != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User ID mismatch: You can only access your own data"
        )
    
    # Proceed with request
    tasks = task_service.get_tasks(db, user_id)
    return {"success": True, "data": tasks}
```

**Pattern Rules**:
- ALWAYS verify user_id from JWT matches path parameter
- Return 403 Forbidden if mismatch (not 401)
- Never trust user_id from URL path alone
- Use user_id from JWT token for database queries

### 3. JWT Token Generation (for Signup/Signin)

**Pattern**: Generate JWT tokens after successful authentication

```python
from jose import jwt
from datetime import datetime, timedelta
import os

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")
JWT_EXPIRATION_DAYS = 7  # 7-day expiration as per constitution

def generate_jwt_token(user_id: str, email: str) -> str:
    """
    Generate JWT token for authenticated user.
    
    Args:
        user_id: User's unique identifier (UUID)
        email: User's email address
    
    Returns:
        str: JWT token string
    """
    # Calculate expiration time
    expiration = datetime.utcnow() + timedelta(days=JWT_EXPIRATION_DAYS)
    
    # Create payload
    payload = {
        "sub": user_id,  # Standard JWT subject claim
        "user_id": user_id,  # Also include for compatibility
        "email": email,
        "exp": expiration,  # Expiration timestamp
        "iat": datetime.utcnow()  # Issued at timestamp
    }
    
    # Encode token
    token = jwt.encode(
        payload,
        BETTER_AUTH_SECRET,
        algorithm="HS256"
    )
    
    return token
```

**Pattern Rules**:
- Use `sub` claim for user_id (JWT standard)
- Include `user_id` for compatibility
- Set expiration to 7 days (as per constitution)
- Use HS256 algorithm
- Include `exp` and `iat` claims
- Use BETTER_AUTH_SECRET for signing

### 4. Password Hashing

**Pattern**: Hash passwords securely before storing

```python
from passlib.context import CryptContext

# Create password context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
    """
    Hash password using bcrypt.
    
    Args:
        password: Plain text password
    
    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.
    
    Args:
        plain_password: Plain text password
        hashed_password: Hashed password from database
    
    Returns:
        bool: True if password matches
    """
    return pwd_context.verify(plain_password, hashed_password)
```

**Pattern Rules**:
- Use bcrypt for password hashing
- Never store plain text passwords
- Use `verify_password()` for authentication
- Use `hash_password()` during signup

### 5. Authentication Endpoints

**Pattern**: Signup, signin, and signout endpoints

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from backend.db import get_db
from backend.middleware.jwt import verify_jwt_token, generate_jwt_token
from backend.services.auth_service import AuthService
from backend.schemas.requests import UserSignupRequest, UserSigninRequest
from backend.schemas.responses import AuthResponse

router = APIRouter(prefix="/api/auth", tags=["authentication"])
auth_service = AuthService()

@router.post("/signup", status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserSignupRequest,
    db: Session = Depends(get_db)
):
    """
    Create new user account and return JWT token.
    """
    try:
        # Create user
        user = auth_service.create_user(
            db,
            email=user_data.email,
            password=user_data.password,
            name=user_data.name
        )
        
        # Generate JWT token
        token = generate_jwt_token(user.id, user.email)
        
        return {
            "success": True,
            "data": {
                "token": token,
                "user": {
                    "id": user.id,
                    "email": user.email,
                    "name": user.name
                }
            }
        }
    
    except ValueError as e:
        # Email already exists or validation error
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create account"
        )

@router.post("/signin")
async def signin(
    credentials: UserSigninRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and return JWT token.
    """
    # Authenticate user
    user = auth_service.authenticate_user(
        db,
        email=credentials.email,
        password=credentials.password
    )
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    # Generate JWT token
    token = generate_jwt_token(user.id, user.email)
    
    return {
        "success": True,
        "data": {
            "token": token,
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name
            }
        }
    }

@router.post("/signout")
async def signout(
    current_user: Dict[str, str] = Depends(verify_jwt_token)
):
    """
    Sign out user (client-side token removal).
    Backend doesn't need to do anything for stateless JWT.
    """
    return {"success": True}
```

**Pattern Rules**:
- Signup returns 201 Created with token
- Signin returns 200 OK with token
- Signout returns 200 OK (stateless, no server action needed)
- Validate email uniqueness in signup
- Return 401 for invalid credentials
- Return 400 for validation errors
- Generate JWT token after successful authentication

### 6. Protected Route Pattern

**Pattern**: Apply JWT verification to all protected routes

```python
from fastapi import Depends
from backend.middleware.jwt import verify_jwt_token

@router.get("/{user_id}/tasks")
async def get_tasks(
    user_id: str,
    db: Session = Depends(get_db),
    current_user: Dict[str, str] = Depends(verify_jwt_token)  # JWT verification
):
    # Verify user_id
    if current_user["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="User ID mismatch")
    
    # Use user_id from JWT (not from path) for security
    tasks = task_service.get_tasks(db, current_user["user_id"])
    return {"success": True, "data": tasks}
```

**Pattern Rules**:
- Add `current_user: Dict = Depends(verify_jwt_token)` to all protected routes
- Verify user_id matches before processing
- Use user_id from JWT token (not path) for database queries
- Return 403 if user_id mismatch

### 7. Token Expiration Handling

**Pattern**: Handle expired tokens gracefully

```python
from jose import ExpiredSignatureError, JWTError

def verify_jwt_token(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> Dict[str, str]:
    token = credentials.credentials
    
    try:
        payload = jwt.decode(
            token,
            BETTER_AUTH_SECRET,
            algorithms=["HS256"]
        )
        # ... extract user info
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired. Please sign in again."
        )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

**Pattern Rules**:
- Catch `ExpiredSignatureError` specifically
- Return clear error message for expired tokens
- Return generic message for other JWT errors
- Client should redirect to login on 401

### 8. Environment Variable Configuration

**Pattern**: Load JWT secret from environment

```python
import os
from typing import Optional

BETTER_AUTH_SECRET = os.getenv("BETTER_AUTH_SECRET")

if not BETTER_AUTH_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is required")

JWT_EXPIRATION_DAYS = int(os.getenv("JWT_EXPIRATION_DAYS", "7"))
```

**Pattern Rules**:
- Use `BETTER_AUTH_SECRET` from environment (required)
- Use same secret as frontend (Better Auth)
- Validate secret exists at startup
- Use environment variable for expiration days (default 7)

## Steps for Adding JWT Protection to New Endpoint

1. **Add JWT Dependency**
   ```python
   current_user: Dict[str, str] = Depends(verify_jwt_token)
   ```

2. **Verify User ID**
   ```python
   if current_user["user_id"] != user_id:
       raise HTTPException(status_code=403, detail="User ID mismatch")
   ```

3. **Use JWT User ID**
   ```python
   # Use current_user["user_id"] for database queries
   tasks = task_service.get_tasks(db, current_user["user_id"])
   ```

## Common Patterns Summary

- ✅ Use Better Auth shared secret (BETTER_AUTH_SECRET)
- ✅ Verify JWT on every protected request
- ✅ Extract user_id from token (sub or user_id claim)
- ✅ Validate user_id matches URL path (403 if mismatch)
- ✅ Use user_id from JWT for database queries
- ✅ Return 401 for invalid/expired tokens
- ✅ Return 403 for user_id mismatch
- ✅ Hash passwords with bcrypt
- ✅ Generate tokens with 7-day expiration
- ✅ Use HS256 algorithm for JWT

