---
name: fastapi
category: backend
version: 2.0.0
description: FastAPI patterns for Australian-first API development
author: Unite Group
priority: 3
triggers:
  - fastapi
  - api
  - endpoint
  - rest api
---

# FastAPI Patterns

## App Setup

```python
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager."""
    await init_database()
    await init_australian_context()  # Load AU locale settings
    yield
    await close_database()

app = FastAPI(
    title="Unite Group API",
    description="Australian-first API",
    version="1.0.0",
    lifespan=lifespan
)

# CORS for Australian domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://unite-group.com.au",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

## Routes

```python
from fastapi import APIRouter, Depends, HTTPException
from typing import Annotated

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/", response_model=list[UserResponse])
async def list_users(
    db: Annotated[Database, Depends(get_db)],
    locale: str = "en-AU"  # Default Australian English
):
    """List all users with Australian formatting."""
    users = await db.get_users()
    return [format_user_response(u, locale) for u in users]

@router.get("/{user_id}")
async def get_user(
    user_id: str,
    db: Annotated[Database, Depends(get_db)]
):
    """Get user by ID."""
    user = await db.get_user(user_id)
    if not user:
        raise HTTPException(404, "User not found")
    return user

@router.post("/", status_code=201)
async def create_user(
    request: CreateUserRequest,
    db: Annotated[Database, Depends(get_db)]
):
    """Create new user."""
    # Validate Australian phone format (04XX XXX XXX)
    if request.phone and not validate_australian_phone(request.phone):
        raise HTTPException(422, "Invalid Australian phone format")

    return await db.create_user(request)
```

## Models

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from typing import Literal

class CreateUserRequest(BaseModel):
    """Create user request with Australian validation."""
    email: EmailStr
    name: str = Field(..., min_length=1, max_length=100)
    phone: str | None = Field(None, pattern=r"^04\d{2}\s?\d{3}\s?\d{3}$")
    state: Literal["QLD", "NSW", "VIC", "SA", "WA", "TAS", "NT", "ACT"] | None = None
    postcode: str | None = Field(None, pattern=r"^\d{4}$")

    @field_validator("phone")
    @classmethod
    def validate_phone(cls, v: str | None) -> str | None:
        """Validate Australian mobile format."""
        if v:
            # Normalize to 04XX XXX XXX format
            cleaned = v.replace(" ", "")
            if len(cleaned) == 10 and cleaned.startswith("04"):
                return f"{cleaned[:4]} {cleaned[4:7]} {cleaned[7:]}"
        return v

class UserResponse(BaseModel):
    """User response with Australian formatting."""
    id: str
    email: str
    name: str
    phone: str | None = None
    state: str | None = None
    postcode: str | None = None
    created_at: str  # DD/MM/YYYY format

    model_config = ConfigDict(from_attributes=True)

    @field_validator("created_at", mode="before")
    @classmethod
    def format_date_au(cls, v) -> str:
        """Format date in DD/MM/YYYY."""
        if isinstance(v, datetime):
            return v.strftime("%d/%m/%Y")
        return v
```

## Dependencies

```python
from fastapi import Request, Header
from typing import Annotated

async def get_db():
    """Database dependency."""
    db = Database()
    try:
        yield db
    finally:
        await db.close()

async def get_australian_context(
    accept_language: Annotated[str | None, Header()] = None
) -> dict:
    """Get Australian context."""
    return {
        "locale": "en-AU",
        "currency": "AUD",
        "date_format": "DD/MM/YYYY",
        "timezone": "Australia/Brisbane",
        "phone_format": "04XX XXX XXX"
    }

async def get_current_user(
    request: Request,
    db: Annotated[Database, Depends(get_db)]
) -> User:
    """Get authenticated user."""
    token = request.headers.get("Authorization", "").replace("Bearer ", "")
    if not token:
        raise HTTPException(401, "Not authenticated")
    return await verify_token(token, db)
```

## Error Handling

```python
from fastapi.responses import JSONResponse
from pydantic import ValidationError

@app.exception_handler(ValidationError)
async def validation_handler(request: Request, exc: ValidationError):
    """Handle validation errors with en-AU messages."""
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation failed",
            "details": exc.errors(),
            "message": "Please check your input and try again."  # en-AU friendly
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def generic_exception_handler(request: Request, exc: Exception):
    """Handle unexpected errors."""
    logger.error("Unhandled exception", error=str(exc), exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )
```

## Australian Compliance Endpoints

```python
@router.get("/privacy-policy")
async def privacy_policy():
    """Privacy policy compliance (Privacy Act 1988)."""
    return {
        "jurisdiction": "Australia",
        "act": "Privacy Act 1988",
        "url": "https://unite-group.com.au/privacy"
    }

@router.post("/consent")
async def record_consent(
    consent: ConsentRequest,
    db: Annotated[Database, Depends(get_db)]
):
    """Record user consent (Privacy Act 1988 compliance)."""
    return await db.record_consent(
        user_id=consent.user_id,
        consent_type=consent.type,
        timestamp=datetime.now(timezone.utc),
        ip_address=consent.ip_address
    )
```

## Health Check

```python
@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "version": "1.0.0",
        "locale": "en-AU",
        "timestamp": datetime.now().isoformat()
    }
```

## Testing

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_create_user_australian_phone():
    """Test Australian phone validation."""
    response = client.post("/users/", json={
        "email": "test@example.com.au",
        "name": "Test User",
        "phone": "0412 345 678",
        "state": "QLD",
        "postcode": "4000"
    })
    assert response.status_code == 201
    assert response.json()["phone"] == "0412 345 678"

def test_invalid_phone_format():
    """Test invalid phone format rejected."""
    response = client.post("/users/", json={
        "email": "test@example.com.au",
        "name": "Test User",
        "phone": "1234567890"  # Invalid format
    })
    assert response.status_code == 422
```

## Integration with Skills

This skill works with:
- `backend/langgraph.skill.md` - Agent workflows
- `backend/advanced-tool-use.skill.md` - Tool patterns
- `database/supabase.skill.md` - Database integration

See: `apps/backend/src/api/`, `verification/verification-first.skill.md`
