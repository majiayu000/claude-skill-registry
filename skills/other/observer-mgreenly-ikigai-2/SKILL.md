---
name: patterns/observer
description: Observer Pattern (Callbacks) pattern for C development
---

# Observer Pattern (Callbacks)

Objects register interest in events and get notified when they occur. In C, implemented as callback function pointers with context.

## ikigai Application

**Streaming chunks:** LLM client notifies REPL as response chunks arrive:
```c
typedef void (*chunk_callback_t)(void *ctx, const char *chunk, size_t len);
res_t ik_llm_stream(client, messages, on_chunk, user_ctx);
```

**Terminal resize:** Signal handler notifies REPL of SIGWINCH.

**Future uses:**
- Database change notifications
- Tool execution progress
- Background task completion

**Convention:** Always pair callback function pointer with `void *user_ctx` parameter.
