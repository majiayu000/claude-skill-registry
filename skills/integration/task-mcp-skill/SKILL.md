---
name: task-mcp-skill
description: Stateless MCP tool execution layer that exposes task CRUD operations (add, list, update, complete, delete) with database-only state persistence for AI agent integration.
---

# Task MCP Skill

Use this skill when implementing MCP tools for task operations that will be invoked by AI agents.

## When to Use

- Exposing task operations as MCP tools for OpenAI Agents SDK
- Implementing stateless, database-backed CRUD operations
- Building tools that AI agents can invoke
- Ensuring horizontal scalability for task operations
- Creating auditable, deterministic task execution layer

## Core Principles

### Stateless Execution
- **No in-memory state**: Every request is independent
- **No conversation awareness**: Tools don't know about chat history
- **Database-only persistence**: All state in PostgreSQL
- **Horizontally scalable**: Any instance can handle any request
- **Deterministic**: Same input → same output

## MCP Tools Specification

### 1. add_task

**Purpose**: Create a new task

```python
# app/mcp/tools.py
from typing import Optional
from sqlmodel import Session
from app.models import Task

async def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: str = "medium",
    due_date: Optional[str] = None,
    tag_ids: Optional[List[int]] = None,
    db: Session = None
) -> dict:
    """
    Create a new task with optional tags.

    Parameters:
        user_id: User identifier
        title: Task title (required, 1-200 chars)
        description: Task description (optional, max 1000 chars)
        priority: Priority level (high/medium/low)
        due_date: Due date ISO format (optional)
        tag_ids: List of tag IDs to associate (optional)

    Returns:
        {
            "task_id": int,
            "status": "created",
            "title": str,
            "tags": List[str]
        }
    """
    # Validate
    if not title or len(title) > 200:
        return {
            "error": "Title is required and must be 1-200 characters",
            "status": "failed"
        }

    # Create task
    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        priority=priority,
        due_date=due_date
    )

    db.add(task)
    db.flush()  # Get task ID before adding tags

    # Add tags if provided
    if tag_ids:
        from app.models import TaskTag
        for tag_id in tag_ids:
            task_tag = TaskTag(task_id=task.id, tag_id=tag_id)
            db.add(task_tag)

    db.commit()
    db.refresh(task)

    # Get tag names
    tag_names = []
    if tag_ids:
        from app.models import Tag
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        tag_names = [t.name for t in tags]

    return {
        "task_id": task.id,
        "status": "created",
        "title": task.title,
        "tags": tag_names
    }
```

**OpenAI Tool Schema**:
```python
{
    "type": "function",
    "function": {
        "name": "add_task",
        "description": "Create a new todo task",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "title": {
                    "type": "string",
                    "description": "Task title"
                },
                "description": {
                    "type": "string",
                    "description": "Optional task description"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Task priority"
                }
            },
            "required": ["user_id", "title"]
        }
    }
}
```

---

### 2. list_tasks

**Purpose**: Retrieve tasks for a user

```python
async def list_tasks(
    user_id: str,
    status: str = "all",
    priority: Optional[str] = None,
    tag_query: Optional[str] = None,
    sort_by: str = "created_at",
    db: Session = None
) -> dict:
    """
    List tasks with optional filters and sorting.

    Parameters:
        user_id: User identifier
        status: "all", "pending", or "completed"
        priority: Optional priority filter (high/medium/low)
        tag_query: Optional tag name filter (e.g., "work")
        sort_by: Sort field (priority/due_date/title/created_at)

    Returns:
        {
            "tasks": [
                {"id": int, "title": str, "completed": bool, "tags": [...], ...}
            ],
            "count": int
        }
    """
    from app.models import Tag, TaskTag

    query = db.query(Task).filter(Task.user_id == user_id)

    # Status filter
    if status == "pending":
        query = query.filter(Task.completed == False)
    elif status == "completed":
        query = query.filter(Task.completed == True)

    # Priority filter
    if priority:
        query = query.filter(Task.priority == priority)

    # Tag filter
    if tag_query:
        query = query.join(TaskTag).join(Tag).filter(
            Tag.name.ilike(f"%{tag_query}%")
        )

    # Sorting
    sort_map = {
        "priority": Task.priority.desc(),
        "due_date": Task.due_date.asc(),
        "title": Task.title.asc(),
        "created_at": Task.created_at.desc()
    }
    order_clause = sort_map.get(sort_by, Task.created_at.desc())
    query = query.order_by(order_clause)

    tasks = query.all()

    # Build response with tags
    result_tasks = []
    for t in tasks:
        # Get tags for this task
        task_tags = db.query(Tag).join(TaskTag).filter(
            TaskTag.task_id == t.id
        ).all()

        result_tasks.append({
            "id": t.id,
            "title": t.title,
            "description": t.description,
            "completed": t.completed,
            "priority": t.priority,
            "due_date": str(t.due_date) if t.due_date else None,
            "tags": [tag.name for tag in task_tags]
        })

    return {
        "tasks": result_tasks,
        "count": len(result_tasks)
    }
```

**OpenAI Tool Schema**:
```python
{
    "type": "function",
    "function": {
        "name": "list_tasks",
        "description": "Retrieve user's tasks with optional filters, tag filter, and sorting",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "status": {
                    "type": "string",
                    "enum": ["all", "pending", "completed"],
                    "description": "Filter by completion status"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "Filter by priority"
                },
                "tag_query": {
                    "type": "string",
                    "description": "Filter by tag name (e.g., 'work', 'personal')"
                },
                "sort_by": {
                    "type": "string",
                    "enum": ["priority", "due_date", "title", "created_at"],
                    "description": "Sort tasks by field"
                }
            },
            "required": ["user_id"]
        }
    }
}
```

---

### 3. complete_task

**Purpose**: Toggle task completion status

```python
async def complete_task(
    user_id: str,
    task_id: int,
    db: Session = None
) -> dict:
    """
    Mark task as complete.

    Parameters:
        user_id: User identifier
        task_id: Task ID to complete

    Returns:
        {
            "task_id": int,
            "status": "completed",
            "title": str
        }
    """
    # Fetch and validate ownership
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        return {
            "error": f"Task {task_id} not found",
            "status": "failed"
        }

    # Toggle completion
    task.completed = True
    task.completed_at = datetime.utcnow()
    db.commit()

    return {
        "task_id": task.id,
        "status": "completed",
        "title": task.title
    }
```

**OpenAI Tool Schema**:
```python
{
    "type": "function",
    "function": {
        "name": "complete_task",
        "description": "Mark a task as complete",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "task_id": {
                    "type": "integer",
                    "description": "ID of task to complete"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
```

---

### 4. delete_task

**Purpose**: Permanently remove a task

```python
async def delete_task(
    user_id: str,
    task_id: int,
    db: Session = None
) -> dict:
    """
    Delete a task permanently.

    Parameters:
        user_id: User identifier
        task_id: Task ID to delete

    Returns:
        {
            "task_id": int,
            "status": "deleted",
            "title": str
        }
    """
    # Fetch and validate
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        return {
            "error": f"Task {task_id} not found",
            "status": "failed"
        }

    title = task.title
    db.delete(task)
    db.commit()

    return {
        "task_id": task_id,
        "status": "deleted",
        "title": title
    }
```

**OpenAI Tool Schema**:
```python
{
    "type": "function",
    "function": {
        "name": "delete_task",
        "description": "Delete a task permanently",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "task_id": {
                    "type": "integer",
                    "description": "ID of task to delete"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
```

---

### 5. update_task

**Purpose**: Modify existing task fields

```python
async def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
    db: Session = None
) -> dict:
    """
    Update task fields.

    Parameters:
        user_id: User identifier
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)
        priority: New priority (optional)

    Returns:
        {
            "task_id": int,
            "status": "updated",
            "title": str
        }
    """
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        return {
            "error": f"Task {task_id} not found",
            "status": "failed"
        }

    # Update fields
    if title:
        task.title = title
    if description is not None:
        task.description = description
    if priority:
        task.priority = priority

    task.updated_at = datetime.utcnow()
    db.commit()

    return {
        "task_id": task.id,
        "status": "updated",
        "title": task.title
    }
```

**OpenAI Tool Schema**:
```python
{
    "type": "function",
    "function": {
        "name": "update_task",
        "description": "Update task fields",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "task_id": {
                    "type": "integer",
                    "description": "ID of task to update"
                },
                "title": {
                    "type": "string",
                    "description": "New title"
                },
                "description": {
                    "type": "string",
                    "description": "New description"
                },
                "priority": {
                    "type": "string",
                    "enum": ["high", "medium", "low"],
                    "description": "New priority"
                }
            },
            "required": ["user_id", "task_id"]
        }
    }
}
```

---

### 6. add_tag_to_task

**Purpose**: Add a tag to an existing task

```python
async def add_tag_to_task(
    user_id: str,
    task_id: int,
    tag_name: str,
    db: Session = None
) -> dict:
    """
    Add or create a tag and associate it with a task.

    Parameters:
        user_id: User identifier
        task_id: Task ID to tag
        tag_name: Tag name (will be created if doesn't exist)

    Returns:
        {
            "task_id": int,
            "tag_name": str,
            "status": "tagged"
        }
    """
    from app.models import Tag, TaskTag

    # Verify task ownership
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.user_id == user_id
    ).first()

    if not task:
        return {
            "error": f"Task {task_id} not found",
            "status": "failed"
        }

    # Get or create tag
    tag = db.query(Tag).filter(
        Tag.name == tag_name,
        Tag.user_id == user_id
    ).first()

    if not tag:
        tag = Tag(name=tag_name, user_id=user_id)
        db.add(tag)
        db.flush()

    # Check if already tagged
    existing = db.query(TaskTag).filter(
        TaskTag.task_id == task_id,
        TaskTag.tag_id == tag.id
    ).first()

    if existing:
        return {
            "task_id": task_id,
            "tag_name": tag_name,
            "status": "already_tagged"
        }

    # Add tag association
    task_tag = TaskTag(task_id=task_id, tag_id=tag.id)
    db.add(task_tag)
    db.commit()

    return {
        "task_id": task_id,
        "tag_name": tag_name,
        "status": "tagged"
    }
```

**OpenAI Tool Schema**:
```python
{
    "type": "function",
    "function": {
        "name": "add_tag_to_task",
        "description": "Add a tag/label to an existing task",
        "parameters": {
            "type": "object",
            "properties": {
                "user_id": {
                    "type": "string",
                    "description": "User identifier"
                },
                "task_id": {
                    "type": "integer",
                    "description": "ID of task to tag"
                },
                "tag_name": {
                    "type": "string",
                    "description": "Tag name (e.g., 'work', 'urgent', 'personal')"
                }
            },
            "required": ["user_id", "task_id", "tag_name"]
        }
    }
}
```

---

## MCP Server Implementation

```python
# app/mcp/server.py
from mcp import MCPServer
from app.mcp.tools import add_task, list_tasks, complete_task, delete_task, update_task

class TodoMCPServer:
    """MCP server exposing task operations."""

    def __init__(self, db_session):
        self.db = db_session
        self.tools = {
            "add_task": add_task,
            "list_tasks": list_tasks,
            "complete_task": complete_task,
            "delete_task": delete_task,
            "update_task": update_task,
        }

    async def call_tool(self, tool_name: str, parameters: dict) -> dict:
        """Execute MCP tool."""
        if tool_name not in self.tools:
            return {
                "error": f"Unknown tool: {tool_name}",
                "status": "failed"
            }

        tool_fn = self.tools[tool_name]

        try:
            result = await tool_fn(**parameters, db=self.db)
            return result
        except Exception as e:
            return {
                "error": str(e),
                "status": "failed"
            }

    def get_tool_schemas(self) -> list:
        """Return OpenAI-compatible tool schemas."""
        return [
            # ... (all 5 tool schemas from above)
        ]
```

---

## Error Handling

```python
# app/mcp/errors.py

class MCPError(Exception):
    """Base MCP error."""
    pass

class TaskNotFoundError(MCPError):
    """Task doesn't exist or doesn't belong to user."""
    pass

class ValidationError(MCPError):
    """Invalid input parameters."""
    pass

# In tools
def add_task(...):
    if not title:
        raise ValidationError("Title is required")

    # ... rest of implementation
```

---

## Testing

```python
# tests/test_mcp_tools.py
import pytest
from app.mcp.tools import add_task, list_tasks, complete_task

@pytest.mark.asyncio
async def test_add_task(db_session):
    result = await add_task(
        user_id="user123",
        title="Buy groceries",
        db=db_session
    )

    assert result["status"] == "created"
    assert result["title"] == "Buy groceries"
    assert "task_id" in result

@pytest.mark.asyncio
async def test_list_tasks_pending(db_session):
    # Create test tasks
    await add_task(user_id="user123", title="Task 1", db=db_session)
    await add_task(user_id="user123", title="Task 2", db=db_session)

    # List pending
    result = await list_tasks(
        user_id="user123",
        status="pending",
        db=db_session
    )

    assert result["count"] == 2
    assert len(result["tasks"]) == 2

@pytest.mark.asyncio
async def test_complete_task(db_session):
    # Create task
    created = await add_task(user_id="user123", title="Test", db=db_session)

    # Complete it
    result = await complete_task(
        user_id="user123",
        task_id=created["task_id"],
        db=db_session
    )

    assert result["status"] == "completed"
```

---

## Integration Flow

```
User Message → ChatKit UI
           ↓
FastAPI Chat Endpoint
           ↓
TodoChatAgent (OpenAI Agents SDK)
           ↓
Task Intent Skill (detects intent)
           ↓
Task MCP Skill (executes tool)
           ↓
Database (PostgreSQL via SQLModel)
           ↓
Structured Result
           ↓
Agent Response
           ↓
ChatKit UI
```

---

## Best Practices

1. **Stateless Design**: No session state, no memory between calls
2. **Database-Only State**: All persistence in PostgreSQL
3. **User Isolation**: Always filter by user_id
4. **Input Validation**: Validate all parameters before DB operations
5. **Error Returns**: Return structured errors, don't raise exceptions
6. **Atomic Operations**: Each tool call is a single transaction
7. **Idempotent Where Possible**: Safe to retry operations
8. **Clear Contracts**: Consistent input/output schemas

---

## Security Considerations

- **Always validate user_id**: Ensure task belongs to requesting user
- **SQL Injection**: Use SQLModel parameterized queries
- **Authorization**: Verify ownership before update/delete
- **Input Sanitization**: Validate lengths and formats
- **Rate Limiting**: Implement at API gateway level

---

**Production Standard**: This skill ensures stateless, scalable, and auditable task operations that AI agents can reliably invoke through MCP protocol.
