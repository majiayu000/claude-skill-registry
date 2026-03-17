---
name: SQLAlchemy 2.0+
description: Modern async ORM with type-safe models and efficient queries
when_to_use: Building database backends, APIs, data services with async support
---

# SQLAlchemy 2.0+ Skill

## Quick Start

### Basic Setup

```python
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine, AsyncSession
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
import asyncio

# Base class for models
class Base(AsyncAttrs, DeclarativeBase):
    pass

# Async engine
engine = create_async_engine("postgresql+asyncpg://user:pass@localhost/db")

# Session factory
async_session = async_sessionmaker(engine, expire_on_commit=False)

# Example model
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50))
    email: Mapped[str] = mapped_column(String(100))
```

### Basic CRUD Operations

```python
async def create_user(name: str, email: str) -> User:
    async with async_session() as session:
        async with session.begin():
            user = User(name=name, email=email)
            session.add(user)
            await session.flush()  # Get the ID
            return user

async def get_user(user_id: int) -> User | None:
    async with async_session() as session:
        result = await session.execute(select(User).where(User.id == user_id))
        return result.scalar_one_or_none()

async def update_user_email(user_id: int, new_email: str) -> bool:
    async with async_session() as session:
        result = await session.execute(
            update(User).where(User.id == user_id).values(email=new_email)
        )
        await session.commit()
        return result.rowcount > 0
```

## Common Patterns

### Models

#### Annotated Type-Safe Models (Recommended)

```python
from typing_extensions import Annotated
from typing import List, Optional

# Reusable column types
intpk = Annotated[int, mapped_column(primary_key=True)]
str50 = Annotated[str, mapped_column(String(50))]
created_at = Annotated[datetime, mapped_column(insert_default=func.now())]

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[intpk]
    title: Mapped[str50]
    content: Mapped[str] = mapped_column(Text)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    created: Mapped[created_at]

    # Relationships
    author: Mapped["User"] = relationship(back_populates="posts")
    tags: Mapped[List["Tag"]] = relationship(secondary="post_tags")
```

#### Classic Style Models

```python
class Post(Base):
    __tablename__ = "posts"

    id = mapped_column(Integer, primary_key=True)
    title = mapped_column(String(50))
    content = mapped_column(Text)
    author_id = mapped_column(ForeignKey("users.id"))

    author = relationship("User", back_populates="posts")
```

### Relationships

#### One-to-Many

```python
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    posts: Mapped[List["Post"]] = relationship(
        back_populates="author",
        cascade="all, delete-orphan"
    )

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
```

#### Many-to-Many

```python
association_table = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", ForeignKey("posts.id"), primary_key=True),
    Column("tag_id", ForeignKey("tags.id"), primary_key=True)
)

class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    tags: Mapped[List["Tag"]] = relationship(
        secondary=association_table,
        back_populates="posts"
    )

class Tag(Base):
    __tablename__ = "tags"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(50), unique=True)
    posts: Mapped[List["Post"]] = relationship(
        secondary=association_table,
        back_populates="tags"
    )
```

### Queries

#### Basic Select

```python
from sqlalchemy import select, and_, or_

# Get all users
async def get_all_users():
    async with async_session() as session:
        result = await session.execute(select(User))
        return result.scalars().all()

# Filter with conditions
async def get_users_by_name(name: str):
    async with async_session() as session:
        stmt = select(User).where(User.name.ilike(f"%{name}%"))
        result = await session.execute(stmt)
        return result.scalars().all()

# Complex conditions
async def search_users(name: str = None, email: str = None):
    async with async_session() as session:
        conditions = []
        if name:
            conditions.append(User.name.ilike(f"%{name}%"))
        if email:
            conditions.append(User.email.ilike(f"%{email}%"))

        if conditions:
            stmt = select(User).where(and_(*conditions))
        else:
            stmt = select(User)

        result = await session.execute(stmt)
        return result.scalars().all()
```

#### Relationship Loading

```python
from sqlalchemy.orm import selectinload, joinedload

# Eager load relationships
async def get_posts_with_author():
    async with async_session() as session:
        stmt = select(Post).options(selectinload(Post.author))
        result = await session.execute(stmt)
        return result.scalars().all()

# Joined loading for single relationships
async def get_post_with_tags(post_id: int):
    async with async_session() as session:
        stmt = select(Post).options(
            joinedload(Post.author),
            selectinload(Post.tags)
        ).where(Post.id == post_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()
```

#### Pagination

```python
async def get_posts_paginated(page: int, size: int):
    async with async_session() as session:
        offset = (page - 1) * size
        stmt = select(Post).offset(offset).limit(size).order_by(Post.created.desc())
        result = await session.execute(stmt)
        return result.scalars().all()
```

#### Aggregations

```python
from sqlalchemy import func

async def get_user_post_count():
    async with async_session() as session:
        stmt = (
            select(User.name, func.count(Post.id).label("post_count"))
            .join(Post)
            .group_by(User.id, User.name)
            .order_by(func.count(Post.id).desc())
        )
        result = await session.execute(stmt)
        return result.all()
```

### Sessions Management

#### Context Manager Pattern

```python
async def create_post(title: str, content: str, author_id: int):
    async with async_session() as session:
        async with session.begin():
            post = Post(title=title, content=content, author_id=author_id)
            session.add(post)
            return post
```

#### Dependency Injection (FastAPI)

```python
from fastapi import Depends

async def get_db_session():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()

async def create_user_endpoint(
    user_data: UserCreate,
    session: AsyncSession = Depends(get_db_session)
):
    user = User(**user_data.dict())
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user
```

#### Scoped Sessions

```python
from sqlalchemy.ext.asyncio import async_scoped_session
import asyncio

# Create scoped session
async_session_scope = async_scoped_session(
    async_sessionmaker(engine, expire_on_commit=False),
    scopefunc=asyncio.current_task
)

# Use in application
async def some_function():
    session = async_session_scope()
    # Use session normally
    await session.commit()
```

### Advanced Patterns

#### Write-Only Relationships (Memory Efficient)

```python
from sqlalchemy.orm import WriteOnlyMapped

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    posts: WriteOnlyMapped["Post"] = relationship()

async def get_user_posts(user_id: int):
    async with async_session() as session:
        user = await session.get(User, user_id)
        if user:
            # Explicit select for collection
            stmt = select(Post).where(Post.author_id == user_id)
            result = await session.execute(stmt)
            return result.scalars().all()
        return []
```

#### Custom Session Classes

```python
class AsyncSessionWithDefaults(AsyncSession):
    async def execute_with_defaults(self, statement, **kwargs):
        # Add default options
        return await self.execute(statement, **kwargs)

# Use custom session
async_session = async_sessionmaker(
    engine,
    class_=AsyncSessionWithDefaults,
    expire_on_commit=False
)
```

#### Connection Routing

```python
class RoutingSession(Session):
    def get_bind(self, mapper=None, clause=None, **kw):
        if mapper and issubclass(mapper.class_, ReadOnlyModel):
            return read_engine
        return write_engine

class AsyncRoutingSession(AsyncSession):
    sync_session_class = RoutingSession
```

### Raw SQL

```python
from sqlalchemy import text

async def run_raw_sql():
    async with async_session() as session:
        result = await session.execute(text("SELECT COUNT(*) FROM users"))
        count = result.scalar()
        return count

async def run_parameterized_query(user_id: int):
    async with async_session() as session:
        stmt = text("SELECT * FROM posts WHERE author_id = :user_id")
        result = await session.execute(stmt, {"user_id": user_id})
        return result.fetchall()
```

## Performance Tips

1. **Use selectinload for collections**: More efficient than lazy loading
2. **Batch operations**: Use `add_all()` for bulk inserts
3. **Connection pooling**: Configure pool size based on load
4. **Index columns**: Add indexes for frequently queried columns
5. **Use streaming**: For large result sets, use `stream()`

```python
# Streaming large results
async def process_all_users():
    async with async_session() as session:
        result = await session.stream(select(User))
        async for user in result.scalars():
            # Process user without loading all into memory
            await process_user(user)
```

## Requirements

```bash
pip install sqlalchemy[asyncio]  # Core SQLAlchemy
pip install asyncpg             # PostgreSQL async driver
# or
pip install aiosqlite           # SQLite async driver
# or
pip install aiomysql            # MySQL async driver
```

## Database URLs

- **PostgreSQL**: `postgresql+asyncpg://user:pass@localhost/db`
- **SQLite**: `sqlite+aiosqlite:///database.db`
- **MySQL**: `mysql+aiomysql://user:pass@localhost/db`

## Migration Integration

Use Alembic for database migrations:

```python
# Generate migration
alembic revision --autogenerate -m "Add users table"

# Apply migrations
alembic upgrade head
```
