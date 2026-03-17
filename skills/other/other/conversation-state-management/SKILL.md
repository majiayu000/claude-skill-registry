---
name: conversation-state-management
description: |
  Implement DB-persisted conversation state for stateless AI agent servers.
  This skill should be used when users need to create/load conversations,
  append messages with role ordering, fetch history for agents, or resume
  conversations after server restart.
---

# Conversation State Management

Guide for implementing stateless server conversation persistence with Neon PostgreSQL.

## What This Skill Does

- Design conversation and message data models
- Implement create/load conversation operations
- Enforce message role ordering (system → user ↔ assistant)
- Fetch full history for agent context
- Resume conversations after server restart
- User-scoped conversation isolation

## What This Skill Does NOT Do

- Implement LLM/AI provider integration
- Handle authentication (assumes auth exists)
- Manage token counting or context window truncation
- Deploy database infrastructure

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing models, database.py, CRUD patterns, router structure |
| **Conversation** | User's specific table naming, additional fields needed |
| **Skill References** | Data models, API patterns, role ordering rules |
| **User Guidelines** | Project conventions, existing auth patterns |

---

## Core Architecture

### Stateless Server Principle

```
Request → Load full conversation from DB → Process → Persist → Response
           ↑                                           ↓
           └──────── No in-memory state ───────────────┘
```

Each request is independent. Server instances are interchangeable.

### Three-Table Architecture

| Table | Purpose | Key Fields |
|-------|---------|------------|
| **users** | Identity (from auth) | id, email |
| **conversations** | Session metadata | id, user_id, title, system_prompt, created_at |
| **messages** | Individual messages | id, conversation_id, role, content, created_at |

---

## Implementation Workflow

### 1. Create Data Models

See `references/data-models.md` for complete SQLModel definitions.

```python
# models/conversation.py
class Conversation(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(foreign_key="user.id", index=True)
    title: str | None = None
    system_prompt: str | None = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

class Message(SQLModel, table=True):
    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    conversation_id: str = Field(foreign_key="conversation.id", index=True)
    role: str  # 'system', 'user', 'assistant'
    content: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
```

### 2. Create CRUD Operations

See `references/api-patterns.md` for complete implementations.

**Essential operations:**
- `create_conversation(user_id, title?, system_prompt?)`
- `get_conversation(conversation_id, user_id)` - with ownership check
- `list_conversations(user_id, skip, limit)`
- `add_message(conversation_id, user_id, role, content)` - with role validation
- `get_messages(conversation_id, user_id)` - ordered by created_at
- `delete_conversation(conversation_id, user_id)`

### 3. Enforce Role Ordering

See `references/role-ordering.md` for validation logic.

**Rules:**
- System message: only at start, max 1
- After system (if any): strict user ↔ assistant alternation
- No consecutive same-role messages

```python
def validate_role_sequence(messages: list[Message], new_role: str) -> bool:
    if not messages:
        return new_role in ('system', 'user')

    last_role = messages[-1].role

    if new_role == 'system':
        return False  # System only at start

    if last_role == 'system':
        return new_role == 'user'

    # Must alternate user ↔ assistant
    return (last_role == 'user' and new_role == 'assistant') or \
           (last_role == 'assistant' and new_role == 'user')
```

### 4. Implement API Endpoints

```python
# routers/conversations.py
@router.post("/conversations")
async def create_conversation(data: ConversationCreate, user: AuthUser):
    return crud.create_conversation(user_id=user.id, **data.model_dump())

@router.get("/conversations/{id}")
async def get_conversation(id: str, user: AuthUser):
    conv = crud.get_conversation(id, user_id=user.id)
    if not conv:
        raise HTTPException(404, "Conversation not found")
    return conv

@router.post("/conversations/{id}/messages")
async def add_message(id: str, data: MessageCreate, user: AuthUser):
    # Validates role ordering internally
    return crud.add_message(id, user_id=user.id, **data.model_dump())

@router.get("/conversations/{id}/messages")
async def get_messages(id: str, user: AuthUser):
    return crud.get_messages(id, user_id=user.id)
```

### 5. Resume Pattern

See `references/resume-patterns.md` for checkpoint strategies.

```python
def get_conversation_context(conversation_id: str, user_id: str) -> list[dict]:
    """Fetch full history formatted for LLM."""
    messages = crud.get_messages(conversation_id, user_id)
    return [{"role": m.role, "content": m.content} for m in messages]

# On resume, simply load and continue
@router.post("/conversations/{id}/continue")
async def continue_conversation(id: str, data: MessageCreate, user: AuthUser):
    # Load existing context
    context = get_conversation_context(id, user.id)

    # Add new user message
    crud.add_message(id, user.id, role="user", content=data.content)
    context.append({"role": "user", "content": data.content})

    # Call LLM with full context
    response = await llm.generate(messages=context)

    # Persist assistant response
    crud.add_message(id, user.id, role="assistant", content=response)

    return {"response": response}
```

---

## Stateless Request Cycle

```
1. Authenticate request (JWT/session)
2. Load conversation from DB (includes all messages)
3. Validate operation (ownership, role ordering)
4. Execute operation (add message, call LLM)
5. Persist changes to DB
6. Return response
7. Connection closed (no state retained)
```

**Key principle**: Any server instance can handle any request.

---

## User Isolation

Always filter by user_id at the data layer:

```python
def get_conversation(conversation_id: str, user_id: str) -> Conversation | None:
    statement = select(Conversation).where(
        Conversation.id == conversation_id,
        Conversation.user_id == user_id  # Ownership check
    )
    return session.exec(statement).first()
```

Return 404 (not 403) when conversation exists but belongs to another user.

---

## Output Checklist

Before delivering implementation:

- [ ] Conversation model with user_id foreign key
- [ ] Message model with conversation_id foreign key and role field
- [ ] Role enum/validation (system, user, assistant)
- [ ] Role ordering validation before insert
- [ ] User ownership check on all operations
- [ ] Messages ordered by created_at
- [ ] CRUD: create, get, list, add_message, get_messages, delete
- [ ] API endpoints with auth dependency
- [ ] No in-memory conversation state

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/data-models.md` | Complete SQLModel/Pydantic definitions |
| `references/api-patterns.md` | CRUD operations and router implementations |
| `references/role-ordering.md` | Role validation logic and edge cases |
| `references/resume-patterns.md` | Checkpoint and continuation strategies |
