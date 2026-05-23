---
name: openai-agents-mcp-integration
description: >
  Build AI agents with OpenAI Agents SDK + Model Context Protocol (MCP) for tool orchestration.
  Supports multi-provider backends (OpenAI, Gemini, Groq, OpenRouter) with MCPServerStdio.
  Use this skill for conversational AI features with external tool access via MCP protocol.
---

# OpenAI Agents SDK + MCP Integration Skill

You are a **specialist in building AI agents with OpenAI Agents SDK and MCP tool orchestration**.

Your job is to help users design and implement **conversational AI agents** that:
- Use **OpenAI Agents SDK** (v0.2.9+) for agent orchestration
- Connect to **MCP servers** via stdio transport for tool access
- Support **multiple LLM providers** (OpenAI, Gemini, Groq, OpenRouter)
- Integrate with **web frameworks** (FastAPI, Django, Flask)
- Handle **streaming responses** with Server-Sent Events (SSE)
- Persist **conversation state** in databases (PostgreSQL, SQLite)

This Skill acts as a **stable, opinionated guide** for:
- Clean separation between agent logic and MCP tools
- Multi-provider model factory patterns
- Database-backed conversation persistence
- Production-ready error handling and timeouts

## 1. When to Use This Skill

Use this Skill **whenever** the user mentions:

- "OpenAI Agents SDK with MCP"
- "conversational AI with external tools"
- "agent with MCP server"
- "multi-provider AI backend"
- "chat agent with database persistence"

Or asks to:
- Build a chatbot that calls external APIs/tools
- Create an agent that uses MCP protocol for tool access
- Implement conversation history with AI agents
- Support multiple LLM providers in one codebase
- Stream agent responses to frontend

If the user wants simple OpenAI API calls without agents or tools, this Skill is overkill.

## 2. Architecture Overview

### 2.1 High-Level Flow

```
User → Frontend → FastAPI Backend → Agent → MCP Server → Tools → Database/APIs
                           ↓                    ↓
                    Conversation DB        Tool Results
```

### 2.2 Component Responsibilities

**Frontend**:
- Sends user messages to backend chat endpoint
- Receives streaming SSE responses
- Displays agent responses and tool results

**FastAPI Backend**:
- Handles `/api/{user_id}/chat` endpoint
- Creates Agent with model from factory
- Manages MCP server connection lifecycle
- Persists conversations to database
- Streams agent responses via SSE

**Agent (OpenAI Agents SDK)**:
- Orchestrates conversation flow
- Decides when to call tools
- Generates natural language responses
- Handles multi-turn conversations

**MCP Server (Official MCP SDK)**:
- Exposes tools via MCP protocol
- Runs as separate process (stdio transport)
- Handles tool execution (database, APIs)
- Returns results to agent

## 3. Core Implementation Patterns

### 3.1 Multi-Provider Model Factory

**Pattern**: Centralized `create_model()` function for LLM provider abstraction.

**Why**:
- Single codebase supports multiple providers
- Easy provider switching via environment variable
- Cost optimization (use free/cheap models for dev)
- Vendor independence

**Implementation**:

```python
# agent_config/factory.py
import os
from pathlib import Path
from dotenv import load_dotenv
from agents import OpenAIChatCompletionsModel
from openai import AsyncOpenAI

# Load .env file
env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path, override=True)

def create_model(provider: str | None = None, model: str | None = None) -> OpenAIChatCompletionsModel:
    """
    Create LLM model instance based on environment configuration.

    Args:
        provider: Override LLM_PROVIDER env var ("openai" | "gemini" | "groq" | "openrouter")
        model: Override model name

    Returns:
        OpenAIChatCompletionsModel configured for selected provider

    Raises:
        ValueError: If provider unsupported or API key missing
    """
    provider = provider or os.getenv("LLM_PROVIDER", "openai").lower()

    if provider == "openai":
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY required when LLM_PROVIDER=openai")

        client = AsyncOpenAI(api_key=api_key)
        model_name = model or os.getenv("OPENAI_DEFAULT_MODEL", "gpt-4o-mini")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    elif provider == "gemini":
        api_key = os.getenv("GEMINI_API_KEY")
        if not api_key:
            raise ValueError("GEMINI_API_KEY required when LLM_PROVIDER=gemini")

        # Gemini via OpenAI-compatible API
        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://generativelanguage.googleapis.com/v1beta/openai/",
        )
        model_name = model or os.getenv("GEMINI_DEFAULT_MODEL", "gemini-2.5-flash")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    elif provider == "groq":
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY required when LLM_PROVIDER=groq")

        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://api.groq.com/openai/v1",
        )
        model_name = model or os.getenv("GROQ_DEFAULT_MODEL", "llama-3.3-70b-versatile")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    elif provider == "openrouter":
        api_key = os.getenv("OPENROUTER_API_KEY")
        if not api_key:
            raise ValueError("OPENROUTER_API_KEY required when LLM_PROVIDER=openrouter")

        client = AsyncOpenAI(
            api_key=api_key,
            base_url="https://openrouter.ai/api/v1",
        )
        model_name = model or os.getenv("OPENROUTER_DEFAULT_MODEL", "openai/gpt-oss-20b:free")

        return OpenAIChatCompletionsModel(model=model_name, openai_client=client)

    else:
        raise ValueError(
            f"Unsupported provider: {provider}. "
            f"Supported: openai, gemini, groq, openrouter"
        )
```

**Environment Variables**:

```bash
# Provider selection
LLM_PROVIDER=openrouter  # "openai", "gemini", "groq", or "openrouter"

# OpenAI
OPENAI_API_KEY=sk-...
OPENAI_DEFAULT_MODEL=gpt-4o-mini

# Gemini
GEMINI_API_KEY=AIza...
GEMINI_DEFAULT_MODEL=gemini-2.5-flash

# Groq
GROQ_API_KEY=gsk_...
GROQ_DEFAULT_MODEL=llama-3.3-70b-versatile

# OpenRouter (free models available!)
OPENROUTER_API_KEY=sk-or-v1-...
OPENROUTER_DEFAULT_MODEL=openai/gpt-oss-20b:free
```

### 3.2 Agent with MCP Server Connection

**Pattern**: Agent connects to MCP server via MCPServerStdio for tool access.

**Why**:
- Clean separation: Agent logic vs tool implementation
- MCP server runs as separate process (stdio transport)
- Tools accessed via standardized MCP protocol
- Easy to add/remove tools without changing agent code

**Critical Configuration**:
```python
# IMPORTANT: Set client_session_timeout_seconds for database operations
# Default 5s is too short - database queries may timeout
# Increase to 30s or more for production workloads
MCPServerStdio(
    name="task-management-server",
    params={...},
    client_session_timeout_seconds=30.0,  # MCP ClientSession timeout
)
```

**Implementation**:

```python
# agent_config/todo_agent.py
import os
from pathlib import Path
from agents import Agent
from agents.mcp import MCPServerStdio
from agents.model_settings import ModelSettings
from agent_config.factory import create_model

class TodoAgent:
    """
    AI agent for conversational task management.

    Connects to MCP server via stdio for tool access.
    Supports multiple LLM providers via model factory.
    """

    def __init__(self, provider: str | None = None, model: str | None = None):
        """
        Initialize agent with model and MCP server.

        Args:
            provider: LLM provider ("openai" | "gemini" | "groq" | "openrouter")
            model: Model name (overrides env var default)
        """
        # Create model from factory
        self.model = create_model(provider=provider, model=model)

        # Get MCP server module path
        backend_dir = Path(__file__).parent.parent
        mcp_server_path = backend_dir / "mcp_server" / "tools.py"

        # Create MCP server connection via stdio
        # CRITICAL: Set client_session_timeout_seconds for database operations
        # Default: 5 seconds → Setting to 30 seconds for production
        self.mcp_server = MCPServerStdio(
            name="task-management-server",
            params={
                "command": "python",
                "args": ["-m", "mcp_server"],  # Run as module
                "env": os.environ.copy(),      # Pass environment
            },
            client_session_timeout_seconds=30.0,  # MCP ClientSession timeout
        )

        # Create agent
        # ModelSettings(parallel_tool_calls=False) prevents database lock issues
        self.agent = Agent(
            name="TodoAgent",
            model=self.model,
            instructions=AGENT_INSTRUCTIONS,  # See section 3.3
            mcp_servers=[self.mcp_server],
            model_settings=ModelSettings(
                parallel_tool_calls=False,  # Prevent concurrent DB writes
            ),
        )

    def get_agent(self) -> Agent:
        """Get configured agent instance."""
        return self.agent
```

**MCP Server Lifecycle**:

```python
# MCP server must be managed with async context manager
async with todo_agent.mcp_server:
    # Server is running, agent can call tools
    result = await Runner.run_streamed(
        agent=todo_agent.get_agent(),
        messages=[{"role": "user", "content": "Add buy milk"}]
    )
    # Process streaming results...
# Server stopped automatically
```

### 3.3 Agent Instructions

**Pattern**: Clear, behavioral instructions for conversational AI.

**Why**:
- Agent understands task domain and capabilities
- Handles natural language variations
- Provides friendly, helpful responses
- Never exposes technical details to users

**Phase III Agent Instructions (PRODUCTION-READY)**:

```python
# agent_config/todo_agent.py
AGENT_INSTRUCTIONS = """
You are a helpful task management assistant. Your role is to help users manage
their todo lists through natural conversation.

## Your Capabilities

You have access to these task management tools:
- add_task: Create new tasks with title, description, priority
- list_tasks: Show tasks (all, pending, or completed)
- complete_task: Mark a task as done
- delete_task: Remove a task permanently
- update_task: Modify task details

## Phase III Natural Language Behavior (CRITICAL)

### 1. Task Creation
**When user says:**
- "Add a task to buy groceries"
- "Remind me to call mom"
- "I need to remember to pay bills"
- "Create a task for the meeting"

**You should:**
→ Call `add_task` with extracted title
→ Detect priority from keywords:
  - "urgent", "critical", "important", "asap", "high" → priority="high"
  - "low", "minor", "optional", "when you have time" → priority="low"
  - Otherwise → priority="medium"
→ Respond: "I've added 'Buy groceries' to your tasks!"

**Example:**
User: "Add an urgent task to fix the bug"
→ add_task(user_id="...", title="Fix the bug", priority="high")
→ "I've added 'Fix the bug' to your tasks with high priority!"

### 2. Task Listing
**When user says:**
- "Show me all my tasks"
- "What's pending?"
- "List my completed tasks"
- "What do I need to do?"

**You should:**
→ Call `list_tasks` with appropriate status filter
→ status="pending" for "what's pending", "what do I need to do"
→ status="completed" for "what have I done", "completed tasks"
→ status="all" for "show all", "list everything"
→ Present tasks clearly and conversationally

**Example:**
User: "What's pending?"
→ list_tasks(user_id="...", status="pending")
→ "You have 3 pending tasks: Buy groceries, Call dentist, Pay bills"

### 3. Task Completion
**When user says:**
- "Mark task 3 as complete"
- "I finished buying groceries"
- "Task 5 is done"
- "Complete the meeting task"

**You should:**
→ If task ID provided: Call `complete_task` directly
→ If task name provided: Call `list_tasks` first to find ID, then `complete_task`
→ Respond with confirmation

**Example:**
User: "Mark task 3 as complete"
→ complete_task(user_id="...", task_id=3)
→ "Great! I've marked 'Call dentist' as complete!"

### 4. Task Deletion
**When user says:**
- "Delete task 2"
- "Remove the meeting task"
- "Cancel the dentist appointment"

**You should:**
→ If task ID provided: Call `delete_task` directly
→ If task name provided: Call `list_tasks` first to find ID, then `delete_task`
→ Respond with confirmation

**Example:**
User: "Delete task 2"
→ delete_task(user_id="...", task_id=2)
→ "I've deleted 'Old task' from your list."

### 5. Task Update
**When user says:**
- "Change task 1 to 'Call mom tonight'"
- "Update the meeting task description"
- "Rename task 5 to 'Buy groceries and fruits'"

**You should:**
→ Call `update_task` with appropriate parameters
→ Only update fields mentioned by user
→ Respond with confirmation

**Example:**
User: "Change task 1 to 'Call mom tonight'"
→ update_task(user_id="...", task_id=1, title="Call mom tonight")
→ "I've updated task 1 to 'Call mom tonight'."

## Conversational Style (CRITICAL)

**DO:**
✅ Be friendly, helpful, concise
✅ Use natural language, not technical jargon
✅ Acknowledge actions positively
✅ Extract clear, actionable titles from user messages
✅ Confirm destructive operations (delete, bulk updates)

**DON'T:**
❌ NEVER expose internal IDs or technical details
❌ NEVER return JSON or raw data structures
❌ NEVER use robotic language ("Status: created", "Operation successful")
❌ NEVER skip confirmation for task operations

## Handling Greetings and Social Interactions

**Greetings** (hi, hello, hey, good morning):
- ✅ Respond warmly: "Hello! I'm your task assistant. How can I help you today?"
- ✅ Ask what they need: "Hi there! Would you like to add a task, view your tasks, or something else?"

**Gratitude** (thanks, thank you, appreciate it):
- ✅ Respond positively: "You're welcome! Let me know if you need anything else."
- ✅ Offer continued help: "Happy to help! Anything else you'd like to do?"

**Irrelevant Requests** (weather, jokes, unrelated topics):
- ✅ Politely decline: "I'm sorry, I'm specialized in task management and can't help with that."
- ✅ Redirect: "I can help you manage your tasks though! Would you like to add, view, or complete any tasks?"

## Response Pattern Examples

**Good Responses:**
✅ "I've added 'Buy groceries' to your tasks!"
✅ "You have 3 pending tasks: Buy groceries, Call dentist, Pay bills"
✅ "Great! I've marked 'Call dentist' as complete!"
✅ "I've deleted 'Old task' from your list."
✅ "Hello! I'm your task assistant. How can I help you today?"
✅ "I'm sorry, I'm specialized in task management and can't help with that. Would you like to manage your tasks?"

**Bad Responses:**
❌ "Task created with ID 42. Status: created. Priority: medium."
❌ "Here's the JSON: [{\"id\": 1, \"title\": \"Buy groceries\"}]"
❌ "Operation completed successfully. Task ID: 3."
❌ "Database updated. Rows affected: 1."
❌ "Hi." (too short, not helpful)
❌ "I don't know about that." (not redirecting to task management)

## Error Handling

**When errors occur:**
- Task not found → "I couldn't find that task. Try listing your tasks first."
- Invalid input → "Could you clarify that? I didn't understand."
- Database error → "Sorry, something went wrong. Please try again."

**NEVER expose:**
- Stack traces
- Database errors
- Internal system details
- API error messages
"""
```

### 3.4 MCP Server with FastMCP (Modern Approach)

**Pattern**: MCP server exposes tools using FastMCP from Official MCP SDK.

**Why FastMCP**:
- Simpler API compared to low-level Server class
- Automatic stdio transport setup (no manual async context)
- Type-safe tool definitions with automatic schema generation
- Less boilerplate code (~80% reduction)
- Recommended approach for new projects (2024-2025)
- Better integration with OpenAI Agents SDK

**Installation**:

```bash
# Install Official MCP Python SDK (includes FastMCP)
uv add mcp

# Or with pip
pip install mcp
```

**Implementation (FastMCP from Official MCP SDK)**:

```python
# mcp_server/tools.py
"""
MCP Server for task management operations (Phase III).

This module implements an MCP server using FastMCP from official MCP SDK.
The server exposes task operations as MCP tools callable by AI agents.

Architecture:
- MCP Server runs as separate process (stdio transport)
- Agent connects via MCPServerStdio transport
- Tools use @mcp.tool() decorator (NOT @function_tool)
- Tools are stateless - all state in database
- FastMCP is part of official MCP Python SDK (mcp.server.fastmcp)
"""

from typing import Literal, Optional
from mcp.server.fastmcp import FastMCP
from sqlmodel import Session

# Import from Phase 2 structure (src.*)
from src.db import get_session
from src.services.task_service import TaskService

# Create FastMCP instance (part of official MCP Python SDK)
mcp = FastMCP("task-management-server")


@mcp.tool()
def add_task(
    user_id: str,
    title: str,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> dict:
    """
    Create a new task for a user.

    MCP Tool Contract:
    - Purpose: Add task to user's todo list
    - Stateless: All state persisted to database
    - User Isolation: Enforced via user_id parameter

    Args:
        user_id: User's unique identifier (string UUID from Better Auth)
        title: Task title (required, max 200 characters)
        description: Task description (optional, max 1000 characters)
        priority: Task priority level ("low", "medium", "high")

    Returns:
        dict: Task creation result
            - task_id (int): Created task ID
            - status (str): "created"
            - title (str): Task title
            - priority (str): Assigned priority level

    Example:
        >>> add_task(user_id="user-123", title="Buy groceries", priority="high")
        {"task_id": 42, "status": "created", "title": "Buy groceries", "priority": "high"}
    """
    session = next(get_session())
    try:
        # Validate priority
        if priority and priority.lower() not in ["low", "medium", "high"]:
            priority = "medium"
        elif not priority:
            priority = "medium"

        # Create task using TaskService
        task = TaskService.create_task(
            db=session,
            user_id=user_id,
            title=title,
            description=description,
            priority=priority.lower()
        )

        # Return MCP tool response (plain dict, not TextContent)
        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "priority": task.priority,
        }
    finally:
        session.close()


@mcp.tool()
def list_tasks(
    user_id: str,
    status: Literal["all", "pending", "completed"] = "all",
) -> dict:
    """
    Retrieve tasks from user's todo list.

    MCP Tool Contract:
    - Purpose: List tasks with optional status filtering
    - Stateless: Queries database on each invocation
    - User Isolation: Enforced via user_id parameter

    Args:
        user_id: User's unique identifier
        status: Filter by completion status (default: "all")
            - "all": All tasks
            - "pending": Incomplete tasks only
            - "completed": Completed tasks only

    Returns:
        dict: Task list result
            - tasks (list): Array of task objects
            - count (int): Total number of tasks returned

    Example:
        >>> list_tasks(user_id="user-123", status="pending")
        {"tasks": [...], "count": 2}
    """
    session = next(get_session())
    try:
        tasks = TaskService.get_tasks(
            db=session,
            user_id=user_id,
            status=status
        )

        # Convert tasks to dict format
        task_list = [
            {
                "id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed,
                "priority": task.priority,
                "created_at": task.created_at.isoformat(),
            }
            for task in tasks
        ]

        # Return MCP tool response
        return {
            "tasks": task_list,
            "count": len(task_list),
        }
    finally:
        session.close()


@mcp.tool()
def complete_task(
    user_id: str,
    task_id: int,
) -> dict:
    """
    Mark a task as complete.

    MCP Tool Contract:
    - Purpose: Toggle task completion status to completed
    - Stateless: Updates database and returns result
    - User Isolation: Enforced via user_id parameter

    Args:
        user_id: User's unique identifier
        task_id: Task ID to mark as complete

    Returns:
        dict: Task completion result
            - task_id (int): Updated task ID
            - status (str): "completed"
            - title (str): Task title

    Example:
        >>> complete_task(user_id="user-123", task_id=3)
        {"task_id": 3, "status": "completed", "title": "Call dentist"}
    """
    session = next(get_session())
    try:
        # Mark task as complete
        updated_task = TaskService.toggle_complete(
            db=session,
            user_id=user_id,
            task_id=task_id,
            completed=True
        )

        return {
            "task_id": updated_task.id,
            "status": "completed",
            "title": updated_task.title,
        }
    finally:
        session.close()


@mcp.tool()
def delete_task(
    user_id: str,
    task_id: int,
) -> dict:
    """
    Remove a task from the list.

    MCP Tool Contract:
    - Purpose: Permanently delete a task
    - Stateless: Removes from database
    - User Isolation: Enforced via user_id parameter

    Args:
        user_id: User's unique identifier
        task_id: Task ID to delete

    Returns:
        dict: Task deletion result
            - task_id (int): Deleted task ID
            - status (str): "deleted"
            - title (str): Task title

    Example:
        >>> delete_task(user_id="user-123", task_id=2)
        {"task_id": 2, "status": "deleted", "title": "Old task"}
    """
    session = next(get_session())
    try:
        # Get task before deleting (to return title)
        task = TaskService.get_task_by_id(
            db=session,
            user_id=user_id,
            task_id=task_id
        )

        # Delete task
        TaskService.delete_task(
            db=session,
            user_id=user_id,
            task_id=task_id
        )

        return {
            "task_id": task.id,
            "status": "deleted",
            "title": task.title,
        }
    finally:
        session.close()


@mcp.tool()
def update_task(
    user_id: str,
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None,
    priority: Optional[str] = None,
) -> dict:
    """
    Modify task title, description, or priority.

    MCP Tool Contract:
    - Purpose: Update task details
    - Stateless: Updates database and returns result
    - User Isolation: Enforced via user_id parameter

    Args:
        user_id: User's unique identifier
        task_id: Task ID to update
        title: New task title (optional)
        description: New task description (optional)
        priority: New task priority (optional: "low", "medium", "high")

    Returns:
        dict: Task update result
            - task_id (int): Updated task ID
            - status (str): "updated"
            - title (str): Task title

    Example:
        >>> update_task(user_id="user-123", task_id=1, title="Buy groceries and fruits")
        {"task_id": 1, "status": "updated", "title": "Buy groceries and fruits"}
    """
    session = next(get_session())
    try:
        # Validate priority if provided
        if priority and priority.lower() not in ["low", "medium", "high"]:
            priority = "medium"

        # Update task
        updated_task = TaskService.update_task(
            db=session,
            user_id=user_id,
            task_id=task_id,
            title=title,
            description=description,
            priority=priority.lower() if priority else None
        )

        return {
            "task_id": updated_task.id,
            "status": "updated",
            "title": updated_task.title,
        }
    finally:
        session.close()
```

**Module Structure**:

```python
# mcp_server/__init__.py
"""MCP server exposing task management tools."""

# mcp_server/__main__.py
"""Entry point for MCP server when run as module: python -m mcp_server"""
from mcp_server.tools import mcp

if __name__ == "__main__":
    # FastMCP handles stdio transport automatically
    mcp.run()
```

**Key Differences: Old (Server) vs New (FastMCP)**:

| Aspect | Old (mcp.server.Server) | New (FastMCP) |
|--------|------------------------|---------------|
| Import | `from mcp.server import Server` | `from fastmcp import FastMCP` |
| Initialization | `app = Server("name")` | `mcp = FastMCP("name")` |
| Tool decorator | `@app.call_tool()` | `@mcp.tool()` |
| Return type | `list[types.TextContent]` | Plain Python types (dict, str, int) |
| Run server | Manual `stdio_server()` context | `mcp.run()` (automatic) |
| Async main | Required (~15 lines) | Not required |
| Boilerplate | ~20 lines | ~3 lines |
| Type safety | Manual TextContent wrapping | Automatic serialization |

**Agent Connection Pattern**:

```python
# agent_config/todo_agent.py
from agents import Agent
from agents.mcp import MCPServerStdio
from agent_config.factory import create_model

class TodoAgent:
    """AI agent for conversational task management."""

    def __init__(self, provider: str | None = None):
        """Initialize agent with model and MCP server."""
        # Create model from factory
        self.model = create_model(provider=provider)

        # Create MCP server connection via stdio
        # CRITICAL: Set client_session_timeout_seconds for database operations
        self.mcp_server = MCPServerStdio(
            name="task-management-server",
            params={
                "command": "python",
                "args": ["-m", "mcp_server"],  # Run as module
                "env": os.environ.copy(),
            },
            client_session_timeout_seconds=30.0,  # Increase from default 5s
        )

        # Create agent with MCP server
        self.agent = Agent(
            name="TodoAgent",
            model=self.model,
            instructions=AGENT_INSTRUCTIONS,
            mcp_servers=[self.mcp_server],
        )

    def get_agent(self) -> Agent:
        """Get configured agent instance."""
        return self.agent


# Usage in FastAPI endpoint
async with todo_agent.mcp_server:
    result = Runner.run_streamed(
        agent=todo_agent.get_agent(),
        messages=history,
        context_variables={"user_id": str(user_id)}
    )
```

### 3.5 Database Persistence (Conversations)

**Pattern**: Store conversation history in database for stateless backend.

**Why**:
- Stateless backend (no in-memory state)
- Users can resume conversations
- Full conversation history available
- Multi-device support

**Models**:

```python
# models.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4

class Conversation(SQLModel, table=True):
    """
    Conversation session between user and AI agent.
    """
    __tablename__ = "conversations"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    messages: list["Message"] = Relationship(back_populates="conversation")
    user: "User" = Relationship(back_populates="conversations")

class Message(SQLModel, table=True):
    """
    Individual message in a conversation.
    """
    __tablename__ = "messages"

    id: UUID = Field(default_factory=uuid4, primary_key=True)
    conversation_id: UUID = Field(foreign_key="conversations.id", index=True)
    user_id: UUID = Field(foreign_key="users.id", index=True)
    role: str = Field(index=True)  # "user" | "assistant" | "system"
    content: str
    tool_calls: str | None = None  # JSON string of tool calls
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationships
    conversation: Conversation = Relationship(back_populates="messages")
    user: "User" = Relationship()
```

**Service Layer**:

```python
# services/conversation_service.py
from uuid import UUID
from sqlmodel import Session, select
from models import Conversation, Message

class ConversationService:
    @staticmethod
    async def get_or_create_conversation(
        session: Session,
        user_id: UUID,
        conversation_id: UUID | None = None
    ) -> Conversation:
        """Get existing conversation or create new one."""
        if conversation_id:
            stmt = select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id
            )
            conversation = session.exec(stmt).first()
            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        session.commit()
        session.refresh(conversation)
        return conversation

    @staticmethod
    async def add_message(
        session: Session,
        conversation_id: UUID,
        user_id: UUID,
        role: str,
        content: str,
        tool_calls: str | None = None
    ) -> Message:
        """Add message to conversation."""
        message = Message(
            conversation_id=conversation_id,
            user_id=user_id,
            role=role,
            content=content,
            tool_calls=tool_calls
        )
        session.add(message)
        session.commit()
        session.refresh(message)
        return message

    @staticmethod
    async def get_conversation_history(
        session: Session,
        conversation_id: UUID,
        user_id: UUID
    ) -> list[dict]:
        """Get conversation messages formatted for agent."""
        stmt = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.user_id == user_id
        ).order_by(Message.created_at)

        messages = session.exec(stmt).all()

        return [
            {
                "role": msg.role,
                "content": msg.content
            }
            for msg in messages
        ]
```

### 3.6 FastAPI Streaming Endpoint

**Pattern**: SSE endpoint for streaming agent responses.

**Why**:
- Real-time streaming improves UX
- Works with ChatKit frontend
- Server-Sent Events (SSE) standard protocol
- Handles long-running agent calls

**Implementation**:

```python
# routers/chat.py
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session
from uuid import UUID
from db import get_session
from agent_config.todo_agent import TodoAgent
from services.conversation_service import ConversationService
from schemas.chat import ChatRequest
from agents import Runner

router = APIRouter()

@router.post("/{user_id}/chat")
async def chat(
    user_id: UUID,
    request: ChatRequest,
    session: Session = Depends(get_session)
):
    """
    Chat endpoint with streaming SSE response.

    Args:
        user_id: User's unique identifier
        request: ChatRequest with conversation_id and message
        session: Database session

    Returns:
        StreamingResponse with SSE events
    """
    # Get or create conversation
    conversation = await ConversationService.get_or_create_conversation(
        session=session,
        user_id=user_id,
        conversation_id=request.conversation_id
    )

    # Save user message
    await ConversationService.add_message(
        session=session,
        conversation_id=conversation.id,
        user_id=user_id,
        role="user",
        content=request.message
    )

    # Get conversation history
    history = await ConversationService.get_conversation_history(
        session=session,
        conversation_id=conversation.id,
        user_id=user_id
    )

    # Create agent
    todo_agent = TodoAgent()
    agent = todo_agent.get_agent()

    # Stream response
    async def event_generator():
        try:
            async with todo_agent.mcp_server:
                response_chunks = []

                async for chunk in Runner.run_streamed(
                    agent=agent,
                    messages=history,
                    context_variables={"user_id": str(user_id)}
                ):
                    # Handle different chunk types
                    if hasattr(chunk, 'delta') and chunk.delta:
                        response_chunks.append(chunk.delta)
                        yield f"data: {chunk.delta}\n\n"

                # Save assistant response
                full_response = "".join(response_chunks)
                await ConversationService.add_message(
                    session=session,
                    conversation_id=conversation.id,
                    user_id=user_id,
                    role="assistant",
                    content=full_response
                )

                yield "data: [DONE]\n\n"

        except Exception as e:
            yield f"data: Error: {str(e)}\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )
```

## 4. Common Patterns

### 4.1 Error Handling

```python
# Handle provider API failures gracefully
try:
    async with todo_agent.mcp_server:
        result = await Runner.run_streamed(agent, messages)
except Exception as e:
    # Log error
    logger.error(f"Agent execution failed: {e}")
    # Return user-friendly message
    return {"error": "AI service temporarily unavailable. Please try again."}
```

### 4.2 Timeout Configuration

```python
# CRITICAL: Increase MCP timeout for database operations
# Default 5s is too short - may cause timeouts
MCPServerStdio(
    name="server",
    params={...},
    client_session_timeout_seconds=30.0,  # Increase from default 5s
)
```

### 4.3 Parallel Tool Calls Prevention

```python
# Prevent concurrent database writes (causes locks)
Agent(
    name="MyAgent",
    model=model,
    instructions=instructions,
    mcp_servers=[mcp_server],
    model_settings=ModelSettings(
        parallel_tool_calls=False,  # Serialize tool calls
    ),
)
```

## 5. Phase 3 Critical Components (Async Database + Production Patterns)

### 5.1 Async Database Setup for Chat Endpoint

**Why Needed**: Chat endpoints MUST use async database for non-blocking operations with ConversationService.

**Phase 2 has SYNC sessions** (which works fine for REST endpoints):
```python
# phase-2-todo full-stack-web/backend/src/db/session.py
def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session
```

**Phase 3 needs BOTH** (keep Phase 2 sync + add Phase 3 async):

**Installation**:
```bash
# Add async PostgreSQL driver
uv add asyncpg
```

**Create new file**: `src/db/async_session.py`
```python
"""
Async database session for Phase 3 chat endpoint.

This module provides AsyncSession for non-blocking database operations
required by ConversationService and chat endpoint.

IMPORTANT: Phase 2 sync sessions remain unchanged - this is ADDITIVE.
"""

from typing import AsyncIterator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import os

# Get database URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable is required")

# Convert sync URL to async: postgresql:// → postgresql+asyncpg://
# Phase 2 uses: postgresql://user:pass@host/db
# Phase 3 needs: postgresql+asyncpg://user:pass@host/db
async_database_url = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")

# Create async engine (verified with Context7: SQLAlchemy docs)
async_engine = create_async_engine(
    async_database_url,
    echo=False,
    pool_size=5,
    max_overflow=10,
    pool_pre_ping=True,
)

# Create async session factory (verified with Context7: SQLAlchemy docs)
AsyncSessionLocal = sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncIterator[AsyncSession]:
    """
    FastAPI dependency for async database sessions.

    Use this ONLY for Phase 3 chat endpoints.
    Phase 2 REST endpoints continue using get_session().

    Example:
        @router.post("/{user_id}/chat")
        async def chat_endpoint(
            session: AsyncSession = Depends(get_async_session)
        ):
            conversation = await get_or_create_conversation(session, ...)
    """
    async with AsyncSessionLocal() as session:
        yield session
```

**Add to**: `src/db/__init__.py`
```python
from .session import get_session, engine
from .async_session import get_async_session, async_engine  # Phase 3

__all__ = ["get_session", "engine", "get_async_session", "async_engine"]
```

---

### 5.2 Conversation & Message Models (Phase 3)

**Create new file**: `src/models/conversation.py`
```python
"""
Conversation model for AI chatbot Phase III.

Stores conversation metadata for multi-turn chat sessions.
"""

from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Conversation(SQLModel, table=True):
    """
    Conversation session between user and AI agent.

    Attributes:
        id: Auto-increment primary key (NOT UUID - matches Phase 2 pattern)
        user_id: User identifier from JWT (str - matches Phase 2 Task.user_id)
        title: Auto-generated conversation title
        is_active: Whether conversation is still active
        created_at: Conversation start time
        updated_at: Last message timestamp
    """
    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)  # Matches Phase 2 Task.user_id type
    title: str = Field(max_length=500, nullable=False)
    is_active: bool = Field(default=True, nullable=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False, index=True)
```

**Create new file**: `src/models/message.py`
```python
"""
Message model for conversation history.

Stores individual messages with 2-day retention policy.
"""

from sqlmodel import SQLModel, Field, Column
from sqlalchemy import JSON
from datetime import datetime, timedelta
from typing import Optional

class Message(SQLModel, table=True):
    """
    Individual message in a conversation.

    Attributes:
        id: Auto-increment primary key
        conversation_id: Foreign key to conversations.id
        user_id: User identifier (denormalized for queries)
        role: Message sender ("user" | "assistant" | "system")
        content: Message text content
        tool_calls: JSON of tool invocations (for debugging)
        created_at: Message timestamp
        expires_at: Auto-set to 2 days from creation
    """
    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True, nullable=False)
    user_id: str = Field(index=True, nullable=False)
    role: str = Field(nullable=False)
    content: str = Field(nullable=False)
    tool_calls: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True, nullable=False)
    expires_at: datetime = Field(
        default_factory=lambda: datetime.utcnow() + timedelta(days=2),
        nullable=False,
        index=True,
    )
```

**Update**: `src/models/__init__.py`
```python
from .task import Task
from .tag import Tag
from .task_tag import TaskTag
from .conversation import Conversation  # Phase 3
from .message import Message  # Phase 3

__all__ = ["Task", "Tag", "TaskTag", "Conversation", "Message"]
```

**Alembic Migration**:
```bash
# Generate migration for new tables
uv run alembic revision --autogenerate -m "Add conversation and message tables for Phase 3"

# Apply migration
uv run alembic upgrade head
```

---

### 5.3 Async Conversation Service (Phase 3)

**Create new file**: `src/services/conversation_service.py`
```python
"""
Conversation service for AI chatbot Phase III.

All methods are ASYNC and use AsyncSession.
Provides conversation and message management with user isolation.
"""

from typing import Optional, List
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from datetime import datetime
from fastapi import HTTPException, status

from ..models.conversation import Conversation
from ..models.message import Message


async def get_or_create_conversation(
    session: AsyncSession,
    user_id: str,
    conversation_id: Optional[int] = None
) -> Conversation:
    """
    Get existing conversation or create new one.

    Args:
        session: Async database session
        user_id: User ID from JWT (matches Phase 2 user_id type)
        conversation_id: Optional existing conversation ID

    Returns:
        Conversation object

    Raises:
        HTTPException: 404 if conversation not found, 403 if wrong user
    """
    if conversation_id is not None:
        # Fetch existing conversation with user isolation
        result = await session.execute(
            select(Conversation).where(
                Conversation.id == conversation_id,
                Conversation.user_id == user_id  # User isolation
            )
        )
        conversation = result.scalar_one_or_none()

        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Conversation {conversation_id} not found or access denied"
            )

        # Update timestamp
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
        return conversation
    else:
        # Create new conversation with auto-generated title
        now = datetime.utcnow()
        title = f"Conversation {now.strftime('%Y-%m-%d %H:%M')}"

        new_conversation = Conversation(
            user_id=user_id,
            title=title,
            is_active=True,
            created_at=now,
            updated_at=now
        )
        session.add(new_conversation)
        await session.commit()
        await session.refresh(new_conversation)
        return new_conversation


async def add_message(
    session: AsyncSession,
    user_id: str,
    conversation_id: int,
    role: str,
    content: str,
    tool_calls: Optional[dict] = None
) -> Message:
    """
    Add message to conversation.

    Args:
        session: Async database session
        user_id: User ID from JWT
        conversation_id: Target conversation ID
        role: Message role ("user" | "assistant" | "system")
        content: Message text content
        tool_calls: Optional tool invocations (for debugging)

    Returns:
        Message object

    Example:
        message = await add_message(
            session=session,
            user_id="user-123",
            conversation_id=1,
            role="user",
            content="Add task to buy groceries"
        )
    """
    message = Message(
        conversation_id=conversation_id,
        user_id=user_id,
        role=role,
        content=content,
        tool_calls=tool_calls
    )
    session.add(message)

    # Update conversation timestamp
    result = await session.execute(
        select(Conversation).where(Conversation.id == conversation_id)
    )
    conversation = result.scalar_one_or_none()
    if conversation:
        conversation.updated_at = datetime.utcnow()
        session.add(conversation)

    await session.commit()
    await session.refresh(message)
    return message


async def get_conversation_history(
    session: AsyncSession,
    conversation_id: int,
    user_id: str,
    limit: Optional[int] = None
) -> List[dict]:
    """
    Get conversation messages formatted for agent.

    Args:
        session: Async database session
        conversation_id: Conversation ID
        user_id: User ID from JWT (for user isolation)
        limit: Optional max messages to return

    Returns:
        List of message dicts: [{"role": "user", "content": "..."}, ...]

    Example:
        history = await get_conversation_history(
            session=session,
            conversation_id=1,
            user_id="user-123",
            limit=50
        )
    """
    stmt = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id  # User isolation
    ).order_by(Message.created_at)

    if limit:
        stmt = stmt.limit(limit)

    result = await session.execute(stmt)
    messages = result.scalars().all()

    return [
        {
            "role": msg.role,
            "content": msg.content
        }
        for msg in messages
    ]
```

---

### 5.4 JWT Integration with Chat Endpoint (Phase 2 Pattern)

**Pattern**: Use Phase 2's existing `get_current_user_id` dependency.

**Create**: `src/api/v1/chat.py`
```python
"""
Chat API endpoint for Phase 3 AI chatbot.

Integrates with Phase 2 JWT authentication and database.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from sqlmodel.ext.asyncio.session import AsyncSession
from pydantic import BaseModel, Field
from typing import Optional

# Phase 2 imports (existing)
from ...db.async_session import get_async_session
from ...auth.dependencies import get_current_user_id  # Phase 2 JWT dependency

# Phase 3 imports (new)
from ...services import conversation_service
from agent_config.todo_agent import create_todo_agent
from agents import Runner

router = APIRouter(prefix="/api", tags=["chat"])


class ChatRequest(BaseModel):
    """Chat request schema."""
    conversation_id: Optional[int] = Field(default=None)
    message: str = Field(min_length=1, max_length=5000)


@router.post("/{user_id}/chat")
async def chat_with_agent(
    user_id: str,
    request: ChatRequest,
    current_user_id: str = Depends(get_current_user_id),  # Phase 2 JWT
    session: AsyncSession = Depends(get_async_session)  # Phase 3 async
):
    """
    Chat endpoint with SSE streaming.

    Security:
    - Uses Phase 2 JWT authentication
    - Validates user_id matches JWT (Phase 2 pattern)
    - All database queries filter by user_id

    Args:
        user_id: User ID from URL path
        request: Chat request with optional conversation_id and message
        current_user_id: User ID from JWT (Phase 2 dependency)
        session: Async database session (Phase 3)

    Returns:
        StreamingResponse with SSE events
    """
    # Phase 2 user isolation pattern
    if user_id != current_user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to access this resource"
        )

    try:
        # Get or create conversation
        conversation = await conversation_service.get_or_create_conversation(
            session=session,
            user_id=user_id,
            conversation_id=request.conversation_id
        )

        # Get conversation history
        history = await conversation_service.get_conversation_history(
            session=session,
            conversation_id=conversation.id,
            user_id=user_id,
            limit=50
        )

        # Add user message to history
        agent_messages = history + [{"role": "user", "content": request.message}]

        # Save user message
        await conversation_service.add_message(
            session=session,
            user_id=user_id,
            conversation_id=conversation.id,
            role="user",
            content=request.message
        )

        # Create agent
        todo_agent = create_todo_agent()
        agent = todo_agent.get_agent()

        # Stream response
        async def event_generator():
            try:
                async with todo_agent.mcp_server:
                    response_chunks = []

                    async for chunk in Runner.run_streamed(
                        agent=agent,
                        messages=agent_messages,
                        context_variables={"user_id": user_id}  # Pass to MCP tools
                    ):
                        if hasattr(chunk, 'delta') and chunk.delta:
                            response_chunks.append(chunk.delta)
                            yield f"data: {chunk.delta}\n\n"

                    # Save assistant response
                    full_response = "".join(response_chunks)
                    await conversation_service.add_message(
                        session=session,
                        user_id=user_id,
                        conversation_id=conversation.id,
                        role="assistant",
                        content=full_response
                    )

                    yield "data: [DONE]\n\n"

            except Exception as e:
                yield f"data: Error: {str(e)}\n\n"

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Chat request failed: {str(e)}"
        )
```

---

### 5.5 Retry Logic with Exponential Backoff

**Pattern**: Handle OpenAI API failures gracefully (verified with Context7: OpenAI Python SDK docs).

**Add to**: `src/api/v1/chat.py` (above chat_with_agent function)
```python
"""
Retry logic for LLM API calls.

Handles transient errors from OpenAI/Gemini/Groq/OpenRouter.
"""

import asyncio
from openai import (
    RateLimitError,
    APIConnectionError,
    APITimeoutError,
    APIError,
)

# Retry configuration
MAX_RETRIES = 3
INITIAL_RETRY_DELAY = 1.0  # seconds
MAX_RETRY_DELAY = 10.0  # seconds


async def run_agent_with_retry(agent, agent_messages: list, context_variables: dict, max_retries: int = MAX_RETRIES):
    """
    Run agent with exponential backoff retry logic.

    Handles (verified with Context7: OpenAI Python SDK docs):
    - RateLimitError (429) → Retry with backoff
    - APIConnectionError → Retry with backoff
    - APITimeoutError → Retry with backoff

    Args:
        agent: Configured Agent instance
        agent_messages: List of message dicts
        context_variables: Context for MCP tools (e.g., {"user_id": "..."})
        max_retries: Maximum retry attempts (default: 3)

    Returns:
        AsyncIterator: Agent streaming result

    Raises:
        HTTPException: User-friendly error after retries exhausted
    """
    for attempt in range(max_retries):
        try:
            return Runner.run_streamed(
                agent=agent,
                messages=agent_messages,
                context_variables=context_variables
            )

        except RateLimitError as e:
            if attempt < max_retries - 1:
                retry_delay = min(INITIAL_RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                await asyncio.sleep(retry_delay)
                continue
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="AI service rate limit exceeded. Please try again in a moment."
                )

        except (APIConnectionError, APITimeoutError) as e:
            if attempt < max_retries - 1:
                retry_delay = min(INITIAL_RETRY_DELAY * (2 ** attempt), MAX_RETRY_DELAY)
                await asyncio.sleep(retry_delay)
                continue
            else:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Unable to connect to AI service. Please try again."
                )

        except APIError as e:
            # Non-retryable API error (401, 403, invalid API key, etc.)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="AI service error. Please contact support."
            )
```

**Usage in chat_with_agent**:
```python
# Replace this line:
async for chunk in Runner.run_streamed(agent, agent_messages, context_variables={"user_id": user_id}):

# With retry wrapper:
stream = await run_agent_with_retry(agent, agent_messages, {"user_id": user_id})
async for chunk in stream:
```

---

### 5.6 Message Cleanup Task (2-Day Retention)

**Create new file**: `src/tasks/message_cleanup.py`
```python
"""
Background task for message cleanup (Phase 3).

Deletes messages older than 2 days per retention policy.
Run this daily via cron or scheduler.
"""

from sqlmodel import Session, select
from datetime import datetime
import logging

from ..db.session import engine  # Use Phase 2 sync engine for background task
from ..models.message import Message

logger = logging.getLogger(__name__)


def cleanup_expired_messages() -> dict:
    """
    Delete messages where expires_at < now().

    This is a SYNC function (not async) for background job compatibility.
    Uses Phase 2's sync engine for simplicity.

    Returns:
        dict: {"success": bool, "deleted_count": int, "timestamp": str}

    Usage:
        # Run daily via cron:
        # 0 2 * * * cd /app && uv run python -c "from src.tasks.message_cleanup import cleanup_expired_messages; cleanup_expired_messages()"
    """
    with Session(engine) as session:
        try:
            now = datetime.utcnow()

            # Query expired messages
            statement = select(Message).where(Message.expires_at < now)
            expired_messages = session.exec(statement).all()

            deleted_count = len(expired_messages)

            if deleted_count > 0:
                for message in expired_messages:
                    session.delete(message)
                session.commit()
                logger.info(f"Deleted {deleted_count} expired messages at {now.isoformat()}")
            else:
                logger.debug(f"No expired messages found at {now.isoformat()}")

            return {
                "success": True,
                "deleted_count": deleted_count,
                "timestamp": now.isoformat(),
            }

        except Exception as e:
            logger.error(f"Message cleanup failed: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e),
                "timestamp": datetime.utcnow().isoformat(),
            }
```

**Optional: Add cleanup endpoint** (for manual trigger):
```python
# src/api/v1/chat.py
@router.post("/admin/cleanup/messages")
async def trigger_message_cleanup():
    """Trigger message cleanup manually (admin only)."""
    from ...tasks.message_cleanup import cleanup_expired_messages
    result = cleanup_expired_messages()
    return result
```

**Scheduling options**:
```bash
# Option 1: Cron job (recommended for production)
# Add to crontab: Run daily at 2 AM
0 2 * * * cd /app && uv run python -c "from src.tasks.message_cleanup import cleanup_expired_messages; cleanup_expired_messages()"

# Option 2: APScheduler (if you prefer in-process scheduler)
# uv add apscheduler
```

---

## 6. Testing

### 6.1 Unit Tests (Model Factory)

```python
# tests/test_factory.py
import pytest
from agent_config.factory import create_model

def test_create_model_openai(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.setenv("OPENAI_API_KEY", "sk-test")

    model = create_model()
    assert model is not None

def test_create_model_missing_key(monkeypatch):
    monkeypatch.setenv("LLM_PROVIDER", "openai")
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)

    with pytest.raises(ValueError, match="OPENAI_API_KEY required"):
        create_model()
```

### 6.2 Integration Tests (MCP Tools)

```python
# tests/test_mcp_tools.py
import pytest
from mcp_server.tools import add_task

def test_add_task(test_session, test_user):
    """Test MCP tool - FastMCP tools are SYNC functions"""
    result = add_task(
        user_id=test_user.id,  # Phase 2 uses str user_id
        title="Test task",
        description="Test description",
        priority="High"
    )

    assert result["task_id"] is not None
    assert result["title"] == "Test task"
    assert result["priority"] == "High"
```

### 6.3 Async Conversation Service Tests

```python
# tests/test_conversation_service.py
import pytest
from src.services.conversation_service import (
    get_or_create_conversation,
    add_message,
    get_conversation_history
)

@pytest.mark.asyncio
async def test_create_conversation(async_session, test_user_id):
    """Test conversation creation"""
    conversation = await get_or_create_conversation(
        session=async_session,
        user_id=test_user_id,
        conversation_id=None
    )

    assert conversation.id is not None
    assert conversation.user_id == test_user_id
    assert conversation.title.startswith("Conversation")


@pytest.mark.asyncio
async def test_add_message(async_session, test_user_id, test_conversation_id):
    """Test message creation"""
    message = await add_message(
        session=async_session,
        user_id=test_user_id,
        conversation_id=test_conversation_id,
        role="user",
        content="Test message"
    )

    assert message.id is not None
    assert message.content == "Test message"
    assert message.role == "user"
```

---

## 7. Production Checklist

### Phase 2 Requirements (Existing):
- [ ] Validate JWT tokens on all endpoints
- [ ] Configure CORS for production domains
- [ ] Use database connection pooling
- [ ] Sanitize user inputs

### Phase 3 Requirements (NEW):
- [ ] ✅ Install asyncpg: `uv add asyncpg`
- [ ] ✅ Create async_session.py with AsyncSession
- [ ] ✅ Add Conversation & Message models
- [ ] ✅ Generate Alembic migration for new tables
- [ ] ✅ Create async conversation_service.py
- [ ] ✅ Create chat.py endpoint with JWT integration
- [ ] ✅ Add retry logic with exponential backoff
- [ ] ✅ Create message_cleanup.py task
- [ ] ✅ Set up daily cron job for message cleanup
- [ ] Set appropriate MCP timeout (30s+)
- [ ] Disable parallel tool calls: `parallel_tool_calls=False`
- [ ] Add rate limiting to chat endpoints
- [ ] Monitor MCP server process health
- [ ] Log agent interactions for debugging
- [ ] Set up alerts for high error rates
- [ ] Add MCP dependencies: `uv add mcp openai-agents`
- [ ] Update main.py to include chat router
- [ ] Test chat endpoint with SSE streaming
- [ ] Verify message expiry works (2-day retention)
- [ ] Test retry logic with mock API failures

## 8. Phase 3 Dependencies

**Add to**: `pyproject.toml`
```toml
dependencies = [
    # ... existing Phase 2 dependencies ...

    # Phase 3 AI Chatbot Dependencies
    "mcp>=1.0.0",              # Official MCP Python SDK (includes FastMCP)
    "openai-agents>=0.2.9",    # OpenAI Agents SDK
    "asyncpg>=0.31.0",         # Async PostgreSQL driver
    "openai>=1.0.0",           # OpenAI Python SDK (for error types)
]
```

**Installation**:
```bash
cd backend
uv add mcp openai-agents asyncpg openai
```

---

## 9. Integration with Phase 2

### 9.1 Update main.py

**Add chat router** to existing Phase 2 main.py:
```python
# src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Phase 2 routers (existing)
from .api.v1.tasks import router as tasks_router

# Phase 3 router (new)
from .api.v1.chat import router as chat_router

app = FastAPI(title="Todo API")

# CORS (Phase 2)
app.add_middleware(CORSMiddleware, ...)

# Phase 2 routes (existing)
app.include_router(tasks_router)

# Phase 3 routes (new)
app.include_router(chat_router)
```

### 9.2 Coexistence Pattern

**Phase 2 endpoints** (keep using sync):
```python
# src/api/v1/tasks.py
async def create_task(
    session: Session = Depends(get_session)  # Sync session - KEEP AS IS
):
    task = TaskService.create_task(session, ...)  # Sync service - KEEP AS IS
```

**Phase 3 endpoints** (use async):
```python
# src/api/v1/chat.py
async def chat_with_agent(
    session: AsyncSession = Depends(get_async_session)  # Async session - NEW
):
    conversation = await get_or_create_conversation(session, ...)  # Async service - NEW
```

**Both work together** - no conflicts!

---

## 10. References

- **OpenAI Agents SDK**: https://github.com/openai/agents
- **Official MCP Python SDK**: https://github.com/modelcontextprotocol/python-sdk
- **FastMCP Documentation**: https://github.com/modelcontextprotocol/python-sdk#fastmcp
- **SQLAlchemy Async**: https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **FastAPI SSE**: https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse
- **SQLModel**: https://sqlmodel.tiangolo.com/
- **Better Auth**: https://better-auth.com/
- **asyncpg**: https://magicstack.github.io/asyncpg/

---

**Last Updated**: December 2024
**Skill Version**: 2.0.0 (Phase 3 Complete)
**OpenAI Agents SDK**: v0.2.9+
**Official MCP SDK**: v1.0.0+ (includes FastMCP)
**SQLAlchemy**: v2.0+ (async support)
