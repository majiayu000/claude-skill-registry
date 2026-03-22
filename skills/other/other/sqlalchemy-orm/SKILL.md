---
name: sqlalchemy-orm
description: SQLAlchemy 2.0 async ORM patterns. Use when defining models, relationships, queries, or migrations with SQLAlchemy in Python.
---

# SQLAlchemy 2.0 Async ORM Patterns

## Database Setup
```python
# database.py
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine(
    settings.DATABASE_URL,  # postgresql+asyncpg://user:pass@host/db
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,  # Verify connection before use
    echo=settings.DEBUG,
)

AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)

class Base(DeclarativeBase):
    pass
```

## Model Pattern
```python
from sqlalchemy import String, ForeignKey, func, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now(), nullable=False
    )

class User(Base, TimestampMixin):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    hashed_password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, server_default=text("true"))

    # Relationship
    posts: Mapped[list["Post"]] = relationship("Post", back_populates="author", lazy="select")

class Post(Base, TimestampMixin):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    body: Mapped[str] = mapped_column(nullable=False)

    author: Mapped["User"] = relationship("User", back_populates="posts")
```

## CRUD Patterns
```python
# SELECT with filter
async def get_user(db: AsyncSession, user_id: int) -> User | None:
    return await db.get(User, user_id)

async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    result = await db.execute(select(User).where(User.email == email))
    return result.scalar_one_or_none()

# SELECT with join (avoid N+1)
async def get_posts_with_authors(db: AsyncSession) -> list[Post]:
    result = await db.execute(
        select(Post).options(selectinload(Post.author)).order_by(Post.created_at.desc())
    )
    return list(result.scalars())

# INSERT
async def create_user(db: AsyncSession, data: UserCreate) -> User:
    user = User(**data.model_dump())
    db.add(user)
    await db.flush()  # Get ID without committing
    await db.refresh(user)
    return user

# UPDATE
async def update_user(db: AsyncSession, user_id: int, data: dict) -> User:
    await db.execute(update(User).where(User.id == user_id).values(**data))
    return await get_user(db, user_id)

# Bulk insert
async def bulk_create_posts(db: AsyncSession, posts: list[dict]):
    await db.execute(insert(Post), posts)
```

## Rules
- Use `selectinload()` or `joinedload()` for relationships — never lazy load in async
- Use `expire_on_commit=False` in async sessions
- `flush()` to get IDs mid-transaction, `commit()` only at end of request
- Rollback on exception (handled by Depends(get_db))
- Use `mapped_column()` not `Column()` (SQLAlchemy 2.0 style)
- Add `index=True` on all ForeignKeys and frequently filtered columns
- `pool_pre_ping=True` to handle connection drops
