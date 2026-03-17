---
name: patterns/arena-allocator
description: Arena Allocator Pattern (C-Specific) pattern for C development
---

# Arena Allocator Pattern (C-Specific)

Allocate many objects from single memory region, free all at once. No individual frees. Hierarchical arenas enable nested lifetimes.

## ikigai Application

**talloc:** ikigai uses talloc for hierarchical arenas:
```c
TALLOC_CTX *request_ctx = talloc_new(parent);
// All allocations are children
char *str = talloc_strdup(request_ctx, "hello");
ik_msg_t *msg = talloc(request_ctx, ik_msg_t);
// Single free cleans everything
talloc_free(request_ctx);
```

**Ownership hierarchy:**
```
root_ctx
  └─> repl_ctx
       └─> scrollback (freed with repl)
       └─> messages[] (freed with repl)
```

**Benefits:** No memory leaks by design. No use-after-free. Clear ownership. Fast bulk deallocation.

**See:** `project/memory.md` for talloc patterns.
