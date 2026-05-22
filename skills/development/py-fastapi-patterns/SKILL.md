---
name: py-fastapi-patterns
description: FastAPI patterns for API design. Use when creating endpoints, handling dependencies, error handling, or working with OpenAPI schemas.
---

# FastAPI Patterns

## Problem Statement

FastAPI API design directly affects frontend. Bad patterns here cause frontend bugs, poor developer experience, and integration issues. The OpenAPI schema drives frontend code generation.

---

## Pattern: Dependency Injection

**Problem:** Repetitive code for auth, sessions, and services.

```python
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

# ✅ CORRECT: Dependencies for common needs
async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

async def get_current_user(
    token: str = Depends(oauth2_scheme),
    session: AsyncSession = Depends(get_session),
) -> User:
    user = await verify_token_and_get_user(token, session)
    if not user:
        raise HTTPException(401, "Invalid authentication")
    return user

async def get_current_active_user(
    user: User = Depends(get_current_user),
) -> User:
    if not user.is_active:
        raise HTTPException(403, "User is inactive")
    return user

# ✅ CORRECT: Endpoint using dependencies
@router.post("/assessments", response_model=AssessmentRead)
async def create_assessment(
    data: AssessmentCreate,
    current_user: User = Depends(get_current_active_user),
    session: AsyncSession = Depends(get_session),
) -> AssessmentRead:
    assessment = Assessment(**data.model_dump(), user_id=current_user.id)
    session.add(assessment)
    await session.commit()
    await session.refresh(assessment)
    return assessment
```

**Dependency chain:** `get_session` → `get_current_user` → `get_current_active_user`

---

## Pattern: Response Models

**Problem:** Inconsistent responses, exposing internal fields, poor OpenAPI docs.

```python
# ✅ CORRECT: Explicit response_model
@router.get("/users/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_session),
) -> UserRead:
    user = await get_user_or_404(user_id, session)
    return user  # Automatically filtered to UserRead fields

# ✅ CORRECT: List response
@router.get("/users", response_model=list[UserRead])
async def list_users(...) -> list[UserRead]:
    ...

# ✅ CORRECT: Paginated response
class PaginatedResponse(SQLModel, Generic[T]):
    items: list[T]
    total: int
    page: int
    size: int

@router.get("/assessments", response_model=PaginatedResponse[AssessmentRead])
async def list_assessments(...):
    ...

# ❌ WRONG: No response_model (exposes everything)
@router.get("/users/{user_id}")
async def get_user(user_id: UUID) -> User:  # Exposes hashed_password!
    ...
```

**Why response_model matters:**
1. Filters output to only specified fields
2. Generates accurate OpenAPI schema
3. Frontend Orval codegen depends on this

---

## Pattern: Error Handling

**Problem:** Inconsistent error responses, missing context.

```python
from fastapi import HTTPException, status

# ✅ CORRECT: Specific HTTP exceptions
@router.get("/assessments/{id}")
async def get_assessment(id: UUID, session: AsyncSession = Depends(get_session)):
    result = await session.execute(
        select(Assessment).where(Assessment.id == id)
    )
    assessment = result.scalar_one_or_none()
    
    if not assessment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Assessment {id} not found",
        )
    
    return assessment

# ✅ CORRECT: Custom exception with handler
class AssessmentNotFoundError(Exception):
    def __init__(self, assessment_id: UUID):
        self.assessment_id = assessment_id

@app.exception_handler(AssessmentNotFoundError)
async def assessment_not_found_handler(request: Request, exc: AssessmentNotFoundError):
    return JSONResponse(
        status_code=404,
        content={
            "detail": f"Assessment {exc.assessment_id} not found",
            "error_code": "ASSESSMENT_NOT_FOUND",
        },
    )

# ✅ CORRECT: Validation error detail
@router.post("/assessments")
async def create_assessment(data: AssessmentCreate):
    if data.end_date < data.start_date:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="end_date must be after start_date",
        )
```

**HTTP Status Codes:**

| Code | Use For |
|------|---------|
| 200 | Successful GET, PUT, PATCH |
| 201 | Successful POST (created) |
| 204 | Successful DELETE (no content) |
| 400 | Bad request (malformed) |
| 401 | Unauthorized (not authenticated) |
| 403 | Forbidden (authenticated but not allowed) |
| 404 | Not found |
| 422 | Validation error |
| 500 | Server error |

---

## Pattern: Route Ordering

**Problem:** FastAPI matches first route. Order matters for overlapping paths.

```python
# ❌ WRONG: Generic route before specific
@router.get("/users/{user_id}")  # This catches "me" as user_id!
async def get_user(user_id: str):
    ...

@router.get("/users/me")  # Never reached
async def get_current_user():
    ...

# ✅ CORRECT: Specific routes before generic
@router.get("/users/me")  # Specific first
async def get_current_user():
    ...

@router.get("/users/{user_id}")  # Generic after
async def get_user(user_id: UUID):  # UUID type also helps
    ...
```

**Remember:** Always define specific routes before generic parameterized routes.

---

## Pattern: Path and Query Parameters

```python
# Path parameter - required, part of URL
@router.get("/users/{user_id}")
async def get_user(user_id: UUID):  # /users/123
    ...

# Query parameters - optional, after ?
@router.get("/assessments")
async def list_assessments(
    status: str | None = None,        # /assessments?status=active
    skip: int = 0,                     # /assessments?skip=10
    limit: int = Query(default=20, le=100),  # With validation
):
    ...

# Enum for constrained values
class AssessmentStatus(str, Enum):
    DRAFT = "draft"
    ACTIVE = "active"
    COMPLETED = "completed"

@router.get("/assessments")
async def list_assessments(status: AssessmentStatus | None = None):
    ...
```

---

## Pattern: Request Body Validation

```python
from pydantic import Field, field_validator

class AssessmentCreate(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: str | None = Field(default=None, max_length=1000)
    skill_areas: list[str] = Field(min_length=1)
    
    @field_validator("skill_areas")
    @classmethod
    def validate_skill_areas(cls, v: list[str]) -> list[str]:
        valid_areas = {"fundamentals", "advanced", "strategy"}
        for area in v:
            if area not in valid_areas:
                raise ValueError(f"Invalid skill area: {area}")
        return v

# Automatic validation - returns 422 on failure
@router.post("/assessments", response_model=AssessmentRead)
async def create_assessment(data: AssessmentCreate):
    ...
```

---

## Pattern: Middleware

**Problem:** Cross-cutting concerns like logging, CORS, timing.

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time

app = FastAPI()

# CORS - order matters, add early
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Or ["*"] for dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Custom timing middleware
@app.middleware("http")
async def add_timing_header(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    response.headers["X-Process-Time"] = str(duration)
    return response

# Middleware order: Last added = First executed
```

---

## Pattern: OpenAPI Schema

**Problem:** Schema affects frontend codegen. Keep it clean.

```python
from fastapi import FastAPI

app = FastAPI(
    title="My API",
    version="1.0.0",
    description="API description here",
)

# Good schema descriptions
class AssessmentCreate(SQLModel):
    """Create a new skill assessment."""
    
    title: str = Field(description="Assessment title shown to user")
    skill_areas: list[str] = Field(
        description="List of skill areas to assess",
        examples=[["fundamentals", "strategy"]],
    )

# Endpoint documentation
@router.post(
    "/assessments",
    response_model=AssessmentRead,
    summary="Create assessment",
    description="Creates a new skill assessment for the current user.",
    responses={
        201: {"description": "Assessment created successfully"},
        422: {"description": "Validation error"},
    },
)
async def create_assessment(data: AssessmentCreate):
    ...
```

---

## Pattern: Router Organization

```python
# app/routers/assessments.py
from fastapi import APIRouter

router = APIRouter(
    prefix="/assessments",
    tags=["Assessments"],
)

@router.get("/")
async def list_assessments():
    ...

@router.post("/")
async def create_assessment():
    ...

# app/main.py
from app.routers import assessments, users, training

app.include_router(assessments.router, prefix="/api")
app.include_router(users.router, prefix="/api")
app.include_router(training.router, prefix="/api")
```

---

## References

- OpenAPI at `/docs` or `/openapi.json`
- FastAPI documentation: https://fastapi.tiangolo.com/

---

## Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| Wrong endpoint matched | Route ordering | Put specific routes before generic |
| Internal fields exposed | Missing response_model | Add `response_model=` |
| 422 errors on valid input | Pydantic v2 strictness | Check field validators |
| CORS errors | Missing/wrong middleware | Add CORSMiddleware first |
| Frontend types wrong | Schema mismatch | Check OpenAPI, regenerate API client |

---

## Detection Commands

```bash
# Find endpoints missing response_model
grep -rn "@router\." --include="*.py" | grep -v "response_model"

# Find potential route ordering issues
grep -rn "@router.get" --include="*.py" | grep -E '"/\w+/\{|"/\w+/\w+"'

# Check OpenAPI schema
curl http://localhost:8000/openapi.json | jq '.paths'
```
