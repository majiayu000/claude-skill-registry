---
name: openai-agents-sdk-skill
description: Expert skill for implementing OpenAI Agents SDK with function tools, MCP server integration, and context management for building intelligent AI assistants.
---

# OpenAI Agents SDK Skill

Use this skill when implementing AI assistants using the OpenAI Agents SDK with function tools, MCP server integration, and context management.

## When to Use

- Creating AI agents with function tools and structured outputs
- Integrating Model Context Protocol (MCP) servers
- Managing conversational history and context
- Building tool-enabled AI assistants
- Implementing dynamic tool filtering and security

## Core Components

### 1. Agent Creation with OpenRouter
```python
# app/agents/todo_agent.py
import os
from agents import Agent, Runner
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from pydantic import BaseModel, Field
from typing import Annotated
import asyncio

class TodoAgent:
    """AI agent for managing todo tasks with OpenAI Agents SDK using OpenRouter."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        
        # Setup OpenRouter client using specific configuration
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        openrouter_model = os.getenv("OPENROUTER_MODEL", "mistralai/devstral-2512:free")
        
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is not set in environment variables")
        
        external_client = AsyncOpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url,
        )

        # Define the model to use (using available OpenRouter models)
        model = OpenAIChatCompletionsModel(
            model=openrouter_model,  # Using mistralai/devstral-2512:free as specified
            openai_client=external_client
        )

        # Create run configuration with OpenRouter
        self.config = RunConfig(
            model=model,
            model_provider=external_client,
            # Add other configuration as needed
        )

        # Create the agent with tools
        self.agent = Agent(
            name="Todo Assistant",
            instructions="You are a helpful assistant for managing todo tasks. Use available tools to add, list, complete, update, and delete tasks.",
            tools=self.get_tools()
        )

    def get_tools(self):
        """Define and return agent tools."""
        return [
            self.add_task_tool,
            self.list_tasks_tool,
            self.complete_task_tool,
            self.update_task_tool,
            self.delete_task_tool
        ]

    async def run(self, message: str):
        """Run the agent with user message using OpenRouter configuration."""
        return await Runner.run(
            self.agent,
            message,
            config=self.config
        )
```

### 2. Function Tools with Pydantic Models
```python
# app/agents/tools.py
from agents import function_tool
from pydantic import BaseModel, Field
from typing import Annotated, Optional
import asyncio

# Define structured output models
class Task(BaseModel):
    id: int = Field(description="Unique task identifier")
    title: str = Field(description="Task title")
    description: Optional[str] = Field(description="Task description")
    completed: bool = Field(description="Whether task is completed")
    priority: str = Field(description="Task priority: low, medium, high")

class AddTaskParams(BaseModel):
    title: str = Field(description="Task title")
    description: Optional[str] = Field(description="Task description")
    priority: str = Field(description="Task priority: low, medium, high")

# Create function tools with decorators
@function_tool
def add_task(params: AddTaskParams) -> Task:
    """Add a new task to the user's list."""
    # In production, this would call your task service
    return Task(
        id=123,
        title=params.title,
        description=params.description,
        completed=False,
        priority=params.priority or "medium"
    )

@function_tool
def list_tasks(
    status: Optional[str] = "all",
    priority: Optional[str] = None
) -> list[Task]:
    """List user's tasks with optional filtering."""
    # In production, this would fetch from your database
    return [
        Task(id=1, title="Buy groceries", completed=False, priority="medium"),
        Task(id=2, title="Call doctor", completed=True, priority="high")
    ]

@function_tool
def complete_task(task_id: int) -> Task:
    """Mark a task as completed."""
    # In production, this would update your database
    return Task(
        id=task_id,
        title="Sample task",
        completed=True,
        priority="medium"
    )

@function_tool
def update_task(
    task_id: int,
    title: Optional[str] = None,
    description: Optional[str] = None
) -> Task:
    """Update an existing task."""
    # In production, this would update your database
    return Task(
        id=task_id,
        title=title or f"Updated task {task_id}",
        description=description,
        completed=False,
        priority="medium"
    )

@function_tool
def delete_task(task_id: int) -> dict:
    """Delete a task by ID."""
    # In production, this would delete from your database
    return {"success": True, "deleted_task_id": task_id}
```

### 3. MCP Server Integration
```python
# app/agents/mcp_integration.py
from agents.mcp import MCPServerStdio
from agents import Agent
import asyncio
import os
from pathlib import Path

class MCPIntegration:
    """Handle MCP server integration for the Todo agent."""

    def __init__(self, user_workspace: str):
        self.user_workspace = user_workspace
        self.server = None

    async def setup_server(self):
        """Setup MCP server connection."""
        # Create MCP server for file operations
        self.server = MCPServerStdio(
            name="Todo Workspace Server",
            params={
                "command": "python",
                "args": ["-m", "app.mcp.todo_server", self.user_workspace]
            }
        )

        # Connect to the server
        await self.server.connect()

        return self.server

    async def get_agent_with_mcp(self):
        """Create agent with MCP server integration."""
        # Setup MCP server
        mcp_server = await self.setup_server()

        # Create agent with MCP server
        agent = Agent(
            name="Todo Assistant with MCP",
            instructions="Use MCP tools to access and manage user's todo workspace.",
            mcp_servers=[mcp_server]
        )

        return agent

    async def cleanup(self):
        """Clean up MCP server connection."""
        if self.server:
            await self.server.cleanup()
```

### 4. Context Management and History
```python
# app/agents/context_manager.py
from agents import user, assistant, system
from typing import List, Dict, Any
from datetime import datetime

class ContextManager:
    """Manage conversational history and context for the agent."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.history = self._initialize_history()

    def _initialize_history(self) -> List[Dict[str, Any]]:
        """Initialize conversation history with system message."""
        return [
            system(f"You are a helpful todo assistant for user {self.user_id}. Today is {datetime.now().strftime('%Y-%m-%d')}."),
        ]

    def add_user_message(self, message: str):
        """Add user message to history."""
        self.history.append(user(message))

    def add_assistant_response(self, response: str):
        """Add assistant response to history."""
        self.history.append(assistant(response))

    def get_context(self) -> List[Dict[str, Any]]:
        """Get current conversation context."""
        return self.history

    def clear_history(self):
        """Clear conversation history."""
        self.history = self._initialize_history()

    def add_memory(self, key: str, value: str):
        """Add contextual memory to the conversation."""
        self.history.append(system(f"[Memory: {key}={value}]"))
```

### 5. Complete Agent Implementation
```python
# app/agents/todo_assistant.py
from agents import Agent, Runner, function_tool
from agents.mcp import MCPServerStdio
from agents import AsyncOpenAI, OpenAIChatCompletionsModel
from agents.run import RunConfig
from pydantic import BaseModel, Field
from typing import Optional, List
import os
import asyncio

class TodoAssistant:
    """Complete implementation of a Todo assistant using OpenAI Agents SDK with OpenRouter."""

    def __init__(self, user_id: str):
        self.user_id = user_id
        self.context_manager = ContextManager(user_id)
        self.mcp_server = None
        
        # Setup OpenRouter client using specific configuration
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        openrouter_model = os.getenv("OPENROUTER_MODEL", "mistralai/devstral-2512:free")
        
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is not set in environment variables")
        
        external_client = AsyncOpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url,
        )

        # Define the model to use (using available OpenRouter models)
        model = OpenAIChatCompletionsModel(
            model=openrouter_model,  # Using mistralai/devstral-2512:free as specified
            openai_client=external_client
        )

        # Create run configuration with OpenRouter
        self.config = RunConfig(
            model=model,
            model_provider=external_client,
            # Add other configuration as needed
        )

    async def setup_mcp_server(self):
        """Setup MCP server for extended functionality."""
        # Create MCP server for advanced operations
        self.mcp_server = MCPServerStdio(
            name="Todo MCP Server",
            params={
                "command": "python",
                "args": ["-m", "app.mcp.todo_operations"]
            }
        )
        await self.mcp_server.connect()

    def create_agent(self) -> Agent:
        """Create the Todo assistant agent."""
        # Prepare tools
        tools = [
            self.add_task_tool,
            self.list_tasks_tool,
            self.complete_task_tool,
            self.update_task_tool,
            self.delete_task_tool,
        ]

        # Create agent with MCP server if available
        agent_kwargs = {
            "name": "Todo Assistant",
            "instructions": """
            You are a helpful assistant for managing todo tasks.
            - Always use the appropriate tools for task operations
            - Confirm actions before executing destructive operations (delete, complete)
            - Provide clear, friendly responses
            - Maintain context throughout the conversation
            """,
            "tools": tools
        }

        if self.mcp_server:
            agent_kwargs["mcp_servers"] = [self.mcp_server]

        return Agent(**agent_kwargs)

    async def process_message(self, message: str) -> Dict[str, Any]:
        """Process user message through the agent."""
        # Add user message to context
        self.context_manager.add_user_message(message)

        # Create agent
        agent = self.create_agent()

        # Run agent with current context
        result = await Runner.run(
            agent,
            self.context_manager.get_context(),
            config=self.config  # Use OpenRouter configuration
        )

        # Add assistant response to context
        self.context_manager.add_assistant_response(result.final_output)

        return {
            "response": result.final_output,
            "tool_calls": result.tool_calls,
            "context": self.context_manager.get_context()
        }

    # Define function tools
    @function_tool
    def add_task_tool(
        self,
        title: str,
        description: Optional[str] = None,
        priority: str = "medium"
    ) -> dict:
        """Add a new task to the user's list."""
        # In production, this would call your task service
        return {
            "success": True,
            "task_id": 123,
            "title": title,
            "description": description,
            "priority": priority,
            "message": f"Added task: {title}"
        }

    @function_tool
    def list_tasks_tool(
        self,
        status: Optional[str] = "all",
        priority: Optional[str] = None,
        limit: Optional[int] = 10
    ) -> dict:
        """List user's tasks with optional filtering."""
        # In production, this would fetch from your database
        tasks = [
            {"id": 1, "title": "Buy groceries", "completed": False, "priority": "medium"},
            {"id": 2, "title": "Call doctor", "completed": True, "priority": "high"}
        ]

        return {
            "tasks": tasks,
            "count": len(tasks),
            "filters_applied": {"status": status, "priority": priority}
        }

    @function_tool
    def complete_task_tool(self, task_id: int) -> dict:
        """Mark a task as completed."""
        # In production, this would update your database
        return {
            "success": True,
            "task_id": task_id,
            "message": f"Marked task {task_id} as completed"
        }

    @function_tool
    def update_task_tool(
        self,
        task_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None
    ) -> dict:
        """Update an existing task."""
        # In production, this would update your database
        return {
            "success": True,
            "task_id": task_id,
            "updates": {"title": title, "description": description},
            "message": f"Updated task {task_id}"
        }

    @function_tool
    def delete_task_tool(self, task_id: int) -> dict:
        """Delete a task by ID."""
        # In production, this would delete from your database
        return {
            "success": True,
            "deleted_task_id": task_id,
            "message": f"Deleted task {task_id}"
        }

# Usage example
async def main():
    assistant = TodoAssistant(user_id="user123")

    # Setup MCP server if needed
    await assistant.setup_mcp_server()

    # Process a message
    result = await assistant.process_message("Add a task to buy groceries")
    print(result["response"])

    # Cleanup
    if assistant.mcp_server:
        await assistant.mcp_server.cleanup()

if __name__ == "__main__":
    asyncio.run(main())
```

## MCP Server Patterns

### 1. Basic MCP Server Implementation
```python
# app/mcp/todo_server.py
import asyncio
import json
import sys
from typing import Dict, Any

class TodoMCPServer:
    """MCP server for todo operations."""

    def __init__(self):
        self.tools = {
            "add_todo": self.add_todo,
            "list_todos": self.list_todos,
            "complete_todo": self.complete_todo,
            "update_todo": self.update_todo,
            "delete_todo": self.delete_todo
        }

    async def run(self):
        """Run the MCP server loop."""
        while True:
            try:
                line = await self._read_line()
                if not line:
                    break

                request = json.loads(line)

                # Process the request
                response = await self._process_request(request)

                # Send response
                await self._write_response(response)

            except KeyboardInterrupt:
                break
            except Exception as e:
                error_response = {
                    "error": str(e),
                    "type": "error"
                }
                await self._write_response(error_response)

    async def _read_line(self) -> str:
        """Read a line from stdin."""
        return await asyncio.get_event_loop().run_in_executor(None, sys.stdin.readline)

    async def _write_response(self, response: Dict[str, Any]):
        """Write response to stdout."""
        print(json.dumps(response), flush=True)

    async def _process_request(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Process an MCP request."""
        if request.get("method") == "tools/list":
            return {
                "result": {
                    "tools": [
                        {
                            "name": name,
                            "description": f"Perform {name} operation",
                            "inputSchema": {
                                "type": "object",
                                "properties": {},
                                "required": []
                            }
                        }
                        for name in self.tools.keys()
                    ]
                },
                "id": request.get("id")
            }

        elif request.get("method") == "tools/call":
            tool_name = request.get("params", {}).get("name")
            tool_args = request.get("params", {}).get("arguments", {})

            if tool_name in self.tools:
                result = await self.tools[tool_name](**tool_args)
                return {
                    "result": result,
                    "id": request.get("id")
                }
            else:
                return {
                    "error": {"message": f"Unknown tool: {tool_name}"},
                    "id": request.get("id")
                }

        return {
            "error": {"message": "Unsupported method"},
            "id": request.get("id")
        }

    async def add_todo(self, title: str, description: str = "") -> Dict[str, Any]:
        """Add a new todo."""
        return {
            "success": True,
            "todo_id": 123,
            "title": title,
            "description": description
        }

    async def list_todos(self, status: str = "all") -> Dict[str, Any]:
        """List todos with optional filtering."""
        return {
            "todos": [
                {"id": 1, "title": "Sample task", "completed": False},
                {"id": 2, "title": "Another task", "completed": True}
            ]
        }

    async def complete_todo(self, todo_id: int) -> Dict[str, Any]:
        """Complete a todo."""
        return {
            "success": True,
            "todo_id": todo_id,
            "status": "completed"
        }

    async def update_todo(self, todo_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update a todo."""
        return {
            "success": True,
            "todo_id": todo_id,
            "updates": {"title": title, "description": description}
        }

    async def delete_todo(self, todo_id: int) -> Dict[str, Any]:
        """Delete a todo."""
        return {
            "success": True,
            "deleted_todo_id": todo_id
        }

if __name__ == "__main__":
    server = TodoMCPServer()
    asyncio.run(server.run())
```

## Best Practices

### 1. Security Considerations
```python
# Secure MCP server with validation
class SecureMCPServer:
    def __init__(self, allowed_tools: List[str]):
        self.allowed_tools = set(allowed_tools)
        self.tools = {
            "safe_operation": self.safe_operation,
            # Only safe operations
        }

    async def _validate_request(self, request: Dict[str, Any]) -> bool:
        """Validate incoming requests."""
        tool_name = request.get("params", {}).get("name")
        if tool_name not in self.allowed_tools:
            return False
        return True
```

### 2. Error Handling
```python
# Robust error handling in tools
@function_tool
def robust_task_tool(
    task_id: int,
    title: Optional[str] = None
) -> dict:
    """Tool with comprehensive error handling."""
    try:
        if not title:
            raise ValueError("Title is required")

        if task_id <= 0:
            raise ValueError("Task ID must be positive")

        # Perform operation
        result = perform_operation(task_id, title)

        return {
            "success": True,
            "result": result
        }

    except ValueError as e:
        return {
            "success": False,
            "error": str(e),
            "error_type": "validation"
        }
    except Exception as e:
        return {
            "success": False,
            "error": "Internal server error",
            "error_type": "internal"
        }
```

## Integration with Existing Systems

### 1. Connecting to Todo Services
```python
# app/agents/todo_service_integration.py
from app.services.task_service import TaskService

class TodoAgentWithService:
    def __init__(self, user_id: str, task_service: TaskService):
        self.user_id = user_id
        self.task_service = task_service
        
        # Setup OpenRouter client using specific configuration
        openrouter_api_key = os.getenv("OPENROUTER_API_KEY")
        openrouter_base_url = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        openrouter_model = os.getenv("OPENROUTER_MODEL", "mistralai/devstral-2512:free")
        
        if not openrouter_api_key:
            raise ValueError("OPENROUTER_API_KEY is not set in environment variables")
        
        external_client = AsyncOpenAI(
            api_key=openrouter_api_key,
            base_url=openrouter_base_url,
        )

        # Define the model to use (using available OpenRouter models)
        model = OpenAIChatCompletionsModel(
            model=openrouter_model,  # Using mistralai/devstral-2512:free as specified
            openai_client=external_client
        )

        # Create run configuration with OpenRouter
        self.config = RunConfig(
            model=model,
            model_provider=external_client,
            # Add other configuration as needed
        )

    @function_tool
    async def add_task_from_service(
        self,
        title: str,
        description: Optional[str] = None
    ) -> dict:
        """Add task using the actual task service."""
        try:
            task = await self.task_service.create_task(
                user_id=self.user_id,
                title=title,
                description=description
            )

            return {
                "success": True,
                "task_id": task.id,
                "title": task.title,
                "message": f"Created task: {task.title}"
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
```

## Example Usage Scenarios

| User Input | Expected Behavior | Tools Called |
|------------|------------------|--------------|
| "Add a task to buy groceries" | Create new task | `add_task_tool` |
| "Show me my tasks" | List all tasks | `list_tasks_tool` |
| "Mark task 3 as complete" | Complete specific task | `complete_task_tool` |
| "Update task 1 to 'Call mom'" | Update task title | `update_task_tool` |
| "Delete the meeting task" | Delete specific task | `delete_task_tool` |

## Production Considerations

1. **Resource Management**: Properly manage MCP server lifecycle with connect/cleanup
2. **Security**: Validate all inputs and restrict tool access appropriately
3. **Error Handling**: Implement comprehensive error handling and recovery
4. **Monitoring**: Log agent runs and tool calls for debugging
5. **Rate Limiting**: Implement rate limiting for expensive operations
6. **Caching**: Cache frequently accessed data to improve performance
7. **OpenRouter Integration**: Use specific configuration with FREE model mistralai/devstral-2512:free

---

**Production Standard**: This skill ensures secure, efficient, and well-structured OpenAI Agents SDK implementations with proper OpenRouter integration, MCP server integration, context management, and production-ready error handling.
