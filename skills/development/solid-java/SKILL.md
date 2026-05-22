---
name: solid-java
description: SOLID principles for Java 21+. Files < 100 lines, interfaces separated, modular architecture. Modules MANDATORY.
versions:
  java: "21"
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/architecture-patterns.md, references/templates/module.md, references/templates/service.md, references/templates/interface.md, references/templates/repository.md, references/templates/error.md, references/templates/test.md
related-skills: solid-detection
---

# SOLID Java - Modular Architecture

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Java docs via Context7
3. **fuse-ai-pilot:sniper** - Post-implementation validation

---

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. **Grep the codebase** for similar interfaces, services, or logic
2. Check shared locations: `modules/core/services/`, `modules/core/interfaces/`
3. If similar code exists -> extend/reuse instead of duplicate
4. If code will be used by 2+ features -> create it in `modules/core/`

---

## Architecture (Modules MANDATORY)

| Layer | Location | Max Lines |
|-------|----------|-----------|
| Controllers | `modules/[feature]/controllers/` | 50 |
| Services | `modules/[feature]/services/` | 100 |
| Repositories | `modules/[feature]/repositories/` | 100 |
| Interfaces | `modules/[feature]/interfaces/` | 30 |
| Models/DTOs | `modules/[feature]/models/` | 50 |
| Shared | `modules/core/{services,interfaces,models}/` | - |

**NEVER use flat `src/` structure - always `modules/[feature]/`**

---

## Critical Rules (MANDATORY)

| Rule | Value |
|------|-------|
| File limit | 100 lines (split at 90) |
| Controllers | < 50 lines, delegate to services |
| Interfaces | `modules/[feature]/interfaces/` ONLY |
| Javadoc | Every public method documented |
| Records | Use for DTOs (Java 16+) |
| Sealed | Use for restricted hierarchies (Java 17+) |

---

## Reference Guide

### Concepts

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **SOLID Overview** | [solid-principles.md](references/solid-principles.md) | Quick reference |
| **SRP** | [single-responsibility.md](references/single-responsibility.md) | Fat classes |
| **OCP** | [open-closed.md](references/open-closed.md) | Adding providers |
| **LSP** | [liskov-substitution.md](references/liskov-substitution.md) | Contracts |
| **ISP** | [interface-segregation.md](references/interface-segregation.md) | Fat interfaces |
| **DIP** | [dependency-inversion.md](references/dependency-inversion.md) | Injection |
| **Architecture** | [architecture-patterns.md](references/architecture-patterns.md) | Modular patterns |

### Templates

| Template | When to use |
|----------|-------------|
| [module.md](references/templates/module.md) | Feature module structure |
| [service.md](references/templates/service.md) | Business logic service |
| [interface.md](references/templates/interface.md) | Contract definition |
| [repository.md](references/templates/repository.md) | Data access layer |
| [error.md](references/templates/error.md) | Custom exceptions |
| [test.md](references/templates/test.md) | Unit tests with mocks |

---

## Forbidden

| Anti-Pattern | Fix |
|--------------|-----|
| Files > 100 lines | Split at 90 |
| Interfaces in impl files | Move to `interfaces/` directory |
| `new ConcreteClass()` in services | Use dependency injection |
| Flat `src/` structure | Use `modules/[feature]/` |
| God classes | Split by responsibility |
