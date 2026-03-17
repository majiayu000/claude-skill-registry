---
name: python-database-patterns
description: "SQLAlchemy and database patterns for Python. Triggers on: sqlalchemy, database, orm, migration, alembic, async database, connection pool, repository pattern, unit of work."
compatibility: "SQLAlchemy 2.0+, Python 3.10+. Async requires asyncpg (PostgreSQL) or aiosqlite."
allowed-tools: "Read Write Bash"
depends-on: [python-typing-patterns, python-async-patterns]
related-skills: [python-fastapi-patterns]
---

# Python Database Patterns

SQLAlchemy 2.0 and database best practices.

## SQLAlchemy 2.0 Basics

```python
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))
    email: Mapped[str] = mapped_column(String(255), unique=True)
    is_active: Mapped[bool] = mapped_column(default=True)

# Create engine and tables
engine = create_engine("postgresql://user:pass@localhost/db")
Base.metadata.create_all(engine)

# Query with 2.0 style
with Session(engine) as session:
    stmt = select(User).where(User.is_active == True)
    users = session.execute(stmt).scalars().all()
```

## Async SQLAlchemy

```python
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import select

# Async engine
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost/db",
    echo=False,
    pool_size=5,
    max_overflow=10,
)

# Session factory
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Usage
async with async_session() as session:
    result = await session.execute(select(User).where(User.id == 1))
    user = result.scalar_one_or_none()
```

## Model Relationships

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]

    # One-to-many
    posts: Mapped[list["Post"]] = relationship(back_populates="author")

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))

    # Many-to-one
    author: Mapped["User"] = relationship(back_populates="posts")
```

## Common Query Patterns

```python
from sqlalchemy import select, and_, or_, func

# Basic select
stmt = select(User).where(User.is_active == True)

# Multiple conditions
stmt = select(User).where(
    and_(
        User.is_active == True,
        User.age >= 18
    )
)

# OR conditions
stmt = select(User).where(
    or_(User.role == "admin", User.role == "moderator")
)

# Ordering and limiting
stmt = select(User).order_by(User.created_at.desc()).limit(10)

# Aggregates
stmt = select(func.count(User.id)).where(User.is_active == True)

# Joins
stmt = select(User, Post).join(Post, User.id == Post.author_id)

# Eager loading
from sqlalchemy.orm import selectinload
stmt = select(User).options(selectinload(User.posts))
```

## FastAPI Integration

```python
from fastapi import Depends, FastAPI
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

DB = Annotated[AsyncSession, Depends(get_db)]

@app.get("/users/{user_id}")
async def get_user(user_id: int, db: DB):
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=404)
    return user
```

## Quick Reference

| Operation | SQLAlchemy 2.0 Style |
|-----------|---------------------|
| Select all | `select(User)` |
| Filter | `.where(User.id == 1)` |
| First | `.scalar_one_or_none()` |
| All | `.scalars().all()` |
| Count | `select(func.count(User.id))` |
| Join | `.join(Post)` |
| Eager load | `.options(selectinload(User.posts))` |

## Additional Resources

- `./references/sqlalchemy-async.md` - Async patterns, session management
- `./references/connection-pooling.md` - Pool configuration, health checks
- `./references/transactions.md` - Transaction patterns, isolation levels
- `./references/migrations.md` - Alembic setup, migration strategies

## Assets

- `./assets/alembic.ini.template` - Alembic configuration template

---

## See Also

**Prerequisites:**
- `python-typing-patterns` - Mapped types and annotations
- `python-async-patterns` - Async database sessions

**Related Skills:**
- `python-fastapi-patterns` - Dependency injection for DB sessions
- `python-pytest-patterns` - Database fixtures and testing
