---
name: fastapi-production
description: Production-grade FastAPI patterns for async APIs, SQLAlchemy 2.0, Pydantic v2, and robust error handling. Use when building API endpoints, handling database operations, implementing middleware, or optimizing performance.
model_tier: opus
parallel_hints:
  can_parallel_with: [test-writer, security-audit, code-review]
  must_serialize_with: [database-migration]
  preferred_batch_size: 5
context_hints:
  max_file_context: 80
  compression_level: 1
  requires_git_context: true
  requires_db_context: true
escalation_triggers:
  - pattern: "auth|security|password|token"
    reason: "Authentication/authorization changes require security-audit"
  - pattern: "migration|schema"
    reason: "Database changes require database-migration skill"
  - keyword: ["rate limit", "ACGME", "external API"]
    reason: "Critical system changes need human approval"
---

# FastAPI Production Patterns Skill

Production-ready patterns for FastAPI applications with async SQLAlchemy, Pydantic validation, and enterprise-grade error handling.

## When This Skill Activates

- Building new API endpoints
- Database query optimization
- Error handling and validation
- Middleware implementation
- Authentication/authorization patterns
- Background task integration
- Performance optimization

## Project Architecture

```
backend/app/
├── api/
│   ├── deps.py          # Dependency injection
│   └── routes/          # API endpoints
├── controllers/         # Request/response handling
├── services/            # Business logic
├── repositories/        # Data access (optional)
├── models/              # SQLAlchemy ORM
├── schemas/             # Pydantic schemas
├── core/                # Config, security
└── db/                  # Database session
```

### Layer Responsibilities

```
Route (thin)     → Parse request, call controller/service, return response
Controller       → Orchestrate service calls, transform data
Service          → Business logic, validation, transactions
Repository       → Database queries (optional abstraction)
Model            → ORM definitions, relationships
Schema           → Request/response validation
```

## Route Patterns

### Standard CRUD Endpoint

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db, get_current_user
from app.schemas.schedule import ScheduleCreate, ScheduleResponse, ScheduleList
from app.services import schedule_service
from app.models.user import User

router = APIRouter(prefix="/schedules", tags=["schedules"])


@router.get("", response_model=ScheduleList)
async def list_schedules(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduleList:
    """
    List all schedules with pagination.

    - **skip**: Number of records to skip
    - **limit**: Maximum number of records to return
    """
    schedules = await schedule_service.get_multi(db, skip=skip, limit=limit)
    total = await schedule_service.count(db)
    return ScheduleList(items=schedules, total=total, skip=skip, limit=limit)


@router.get("/{schedule_id}", response_model=ScheduleResponse)
async def get_schedule(
    schedule_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduleResponse:
    """Get a specific schedule by ID."""
    schedule = await schedule_service.get(db, id=schedule_id)
    if not schedule:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Schedule not found",
        )
    return schedule


@router.post("", response_model=ScheduleResponse, status_code=status.HTTP_201_CREATED)
async def create_schedule(
    schedule_in: ScheduleCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> ScheduleResponse:
    """Create a new schedule."""
    schedule = await schedule_service.create(db, obj_in=schedule_in, created_by=current_user.id)
    return schedule
```

### Bulk Operations

```python
from typing import List

@router.post("/bulk", response_model=List[ScheduleResponse])
async def create_schedules_bulk(
    schedules_in: List[ScheduleCreate],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> List[ScheduleResponse]:
    """Create multiple schedules in a single transaction."""
    if len(schedules_in) > 100:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Maximum 100 schedules per request",
        )

    async with db.begin():
        schedules = await schedule_service.create_multi(
            db, objs_in=schedules_in, created_by=current_user.id
        )
    return schedules
```

## Pydantic Schema Patterns

### Request/Response Separation

```python
from pydantic import BaseModel, Field, field_validator
from datetime import date, datetime
from typing import Optional, List


# Base schema with shared fields
class ScheduleBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    start_date: date
    end_date: date

    @field_validator("end_date")
    @classmethod
    def end_date_after_start(cls, v: date, info) -> date:
        if "start_date" in info.data and v < info.data["start_date"]:
            raise ValueError("end_date must be after start_date")
        return v


# Create schema - fields required for creation
class ScheduleCreate(ScheduleBase):
    description: Optional[str] = None


# Update schema - all fields optional
class ScheduleUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    description: Optional[str] = None


# Response schema - includes DB fields
class ScheduleResponse(ScheduleBase):
    id: str
    description: Optional[str]
    created_at: datetime
    updated_at: Optional[datetime]
    created_by: str

    model_config = {"from_attributes": True}


# List response with pagination
class ScheduleList(BaseModel):
    items: List[ScheduleResponse]
    total: int
    skip: int
    limit: int
```

### Nested Schemas

```python
class AssignmentResponse(BaseModel):
    id: str
    person_id: str
    block_id: str
    rotation_type: str

    model_config = {"from_attributes": True}


class ScheduleWithAssignments(ScheduleResponse):
    assignments: List[AssignmentResponse] = []
```

## Service Layer Patterns

### Service Structure

```python
from typing import Optional, List, TypeVar, Generic
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from pydantic import BaseModel

from app.models.schedule import Schedule
from app.schemas.schedule import ScheduleCreate, ScheduleUpdate


class ScheduleService:
    """Service for schedule business logic."""

    async def get(self, db: AsyncSession, *, id: str) -> Optional[Schedule]:
        """Get a schedule by ID."""
        result = await db.execute(select(Schedule).where(Schedule.id == id))
        return result.scalar_one_or_none()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 100,
    ) -> List[Schedule]:
        """Get multiple schedules with pagination."""
        result = await db.execute(
            select(Schedule)
            .offset(skip)
            .limit(limit)
            .order_by(Schedule.created_at.desc())
        )
        return list(result.scalars().all())

    async def count(self, db: AsyncSession) -> int:
        """Count total schedules."""
        result = await db.execute(select(func.count()).select_from(Schedule))
        return result.scalar() or 0

    async def create(
        self,
        db: AsyncSession,
        *,
        obj_in: ScheduleCreate,
        created_by: str,
    ) -> Schedule:
        """Create a new schedule."""
        db_obj = Schedule(
            **obj_in.model_dump(),
            created_by=created_by,
        )
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: AsyncSession,
        *,
        db_obj: Schedule,
        obj_in: ScheduleUpdate,
    ) -> Schedule:
        """Update an existing schedule."""
        update_data = obj_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.add(db_obj)
        await db.flush()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, *, id: str) -> bool:
        """Delete a schedule by ID."""
        obj = await self.get(db, id=id)
        if obj:
            await db.delete(obj)
            await db.flush()
            return True
        return False


# Singleton instance
schedule_service = ScheduleService()
```

### Business Logic with Validation

```python
from app.scheduling.acgme_validator import ACGMEValidator


class AssignmentService:
    """Service with business logic and validation."""

    def __init__(self):
        self.validator = ACGMEValidator()

    async def create_assignment(
        self,
        db: AsyncSession,
        *,
        obj_in: AssignmentCreate,
        created_by: str,
    ) -> Assignment:
        """Create assignment with ACGME validation."""
        # Check existing assignments for conflicts
        conflicts = await self._check_conflicts(db, obj_in)
        if conflicts:
            raise ValueError(f"Assignment conflicts with: {conflicts}")

        # Validate ACGME compliance
        violations = await self.validator.validate_assignment(db, obj_in)
        if violations:
            raise ACGMEViolationError(violations)

        # Create assignment
        assignment = Assignment(**obj_in.model_dump(), created_by=created_by)
        db.add(assignment)
        await db.flush()

        return assignment

    async def _check_conflicts(
        self,
        db: AsyncSession,
        obj_in: AssignmentCreate,
    ) -> List[Assignment]:
        """Check for conflicting assignments."""
        result = await db.execute(
            select(Assignment)
            .where(Assignment.person_id == obj_in.person_id)
            .where(Assignment.block_id == obj_in.block_id)
        )
        return list(result.scalars().all())
```

## Database Query Patterns

### Eager Loading (Prevent N+1)

```python
from sqlalchemy.orm import selectinload, joinedload

async def get_schedule_with_assignments(
    db: AsyncSession, schedule_id: str
) -> Optional[Schedule]:
    """Get schedule with all assignments eagerly loaded."""
    result = await db.execute(
        select(Schedule)
        .options(
            selectinload(Schedule.assignments).selectinload(Assignment.person),
            selectinload(Schedule.assignments).selectinload(Assignment.block),
        )
        .where(Schedule.id == schedule_id)
    )
    return result.scalar_one_or_none()
```

### Complex Queries

```python
from sqlalchemy import and_, or_, func
from datetime import date, timedelta


async def get_upcoming_assignments(
    db: AsyncSession,
    person_id: str,
    days_ahead: int = 7,
) -> List[Assignment]:
    """Get assignments for the next N days."""
    today = date.today()
    end_date = today + timedelta(days=days_ahead)

    result = await db.execute(
        select(Assignment)
        .join(Block)
        .where(
            and_(
                Assignment.person_id == person_id,
                Block.date >= today,
                Block.date <= end_date,
            )
        )
        .order_by(Block.date, Block.session)
    )
    return list(result.scalars().all())


async def get_coverage_stats(
    db: AsyncSession,
    schedule_id: str,
) -> dict:
    """Get coverage statistics for a schedule."""
    result = await db.execute(
        select(
            Block.date,
            func.count(Assignment.id).label("assigned_count"),
        )
        .outerjoin(Assignment, Assignment.block_id == Block.id)
        .where(Assignment.schedule_id == schedule_id)
        .group_by(Block.date)
    )

    return {row.date: row.assigned_count for row in result.all()}
```

### Row Locking for Concurrency

```python
from sqlalchemy import select
from sqlalchemy.orm import with_for_update


async def update_with_lock(
    db: AsyncSession,
    assignment_id: str,
    new_status: str,
) -> Assignment:
    """Update with row lock to prevent race conditions."""
    result = await db.execute(
        select(Assignment)
        .where(Assignment.id == assignment_id)
        .with_for_update()  # Lock the row
    )
    assignment = result.scalar_one_or_none()

    if not assignment:
        raise ValueError("Assignment not found")

    assignment.status = new_status
    await db.flush()
    return assignment
```

## Error Handling

### Custom Exception Classes

```python
# app/core/exceptions.py
from typing import Any, Optional


class AppException(Exception):
    """Base application exception."""

    def __init__(
        self,
        message: str,
        code: str = "APP_ERROR",
        details: Optional[dict] = None,
    ):
        self.message = message
        self.code = code
        self.details = details or {}
        super().__init__(message)


class NotFoundError(AppException):
    """Resource not found."""

    def __init__(self, resource: str, id: str):
        super().__init__(
            message=f"{resource} not found",
            code="NOT_FOUND",
            details={"resource": resource, "id": id},
        )


class ValidationError(AppException):
    """Validation failed."""

    def __init__(self, errors: list):
        super().__init__(
            message="Validation failed",
            code="VALIDATION_ERROR",
            details={"errors": errors},
        )


class ACGMEViolationError(AppException):
    """ACGME compliance violation."""

    def __init__(self, violations: list):
        super().__init__(
            message="ACGME compliance violation",
            code="ACGME_VIOLATION",
            details={"violations": violations},
        )
```

### Global Exception Handler

```python
# app/api/exception_handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse

from app.core.exceptions import AppException, NotFoundError, ValidationError


async def app_exception_handler(request: Request, exc: AppException) -> JSONResponse:
    """Handle application exceptions."""
    status_map = {
        "NOT_FOUND": status.HTTP_404_NOT_FOUND,
        "VALIDATION_ERROR": status.HTTP_400_BAD_REQUEST,
        "ACGME_VIOLATION": status.HTTP_422_UNPROCESSABLE_ENTITY,
    }

    return JSONResponse(
        status_code=status_map.get(exc.code, status.HTTP_500_INTERNAL_SERVER_ERROR),
        content={
            "error": {
                "code": exc.code,
                "message": exc.message,
                "details": exc.details,
            }
        },
    )


# Register in main.py
app.add_exception_handler(AppException, app_exception_handler)
```

## Dependency Injection

### Database Session

```python
# app/api/deps.py
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import async_session


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Dependency for database session."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

### Current User

```python
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_token
from app.models.user import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    """Get current authenticated user."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_token(token)
    if payload is None:
        raise credentials_exception

    user_id = payload.get("sub")
    if user_id is None:
        raise credentials_exception

    user = await user_service.get(db, id=user_id)
    if user is None:
        raise credentials_exception

    return user


async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    """Ensure user is active."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user",
        )
    return current_user
```

### Role-Based Access

```python
from functools import wraps
from typing import List


def require_roles(roles: List[str]):
    """Dependency factory for role-based access."""

    async def role_checker(
        current_user: User = Depends(get_current_active_user),
    ) -> User:
        if current_user.role not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Insufficient permissions",
            )
        return current_user

    return role_checker


# Usage
@router.delete("/{schedule_id}")
async def delete_schedule(
    schedule_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(require_roles(["ADMIN", "COORDINATOR"])),
) -> dict:
    """Delete a schedule (admin/coordinator only)."""
    await schedule_service.delete(db, id=schedule_id)
    return {"status": "deleted"}
```

## Background Tasks

### FastAPI Background Tasks

```python
from fastapi import BackgroundTasks


async def send_notification(user_id: str, message: str):
    """Background task to send notification."""
    # Implementation
    pass


@router.post("/assignments")
async def create_assignment(
    assignment_in: AssignmentCreate,
    background_tasks: BackgroundTasks,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Create assignment and notify affected users."""
    assignment = await assignment_service.create(db, obj_in=assignment_in)

    # Add background task
    background_tasks.add_task(
        send_notification,
        assignment.person_id,
        f"New assignment: {assignment.rotation_type}",
    )

    return assignment
```

### Celery Integration

```python
from app.core.celery import celery_app


@celery_app.task(bind=True, max_retries=3)
def generate_schedule_task(self, schedule_id: str, params: dict):
    """Celery task for schedule generation."""
    try:
        # Long-running operation
        result = generate_schedule(schedule_id, **params)
        return {"status": "success", "result": result}
    except Exception as exc:
        self.retry(exc=exc, countdown=60)


@router.post("/schedules/{schedule_id}/generate")
async def trigger_generation(
    schedule_id: str,
    params: GenerationParams,
    current_user: User = Depends(get_current_user),
):
    """Trigger async schedule generation."""
    task = generate_schedule_task.delay(schedule_id, params.model_dump())
    return {"task_id": task.id, "status": "queued"}
```

## Performance Patterns

### Response Caching

```python
from functools import lru_cache
from fastapi_cache import FastAPICache
from fastapi_cache.decorator import cache


@router.get("/stats")
@cache(expire=300)  # Cache for 5 minutes
async def get_stats(db: AsyncSession = Depends(get_db)):
    """Get cached statistics."""
    return await stats_service.calculate(db)
```

### Streaming Responses

```python
from fastapi.responses import StreamingResponse
import csv
import io


@router.get("/export/csv")
async def export_csv(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Stream large CSV export."""

    async def generate_csv():
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(["ID", "Name", "Date"])

        async for batch in get_data_batches(db):
            for row in batch:
                writer.writerow([row.id, row.name, row.date])
                yield output.getvalue()
                output.seek(0)
                output.truncate(0)

    return StreamingResponse(
        generate_csv(),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=export.csv"},
    )
```

## Commands

```bash
cd /home/user/Autonomous-Assignment-Program-Manager/backend

# Development
uvicorn app.main:app --reload

# Testing
pytest
pytest --cov=app

# Linting
ruff check app/
ruff format app/

# Type checking
mypy app/

# Database
alembic upgrade head
alembic revision --autogenerate -m "description"
```

## Integration with Other Skills

### With database-migration
For schema changes:
1. Modify model
2. Use database-migration skill for Alembic
3. Update Pydantic schemas to match

### With security-audit
For auth/security code:
1. Defer to security-audit for review
2. Follow OWASP guidelines
3. Validate HIPAA compliance

### With test-writer
After creating endpoints:
1. test-writer generates API tests
2. Cover happy path and errors
3. Test auth/permissions

## Escalation Rules

**Escalate to human when:**

1. Authentication/authorization changes
2. Database schema modifications
3. ACGME compliance logic changes
4. Rate limiting configuration
5. External API integrations
6. Performance-critical optimizations
