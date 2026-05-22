---
name: py-sqlmodel-patterns
description: SQLModel and async SQLAlchemy patterns. Use when working with database models, queries, relationships, or debugging ORM issues.
---

# SQLModel Patterns

## Problem Statement

SQLModel combines Pydantic and SQLAlchemy, blurring the line between models and schemas. Async SQLAlchemy has different rules than sync. Mistakes here cause data corruption, N+1 queries, and hard-to-debug errors.

---

## Pattern: Eager Loading for Async

**Problem:** Lazy loading doesn't work with async SQLAlchemy. Accessing relationships without eager loading raises errors.

```python
# ❌ WRONG: Lazy loading fails in async
result = await session.execute(select(User).where(User.id == user_id))
user = result.scalar_one()
assessments = user.assessments  # ERROR: greenlet_spawn has not been called

# ✅ CORRECT: selectinload for collections
from sqlalchemy.orm import selectinload

result = await session.execute(
    select(User)
    .where(User.id == user_id)
    .options(selectinload(User.assessments))
)
user = result.scalar_one()
assessments = user.assessments  # Works - already loaded

# ✅ CORRECT: joinedload for single relationships
from sqlalchemy.orm import joinedload

result = await session.execute(
    select(Assessment)
    .where(Assessment.id == assessment_id)
    .options(joinedload(Assessment.user))
)
assessment = result.scalar_one()
user = assessment.user  # Works - already loaded
```

**When to use which:**

| Relationship | Loading Strategy |
|--------------|------------------|
| One-to-many (collections) | `selectinload()` |
| Many-to-one (single) | `joinedload()` |
| Nested relationships | Chain: `.options(selectinload(A.b).selectinload(B.c))` |

---

## Pattern: N+1 Query Detection

**Problem:** Fetching related objects one-by-one instead of in batch.

```python
# ❌ WRONG: N+1 queries
users = await session.execute(select(User))
for user in users.scalars():
    # Each access triggers a query!
    print(user.team.name)  # Query 1, 2, 3... N

# ✅ CORRECT: Single query with eager loading
users = await session.execute(
    select(User).options(joinedload(User.team))
)
for user in users.scalars():
    print(user.team.name)  # No additional queries

# Detection: Enable SQL echo in development
engine = create_async_engine(DATABASE_URL, echo=True)
# Watch logs for repeated similar queries
```

---

## Pattern: Model vs Schema Separation

**Problem:** SQLModel blurs models (DB) and schemas (API). Need clear separation.

```python
# Database Model - represents table
class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    email: str = Field(index=True, unique=True)
    hashed_password: str  # Never expose this
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Relationships
    assessments: list["Assessment"] = Relationship(back_populates="user")

# API Schema - Create (input)
class UserCreate(SQLModel):
    email: str
    password: str  # Plain password, will be hashed

# API Schema - Read (output)
class UserRead(SQLModel):
    id: UUID
    email: str
    created_at: datetime
    # Note: No password field!

# API Schema - Update (partial)
class UserUpdate(SQLModel):
    email: str | None = None
    password: str | None = None
```

**Naming convention:**
- `ModelName` - Database table model
- `ModelNameCreate` - Input for creation
- `ModelNameRead` - Output for reading
- `ModelNameUpdate` - Input for partial updates

---

## Pattern: Session State Management

**Problem:** Understanding `expire_on_commit` and when objects become stale.

```python
# This codebase setting
async_session = async_sessionmaker(
    engine,
    expire_on_commit=False,  # Objects stay valid after commit
)

# With expire_on_commit=False:
user = User(email="test@example.com")
session.add(user)
await session.commit()
print(user.email)  # Works - object still valid

# With expire_on_commit=True (default):
await session.commit()
print(user.email)  # Would need refresh() first

# ✅ CORRECT: Refresh when you need DB-generated values
await session.commit()
await session.refresh(user)  # Get id, created_at, updated DB values
return user
```

---

## Pattern: UUID Handling

**Problem:** Inconsistent UUID handling between Python and PostgreSQL.

```python
from uuid import UUID, uuid4

# ✅ CORRECT: UUID with default factory
class Assessment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")

# ✅ CORRECT: UUID in queries
await session.execute(
    select(Assessment).where(Assessment.id == UUID("..."))
)

# ❌ WRONG: String comparison
await session.execute(
    select(Assessment).where(Assessment.id == "some-uuid-string")
)

# ✅ CORRECT: Converting in API layer
@router.get("/assessments/{assessment_id}")
async def get_assessment(assessment_id: UUID):  # FastAPI converts string to UUID
    ...
```

---

## Pattern: Nullable Fields

**Problem:** SQLModel requires specific syntax for optional fields.

```python
# ✅ CORRECT: Optional field with None default
class Assessment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    title: str  # Required
    description: str | None = Field(default=None)  # Optional
    completed_at: datetime | None = Field(default=None)  # Optional
    
    # Foreign key that's optional
    coach_id: UUID | None = Field(default=None, foreign_key="user.id")

# ❌ WRONG: Optional without Field default
class BadModel(SQLModel, table=True):
    description: str | None  # Missing default - causes issues
```

---

## Pattern: Relationship Definitions

```python
from sqlmodel import Relationship

class User(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    
    # One-to-many: User has many assessments
    assessments: list["Assessment"] = Relationship(back_populates="user")
    
    # One-to-many: User has many answers
    answers: list["UserAnswer"] = Relationship(back_populates="user")

class Assessment(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="user.id")
    
    # Many-to-one: Assessment belongs to user
    user: User = Relationship(back_populates="assessments")
    
    # One-to-many: Assessment has many questions
    questions: list["Question"] = Relationship(back_populates="assessment")

class Question(SQLModel, table=True):
    id: UUID = Field(default_factory=uuid4, primary_key=True)
    assessment_id: UUID = Field(foreign_key="assessment.id")
    
    # Many-to-one
    assessment: Assessment = Relationship(back_populates="questions")
```

---

## Pattern: Query Patterns

```python
# Get one or None
result = await session.execute(
    select(User).where(User.id == user_id)
)
user = result.scalar_one_or_none()

# Get one or raise
user = result.scalar_one()  # Raises if 0 or >1 results

# Get list
result = await session.execute(
    select(Assessment).where(Assessment.user_id == user_id)
)
assessments = result.scalars().all()

# Get with pagination
result = await session.execute(
    select(Assessment)
    .where(Assessment.user_id == user_id)
    .order_by(Assessment.created_at.desc())
    .offset(skip)
    .limit(limit)
)

# Count
result = await session.execute(
    select(func.count()).select_from(Assessment).where(...)
)
count = result.scalar_one()

# Exists check
result = await session.execute(
    select(exists().where(User.email == email))
)
email_exists = result.scalar()
```

---

## Pattern: Upsert (Insert or Update)

```python
from sqlalchemy.dialects.postgresql import insert

# ✅ CORRECT: PostgreSQL upsert
stmt = insert(UserAnswer).values(
    user_id=user_id,
    question_id=question_id,
    value=value,
)
stmt = stmt.on_conflict_do_update(
    index_elements=["user_id", "question_id"],
    set_={"value": value, "updated_at": datetime.utcnow()},
)
await session.execute(stmt)
await session.commit()
```

---

## References

- SQLModel documentation: https://sqlmodel.tiangolo.com/
- SQLAlchemy 2.0 documentation: https://docs.sqlalchemy.org/

---

## Common Issues

| Issue | Likely Cause | Solution |
|-------|--------------|----------|
| "greenlet_spawn has not been called" | Lazy loading in async | Use `selectinload`/`joinedload` |
| N+1 queries (slow) | Missing eager loading | Add appropriate loading strategy |
| "Object not bound to session" | Using object after session closed | Keep operations within session scope |
| Stale data | Missing `refresh()` | Call `refresh()` after commit |
| "None is not valid" for UUID | Missing `default_factory` | Add `Field(default_factory=uuid4)` |

---

## Detection Commands

```bash
# Find lazy relationship access
grep -rn "\.scalars\(\)" --include="*.py" -A5 | grep -E "\.\w+\s*$"

# Find models missing relationship loading
grep -rn "select(" --include="*.py" | grep -v "options("

# Check for N+1 in logs (with echo=True)
# Look for repeated similar queries
```
