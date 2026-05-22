---
name: fastapi-development
description: Build high-performance FastAPI applications with async routes, validation, dependency injection, security, and automatic API documentation. Use when developing modern Python APIs with async support, automatic OpenAPI documentation, and high performance requirements.
---

# FastAPI Development

## Overview

Create fast, modern Python APIs using FastAPI with async/await support, automatic API documentation, type validation using Pydantic, dependency injection, JWT authentication, and SQLAlchemy ORM integration.

## When to Use

- Building high-performance Python REST APIs
- Creating async API endpoints
- Implementing automatic OpenAPI/Swagger documentation
- Leveraging Python type hints for validation
- Building microservices with async support
- Integrating Pydantic for data validation

## Instructions

### 1. **FastAPI Application Setup**

```python
# main.py
from fastapi import FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI instance
app = FastAPI(
    title="API Service",
    description="A modern FastAPI application",
    version="1.0.0",
    docs_url="/api/docs",
    openapi_url="/api/openapi.json"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Lifespan events
@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Application startup")
    yield
    logger.info("Application shutdown")

app = FastAPI(lifespan=lifespan)

# Health check
@app.get("/health", tags=["Health"])
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0"
    }

# Exception handler
@app.exception_handler(ValueError)
async def value_error_handler(request, exc):
    return HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=str(exc)
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### 2. **Pydantic Models for Validation**

```python
# models.py
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Optional
from datetime import datetime
from enum import Enum

class UserRole(str, Enum):
    ADMIN = "admin"
    USER = "user"

class UserBase(BaseModel):
    email: EmailStr = Field(..., description="User email address")
    first_name: str = Field(..., min_length=1, max_length=100)
    last_name: str = Field(..., min_length=1, max_length=100)

    @field_validator('email')
    @classmethod
    def email_lowercase(cls, v):
        return v.lower()

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, max_length=255)

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserResponse(UserBase):
    id: str = Field(..., description="User ID")
    role: UserRole = UserRole.USER
    created_at: datetime
    updated_at: datetime
    is_active: bool = True

    class Config:
        from_attributes = True

class UserUpdate(BaseModel):
    first_name: Optional[str] = Field(None, min_length=1, max_length=100)
    last_name: Optional[str] = Field(None, min_length=1, max_length=100)

class PostBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=255)
    content: str = Field(..., min_length=1)
    published: bool = False

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id: str
    author_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    limit: int = Field(20, ge=1, le=100)

class PaginatedResponse(BaseModel):
    data: list
    pagination: dict
```

### 3. **Async Database Models and Queries**

```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy import Column, String, Text, Boolean, DateTime, ForeignKey, Enum, Index
from datetime import datetime
import uuid
import os

DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

Base = declarative_base()

# Models
class User(Base):
    __tablename__ = "users"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    first_name = Column(String(100))
    last_name = Column(String(100))
    role = Column(String(20), default="user", index=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        Index('idx_email_active', 'email', 'is_active'),
    )

class Post(Base):
    __tablename__ = "posts"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False, index=True)
    content = Column(Text, nullable=False)
    published = Column(Boolean, default=False)
    author_id = Column(String(36), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

# Database initialization
async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_db() -> AsyncSession:
    async with async_session() as session:
        yield session
```

### 4. **Security and JWT Authentication**

```python
# security.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthCredentials
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
import os

SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
security = HTTPBearer()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(user_id: str, expires_delta: Optional[timedelta] = None) -> str:
    if expires_delta is None:
        expires_delta = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS)

    expire = datetime.utcnow() + expires_delta
    to_encode = {"sub": user_id, "exp": expire}
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(credentials: HTTPAuthCredentials = Depends(security)):
    try:
        payload = jwt.decode(credentials.credentials, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

    return user_id

async def get_admin_user(user_id: str = Depends(get_current_user)):
    # Add role check logic
    return user_id
```

### 5. **Service Layer for Business Logic**

```python
# services.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from database import User, Post
from models import UserCreate, UserUpdate, PostCreate
from security import hash_password, verify_password
from typing import Optional

class UserService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_user(self, user_data: UserCreate) -> User:
        db_user = User(
            email=user_data.email,
            password_hash=hash_password(user_data.password),
            first_name=user_data.first_name,
            last_name=user_data.last_name
        )
        self.db.add(db_user)
        await self.db.commit()
        await self.db.refresh(db_user)
        return db_user

    async def get_user_by_email(self, email: str) -> Optional[User]:
        stmt = select(User).where(User.email == email.lower())
        result = await self.db.execute(stmt)
        return result.scalar_one_or_none()

    async def get_user_by_id(self, user_id: str) -> Optional[User]:
        return await self.db.get(User, user_id)

    async def authenticate_user(self, email: str, password: str) -> Optional[User]:
        user = await self.get_user_by_email(email)
        if user and verify_password(password, user.password_hash):
            return user
        return None

    async def update_user(self, user_id: str, user_data: UserUpdate) -> Optional[User]:
        user = await self.get_user_by_id(user_id)
        if not user:
            return None

        update_data = user_data.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(user, field, value)

        await self.db.commit()
        await self.db.refresh(user)
        return user

    async def list_users(self, skip: int = 0, limit: int = 20) -> tuple:
        stmt = select(User).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        users = result.scalars().all()

        count_stmt = select(User)
        count_result = await self.db.execute(count_stmt)
        total = len(count_result.scalars().all())

        return users, total

class PostService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_post(self, author_id: str, post_data: PostCreate) -> Post:
        db_post = Post(
            title=post_data.title,
            content=post_data.content,
            author_id=author_id,
            published=post_data.published
        )
        self.db.add(db_post)
        await self.db.commit()
        await self.db.refresh(db_post)
        return db_post

    async def get_published_posts(self, skip: int = 0, limit: int = 20) -> tuple:
        stmt = select(Post).where(Post.published == True).offset(skip).limit(limit)
        result = await self.db.execute(stmt)
        posts = result.scalars().all()
        return posts, len(posts)
```

### 6. **API Routes with Async Endpoints**

```python
# routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession
from database import get_db
from models import UserCreate, UserUpdate, UserResponse, PostCreate, PostResponse
from security import get_current_user, create_access_token
from services import UserService, PostService

router = APIRouter(prefix="/api", tags=["users"])

@router.post("/auth/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    existing_user = await user_service.get_user_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered"
        )
    user = await user_service.create_user(user_data)
    return user

@router.post("/auth/login")
async def login(email: str, password: str, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.authenticate_user(email, password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials"
        )
    access_token = create_access_token(user.id)
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/users", response_model=list[UserResponse])
async def list_users(
    skip: int = 0,
    limit: int = 20,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    users, total = await user_service.list_users(skip, limit)
    return users

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: str,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user_service = UserService(db)
    user = await user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.patch("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: str,
    user_data: UserUpdate,
    current_user: str = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    if user_id != current_user:
        raise HTTPException(status_code=403, detail="Cannot update other users")

    user_service = UserService(db)
    user = await user_service.update_user(user_id, user_data)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

## Best Practices

### ✅ DO
- Use async/await for I/O operations
- Leverage Pydantic for validation
- Use dependency injection for services
- Implement proper error handling with HTTPException
- Use type hints for automatic OpenAPI documentation
- Create service layers for business logic
- Implement authentication on protected routes
- Use environment variables for configuration
- Return appropriate HTTP status codes
- Document endpoints with docstrings and tags

### ❌ DON'T
- Use synchronous database operations
- Trust user input without validation
- Store secrets in code
- Ignore type hints
- Return database models in responses
- Implement authentication in route handlers
- Use mutable default arguments
- Forget to validate query parameters
- Expose stack traces in production

## Complete Example

```python
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from database import get_db, User

app = FastAPI()

class UserResponse(BaseModel):
    id: str
    email: str

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404)
    return user

@app.post("/users")
async def create_user(email: str, db: AsyncSession = Depends(get_db)):
    user = User(email=email)
    db.add(user)
    await db.commit()
    return {"id": user.id, "email": user.email}
```
