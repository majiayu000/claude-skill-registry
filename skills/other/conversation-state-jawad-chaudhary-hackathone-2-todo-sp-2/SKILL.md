---
name: conversation-state
description: Stateless conversation management with database-backed history, message persistence, and scalable architecture. Use when handling chat state, loading history, or building stateless APIs.
---

# Stateless Conversation State Management

## Load Conversation History
```python
async def load_conversation_history(
    session: AsyncSession,
    user_id: str,
    conversation_id: int | None
) -> tuple[Conversation, list[dict]]:
    """Load or create conversation with message history."""
    if conversation_id:
        stmt = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await session.execute(stmt)
        conversation = result.scalar_one_or_none()
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
    else:
        conversation = Conversation(user_id=user_id)
        session.add(conversation)
        await session.commit()
        await session.refresh(conversation)
    
    # Load messages
    stmt = select(Message).where(
        Message.conversation_id == conversation.id
    ).order_by(Message.created_at)
    result = await session.execute(stmt)
    db_messages = result.scalars().all()
    
    messages = [{"role": msg.role, "content": msg.content} for msg in db_messages]
    return conversation, messages
```

## Complete Stateless Flow
```python
@app.post("/api/{user_id}/chat")
async def chat(
    user_id: str,
    request: ChatRequest,
    session: AsyncSession = Depends(get_db_session),
    current_user: str = Depends(verify_jwt)
):
    # 1. Load history from DB
    conversation, messages = await load_conversation_history(
        session, user_id, request.conversation_id
    )
    
    # 2. Save user message
    user_msg = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="user",
        content=request.message
    )
    session.add(user_msg)
    await session.commit()
    
    # 3. Add to history array
    messages.append({"role": "user", "content": request.message})
    
    # 4. Run agent
    response, tool_calls = await run_agent(messages)
    
    # 5. Save assistant response
    assistant_msg = Message(
        user_id=user_id,
        conversation_id=conversation.id,
        role="assistant",
        content=response
    )
    session.add(assistant_msg)
    await session.commit()
    
    # 6. Return (server holds NO state)
    return ChatResponse(
        conversation_id=conversation.id,
        response=response,
        tool_calls=tool_calls
    )
```

## Benefits
- Horizontal scalability (any server handles any request)
- Resilience (server restart doesn't lose conversations)
- Testability (each request independent)
- No sticky sessions needed