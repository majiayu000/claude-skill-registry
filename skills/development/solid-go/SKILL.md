---
name: solid-go
description: SOLID principles for Go 1.23+. Files < 100 lines, interfaces separated, modular architecture. Modules MANDATORY.
versions:
  go: "1.23"
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/architecture-patterns.md, references/templates/module.md, references/templates/service.md, references/templates/interface.md, references/templates/handler.md, references/templates/error.md, references/templates/test.md
related-skills: solid-detection
---

# SOLID Go - Modular Architecture

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Go docs via Context7
3. **fuse-ai-pilot:sniper** - Post-implementation validation

---

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. **Grep the codebase** for similar interfaces, services, or logic
2. Check shared locations: `internal/core/services/`, `internal/core/ports/`
3. If similar code exists -> extend/reuse instead of duplicate
4. If code will be used by 2+ features -> create it in `internal/core/`

---

## Architecture (Modules MANDATORY)

| Layer | Location | Max Lines |
|-------|----------|-----------|
| Handlers | `internal/modules/[feature]/handlers/` | 50 |
| Services | `internal/modules/[feature]/services/` | 100 |
| Repositories | `internal/modules/[feature]/repositories/` | 100 |
| Ports (interfaces) | `internal/modules/[feature]/ports/` | 30 |
| Models | `internal/modules/[feature]/models/` | 50 |
| Shared | `internal/core/{services,ports,models}/` | - |

**NEVER use flat `internal/` structure - always `internal/modules/[feature]/`**

---

## Critical Rules (MANDATORY)

| Rule | Value |
|------|-------|
| File limit | 100 lines (split at 90) |
| Handlers | < 50 lines, delegate to services |
| Interfaces | `ports/` directory ONLY |
| Godoc | Every exported function documented |
| Accept interfaces | Return structs |
| Small interfaces | 1-3 methods max (Go idiom) |

---

## Reference Guide

### Concepts

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **SOLID Overview** | [solid-principles.md](references/solid-principles.md) | Quick reference |
| **SRP** | [single-responsibility.md](references/single-responsibility.md) | Fat structs |
| **OCP** | [open-closed.md](references/open-closed.md) | Adding providers |
| **LSP** | [liskov-substitution.md](references/liskov-substitution.md) | Contracts |
| **ISP** | [interface-segregation.md](references/interface-segregation.md) | Fat interfaces |
| **DIP** | [dependency-inversion.md](references/dependency-inversion.md) | Injection |
| **Architecture** | [architecture-patterns.md](references/architecture-patterns.md) | Hex/modular |

### Templates

| Template | When to use |
|----------|-------------|
| [module.md](references/templates/module.md) | Feature module structure |
| [service.md](references/templates/service.md) | Business logic service |
| [interface.md](references/templates/interface.md) | Port definition |
| [handler.md](references/templates/handler.md) | HTTP handler |
| [error.md](references/templates/error.md) | Custom errors |
| [test.md](references/templates/test.md) | Table-driven tests |

---

## Forbidden

| Anti-Pattern | Fix |
|--------------|-----|
| Files > 100 lines | Split at 90 |
| Interfaces in impl files | Move to `ports/` directory |
| Fat interfaces (4+ methods) | Split into small interfaces |
| Flat `internal/` structure | Use `internal/modules/[feature]/` |
| `init()` for dependency wiring | Use constructor injection |
