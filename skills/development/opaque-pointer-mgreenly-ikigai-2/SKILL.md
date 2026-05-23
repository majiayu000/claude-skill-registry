---
name: patterns/opaque-pointer
description: Opaque Pointer Pattern pattern for C development
---

# Opaque Pointer Pattern

Declare struct in header without defining fields. Implementation hidden in .c file. Callers only see pointer, never fields.

## ikigai Application

**Header:**
```c
typedef struct ik_scrollback ik_scrollback_t;  // Forward declaration
res_t ik_scrollback_create(void *ctx, ik_scrollback_t **out);
```

**Implementation in .c:**
```c
struct ik_scrollback {
    // Fields hidden from callers
};
```

**Benefits:**
- Callers can't depend on internal fields
- Change internals without recompiling callers
- Enforces use of accessor functions

**ikigai usage:** Most context types could use this. Currently structs are defined in headers. Consider for stable public APIs.
