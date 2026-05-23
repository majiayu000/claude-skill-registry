---
name: openai-agents-setup
description: Initialize and configure OpenAI Agents SDK for building AI-powered chatbots. Uses NATIVE MCP integration via MCPServerStreamableHttp - no @function_tool wrappers needed! Use when setting up AI agents for Phase 3 chatbot implementation.
allowed-tools: Bash, Write, Read, Edit, Glob
---

# OpenAI Agents SDK Setup with Gemini + Native MCP Integration

Quick reference for initializing OpenAI Agents SDK with **Gemini models** (gemini-2.5-flash) using **native MCP integration** for the Todo AI Chatbot Phase 3.

**CRITICAL INSIGHT**: The OpenAI Agents SDK has **native MCP support** via `MCPServerStreamableHttp`. We do NOT need `@function_tool` wrappers! The agent connects directly to the MCP server and discovers tools automatically.

**Reference Repository**: https://github.com/panaversity/learn-agentic-ai

---

## Architecture Overview

```
+-------------------------------------------------------------+
|                      FastAPI Backend                         |
+-------------------------------------------------------------+
|  +---------------+     +-----------------------------+      |
|  | Chat Endpoint |---->| OpenAI Agents SDK           |      |
|  | /api/chat     |     | (Agent + Gemini Model)      |      |
|  +---------------+     +-------------+---------------+      |
|                                      |                      |
|                        MCPServerStreamableHttp              |
|                        (Native MCP Integration!)            |
|                                      |                      |
+--------------------------------------+----------------------+
                                       |
                        +--------------v---------------+
                        | FastMCP Server               |
                        | (Task Tools: add, list, etc.)|
                        | -> Database Operations       |
                        +------------------------------+
```

**Key Insight**: The Agent uses `MCPServerStreamableHttp` for NATIVE MCP support. No `@function_tool` wrappers needed! Tools are discovered automatically from the MCP server.

---

## Project Structure

```
backend/src/
+-- agents/
|   +-- __init__.py          # Package exports
|   +-- config.py            # Gemini + AsyncOpenAI + MCP URL config
|   +-- hooks.py             # Agent and Runner lifecycle hooks
|   +-- todo_agent.py        # Agent config (no MCP attached)
|   +-- runner.py            # Agent execution with NATIVE MCP
|   +-- tools.py             # DEPRECATED - documentation only
|   +-- errors.py            # Custom exception classes
|
+-- mcp_server/
|   +-- __init__.py
|   +-- server.py            # FastMCP server with task tools
|
+-- api/routes/
    +-- chat.py              # Chat API endpoint
```

---

## Installation

```bash
cd backend
uv add openai-agents httpx
# Note: fastmcp is only needed for the MCP SERVER, not the agent!
```

**Required Environment Variables** (`.env`):
```env
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
MCP_SERVER_URL=http://localhost:8001
```

---

## Core Setup Files

### 1. Gemini Configuration (`config.py`)

```python
# backend/src/agents/config.py
"""
Gemini model configuration for OpenAI Agents SDK.
Uses Gemini's OpenAI-compatible endpoint via AsyncOpenAI.
"""
from openai import AsyncOpenAI
from agents import OpenAIChatCompletionsModel

from src.core.config import settings

GEMINI_BASE_URL = "https://generativelanguage.googleapis.com/v1beta/openai/"


def get_gemini_client() -> AsyncOpenAI:
    """Create AsyncOpenAI client configured for Gemini API."""
    if not settings.GEMINI_API_KEY:
        raise ValueError("GEMINI_API_KEY is not configured")

    return AsyncOpenAI(
        api_key=settings.GEMINI_API_KEY,
        base_url=GEMINI_BASE_URL,
    )


def get_gemini_model(model_name: str | None = None) -> OpenAIChatCompletionsModel:
    """Create OpenAIChatCompletionsModel wrapper for Gemini."""
    client = get_gemini_client()
    model = model_name or settings.GEMINI_MODEL

    return OpenAIChatCompletionsModel(
        model=model,
        openai_client=client,
    )


def get_mcp_server_url() -> str:
    """Get the MCP server URL (no /mcp path needed for HTTP transport)."""
    return settings.MCP_SERVER_URL.rstrip("/")
```

### 2. Agent Definition (`todo_agent.py`)

```python
# backend/src/agents/todo_agent.py
"""
TodoBot Agent definition.
NOTE: MCP servers are attached via context manager in runner.py!
"""
from agents import Agent
from src.agents.config import get_gemini_model


SYSTEM_PROMPT = """You are TodoBot, a helpful AI assistant...
[Your system prompt here]

## Current User Context
- User ID: {user_id}
- All task operations should use this user_id
"""


def create_todo_agent_config(user_id: str) -> tuple[str, str]:
    """Create agent config for a specific user."""
    instructions = SYSTEM_PROMPT.format(user_id=user_id)
    return ("TodoBot", instructions)


def create_todo_agent_without_mcp(user_id: str) -> Agent:
    """Create agent WITHOUT MCP servers (attach them via context manager)."""
    name, instructions = create_todo_agent_config(user_id)

    return Agent(
        name=name,
        instructions=instructions,
        model=get_gemini_model(),
        # NO tools or mcp_servers here - attached via context manager!
    )
```

### 3. Runner with Native MCP (`runner.py`) - **KEY FILE**

```python
# backend/src/agents/runner.py
"""
Agent execution with NATIVE MCP integration via MCPServerStreamableHttp.
"""
import logging
from dataclasses import dataclass
from typing import AsyncGenerator, Optional

from agents import Agent, Runner
from agents.mcp import MCPServerStreamableHttp
from agents.items import (
    TResponseInputItem,
    MessageOutputItem,
    ToolCallItem,
    ToolCallOutputItem,
)

from src.agents.config import get_gemini_model, get_mcp_server_url
from src.agents.hooks import run_hooks

logger = logging.getLogger("todobot.runner")


@dataclass
class AgentResponse:
    content: str
    tool_calls: Optional[list[dict]] = None


@dataclass
class StreamEvent:
    type: str  # 'token', 'tool_call', 'tool_result', 'done', 'error'
    content: Optional[str] = None
    data: Optional[dict] = None


async def run_agent(
    user_id: str,
    message: str,
    history: Optional[list[dict[str, str]]] = None,
) -> AgentResponse:
    """Run agent with native MCP integration (non-streaming)."""
    input_messages: list[TResponseInputItem] = []

    if history:
        for msg in history:
            input_messages.append({"role": msg["role"], "content": msg["content"]})

    input_messages.append({"role": "user", "content": message})

    mcp_url = get_mcp_server_url()

    # KEY: Native MCP integration via async context manager!
    async with MCPServerStreamableHttp(
        name="Todo MCP Server",
        params={"url": mcp_url},
        cache_tools_list=True,
    ) as mcp_server:
        from src.agents.todo_agent import create_todo_agent_config
        name, instructions = create_todo_agent_config(user_id)

        # Create agent with MCP server attached
        agent = Agent(
            name=name,
            instructions=instructions,
            model=get_gemini_model(),
            mcp_servers=[mcp_server],  # Native MCP integration!
        )

        result = await Runner.run(
            agent,
            input=input_messages,
            hooks=run_hooks,
        )

        # Extract content and tool calls from result
        content = result.final_output or ""
        tool_calls = []

        for item in result.new_items:
            if isinstance(item, ToolCallItem):
                tool_calls.append({
                    "tool": item.name,
                    "args": item.arguments,
                    "call_id": item.call_id,
                })
            elif isinstance(item, ToolCallOutputItem):
                for tc in tool_calls:
                    if tc.get("call_id") == item.call_id:
                        tc["result"] = item.output
                        break

        return AgentResponse(
            content=content,
            tool_calls=tool_calls if tool_calls else None,
        )


async def run_agent_streamed(
    user_id: str,
    message: str,
    history: Optional[list[dict[str, str]]] = None,
) -> AsyncGenerator[StreamEvent, None]:
    """Run agent with native MCP integration (streaming)."""
    input_messages: list[TResponseInputItem] = []

    if history:
        for msg in history:
            input_messages.append({"role": msg["role"], "content": msg["content"]})

    input_messages.append({"role": "user", "content": message})

    mcp_url = get_mcp_server_url()
    tool_calls: list[dict] = []

    async with MCPServerStreamableHttp(
        name="Todo MCP Server",
        params={"url": mcp_url},
        cache_tools_list=True,
    ) as mcp_server:
        from src.agents.todo_agent import create_todo_agent_config
        name, instructions = create_todo_agent_config(user_id)

        agent = Agent(
            name=name,
            instructions=instructions,
            model=get_gemini_model(),
            mcp_servers=[mcp_server],
        )

        async with Runner.run_streamed(
            agent,
            input=input_messages,
            hooks=run_hooks,
        ) as stream:
            async for event in stream.stream_events():
                event_type = type(event).__name__

                if event_type == "RunItemStreamEvent":
                    item = event.item

                    if isinstance(item, MessageOutputItem):
                        if hasattr(item, "content") and isinstance(item.content, str):
                            yield StreamEvent(type="token", content=item.content)

                    elif isinstance(item, ToolCallItem):
                        tool_data = {
                            "tool": item.name,
                            "args": item.arguments,
                            "call_id": item.call_id,
                        }
                        tool_calls.append(tool_data)
                        yield StreamEvent(type="tool_call", data=tool_data)

                    elif isinstance(item, ToolCallOutputItem):
                        result_data = {
                            "call_id": item.call_id,
                            "output": item.output,
                        }
                        yield StreamEvent(type="tool_result", data=result_data)

    yield StreamEvent(
        type="done",
        data={"tool_calls": tool_calls if tool_calls else None},
    )
```

### 4. Chat Endpoint Usage

```python
# backend/src/api/routes/chat.py
from src.agents.runner import run_agent, run_agent_streamed

@router.post("/chat")
async def send_message(request: ChatRequest, current_user = Depends(get_current_user)):
    user_id = current_user["id"]

    # Simple! Runner handles MCP connection internally
    response = await run_agent(
        user_id=user_id,
        message=request.message,
        history=history,
    )

    return {"response": response.content, "tool_calls": response.tool_calls}


@router.post("/chat/stream")
async def send_message_stream(request: ChatRequest, current_user = Depends(get_current_user)):
    user_id = current_user["id"]

    async def generate():
        async for event in run_agent_streamed(
            user_id=user_id,
            message=request.message,
            history=history,
        ):
            yield event_to_sse(event)

    return EventSourceResponse(generate())
```

---

## OLD vs NEW Approach

### OLD (Deprecated) - Function Tool Wrappers

```python
# DON'T DO THIS - it's verbose and unnecessary!
from agents import function_tool
from fastmcp import Client

@function_tool
async def add_task(user_id: str, title: str) -> str:
    async with Client(mcp_url) as client:
        result = await client.call_tool("add_task", {"user_id": user_id, "title": title})
        return str(result)

agent = Agent(
    name="TodoBot",
    tools=[add_task, list_tasks, ...],  # Manual tool wrappers
)
```

### NEW (Recommended) - Native MCP Integration

```python
# DO THIS - native MCP support, tools discovered automatically!
from agents.mcp import MCPServerStreamableHttp

async with MCPServerStreamableHttp(
    name="Todo MCP Server",
    params={"url": mcp_url},
) as mcp_server:
    agent = Agent(
        name="TodoBot",
        mcp_servers=[mcp_server],  # Tools discovered automatically!
    )
    result = await Runner.run(agent, input=message)
```

---

## Quick Start

### 1. Start MCP Server First
```bash
cd backend
uv run python -m src.mcp_server.server
# Running on http://localhost:8001
```

### 2. Test Agent with Native MCP
```python
import asyncio
from src.agents import run_agent

async def main():
    response = await run_agent(
        user_id="test-user-123",
        message="Add a task to buy groceries"
    )
    print(response.content)

asyncio.run(main())
```

---

## Verification Checklist

- [ ] `openai-agents` package installed
- [ ] `GEMINI_API_KEY` set in environment
- [ ] `MCP_SERVER_URL` set in environment (e.g., `http://localhost:8001` - no /mcp path)
- [ ] FastMCP server running on port 8001
- [ ] Agent connects via MCPServerStreamableHttp
- [ ] Tools discovered automatically from MCP server
- [ ] Runner executes without errors

---

## Environment Variables

```env
# Required
GEMINI_API_KEY=your_api_key_here
MCP_SERVER_URL=http://localhost:8001

# Optional
GEMINI_MODEL=gemini-2.5-flash
```

---

## Key Differences from Previous Approach

| Aspect | Old (Function Tools) | New (Native MCP) |
|--------|---------------------|------------------|
| Tool Definition | `@function_tool` wrappers | Automatic discovery |
| MCP Connection | Manual `Client` in each tool | `MCPServerStreamableHttp` context |
| Agent Creation | `tools=[add_task, ...]` | `mcp_servers=[server]` |
| Maintenance | Update wrappers when server changes | Zero maintenance |
| Code Size | ~200 lines for 5 tools | ~10 lines total |

---

## See Also

- [fastmcp-server-setup](../fastmcp-server-setup/) - MCP server setup
- [chat-api-integration](../chat-api-integration/) - Chat endpoint setup
- [streaming-sse-setup](../streaming-sse-setup/) - SSE streaming setup
