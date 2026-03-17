---
name: chat-api-integration
description: DEPRECATED - Use chatkit-backend skill instead. Chat API functionality is now part of the chatkit-backend skill.
allowed-tools: Bash, Write, Read, Edit, Glob
deprecated: true
---

# Chat API Integration (DEPRECATED)

> **This skill has been deprecated and consolidated into `chatkit-backend`.**
>
> Please use the `chatkit-backend` skill instead for all chat API implementation.

## Migration

Use the consolidated skill:

```
.claude/skills/chatkit-backend/SKILL.md
```

The `chatkit-backend` skill includes:
- Complete `/chatkit` SSE endpoint for ChatKit frontend
- Conversation and Message models with SQLModel
- Get or create conversation logic
- Load conversation history for agent context
- Store user messages and assistant responses
- ChatKit-compatible SSE streaming format
- Agent execution and tool call handling
- Conversation CRUD endpoints
- Comprehensive examples

## See Also

- [chatkit-backend](../chatkit-backend/SKILL.md) - **USE THIS INSTEAD**
- [chatkit-frontend](../chatkit-frontend/SKILL.md) - Frontend ChatKit setup
