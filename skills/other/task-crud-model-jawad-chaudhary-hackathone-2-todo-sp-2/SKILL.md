---
name: task-crud-model
description: Create SQLModel models for Todo tasks. Use for database schema generation.
---
# TaskCRUDModel Instructions
Input: Fields (title, description, completed, user_id).
Output: Model class.
Steps:
1. Import SQLModel, Field.
2. Define Task class.
Example Code:
from sqlmodel import SQLModel, Field
class Task(SQLModel, table=True):
    id: int = Field(primary_key=True)
    title: str
    description: str | None
    completed: bool = False
    user_id: int = Field(foreign_key="user.id")