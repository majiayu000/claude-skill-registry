---
name: fastapi-full-stack
description: Enterprise-grade FastAPI development covering complete full-stack architecture with Next.js/React frontend, Neon Serverless PostgreSQL, SQLModel ORM, security hardening, payment integrations (Stripe, JazzCash, EasyPaisa), async patterns, real-time features, microservices, and production deployment. Use when building APIs, integrating with databases, implementing authentication/authorization, payment systems, real-time functionality, or deploying to production.
---

# FastAPI Full Stack Development

Production-grade FastAPI applications require comprehensive architecture across database design, security, API patterns, payment processing, and deployment. This skill provides enterprise-level guidance covering all aspects of building scalable, secure APIs integrated with modern frontend frameworks.

## Core Architecture

### Project Structure
Organize FastAPI projects for scalability and maintainability:

```
my_api/
├── app/
│   ├── __init__.py
│   ├── main.py              # Application entry point
│   ├── config.py            # Configuration & environment
│   ├── models/              # SQLModel database models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── payment.py
│   │   └── order.py
│   ├── schemas/             # Pydantic request/response models
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── payment.py
│   ├── routes/              # API endpoint routers
│   │   ├── __init__.py
│   │   ├── users.py
│   │   ├── auth.py
│   │   └── payments.py
│   ├── services/            # Business logic layer
│   │   ├── __init__.py
│   │   ├── user_service.py
│   │   └── payment_service.py
│   ├── dependencies/        # Dependency injection
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── database.py
│   ├── middleware/          # Custom middleware
│   │   ├── __init__.py
│   │   ├── cors.py
│   │   └── security.py
│   └── utils/               # Helper functions
│       ├── __init__.py
│       └── validators.py
├── tests/
│   ├── __init__.py
│   ├── conftest.py
│   ├── test_users.py
│   └── test_payments.py
├── migrations/              # Alembic migrations
├── requirements.txt
├── .env
├── .env.example
└── docker-compose.yml
```

### Configuration Management

Use Pydantic BaseSettings for environment-based configuration:

```python
# app/config.py
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Database
    database_url: str
    db_echo: bool = False
    
    # JWT
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    refresh_token_expire_days: int = 7
    
    # Security
    allowed_origins: list[str] = ["http://localhost:3000"]
    cors_credentials: bool = True
    
    # Payments
    stripe_secret_key: str
    stripe_publishable_key: str
    stripe_webhook_secret: str
    
    # Email
    smtp_server: str
    smtp_port: int = 587
    smtp_user: str
    smtp_password: str
    
    # App
    debug: bool = False
    environment: str = "development"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
```

## Database Layer with Neon & SQLModel

### Connection Setup for Serverless

Neon's serverless PostgreSQL requires specific connection pooling configuration:

```python
# app/dependencies/database.py
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.pool import NullPool
from app.config import settings

# Critical: Use NullPool for serverless (no persistent connections)
engine = create_engine(
    settings.database_url,
    echo=settings.db_echo,
    poolclass=NullPool,  # Essential for Neon serverless
    connect_args={
        "connect_timeout": 5,
        "application_name": "my_api"
    }
)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
```

### Model Definitions with Validation

Design SQLModel models with security and validation:

```python
# app/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional
from pydantic import EmailStr, field_validator

class UserBase(SQLModel):
    email: EmailStr = Field(unique=True, index=True)
    full_name: str = Field(min_length=1, max_length=255)
    is_active: bool = True
    
class User(UserBase, table=True):
    __tablename__ = "users"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    hashed_password: str = Field(min_length=60)  # bcrypt hash
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    deleted_at: Optional[datetime] = None
    role: str = Field(default="user", index=True)
    
    # Relationships
    payments: list["Payment"] = Relationship(back_populates="user")
    
    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "full_name": "John Doe",
                "is_active": True
            }
        }

class UserCreate(UserBase):
    password: str = Field(min_length=8)
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError('Password must contain uppercase letter')
        if not any(c.isdigit() for c in v):
            raise ValueError('Password must contain digit')
        return v

class UserResponse(UserBase):
    id: int
    created_at: datetime
    role: str
```

See **[DATABASE.md](references/database.md)** for migrations, relationships, indexing, and advanced patterns.

## Authentication & Authorization

### JWT Implementation

```python
# app/dependencies/auth.py
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
from passlib.context import CryptContext
from app.config import settings
from sqlmodel import Session, select
from app.models.user import User

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=settings.access_token_expire_minutes))
    to_encode.update({"exp": expire, "type": "access"})
    return jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)

def create_refresh_token(user_id: int):
    data = {"sub": str(user_id), "type": "refresh"}
    expire = datetime.utcnow() + timedelta(days=settings.refresh_token_expire_days)
    data["exp"] = expire
    return jwt.encode(data, settings.secret_key, algorithm=settings.algorithm)

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: Session = Depends(get_session)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        user_id: str = payload.get("sub")
        token_type: str = payload.get("type")
        
        if user_id is None or token_type != "access":
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    user = session.exec(select(User).where(User.id == int(user_id))).first()
    if user is None:
        raise credentials_exception
    
    return user

def verify_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return current_user
```

See **[SECURITY.md](references/security.md)** for role-based access control, OAuth2, password reset flows, and security best practices.

## API Routes & Patterns

### RESTful Endpoint Design

```python
# app/routes/users.py
from fastapi import APIRouter, Depends, HTTPException, Query, status
from typing import List
from sqlmodel import Session, select
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.dependencies.auth import get_current_user
from app.dependencies.database import get_session
from app.services.user_service import UserService

router = APIRouter(prefix="/api/v1/users", tags=["users"])
user_service = UserService()

@router.get("/", response_model=List[UserResponse])
async def list_users(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """List all users with pagination - requires authentication"""
    statement = select(User).where(User.deleted_at == None).offset(skip).limit(limit)
    users = session.exec(statement).all()
    return users

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(
    user_in: UserCreate,
    session: Session = Depends(get_session)
):
    """Create new user - no auth required for registration"""
    existing_user = session.exec(select(User).where(User.email == user_in.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    user = await user_service.create_user(user_in, session)
    return user

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Get user by ID"""
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_in: UserCreate,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Update user - only owners or admins"""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = await user_service.update_user(user, user_in, session)
    return user

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    """Soft delete user"""
    if current_user.id != user_id and current_user.role != "admin":
        raise HTTPException(status_code=403, detail="Not authorized")
    
    user = session.exec(select(User).where(User.id == user_id)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    await user_service.delete_user(user, session)
```

## Payment Integration

### Stripe Implementation

See **[PAYMENTS.md](references/payments.md)** for complete Stripe, JazzCash, and EasyPaisa integration patterns including webhook handling, transaction management, and error recovery.

### Webhook Pattern

```python
# app/routes/payments.py
from fastapi import APIRouter, Request, HTTPException
import stripe
from app.config import settings

router = APIRouter(prefix="/api/v1/payments", tags=["payments"])

@router.post("/webhook/stripe")
async def stripe_webhook(request: Request, session: Session = Depends(get_session)):
    """Handle Stripe webhook events securely"""
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    
    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=403, detail="Invalid signature")
    
    # Handle events
    if event["type"] == "checkout.session.completed":
        await handle_checkout_completed(event["data"]["object"], session)
    elif event["type"] == "charge.refunded":
        await handle_charge_refunded(event["data"]["object"], session)
    
    return {"status": "received"}
```

## Middleware & Security

### Security Headers Middleware

```python
# app/middleware/security.py
from fastapi import Request
from fastapi.responses import Response
import time

async def add_security_headers(request: Request, call_next):
    response = await call_next(request)
    
    # Content Security
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["X-XSS-Protection"] = "1; mode=block"
    
    # HSTS (HTTP Strict Transport Security)
    response.headers["Strict-Transport-Security"] = "max-age=31536000; includeSubDomains; preload"
    
    # Additional
    response.headers["Content-Security-Policy"] = "default-src 'self'"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    
    return response

async def request_logging(request: Request, call_next):
    """Log all requests with response times"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response
```

See **[SECURITY.md](references/security.md)** for CORS configuration, rate limiting, and comprehensive security hardening.

## Testing

Use pytest for comprehensive test coverage:

```python
# tests/conftest.py
import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, create_engine, SQLModel
from sqlmodel.pool import StaticPool
from app.main import app
from app.dependencies.database import get_session

@pytest.fixture(name="session")
def session_fixture():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session

@pytest.fixture(name="client")
def client_fixture(session: Session):
    def get_session_override():
        return session
    
    app.dependency_overrides[get_session] = get_session_override
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

# tests/test_users.py
def test_create_user(client: TestClient):
    response = client.post("/api/v1/users", json={
        "email": "test@example.com",
        "full_name": "Test User",
        "password": "SecurePass123"
    })
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"

def test_auth_required(client: TestClient):
    response = client.get("/api/v1/users")
    assert response.status_code == 401
```

## Next.js/React Integration

### Frontend API Client Setup

```typescript
// lib/api.ts
import axios from 'axios';
import { useRouter } from 'next/router';

const apiClient = axios.create({
  baseURL: process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000',
  timeout: 10000,
});

// Token management
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle token refresh on 401
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      const refreshToken = localStorage.getItem('refresh_token');
      if (refreshToken) {
        try {
          const { data } = await axios.post('/api/v1/auth/refresh', {
            refresh_token: refreshToken
          });
          localStorage.setItem('access_token', data.access_token);
          return apiClient(error.config);
        } catch {
          localStorage.removeItem('access_token');
          localStorage.removeItem('refresh_token');
        }
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
```

See **[FRONTEND.md](references/frontend.md)** for complete Next.js/React setup and integration patterns.

## Deployment & Production

### Docker Configuration

See **[DEPLOYMENT.md](references/deployment.md)** for Docker, Kubernetes, serverless deployment, CI/CD pipelines, and monitoring setup.

### Environment Variables

```bash
# .env.production
DATABASE_URL=postgresql://user:password@neon-endpoint/dbname
SECRET_KEY=your-secret-key-minimum-32-characters-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7

STRIPE_SECRET_KEY=sk_live_...
STRIPE_PUBLISHABLE_KEY=pk_live_...
STRIPE_WEBHOOK_SECRET=whsec_...

ALLOWED_ORIGINS=https://yourdomain.com,https://api.yourdomain.com
DEBUG=False
ENVIRONMENT=production
```

## Key Security Checklist

✅ **Input Validation** - All inputs validated via Pydantic  
✅ **Password Security** - Bcrypt hashing, complexity requirements  
✅ **JWT** - Short expiration times, refresh token rotation  
✅ **CORS** - Strictly configured for frontend only  
✅ **SQL Injection** - Parameterized queries (SQLModel handles)  
✅ **Rate Limiting** - On auth and payment endpoints  
✅ **HTTPS** - Enforced with HSTS header  
✅ **Secrets** - Environment variables, never committed  
✅ **Logging** - Comprehensive without sensitive data  
✅ **Dependencies** - Regular updates and security patches  

## Quick Start Commands

```bash
# New project setup
python scripts/generate_boilerplate.py --name my_api
cd my_api
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Database
alembic upgrade head

# Development
uvicorn app.main:app --reload

# Testing
pytest -v --cov=app

# Production
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker
```

## Resource Files

- **[DATABASE.md](references/database.md)** - Complete database patterns, migrations, relationships
- **[SECURITY.md](references/security.md)** - Auth, authorization, security hardening
- **[ROUTES.md](references/routes.md)** - API design patterns, error handling, validation
- **[PAYMENTS.md](references/payments.md)** - Stripe, JazzCash, EasyPaisa integration
- **[FRONTEND.md](references/frontend.md)** - Next.js/React integration patterns
- **[TESTING.md](references/testing.md)** - Test strategies, fixtures, coverage
- **[DEPLOYMENT.md](references/deployment.md)** - Docker, Kubernetes, CI/CD, monitoring
- **[EXAMPLES.md](references/examples.md)** - Complete working examples

## Script Resources

- **[generate_boilerplate.py](scripts/generate_boilerplate.py)** - Create complete project structure
- **[security_audit.py](scripts/security_audit.py)** - Scan for vulnerabilities
- **[db_migrate.py](scripts/db_migrate.py)** - Migration utilities