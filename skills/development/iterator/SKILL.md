---
name: patterns/iterator
description: Iterator Pattern pattern for C development
---

# Iterator Pattern

Provide sequential access to collection elements without exposing underlying structure. In C, typically a struct with `next()` function or index-based traversal.

## ikigai Application

**Scrollback traversal:** Iterate visible lines for rendering without exposing ring buffer internals.

**Message iteration:** Walk session messages for LLM context building.

**Implementation options:**
```c
// Index-based (simple)
for (size_t i = 0; i < scrollback->count; i++) { ... }

// Iterator struct (encapsulated)
ik_iter_t *iter = ik_scrollback_iter(scrollback);
while (ik_iter_next(iter, &line)) { ... }
```

**Current approach:** Index-based iteration is sufficient. Iterator struct adds value when traversal logic is complex or needs to hide internals.
