---
name: better-auth-integration
description: Integrate Better Auth for JWT-based authentication in Next.js frontend and FastAPI backend. Handles signup, login, logout, token management, and protected routes. Use when implementing authentication for Phase 2.
allowed-tools: Bash, Write, Read, Edit
---

# Better Auth Integration

Quick reference for integrating Better Auth with Next.js frontend and FastAPI backend for the Todo Web Application Phase 2.

## Overview

Better Auth provides:
- JWT-based authentication
- Social OAuth providers (optional)
- Session management
- Secure cookie handling
- Type-safe client

## Architecture

```
┌─────────────────────┐     ┌─────────────────────┐
│   Next.js Frontend  │     │   FastAPI Backend   │
│                     │     │                     │
│  ┌───────────────┐  │     │  ┌───────────────┐  │
│  │ Better Auth   │  │────▶│  │ JWT Validator │  │
│  │   Client      │  │     │  │  Middleware   │  │
│  └───────────────┘  │     │  └───────────────┘  │
│         │           │     │         │           │
│  ┌───────────────┐  │     │  ┌───────────────┐  │
│  │ Auth Context  │  │     │  │ Protected     │  │
│  │   Provider    │  │     │  │ Routes        │  │
│  └───────────────┘  │     │  └───────────────┘  │
└─────────────────────┘     └─────────────────────┘
```

## Frontend Setup (Next.js)

### 1. Install Dependencies

```bash
cd frontend
npm install better-auth @better-auth/client
```

### 2. Environment Variables

Create `frontend/.env.local`:

```env
# Better Auth Configuration
BETTER_AUTH_SECRET=your-super-secret-key-min-32-chars
NEXT_PUBLIC_API_URL=http://localhost:8000

# NextAuth URL (for local development)
NEXTAUTH_URL=http://localhost:3000
```

### 3. Auth Configuration

Create `frontend/src/lib/auth.ts`:

```typescript
import { createAuthClient } from "@better-auth/client";

// Create auth client
export const authClient = createAuthClient({
  baseURL: process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000",
});

// Export commonly used methods
export const { signIn, signUp, signOut, useSession, getSession } = authClient;
```

### 4. Auth Provider

Create `frontend/src/components/providers/auth-provider.tsx`:

```typescript
"use client";

import { createContext, useContext, useEffect, useState, ReactNode } from "react";
import { authClient } from "@/lib/auth";

interface User {
  id: string;
  email: string;
  name?: string;
}

interface AuthContextType {
  user: User | null;
  isLoading: boolean;
  isAuthenticated: boolean;
  signIn: (email: string, password: string) => Promise<void>;
  signUp: (email: string, password: string, name?: string) => Promise<void>;
  signOut: () => Promise<void>;
  getToken: () => Promise<string | null>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<User | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    // Check for existing session on mount
    checkSession();
  }, []);

  const checkSession = async () => {
    try {
      const session = await authClient.getSession();
      if (session?.user) {
        setUser(session.user);
      }
    } catch (error) {
      console.error("Session check failed:", error);
    } finally {
      setIsLoading(false);
    }
  };

  const signIn = async (email: string, password: string) => {
    setIsLoading(true);
    try {
      const result = await authClient.signIn.email({
        email,
        password,
      });
      if (result.user) {
        setUser(result.user);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const signUp = async (email: string, password: string, name?: string) => {
    setIsLoading(true);
    try {
      const result = await authClient.signUp.email({
        email,
        password,
        name: name || email.split("@")[0],
      });
      if (result.user) {
        setUser(result.user);
      }
    } finally {
      setIsLoading(false);
    }
  };

  const signOut = async () => {
    setIsLoading(true);
    try {
      await authClient.signOut();
      setUser(null);
    } finally {
      setIsLoading(false);
    }
  };

  const getToken = async (): Promise<string | null> => {
    const session = await authClient.getSession();
    return session?.token || null;
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        isAuthenticated: !!user,
        signIn,
        signUp,
        signOut,
        getToken,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }
  return context;
}
```

### 5. Protected Route Middleware

Create `frontend/src/middleware.ts`:

```typescript
import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

// Routes that require authentication
const protectedRoutes = ["/tasks", "/dashboard", "/settings"];

// Routes that should redirect to dashboard if authenticated
const authRoutes = ["/login", "/signup"];

export function middleware(request: NextRequest) {
  const token = request.cookies.get("auth-token")?.value;
  const { pathname } = request.nextUrl;

  // Check if accessing protected route without token
  if (protectedRoutes.some((route) => pathname.startsWith(route))) {
    if (!token) {
      const loginUrl = new URL("/login", request.url);
      loginUrl.searchParams.set("redirect", pathname);
      return NextResponse.redirect(loginUrl);
    }
  }

  // Redirect authenticated users away from auth pages
  if (authRoutes.some((route) => pathname.startsWith(route))) {
    if (token) {
      return NextResponse.redirect(new URL("/tasks", request.url));
    }
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/tasks/:path*", "/dashboard/:path*", "/login", "/signup"],
};
```

### 6. Login Form Component

Create `frontend/src/components/auth/login-form.tsx`:

```typescript
"use client";

import { useState } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { useAuth } from "@/components/providers/auth-provider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import Link from "next/link";

export function LoginForm() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const { signIn } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const redirectTo = searchParams.get("redirect") || "/tasks";

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      await signIn(email, password);
      router.push(redirectTo);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Welcome Back</CardTitle>
        <CardDescription>Sign in to your account to continue</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              minLength={8}
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Signing in..." : "Sign In"}
          </Button>
          <p className="text-sm text-muted-foreground">
            Don't have an account?{" "}
            <Link href="/signup" className="text-primary hover:underline">
              Sign up
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
```

### 7. Signup Form Component

Create `frontend/src/components/auth/signup-form.tsx`:

```typescript
"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/components/providers/auth-provider";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Alert, AlertDescription } from "@/components/ui/alert";
import Link from "next/link";

export function SignupForm() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  
  const { signUp } = useAuth();
  const router = useRouter();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (password !== confirmPassword) {
      setError("Passwords do not match");
      return;
    }

    if (password.length < 8) {
      setError("Password must be at least 8 characters");
      return;
    }

    setIsLoading(true);

    try {
      await signUp(email, password, name);
      router.push("/tasks");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Signup failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <Card className="w-full max-w-md">
      <CardHeader>
        <CardTitle>Create Account</CardTitle>
        <CardDescription>Sign up to start managing your tasks</CardDescription>
      </CardHeader>
      <form onSubmit={handleSubmit}>
        <CardContent className="space-y-4">
          {error && (
            <Alert variant="destructive">
              <AlertDescription>{error}</AlertDescription>
            </Alert>
          )}
          <div className="space-y-2">
            <Label htmlFor="name">Name</Label>
            <Input
              id="name"
              type="text"
              placeholder="John Doe"
              value={name}
              onChange={(e) => setName(e.target.value)}
              disabled={isLoading}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="email">Email</Label>
            <Input
              id="email"
              type="email"
              placeholder="you@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
              disabled={isLoading}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
              disabled={isLoading}
              minLength={8}
            />
          </div>
          <div className="space-y-2">
            <Label htmlFor="confirmPassword">Confirm Password</Label>
            <Input
              id="confirmPassword"
              type="password"
              placeholder="••••••••"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              required
              disabled={isLoading}
              minLength={8}
            />
          </div>
        </CardContent>
        <CardFooter className="flex flex-col space-y-4">
          <Button type="submit" className="w-full" disabled={isLoading}>
            {isLoading ? "Creating account..." : "Create Account"}
          </Button>
          <p className="text-sm text-muted-foreground">
            Already have an account?{" "}
            <Link href="/login" className="text-primary hover:underline">
              Sign in
            </Link>
          </p>
        </CardFooter>
      </form>
    </Card>
  );
}
```

## Backend Setup (FastAPI)

### 1. Install Dependencies

```bash
cd backend
uv add python-jose[cryptography] passlib[bcrypt] pydantic-settings
```

### 2. Environment Variables

Add to `backend/.env`:

```env
# JWT Configuration
JWT_SECRET_KEY=your-super-secret-key-min-32-chars
JWT_ALGORITHM=HS256
JWT_ACCESS_TOKEN_EXPIRE_MINUTES=10080  # 7 days

# Security
CORS_ORIGINS=http://localhost:3000
```

### 3. Auth Configuration

Create `backend/src/config.py`:

```python
from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    database_url: str
    
    # JWT
    jwt_secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_access_token_expire_minutes: int = 10080  # 7 days
    
    # Security
    cors_origins: str = "http://localhost:3000"
    
    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",")]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()
```

### 4. JWT Utilities

Create `backend/src/utils/jwt.py`:

```python
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel

from src.config import get_settings

settings = get_settings()

# Password hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class TokenPayload(BaseModel):
    """JWT token payload."""
    sub: str  # user_id
    email: str
    exp: datetime
    iat: datetime


class TokenData(BaseModel):
    """Decoded token data."""
    user_id: str
    email: str


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against its hash."""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Hash a password."""
    return pwd_context.hash(password)


def create_access_token(user_id: str, email: str, expires_delta: Optional[timedelta] = None) -> str:
    """Create a JWT access token."""
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.jwt_access_token_expire_minutes)
    
    payload = {
        "sub": user_id,
        "email": email,
        "exp": expire,
        "iat": datetime.utcnow(),
    }
    
    encoded_jwt = jwt.encode(
        payload,
        settings.jwt_secret_key,
        algorithm=settings.jwt_algorithm
    )
    return encoded_jwt


def decode_access_token(token: str) -> Optional[TokenData]:
    """Decode and validate a JWT access token."""
    try:
        payload = jwt.decode(
            token,
            settings.jwt_secret_key,
            algorithms=[settings.jwt_algorithm]
        )
        user_id: str = payload.get("sub")
        email: str = payload.get("email")
        
        if user_id is None or email is None:
            return None
            
        return TokenData(user_id=user_id, email=email)
    except JWTError:
        return None
```

### 5. Auth Middleware

Create `backend/src/middleware/auth.py`:

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional
from pydantic import BaseModel

from src.utils.jwt import decode_access_token, TokenData

security = HTTPBearer()


class CurrentUser(BaseModel):
    """Current authenticated user."""
    id: str
    email: str


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> CurrentUser:
    """
    Dependency to get the current authenticated user from JWT token.
    
    Usage:
        @router.get("/protected")
        async def protected_route(current_user: CurrentUser = Depends(get_current_user)):
            return {"user_id": current_user.id}
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    token = credentials.credentials
    token_data = decode_access_token(token)
    
    if token_data is None:
        raise credentials_exception
    
    return CurrentUser(id=token_data.user_id, email=token_data.email)


async def get_current_user_optional(
    credentials: Optional[HTTPAuthorizationCredentials] = Depends(
        HTTPBearer(auto_error=False)
    )
) -> Optional[CurrentUser]:
    """
    Optional dependency - returns None if no valid token provided.
    
    Usage for routes that work with or without authentication:
        @router.get("/public-or-private")
        async def route(current_user: Optional[CurrentUser] = Depends(get_current_user_optional)):
            if current_user:
                return {"authenticated": True, "user_id": current_user.id}
            return {"authenticated": False}
    """
    if credentials is None:
        return None
    
    token_data = decode_access_token(credentials.credentials)
    if token_data is None:
        return None
    
    return CurrentUser(id=token_data.user_id, email=token_data.email)


def verify_user_access(current_user: CurrentUser, resource_user_id: str) -> None:
    """
    Verify that the current user has access to a resource owned by resource_user_id.
    Raises 403 Forbidden if access is denied.
    
    Usage:
        @router.get("/users/{user_id}/tasks")
        async def get_user_tasks(
            user_id: str,
            current_user: CurrentUser = Depends(get_current_user)
        ):
            verify_user_access(current_user, user_id)
            # ... fetch tasks
    """
    if current_user.id != resource_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied to this resource"
        )
```

### 6. Auth Schemas

Create `backend/src/schemas/auth.py`:

```python
from pydantic import BaseModel, EmailStr, Field


class UserSignup(BaseModel):
    """Request schema for user signup."""
    email: EmailStr
    password: str = Field(min_length=8, max_length=100)
    name: str = Field(default="", max_length=100)


class UserLogin(BaseModel):
    """Request schema for user login."""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """Response schema for authentication."""
    access_token: str
    token_type: str = "bearer"
    user: "UserResponse"


class UserResponse(BaseModel):
    """Response schema for user data."""
    id: str
    email: str
    name: str
    
    class Config:
        from_attributes = True


class AuthError(BaseModel):
    """Error response for authentication failures."""
    detail: str
```

### 7. User Model

Create `backend/src/models/user.py`:

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel
import uuid


class UserBase(SQLModel):
    """Base user model."""
    email: str = Field(unique=True, index=True, max_length=255)
    name: str = Field(default="", max_length=100)


class User(UserBase, table=True):
    """User database model."""
    __tablename__ = "users"
    
    id: str = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    """Schema for creating a user (internal use)."""
    hashed_password: str
```

### 8. Auth Router

Create `backend/src/routers/auth.py`:

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from src.database import get_session
from src.models.user import User, UserCreate
from src.schemas.auth import UserSignup, UserLogin, TokenResponse, UserResponse
from src.utils.jwt import get_password_hash, verify_password, create_access_token
from src.middleware.auth import get_current_user, CurrentUser

router = APIRouter(prefix="/api/auth", tags=["authentication"])


@router.post("/signup", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def signup(
    user_data: UserSignup,
    session: Session = Depends(get_session)
):
    """
    Create a new user account.
    
    - **email**: Valid email address (must be unique)
    - **password**: Minimum 8 characters
    - **name**: Optional display name
    """
    # Check if user already exists
    existing_user = session.exec(
        select(User).where(User.email == user_data.email)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    user = User(
        email=user_data.email,
        name=user_data.name or user_data.email.split("@")[0],
        hashed_password=hashed_password
    )
    
    session.add(user)
    session.commit()
    session.refresh(user)
    
    # Generate token
    access_token = create_access_token(user_id=user.id, email=user.email)
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(id=user.id, email=user.email, name=user.name)
    )


@router.post("/login", response_model=TokenResponse)
async def login(
    credentials: UserLogin,
    session: Session = Depends(get_session)
):
    """
    Authenticate user and return JWT token.
    
    - **email**: Registered email address
    - **password**: Account password
    """
    # Find user
    user = session.exec(
        select(User).where(User.email == credentials.email)
    ).first()
    
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is disabled"
        )
    
    # Generate token
    access_token = create_access_token(user_id=user.id, email=user.email)
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(id=user.id, email=user.email, name=user.name)
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: CurrentUser = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get current authenticated user's information.
    
    Requires valid JWT token in Authorization header.
    """
    user = session.get(User, current_user.id)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return UserResponse(id=user.id, email=user.email, name=user.name)


@router.post("/logout")
async def logout(current_user: CurrentUser = Depends(get_current_user)):
    """
    Logout current user.
    
    Note: JWT tokens are stateless, so this endpoint is mainly for
    client-side cleanup. The token will still be valid until expiration.
    For production, consider implementing token blacklisting.
    """
    return {"message": "Successfully logged out"}
```

### 9. API Client with Auth

Create `frontend/src/lib/api.ts`:

```typescript
import { authClient } from "./auth";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

interface ApiOptions extends RequestInit {
  requireAuth?: boolean;
}

class ApiClient {
  private baseUrl: string;

  constructor(baseUrl: string) {
    this.baseUrl = baseUrl;
  }

  private async getAuthHeaders(): Promise<HeadersInit> {
    const session = await authClient.getSession();
    if (session?.token) {
      return {
        Authorization: `Bearer ${session.token}`,
      };
    }
    return {};
  }

  async request<T>(endpoint: string, options: ApiOptions = {}): Promise<T> {
    const { requireAuth = true, ...fetchOptions } = options;

    const headers: HeadersInit = {
      "Content-Type": "application/json",
      ...(requireAuth ? await this.getAuthHeaders() : {}),
      ...fetchOptions.headers,
    };

    const response = await fetch(`${this.baseUrl}${endpoint}`, {
      ...fetchOptions,
      headers,
    });

    if (!response.ok) {
      const error = await response.json().catch(() => ({ detail: "Request failed" }));
      throw new Error(error.detail || `HTTP ${response.status}`);
    }

    return response.json();
  }

  // Task API methods
  async getTasks(userId: string) {
    return this.request<Task[]>(`/api/${userId}/tasks`);
  }

  async createTask(userId: string, data: CreateTaskInput) {
    return this.request<Task>(`/api/${userId}/tasks`, {
      method: "POST",
      body: JSON.stringify(data),
    });
  }

  async updateTask(userId: string, taskId: number, data: UpdateTaskInput) {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}`, {
      method: "PUT",
      body: JSON.stringify(data),
    });
  }

  async toggleTaskComplete(userId: string, taskId: number) {
    return this.request<Task>(`/api/${userId}/tasks/${taskId}/complete`, {
      method: "PATCH",
    });
  }

  async deleteTask(userId: string, taskId: number) {
    return this.request<void>(`/api/${userId}/tasks/${taskId}`, {
      method: "DELETE",
    });
  }
}

export const api = new ApiClient(API_BASE_URL);

// Type definitions
export interface Task {
  id: number;
  user_id: string;
  title: string;
  description?: string;
  completed: boolean;
  priority: "low" | "medium" | "high";
  due_date?: string;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskInput {
  title: string;
  description?: string;
  priority?: "low" | "medium" | "high";
  due_date?: string;
}

export interface UpdateTaskInput {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: "low" | "medium" | "high";
  due_date?: string;
}
```

## Security Best Practices

### 1. Password Requirements
- Minimum 8 characters
- Use bcrypt hashing with salt
- Never store plain text passwords

### 2. JWT Security
- Use strong secret key (min 32 characters)
- Set reasonable expiration (7 days)
- Validate token on every protected request
- Use HTTPS in production

### 3. User Isolation
- Always verify user owns the resource
- Use `verify_user_access()` helper
- Never expose other users' data

### 4. Input Validation
- Use Pydantic for request validation
- Sanitize all inputs
- Limit field lengths

### 5. Error Handling
- Don't expose internal errors
- Use generic error messages for auth failures
- Log detailed errors server-side

## Testing Authentication

### Backend Tests

```python
import pytest
from fastapi.testclient import TestClient

def test_signup_success(client):
    response = client.post("/api/auth/signup", json={
        "email": "test@example.com",
        "password": "password123",
        "name": "Test User"
    })
    assert response.status_code == 201
    data = response.json()
    assert "access_token" in data
    assert data["user"]["email"] == "test@example.com"

def test_login_success(client, test_user):
    response = client.post("/api/auth/login", json={
        "email": test_user.email,
        "password": "password123"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_protected_route_without_token(client):
    response = client.get("/api/test-user/tasks")
    assert response.status_code == 401
```

## References

- [Better Auth Documentation](https://better-auth.com/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Phase 2 Constitution](../../constitution-prompt-phase-2.md)
- [Phase 2 Specification](../../spec-prompt-phase-2.md)
