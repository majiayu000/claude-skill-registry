---
name: patterns/factory
description: Factory Pattern pattern for C development
---

# Factory Pattern

Function that encapsulates object creation, returning an allocated and initialized struct. Centralizes construction logic and hides allocation details from callers.

## ikigai Application

**Current usage:**
- `ik_scrollback_create()` - creates scrollback buffer
- `ik_mark_create()` - creates checkpoint marks
- `ik_input_parser_create()` - creates input parser

**Convention:** Use `*_create()` for heap allocation (caller owns), `*_init()` for initializing pre-allocated memory.

**With ik_env_t:** Factories should receive `ik_env_t *env` as first parameter for access to logger, config, and clock during construction.

**Testing:** Factories enable injecting dependencies at creation time rather than reaching for globals.
