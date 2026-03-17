---
name: patterns/chain-of-responsibility
description: Chain of Responsibility Pattern pattern for C development
---

# Chain of Responsibility Pattern

Pass request along a chain of handlers until one handles it. Each handler decides to process or pass to next. In C, linked list of handler functions.

## ikigai Application

**Input processing:** Bytes flow through: escape sequence detector → UTF-8 assembler → action mapper → REPL handler.

**Command dispatch:** Try slash command handlers in order until one matches.

**Future uses:**
- Middleware for tool execution (auth, logging, rate limiting)
- Message preprocessing pipeline
- Error recovery chain

**Implementation:**
```c
typedef res_t (*handler_fn)(void *ctx, request_t *req, handler_fn next);
```

**Benefit:** Add/remove processing steps without modifying existing handlers.
