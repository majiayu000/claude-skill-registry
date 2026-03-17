---
name: fastapi-development
description: Modern Python API development with FastAPI covering async patterns, Pydantic validation, dependency injection, and production deployment
---

# FastAPI Development

A comprehensive skill for building modern, high-performance Python APIs with FastAPI. Master async/await patterns, Pydantic data validation, dependency injection, authentication, database integration, and production-ready deployment strategies.

## When to Use This Skill

Use this skill when:

- Building RESTful APIs with Python for web, mobile, or microservices
- Developing high-performance, asynchronous backend services
- Creating APIs with automatic interactive documentation (OpenAPI/Swagger)
- Implementing OAuth2, JWT authentication, or other security patterns
- Integrating with SQL or NoSQL databases in Python applications
- Building APIs that require strong data validation and type safety
- Developing microservices with automatic request/response validation
- Creating APIs with WebSocket support for real-time features
- Migrating from Flask, Django REST Framework, or other Python frameworks
- Building production-ready APIs with proper error handling and testing

## Core Concepts

### FastAPI Philosophy

FastAPI is built on three foundational principles:

- **Fast to Code**: Reduce development time with automatic validation and documentation
- **Fast to Run**: High performance comparable to NodeJS and Go (via Starlette and Pydantic)
- **Fewer Bugs**: Automatic validation reduces human errors by about 40%
- **Standards-Based**: Built on OpenAPI and JSON Schema standards
- **Editor Support**: Full autocomplete, type checking, and inline documentation

### Key FastAPI Features

1. **Type Hints**: Python 3.6+ type hints for validation and documentation
2. **Async Support**: Native async/await for high-performance I/O operations
3. **Pydantic Models**: Automatic request/response validation and serialization
4. **Dependency Injection**: Elegant system for sharing logic across endpoints
5. **OpenAPI Docs**: Automatic interactive API documentation
6. **Security**: Built-in support for OAuth2, JWT, API keys, and more
7. **Testing**: Easy to test with TestClient and async test support

### Core Architecture Components

1. **FastAPI App**: The main application instance
2. **Path Operations**: Endpoint definitions with HTTP methods
3. **Pydantic Models**: Data validation and serialization schemas
4. **Dependencies**: Reusable logic for authentication, database, etc.
5. **Routers**: Organize endpoints into modules
6. **Middleware**: Process requests/responses globally
7. **Background Tasks**: Execute code after returning responses

## Getting Started

### Installation

```bash
# Basic installation
pip install fastapi

# With ASGI server for production
pip install "fastapi[all]"

# Or install separately
pip install fastapi uvicorn[standard]

# Additional dependencies
pip install python-multipart  # For form data
pip install python-jose[cryptography]  # For JWT
pip install passlib[bcrypt]  # For password hashing
pip install sqlalchemy  # For SQL databases
pip install databases  # For async database support
```

### Minimal FastAPI Application

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# Run with: uvicorn main:app --reload
```

## Pydantic Models for Data Validation

### Basic Model Definition

```python
from pydantic import BaseModel, Field, EmailStr, HttpUrl
from typing import Optional, List
from datetime import datetime

class User(BaseModel):
    id: int
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    full_name: Optional[str] = None
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
    full_name: Optional[str] = None

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    full_name: Optional[str]
    is_active: bool

    class Config:
        orm_mode = True  # For SQLAlchemy models
```

### Nested Models

```python
class Image(BaseModel):
    url: HttpUrl
    name: str

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    tax: Optional[float] = None
    tags: List[str] = []
    images: Optional[List[Image]] = None

# Request example:
# {
#   "name": "Laptop",
#   "price": 999.99,
#   "tags": ["electronics", "computers"],
#   "images": [
#     {"url": "http://example.com/img1.jpg", "name": "Front view"}
#   ]
# }
```

### Model Validation and Examples

```python
from pydantic import BaseModel, Field, validator

class Product(BaseModel):
    name: str = Field(..., example="MacBook Pro")
    price: float = Field(..., gt=0, example=1999.99)
    discount: Optional[float] = Field(None, ge=0, le=100, example=10.0)

    @validator('discount')
    def discount_check(cls, v, values):
        if v and 'price' in values:
            discounted = values['price'] * (1 - v/100)
            if discounted < 0:
                raise ValueError('Discounted price cannot be negative')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "MacBook Pro 16",
                "price": 2499.99,
                "discount": 15.0
            }
        }
```

## Path Operations and Routing

### HTTP Methods and Path Parameters

```python
from fastapi import FastAPI, Path, Query, Body
from typing import Optional

app = FastAPI()

# GET with path parameter
@app.get("/items/{item_id}")
async def read_item(
    item_id: int = Path(..., title="The ID of the item", ge=1),
    q: Optional[str] = Query(None, max_length=50)
):
    return {"item_id": item_id, "q": q}

# POST with request body
@app.post("/items/")
async def create_item(item: Item):
    return {"item": item, "message": "Item created"}

# PUT for updates
@app.put("/items/{item_id}")
async def update_item(
    item_id: int,
    item: Item = Body(...),
):
    return {"item_id": item_id, "item": item}

# DELETE
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    return {"message": f"Item {item_id} deleted"}

# PATCH for partial updates
@app.patch("/items/{item_id}")
async def partial_update_item(
    item_id: int,
    item: dict = Body(...)
):
    return {"item_id": item_id, "updated_fields": item}
```

### Query Parameters with Validation

```python
from fastapi import Query
from typing import List, Optional

@app.get("/search/")
async def search_items(
    q: str = Query(..., min_length=3, max_length=50),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort_by: Optional[str] = Query(None, regex="^(name|price|date)$"),
    tags: List[str] = Query([], description="Filter by tags")
):
    return {
        "q": q,
        "skip": skip,
        "limit": limit,
        "sort_by": sort_by,
        "tags": tags
    }
```

### Response Models

```python
from typing import List

@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate):
    # Hash password, save to DB
    db_user = {
        "id": 1,
        "username": user.username,
        "email": user.email,
        "full_name": user.full_name,
        "is_active": True
    }
    return db_user

@app.get("/users/", response_model=List[UserResponse])
async def list_users(skip: int = 0, limit: int = 100):
    users = [...]  # Fetch from database
    return users

# Exclude fields from response
class UserInDB(User):
    hashed_password: str

@app.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int):
    user = get_user_from_db(user_id)  # Returns UserInDB
    return user  # Password excluded automatically
```

## Async/Await Patterns

### When to Use async vs def

```python
# Use async def when:
# - Making database queries with async driver
# - Calling external APIs with httpx/aiohttp
# - Using async I/O operations
# - Working with async libraries

@app.get("/async-example")
async def async_endpoint():
    # Can use await inside
    result = await async_database_query()
    external_data = await async_http_call()
    return {"result": result, "external": external_data}

# Use def when:
# - Working with synchronous libraries
# - Performing CPU-bound operations
# - No async operations needed

@app.get("/sync-example")
def sync_endpoint():
    # Regular synchronous code
    result = synchronous_database_query()
    return {"result": result}
```

### Async Database Operations

```python
import asyncio
from databases import Database

DATABASE_URL = "postgresql://user:password@localhost/dbname"
database = Database(DATABASE_URL)

@app.on_event("startup")
async def startup():
    await database.connect()

@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()

@app.get("/users/{user_id}")
async def get_user(user_id: int):
    query = "SELECT * FROM users WHERE id = :user_id"
    user = await database.fetch_one(query, {"user_id": user_id})
    return user

@app.post("/users/")
async def create_user(user: UserCreate):
    query = """
        INSERT INTO users (username, email, hashed_password)
        VALUES (:username, :email, :password)
        RETURNING *
    """
    hashed_password = hash_password(user.password)
    new_user = await database.fetch_one(
        query,
        {
            "username": user.username,
            "email": user.email,
            "password": hashed_password
        }
    )
    return new_user
```

### Concurrent Operations

```python
import asyncio
import httpx

async def fetch_user(user_id: int):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.example.com/users/{user_id}")
        return response.json()

@app.get("/users/batch")
async def get_multiple_users(user_ids: List[int] = Query(...)):
    # Fetch all users concurrently
    users = await asyncio.gather(*[fetch_user(uid) for uid in user_ids])
    return {"users": users}
```

## Dependency Injection

### Basic Dependencies

```python
from fastapi import Depends
from typing import Optional

# Simple dependency function
async def common_parameters(
    q: Optional[str] = None,
    skip: int = 0,
    limit: int = 100
):
    return {"q": q, "skip": skip, "limit": limit}

@app.get("/items/")
async def read_items(commons: dict = Depends(common_parameters)):
    return commons

@app.get("/users/")
async def read_users(commons: dict = Depends(common_parameters)):
    return commons
```

### Class-Based Dependencies

```python
class Pagination:
    def __init__(
        self,
        skip: int = Query(0, ge=0),
        limit: int = Query(100, ge=1, le=100)
    ):
        self.skip = skip
        self.limit = limit

@app.get("/items/")
async def list_items(pagination: Pagination = Depends()):
    return {
        "skip": pagination.skip,
        "limit": pagination.limit,
        "items": []  # Fetch with pagination
    }
```

### Database Session Dependency

```python
from sqlalchemy.orm import Session
from typing import Generator

def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Sub-Dependencies

```python
from fastapi import Header, HTTPException

async def verify_token(x_token: str = Header(...)):
    if x_token != "secret-token":
        raise HTTPException(status_code=400, detail="Invalid token")
    return x_token

async def verify_key(x_key: str = Header(...)):
    if x_key != "secret-key":
        raise HTTPException(status_code=400, detail="Invalid key")
    return x_key

async def verify_credentials(
    token: str = Depends(verify_token),
    key: str = Depends(verify_key)
):
    return {"token": token, "key": key}

@app.get("/protected/")
async def protected_route(credentials: dict = Depends(verify_credentials)):
    return {"message": "Access granted", "credentials": credentials}
```

### Global Dependencies

```python
async def log_requests():
    print("Request received")

app = FastAPI(dependencies=[Depends(log_requests)])

# This dependency runs for ALL endpoints
```

## Authentication and Security

### OAuth2 Password Bearer with JWT

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta
from typing import Optional

SECRET_KEY = "your-secret-key-here"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception

    user = get_user_from_db(username=token_data.username)
    if user is None:
        raise credentials_exception
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user)
):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

@app.post("/token", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user
```

### API Key Authentication

```python
from fastapi import Security
from fastapi.security import APIKeyHeader

API_KEY = "your-api-key"
api_key_header = APIKeyHeader(name="X-API-Key")

async def verify_api_key(api_key: str = Security(api_key_header)):
    if api_key != API_KEY:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid API Key"
        )
    return api_key

@app.get("/secure-data")
async def get_secure_data(api_key: str = Depends(verify_api_key)):
    return {"data": "This is secure data"}
```

### OAuth2 with Scopes

```python
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="token",
    scopes={
        "items:read": "Read items",
        "items:write": "Create and update items",
        "users:read": "Read user information"
    }
)

async def get_current_user_with_scopes(
    security_scopes: SecurityScopes,
    token: str = Depends(oauth2_scheme)
):
    # Verify token and check scopes
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = "Bearer"

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )

    # Decode JWT and verify scopes...
    return user

@app.get("/items/", dependencies=[Security(get_current_user_with_scopes, scopes=["items:read"])])
async def read_items():
    return [{"item": "Item 1"}, {"item": "Item 2"}]

@app.post("/items/", dependencies=[Security(get_current_user_with_scopes, scopes=["items:write"])])
async def create_item(item: Item):
    return {"item": item}
```

## Database Integration

### SQLAlchemy Setup

```python
from sqlalchemy import create_engine, Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "postgresql://user:password@localhost/dbname"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Models
class UserModel(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

Base.metadata.create_all(bind=engine)
```

### CRUD Operations

```python
from sqlalchemy.orm import Session

# Create
@app.post("/users/", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(
        username=user.username,
        email=user.email,
        hashed_password=get_password_hash(user.password)
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Read
@app.get("/users/{user_id}", response_model=UserResponse)
async def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

# Update
@app.put("/users/{user_id}", response_model=UserResponse)
async def update_user(
    user_id: int,
    user_update: UserCreate,
    db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    user.username = user_update.username
    user.email = user_update.email
    if user_update.password:
        user.hashed_password = get_password_hash(user_update.password)

    db.commit()
    db.refresh(user)
    return user

# Delete
@app.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"message": "User deleted successfully"}
```

## Background Tasks

```python
from fastapi import BackgroundTasks

def send_email(email: str, message: str):
    # Simulate sending email
    print(f"Sending email to {email}: {message}")

def process_file(filename: str):
    # Simulate file processing
    print(f"Processing file: {filename}")

@app.post("/send-notification/")
async def send_notification(
    email: str,
    background_tasks: BackgroundTasks
):
    background_tasks.add_task(send_email, email, "Welcome!")
    return {"message": "Notification scheduled"}

@app.post("/upload/")
async def upload_file(
    file: str,
    background_tasks: BackgroundTasks
):
    # Save file first
    background_tasks.add_task(process_file, file)
    return {"message": "File uploaded, processing in background"}
```

## Error Handling

### Custom Exception Handlers

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

class CustomException(Exception):
    def __init__(self, name: str):
        self.name = name

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=418,
        content={"message": f"Oops! {exc.name} did something wrong."},
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={"detail": exc.errors()},
    )

@app.get("/items/{item_id}")
async def read_item(item_id: str):
    if item_id == "error":
        raise CustomException(name="Item")
    return {"item_id": item_id}
```

## Testing

### Basic Tests with TestClient

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}

def test_create_item():
    response = client.post(
        "/items/",
        json={"name": "Test Item", "price": 10.5}
    )
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_authentication():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    assert "access_token" in response.json()
```

### Async Tests

```python
import pytest
from httpx import AsyncClient

@pytest.mark.anyio
async def test_read_items():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

@pytest.mark.anyio
async def test_create_user():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post(
            "/users/",
            json={
                "username": "newuser",
                "email": "new@example.com",
                "password": "securepass123"
            }
        )
    assert response.status_code == 200
    assert response.json()["username"] == "newuser"
```

## Routers and Organization

### APIRouter for Modular Code

```python
# routers/users.py
from fastapi import APIRouter, Depends

router = APIRouter(
    prefix="/users",
    tags=["users"],
    dependencies=[Depends(verify_token)],
    responses={404: {"description": "Not found"}},
)

@router.get("/")
async def list_users():
    return [{"username": "user1"}, {"username": "user2"}]

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id}

# main.py
from routers import users

app = FastAPI()
app.include_router(users.router)
```

## Best Practices

### 1. Project Structure

```
my_fastapi_project/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   └── item.py
│   ├── routers/
│   │   ├── __init__.py
│   │   ├── users.py
│   │   └── items.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   └── database.py
│   └── utils/
│       ├── __init__.py
│       └── security.py
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   └── test_items.py
├── requirements.txt
├── .env
└── README.md
```

### 2. Configuration Management

```python
from pydantic import BaseSettings

class Settings(BaseSettings):
    app_name: str = "My FastAPI App"
    database_url: str
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

settings = Settings()
```

### 3. Documentation

```python
app = FastAPI(
    title="My API",
    description="This is a very custom API",
    version="1.0.0",
    openapi_tags=[
        {
            "name": "users",
            "description": "Operations with users.",
        },
        {
            "name": "items",
            "description": "Manage items.",
        },
    ]
)

@app.post(
    "/items/",
    response_model=Item,
    tags=["items"],
    summary="Create an item",
    description="Create an item with all the information",
    response_description="The created item",
)
async def create_item(item: Item):
    return item
```

## Production Deployment

### Docker Setup

```dockerfile
# Dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY ./app /app

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Run with Gunicorn and Uvicorn Workers

```bash
gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

**Skill Version**: 1.0.0
**Last Updated**: October 2025
**Skill Category**: Backend Development, API Development, Python
**Compatible With**: FastAPI 0.100+, Python 3.7+, Pydantic 2.0+
