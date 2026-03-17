---
name: database
description: Universal database operations skill for modern applications. Expert in SQLModel/SQLAlchemy patterns, async database operations, connection pooling, migrations, performance optimization, and multi-database support (PostgreSQL, MySQL, SQLite). Provides production-ready patterns for any database-driven application.
license: MIT
---

# Database Operations & Management

This skill provides comprehensive database patterns and best practices for 2025, focusing on async operations, performance optimization, and production-ready configurations that work across different database systems.

## When to Use This Skill

Use this skill when you need to:
- Design database schemas with SQLModel/SQLAlchemy
- Implement async database operations
- Optimize database performance
- Set up connection pooling
- Create and manage database migrations
- Handle complex relationships and queries
- Set up production database configurations
- Monitor and troubleshoot database issues

## Core Database Patterns

### 1. Async Connection Management

```python
# Database connection setup with connection pooling
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.pool import NullPool
from contextlib import asynccontextmanager
import os

# Environment-based configuration
DATABASE_CONFIG = {
    "development": {
        "url": "sqlite+aiosqlite:///./app.db",
        "poolclass": NullPool,
        "echo": True
    },
    "production": {
        "url": os.getenv("DATABASE_URL", "postgresql+asyncpg://user:pass@localhost/db"),
        "pool_size": 30,
        "max_overflow": 40,
        "pool_pre_ping": True,
        "pool_recycle": 3600,
        "echo": False
    }
}

class DatabaseManager:
    """Universal database manager for async operations"""

    def __init__(self, env: str = "development"):
        config = DATABASE_CONFIG[env]
        self.engine = create_async_engine(**config)
        self.async_session = async_sessionmaker(
            self.engine,
            class_=AsyncSession,
            expire_on_commit=False
        )

    @asynccontextmanager
    async def get_session(self):
        """Get async database session with proper cleanup"""
        async with self.async_session() as session:
            try:
                yield session
                await session.commit()
            except Exception:
                await session.rollback()
                raise
            finally:
                await session.close()

    async def create_tables(self, metadata):
        """Create all tables from metadata"""
        async with self.engine.begin() as conn:
            await conn.run_sync(metadata.create_all)

    async def close(self):
        """Close database connections"""
        await self.engine.dispose()

# Singleton instance
db_manager = DatabaseManager(os.getenv("ENV", "development"))
```

### 2. Base Model with Best Practices

```python
# models/base.py
from sqlmodel import SQLModel, Field, DateTime, func
from typing import Optional
from datetime import datetime
from sqlalchemy import Column, DateTime as SQLDateTime, Index

class TimestampMixin(SQLModel):
    """Mixin for timestamp fields"""

    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        sa_column=Column(
            SQLDateTime(timezone=True),
            server_default=func.now(),
            nullable=False
        )
    )

    updated_at: Optional[datetime] = Field(
        default=None,
        sa_column=Column(
            SQLDateTime(timezone=True),
            onupdate=func.now(),
            nullable=True
        )
    )

class SoftDeleteMixin(SQLModel):
    """Mixin for soft delete functionality"""

    deleted_at: Optional[datetime] = None
    is_deleted: bool = Field(default=False)

class BaseModel(SQLModel, TimestampMixin):
    """Base model with common fields and patterns"""

    id: Optional[int] = Field(default=None, primary_key=True)

    class Config:
        # Enable Pydantic's strict mode
        strict = True
        # Validate defaults
        validate_assignment = True
        # Use enum values
        use_enum_values = True

# Indexes for common queries
Index("idx_base_created_at", BaseModel.created_at)
```

### 3. Advanced Model Patterns

```python
# models/examples.py
from enum import Enum
from typing import Optional, List
from sqlalchemy import Column, String, Text, Boolean, Integer, Index, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from sqlmodel import SQLModel, Field, Session, select, update, delete

# Enums for type safety
class Status(str, Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    PENDING = "pending"

class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class User(BaseModel, table=True):
    """User model with optimized fields and indexes"""

    __tablename__ = "users"

    email: str = Field(
        sa_column=Column(String(255), unique=True, nullable=False, index=True)
    )
    username: str = Field(
        sa_column=Column(String(100), unique=True, nullable=False, index=True)
    )
    full_name: Optional[str] = Field(default=None, max_length=200)
    is_active: bool = Field(default=True, sa_column=Column(Boolean, default=True))

    # Optimized text fields
    bio: Optional[str] = Field(
        default=None,
        sa_column=Column(Text)  # Use Text for longer content
    )

    # Relationships
    tasks: List["Task"] = Relationship(back_populates="owner")

    # Optimized queries
    __table_args__ = (
        Index("idx_user_active_email", "is_active", "email"),
        Index("idx_user_created_at", "created_at"),
    )

class Task(BaseModel, SoftDeleteMixin, table=True):
    """Task model with advanced patterns"""

    __tablename__ = "tasks"

    # Foreign key with index
    owner_id: int = Field(
        foreign_key="users.id",
        sa_column=Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    )

    # Optimized fields
    title: str = Field(
        sa_column=Column(String(200), nullable=False)
    )
    description: Optional[str] = Field(
        default=None,
        sa_column=Column(Text)
    )

    # Enum fields
    status: Status = Field(default=Status.PENDING)
    priority: Priority = Field(default=Priority.MEDIUM)

    # JSON field for flexible metadata
    metadata: dict = Field(
        default_factory=dict,
        sa_column=Column("metadata", JSON)
    )

    # Relationships
    owner: User = Relationship(back_populates="tasks")
    tags: List["TaskTag"] = Relationship(back_populates="task")

    # Optimized queries
    __table_args__ = (
        Index("idx_task_owner_status", "owner_id", "status"),
        Index("idx_task_priority_created", "priority", "created_at"),
        Index("idx_task_deleted", "is_deleted"),
    )

class Tag(BaseModel, table=True):
    """Tag model for many-to-many relationships"""

    __tablename__ = "tags"

    name: str = Field(
        sa_column=Column(String(50), unique=True, nullable=False, index=True)
    )
    color: Optional[str] = Field(default=None, max_length=7)  # Hex color code

class TaskTag(BaseModel, table=True):
    """Many-to-many relationship table"""

    __tablename__ = "task_tags"

    task_id: int = Field(foreign_key="tasks.id", primary_key=True)
    tag_id: int = Field(foreign_key="tags.id", primary_key=True)

    task: Task = Relationship()
    tag: Tag = Relationship()
```

### 4. Repository Pattern for Clean Code

```python
# repositories/base.py
from abc import ABC, abstractmethod
from typing import TypeVar, Generic, List, Optional, Dict, Any
from sqlmodel import SQLModel, Session, select, update, delete, func

ModelType = TypeVar("ModelType", bound=SQLModel)

class BaseRepository(Generic[ModelType], ABC):
    """Base repository with common CRUD operations"""

    def __init__(self, model: type[ModelType]):
        self.model = model

    async def create(self, db: Session, *, obj_in: Dict[str, Any]) -> ModelType:
        """Create a new record"""
        db_obj = self.model(**obj_in)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """Get a record by ID"""
        statement = select(self.model).where(self.model.id == id)
        return db.exec(statement).first()

    async def get_multi(
        self,
        db: Session,
        *,
        skip: int = 0,
        limit: int = 100,
        filters: Optional[Dict[str, Any]] = None
    ) -> List[ModelType]:
        """Get multiple records with pagination"""
        statement = select(self.model)

        # Apply filters
        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    statement = statement.where(getattr(self.model, key) == value)

        statement = statement.offset(skip).limit(limit)
        return db.exec(statement).all()

    async def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Dict[str, Any]
    ) -> ModelType:
        """Update a record"""
        for field, value in obj_in.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def remove(self, db: Session, *, id: int) -> ModelType:
        """Remove a record"""
        obj = await self.get(db, id=id)
        if obj:
            db.delete(obj)
            db.commit()
        return obj

    async def count(self, db: Session, filters: Optional[Dict[str, Any]] = None) -> int:
        """Count records with optional filters"""
        statement = select(func.count(self.model.id))

        if filters:
            for key, value in filters.items():
                if hasattr(self.model, key):
                    statement = statement.where(getattr(self.model, key) == value)

        return db.exec(statement).scalar()

# repositories/user.py
class UserRepository(BaseRepository[User]):
    """User repository with specific queries"""

    async def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """Get user by email"""
        statement = select(User).where(User.email == email)
        return db.exec(statement).first()

    async def get_active_users(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[User]:
        """Get active users"""
        statement = select(User).where(User.is_active == True)
        statement = statement.offset(skip).limit(limit)
        return db.exec(statement).all()
```

### 5. Advanced Query Patterns

```python
# services/query_builder.py
from sqlalchemy import and_, or_, func, asc, desc, extract
from typing import List, Optional, Dict, Any, Union
from datetime import datetime, date
from models.base import db_manager

class QueryBuilder:
    """Advanced query builder for complex database operations"""

    def __init__(self, model):
        self.model = model
        self._filters = []
        self._order_by = []
        self._joins = []
        self._group_by = []

    def filter(self, *conditions) -> "QueryBuilder":
        """Add filter conditions"""
        self._filters.extend(conditions)
        return self

    def where(self, condition) -> "QueryBuilder":
        """Add where condition"""
        self._filters.append(condition)
        return self

    def order_by(self, *columns) -> "QueryBuilder":
        """Add order by clauses"""
        self._order_by.extend(columns)
        return self

    def join(self, model, condition=None) -> "QueryBuilder":
        """Add join"""
        self._joins.append((model, condition))
        return self

    def group_by(self, *columns) -> "QueryBuilder":
        """Add group by clauses"""
        self._group_by.extend(columns)
        return self

    async def execute(self, db: Session):
        """Execute the built query"""
        statement = select(self.model)

        # Apply filters
        if self._filters:
            statement = statement.where(and_(*self._filters))

        # Apply joins
        for model, condition in self._joins:
            if condition:
                statement = statement.join(model, condition)
            else:
                statement = statement.join(model)

        # Apply group by
        if self._group_by:
            statement = statement.group_by(*self._group_by)

        # Apply order by
        if self._order_by:
            statement = statement.order_by(*self._order_by)

        return db.exec(statement).all()

# Usage examples
async def search_tasks_advanced(
    owner_id: int,
    keywords: Optional[str] = None,
    status: Optional[Status] = None,
    priority: Optional[Priority] = None,
    date_range: Optional[tuple] = None
) -> List[Task]:
    """Advanced task search with multiple filters"""

    async with db_manager.get_session() as db:
        query = QueryBuilder(Task)

        # Base filters
        query = query.filter(Task.owner_id == owner_id, Task.is_deleted == False)

        # Text search
        if keywords:
            search_pattern = f"%{keywords}%"
            query = query.where(
                or_(
                    Task.title.ilike(search_pattern),
                    Task.description.ilike(search_pattern)
                )
            )

        # Status filter
        if status:
            query = query.filter(Task.status == status)

        # Priority filter
        if priority:
            query = query.filter(Task.priority == priority)

        # Date range filter
        if date_range:
            start_date, end_date = date_range
            query = query.filter(
                and_(
                    Task.created_at >= start_date,
                    Task.created_at <= end_date
                )
            )

        # Order by priority and creation date
        query = query.order_by(
            desc(Task.priority),
            desc(Task.created_at)
        )

        return await query.execute(db)
```

### 6. Database Migrations Best Practices

```python
# migrations/versions/001_initial_tables.py
"""Initial tables migration

Revision ID: 001_initial
Revises:
Create Date: 2025-01-01 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers
revision = '001_initial'
down_revision = None
branch_labels = None
depends_on = None

def upgrade():
    """Create initial tables with optimized schema"""

    # Users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('username', sa.String(length=100), nullable=False),
        sa.Column('full_name', sa.String(length=200), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=True, default=True),
        sa.Column('bio', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('email'),
        sa.UniqueConstraint('username')
    )

    # Create indexes
    op.create_index('idx_user_email', 'users', ['email'])
    op.create_index('idx_user_username', 'users', ['username'])
    op.create_index('idx_user_active_email', 'users', ['is_active', 'email'])

    # Tasks table
    op.create_table(
        'tasks',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('owner_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=200), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('status', sa.Enum('ACTIVE', 'INACTIVE', 'PENDING', name='status'), nullable=True),
        sa.Column('priority', sa.Enum('LOW', 'MEDIUM', 'HIGH', 'CRITICAL', name='priority'), nullable=True),
        sa.Column('metadata', sa.JSON(), nullable=True),
        sa.Column('is_deleted', sa.Boolean(), nullable=True, default=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['owner_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    # Create indexes
    op.create_index('idx_task_owner', 'tasks', ['owner_id'])
    op.create_index('idx_task_owner_status', 'tasks', ['owner_id', 'status'])
    op.create_index('idx_task_priority_created', 'tasks', ['priority', 'created_at'])
    op.create_index('idx_task_deleted', 'tasks', ['is_deleted'])

    # Tags table
    op.create_table(
        'tags',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('color', sa.String(length=7), nullable=True),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('name')
    )

    op.create_index('idx_tag_name', 'tags', ['name'])

    # Task-Tag relationship table
    op.create_table(
        'task_tags',
        sa.Column('task_id', sa.Integer(), nullable=False),
        sa.Column('tag_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ),
        sa.ForeignKeyConstraint(['tag_id'], ['tags.id'], ),
        sa.PrimaryKeyConstraint('task_id', 'tag_id')
    )

def downgrade():
    """Drop all tables"""
    op.drop_table('task_tags')
    op.drop_table('tags')
    op.drop_table('tasks')
    op.drop_table('users')
```

### 7. Performance Optimization

```python
# utils/performance.py
import time
from functools import wraps
from typing import Callable, Any
from sqlmodel import Session

def measure_query_time(func: Callable) -> Callable:
    """Decorator to measure query execution time"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start_time = time.time()
        result = await func(*args, **kwargs)
        execution_time = time.time() - start_time

        # Log slow queries
        if execution_time > 1.0:  # 1 second threshold
            print(f"Slow query detected: {func.__name__} took {execution_time:.2f}s")

        return result
    return wrapper

class DatabaseOptimizer:
    """Database performance optimization utilities"""

    @staticmethod
    async def analyze_slow_queries(db: Session, threshold: float = 1.0) -> List[Dict]:
        """Analyze slow queries (PostgreSQL specific)"""
        if db.bind.dialect.name != 'postgresql':
            return []

        query = """
        SELECT query, calls, total_time, mean_time, rows
        FROM pg_stat_statements
        WHERE mean_time > %s
        ORDER BY total_time DESC
        LIMIT 10
        """

        result = db.execute(query, threshold)
        return [dict(row) for row in result]

    @staticmethod
    async def get_table_statistics(db: Session) -> Dict[str, Any]:
        """Get table statistics"""
        stats = {}

        if db.bind.dialect.name == 'postgresql':
            # PostgreSQL statistics
            tables_query = """
            SELECT schemaname, tablename, n_tup_ins, n_tup_upd, n_tup_del, n_live_tup, n_dead_tup
            FROM pg_stat_user_tables
            """

            for row in db.execute(tables_query):
                table_name = row.tablename
                stats[table_name] = {
                    'inserts': row.n_tup_ins,
                    'updates': row.n_tup_upd,
                    'deletes': row.n_tup_del,
                    'live_rows': row.n_live_tup,
                    'dead_rows': row.n_dead_tup
                }

        return stats
```

### 8. Testing Database Operations

```python
# tests/conftest.py
import pytest
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from httpx import AsyncClient
from sqlmodel import SQLModel
from models.base import BaseModel
from repositories.base import BaseRepository

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop"""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
async def test_db_session():
    """Create test database session"""
    # In-memory SQLite for testing
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        echo=False
    )

    # Create tables
    async with engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.create_all)

    # Create session
    async_session = async_sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        yield session

@pytest.fixture
def user_repository():
    """Create user repository instance"""
    return UserRepository(User)

# tests/test_repositories.py
@pytest.mark.asyncio
async def test_create_user(test_db_session: AsyncSession, user_repository):
    """Test user creation"""
    user_data = {
        "email": "test@example.com",
        "username": "testuser",
        "full_name": "Test User"
    }

    user = await user_repository.create(test_db_session, obj_in=user_data)

    assert user.email == user_data["email"]
    assert user.username == user_data["username"]
    assert user.is_active == True
```

### 9. Production Configuration Checklist

```yaml
# config/production_checklist.yaml
database:
  production_ready:
    connection_pooling: true
    ssl_enabled: true
    max_connections: 100
    min_connections: 10
    connection_timeout: 30
    idle_timeout: 300

  monitoring:
    slow_query_log: true
    query_threshold: 1.0
    connection_pool_metrics: true

  backup:
    automated_backups: true
    backup_retention: 30_days
    point_in_time_recovery: true

  security:
    encryption_at_rest: true
    encryption_in_transit: true
    least_privilege_access: true
    regular_rotation: true
```

This comprehensive database skill provides production-ready patterns optimized for 2025, including async operations, performance optimization, proper indexing, and comprehensive testing strategies that work across different database systems.