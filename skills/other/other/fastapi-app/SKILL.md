---
name: fastapi-app
description: |
  Use when creating FastAPI backend applications - route handlers, dependencies, CORS config, or Pydantic models.
  NOT when frontend logic, non-Python backends, or unrelated server-side code.
  Triggers: "FastAPI", "student endpoint", "API route", "dependency injection", "CORS", "Pydantic model".
---

# FastAPI Application Skill

## Overview

Expert guidance for building FastAPI backend applications with route decorators, dependency injection, CORS configuration, and Pydantic v2 validation. Supports ERP endpoints for students, fees, attendance, and authentication.

## When This Skill Applies

This skill triggers when users request:
- **App Setup**: "Create FastAPI app", "Initialize FastAPI", "Lifespan events"
- **Routes**: "Student endpoint", "API route", "GET/POST handler", "APIRouter"
- **Dependencies**: "DB dependency", "Auth dependency", "Depends()", "JWT auth"
- **CORS**: "CORS enable frontend", "Cross-origin config", "credentials"
- **Models**: "Pydantic model", "Student schema", "Fee validation"

## Core Rules

### 1. Init: FastAPI App and Lifespan

```python
# main.py
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import students, fees, attendance, auth
from dependencies.database import get_db
from dependencies.auth import get_current_user
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    logger.info("Starting up FastAPI application...")
    yield
    # Shutdown
    logger.info("Shutting down FastAPI application...")

app = FastAPI(
    title="ERP API",
    description="Educational Resource Planning API",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers with prefix and tags
app.include_router(
    auth.router,
    prefix="/api/v1/auth",
    tags=["Authentication"],
)

app.include_router(
    students.router,
    prefix="/api/v1/students",
    tags=["Students"],
    dependencies=[Depends(get_current_user)],
)

app.include_router(
    fees.router,
    prefix="/api/v1/fees",
    tags=["Fees"],
    dependencies=[Depends(get_current_user)],
)

app.include_router(
    attendance.router,
    prefix="/api/v1/attendance",
    tags=["Attendance"],
    dependencies=[Depends(get_current_user)],
)
```

**Requirements:**
- Use FastAPI() with lifespan context manager
- Configure CORS for frontend origins
- Include routers with APIRouter
- Set up logging for production
- Enable Swagger docs at /docs

### 2. Routes: APIRouter with Tags and Responses

```python
# routers/students.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field

from dependencies.database import get_db
from dependencies.auth import get_current_user, get_admin_user
from models.student import Student as StudentModel
from schemas.student import StudentCreate, StudentUpdate, StudentResponse

router = APIRouter()

@router.get("/", response_model=List[StudentResponse])
async def get_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Get all students with pagination"""
    students = await db.execute(
        select(StudentModel)
        .offset(skip)
        .limit(limit)
    )
    return students.scalars().all()

@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Get a single student by ID"""
    student = await db.execute(
        select(StudentModel).where(StudentModel.id == student_id)
    )
    student = student.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )
    return student

@router.post("/", response_model=StudentResponse, status_code=status.HTTP_201_CREATED)
async def create_student(
    student_data: StudentCreate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user),
):
    """Create a new student"""
    # Check if email exists
    existing = await db.execute(
        select(StudentModel).where(StudentModel.email == student_data.email)
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    student = StudentModel(**student_data.model_dump())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student

@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: str,
    student_data: StudentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user),
):
    """Update a student"""
    student = await db.execute(
        select(StudentModel).where(StudentModel.id == student_id)
    )
    student = student.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    update_data = student_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)

    await db.commit()
    await db.refresh(student)
    return student

@router.delete("/{student_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_student(
    student_id: str,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_admin_user),
):
    """Delete a student"""
    student = await db.execute(
        select(StudentModel).where(StudentModel.id == student_id)
    )
    student = student.scalar_one_or_none()

    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found"
        )

    await db.delete(student)
    await db.commit()
```

**Requirements:**
- Use APIRouter with prefix and tags
- Response models with Pydantic schemas
- Proper HTTP status codes (200, 201, 204, 404, 400)
- Dependencies for auth and DB
- Pagination with skip/limit

### 3. Dependencies: Auth and DB Sessions

```python
# dependencies/database.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from databases import Database
import os

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://user:password@localhost:5432/erp_db"
)

engine = create_async_engine(DATABASE_URL, echo=True)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)

async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()

async def init_db():
    """Initialize database tables"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
```

```python
# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError, jwt
from datetime import datetime, timedelta
from typing import Optional
import os

SECRET_KEY = os.getenv("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

security = HTTPBearer()

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            credentials.credentials,
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )
        user_id: str = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    return {"user_id": user_id, "role": payload.get("role")}

async def get_admin_user(current_user = Depends(get_current_user)):
    if current_user.get("role") not in ["admin", "teacher"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
```

**Requirements:**
- Async SQLAlchemy sessions with context manager
- JWT token creation and validation
- HTTPBearer for token extraction
- Role-based access control
- Environment variables for secrets

### 4. Pydantic v2 Models

```python
# schemas/student.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from datetime import datetime
from typing import Optional
from enum import Enum

class StudentRole(str, Enum):
    STUDENT = "student"
    TEACHER = "teacher"
    ADMIN = "admin"

# Base model with config
class StudentBase(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: str = Field(..., min_length=2, max_length=100)
    email: EmailStr
    phone: Optional[str] = Field(None, pattern=r'^\+?[\d\s-]+$')

# Create schema
class StudentCreate(StudentBase):
    password: str = Field(..., min_length=8)
    class_id: Optional[str] = None

# Update schema (partial updates)
class StudentUpdate(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    class_id: Optional[str] = None

# Response schema
class StudentResponse(StudentBase):
    id: str
    class_id: Optional[str] = None
    created_at: datetime
    updated_at: datetime

# Pagination response
class PaginatedResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    data: list[StudentResponse]
    meta: dict = {
        "total": 0,
        "page": 1,
        "page_size": 100,
        "total_pages": 1
    }
```

```python
# schemas/fees.py
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from enum import Enum

class FeeStatus(str, Enum):
    PENDING = "pending"
    PAID = "paid"
    OVERDUE = "overdue"
    WAIVED = "waived"

class FeeBase(BaseModel):
    student_id: str
    amount: float = Field(..., gt=0)
    description: str = Field(..., max_length=500)
    due_date: datetime

class FeeCreate(FeeBase):
    pass

class FeeUpdate(BaseModel):
    status: Optional[FeeStatus] = None
    paid_date: Optional[datetime] = None
    notes: Optional[str] = None

class FeeResponse(FeeBase):
    id: str
    status: FeeStatus
    paid_date: Optional[datetime] = None
    created_at: datetime
```

**Requirements:**
- Use Pydantic v2 ConfigDict instead of Config class
- Field validation with min/max, patterns, gt/lt
- EmailStr for email validation
- Enum for status fields
- Optional fields with defaults
- From_attributes for ORM compatibility

## Output Requirements

### Code Files

1. **Main Application**:
   - `main.py` - FastAPI app initialization
   - `config.py` - Settings and environment variables

2. **Routers**:
   - `routers/__init__.py`
   - `routers/students.py`
   - `routers/fees.py`
   - `routers/attendance.py`
   - `routers/auth.py`

3. **Dependencies**:
   - `dependencies/__init__.py`
   - `dependencies/database.py`
   - `dependencies/auth.py`

4. **Models and Schemas**:
   - `models/__init__.py`
   - `models/student.py`
   - `schemas/__init__.py`
   - `schemas/student.py`
   - `schemas/fees.py`

### Integration Requirements

- **@api-client**: JSON response formatting for frontend
- **@auth-integration**: JWT validation
- **@react-component**: Error response schemas

### Documentation

- **PHR**: Create Prompt History Record for auth/DB decisions
- **ADR**: Document auth strategy (JWT vs session), DB choice (async SQLAlchemy)
- **Comments**: Document endpoint purposes and validation rules

## Workflow

1. **Initialize App**
   - Create FastAPI instance with lifespan
   - Configure CORS middleware
   - Set up logging

2. **Setup Database**
   - Create async SQLAlchemy engine
   - Define session dependency
   - Create database models

3. **Create Dependencies**
   - Auth dependency with JWT
   - Role-based access
   - DB session management

4. **Define Schemas**
   - Pydantic v2 models for requests/responses
   - Validation rules
   - Response formatting

5. **Build Routes**
   - Create APIRouter for each domain
   - Implement CRUD operations
   - Add pagination and filtering

6. **Test and Document**
   - Verify Swagger docs
   - Test authentication
   - Validate error responses

## Quality Checklist

Before completing any FastAPI implementation:

- [ ] **Pydantic v2 Validation**: ConfigDict, Field validators
- [ ] **SQLAlchemy Async**: Use async sessions, avoid blocking calls
- [ ] **Rate Limiting**: Implement slowapi or similar for endpoints
- [ ] **Swagger Docs Auto**: /docs shows all endpoints
- [ ] **Error Handling**: Proper HTTPException with status codes
- [ ] **Auth Protected**: All endpoints with dependencies
- [ ] **Pagination**: skip/limit for list endpoints
- [ ] **Type Hints**: All functions fully typed
- [ ] **Environment Config**: Secrets in environment variables
- [ ] **CORS Config**: Allow frontend origins with credentials

## Common Patterns

### Student Endpoint with Auth

```python
# routers/students.py
@router.get("/students/", response_model=List[StudentResponse])
async def get_students(
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    class_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user = Depends(get_current_user),
):
    """Get students with pagination and optional class filter"""
    query = select(StudentModel)

    if class_id:
        query = query.where(StudentModel.class_id == class_id)

    query = query.offset(skip).limit(limit).order_by(StudentModel.created_at.desc())

    result = await db.execute(query)
    return result.scalars().all()
```

### CORS Enable Frontend

```python
# main.py
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",   # Next.js dev
        "http://localhost:5173",   # Vite dev
        "https://yourdomain.com",  # Production
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
    allow_headers=["Authorization", "Content-Type"],
)
```

### DB Dependency with Session

```python
# dependencies/database.py
async def get_db() -> AsyncSession:
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

### JWT Auth Dependency

```python
# dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer

oauth2_scheme = HTTPBearer()

async def get_token_data(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
```

## Rate Limiting

```python
# dependencies/rate_limit.py
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)

def rate_limit(requests: int = 60, seconds: int = 60):
    def decorator(func):
        return limiter.limit(f"{requests}/{seconds}")(func)
    return decorator

# Usage
@router.get("/students/")
@rate_limit(requests=100, seconds=60)
async def get_students():
    return {"message": "Students list"}
```

## Environment Configuration

```python
# config.py
from pydantic_settings import BaseSettings
from typing import List

class Settings(BaseSettings):
    APP_NAME: str = "ERP API"
    DEBUG: bool = False
    API_V1_PREFIX: str = "/api/v1"

    # Database
    DATABASE_URL: str = "postgresql+asyncpg://user:password@localhost:5432/erp_db"

    # JWT
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    # CORS
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
```

## Running the Application

```bash
# Install dependencies
pip install fastapi uvicorn[standard] sqlalchemy[asyncio] asyncpg
pip install python-jose[cryptography] passlib[bcrypt]
pip install slowapi pydantic-settings

# Run development
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Run production
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

## References

- FastAPI Documentation: https://fastapi.tiangolo.com
- Pydantic v2: https://docs.pydantic.dev/latest/
- SQLAlchemy Async: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- JWT with FastAPI: https://fastapi.tiangolo.com/tutorial/security/oauth2-jwt/
- SlowAPI Rate Limiting: https://pypi.org/project/slowapi/
