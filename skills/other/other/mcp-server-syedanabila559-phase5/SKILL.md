---
name: mcp-server
description: This skill should be used when setting up a stateless MCP (Model Context Protocol) server in FastAPI using the Official MCP SDK with 5 task management tools that interact with SQLModel database.
---

# MCP Server Setup Skill

This skill provides guidance for setting up a stateless MCP server using the Official MCP SDK in FastAPI.

## Purpose

Create a stateless MCP server that provides 5 task management tools (add_task, list_tasks, complete_task, delete_task, update_task) with proper user isolation, database integration, and error handling.

## When to Use

Use this skill when:
- Setting up a new MCP server for chatbot integration
- Adding MCP tools for task management functionality
- Creating MCP server infrastructure with database integration
- Implementing tool chaining and error handling for MCP

## Capabilities

- **Stateless Design**: Each request independent, no server-side state between calls
- **User Isolation**: All tools require user_id and enforce ownership at query level
- **Tool Chaining**: Tools designed to be safely called by other tools
- **Async Performance**: Full async/await support for concurrent operations
- **Error Handling**: Structured errors (400, 401, 403, 404, 500) with descriptive messages

## MCP Server Architecture

### Server Structure

```
backend/
├── mcp_server.py      # Main MCP server with FastAPI integration
├── mcp_tools.py       # Tool implementations
├── mcp_config.py      # Server configuration
└── main.py            # Updated with MCP server startup
```

### Tool Signatures

| Tool | Parameters | Returns |
|------|------------|---------|
| `add_task` | user_id: str, title: str, description?: str, priority?: int, due_date?: str | {success: bool, task_id: str, task: dict} |
| `list_tasks` | user_id: str, status?: str, priority?: int | {success: bool, tasks: list[dict]} |
| `complete_task` | user_id: str, task_id: str | {success: bool, task: dict} |
| `delete_task` | user_id: str, task_id: str | {success: bool, deleted_task_id: str} |
| `update_task` | user_id: str, task_id: str, title?: str, description?: str, priority?: int, due_date?: str | {success: bool, task: dict} |

## Implementation Pattern

### MCP Server Setup

```python
from mcp.server.fastapi import FastAPIMCP
from fastapi import FastAPI

app = FastAPI()
mcp_server = FastAPIMCP(app)

@mcp_server.tool()
async def add_task(user_id: str, title: str, description: str = None) -> dict:
    """Add a new task for the specified user."""
    # Extract user_id from context
    # Validate parameters
    # Execute with user_id filter: WHERE user_id = :user_id
    # Return structured JSON response
```

### Database Session Management

```python
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

engine = create_async_engine(DATABASE_URL)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_db_session():
    async with async_session() as session:
        yield session
```

### User ID Enforcement

```python
async def add_task(user_id: str, title: str, ...) -> dict:
    if not user_id:
        raise ValueError("user_id is required")

    # Always filter by user_id in queries
    statement = select(Task).where(
        Task.id == task_id,
        Task.user_id == user_id  # Critical for isolation
    )
```

## Tool Implementation Checklist

For each tool, implement:

1. **Parameter Validation**: Check required fields, types, and constraints
2. **User ID Extraction**: Get user_id from request context or parameters
3. **Database Operation**: Execute with proper user_id filtering
4. **Response Construction**: Return structured JSON with success status
5. **Error Handling**: Catch exceptions and return appropriate error codes
6. **Logging**: Log operation outcomes for debugging

## Error Taxonomy

| Status | Condition | Example |
|--------|-----------|---------|
| 400 | Invalid input parameters | Missing required fields, invalid types |
| 401 | Missing/unauthorized user | No user_id provided |
| 403 | User not authorized | user_id doesn't match resource owner |
| 404 | Resource not found | Task doesn't exist |
| 500 | Internal error | Database connection failed |

## Tool Chaining Support

Design tools to support chaining:

```python
async def complete_task(user_id: str, task_id: str) -> dict:
    """Mark a task as complete. Can be called by other tools."""
    task = await get_task_by_id(user_id, task_id)
    if task:
        task.completed = True
        await session.commit()
    return {"success": True, "task": task_to_dict(task)}

async def list_tasks(user_id: str, status: str = None) -> dict:
    """List tasks. Supports filtering by status."""
    # This can chain to complete_task or other tools
```

## Dependencies

```txt
mcp>=0.9.0
fastapi>=0.100.0
sqlmodel>=0.0.14
sqlalchemy>=2.0.0
```

## Running the Server

```bash
cd backend
uvicorn mcp_server:app --host 0.0.0.0 --port 8001
```

## Integration with Main App

```python
# main.py
from mcp_server import mcp

app = FastAPI()
app.include_router(mcp.router)

@app.on_event("startup")
async def startup():
    await mcp.run()
```

## Verification Checklist

- [ ] All 5 tools registered and accessible
- [ ] User ID enforced in every database query
- [ ] JSON responses match specification
- [ ] Error handling returns appropriate codes
- [ ] Tool chaining works correctly
- [ ] Server starts without errors
- [ ] Database connections work
