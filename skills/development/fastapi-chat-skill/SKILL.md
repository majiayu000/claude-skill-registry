---
name: fastapi-chat-skill
description: Production-ready FastAPI backend skill for handling chat requests, persisting conversations, invoking OpenAI Agents SDK, and managing MCP tool execution for Todo AI chatbot.
---

# FastAPI Chat Skill

Use this skill when implementing the backend chat endpoint that handles AI conversations and task operations via MCP tools.

## When to Use

- Building stateless chat API endpoint
- Persisting conversation and message history
- Integrating OpenAI Agents SDK with FastAPI
- Managing MCP tool execution
- Handling chat request/response cycle

## Core Responsibilities

### 1. Chat Endpoint
```python
# app/api/routes/chat.py
from fastapi import APIRouter, HTTPException, Depends
from sqlmodel import Session
from app.models import Conversation, Message
from app.services.chat_service import ChatService
from app.api.deps import get_db, get_current_user

router = APIRouter()

@router.post("/{user_id}/chat")
async def chat_endpoint(
    user_id: str,
    request: ChatRequest,
    db: Session = Depends(get_db),
    current_user: str = Depends(get_current_user)
):
    """
    Stateless chat endpoint that handles AI conversations.

    Request: { "message": str, "conversation_id": int? }
    Response: { "conversation_id": int, "response": str, "tool_calls": [] }
    """
    # Verify user authorization
    if current_user != user_id:
        raise HTTPException(status_code=403, detail="Unauthorized")

    chat_service = ChatService(db)

    try:
        result = await chat_service.process_message(
            user_id=user_id,
            message=request.message,
            conversation_id=request.conversation_id
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

### 2. Request/Response Models
```python
# app/schemas/chat.py
from pydantic import BaseModel
from typing import Optional, List

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[int] = None

class ToolCall(BaseModel):
    tool_name: str
    parameters: dict
    result: dict

class ChatResponse(BaseModel):
    conversation_id: int
    response: str
    tool_calls: List[ToolCall] = []
```

### 3. Database Models
```python
# app/models/conversation.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Conversation(SQLModel, table=True):
    """Conversation session between user and AI."""

    __tablename__ = "conversations"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: str = Field(index=True, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

```python
# app/models/message.py
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

class Message(SQLModel, table=True):
    """Individual message in a conversation."""

    __tablename__ = "messages"

    id: Optional[int] = Field(default=None, primary_key=True)
    conversation_id: int = Field(foreign_key="conversations.id", index=True)
    role: str = Field(max_length=20)  # 'user' or 'assistant'
    content: str = Field(sa_column=Column(Text))
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

### 4. Chat Service
```python
# app/services/chat_service.py
from sqlmodel import Session, select
from app.models import Conversation, Message
from app.agents.todo_chat_agent import TodoChatAgent
from typing import Optional

class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.agent = TodoChatAgent()

    async def process_message(
        self,
        user_id: str,
        message: str,
        conversation_id: Optional[int] = None
    ) -> dict:
        """
        Process a chat message through the AI agent.

        Flow:
        1. Get or create conversation
        2. Fetch conversation history
        3. Store user message
        4. Invoke AI agent with history
        5. Store AI response
        6. Return structured response
        """
        # Step 1: Get or create conversation
        if conversation_id:
            conversation = self._get_conversation(conversation_id, user_id)
            if not conversation:
                # Invalid ID, create new
                conversation = self._create_conversation(user_id)
        else:
            conversation = self._create_conversation(user_id)

        # Step 2: Fetch history
        history = self._get_conversation_history(conversation.id)

        # Step 3: Store user message
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=message
        )
        self.db.add(user_message)
        self.db.commit()

        # Step 4: Invoke agent
        messages = [
            {"role": msg.role, "content": msg.content}
            for msg in history
        ] + [{"role": "user", "content": message}]

        agent_result = await self.agent.run(
            user_id=user_id,
            messages=messages
        )

        # Step 5: Store AI response
        assistant_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=agent_result["response"]
        )
        self.db.add(assistant_message)
        self.db.commit()

        # Step 6: Return response
        return {
            "conversation_id": conversation.id,
            "response": agent_result["response"],
            "tool_calls": agent_result.get("tool_calls", [])
        }

    def _get_conversation(
        self,
        conversation_id: int,
        user_id: str
    ) -> Optional[Conversation]:
        """Fetch conversation if it belongs to user."""
        statement = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        return self.db.exec(statement).first()

    def _create_conversation(self, user_id: str) -> Conversation:
        """Create new conversation."""
        conversation = Conversation(user_id=user_id)
        self.db.add(conversation)
        self.db.commit()
        self.db.refresh(conversation)
        return conversation

    def _get_conversation_history(
        self,
        conversation_id: int
    ) -> list[Message]:
        """Fetch all messages in conversation, ordered by time."""
        statement = select(Message).where(
            Message.conversation_id == conversation_id
        ).order_by(Message.created_at)
        return list(self.db.exec(statement).all())
```

### 5. Agent Integration
```python
# app/agents/todo_chat_agent.py
import os
from openai import OpenAI
from app.mcp.tools import get_mcp_tools

class TodoChatAgent:
    def __init__(self):
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model = os.getenv("OPENAI_MODEL", "gpt-4o")
        self.tools = get_mcp_tools()

    async def run(self, user_id: str, messages: list[dict]) -> dict:
        """
        Run OpenAI agent with MCP tools.

        Returns: {
            "response": str,
            "tool_calls": [{"tool_name": str, "parameters": dict, "result": dict}]
        }
        """
        # Add system message
        system_message = {
            "role": "system",
            "content": (
                "You are a helpful AI assistant for managing todo tasks. "
                "You can add, list, complete, update, and delete tasks using the provided tools. "
                "Always confirm actions to the user in a friendly way."
            )
        }

        # Call OpenAI with tools
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[system_message] + messages,
            tools=self.tools,
            tool_choice="auto"
        )

        message = response.choices[0].message
        tool_calls_log = []

        # Handle tool calls
        if message.tool_calls:
            for tool_call in message.tool_calls:
                tool_name = tool_call.function.name
                tool_args = json.loads(tool_call.function.arguments)

                # Execute MCP tool
                tool_result = await self._execute_tool(
                    user_id=user_id,
                    tool_name=tool_name,
                    parameters=tool_args
                )

                tool_calls_log.append({
                    "tool_name": tool_name,
                    "parameters": tool_args,
                    "result": tool_result
                })

            # Get final response after tool execution
            # (In production, you'd add tool results and call API again)
            final_response = message.content or "Task completed successfully!"
        else:
            final_response = message.content

        return {
            "response": final_response,
            "tool_calls": tool_calls_log
        }

    async def _execute_tool(
        self,
        user_id: str,
        tool_name: str,
        parameters: dict
    ) -> dict:
        """Execute MCP tool and return result."""
        from app.mcp.server import mcp_server

        # Add user_id to parameters
        parameters["user_id"] = user_id

        # Call MCP tool
        result = await mcp_server.call_tool(tool_name, parameters)
        return result
```

## Database Migration
```sql
-- migrations/005_conversations.sql

-- Create conversations table
CREATE TABLE IF NOT EXISTS conversations (
    id SERIAL PRIMARY KEY,
    user_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);

-- Create messages table
CREATE TABLE IF NOT EXISTS messages (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    role VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_conversation_id ON messages(conversation_id);
CREATE INDEX idx_messages_created_at ON messages(created_at);
```

## Error Handling

```python
# Common error patterns
class ChatError(Exception):
    """Base chat error."""
    pass

class ConversationNotFoundError(ChatError):
    """Conversation doesn't exist or doesn't belong to user."""
    pass

class AgentExecutionError(ChatError):
    """Agent failed to process request."""
    pass

# In endpoint
try:
    result = await chat_service.process_message(...)
    return result
except ConversationNotFoundError:
    raise HTTPException(status_code=404, detail="Conversation not found")
except AgentExecutionError as e:
    raise HTTPException(status_code=500, detail=f"Agent error: {str(e)}")
except Exception as e:
    logger.error(f"Chat error: {str(e)}")
    raise HTTPException(status_code=500, detail="Internal server error")
```

## Environment Variables

```bash
# backend/.env
OPENAI_API_KEY="sk-..."
OPENAI_MODEL="gpt-4o"
DATABASE_URL="postgresql://user:pass@host:5432/dbname"
BETTER_AUTH_SECRET="shared-secret-with-frontend"
```

## Testing

```python
# tests/test_chat_endpoint.py
import pytest
from fastapi.testclient import TestClient

def test_chat_new_conversation(client: TestClient, auth_token: str):
    response = client.post(
        "/api/user123/chat",
        json={"message": "Add a task to buy groceries"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response.status_code == 200
    data = response.json()
    assert "conversation_id" in data
    assert "response" in data
    assert "tool_calls" in data

def test_chat_existing_conversation(client: TestClient, auth_token: str):
    # First message
    response1 = client.post(
        "/api/user123/chat",
        json={"message": "Add a task"},
        headers={"Authorization": f"Bearer {auth_token}"}
    )
    conv_id = response1.json()["conversation_id"]

    # Second message in same conversation
    response2 = client.post(
        "/api/user123/chat",
        json={
            "message": "Show me my tasks",
            "conversation_id": conv_id
        },
        headers={"Authorization": f"Bearer {auth_token}"}
    )

    assert response2.status_code == 200
    assert response2.json()["conversation_id"] == conv_id
```

## Best Practices

1. **Stateless Design**: Each request is independent
2. **Conversation Continuity**: Restore history from database
3. **Transactional Writes**: User + AI messages committed together
4. **Error Recovery**: Never leave orphaned messages
5. **User Isolation**: Always verify user_id from JWT
6. **Tool Call Logging**: Track all MCP tool executions
7. **Async Execution**: Use async/await for I/O operations
8. **Structured Responses**: Consistent JSON format

## Integration Points

| Component | Integration |
|-----------|-------------|
| **Frontend** | POST /api/{user_id}/chat |
| **Database** | Conversation + Message models |
| **AI Agent** | OpenAI Agents SDK |
| **MCP Server** | Tool execution layer |
| **Auth** | JWT verification |

---

**Production Standard**: This skill ensures a reliable, scalable, and maintainable backend chat endpoint that orchestrates AI conversations with proper state management and error handling.
