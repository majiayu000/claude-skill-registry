---
name: sqlmodel-task-models
description: This skill should be used when defining a robust, type-safe, and async-compatible database schema for the Todo application using SQLModel, ensuring compatibility with Better Auth and optimized for PostgreSQL.
---

# SQLModel Task Models

This skill providing guidance on defining a robust database schema using SQLModel for the Todo application.

## Purpose
Defining a robust, type-safe, and async-compatible database schema for the Todo application using SQLModel, ensuring compatibility with Better Auth and optimized for PostgreSQL.

## Capabilities
- **User Model**: Schema aligned with Better Auth requirements.
- **Task Model**: Full CRUD capability with relational mapping to Users.
- **Relational Integrity**: Proper foreign key constraints and back-references.
- **Performance**: Strategic indexing on `user_id` and `completed` fields.
- **Safety**: Automated timestamp management (`created_at`, `updated_at`).

## Implementation Details

### Models Definition
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    tasks: List["Task"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str
    description: Optional[str] = None
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    user: Optional[User] = Relationship(back_populates="tasks")
```

## Best Practices
- Using `table=True` for models that map to database tables.
- Explicitly defining indexes for fields used in `WHERE` clauses (e.g., `user_id`, `completed`).
- Using `datetime.utcnow` for consistent cross-region timestamping.
- Keeping `user_id` as a string to match Better Auth's UUID/ID format.
