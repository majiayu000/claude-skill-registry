---
name: gleam
description: Develop with Gleam using idiomatic patterns, TDD, and type-driven design. Activate when working with .gleam files, gleam.toml, or user mentions Gleam, BEAM, or Erlang.
---

# Gleam Development

Idiomatic Gleam with **type-driven design** and **TDD**.

## Workflow

```
1. MODEL    → Define domain types first (make illegal states unrepresentable)
2. RED      → Write failing test
3. GREEN    → Minimal implementation
4. REFACTOR → Clean up, use pipelines
5. RUN      → gleam test && gleam run
```

## Research

Use Context7 `query-docs` first, then gh as fallback. Routing table and example queries live in `reference.md`.

## CLI

```bash
gleam check                    # Fast type feedback (use often)
gleam test                     # Run tests
gleam run                      # Execute main
gleam format                   # Format all
gleam add pkg --dev            # Dev dependency
```

## References

- [reference.md](reference.md) - Research routing, patterns, anti-patterns
