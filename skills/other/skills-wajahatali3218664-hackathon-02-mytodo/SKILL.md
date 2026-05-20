---
name: mcp-tools-skill
description: Define and implement MCP tools for task CRUD operations
when-to-use: Adding new task management capabilities for AI agent
---
# MCP Tools Skill

## Instructions

This skill provides guidance for defining and implementing Model Context Protocol (MCP) tools for task CRUD operations that AI agents can use.

### Project Structure
```
backend/
├── mcp/
│   ├── __init__.py
│   ├── server.py              # MCP server implementation
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── task_tools.py      # Task CRUD tools
│   │   └── user_tools.py      # User-related tools
│   └── schemas/
│       ├── __init__.py
│       └── tool_schemas.py    # JSON schemas for tools
```

### MCP Server Setup

```python
# backend/mcp/server.py
from mcp.server import Server
from mcp.types import Tool, TextContent
from contextlib import asynccontextmanager
import json

from database import get_db, AsyncSessionLocal
from tasks.service import TaskService
from auth.dependencies import get_current_user

app = Server("todo-mcp-server")

@asynccontextmanager
async def lifespan(app):
    # Startup: Initialize resources
    print("MCP Server starting...")
    yield
    # Shutdown: Cleanup resources
    print("MCP Server shutting down...")

# Dependency for getting database session
async def get_db_session():
    async with AsyncSessionLocal() as session:
        yield session

# Dependency for getting current user
async def get_current_user_context():
    # In production, this would extract user from context
    return {"id": 1, "email": "user@example.com"}
```

### Task CRUD Tools

```python
# backend/mcp/tools/task_tools.py
from mcp.types import Tool, TextContent
from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel

from database import AsyncSessionLocal
from tasks.service import TaskService
from auth.dependencies import get_current_user

class GetTasksInput(BaseModel):
    """Input for getting tasks"""
    completed: Optional[bool] = None
    limit: Optional[int] = 100
    offset: Optional[int] = 0

class CreateTaskInput(BaseModel):
    """Input for creating a task"""
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = "medium"

class UpdateTaskInput(BaseModel):
    """Input for updating a task"""
    task_id: int
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None
    due_date: Optional[datetime] = None
    priority: Optional[str] = None

class DeleteTaskInput(BaseModel):
    """Input for deleting a task"""
    task_id: int

# Tool: Get Tasks
async def get_tasks(input_json: str) -> List[TextContent]:
    """Get all tasks for the current user, optionally filtered by completion status."""
    try:
        data = GetTasksInput.model_validate_json(input_json)
    except Exception as e:
        return [TextContent(type="text", text=f"Error parsing input: {e}")]

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        service = TaskService(db)
        tasks = await service.get_tasks(
            owner_id=user.id,
            completed=data.completed,
            limit=data.limit,
            offset=data.offset
        )

        result = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

        return [TextContent(
            type="text",
            text=json.dumps({"tasks": result, "count": len(result)}, indent=2)
        )]

# Tool: Create Task
async def create_task(input_json: str) -> List[TextContent]:
    """Create a new task for the current user."""
    try:
        data = CreateTaskInput.model_validate_json(input_json)
    except Exception as e:
        return [TextContent(type="text", text=f"Error parsing input: {e}")]

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        service = TaskService(db)
        task = await service.create_task(
            task_data={
                "title": data.title,
                "description": data.description,
                "due_date": data.due_date,
                "priority": data.priority,
            },
            owner_id=user.id
        )

        return [TextContent(
            type="text",
            text=json.dumps({
                "message": f"Task '{task.title}' created successfully",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "created_at": task.created_at.isoformat(),
                }
            }, indent=2)
        )]

# Tool: Update Task
async def update_task(input_json: str) -> List[TextContent]:
    """Update an existing task."""
    try:
        data = UpdateTaskInput.model_validate_json(input_json)
    except Exception as e:
        return [TextContent(type="text", text=f"Error parsing input: {e}")]

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        service = TaskService(db)

        update_data = {}
        if data.title is not None:
            update_data["title"] = data.title
        if data.description is not None:
            update_data["description"] = data.description
        if data.completed is not None:
            update_data["completed"] = data.completed
        if data.due_date is not None:
            update_data["due_date"] = data.due_date
        if data.priority is not None:
            update_data["priority"] = data.priority

        task = await service.update_task(
            task_id=data.task_id,
            update_data=update_data,
            owner_id=user.id
        )

        if not task:
            return [TextContent(
                type="text",
                text=f"Task {data.task_id} not found or you don't have permission to update it."
            )]

        return [TextContent(
            type="text",
            text=f"Task {task.id} updated successfully"
        )]

# Tool: Delete Task
async def delete_task(input_json: str) -> List[TextContent]:
    """Delete a task."""
    try:
        data = DeleteTaskInput.model_validate_json(input_json)
    except Exception as e:
        return [TextContent(type="text", text=f"Error parsing input: {e}")]

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        service = TaskService(db)
        success = await service.delete_task(
            task_id=data.task_id,
            owner_id=user.id
        )

        if not success:
            return [TextContent(
                type="text",
                text=f"Task {data.task_id} not found or you don't have permission to delete it."
            )]

        return [TextContent(
            type="text",
            text=f"Task {data.task_id} deleted successfully"
        )]
```

### Register Tools with Server

```python
# backend/mcp/server.py (continued)
from mcp.tools.task_tools import (
    get_tasks,
    create_task,
    update_task,
    delete_task,
)

# Define tool definitions for discovery
TOOLS = [
    Tool(
        name="get_tasks",
        description="Get all tasks for the current user, optionally filtered by completion status",
        inputSchema={
            "type": "object",
            "properties": {
                "completed": {
                    "type": "boolean",
                    "description": "Filter by completion status"
                },
                "limit": {
                    "type": "integer",
                    "description": "Maximum number of tasks to return",
                    "default": 100
                },
                "offset": {
                    "type": "integer",
                    "description": "Number of tasks to skip",
                    "default": 0
                }
            }
        }
    ),
    Tool(
        name="create_task",
        description="Create a new task for the current user",
        inputSchema={
            "type": "object",
            "properties": {
                "title": {
                    "type": "string",
                    "description": "Task title (required)"
                },
                "description": {
                    "type": "string",
                    "description": "Optional task description"
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "Optional due date in ISO format"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "Task priority",
                    "default": "medium"
                }
            },
            "required": ["title"]
        }
    ),
    Tool(
        name="update_task",
        description="Update an existing task's properties",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID of the task to update (required)"
                },
                "title": {
                    "type": "string",
                    "description": "New task title"
                },
                "description": {
                    "type": "string",
                    "description": "New task description"
                },
                "completed": {
                    "type": "boolean",
                    "description": "Completion status"
                },
                "due_date": {
                    "type": "string",
                    "format": "date-time",
                    "description": "New due date"
                },
                "priority": {
                    "type": "string",
                    "enum": ["low", "medium", "high"],
                    "description": "New priority"
                }
            },
            "required": ["task_id"]
        }
    ),
    Tool(
        name="delete_task",
        description="Delete a task",
        inputSchema={
            "type": "object",
            "properties": {
                "task_id": {
                    "type": "integer",
                    "description": "ID of the task to delete (required)"
                }
            },
            "required": ["task_id"]
        }
    ),
]

@app.list_tools()
async def list_tools():
    return TOOLS

@app.call_tool()
async def call_tool(name: str, arguments: str) -> List[TextContent]:
    """Handle tool calls from the client."""
    if name == "get_tasks":
        return await get_tasks(arguments)
    elif name == "create_task":
        return await create_task(arguments)
    elif name == "update_task":
        return await update_task(arguments)
    elif name == "delete_task":
        return await delete_task(arguments)
    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]
```

## Examples

### User-Related MCP Tools

```python
# backend/mcp/tools/user_tools.py
from mcp.types import Tool, TextContent
from typing import Optional
from pydantic import BaseModel
import json

class GetUserProfileInput(BaseModel):
    include_tasks_count: bool = False

class UpdatePreferencesInput(BaseModel):
    theme: Optional[str] = None
    notifications_enabled: Optional[bool] = None
    default_priority: Optional[str] = None

async def get_user_profile(input_json: str) -> List[TextContent]:
    """Get the current user's profile information."""
    data = GetUserProfileInput.model_validate_json(input_json)

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        result = {
            "id": user.id,
            "email": user.email,
            "name": user.name,
            "created_at": user.created_at.isoformat(),
        }

        if data.include_tasks_count:
            service = TaskService(db)
            result["tasks_count"] = {
                "total": await service.count_tasks(user.id),
                "completed": await service.count_tasks(user.id, completed=True),
                "pending": await service.count_tasks(user.id, completed=False),
            }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]

async def update_user_preferences(input_json: str) -> List[TextContent]:
    """Update user preferences."""
    data = UpdatePreferencesInput.model_validate_json(input_json)

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        service = UserService(db)

        update_data = {}
        if data.theme is not None:
            update_data["theme"] = data.theme
        if data.notifications_enabled is not None:
            update_data["notifications_enabled"] = data.notifications_enabled
        if data.default_priority is not None:
            update_data["default_priority"] = data.default_priority

        await service.update_preferences(user.id, update_data)

        return [TextContent(type="text", text="Preferences updated successfully")]
```

### Search Tool

```python
# backend/mcp/tools/search_tools.py
from mcp.types import Tool, TextContent
from typing import Optional
from pydantic import BaseModel
import json

class SearchTasksInput(BaseModel):
    query: str
    completed: Optional[bool] = None
    limit: Optional[int] = 20

async def search_tasks(input_json: str) -> List[TextContent]:
    """Search tasks by title or description using keyword matching."""
    data = SearchTasksInput.model_validate_json(input_json)

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        service = TaskService(db)
        tasks = await service.search_tasks(
            user.id,
            data.query,
            completed=data.completed,
            limit=data.limit
        )

        result = {
            "query": data.query,
            "results": [
                {
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "match_type": "title" if data.query.lower() in task.title.lower() else "description"
                }
                for task in tasks
            ],
            "count": len(tasks)
        }

        return [TextContent(type="text", text=json.dumps(result, indent=2))]
```

### Bulk Operations Tool

```python
# backend/mcp/tools/bulk_tools.py
from mcp.types import Tool, TextContent
from typing import List
from pydantic import BaseModel
import json

class BulkCompleteInput(BaseModel):
    task_ids: List[int]
    completed: bool = True

async def bulk_update_tasks(input_json: str) -> List[TextContent]:
    """Bulk update multiple tasks at once."""
    data = BulkCompleteInput.model_validate_json(input_json)

    async with AsyncSessionLocal() as db:
        user = await get_current_user(db)
        service = TaskService(db)

        updated = await service.bulk_update(
            user.id,
            data.task_ids,
            {"completed": data.completed}
        )

        return [TextContent(
            type="text",
            text=f"Updated {updated} tasks successfully"
        )]
```

### MCP Server Entry Point

```python
# backend/mcp/__main__.py
from mcp.server.stdio import stdio_server
import asyncio

async def main():
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
```

### Run MCP Server

```bash
# Start MCP server with stdio transport
python -m mcp
```

### Connect from AI Client

```typescript
// Example: Connecting to MCP server from AI agent
import { MCPClient } from 'mcp-client'

const client = new MCPClient()

async function setupTaskTools() {
  // Connect to MCP server via stdio
  const tools = await client.connect({
    command: 'python',
    args: ['-m', 'mcp'],
    env: {
      DATABASE_URL: process.env.DATABASE_URL,
      JWT_SECRET_KEY: process.env.JWT_SECRET_KEY,
    }
  })

  // Now the AI agent can call tools
  const tasks = await tools.get_tasks({ completed: false })
  return tasks
}
```
