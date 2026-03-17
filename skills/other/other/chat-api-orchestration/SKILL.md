---
name: chat-api-orchestration
description: |
  Implement single-endpoint chat API with deterministic request orchestration.
  This skill should be used when users need to create /api/{user_id}/chat endpoint,
  implement request validation, resolve conversation IDs, call agent runners,
  or design chat API contracts with structured responses.
---

# Chat API Orchestration

Guide for implementing a single-endpoint chat API with deterministic request flow.

## What This Skill Does

- Design `/api/{user_id}/chat` endpoint contract
- Implement deterministic 5-step request flow
- Validate incoming chat requests
- Resolve or create conversation_id
- Orchestrate agent runner calls
- Return structured responses

## What This Skill Does NOT Do

- Implement the agent/LLM logic itself
- Handle conversation persistence (see conversation-state-management skill)
- Manage authentication tokens (assumes auth exists)
- Deploy or scale the API

---

## Before Implementation

Gather context to ensure successful implementation:

| Source | Gather |
|--------|--------|
| **Codebase** | Existing routers, auth dependencies, error handling patterns |
| **Conversation** | User's agent runner interface, specific response fields needed |
| **Skill References** | API contract, request flow, error handling patterns |
| **User Guidelines** | Project conventions, existing schema patterns |

---

## Core Architecture

### Single Endpoint Design

```
POST /api/{user_id}/chat
     │
     ▼
┌─────────────────────────────────────────┐
│         DETERMINISTIC FLOW              │
│                                         │
│  1. Validate Request                    │
│  2. Authenticate User                   │
│  3. Resolve Conversation                │
│  4. Execute Agent                       │
│  5. Return Response                     │
│                                         │
└─────────────────────────────────────────┘
```

### Why Single Endpoint?

| Benefit | Description |
|---------|-------------|
| **Simplicity** | One URL to remember, one contract to maintain |
| **Stateless** | Each request is self-contained |
| **Idempotent design** | Can safely retry failed requests |
| **Clear ownership** | user_id in path ensures proper scoping |

---

## The 5-Step Deterministic Flow

Every request follows this exact sequence. No shortcuts, no variations.

```
┌─────────────────────────────────────────────────────────────┐
│ Step 1: VALIDATE REQUEST                                    │
│   • Check required fields (message)                         │
│   • Validate field types and constraints                    │
│   • Return 400 if invalid                                   │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 2: AUTHENTICATE USER                                   │
│   • Verify JWT from Authorization header                    │
│   • Extract user_id from token                              │
│   • Verify path user_id matches token user_id               │
│   • Return 401/403 if unauthorized                          │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 3: RESOLVE CONVERSATION                                │
│   • If conversation_id provided: load existing              │
│   • If not provided: create new conversation                │
│   • Verify conversation ownership                           │
│   • Return 404 if conversation not found                    │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 4: EXECUTE AGENT                                       │
│   • Build context from conversation history                 │
│   • Add user message to context                             │
│   • Call agent runner with context                          │
│   • Persist user message + agent response                   │
│   • Return 503 if agent fails                               │
└─────────────────────────────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│ Step 5: RETURN RESPONSE                                     │
│   • Format structured response                              │
│   • Include conversation_id for continuation                │
│   • Return 200 with ChatResponse                            │
└─────────────────────────────────────────────────────────────┘
```

---

## Implementation Workflow

### Step 1: Define Request/Response Schemas

See `references/api-contract.md` for complete schemas.

```python
# schemas/chat.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class ChatRequest(BaseModel):
    """Incoming chat request."""
    message: str = Field(..., min_length=1, max_length=10000)
    conversation_id: Optional[str] = Field(
        None,
        description="Existing conversation ID, or omit to create new"
    )
    model: Optional[str] = Field("gpt-4", description="Model to use")


class ChatResponse(BaseModel):
    """Chat API response."""
    conversation_id: str
    message: str
    role: str = "assistant"
    created_at: datetime
    usage: Optional[dict] = None
```

### Step 2: Create the Router

See `references/request-flow.md` for detailed implementation.

```python
# routers/chat.py
from fastapi import APIRouter, Depends, HTTPException, status

router = APIRouter(prefix="/api", tags=["chat"])


@router.post("/{user_id}/chat", response_model=ChatResponse)
async def chat(
    user_id: str,
    request: ChatRequest,
    current_user: AuthenticatedUser = Depends(get_current_user),
    session: Session = Depends(get_session),
    agent: AgentRunner = Depends(get_agent_runner)
):
    """
    Single chat endpoint with deterministic flow.

    1. Validate (handled by Pydantic)
    2. Authenticate (handled by dependency)
    3. Resolve conversation
    4. Execute agent
    5. Return response
    """
    # Step 2: Verify user_id matches authenticated user
    if user_id != current_user.user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot access another user's chat"
        )

    # Step 3: Resolve conversation
    conversation_id = await resolve_conversation(
        session=session,
        user_id=user_id,
        conversation_id=request.conversation_id
    )

    # Step 4: Execute agent
    response = await execute_agent(
        session=session,
        agent=agent,
        conversation_id=conversation_id,
        user_id=user_id,
        message=request.message,
        model=request.model
    )

    # Step 5: Return response
    return response
```

### Step 3: Implement Conversation Resolution

```python
# services/conversation.py
async def resolve_conversation(
    session: Session,
    user_id: str,
    conversation_id: Optional[str]
) -> str:
    """
    Resolve or create conversation.

    - If conversation_id provided: verify exists and owned by user
    - If not provided: create new conversation

    Returns: conversation_id (existing or new)
    """
    if conversation_id:
        # Load existing
        conv = get_conversation(session, conversation_id, user_id)
        if not conv:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        return conv.id
    else:
        # Create new
        conv = create_conversation(session, user_id=user_id)
        return conv.id
```

### Step 4: Implement Agent Execution

```python
# services/agent.py
async def execute_agent(
    session: Session,
    agent: AgentRunner,
    conversation_id: str,
    user_id: str,
    message: str,
    model: str
) -> ChatResponse:
    """
    Execute agent with conversation context.

    1. Load conversation history
    2. Add user message
    3. Call agent
    4. Persist response
    5. Return structured response
    """
    # Load context
    history = get_messages(session, conversation_id, user_id)
    context = [{"role": m.role, "content": m.content} for m in history]

    # Add user message
    add_message(session, conversation_id, user_id, "user", message)
    context.append({"role": "user", "content": message})

    try:
        # Call agent
        result = await agent.run(messages=context, model=model)

        # Persist response
        add_message(session, conversation_id, user_id, "assistant", result.content)

        return ChatResponse(
            conversation_id=conversation_id,
            message=result.content,
            role="assistant",
            created_at=datetime.now(timezone.utc),
            usage=result.usage
        )
    except AgentError as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Agent error: {str(e)}"
        )
```

---

## Error Handling

See `references/error-handling.md` for complete patterns.

| Step | Error | Status | Response |
|------|-------|--------|----------|
| 1. Validate | Invalid request | 400 | `{"detail": "Field X is required"}` |
| 2. Auth | Missing token | 401 | `{"detail": "Authentication required"}` |
| 2. Auth | Wrong user | 403 | `{"detail": "Cannot access another user's chat"}` |
| 3. Resolve | Conv not found | 404 | `{"detail": "Conversation not found"}` |
| 4. Execute | Agent fails | 503 | `{"detail": "Agent error: ..."}` |
| * | Unexpected | 500 | `{"detail": "Internal server error"}` |

---

## Idempotency Considerations

For safe retries, consider adding request deduplication:

```python
class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    request_id: Optional[str] = Field(
        None,
        description="Client-generated UUID for idempotency"
    )
```

If `request_id` was seen recently, return cached response instead of re-executing.

---

## Output Checklist

Before delivering implementation:

- [ ] ChatRequest schema with message, conversation_id, model
- [ ] ChatResponse schema with conversation_id, message, role, created_at
- [ ] POST /{user_id}/chat endpoint
- [ ] Path user_id validated against token user_id
- [ ] Conversation resolution (create or load)
- [ ] Agent execution with context
- [ ] Message persistence (user + assistant)
- [ ] Error handling for all 5 steps
- [ ] Consistent error response format

---

## Reference Files

| File | When to Read |
|------|--------------|
| `references/api-contract.md` | Complete request/response schemas and examples |
| `references/request-flow.md` | Detailed implementation of each step |
| `references/error-handling.md` | Error codes, formats, and recovery patterns |
