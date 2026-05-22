---
name: neon-db-setup
description: Set up Neon Serverless PostgreSQL database, configure connection strings, manage database credentials, and integrate with SQLModel ORM. Use when setting up database infrastructure for Phase 2 or configuring database connections.
allowed-tools: Bash, Write, Read, Edit
---

# Neon Serverless PostgreSQL Setup

Quick reference for setting up Neon Serverless PostgreSQL database for the Todo Web Application Phase 2.

## Overview

Neon is a serverless PostgreSQL database that offers:
- Auto-scaling compute
- Branching for development
- Connection pooling
- Free tier for development

## Setup Steps

### 1. Create Neon Account and Project

1. Go to [https://neon.tech](https://neon.tech)
2. Sign up or log in
3. Create a new project:
   - Name: `todo-web-phase2`
   - Region: Choose closest to your deployment (e.g., `us-east-1`)
   - PostgreSQL version: 16+ recommended

### 2. Get Connection String

After creating project, you'll receive connection strings:

```
# Direct connection (for migrations)
postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# Pooled connection (for application - recommended)
postgresql://username:password@ep-xxx-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
```

### 3. Environment Variables

Create `.env` file in backend directory:

```env
# Database Configuration
DATABASE_URL=postgresql://username:password@ep-xxx-pooler.us-east-1.aws.neon.tech/neondb?sslmode=require
DATABASE_URL_DIRECT=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/neondb?sslmode=require

# Use pooled connection for app, direct for migrations
```

Create `.env.example` for version control:

```env
# Database Configuration
DATABASE_URL=postgresql://user:password@host/database?sslmode=require
DATABASE_URL_DIRECT=postgresql://user:password@host/database?sslmode=require
```

### 4. SQLModel Database Configuration

Create `backend/src/database.py`:

```python
import os
from sqlmodel import SQLModel, Session, create_engine
from contextlib import contextmanager

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is not set")

# Create engine with connection pooling settings
engine = create_engine(
    DATABASE_URL,
    echo=False,  # Set to True for SQL debugging
    pool_pre_ping=True,  # Verify connections before use
    pool_size=5,  # Maintain 5 connections in pool
    max_overflow=10,  # Allow up to 10 additional connections
)


def create_db_and_tables():
    """Create all tables defined in SQLModel models."""
    SQLModel.metadata.create_all(engine)


def get_session():
    """Dependency for FastAPI endpoints."""
    with Session(engine) as session:
        yield session


@contextmanager
def get_session_context():
    """Context manager for scripts and migrations."""
    session = Session(engine)
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

### 5. Async Database Configuration (Optional)

For async operations, use `asyncpg`:

```python
import os
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

# Convert postgresql:// to postgresql+asyncpg://
DATABASE_URL = os.getenv("DATABASE_URL", "").replace(
    "postgresql://", "postgresql+asyncpg://"
)

async_engine = create_async_engine(
    DATABASE_URL,
    echo=False,
    pool_pre_ping=True,
    pool_size=5,
    max_overflow=10,
)

async_session_maker = sessionmaker(
    async_engine, class_=AsyncSession, expire_on_commit=False
)


async def get_async_session():
    """Async dependency for FastAPI endpoints."""
    async with async_session_maker() as session:
        yield session


async def create_db_and_tables_async():
    """Create tables asynchronously."""
    async with async_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
```

### 6. Alembic Configuration for Migrations

Initialize Alembic:

```bash
cd backend
alembic init alembic
```

Update `alembic/env.py`:

```python
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import your models
from src.models.task import Task
from src.models.user import User  # if you have user model
from sqlmodel import SQLModel

# Alembic Config object
config = context.config

# Set database URL from environment
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL_DIRECT", ""))

# Interpret the config file for Python logging
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Set target metadata for autogenerate
target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(connection=connection, target_metadata=target_metadata)

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

### 7. Database Schema for Todo App

Create `backend/src/models/task.py`:

```python
from datetime import datetime
from typing import Optional
from sqlmodel import Field, SQLModel


class TaskBase(SQLModel):
    """Base task model with shared fields."""
    title: str = Field(max_length=200, index=True)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    priority: str = Field(default="medium", max_length=20)  # low, medium, high
    due_date: Optional[datetime] = Field(default=None)


class Task(TaskBase, table=True):
    """Task database model."""
    __tablename__ = "tasks"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskCreate(TaskBase):
    """Schema for creating a task."""
    pass


class TaskUpdate(SQLModel):
    """Schema for updating a task (all fields optional)."""
    title: Optional[str] = Field(default=None, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: Optional[bool] = None
    priority: Optional[str] = Field(default=None, max_length=20)
    due_date: Optional[datetime] = None


class TaskResponse(TaskBase):
    """Schema for task API responses."""
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
```

### 8. Migration Commands

```bash
# Create a new migration
alembic revision --autogenerate -m "Create tasks table"

# Apply all pending migrations
alembic upgrade head

# View migration history
alembic history

# Rollback last migration
alembic downgrade -1

# Rollback to specific revision
alembic downgrade <revision_id>

# View current revision
alembic current
```

### 9. Testing Database Connection

Create a test script `backend/scripts/test_db.py`:

```python
#!/usr/bin/env python
"""Test database connection and basic operations."""

import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from dotenv import load_dotenv
load_dotenv()

from sqlmodel import Session, select
from src.database import engine, create_db_and_tables
from src.models.task import Task

def test_connection():
    """Test database connection."""
    try:
        with Session(engine) as session:
            # Simple query to test connection
            result = session.exec(select(1)).first()
            print(f"✅ Database connection successful! Result: {result}")
            return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

def test_crud_operations():
    """Test basic CRUD operations."""
    try:
        # Create tables
        create_db_and_tables()
        print("✅ Tables created successfully")

        with Session(engine) as session:
            # Create a test task
            task = Task(
                title="Test Task",
                description="Testing database operations",
                user_id="test-user-123"
            )
            session.add(task)
            session.commit()
            session.refresh(task)
            print(f"✅ Created task with ID: {task.id}")

            # Read the task
            fetched_task = session.get(Task, task.id)
            print(f"✅ Read task: {fetched_task.title}")

            # Update the task
            fetched_task.completed = True
            session.add(fetched_task)
            session.commit()
            print(f"✅ Updated task completed status: {fetched_task.completed}")

            # Delete the task
            session.delete(fetched_task)
            session.commit()
            print("✅ Deleted test task")

        return True
    except Exception as e:
        print(f"❌ CRUD operations failed: {e}")
        return False

if __name__ == "__main__":
    print("Testing Neon PostgreSQL connection...\n")
    
    if test_connection():
        print("\nTesting CRUD operations...\n")
        test_crud_operations()
```

### 10. Neon Branching for Development

Neon supports database branching - useful for development:

```bash
# Using Neon CLI (install: npm i -g neonctl)
neonctl branches create --name dev-branch

# Get connection string for branch
neonctl connection-string dev-branch

# Delete branch when done
neonctl branches delete dev-branch
```

## Troubleshooting

### Connection Issues

1. **SSL Required**: Neon requires SSL. Ensure `?sslmode=require` in connection string.

2. **Connection Timeout**: Neon has cold start times. First connection may be slow.

3. **IP Restrictions**: Check if your IP is allowed in Neon project settings.

4. **Connection Pooling**: Use pooled connection string for better performance.

### Common Errors

```python
# Error: connection refused
# Solution: Check if DATABASE_URL is correct and Neon project is active

# Error: SSL certificate verify failed
# Solution: Add ?sslmode=require to connection string

# Error: too many connections
# Solution: Use connection pooling, reduce pool_size
```

## Security Best Practices

1. **Never commit credentials**: Use `.env` files, add to `.gitignore`
2. **Use environment variables**: Access via `os.getenv()`
3. **Rotate passwords**: Regularly update database passwords
4. **IP allowlisting**: Restrict database access to known IPs in production
5. **Connection encryption**: Always use SSL (`sslmode=require`)

## Integration with Phase 2

This skill integrates with:
- **Backend API Builder**: For database connection in FastAPI endpoints
- **Better Auth Integration**: For user authentication storage
- **FastAPI Setup**: For initial project configuration

## References

- [Neon Documentation](https://neon.tech/docs)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Phase 2 Database Schema](../../specs/database/schema.md)
