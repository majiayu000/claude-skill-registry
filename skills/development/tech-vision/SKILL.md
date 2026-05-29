---
name: Tech Vision
description: This skill should be used when the user asks about "tech direction", "architecture", "code patterns", "technical vision", "code quality", "module structure", "file organization", "code splitting", "architecture decisions", "technical debt", "performance patterns", or discusses establishing or reviewing technical direction. Provides architecture framework for code coherence.
version: 1.0.0
---

# Tech Vision

Establish and maintain technical coherence through architecture decisions and quality standards.

## Architecture Decision Records (ADRs)

Document significant decisions in `.studio/architecture/`:

```
.studio/architecture/
├── decisions.md         # Index
├── 001-ecs-over-oop.md
└── 002-rollback-state.md
```

Each ADR: Context → Decision → Consequences

## Module Organization

```
src/
├── core/       # Engine-level (input, render, audio)
├── game/       # Game-specific (player, enemy, world)
├── ui/         # User interface
└── shared/     # Cross-cutting (math, constants)
```

## File Size Limits (CRITICAL)

| Type | Soft | Hard | Action at Hard |
|------|------|------|----------------|
| Source code | 300 | 500 | Split into modules |
| Documentation | 500 | 1000 | Split into sections |
| Generated | 100 | 200 | External file + loader |

When approaching limits: identify subsections → extract → create interfaces → document split.

## Technical Pillars (Examples)

- "Deterministic execution for rollback"
- "Data-oriented for cache efficiency"
- "Fail-fast on invalid state"
- "No allocations in hot paths"

## Code Quality Standards

| Item | Convention |
|------|------------|
| Types | PascalCase |
| Functions | snake_case |
| Constants | SCREAMING_SNAKE |
| Modules | snake_case |

**Public API:** Brief description, examples for non-obvious.
**Private:** Explain "why" not "what".
**Errors:** Result for recoverable, panic for programming errors.

## ZX-Specific

**Rollback:** All game state deterministic, serializable, separable.

**Memory:**
- Game State: 256KB max
- Render State: 64KB max
- Audio State: 32KB max

**FFI:** Minimize and batch calls.

Store in `.studio/architecture/` and `.studio/creative-direction.md`.

## References

- **`references/module-patterns.md`** - Organization patterns
- **`references/file-splitting.md`** - When/how to split
- **`references/architecture-docs.md`** - Documentation templates
