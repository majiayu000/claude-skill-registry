---
name: patterns/facade
description: Facade Pattern pattern for C development
---

# Facade Pattern

Provides a simplified interface to a complex subsystem, hiding internal complexity behind a cohesive API. Clients interact with the facade rather than individual components.

## ikigai Application

**Primary facade:** `ik_repl_ctx_t` is a facade over:
- Terminal management (`ik_term_ctx_t`)
- Scrollback buffer (`ik_scrollback_t`)
- Input handling (`ik_input_buffer_t`)
- Layer rendering system
- LLM client interaction
- Conversation state

**User sees:** `ik_repl_init()`, `ik_repl_run()`, `ik_repl_cleanup()`

**Subsystems hidden:** Terminal raw mode, ANSI escapes, viewport calculations, streaming chunk assembly.

**Benefit:** Main only knows about REPL. REPL orchestrates everything else. Changes to internals don't affect main.
