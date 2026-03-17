---
name: solid-php
description: SOLID principles for Laravel 12 and PHP 8.5. Files < 100 lines, interfaces separated, PHPDoc mandatory. Auto-detects Laravel and FuseCore architecture.
versions:
  laravel: "12.46"
  php: "8.5"
user-invocable: true
references: references/solid-principles.md, references/single-responsibility.md, references/open-closed.md, references/liskov-substitution.md, references/interface-segregation.md, references/dependency-inversion.md, references/anti-patterns.md, references/decision-guide.md, references/php85-features.md, references/laravel12-structure.md, references/fusecore-structure.md, references/templates/code-templates.md, references/templates/controller-templates.md, references/templates/refactoring-guide.md
related-skills: laravel-architecture, fusecore
---

# SOLID PHP - Laravel 12 + PHP 8.5

## Agent Workflow (MANDATORY)

Before ANY implementation, use `TeamCreate` to spawn 3 agents:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Laravel/PHP docs via Context7
3. **mcp__context7__query-docs** - Check SOLID patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. **Grep the codebase** for similar class names, methods, or logic
2. Check shared locations: `FuseCore/Core/App/Services/`, `FuseCore/Core/App/Traits/`, `FuseCore/[Module]/App/Contracts/`
3. If similar code exists → extend/reuse instead of duplicate
4. If code will be used by 2+ features → create it in shared Services or Traits
5. Extract repeated logic (3+ occurrences) into shared helpers or Traits
6. Verify no duplication introduced after writing

---

## Auto-Detection (Modular MANDATORY)

| Files Detected | Architecture | Interfaces Location |
|----------------|--------------|---------------------|
| `FuseCore/` directory | FuseCore Modular | `FuseCore/[Module]/App/Contracts/` |
| `module.json` in modules | FuseCore Modular | `FuseCore/[Module]/App/Contracts/` |

**Verification**: `php artisan --version` → Laravel 12.x
**Structure**: Always FuseCore modular. Shared in `FuseCore/Core/App/`.

---

## Decision Tree: Where to Put Code? (FuseCore Modular)

```
New code needed?
├── HTTP validation → FuseCore/[Module]/App/Http/Requests/
├── Single action → FuseCore/[Module]/App/Actions/
├── Business logic → FuseCore/[Module]/App/Services/
├── Data access → FuseCore/[Module]/App/Repositories/
├── Data transfer → FuseCore/[Module]/App/DTOs/
├── Interface → FuseCore/[Module]/App/Contracts/
├── Event → FuseCore/[Module]/App/Events/
└── Authorization → FuseCore/[Module]/App/Policies/
```

---

## Decision Tree: Which Pattern?

| Need | Pattern | Location | Max Lines |
|------|---------|----------|-----------|
| HTTP handling | Controller | Controllers/ | 50 |
| Validation | FormRequest | Requests/ | 50 |
| Single operation | Action | Actions/ | 50 |
| Complex logic | Service | Services/ | 100 |
| Data access | Repository | Repositories/ | 100 |
| Data structure | DTO | DTOs/ | 50 |
| Abstraction | Interface | Contracts/ | 30 |

---

## Critical Rules (MANDATORY)

### 1. Files < 100 lines
- **Split at 90 lines** - Never exceed 100
- Controllers < 50 lines
- Models < 80 lines (excluding relations)
- Services < 100 lines

### 2. Interfaces Separated (FuseCore Modular MANDATORY)
```
FuseCore/[Module]/App/Contracts/   # Module interfaces ONLY
├── UserRepositoryInterface.php
└── PaymentGatewayInterface.php
FuseCore/Core/App/Contracts/       # Shared interfaces
```

### 3. PHPDoc Mandatory
```php
/**
 * Create a new user from DTO.
 *
 * @param CreateUserDTO $dto User data transfer object
 * @return User Created user model
 * @throws ValidationException If email already exists
 */
public function create(CreateUserDTO $dto): User
```

---

## Reference Guide

### Concepts

| Topic | Reference | When to consult |
|-------|-----------|-----------------|
| **SOLID Overview** | [solid-principles.md](references/solid-principles.md) | Quick reference all principles |
| **SRP** | [single-responsibility.md](references/single-responsibility.md) | File too long, fat controller/model |
| **OCP** | [open-closed.md](references/open-closed.md) | Adding payment methods, channels |
| **LSP** | [liskov-substitution.md](references/liskov-substitution.md) | Interface contracts, swapping providers |
| **ISP** | [interface-segregation.md](references/interface-segregation.md) | Fat interfaces, unused methods |
| **DIP** | [dependency-inversion.md](references/dependency-inversion.md) | Tight coupling, testing, mocking |
| **Anti-Patterns** | [anti-patterns.md](references/anti-patterns.md) | Code smells detection |
| **Decisions** | [decision-guide.md](references/decision-guide.md) | Pattern selection |
| **PHP 8.5** | [php85-features.md](references/php85-features.md) | Modern PHP features |
| **Structure** | [laravel12-structure.md](references/laravel12-structure.md) | Standard Laravel |
| **FuseCore** | [fusecore-structure.md](references/fusecore-structure.md) | Modular architecture |

### Templates

| Template | When to use |
|----------|-------------|
| [code-templates.md](references/templates/code-templates.md) | Service, DTO, Repository, Interface |
| [controller-templates.md](references/templates/controller-templates.md) | Controller, Action, FormRequest, Policy |
| [refactoring-guide.md](references/templates/refactoring-guide.md) | Step-by-step migration from legacy code |

---

## Forbidden

| Anti-Pattern | Detection | Fix |
|--------------|-----------|-----|
| Files > 100 lines | Line count | Split into smaller files |
| Controllers > 50 lines | Line count | Extract to Service |
| Interfaces in impl files | Location | Move to `FuseCore/[Module]/App/Contracts/` |
| Business logic in Models | Code in model | Extract to Service |
| Concrete dependencies | `new Class()` | Inject via ModuleServiceProvider |
| Missing PHPDoc | No doc block | Add documentation |
| Missing strict_types | No declare | Add to all files |
| Fat classes | > 5 public methods | Split responsibilities |
| Duplicated logic | Same code in 2+ files | Extract to Service/Trait |
| No Grep before coding | Creating without search | Grep codebase first |

---

## Best Practices

| DO | DON'T |
|----|-------|
| Use constructor property promotion | Use property assignment |
| Depend on interfaces | Depend on concrete classes |
| Use `final readonly class` | Use mutable classes |
| Use `declare(strict_types=1)` | Skip type declarations |
| Split at 90 lines | Wait until 100 lines |
| Use DTOs for data transfer | Use arrays |
