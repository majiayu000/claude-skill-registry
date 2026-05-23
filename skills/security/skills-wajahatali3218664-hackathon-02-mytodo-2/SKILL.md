---
name: better-auth-skill
description: Configure Better Auth with JWT for secure authentication
when-to-use: User signup, login, session management
---
# Better Auth Skill

## Instructions

This skill provides guidance for configuring Better Auth with JWT for secure user authentication.

### Project Structure
```
backend/
├── auth/
│   ├── __init__.py
│   ├── service.py          # Auth business logic
│   ├── dependencies.py     # FastAPI dependencies
│   ├── routes.py           # Auth endpoints
│   └── schemas.py          # Pydantic schemas
frontend/
└── src/
    ├── lib/
    │   └── auth.ts         # Frontend auth utilities
    └── hooks/
        └── useAuth.ts      # Auth state hook
```

### JWT Configuration

```python
# backend/auth/config.py
from pydantic_settings import BaseSettings
from datetime import timedelta
from typing import Optional

class AuthSettings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

auth_settings = AuthSettings()
```

### Better Auth Setup

```python
# backend/auth/service.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from models.user import User
from database import AsyncSessionLocal
from sqlalchemy import select
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token."""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        auth_settings.SECRET_KEY,
        algorithm=ALGORITHM
    )
    return encoded_jwt

def create_refresh_token(data: dict) -> str:
    """Create JWT refresh token."""
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(days=7)
    to_encode.update({"exp": expire, "type": "refresh"})
    return jwt.encode(to_encode, auth_settings.SECRET_KEY, algorithm=ALGORITHM)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash."""
    return pwd_context.verify(plain_password, hashed_password)

def hash_password(password: str) -> str:
    """Hash password for storage."""
    return pwd_context.hash(password)

async def authenticate_user(email: str, password: str) -> Optional[User]:
    """Authenticate user by email and password."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

async def get_user_by_email(email: str) -> Optional[User]:
    """Get user by email."""
    async with AsyncSessionLocal() as db:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        return result.scalar_one_or_none()

async def create_user(email: str, password: str, name: str) -> User:
    """Create new user."""
    async with AsyncSessionLocal() as db:
        hashed_password = hash_password(password)
        user = User(
            email=email,
            hashed_password=hashed_password,
            name=name
        )
        db.add(user)
        await db.commit()
        await db.refresh(user)
        return user
```

### Auth Dependencies

```python
# backend/auth/dependencies.py
from datetime import datetime
from typing import Optional
from jose import JWTError, jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models.user import User
from auth.service import oauth2_scheme, ALGORITHM, auth_settings

class TokenData:
    """Data extracted from JWT token."""
    email: Optional[str] = None
    user_id: Optional[int] = None

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    """Get current authenticated user from JWT token."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token,
            auth_settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception

        token_data = TokenData(email=email, user_id=payload.get("user_id"))
    except JWTError:
        raise credentials_exception

    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == token_data.email)
        )
        user = result.scalar_one_or_none()

        if user is None:
            raise credentials_exception

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="User account is disabled"
            )

        return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
) -> User:
    """Get current active user (alias for get_current_user)."""
    return current_user

def decode_token(token: str) -> TokenData:
    """Decode JWT token without raising exceptions."""
    try:
        payload = jwt.decode(
            token,
            auth_settings.SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        return TokenData(
            email=payload.get("sub"),
            user_id=payload.get("user_id")
        )
    except JWTError:
        return TokenData()
```

### Auth Schemas (Pydantic)

```python
# backend/auth/schemas.py
from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

# Request schemas
class UserCreate(BaseModel):
    """Schema for user registration."""
    email: EmailStr
    password: str = Field(..., min_length=8)
    name: str = Field(..., min_length=1, max_length=100)

class UserLogin(BaseModel):
    """Schema for user login."""
    email: EmailStr
    password: str

class TokenRefresh(BaseModel):
    """Schema for token refresh."""
    refresh_token: str

# Response schemas
class Token(BaseModel):
    """Schema for authentication tokens."""
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class TokenPayload(BaseModel):
    """Schema for token payload."""
    sub: str
    user_id: int
    exp: datetime

class UserResponse(BaseModel):
    """Schema for user response."""
    id: int
    email: str
    name: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    """Schema for authentication response."""
    user: UserResponse
    tokens: Token
```

### Auth Routes

```python
# backend/auth/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from auth.service import (
    authenticate_user,
    create_user,
    create_access_token,
    create_refresh_token,
    get_user_by_email,
)
from auth.schemas import (
    UserCreate,
    UserLogin,
    Token,
    UserResponse,
    AuthResponse,
    TokenRefresh,
)
from auth.dependencies import get_current_user
from models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=AuthResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    db: AsyncSession = Depends(get_db)
):
    """Register a new user."""
    # Check if user exists
    existing_user = await get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Create user
    user = await create_user(
        email=user_data.email,
        password=user_data.password,
        name=user_data.name
    )

    # Create tokens
    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=Token(access_token=access_token, refresh_token=refresh_token)
    )

@router.post("/login", response_model=AuthResponse)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """Login with email and password (OAuth2 compatible)."""
    user = await authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=Token(access_token=access_token, refresh_token=refresh_token)
    )

@router.post("/login/json", response_model=AuthResponse)
async def login_json(
    credentials: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    """Login with JSON body."""
    user = await authenticate_user(credentials.email, credentials.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )
    refresh_token = create_refresh_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return AuthResponse(
        user=UserResponse.model_validate(user),
        tokens=Token(access_token=access_token, refresh_token=refresh_token)
    )

@router.post("/refresh", response_model=Token)
async def refresh_token(
    refresh_data: TokenRefresh,
    db: AsyncSession = Depends(get_db)
):
    """Refresh access token using refresh token."""
    from auth.service import decode_token, get_user_by_email

    token_data = decode_token(refresh_data.refresh_token)
    if not token_data.email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    user = await get_user_by_email(token_data.email)
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or inactive"
        )

    access_token = create_access_token(
        data={"sub": user.email, "user_id": user.id}
    )

    return Token(access_token=access_token, refresh_token=refresh_data.refresh_token)

@router.get("/me", response_model=UserResponse)
async def get_me(current_user: User = Depends(get_current_user)):
    """Get current user profile."""
    return UserResponse.model_validate(current_user)

@router.post("/logout")
async def logout():
    """Logout (client-side token removal)."""
    return {"message": "Successfully logged out"}
```

## Examples

### Frontend Auth Hook

```typescript
// src/hooks/useAuth.ts
'use client'

import { createContext, useContext, useState, useEffect, ReactNode } from 'react'

interface User {
  id: number
  email: string
  name: string
  is_active: boolean
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (email: string, password: string) => Promise<void>
  register: (email: string, password: string, name: string) => Promise<void>
  logout: () => void
  refreshToken: () => Promise<void>
}

const AuthContext = createContext<AuthContextType | null>(null)

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  // Check for existing session on mount
  useEffect(() => {
    const token = localStorage.getItem('access_token')
    if (token) {
      fetchUserProfile()
    } else {
      setIsLoading(false)
    }
  }, [])

  const fetchUserProfile = async () => {
    try {
      const res = await fetch('/api/v1/auth/me', {
        headers: {
          'Authorization': `Bearer ${localStorage.getItem('access_token')}`
        }
      })
      if (res.ok) {
        const userData = await res.json()
        setUser(userData)
      } else {
        localStorage.removeItem('access_token')
        localStorage.removeItem('refresh_token')
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
    } finally {
      setIsLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    const res = await fetch('/api/v1/auth/login/json', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password })
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || 'Login failed')
    }

    const data = await res.json()
    localStorage.setItem('access_token', data.tokens.access_token)
    localStorage.setItem('refresh_token', data.tokens.refresh_token)
    setUser(data.user)
  }

  const register = async (email: string, password: string, name: string) => {
    const res = await fetch('/api/v1/auth/register', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password, name })
    })

    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || 'Registration failed')
    }

    const data = await res.json()
    localStorage.setItem('access_token', data.tokens.access_token)
    localStorage.setItem('refresh_token', data.tokens.refresh_token)
    setUser(data.user)
  }

  const logout = () => {
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    setUser(null)
  }

  const refreshToken = async () => {
    const refresh_token = localStorage.getItem('refresh_token')
    if (!refresh_token) {
      logout()
      return
    }

    const res = await fetch('/api/v1/auth/refresh', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ refresh_token })
    })

    if (!res.ok) {
      logout()
      return
    }

    const data = await res.json()
    localStorage.setItem('access_token', data.access_token)
  }

  return (
    <AuthContext.Provider value={{ user, isLoading, login, register, logout, refreshToken }}>
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}
```

### Protected Route

```typescript
// src/components/ProtectedRoute.tsx
'use client'

import { useAuth } from '@/hooks/useAuth'
import { useRouter } from 'next/navigation'
import { useEffect } from 'react'

export function ProtectedRoute({ children }: { children: ReactNode }) {
  const { user, isLoading } = useAuth()
  const router = useRouter()

  useEffect(() => {
    if (!isLoading && !user) {
      router.push('/auth/login')
    }
  }, [user, isLoading, router])

  if (isLoading) {
    return <div>Loading...</div>
  }

  if (!user) {
    return null
  }

  return children
}
```

### API Client with Auth

```typescript
// src/lib/api.ts
const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

class ApiClient {
  private getToken(): string | null {
    return localStorage.getItem('access_token')
  }

  private async request<T>(
    endpoint: string,
    options: RequestInit = {}
  ): Promise<T> {
    const token = this.getToken()

    const headers: HeadersInit = {
      'Content-Type': 'application/json',
      ...(token ? { 'Authorization': `Bearer ${token}` } : {}),
      ...options.headers,
    }

    const response = await fetch(`${API_BASE}${endpoint}`, {
      ...options,
      headers,
    })

    if (response.status === 401) {
      // Try to refresh token
      const refreshed = await this.refresh()
      if (refreshed) {
        // Retry request
        return this.request(endpoint, options)
      }
      // Redirect to login
      window.location.href = '/auth/login'
      throw new Error('Unauthorized')
    }

    if (!response.ok) {
      const error = await response.json().catch(() => ({}))
      throw new Error(error.detail || 'Request failed')
    }

    return response.json()
  }

  private async refresh(): Promise<boolean> {
    try {
      const refresh_token = localStorage.getItem('refresh_token')
      if (!refresh_token) return false

      const res = await fetch(`${API_BASE}/api/v1/auth/refresh`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ refresh_token })
      })

      if (!res.ok) return false

      const data = await res.json()
      localStorage.setItem('access_token', data.access_token)
      return true
    } catch {
      return false
    }
  }

  // API methods
  async get<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'GET' })
  }

  async post<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'POST',
      body: JSON.stringify(data)
    })
  }

  async put<T>(endpoint: string, data: unknown): Promise<T> {
    return this.request<T>(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data)
    })
  }

  async delete<T>(endpoint: string): Promise<T> {
    return this.request<T>(endpoint, { method: 'DELETE' })
  }
}

export const api = new ApiClient()
```
