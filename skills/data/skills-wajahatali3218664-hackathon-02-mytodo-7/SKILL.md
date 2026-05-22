---
name: sqlmodel-database-skill
description: Define SQLModel models and manage Neon PostgreSQL schema
when-to-use: Adding new database tables or relationships
---
# SQLModel Database Skill

## Instructions

This skill provides guidance for defining SQLModel models and managing Neon PostgreSQL database schema.

### Project Structure
```
backend/
├── database.py              # Database connection and session management
├── models/
│   ├── __init__.py
│   ├── user.py              # User model
│   ├── task.py              # Task model
│   └── base.py              # Base model and utilities
└── migrations/              # Alembic migrations (if needed)
```

### Database Setup

```python
# backend/database.py
from sqlmodel import SQLModel, create_engine, Session, AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession as AsyncSessionType
from sqlalchemy.orm import sessionmaker

# For async Neon PostgreSQL
DATABASE_URL = "postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require"

async_engine = create_async_engine(DATABASE_URL, echo=False, pool_pre_ping=True)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSessionType,
    expire_on_commit=False,
)

# Sync engine for migrations
sync_engine = create_engine(DATABASE_URL.replace("+asyncpg", "+psycopg2"))

async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise

async def init_db():
    """Initialize database tables."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

async def close_db():
    """Close database connections."""
    await async_engine.dispose()
```

### Base Model

```python
# backend/models/base.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Any
from uuid import UUID, uuid4

class TimestampMixin:
    """Mixin for created_at and updated_at timestamps."""
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        sa_column_kwargs={"onupdate": datetime.utcnow}
    )

class UUIDMixin:
    """Mixin for UUID primary key."""
    id: UUID = Field(default_factory=uuid4, primary_key=True)

def create_table_args(base):
    """Create table arguments for all models."""
    return {
        "schema": None,  # Use default schema
    }
```

### User Model

```python
# backend/models/user.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class User(SQLModel, TimestampMixin, table=True):
    """User model for authentication and task ownership."""
    __tablename__ = "users"

    id: int = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    name: str = Field(nullable=False)
    is_active: bool = Field(default=True, nullable=False)

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="owner")

    def verify_password(self, plain_password: str) -> bool:
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(password: str) -> str:
        return pwd_context.hash(password)

    def to_response(self) -> dict:
        """Convert to safe response dict (no password)."""
        return {
            "id": self.id,
            "email": self.email,
            "name": self.name,
            "is_active": self.is_active,
            "created_at": self.created_at.isoformat(),
        }
```

### Task Model

```python
# backend/models/task.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from models.user import User

class Task(SQLModel, TimestampMixin, table=True):
    """Task model for todo items."""
    __tablename__ = "tasks"

    id: int = Field(default=None, primary_key=True)
    title: str = Field(min_length=1, max_length=255, nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)
    completed: bool = Field(default=False, nullable=False)
    due_date: Optional[datetime] = Field(default=None, nullable=True)
    priority: str = Field(default="medium", nullable=False)

    # Foreign key to User
    owner_id: int = Field(foreign_key="users.id", nullable=False)

    # Relationship
    owner: "User" = Relationship(back_populates="tasks")

    def to_response(self) -> dict:
        """Convert to response dict."""
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "completed": self.completed,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "priority": self.priority,
            "owner_id": self.owner_id,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat(),
        }
```

### Creating New Models

```python
# backend/models/category.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import List, Optional

class Category(SQLModel, TimestampMixin, table=True):
    """Category for organizing tasks."""
    __tablename__ = "categories"

    id: int = Field(default=None, primary_key=True)
    name: str = Field(unique=True, nullable=False)
    color: str = Field(default="#3B82F6", nullable=False)
    description: Optional[str] = Field(default=None, nullable=True)

    # Self-referential many-to-many for subcategories
    parent_id: Optional[int] = Field(default=None, foreign_key="categories.id", nullable=True)

    # Relationships
    tasks: List["TaskCategory"] = Relationship(back_populates="category")

class TaskCategory(SQLModel, table=True):
    """Association table for tasks and categories (many-to-many)."""
    __tablename__ = "task_categories"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    category_id: int = Field(foreign_key="categories.id", primary_key=True)

    category: "Category" = Relationship(back_populates="tasks")
```

### Model Relationships

```python
# Understanding relationships

# One-to-Many (User -> Tasks)
class User(SQLModel, table=True):
    id: int
    tasks: List["Task"] = Relationship(back_populates="owner")

class Task(SQLModel, table=True):
    id: int
    owner_id: int = Field(foreign_key="users.id")
    owner: "User" = Relationship(back_populates="tasks")

# Many-to-Many (Tasks <-> Categories)
class TaskCategory(SQLModel, table=True):
    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    category_id: int = Field(foreign_key="categories.id", primary_key=True)

class Task(SQLModel, table=True):
    categories: List["Category"] = Relationship(
        link_model=TaskCategory,
        back_populates="tasks"
    )

class Category(SQLModel, table=True):
    tasks: List["Task"] = Relationship(
        link_model=TaskCategory,
        back_populates="categories"
    )
```

## Examples

### Using SQLModel with FastAPI

```python
# tasks/service.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from models.task import Task
from models.user import User
from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: str = "medium"

class TaskService:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create_task(self, task_data: TaskCreate, owner_id: int) -> Task:
        task = Task(
            **task_data.model_dump(),
            owner_id=owner_id
        )
        self.db.add(task)
        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def get_tasks(
        self,
        owner_id: int,
        completed: Optional[bool] = None,
        limit: int = 100,
        offset: int = 0
    ) -> List[Task]:
        query = select(Task).where(Task.owner_id == owner_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        query = query.offset(offset).limit(limit).order_by(Task.created_at.desc())

        result = await self.db.execute(query)
        return result.scalars().all()

    async def get_task(self, task_id: int, owner_id: int) -> Optional[Task]:
        query = select(Task).where(
            Task.id == task_id,
            Task.owner_id == owner_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_task(
        self,
        task_id: int,
        owner_id: int,
        **updates
    ) -> Optional[Task]:
        task = await self.get_task(task_id, owner_id)
        if not task:
            return None

        for key, value in updates.items():
            setattr(task, key, value)

        await self.db.commit()
        await self.db.refresh(task)
        return task

    async def delete_task(self, task_id: int, owner_id: int) -> bool:
        task = await self.get_task(task_id, owner_id)
        if not task:
            return False

        await self.db.delete(task)
        await self.db.commit()
        return True
```

### Neon PostgreSQL Connection

```python
# backend/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    DB_POOL_SIZE: int = 5
    DB_MAX_OVERFLOW: int = 10
    DB_POOL_TIMEOUT: int = 30

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()

# Connection string format for Neon:
# postgresql+asyncpg://user:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### Database Migrations with Alembic

```python
# alembic/env.py
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

from sqlmodel import SQLModel
from models.user import User
from models.task import Task

config = context.config
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = SQLModel.metadata

def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

async def run_async_migrations() -> None:
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()

def do_run_migrations(connection: Connection) -> None:
    context.configure(
        connection=connection,
        target_metadata=target_metadata,
    )
    with context.begin_transaction():
        context.run_migrations()
```

### Running Migrations

```bash
# Initialize Alembic (one-time)
alembic init migrations

# Generate migration
alembic revision --autogenerate -m "add categories table"

# Apply migration
alembic upgrade head

# Check current revision
alembic current

# Rollback
alembic downgrade -1
```

### Testing Models

```python
# tests/test_models.py
import pytest
from datetime import datetime
from models.task import Task
from models.user import User

def test_user_password_hashing():
    password = "secure_password"
    hashed = User.hash_password(password)

    user = User(
        email="test@example.com",
        hashed_password=hashed,
        name="Test User"
    )

    assert user.verify_password(password)
    assert not user.verify_password("wrong_password")

def test_task_creation():
    task = Task(
        title="Test Task",
        description="Test Description",
        priority="high",
        owner_id=1
    )

    assert task.title == "Test Task"
    assert task.completed is False
    assert task.priority == "high"
    assert isinstance(task.created_at, datetime)

def test_task_to_response():
    task = Task(
        id=1,
        title="Test Task",
        description="Test Description",
        completed=False,
        priority="medium",
        owner_id=1
    )

    response = task.to_response()
    assert response["id"] == 1
    assert response["title"] == "Test Task"
    assert "hashed_password" not in response
```
