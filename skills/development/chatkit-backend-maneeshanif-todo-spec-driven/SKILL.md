---
name: chatkit-backend
description: Build FastAPI backend for OpenAI ChatKit with SSE streaming, conversation persistence, and AI agent integration. Handles /chatkit endpoint, ChatKit-compatible SSE format, conversation models, and message storage. Use when implementing chat backend, SSE streaming endpoint, or connecting AI agent to ChatKit frontend.
allowed-tools: Bash, Write, Read, Edit, Glob, Grep
---

# ChatKit Backend Skill

Production-ready skill for implementing FastAPI backend that powers OpenAI ChatKit frontend.

**Reference Repositories**:
- [ChatKit Advanced Samples](https://github.com/openai/openai-chatkit-advanced-samples)
- [Learn Agentic AI](https://github.com/panaversity/learn-agentic-ai)

---

## Overview

ChatKit backend provides:

- **SSE Streaming Endpoint** - Real-time response streaming in ChatKit format
- **Conversation Persistence** - Store conversations and messages in database
- **AI Agent Integration** - Connect OpenAI Agents SDK to ChatKit
- **Tool Execution** - Execute tools and stream results to frontend

---

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                        FastAPI Backend                                   │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  POST /chatkit                                                           │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  1. Validate request (auth, user_id)                                │ │
│  │  2. Get/create conversation                                         │ │
│  │  3. Load conversation history                                       │ │
│  │  4. Run AI agent with message                                       │ │
│  │  5. Stream response in ChatKit SSE format                           │ │
│  │  6. Store message and response                                      │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                 │                                        │
│                                 ▼                                        │
│  ┌────────────────────────────────────────────────────────────────────┐ │
│  │  SSE Response Format:                                               │ │
│  │  data: {"type": "text", "content": "Hello"}\n\n                    │ │
│  │  data: {"type": "tool_call", "name": "add_task", "args": {...}}\n\n│ │
│  │  data: {"type": "tool_result", "result": {...}}\n\n                │ │
│  │  data: [DONE]\n\n                                                   │ │
│  └────────────────────────────────────────────────────────────────────┘ │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

---

## SSE Event Format

ChatKit expects specific SSE event types:

### Text Event (Streaming Content)

```python
yield f"data: {json.dumps({'type': 'text', 'content': 'Hello'})}\n\n"
```

### Tool Call Event

```python
yield f"data: {json.dumps({'type': 'tool_call', 'name': 'add_task', 'args': {'title': 'Buy groceries'}})}\n\n"
```

### Tool Result Event

```python
yield f"data: {json.dumps({'type': 'tool_result', 'name': 'add_task', 'result': {'success': True, 'task_id': 123}})}\n\n"
```

### Done Event

```python
yield "data: [DONE]\n\n"
```

Or:

```python
yield f"data: {json.dumps({'type': 'done'})}\n\n"
```

---

## Project Structure

```
backend/src/
├── routers/
│   ├── chatkit.py              # ChatKit SSE endpoint (NEW!)
│   └── conversations.py        # Conversation CRUD endpoints
│
├── models/
│   ├── conversation.py         # Conversation model
│   └── message.py              # Message model
│
├── schemas/
│   └── chatkit.py              # ChatKit request/response schemas
│
├── services/
│   └── chatkit_service.py      # ChatKit business logic
│
├── agents/                     # OpenAI Agents (from openai-agents-setup)
│   ├── config.py               # Gemini/LiteLLM config
│   ├── todo_agent.py           # Agent definition
│   └── runner.py               # Agent execution
│
└── main.py                     # Register chatkit router
```

---

## Quick Start

### Step 1: Create ChatKit Router

```python
# backend/src/routers/chatkit.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import StreamingResponse
from sqlmodel import Session, select
from src.database import get_session
from src.middleware.auth import verify_jwt
from src.models.conversation import Conversation
from src.models.message import Message
from src.agents import run_todo_agent_streaming
from datetime import datetime
import json
import logging

router = APIRouter(tags=["chatkit"])
logger = logging.getLogger(__name__)


@router.post("/chatkit")
async def chatkit_endpoint(
    request: Request,
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """
    ChatKit SSE streaming endpoint.

    Receives messages from ChatKit frontend and streams responses
    in ChatKit-compatible SSE format.
    """
    user_id = current_user["id"]

    # Parse request body
    body = await request.json()
    message = body.get("message", "")
    thread_id = body.get("thread_id")  # Optional conversation ID

    if not message:
        raise HTTPException(status_code=400, detail="Message is required")

    # Get or create conversation
    conversation = await get_or_create_conversation(
        session, user_id, thread_id, message
    )

    # Load conversation history
    history = await load_conversation_history(session, conversation.id)

    # Store user message
    user_msg = Message(
        conversation_id=conversation.id,
        role="user",
        content=message,
    )
    session.add(user_msg)
    session.commit()

    async def generate():
        response_content = ""

        try:
            # Stream agent response
            async for event in run_todo_agent_streaming(
                user_message=message,
                user_id=user_id,
                conversation_history=history,
            ):
                event_type = event.get("type")

                if event_type == "text":
                    content = event.get("content", "")
                    response_content += content
                    yield f"data: {json.dumps(event)}\n\n"

                elif event_type == "tool_call":
                    yield f"data: {json.dumps(event)}\n\n"

                elif event_type == "tool_result":
                    yield f"data: {json.dumps(event)}\n\n"

                elif event_type == "thinking":
                    # Optional: send thinking events
                    yield f"data: {json.dumps(event)}\n\n"

            # Store assistant response
            if response_content:
                assistant_msg = Message(
                    conversation_id=conversation.id,
                    role="assistant",
                    content=response_content,
                )
                session.add(assistant_msg)

                # Update conversation timestamp
                conversation.updated_at = datetime.utcnow()
                session.add(conversation)
                session.commit()

            # Signal completion
            yield "data: [DONE]\n\n"

        except Exception as e:
            logger.error(f"ChatKit streaming error: {e}")
            yield f"data: {json.dumps({'type': 'error', 'message': 'An error occurred'})}\n\n"

    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


async def get_or_create_conversation(
    session: Session,
    user_id: str,
    thread_id: int | None,
    message: str,
) -> Conversation:
    """Get existing conversation or create new one."""
    if thread_id:
        conversation = session.exec(
            select(Conversation).where(
                Conversation.id == thread_id,
                Conversation.user_id == user_id,
            )
        ).first()
        if conversation:
            return conversation

    # Create new conversation
    title = message[:50] + "..." if len(message) > 50 else message
    conversation = Conversation(user_id=user_id, title=title)
    session.add(conversation)
    session.commit()
    session.refresh(conversation)
    return conversation


async def load_conversation_history(
    session: Session,
    conversation_id: int,
) -> list[dict]:
    """Load conversation history for context."""
    messages = session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at)
    ).all()

    return [
        {"role": msg.role, "content": msg.content}
        for msg in messages
    ]
```

### Step 2: Register Router

```python
# backend/src/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routers import tasks, chatkit, conversations

app = FastAPI(title="Todo API")

# CORS for ChatKit
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "https://your-app.vercel.app",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register routers
app.include_router(tasks.router)
app.include_router(chatkit.router)
app.include_router(conversations.router)
```

---

## Streaming Agent Runner

Integrate with OpenAI Agents SDK:

```python
# backend/src/agents/runner.py
from typing import AsyncGenerator
from agents import Runner
from .todo_agent import todo_agent
import asyncio
import logging

logger = logging.getLogger(__name__)


async def run_todo_agent_streaming(
    user_message: str,
    user_id: str,
    conversation_history: list[dict] | None = None,
) -> AsyncGenerator[dict, None]:
    """
    Execute agent and yield events for ChatKit streaming.

    Event Types:
    - {"type": "thinking", "content": "Analyzing request..."}
    - {"type": "text", "content": "Hello"}
    - {"type": "tool_call", "name": "add_task", "args": {...}}
    - {"type": "tool_result", "name": "add_task", "result": {...}}
    """
    # Enhance message with user context
    enhanced_message = f"[User ID: {user_id}]\n{user_message}"

    # Build input with history
    input_messages = []
    if conversation_history:
        input_messages.extend(conversation_history)
    input_messages.append({"role": "user", "content": enhanced_message})

    try:
        # Signal thinking
        yield {"type": "thinking", "content": "Processing your request..."}

        # Run agent
        result = await Runner.run(
            todo_agent,
            input=input_messages if conversation_history else enhanced_message,
            max_turns=10,
        )

        response_text = result.final_output

        # Stream text in chunks for natural feel
        chunk_size = 20
        for i in range(0, len(response_text), chunk_size):
            chunk = response_text[i:i + chunk_size]
            yield {"type": "text", "content": chunk}
            await asyncio.sleep(0.02)  # Natural streaming pace

    except Exception as e:
        logger.error(f"Agent streaming error: {e}")
        yield {"type": "error", "message": str(e)}
```

---

## Streaming with Tool Events

Full streaming with tool call/result events:

```python
# backend/src/agents/runner.py
async def run_todo_agent_streaming_with_tools(
    user_message: str,
    user_id: str,
    conversation_history: list[dict] | None = None,
) -> AsyncGenerator[dict, None]:
    """
    Stream agent response with tool execution events.
    """
    from agents import Runner

    enhanced_message = f"[User ID: {user_id}]\n{user_message}"

    input_messages = []
    if conversation_history:
        input_messages.extend(conversation_history)
    input_messages.append({"role": "user", "content": enhanced_message})

    try:
        yield {"type": "thinking", "content": "Analyzing your request..."}

        # Use streaming run for real-time events
        async with Runner.run_streamed(
            todo_agent,
            input=input_messages,
        ) as stream:
            async for event in stream:
                if event.type == "raw_model_stream_event":
                    # Text delta from model
                    if hasattr(event.data, "delta") and event.data.delta:
                        yield {"type": "text", "content": event.data.delta}

                elif event.type == "tool_call_start":
                    yield {
                        "type": "tool_call",
                        "name": event.tool.name,
                        "args": event.arguments,
                    }

                elif event.type == "tool_call_end":
                    yield {
                        "type": "tool_result",
                        "name": event.tool.name,
                        "result": event.result if hasattr(event, 'result') else {},
                    }

    except Exception as e:
        logger.error(f"Streaming error: {e}")
        yield {"type": "error", "message": str(e)}
```

---

## Database Models

### Conversation Model

```python
# backend/src/models/conversation.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .message import Message


class Conversation(SQLModel, table=True):
    __tablename__ = "conversations"

    id: int | None = Field(default=None, primary_key=True)
    user_id: str = Field(index=True)
    title: str | None = Field(default=None, max_length=200)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    messages: list["Message"] = Relationship(back_populates="conversation")
```

### Message Model

```python
# backend/src/models/message.py
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .conversation import Conversation


class Message(SQLModel, table=True):
    __tablename__ = "messages"

    id: int | None = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # "user", "assistant", "system"
    content: str = Field()
    tool_calls: str | None = Field(default=None)  # JSON string
    created_at: datetime = Field(default_factory=datetime.utcnow)

    conversation: "Conversation" = Relationship(back_populates="messages")
```

---

## Conversation CRUD Endpoints

```python
# backend/src/routers/conversations.py
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select, desc
from src.database import get_session
from src.middleware.auth import verify_jwt
from src.models.conversation import Conversation
from src.models.message import Message
from pydantic import BaseModel
from datetime import datetime

router = APIRouter(prefix="/api/conversations", tags=["conversations"])


class ConversationResponse(BaseModel):
    id: int
    title: str | None
    created_at: datetime
    updated_at: datetime


@router.get("/", response_model=list[ConversationResponse])
async def list_conversations(
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """List user's conversations."""
    conversations = session.exec(
        select(Conversation)
        .where(Conversation.user_id == current_user["id"])
        .order_by(desc(Conversation.updated_at))
    ).all()
    return conversations


@router.delete("/{conversation_id}")
async def delete_conversation(
    conversation_id: int,
    session: Session = Depends(get_session),
    current_user: dict = Depends(verify_jwt),
):
    """Delete conversation and messages."""
    conversation = session.exec(
        select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == current_user["id"],
        )
    ).first()

    if not conversation:
        raise HTTPException(status_code=404, detail="Not found")

    # Delete messages
    for msg in conversation.messages:
        session.delete(msg)

    # Delete conversation
    session.delete(conversation)
    session.commit()

    return {"status": "deleted"}
```

---

## Database Migration

```bash
# Create migration
cd backend
uv run alembic revision --autogenerate -m "Add conversations and messages"
uv run alembic upgrade head
```

---

## Environment Variables

```env
# Backend (.env)
DATABASE_URL=postgresql://user:pass@host/db
BETTER_AUTH_SECRET=your_auth_secret
GEMINI_API_KEY=your_gemini_api_key
GEMINI_MODEL=gemini-2.5-flash
```

---

## Testing

### Test SSE Endpoint

```bash
# Test with curl
curl -X POST http://localhost:8000/chatkit \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"message": "Show my tasks"}'
```

### Python Test

```python
import httpx
import asyncio

async def test_chatkit():
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://localhost:8000/chatkit",
            json={"message": "Show my tasks"},
            headers={"Authorization": "Bearer TOKEN"},
        ) as response:
            async for line in response.aiter_lines():
                if line.startswith("data: "):
                    print(line[6:])

asyncio.run(test_chatkit())
```

---

## Verification Checklist

- [ ] `/chatkit` endpoint created
- [ ] SSE format matches ChatKit expectations
- [ ] Conversation model with user_id
- [ ] Message model with role and content
- [ ] Messages stored after streaming
- [ ] Conversation updated_at updated
- [ ] CORS configured for frontend
- [ ] Agent integration working
- [ ] Tool events streaming correctly
- [ ] Error handling with SSE error events

---

## See Also

- [REFERENCE.md](./REFERENCE.md) - SSE format reference
- [examples.md](./examples.md) - Full code examples
- [chatkit-frontend skill](../chatkit-frontend/) - Frontend integration
- [openai-agents-setup skill](../openai-agents-setup/) - Agent configuration
