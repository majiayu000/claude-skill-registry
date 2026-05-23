---
name: patterns/command
description: Command Pattern pattern for C development
---

# Command Pattern

Encapsulate a request as an object, allowing parameterization, queuing, and undo. In C, a struct containing function pointer plus arguments.

## ikigai Application

**Slash commands:** Each command (`/clear`, `/mark`, `/rewind`) is a discrete operation:
```c
typedef struct {
    const char *name;
    res_t (*execute)(ik_repl_ctx_t *repl, const char *args);
    const char *help;
} ik_command_t;
```

**Input actions:** Parser emits action structs that REPL executes.

**Future uses:**
- Undo/redo stack for input editing
- Queued tool executions
- Macro recording and playback

**Benefit:** Commands become first-class, can be logged, serialized, or replayed.
