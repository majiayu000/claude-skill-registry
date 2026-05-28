---
name: errors
description: Error Handling skill for the ikigai project
---

# Error Handling

## Three Mechanisms

| Mechanism | When | Compiles Out? |
|-----------|------|---------------|
| `res_t` | IO, parsing, external failures | No |
| `assert()` | Preconditions, contracts | Yes (-DNDEBUG) |
| `PANIC()` | OOM, corruption, impossible states | No |

## Decision Framework

1. **OOM?** → `PANIC()`
2. **Can happen with correct code?** → `res_t`
3. **Precondition/contract?** → `assert()`
4. **Impossible state?** → `PANIC()`

## Return Patterns

1. **res_t** - Failable operations (IO, parsing)
2. **Direct pointer** - Simple creation (PANICs on OOM)
3. **void** - Cannot fail
4. **Primitive** - Queries (size, bool checks)
5. **Raw pointer** - Into buffer (use `_ptr` suffix)
6. **Callback** - res_t for events, value for queries, void for side-effects

## Core Types

```c
typedef struct {
    union { void *ok; err_t *err; };
    bool is_err;
} res_t;

typedef struct err {
    err_code_t code;
    const char *file;
    int32_t line;
    char msg[256];
} err_t;
```

## Error Codes

| Code | Value | Usage |
|------|-------|-------|
| `OK` | 0 | Success/no error |
| `ERR_INVALID_ARG` | 1 | Invalid argument validation |
| `ERR_OUT_OF_RANGE` | 2 | Out of range values |
| `ERR_IO` | 3 | File operations, config loading |
| `ERR_PARSE` | 4 | JSON/protocol parsing |
| `ERR_DB_CONNECT` | 5 | Database connection failures |
| `ERR_DB_MIGRATE` | 6 | Database migration failures |
| `ERR_OUT_OF_MEMORY` | 7 | Memory allocation failures |
| `ERR_AGENT_NOT_FOUND` | 8 | Agent not found in array |
| `ERR_PROVIDER` | 9 | Provider error |
| `ERR_MISSING_CREDENTIALS` | 10 | Missing credentials |
| `ERR_NOT_IMPLEMENTED` | 11 | Not implemented |

## Macros

- `OK(value)` / `ERR(ctx, CODE, "msg", ...)` - Create results
- `TRY(expr)` - Extract value or return error
- `CHECK(res)` - Propagate error if failed
- `is_ok(&res)` / `is_err(&res)` - Inspect

## Assertions

**Build behavior:**
- `debug` build (default): asserts are **ACTIVE** → violation triggers `SIGABRT`
- `release` build (`-DNDEBUG`): asserts are **COMPILED OUT** → violation causes undefined behavior (segfault, corruption, etc.)

**We normally run debug builds.** When you see `assert(x)` fail, expect `SIGABRT`, not a segfault.

**Guidelines:**
- Mark with `// LCOV_EXCL_BR_LINE`
- Test both paths (pass + SIGABRT)
- Split compound assertions
- Assert side-effect free

## PANIC Usage

```c
// OOM - most common
if (ptr == NULL) PANIC("Out of memory");  // LCOV_EXCL_BR_LINE

// Switch default
default: PANIC("Invalid state");  // LCOV_EXCL_LINE

// Corruption
if (size > capacity) PANIC("Array corruption");  // LCOV_EXCL_LINE
```

## Trust Boundary

- **User input** → validate exhaustively with `res_t`, never crash
- **Internal functions** → `assert()` preconditions, trust caller validated

## Testing

- Assertions: `#ifndef NDEBUG` + `tcase_add_test_raise_signal(tc, test, SIGABRT)`
- PANIC: `tcase_add_test_raise_signal(tc, test, SIGABRT)` (all builds)
- OOM: Cannot be tested (process terminates)

## Coverage Exclusions

| Code | Marker |
|------|--------|
| Assertions | `// LCOV_EXCL_BR_LINE` |
| OOM checks | `// LCOV_EXCL_BR_LINE` |
| PANIC logic errors | `// LCOV_EXCL_LINE` |

New exclusions require updating `LCOV_EXCL_COVERAGE` in Makefile.

## Error Context Lifetime (Critical Rule)

**THE TRAP:** Errors allocated on a context that gets freed become use-after-free bugs.

```c
// BROKEN - error is allocated on foo, then foo is freed
res_t ik_foo_init(void *parent, foo_t **out) {
    foo_t *foo = talloc_zero_(parent, sizeof(foo_t));
    res_t result = ik_bar_init(foo, &foo->bar);  // Error allocated on foo
    if (is_err(&result)) {
        talloc_free(foo);  // FREES THE ERROR TOO!
        return result;     // USE-AFTER-FREE CRASH
    }
}
```

**THE FIX:** Error allocation context must survive the error's return. Either:

**Option A (Preferred):** Pass parent to sub-functions for error allocation:
```c
res_t ik_foo_init(void *parent, foo_t **out) {
    bar_t *bar = NULL;
    res_t result = ik_bar_init(parent, &bar);  // Error on parent - survives!
    if (is_err(&result)) return result;

    foo_t *foo = talloc_zero_(parent, sizeof(foo_t));
    talloc_steal(foo, bar);
    foo->bar = bar;
    *out = foo;
}
```

**Option B (Band-aid):** Reparent error before freeing context:
```c
res_t ik_foo_init(void *parent, foo_t **out) {
    foo_t *foo = talloc_zero_(parent, sizeof(foo_t));
    res_t result = ik_bar_init(foo, &foo->bar);
    if (is_err(&result)) {
        talloc_steal(parent, result.err);  // Save error to survivor
        talloc_free(foo);
        return result;
    }
}
```

**Rule:** When returning an error after freeing a context:
1. The error must be allocated on a context that survives the free
2. Prefer Option A (pass parent for error allocation)
3. Use Option B (talloc_steal) as fallback

**Reference:** See `fix.md` and `project/error_handling.md#error-context-lifetime-critical` for detailed analysis.

## References

Full details: `project/return_values.md`, `project/error_handling.md`, `project/error_patterns.md`, `project/error_testing.md`
