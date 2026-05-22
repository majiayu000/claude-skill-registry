---
name: "SQLModel Database Designer"
description: "Define SQLModel models for User and Task (priority, tags as array, user_id FK) and Neon connection when database schema is required"
version: "1.0.0"
---

# SQLModel Database Designer Skill

## Purpose

Automatically design and implement database schemas using SQLModel with proper relationships, indexes, constraints, and Neon PostgreSQL integration when the user requests database implementation for the Phase II full-stack todo application.

## When This Skill Triggers

Use this skill when the user asks to:
- "Create the database schema"
- "Define SQLModel models for users and todos"
- "Set up the database with Neon"
- "Add database models with relationships"
- "Create migration files"
- Any request to design or implement database schema

## Prerequisites

Before designing database:
1. Read `specs/phase-2/spec.md` for data requirements
2. Read `.specify/memory/constitution.md` for database standards
3. Verify backend project exists in `backend/` directory
4. Ensure SQLModel and Alembic are installed
5. Confirm Neon database credentials available

## Step-by-Step Procedure

### Step 1: Analyze Data Requirements
- Identify entities (User, Todo)
- Determine relationships (User has many Todos)
- List required fields for each entity
- Identify indexes needed for queries
- Plan for user isolation (foreign keys)

### Step 2: Create Database Configuration

```python
# app/config.py
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    """Application settings from environment variables."""
    DATABASE_URL: str
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    DEBUG: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
```

```python
# app/database.py
from sqlmodel import create_engine, Session, SQLModel
from app.config import settings

# Create engine with connection pooling for Neon
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Log SQL in development
    pool_pre_ping=True,   # Verify connections before use
    pool_size=10,         # Connection pool size
    max_overflow=20,      # Max connections beyond pool_size
    pool_recycle=3600,    # Recycle connections after 1 hour
    connect_args={
        "sslmode": "require",  # Required for Neon
        "connect_timeout": 10,
    },
)

def create_db_and_tables():
    """Create all database tables."""
    SQLModel.metadata.create_all(engine)

def get_session():
    """
    Dependency for database session.

    Usage in FastAPI:
        @router.get("/todos")
        async def get_todos(session: Session = Depends(get_session)):
            ...
    """
    with Session(engine) as session:
        try:
            yield session
        finally:
            session.close()
```

### Step 3: Define User Model

```python
# app/models/user.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class User(SQLModel, table=True):
    """
    User model for authentication and todo ownership.

    Relationships:
        - One user has many todos (one-to-many)
    """
    __tablename__ = "users"

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing user ID",
    )

    # Authentication fields
    email: str = Field(
        unique=True,
        index=True,
        max_length=255,
        description="User email address (unique, indexed for login queries)",
    )
    hashed_password: str = Field(
        max_length=255,
        description="Bcrypt hashed password (never store plain text)",
    )

    # Profile fields
    name: str = Field(
        max_length=255,
        description="User's full name",
    )

    # Status flags
    is_active: bool = Field(
        default=True,
        description="Whether user account is active",
    )

    # Timestamps (auto-managed)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Account creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    # Optional: Relationship (for ORM queries, not required)
    # todos: List["Todo"] = Relationship(back_populates="user")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
                "is_active": True,
            }
        }
```

### Step 4: Define Todo Model

```python
# app/models/todo.py
from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime
from typing import Optional, List
from enum import Enum

class Priority(str, Enum):
    """Priority levels for todos."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Todo(SQLModel, table=True):
    """
    Todo item model with user isolation.

    Relationships:
        - Many todos belong to one user (many-to-one via user_id FK)

    Indexes:
        - user_id: For filtering todos by user (critical for performance)
        - completed: For filtering completed/pending todos
        - priority: For filtering by priority level
        - title: For search queries
        - created_at: For sorting by creation date
    """
    __tablename__ = "todos"

    # Primary key
    id: Optional[int] = Field(
        default=None,
        primary_key=True,
        description="Auto-incrementing todo ID",
    )

    # Foreign key (user ownership) - CRITICAL for user isolation
    user_id: int = Field(
        foreign_key="users.id",
        index=True,
        description="Owner of this todo (foreign key to users.id)",
    )

    # Todo content fields
    title: str = Field(
        max_length=500,
        index=True,  # Index for search queries
        description="Todo title (required, max 500 chars)",
    )
    description: Optional[str] = Field(
        default=None,
        max_length=5000,
        description="Optional detailed description (max 5000 chars)",
    )

    # Status and priority fields
    completed: bool = Field(
        default=False,
        index=True,  # Index for filtering completed/pending
        description="Completion status (default: false)",
    )
    priority: Priority = Field(
        default=Priority.MEDIUM,
        index=True,  # Index for filtering by priority
        description="Priority level: low, medium (default), or high",
    )

    # Tags (stored as JSON array in PostgreSQL)
    tags: List[str] = Field(
        default_factory=list,
        sa_column=Column(JSON),
        description="Array of tag strings for categorization",
    )

    # Timestamps (auto-managed)
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        index=True,  # Index for sorting by creation date
        description="Creation timestamp",
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Last update timestamp",
    )

    # Optional: Relationship (for ORM queries)
    # user: User = Relationship(back_populates="todos")

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, vegetables",
                "priority": "high",
                "tags": ["shopping", "urgent"],
                "completed": False,
            }
        }
```

### Step 5: Create Database Indexes

Indexes are defined inline with `index=True`, but for composite indexes, create migration:

```sql
-- Composite indexes for common query patterns
CREATE INDEX idx_todos_user_completed ON todos(user_id, completed);
CREATE INDEX idx_todos_user_priority ON todos(user_id, priority);
CREATE INDEX idx_todos_user_created ON todos(user_id, created_at DESC);
```

### Step 6: Set Up Alembic Migrations

```bash
# Initialize Alembic (one-time setup)
alembic init alembic
```

```python
# alembic/env.py
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.config import settings
from app.models.user import User
from app.models.todo import Todo
from sqlmodel import SQLModel

# This is the Alembic Config object
config = context.config

# Override sqlalchemy.url with our DATABASE_URL
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

# Import all models so Alembic can detect them
target_metadata = SQLModel.metadata

def run_migrations_online():
    """Run migrations in 'online' mode."""
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )

        with context.begin_transaction():
            context.run_migrations()

run_migrations_online()
```

### Step 7: Generate and Apply Migrations

```bash
# Generate migration from models
alembic revision --autogenerate -m "Create users and todos tables"

# Review generated migration in alembic/versions/

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

**Generated Migration Example:**
```python
# alembic/versions/xxx_create_users_and_todos.py
"""Create users and todos tables

Revision ID: 001
Create Date: 2024-01-15
"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '001'
down_revision = None

def upgrade():
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create todos table
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=500), nullable=False),
        sa.Column('description', sa.String(length=5000), nullable=True),
        sa.Column('completed', sa.Boolean(), nullable=False, server_default='false'),
        sa.Column('priority', sa.String(length=10), nullable=False, server_default='medium'),
        sa.Column('tags', postgresql.JSON(), nullable=False, server_default='[]'),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_todos_user_id', 'todos', ['user_id'])
    op.create_index('ix_todos_completed', 'todos', ['completed'])
    op.create_index('ix_todos_priority', 'todos', ['priority'])
    op.create_index('ix_todos_title', 'todos', ['title'])
    op.create_index('ix_todos_created_at', 'todos', ['created_at'])

    # Composite indexes
    op.create_index('ix_todos_user_completed', 'todos', ['user_id', 'completed'])
    op.create_index('ix_todos_user_priority', 'todos', ['user_id', 'priority'])

def downgrade():
    op.drop_table('todos')
    op.drop_table('users')
```

### Step 8: Create Seed Data (Development)

```python
# scripts/seed.py
from app.database import engine, Session
from app.models.user import User
from app.models.todo import Todo, Priority
from app.utils.security import hash_password

def seed_database():
    """Create sample data for development/testing."""
    with Session(engine) as session:
        # Create test users
        user1 = User(
            email="test@example.com",
            name="Test User",
            hashed_password=hash_password("password123"),
        )
        user2 = User(
            email="demo@example.com",
            name="Demo User",
            hashed_password=hash_password("demo123"),
        )
        session.add_all([user1, user2])
        session.commit()
        session.refresh(user1)
        session.refresh(user2)

        # Create sample todos
        todos = [
            Todo(
                title="Buy groceries",
                description="Milk, eggs, bread",
                priority=Priority.HIGH,
                tags=["shopping", "urgent"],
                user_id=user1.id,
            ),
            Todo(
                title="Finish project",
                description="Complete Phase II implementation",
                priority=Priority.MEDIUM,
                tags=["work"],
                completed=True,
                user_id=user1.id,
            ),
            Todo(
                title="Exercise",
                priority=Priority.LOW,
                tags=["health"],
                user_id=user1.id,
            ),
            # Demo user's todos
            Todo(
                title="Demo task 1",
                priority=Priority.MEDIUM,
                user_id=user2.id,
            ),
        ]
        session.add_all(todos)
        session.commit()

        print(f"✅ Created {len([user1, user2])} users")
        print(f"✅ Created {len(todos)} todos")

if __name__ == "__main__":
    seed_database()
```

## Output Format

### Generated Files Structure
```
backend/
├── app/
│   ├── config.py                 # Database config
│   ├── database.py               # Engine and session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py              # User model
│   │   └── todo.py              # Todo model
│   └── dependencies/
│       └── database.py          # get_session dependency
├── alembic/
│   ├── env.py                   # Alembic config
│   └── versions/
│       └── xxx_create_tables.py # Migration
├── scripts/
│   └── seed.py                  # Seed data
└── .env                         # DATABASE_URL
```

### Environment Variables (.env)
```bash
DATABASE_URL=postgresql://user:password@ep-xxx.us-east-2.aws.neon.tech/neondb?sslmode=require
SECRET_KEY=your-secret-key-256-bit
DEBUG=false
```

## Quality Criteria

**Schema Design:**
- ✅ Normalized to 3NF (no redundancy)
- ✅ Foreign keys for relationships
- ✅ Indexes on frequently queried columns
- ✅ Timestamps on all tables
- ✅ Appropriate data types (VARCHAR vs TEXT)
- ✅ NOT NULL constraints where appropriate
- ✅ UNIQUE constraints on emails

**User Isolation:**
- ✅ user_id foreign key on todos table
- ✅ Index on user_id for fast filtering
- ✅ All queries filter by user_id

**Performance:**
- ✅ Connection pooling configured
- ✅ Indexes on filter/sort columns
- ✅ Composite indexes for common queries
- ✅ pool_pre_ping for connection health

**Migrations:**
- ✅ Reversible (upgrade/downgrade)
- ✅ Idempotent (can run multiple times)
- ✅ Version controlled
- ✅ Tested before production

## Examples

### Example 1: Query with User Isolation

```python
from sqlmodel import select, Session

def get_user_todos(user_id: int, session: Session):
    """Get all todos for a specific user."""
    statement = select(Todo).where(Todo.user_id == user_id)
    todos = session.exec(statement).all()
    return todos
```

### Example 2: Complex Query with Joins

```python
from sqlmodel import select, Session
from sqlalchemy.orm import selectinload

def get_todos_with_users(session: Session):
    """Get todos with user information (eager loading)."""
    statement = select(Todo).options(selectinload(Todo.user))
    todos = session.exec(statement).all()
    return todos
```

### Example 3: Filtered Query

```python
def search_todos(user_id: int, search: str, session: Session):
    """Search user's todos by title."""
    statement = (
        select(Todo)
        .where(Todo.user_id == user_id)
        .where(col(Todo.title).contains(search))
        .order_by(Todo.created_at.desc())
    )
    return session.exec(statement).all()
```

## Success Indicators

The skill execution is successful when:
- ✅ Models compile without errors
- ✅ Migrations apply successfully
- ✅ Database tables created in Neon
- ✅ Foreign key constraints enforced
- ✅ Indexes created for performance
- ✅ Connection pooling working
- ✅ User isolation verified in queries
- ✅ Seed data loads successfully
- ✅ Rollback migrations work correctly
