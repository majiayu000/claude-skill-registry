---
name: fastapi-backend
description: FastAPI best practices for building production Python backends. Use when building REST APIs, async endpoints, Pydantic models, dependency injection, middleware, or any FastAPI server.
---

# FastAPI Backend Patterns

## Project Structure
```
app/
  main.py          # FastAPI app, lifespan, middleware
  config.py        # Pydantic Settings, env vars
  models/          # SQLAlchemy ORM models
  schemas/         # Pydantic request/response schemas
  routers/         # APIRouter per domain (auth, users, posts)
  services/        # Business logic (no DB or HTTP here)
  deps.py          # Shared dependencies (get_db, get_current_user)
  database.py      # Engine, SessionLocal, Base
```

## Core Patterns

### App setup with lifespan
```python
from contextlib import asynccontextmanager
from fastapi import FastAPI

@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup
    await database.connect()
    yield
    # shutdown
    await database.disconnect()

app = FastAPI(lifespan=lifespan)
```

### Dependency injection
```python
# deps.py
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
) -> User:
    ...
```

### Router pattern
```python
router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    user = await db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### Error handling
```python
from fastapi import Request
from fastapi.responses import JSONResponse

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(status_code=400, content={"detail": str(exc)})
```

### Pydantic schemas
```python
class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    name: str = Field(max_length=100)

class UserResponse(BaseModel):
    id: int
    email: str
    name: str
    model_config = ConfigDict(from_attributes=True)
```

## Rules
- Always use async def for endpoints
- Validate ALL input with Pydantic (never trust raw dicts)
- Use HTTPException with specific status codes (not 500 for everything)
- Never put business logic in route handlers — use service layer
- Use response_model to control what's returned (never expose passwords)
- Add CORS middleware for browser clients
- Use Depends() for database sessions — never create sessions manually
