---
name: patterns/callback-context
description: Callback + Context Pattern (C-Specific) pattern for C development
---

# Callback + Context Pattern (C-Specific)

Pair function pointer with `void *` user data. Callback receives user data, enabling state access without globals. Universal C pattern for async/event handling.

## ikigai Application

**Streaming responses:**
```c
typedef void (*chunk_cb_t)(void *user_ctx, const char *data, size_t len);

res_t ik_llm_stream(ik_llm_client_t *client,
                    ik_message_t **msgs,
                    chunk_cb_t on_chunk,
                    void *user_ctx);  // Passed to callback
```

**Usage:** REPL passes itself as context, callback updates scrollback.

**Convention:** Callback function pointer immediately followed by `void *` context parameter. Callback signature includes context as first param.

**Benefit:** Stateful callbacks without globals. Each caller provides own context.
