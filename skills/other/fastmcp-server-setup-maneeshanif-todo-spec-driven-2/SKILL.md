---
name: fastmcp-server-setup
description: Create MCP (Model Context Protocol) servers using FastMCP Python SDK. Define tools that AI agents can call to perform task operations. Use when building MCP servers for Phase 3 AI chatbot integration.
allowed-tools: Bash, Write, Read, Edit, Glob
---

# FastMCP Server Setup

Quick reference for creating MCP servers using FastMCP for the Todo AI Chatbot Phase 3.

**Reference Repository**: https://github.com/panaversity/learn-agentic-ai

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                      FastMCP Server                         │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐     ┌─────────────────────────────┐   │
│  │  @mcp.tool      │     │  Database Operations        │   │
│  │  add_task       │────▶│  SQLModel + Session         │   │
│  │  list_tasks     │     │                             │   │
│  │  complete_task  │     │  Task CRUD Operations       │   │
│  │  delete_task    │     │                             │   │
│  │  update_task    │     └─────────────────────────────┘   │
│  └─────────────────┘                                       │
│                                                             │
│  Transport Options: stdio | http | sse                      │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │ FastMCP Client calls
                              │
┌─────────────────────────────┴───────────────────────────────┐
│  OpenAI Agents SDK (Agent with MCP Tools)                   │
│  @function_tool wrappers → Client.call_tool()               │
└─────────────────────────────────────────────────────────────┘
```

**Key Insight**: The MCP server handles ALL database operations. The OpenAI Agent uses FastMCP Client to call these tools.

---

## Quick Start

### 1. Install Dependencies

```bash
cd backend
uv add fastmcp
```

### 2. Create Basic MCP Server

Create `backend/src/mcp_server/server.py`:

```python
from fastmcp import FastMCP

# Create MCP server
mcp = FastMCP("Todo MCP Server")

@mcp.tool
def hello(name: str = "World") -> str:
    """Say hello to someone."""
    return f"Hello, {name}!"

# Run server
if __name__ == "__main__":
    mcp.run()  # Default: stdio transport
```

### 3. Run the Server

```bash
# Default stdio transport (for CLI integration)
uv run python -m src.mcp_server.server

# HTTP transport (for web deployment) - RECOMMENDED for Phase 3
uv run python -m src.mcp_server.server  # modify server to use http

# SSE transport (legacy, for backward compatibility)
# Modify server: mcp.run(transport="sse", host="127.0.0.1", port=8001)
```

---

## Transport Options

| Transport | Use Case | Code | URL Pattern |
|-----------|----------|------|-------------|
| `stdio` | CLI, desktop apps, local dev | `mcp.run()` | N/A (spawned process) |
| `http` | Web deployment, API access | `mcp.run(transport="http", host="0.0.0.0", port=8001)` | `http://localhost:8001` |
| `sse` | Legacy SSE clients | `mcp.run(transport="sse", host="127.0.0.1", port=8001)` | `http://localhost:8001/sse` |

**Recommended for Phase 3**: Use `http` transport for agent integration. No `path` parameter needed for HTTP transport.

---

## Defining Tools

### Basic Tool (No Parentheses)

```python
@mcp.tool
def add_numbers(a: int, b: int) -> int:
    """Add two numbers together."""
    return a + b
```

### Tool with Custom Name

```python
@mcp.tool(name="custom_tool_name")
def my_function(x: int) -> str:
    """This tool has a custom name."""
    return str(x)
```

### Tool with Tags and Metadata

```python
@mcp.tool(
    name="find_products",
    description="Search the product catalog.",
    tags={"catalog", "search"},
    meta={"version": "1.2", "author": "team"}
)
def search_products(query: str, category: str | None = None) -> list[dict]:
    """Internal docstring (ignored if description provided above)."""
    return [{"id": 1, "name": "Product"}]
```

### Tool with Optional Parameters

```python
@mcp.tool
def create_task(
    title: str,
    description: str | None = None,
    priority: str = "medium"
) -> dict:
    """Create a new task.

    Args:
        title: The task title (required)
        description: Optional task description
        priority: Task priority (low, medium, high)
    """
    return {
        "status": "created",
        "title": title,
        "description": description,
        "priority": priority
    }
```

### Disabled Tool (Feature Flag)

```python
@mcp.tool(enabled=False)
def maintenance_tool() -> str:
    """This tool is currently under maintenance."""
    return "Disabled"
```

---

## Project Structure

```
backend/src/
├── mcp_server/
│   ├── __init__.py           # Package init
│   └── server.py             # FastMCP server with all tools
│
├── models/
│   └── task.py               # SQLModel Task model
│
├── database.py               # Database engine & session
│
└── agents/                   # OpenAI Agents (separate from MCP)
    ├── mcp_tools.py          # @function_tool wrappers for MCP
    └── ...
```

---

## Complete Todo MCP Server

```python
# backend/src/mcp_server/server.py
"""
FastMCP Server for Todo operations.
This server handles ALL database operations - the Agent just calls these tools.
"""
from fastmcp import FastMCP
from sqlmodel import Session, select
from src.database import engine
from src.models.task import Task

# Create MCP server
mcp = FastMCP("Todo MCP Server")


@mcp.tool
def add_task(user_id: str, title: str, description: str | None = None) -> dict:
    """Add a new task for a user.

    Args:
        user_id: The user's unique identifier
        title: The task title (required)
        description: Optional task description
    """
    with Session(engine) as session:
        task = Task(user_id=user_id, title=title, description=description)
        session.add(task)
        session.commit()
        session.refresh(task)
        return {
            "status": "created",
            "task_id": task.id,
            "title": task.title
        }


@mcp.tool
def list_tasks(user_id: str, status: str = "all") -> list[dict]:
    """List tasks for a user with optional status filter.

    Args:
        user_id: The user's unique identifier
        status: Filter by 'all', 'pending', or 'completed'
    """
    with Session(engine) as session:
        query = select(Task).where(Task.user_id == user_id)

        if status == "pending":
            query = query.where(Task.completed == False)
        elif status == "completed":
            query = query.where(Task.completed == True)

        tasks = session.exec(query).all()
        return [
            {
                "id": t.id,
                "title": t.title,
                "description": t.description,
                "completed": t.completed
            }
            for t in tasks
        ]


@mcp.tool
def complete_task(user_id: str, task_id: int) -> dict:
    """Mark a task as completed.

    Args:
        user_id: The user's unique identifier
        task_id: The ID of the task to mark complete
    """
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return {"status": "error", "message": "Task not found"}

        task.completed = True
        session.add(task)
        session.commit()
        return {"status": "completed", "task_id": task.id}


@mcp.tool
def delete_task(user_id: str, task_id: int) -> dict:
    """Delete a task permanently.

    Args:
        user_id: The user's unique identifier
        task_id: The ID of the task to delete
    """
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return {"status": "error", "message": "Task not found"}

        session.delete(task)
        session.commit()
        return {"status": "deleted", "task_id": task_id}


@mcp.tool
def update_task(
    user_id: str,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> dict:
    """Update a task's title and/or description.

    Args:
        user_id: The user's unique identifier
        task_id: The ID of the task to update
        title: New title for the task (optional)
        description: New description for the task (optional)
    """
    with Session(engine) as session:
        task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if not task:
            return {"status": "error", "message": "Task not found"}

        if title is not None:
            task.title = title
        if description is not None:
            task.description = description

        session.add(task)
        session.commit()
        return {
            "status": "updated",
            "task_id": task.id,
            "title": task.title
        }


if __name__ == "__main__":
    # HTTP transport for web integration (no path parameter needed)
    mcp.run(
        transport="http",
        host="0.0.0.0",
        port=8001,
    )
```

---

## FastMCP Client (for testing or Agent integration)

```python
# Test the MCP server with FastMCP Client
import asyncio
from fastmcp import Client

async def test_mcp_server():
    # Connect to HTTP server (no /mcp path needed)
    async with Client("http://localhost:8001") as client:
        # List available tools
        tools = await client.list_tools()
        print("Available tools:")
        for tool in tools:
            print(f"  - {tool.name}")

        # Call a tool
        result = await client.call_tool(
            "add_task",
            {
                "user_id": "test-user",
                "title": "Test task",
                "description": "Created via MCP client"
            }
        )
        print(f"Result: {result}")

if __name__ == "__main__":
    asyncio.run(test_mcp_server())
```

---

## Environment Variables

```env
# Database
DATABASE_URL=postgresql://user:pass@host/db

# MCP Server
MCP_SERVER_HOST=0.0.0.0
MCP_SERVER_PORT=8001
MCP_SERVER_PATH=/mcp
```

---

## Verification Checklist

- [ ] `fastmcp` package installed (`uv add fastmcp`)
- [ ] MCP server created with `FastMCP("name")`
- [ ] All 5 task tools implemented (add, list, complete, delete, update)
- [ ] Tools handle database operations correctly
- [ ] Server runs without errors
- [ ] Tools return proper dict/list responses
- [ ] HTTP transport configured for agent integration
- [ ] Can test with FastMCP Client

---

## See Also

- [REFERENCE.md](./REFERENCE.md) - Detailed FastMCP API reference
- [TOOLS.md](./TOOLS.md) - Tool definition patterns
- [examples.md](./examples.md) - More code examples
- [openai-agents-setup](../openai-agents-setup/) - Agent setup with MCP tools
- [FastMCP GitHub](https://github.com/jlowin/fastmcp)
