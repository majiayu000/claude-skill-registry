---
name: error-handling
description: |
  Error handling patterns and best practices for FastAPI endpoints.
  Auto-activates on "error", "exception", "validation", "錯誤處理", "異常" keywords.
  Provides consistent error responses and logging strategies.
allowed-tools: [Read, Edit, Grep]
---

# Error Handling Skill

## Purpose
Consistent error handling patterns for career_ios_backend FastAPI application.

## Auto-Activation

Triggers on:
- ✅ "error", "exception", "validation"
- ✅ "錯誤處理", "異常處理"
- ✅ "error handling", "exception handling"

---

## Core Principles (Prototype Phase)

**Keep it simple**:
- ✅ Use FastAPI's HTTPException
- ✅ Return clear error messages
- ✅ Log errors appropriately
- ❌ Don't over-engineer custom exceptions (yet)

---

## Standard Error Response Format

### FastAPI HTTPException Pattern

```python
from fastapi import HTTPException, status

# 404 Not Found
raise HTTPException(
    status_code=status.HTTP_404_NOT_FOUND,
    detail="Client not found"
)

# 400 Bad Request
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Invalid client code format"
)

# 401 Unauthorized
raise HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="Invalid credentials",
    headers={"WWW-Authenticate": "Bearer"}
)

# 403 Forbidden
raise HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Insufficient permissions"
)

# 500 Internal Server Error
raise HTTPException(
    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
    detail="Database connection failed"
)
```

---

## HTTP Status Codes (Quick Reference)

| Code | When to Use | Example |
|------|------------|---------|
| **200** | Success | GET resource |
| **201** | Created | POST new resource |
| **204** | No Content | DELETE successful |
| **400** | Bad Request | Invalid input |
| **401** | Unauthorized | Missing/invalid token |
| **403** | Forbidden | Insufficient permissions |
| **404** | Not Found | Resource doesn't exist |
| **409** | Conflict | Duplicate resource |
| **422** | Validation Error | Pydantic validation fails |
| **500** | Server Error | Unexpected error |

---

## Common Patterns

### Pattern 1: Resource Not Found

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

@router.get("/clients/{client_id}")
async def get_client(
    client_id: int,
    db: Session = Depends(get_db)
):
    client = db.query(Client).filter(Client.id == client_id).first()

    if not client:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Client with id {client_id} not found"
        )

    return client
```

### Pattern 2: Validation Error

```python
@router.post("/clients", status_code=status.HTTP_201_CREATED)
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db)
):
    # Check for duplicate
    existing = db.query(Client).filter(
        Client.email == client_data.email
    ).first()

    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Client with email {client_data.email} already exists"
        )

    # Create client
    new_client = Client(**client_data.dict())
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

    return new_client
```

### Pattern 3: Database Error

```python
from sqlalchemy.exc import SQLAlchemyError
import logging

logger = logging.getLogger(__name__)

@router.post("/clients")
async def create_client(
    client_data: ClientCreate,
    db: Session = Depends(get_db)
):
    try:
        new_client = Client(**client_data.dict())
        db.add(new_client)
        db.commit()
        db.refresh(new_client)
        return new_client

    except SQLAlchemyError as e:
        db.rollback()
        logger.error(f"Database error creating client: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create client"
        )
```

### Pattern 4: Authentication Error

```python
from app.core.security import verify_password

@router.post("/auth/login")
async def login(
    credentials: LoginRequest,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.username == credentials.username).first()

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    # Generate token
    access_token = create_access_token(data={"sub": user.username})
    return {"access_token": access_token, "token_type": "bearer"}
```

---

## Pydantic Validation (Automatic)

FastAPI automatically validates request bodies using Pydantic:

```python
from pydantic import BaseModel, EmailStr, validator

class ClientCreate(BaseModel):
    name: str
    email: EmailStr  # Automatic email validation
    age: int

    @validator('age')
    def age_must_be_positive(cls, v):
        if v < 0:
            raise ValueError('Age must be positive')
        return v

    @validator('name')
    def name_must_not_be_empty(cls, v):
        if not v.strip():
            raise ValueError('Name cannot be empty')
        return v
```

**Automatic 422 Response**:
When validation fails, FastAPI returns:
```json
{
  "detail": [
    {
      "loc": ["body", "email"],
      "msg": "value is not a valid email address",
      "type": "value_error.email"
    }
  ]
}
```

---

## Logging Best Practices

### Basic Logging Setup

```python
import logging

# At the top of your module
logger = logging.getLogger(__name__)

# Log levels
logger.debug("Detailed debug info")      # Development only
logger.info("General information")       # Normal operations
logger.warning("Warning message")        # Potential issues
logger.error("Error occurred")           # Error happened
logger.critical("Critical failure")      # System failure
```

### Log with Context

```python
@router.post("/clients")
async def create_client(client_data: ClientCreate, db: Session = Depends(get_db)):
    logger.info(f"Creating client: {client_data.name}")

    try:
        # ... create client
        logger.info(f"Client created successfully: id={new_client.id}")
        return new_client

    except Exception as e:
        logger.error(
            f"Failed to create client: {client_data.name}",
            exc_info=True  # Include full traceback
        )
        raise
```

### What to Log

**✅ Do Log**:
- Incoming requests (at INFO level)
- Successful operations (at INFO level)
- Errors with context (at ERROR level)
- Authentication failures (at WARNING level)

**❌ Don't Log**:
- Passwords or tokens
- Sensitive user data
- Too much detail in production (use DEBUG level in development)

---

## Error Handling Checklist

### Before Commit

- [ ] All error cases return appropriate HTTP status codes
- [ ] Error messages are clear and actionable
- [ ] Sensitive data not exposed in error messages
- [ ] Errors are logged with sufficient context
- [ ] Database transactions rolled back on error
- [ ] Tests cover error scenarios

---

## Testing Error Cases

```python
import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_client_not_found():
    """Test 404 when client doesn't exist"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/api/v1/clients/99999")

    assert response.status_code == 404
    assert "not found" in response.json()["detail"].lower()

@pytest.mark.asyncio
async def test_duplicate_client(auth_headers):
    """Test 400 when creating duplicate client"""
    client_data = {
        "name": "Test Client",
        "email": "test@example.com"
    }

    async with AsyncClient(app=app, base_url="http://test") as client:
        # Create first time
        response1 = await client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json=client_data
        )
        assert response1.status_code == 201

        # Try to create duplicate
        response2 = await client.post(
            "/api/v1/clients",
            headers=auth_headers,
            json=client_data
        )
        assert response2.status_code == 400
        assert "already exists" in response2.json()["detail"].lower()

@pytest.mark.asyncio
async def test_invalid_token():
    """Test 401 with invalid token"""
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get(
            "/api/v1/clients",
            headers={"Authorization": "Bearer invalid_token"}
        )

    assert response.status_code == 401
```

---

## Quick Reference Table

| Scenario | Status Code | Pattern |
|----------|------------|---------|
| Resource not found | 404 | Check `if not resource: raise HTTPException(404)` |
| Invalid input | 400 | Validate before processing |
| Duplicate resource | 400 | Check existence first |
| Unauthorized | 401 | Verify token/credentials |
| Forbidden | 403 | Check permissions |
| Validation error | 422 | Use Pydantic validators |
| Database error | 500 | Try-except with rollback |

---

## Anti-Patterns to Avoid

### ❌ Generic Error Messages

```python
# Bad
raise HTTPException(status_code=400, detail="Bad request")

# Good
raise HTTPException(
    status_code=400,
    detail="Client email format is invalid"
)
```

### ❌ Exposing Internal Details

```python
# Bad - exposes database structure
raise HTTPException(
    status_code=500,
    detail=f"SQLAlchemy error: {str(e)}"
)

# Good - user-friendly message
logger.error(f"Database error: {str(e)}", exc_info=True)
raise HTTPException(
    status_code=500,
    detail="Failed to process request"
)
```

### ❌ Swallowing Exceptions

```python
# Bad - silently fails
try:
    db.commit()
except Exception:
    pass  # Error ignored!

# Good - handle or re-raise
try:
    db.commit()
except Exception as e:
    logger.error(f"Commit failed: {e}", exc_info=True)
    db.rollback()
    raise HTTPException(500, detail="Operation failed")
```

---

## Related Skills

- **api-development**: API design patterns
- **debugging**: Debug error scenarios
- **quality-standards**: Code quality requirements

---

**Skill Version**: v1.0
**Last Updated**: 2025-12-25
**Project**: career_ios_backend (Prototype Phase)
