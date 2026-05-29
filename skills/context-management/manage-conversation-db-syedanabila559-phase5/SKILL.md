---
name: manage-conversation-db
description: This skill should be used when implementing stateless conversation persistence, creating/loading conversations by ID, saving user/assistant messages, fetching history for agent input, and handling async database queries.
---

# Manage Conversation DB Skill

This skill provides guidance for implementing conversation persistence in the database.

## Purpose

Handle stateless conversation persistence:
- Create/load conversation by ID
- Save user/assistant messages with role and content
- Fetch history for agent input
- Async queries for performance

## When to Use

Use this skill when:
- Implementing conversation storage layer
- Building message history retrieval
- Creating conversation management utilities
- Setting up async database operations for chat

## Capabilities

- **Conversation Lifecycle**: Create new or load existing conversations
- **Message Storage**: Save messages with role, content, and metadata
- **History Retrieval**: Fetch conversation messages in chronological order
- **Async Operations**: Non-blocking database queries
- **User Isolation**: Conversations tied to user_id

## Database Schema

```python
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from typing import Optional, List

class Conversation(SQLModel, table=True):
    id: str = Field(primary_key=True)
    user_id: str = Field(index=True)
    title: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    messages: List["Message"] = Relationship(back_populates="conversation")

class Message(SQLModel, table=True):
    id: int = Field(primary_key=True, autoincrement=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str = Field(index=True)  # "user", "assistant", "tool"
    content: str
    tool_name: Optional[str] = None
    tool_call_id: Optional[str] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    conversation: Optional[Conversation] = Relationship(back_populates="messages")
```

## Implementation Pattern

### Conversation Service

```python
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, desc

class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_or_create_conversation(
        self,
        conversation_id: Optional[str],
        user_id: str
    ) -> Conversation:
        """Get existing or create new conversation."""
        if conversation_id:
            result = await self.session.execute(
                select(Conversation).where(
                    Conversation.id == conversation_id,
                    Conversation.user_id == user_id
                )
            )
            conversation = result.scalar_one_or_none()
            if conversation:
                return conversation

        # Create new conversation
        conversation = Conversation(
            id=conversation_id or str(uuid.uuid4()),
            user_id=user_id,
            title="New Chat"
        )
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def save_message(
        self,
        conversation_id: str,
        role: str,
        content: str,
        tool_name: Optional[str] = None,
        tool_call_id: Optional[str] = None
    ) -> Message:
        """Save a message to the conversation."""
        message = Message(
            conversation_id=conversation_id,
            role=role,
            content=content,
            tool_name=tool_name,
            tool_call_id=tool_call_id
        )
        self.session.add(message)
        await self.session.commit()
        await self.session.refresh(message)
        return message

    async def get_conversation_history(
        self,
        conversation_id: str,
        user_id: str,
        limit: int = 50
    ) -> List[Message]:
        """Fetch conversation messages for agent input."""
        result = await self.session.execute(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .order_by(Message.created_at.asc())
            .limit(limit)
        )
        messages = result.scalars().all()

        # Verify user owns this conversation
        conv_result = await self.session.execute(
            select(Conversation).where(Conversation.id == conversation_id)
        )
        conversation = conv_result.scalar_one_or_none()
        if not conversation or conversation.user_id != user_id:
            raise PermissionError("Conversation not found")

        return messages

    async def save_conversation_messages(
        self,
        conversation_id: str,
        user_id: str,
        messages: List[dict]
    ) -> None:
        """Save multiple messages atomically."""
        for msg in messages:
            await self.save_message(
                conversation_id=conversation_id,
                role=msg["role"],
                content=msg["content"],
                tool_name=msg.get("tool_name"),
                tool_call_id=msg.get("tool_call_id")
            )

        # Update conversation timestamp
        await self.session.execute(
            select(Conversation)
            .where(Conversation.id == conversation_id)
        )
        # ... update updated_at
```

### Helper Functions

```python
async def build_message_array(
    db_messages: List[Message],
    user_message: str
) -> List[dict]:
    """Convert DB messages to agent input format."""
    message_array = [{"role": "system", "content": SYSTEM_PROMPT}]

    for msg in db_messages:
        message_array.append({
            "role": msg.role,
            "content": msg.content
        })

    message_array.append({
        "role": "user",
        "content": user_message
    })

    return message_array

def message_to_dict(message: Message) -> dict:
    """Convert Message to dictionary."""
    return {
        "id": message.id,
        "role": message.role,
        "content": message.content,
        "tool_name": message.tool_name,
        "tool_call_id": message.tool_call_id,
        "created_at": message.created_at.isoformat()
    }
```

## Async Session Management

```python
from contextlib import asynccontextmanager
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

@asynccontextmanager
async def get_db_session():
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
```

## Verification Checklist

- [ ] Conversations can be created and loaded by ID
- [ ] Messages saved with correct role and content
- [ ] History retrieved in chronological order
- [ ] User isolation enforced on conversations
- [ ] Async queries work without blocking
- [ ] Tool calls stored with metadata
