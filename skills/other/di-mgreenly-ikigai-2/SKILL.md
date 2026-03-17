---
name: di
description: Dependency Injection (DI) skill for the ikigai project
---

# Dependency Injection (DI)

## Core Concept

**Dependency Injection** - Pass dependencies to a module from the outside rather than having the module create or locate them internally.

Instead of:
```c
void repl_init() {
    config = load_config();      // Hidden dependency - where does it load from?
    db = connect_database();     // Hidden dependency - what connection string?
    llm = create_llm_client();   // Hidden dependency - which API key?
}
```

Do this:
```c
void repl_init(config_t *cfg, db_t *db, llm_t *llm) {
    // Dependencies are explicit - passed from caller
    // This function doesn't know or care where they came from
}
```

## Why DI Matters

**Explicit Dependencies** - Function signature reveals what it needs. No hidden file I/O, global state, or magic.

**Testability** - Pass mock/fake implementations in tests. Real implementations in production.

**Composability** - Modules become building blocks. Wire them together differently for different contexts.

**No Global State** - Eliminates hidden coupling. Multiple instances can coexist with different configs.

**Clear Ownership** - Caller controls lifecycle. Knows when dependencies are created and destroyed.

## How ikigai Uses DI

### Pattern 1: Explicit Constructor Injection

Main creates all dependencies, passes them down:

```c
// From v1-architecture.md
int main(void) {
    void *root_ctx = talloc_new(NULL);

    // Load config
    ik_cfg_t *cfg = NULL;
    TRY(ik_cfg_load(root_ctx, "~/.ikigai/config.json", &cfg));

    // Initialize database with config
    ik_db_ctx_t *db = NULL;
    TRY(ik_db_init(root_ctx, cfg->db_connection_string, &db));

    // Initialize LLM client with config
    ik_llm_client_t *llm = NULL;
    TRY(ik_llm_init(root_ctx, cfg->openai_api_key, &llm));

    // Initialize REPL - receives all dependencies
    ik_repl_ctx_t *repl = NULL;
    TRY(ik_repl_init(root_ctx, cfg, db, llm, &repl));

    // Run
    ik_repl_run(repl);

    talloc_free(root_ctx);
    return 0;
}
```

**Key insight:** `main()` is the composition root. It knows the full dependency graph. Everything else just receives what it needs.

### Pattern 2: Context Parameter

First parameter is always the talloc context:

```c
// Config loading
res_t ik_cfg_load(TALLOC_CTX *ctx, const char *path, ik_cfg_t **out_cfg);

// Database init
res_t ik_db_init(TALLOC_CTX *ctx, const char *conn_str, ik_db_ctx_t **out_db);

// REPL init
res_t ik_repl_init(TALLOC_CTX *ctx, ik_cfg_t *cfg, ik_db_ctx_t *db,
                   ik_llm_client_t *llm, ik_repl_ctx_t **out_repl);
```

**Benefits:**
- Caller controls memory lifetime
- Clear ownership hierarchy
- No hidden malloc() calls
- Everything hangs off root_ctx

### Pattern 3: Struct Composition

REPL context holds injected dependencies:

```c
struct ik_repl_ctx_t {
    ik_cfg_t *cfg;              // Injected config
    ik_db_ctx_t *db;            // Injected database
    ik_llm_client_t *llm;       // Injected LLM client

    ik_term_ctx_t *term;        // Created internally
    ik_scrollback_t *scrollback;// Created internally
    ik_input_buffer_t *input;   // Created internally

    // ... other fields
};
```

**Two types of dependencies:**
1. **External** (cfg, db, llm) - Created before REPL, injected in
2. **Internal** (term, scrollback, input) - REPL owns, creates during init

## DI for Testing

### Production Code
```c
// production main.c
int main(void) {
    ik_llm_client_t *llm = ik_llm_init(ctx, real_api_key);
    ik_repl_init(ctx, cfg, db, llm, &repl);
    // Uses real OpenAI API
}
```

### Test Code
```c
// test_repl.c
void test_repl_handles_llm_error(void) {
    ik_llm_client_t *mock_llm = create_mock_llm_that_fails();
    ik_repl_init(ctx, cfg, db, mock_llm, &repl);
    // Uses mock that returns errors - no real API calls
}
```

**Key:** Same `ik_repl_init()` function works with real or mock dependencies.

## Anti-Patterns to Avoid

**Service Locator** - Global registry of dependencies:
```c
// BAD - hidden dependency
void repl_init() {
    llm_client_t *llm = service_locator_get("llm");  // Where did this come from?
}
```

**Singleton** - Global static instance:
```c
// BAD - global state
static config_t *g_config = NULL;

void repl_init() {
    const char *key = g_config->api_key;  // Hidden dependency on global
}
```

**Constructor Does I/O** - Function creates its own dependencies:
```c
// BAD - hidden file I/O
void repl_init() {
    config = load_config_from_disk();  // Which file? Can't test without filesystem
}
```

**Null Checking Injected Deps** - Don't do this:
```c
// BAD - dependency is required, why allow NULL?
void repl_init(config_t *cfg, db_t *db, llm_t *llm) {
    if (!cfg || !db || !llm) {
        PANIC("Missing dependencies");  // If they're required, assert it
    }
}
```

Use assertions for required dependencies:
```c
// GOOD - document requirements
void repl_init(config_t *cfg, db_t *db, llm_t *llm) {
    assert(cfg != NULL);
    assert(db != NULL);
    assert(llm != NULL);
    // Proceed knowing dependencies exist
}
```

## DI in C vs OOP Languages

**No interfaces** - C doesn't have interfaces. Use function pointers in structs for polymorphism:
```c
typedef struct {
    res_t (*send)(void *ctx, message_t *msg);
    res_t (*stream)(void *ctx, message_t *msg, chunk_callback_t cb);
} llm_provider_vtable_t;

typedef struct {
    llm_provider_vtable_t *vtable;
    void *impl_ctx;  // OpenAI context, Anthropic context, etc.
} llm_client_t;
```

**No frameworks** - No Spring, no Guice. Composition happens in `main()`. Simple and explicit.

**Manual wiring** - You write the composition logic. More code, but totally transparent.

## Rules for ikigai

1. **main() is composition root** - Creates all top-level dependencies, wires them together
2. **First param is TALLOC_CTX** - Explicit memory ownership
3. **Pass dependencies as function parameters** - Never load/create internally
4. **Modules don't know about config files** - Config is loaded once, values passed down
5. **No global state** - Everything owned by talloc hierarchy
6. **Assert required dependencies** - Don't defensively check for NULL if it's a contract violation

## Summary

**Dependency Injection** = Pass dependencies in, don't create them internally.

**Benefits:**
- Explicit dependencies (no surprises)
- Testable (mock dependencies)
- Composable (wire differently for different needs)
- No global state (multiple instances possible)
- Clear ownership (caller controls lifecycle)

**In ikigai:** main() creates config, database, LLM client. Passes them to REPL. REPL doesn't know where they came from. Easy to test with mocks. No hidden file I/O or global state.
