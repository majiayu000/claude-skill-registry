---
name: solid-ruby
description: SOLID principles for Ruby 3.3+ and Rails 8. Files < 100 lines, contracts separated, modular architecture. Modules MANDATORY.
versions:
  ruby: "3.3"
  rails: "8"
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/architecture-patterns.md, references/templates/module.md, references/templates/service.md, references/templates/contract.md, references/templates/model.md, references/templates/error.md, references/templates/test.md
related-skills: solid-detection
---

# SOLID Ruby - Modular Architecture

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Ruby/Rails docs via Context7
3. **fuse-ai-pilot:sniper** - Post-implementation validation

---

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. **Grep the codebase** for similar modules, services, or logic
2. Check shared locations: `app/modules/core/services/`, `app/modules/core/contracts/`
3. If similar code exists -> extend/reuse instead of duplicate
4. If code will be used by 2+ features -> create it in `app/modules/core/`

---

## Architecture (Modules MANDATORY)

| Layer | Location | Max Lines |
|-------|----------|-----------|
| Controllers | `app/modules/[feature]/controllers/` | 50 |
| Services | `app/modules/[feature]/services/` | 100 |
| Repositories | `app/modules/[feature]/repositories/` | 100 |
| Contracts | `app/modules/[feature]/contracts/` | 30 |
| Models | `app/modules/[feature]/models/` | 50 |
| Shared | `app/modules/core/{services,contracts,concerns}/` | - |

**NEVER use flat `app/` structure - always `app/modules/[feature]/`**

---

## Critical Rules (MANDATORY)

| Rule | Value |
|------|-------|
| File limit | 100 lines (split at 90) |
| Controllers | < 50 lines, delegate to services |
| Contracts | `contracts/` directory ONLY (duck typing modules) |
| YARD doc | Every public method documented |
| Frozen string | `# frozen_string_literal: true` in every file |
| Concerns | Use for shared behavior (like interfaces) |

---

## Reference Guide

### Concepts

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **SOLID Overview** | [solid-principles.md](references/solid-principles.md) | Quick reference |
| **SRP** | [single-responsibility.md](references/single-responsibility.md) | Fat classes |
| **OCP** | [open-closed.md](references/open-closed.md) | Adding strategies |
| **LSP** | [liskov-substitution.md](references/liskov-substitution.md) | Contracts |
| **ISP** | [interface-segregation.md](references/interface-segregation.md) | Fat modules |
| **DIP** | [dependency-inversion.md](references/dependency-inversion.md) | Injection |
| **Architecture** | [architecture-patterns.md](references/architecture-patterns.md) | Modular Rails |

### Templates

| Template | When to use |
|----------|-------------|
| [module.md](references/templates/module.md) | Feature module structure |
| [service.md](references/templates/service.md) | Business logic service |
| [contract.md](references/templates/contract.md) | Duck typing contracts |
| [model.md](references/templates/model.md) | Active Record model |
| [error.md](references/templates/error.md) | Custom exceptions |
| [test.md](references/templates/test.md) | RSpec tests |

---

## Forbidden

| Anti-Pattern | Fix |
|--------------|-----|
| Files > 100 lines | Split at 90 |
| Business logic in models | Extract to service |
| Fat controllers | Delegate to services |
| Flat `app/` structure | Use `app/modules/[feature]/` |
| God classes | Split by responsibility |
