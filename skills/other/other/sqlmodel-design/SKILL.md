---
name: sqlmodel-design
description: |
  This skill designs SQLModel schemas aligned with PostgreSQL and FastAPI. It establishes patterns for defining database models that leverage SQLModel's dual nature as both SQLAlchemy ORM models and Pydantic validation schemas. Use when designing database table schemas, defining model relationships, or creating request/response models for API endpoints.
allowed-tools: Read, Grep, Glob
---

# SQLModel Design

## What This Skill Does

This skill designs SQLModel schemas aligned with PostgreSQL and FastAPI. It establishes patterns for defining database models that leverage SQLModel's dual nature as both SQLAlchemy ORM models and Pydantic validation schemas.

## When to Use

- When designing database table schemas
- When defining model relationships and foreign keys
- When creating request/response models for API endpoints
- When establishing field validation rules
- When planning model inheritance and mixins
- When coordinating between database and API layers

## When NOT to Use

- When the database technology isn't PostgreSQL
- When not using SQLModel (pure SQLAlchemy or other ORM)
- When designing API contracts without database backing
- When working on frontend data models
- When the data model hasn't been specified

## Required Clarifications

Before implementing SQLModel design, clarify:

1. **Entity Relationships**: What are the primary entities and their relationships?
2. **Data Validation**: What are the validation requirements for each field?
3. **Indexing Needs**: What fields require indexes for performance?
4. **API Exposure**: Which fields should be exposed in API responses?
5. **Constraints**: What are the unique and foreign key constraints?

## SQLModel Schema Patterns

### Basic Model Definition
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime
import uuid

class User(SQLModel, table=True):
    """User model with basic fields."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True, sa_column_kwargs={"nullable": False})
    full_name: Optional[str] = Field(default=None, max_length=255)
    is_active: bool = Field(default=True)

    # Timestamps using mixins (see below)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")
```

### Model with Relationships
```python
class Task(SQLModel, table=True):
    """Task model with relationships."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(sa_column_kwargs={"nullable": False})
    description: Optional[str] = Field(default=None)
    status: str = Field(default="pending", sa_column_kwargs={"nullable": False})
    priority: str = Field(default="medium", sa_column_kwargs={"nullable": False})

    # Foreign key relationship
    user_id: uuid.UUID = Field(foreign_key="user.id", sa_column_kwargs={"nullable": False})

    # Relationship back-reference
    user: User = Relationship(back_populates="tasks")

    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

### Pydantic-Only Models for API
```python
from pydantic import BaseModel

# For creating new users (password required)
class UserCreate(BaseModel):
    email: str
    full_name: Optional[str] = None
    password: str

# For updating users (password optional)
class UserUpdate(BaseModel):
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

# For API responses (password never exposed)
class UserResponse(BaseModel):
    id: uuid.UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime
    updated_at: datetime
```

## Field Type Mapping

### PostgreSQL Compatible Types
```python
from sqlmodel import Field
from typing import Optional
from decimal import Decimal
from datetime import datetime
import uuid

class Product(SQLModel, table=True):
    """Product model demonstrating field type mapping."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # String fields
    name: str = Field(sa_column_kwargs={"nullable": False, "max_length": 255})
    description: Optional[str] = Field(default=None)
    sku: str = Field(unique=True, sa_column_kwargs={"nullable": False, "max_length": 100})

    # Numeric fields
    price: Decimal = Field(sa_column_kwargs={"nullable": False, "scale": 2, "precision": 10})
    quantity: int = Field(default=0, sa_column_kwargs={"nullable": False})

    # Boolean fields
    is_available: bool = Field(default=True)

    # DateTime fields
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # JSON fields (PostgreSQL specific)
    metadata: Optional[dict] = Field(default=None, sa_column=sa.Column(JSON))
```

## Relationship Patterns

### One-to-Many Relationship
```python
class Category(SQLModel, table=True):
    """Category model with one-to-many relationship to products."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False, "unique": True})

    # One-to-many relationship
    products: list["Product"] = Relationship(back_populates="category")

class Product(SQLModel, table=True):
    """Product model with foreign key to category."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False})

    # Foreign key
    category_id: uuid.UUID = Field(foreign_key="category.id")

    # Relationship back-reference
    category: Category = Relationship(back_populates="products")
```

### Many-to-Many Relationship
```python
from sqlmodel import create_engine, SQLModel, select
from sqlalchemy import Table, Column, ForeignKey

# Association table for many-to-many relationship
user_project_association = Table(
    "user_project",
    SQLModel.metadata,
    Column("user_id", UUID(as_uuid=True), ForeignKey("user.id")),
    Column("project_id", UUID(as_uuid=True), ForeignKey("project.id"))
)

class Project(SQLModel, table=True):
    """Project model for many-to-many relationship."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    name: str = Field(sa_column_kwargs={"nullable": False})

    # Many-to-many relationship
    users: list["User"] = Relationship(
        back_populates="projects",
        link_model=user_project_association
    )

class User(SQLModel, table=True):
    """User model with many-to-many relationship."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(sa_column_kwargs={"nullable": False})

    # Many-to-many relationship
    projects: list[Project] = Relationship(
        back_populates="users",
        link_model=user_project_association
    )
```

## Validation Patterns

### Field Validation
```python
from pydantic import field_validator, EmailStr
from sqlmodel import Field
from typing import Optional

class User(SQLModel, table=True):
    """User model with field validation."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: EmailStr = Field(sa_column_kwargs={"nullable": False, "unique": True})
    full_name: Optional[str] = Field(default=None, max_length=255)
    age: Optional[int] = Field(default=None, ge=0, le=150)  # Greater than/equal to 0, less than/equal to 150
    phone: Optional[str] = Field(default=None)

    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        if v and len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters')
        return v.title() if v else v

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        if v:
            # Simple phone validation - adjust as needed
            import re
            if not re.match(r'^\+?1?\d{9,15}$', v.replace('-', '').replace(' ', '').replace('(', '').replace(')', '')):
                raise ValueError('Phone number format is invalid')
        return v
```

### Custom Validation Classes
```python
from pydantic import BaseModel, field_validator
from typing import Optional

class PasswordValidationMixin:
    """Mixin class for password validation."""

    @staticmethod
    def validate_password_strength(password: str) -> str:
        """Validate password strength."""
        if len(password) < 8:
            raise ValueError('Password must be at least 8 characters long')

        if not any(c.isupper() for c in password):
            raise ValueError('Password must contain at least one uppercase letter')

        if not any(c.islower() for c in password):
            raise ValueError('Password must contain at least one lowercase letter')

        if not any(c.isdigit() for c in password):
            raise ValueError('Password must contain at least one digit')

        if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
            raise ValueError('Password must contain at least one special character')

        return password

class UserCreate(BaseModel, PasswordValidationMixin):
    """User creation model with password validation."""
    email: str
    full_name: Optional[str] = None
    password: str

    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        return cls.validate_password_strength(v)
```

## Indexing and Performance

### Index Definition Patterns
```python
from sqlmodel import Field
from sqlalchemy import Index

class User(SQLModel, table=True):
    """User model with custom indexes."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)  # Creates both unique constraint and index
    full_name: Optional[str] = Field(default=None, sa_column_kwargs={"index": True})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"index": True})

    # Additional indexes can be defined at class level
    __table_args__ = (
        Index('idx_user_name_email', 'full_name', 'email'),
        Index('idx_user_created_desc', 'created_at', postgresql_ops={'created_at': 'DESC'}),
    )

class Task(SQLModel, table=True):
    """Task model with performance-focused indexes."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(sa_column_kwargs={"index": True})
    status: str = Field(default="pending", sa_column_kwargs={"index": True})
    priority: str = Field(default="medium", sa_column_kwargs={"index": True})
    user_id: uuid.UUID = Field(foreign_key="user.id", sa_column_kwargs={"index": True})
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"index": True})

    # Composite index for common query patterns
    __table_args__ = (
        Index('idx_task_status_priority', 'status', 'priority'),
        Index('idx_task_user_status', 'user_id', 'status'),
    )
```

## Timestamp Management

### Timestamp Mixin Pattern
```python
from sqlmodel import Field
from datetime import datetime

class TimestampMixin:
    """Mixin to add timestamp fields to models."""
    created_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})
    updated_at: datetime = Field(default_factory=datetime.utcnow, sa_column_kwargs={"nullable": False})

class User(TimestampMixin, SQLModel, table=True):
    """User model with timestamp mixin."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, sa_column_kwargs={"nullable": False})

class Task(TimestampMixin, SQLModel, table=True):
    """Task model with timestamp mixin."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(sa_column_kwargs={"nullable": False})
    user_id: uuid.UUID = Field(foreign_key="user.id")
```

### Automatic Timestamp Updates
```python
from sqlalchemy import event
from sqlalchemy.engine import Connection
from sqlalchemy.orm import Mapper
from datetime import datetime

# SQLAlchemy event listener to update timestamps
@event.listens_for(SQLModel, 'before_update', propagate=True)
def update_timestamps(mapper: Mapper, connection: Connection, target: SQLModel):
    """Automatically update updated_at timestamp before any update."""
    if hasattr(target, 'updated_at'):
        target.updated_at = datetime.utcnow()
```

## API Model Variants

### Model Inheritance for Different Purposes
```python
# Base model with all fields
class UserBase(SQLModel):
    """Base user model with common fields."""
    email: str
    full_name: Optional[str] = None
    is_active: bool = True

# Database model with all fields plus primary key
class User(UserBase, table=True):
    """User model for database operations."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)

    # Relationships
    tasks: list["Task"] = Relationship(back_populates="user")

# Create model with required fields for creation
class UserCreate(UserBase):
    """User model for creation with required fields."""
    password: str

# Update model with optional fields for updates
class UserUpdate(BaseModel):
    """User model for updates with optional fields."""
    email: Optional[str] = None
    full_name: Optional[str] = None
    is_active: Optional[bool] = None
    password: Optional[str] = None

# Response model without sensitive fields
class UserResponse(UserBase):
    """User model for API responses."""
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime
```

## Security Considerations

### Field Filtering
```python
from pydantic import BaseModel

class User(SQLModel, table=True):
    """User model with sensitive fields."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(sa_column_kwargs={"nullable": False})
    full_name: Optional[str] = None
    hashed_password: str = Field(sa_column_kwargs={"nullable": False})  # Never expose this
    salt: str = Field(sa_column_kwargs={"nullable": False})  # Never expose this
    is_active: bool = True
    created_at: datetime = Field(default_factory=datetime.utcnow)

class UserResponse(BaseModel):
    """Secure user response model without sensitive fields."""
    id: uuid.UUID
    email: str
    full_name: Optional[str]
    is_active: bool
    created_at: datetime

class UserCreate(BaseModel):
    """User creation model with password instead of hash."""
    email: str
    full_name: Optional[str] = None
    password: str  # Plain text password for input validation
```

## Migration Considerations

### Version-Compatible Models
```python
from sqlmodel import Field
from typing import Optional

class UserV1(SQLModel, table=True):
    """Version 1 of user model."""
    id: int = Field(primary_key=True)
    email: str = Field(sa_column_kwargs={"nullable": False})
    name: str = Field(sa_column_kwargs={"nullable": False})  # Old field name

class UserV2(SQLModel, table=True):
    """Version 2 of user model with improved naming."""
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)  # Changed from int to UUID
    email: str = Field(sa_column_kwargs={"nullable": False})
    full_name: str = Field(sa_column_kwargs={"nullable": False})  # Renamed from 'name'
    is_active: bool = Field(default=True)  # Added new field

    # Migration considerations:
    # - Add new column 'full_name' first
    # - Populate from 'name' column
    # - Drop 'name' column in separate migration
    # - Add new 'is_active' column with default value
```

## Anti-Patterns to Avoid

- **Table Confusion**: Forgetting table=True on database models
- **Validation Skip**: Not leveraging Pydantic validation
- **Type Mismatch**: Using Python types incompatible with PostgreSQL
- **Relationship Ambiguity**: Unclear or missing relationship definitions
- **Field Exposure**: Exposing sensitive fields like password hashes in responses
- **Over-Modeling**: Creating too many model variants for same entity
- **Migration Ignorance**: Designing schemas without considering migrations
- **Timestamp Inconsistency**: Not managing created_at/updated_at properly
- **Index Neglect**: Not considering performance implications of queries

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing structure, patterns, conventions to integrate with |
| **Conversation** | User's specific requirements, constraints, preferences |
| **Skill References** | Domain patterns from `references/` (library docs, best practices, examples) |
| **User Guidelines** | Project-specific conventions, team standards |

## Interaction With Other Skills

- **relational-data-modeling**: Implements relational design in SQLModel
- **python-backend-structure**: Fits within models/ directory
- **fastapi-architecture**: Provides models for dependency injection
- **neon-postgres-integration**: Ensures compatibility with Neon
- **rest-api-design**: Aligns models with API resource structure

## Phase Applicability

Phase II only. Phase I uses in-memory dataclass without database persistence.
