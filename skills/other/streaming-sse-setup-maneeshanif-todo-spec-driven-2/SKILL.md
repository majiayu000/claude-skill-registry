---
name: streaming-sse-setup
description: DEPRECATED - Use chatkit-backend skill instead. SSE streaming is now part of the chatkit-backend skill for ChatKit integration.
allowed-tools: Bash, Write, Read, Edit, Glob
deprecated: true
---

# Streaming SSE Setup (DEPRECATED)

> **This skill has been deprecated and consolidated into `chatkit-backend`.**
>
> Please use the `chatkit-backend` skill instead for all SSE streaming implementation.

## Migration

Use the consolidated skill:

```
.claude/skills/chatkit-backend/SKILL.md
```

The `chatkit-backend` skill includes:
- Complete SSE streaming endpoint for ChatKit
- ChatKit-compatible SSE event format (text, tool_call, tool_result, done)
- Conversation and Message model persistence
- AI agent integration with streaming
- Response chunking for natural UX
- Error handling with SSE error events
- Comprehensive examples

## See Also

- [chatkit-backend](../chatkit-backend/SKILL.md) - **USE THIS INSTEAD**
- [chatkit-frontend](../chatkit-frontend/SKILL.md) - Frontend ChatKit setup
