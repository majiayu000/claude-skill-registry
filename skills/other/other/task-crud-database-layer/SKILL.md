---
name: task-crud-database-layer
description: |
  This skill implements task persistence with user scoping, supporting add, list, update, complete, and delete operations. It enforces business logic correctness and handles missing tasks safely. Use when implementing task management systems with proper user isolation and data integrity.
allowed-tools: Read, Grep, Glob, Bash
---

# Task CRUD Database Layer Skill

This skill implements the core database layer for task management with user scoping, providing persistent storage and retrieval of tasks with proper access controls and business logic enforcement.

## Core Capabilities

### 1. Task Persistence Operations
- **Add**: Create new tasks with user association and validation
- **List**: Retrieve tasks with user scoping and filtering options
- **Update**: Modify existing tasks with permission checks
- **Complete**: Mark tasks as completed with status tracking
- **Delete**: Remove tasks with cascade effects and validation

### 2. User Scoping Enforcement
- Ensures users can only access their own tasks
- Implements row-level security at the database level
- Validates user permissions before operations
- Prevents cross-user data access

### 3. Safe Error Handling
- Gracefully handles missing tasks
- Provides meaningful error messages
- Implements transaction safety
- Maintains data integrity

## Implementation Patterns

### Task Model Structure
```python
from datetime import datetime
from typing import Optional, List
from enum import Enum

class TaskStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    ARCHIVED = "archived"

class Task:
    def __init__(
        self,
        id: Optional[str] = None,
        user_id: str,
        title: str,
        description: Optional[str] = None,
        status: TaskStatus = TaskStatus.PENDING,
        priority: str = "medium",
        due_date: Optional[datetime] = None,
        created_at: Optional[datetime] = None,
        updated_at: Optional[datetime] = None
    ):
        self.id = id
        self.user_id = user_id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.due_date = due_date
        self.created_at = created_at or datetime.now()
        self.updated_at = updated_at or datetime.now()

    def to_dict(self) -> dict:
        """Convert task to dictionary representation"""
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "status": self.status.value,
            "priority": self.priority,
            "due_date": self.due_date.isoformat() if self.due_date else None,
            "created_at": self.created_at.isoformat(),
            "updated_at": self.updated_at.isoformat()
        }
```

### Database Operations Class
```python
import sqlite3
from typing import List, Optional
from contextlib import contextmanager

class TaskDatabase:
    def __init__(self, db_path: str):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize database with tasks table"""
        with self.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    user_id TEXT NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT,
                    status TEXT DEFAULT 'pending',
                    priority TEXT DEFAULT 'medium',
                    due_date TIMESTAMP,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_tasks_user_id ON tasks(user_id)')
            conn.execute('CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)')

    @contextmanager
    def get_connection(self):
        """Context manager for database connections"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def add_task(self, task: Task) -> Optional[Task]:
        """Add a new task to the database"""
        try:
            with self.get_connection() as conn:
                cursor = conn.cursor()

                # Generate ID if not provided
                if not task.id:
                    import uuid
                    task.id = str(uuid.uuid4())

                cursor.execute('''
                    INSERT INTO tasks (id, user_id, title, description, status, priority, due_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                ''', (
                    task.id, task.user_id, task.title, task.description,
                    task.status.value, task.priority, task.due_date
                ))

                # Retrieve the created task
                cursor.execute('SELECT * FROM tasks WHERE id = ?', (task.id,))
                row = cursor.fetchone()

                if row:
                    return self._row_to_task(row)

        except sqlite3.IntegrityError as e:
            raise ValueError(f"Failed to add task: {str(e)}")

        return None

    def list_tasks(self, user_id: str, status_filter: Optional[str] = None, limit: int = 100) -> List[Task]:
        """List tasks for a specific user with optional filters"""
        with self.get_connection() as conn:
            query = "SELECT * FROM tasks WHERE user_id = ?"
            params = [user_id]

            if status_filter:
                query += " AND status = ?"
                params.append(status_filter)

            query += " ORDER BY created_at DESC LIMIT ?"
            params.append(limit)

            cursor = conn.cursor()
            cursor.execute(query, params)
            rows = cursor.fetchall()

            return [self._row_to_task(row) for row in rows]

    def get_task(self, task_id: str, user_id: str) -> Optional[Task]:
        """Get a specific task for a user"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )
            row = cursor.fetchone()

            if row:
                return self._row_to_task(row)

            return None

    def update_task(self, task_id: str, user_id: str, **updates) -> Optional[Task]:
        """Update a task with user validation"""
        # Validate task exists and belongs to user
        existing_task = self.get_task(task_id, user_id)
        if not existing_task:
            raise ValueError("Task not found or access denied")

        # Prepare update query
        valid_fields = {'title', 'description', 'status', 'priority', 'due_date'}
        filtered_updates = {k: v for k, v in updates.items() if k in valid_fields}

        if not filtered_updates:
            return existing_task

        # Add updated_at timestamp
        filtered_updates['updated_at'] = datetime.now()

        with self.get_connection() as conn:
            set_clause = ", ".join([f"{k} = ?" for k in filtered_updates.keys()])
            params = list(filtered_updates.values()) + [task_id, user_id]

            cursor = conn.cursor()
            cursor.execute(
                f"UPDATE tasks SET {set_clause}, updated_at = CURRENT_TIMESTAMP WHERE id = ? AND user_id = ?",
                params
            )

            if cursor.rowcount == 0:
                raise ValueError("Task not found or access denied")

            # Return updated task
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if row:
                return self._row_to_task(row)

        return None

    def complete_task(self, task_id: str, user_id: str) -> bool:
        """Mark a task as completed"""
        try:
            updated_task = self.update_task(
                task_id, user_id,
                status=TaskStatus.COMPLETED.value,
                updated_at=datetime.now()
            )
            return updated_task is not None
        except ValueError:
            return False

    def delete_task(self, task_id: str, user_id: str) -> bool:
        """Delete a task with user validation"""
        with self.get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM tasks WHERE id = ? AND user_id = ?",
                (task_id, user_id)
            )

            return cursor.rowcount > 0

    def _row_to_task(self, row) -> Task:
        """Convert database row to Task object"""
        return Task(
            id=row['id'],
            user_id=row['user_id'],
            title=row['title'],
            description=row['description'],
            status=TaskStatus(row['status']),
            priority=row['priority'],
            due_date=row['due_date'],
            created_at=row['created_at'],
            updated_at=row['updated_at']
        )
```

### MCP Tool Internals
```python
import json
from typing import Dict, Any, List
from mcp.server.fastmcp import FastMCP

class TaskService:
    def __init__(self, db: TaskDatabase):
        self.db = db

    def create_task(self, user_id: str, title: str, description: str = None,
                   priority: str = "medium", due_date: str = None) -> Dict[str, Any]:
        """Create a new task"""
        if not title or not title.strip():
            raise ValueError("Title is required")

        from datetime import datetime
        parsed_due_date = datetime.fromisoformat(due_date) if due_date else None

        task = Task(
            user_id=user_id,
            title=title.strip(),
            description=description,
            priority=priority,
            due_date=parsed_due_date
        )

        created_task = self.db.add_task(task)
        if not created_task:
            raise ValueError("Failed to create task")

        return created_task.to_dict()

    def get_tasks(self, user_id: str, status: str = None) -> List[Dict[str, Any]]:
        """Get tasks for a user"""
        return [task.to_dict() for task in self.db.list_tasks(user_id, status)]

    def update_task(self, task_id: str, user_id: str, **updates) -> Dict[str, Any]:
        """Update an existing task"""
        updated_task = self.db.update_task(task_id, user_id, **updates)
        if not updated_task:
            raise ValueError("Task not found or could not be updated")

        return updated_task.to_dict()

    def complete_task(self, task_id: str, user_id: str) -> Dict[str, Any]:
        """Complete a task"""
        success = self.db.complete_task(task_id, user_id)
        if not success:
            raise ValueError("Task not found or could not be completed")

        task = self.db.get_task(task_id, user_id)
        return task.to_dict() if task else {"id": task_id, "completed": True}

    def delete_task(self, task_id: str, user_id: str) -> Dict[str, Any]:
        """Delete a task"""
        success = self.db.delete_task(task_id, user_id)
        if not success:
            raise ValueError("Task not found or could not be deleted")

        return {"id": task_id, "deleted": True}
```

### MCP Server Integration
```python
def create_task_mcp_server(db_path: str = "tasks.db"):
    """Create MCP server for task operations"""
    from mcp.server.fastmcp import FastMCP

    mcp_app = FastMCP(
        name="task-crud-server",
        description="MCP server for task CRUD operations with user scoping",
        stateless_http=True,
        json_response=True
    )

    # Initialize database
    db = TaskDatabase(db_path)
    task_service = TaskService(db)

    @mcp_app.tool(
        name="create_task",
        description="Create a new task for the current user"
    )
    def create_task_tool(user_id: str, title: str, description: str = "",
                        priority: str = "medium", due_date: str = "") -> dict:
        return task_service.create_task(user_id, title, description, priority, due_date)

    @mcp_app.tool(
        name="get_tasks",
        description="Get all tasks for the current user, optionally filtered by status"
    )
    def get_tasks_tool(user_id: str, status: str = "") -> list:
        return task_service.get_tasks(user_id, status if status else None)

    @mcp_app.tool(
        name="update_task",
        description="Update an existing task for the current user"
    )
    def update_task_tool(task_id: str, user_id: str, title: str = "",
                        description: str = "", status: str = "",
                        priority: str = "", due_date: str = "") -> dict:
        updates = {}
        if title:
            updates['title'] = title
        if description:
            updates['description'] = description
        if status:
            updates['status'] = status
        if priority:
            updates['priority'] = priority
        if due_date:
            updates['due_date'] = due_date

        return task_service.update_task(task_id, user_id, **updates)

    @mcp_app.tool(
        name="complete_task",
        description="Mark a task as completed for the current user"
    )
    def complete_task_tool(task_id: str, user_id: str) -> dict:
        return task_service.complete_task(task_id, user_id)

    @mcp_app.tool(
        name="delete_task",
        description="Delete a task for the current user"
    )
    def delete_task_tool(task_id: str, user_id: str) -> dict:
        return task_service.delete_task(task_id, user_id)

    return mcp_app.streamable_http_app()
```

## Business Logic Enforcement

### User Scoping Rules
- All operations require user_id parameter
- Tasks can only be accessed by their owner
- Cross-user access is prevented at database level
- Permissions are validated before each operation

### Validation Checks
- Task existence verification
- User ownership validation
- Required field validation
- Data format validation
- Status transition validation

### Error Handling
- Missing task: Return appropriate error message
- Permission denied: Prevent operation with clear error
- Database errors: Handle gracefully with rollback
- Invalid data: Validate before persistence

## Security Considerations

### Data Isolation
- Row-level security ensures user data isolation
- All queries include user_id filter
- Foreign key relationships enforce referential integrity

### Input Validation
- Sanitize all user inputs
- Validate data types and formats
- Check for SQL injection possibilities
- Implement proper parameter binding

## Best Practices

### Transaction Safety
- Use database transactions for multi-step operations
- Implement proper rollback mechanisms
- Handle concurrent access appropriately
- Maintain consistency during updates

### Performance Optimization
- Index frequently queried columns
- Limit result sets with pagination
- Optimize queries for common access patterns
- Cache frequently accessed data when appropriate

### Data Integrity
- Implement proper foreign key constraints
- Use database triggers for automatic updates
- Validate data consistency across related entities
- Maintain audit trails for important operations