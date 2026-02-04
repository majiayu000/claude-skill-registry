---
name: solid-php
description: SOLID principles for Laravel 12 and PHP 8.5. Files < 100 lines, interfaces separated, PHPDoc mandatory. Auto-detects Laravel and FuseCore architecture.
versions:
  laravel: "12.46"
  php: "8.5"
user-invocable: true
references: references/solid-principles.md, references/anti-patterns.md, references/decision-guide.md, references/php85-features.md, references/laravel12-structure.md, references/fusecore-structure.md, references/templates/code-templates.md, references/templates/controller-templates.md, references/templates/refactoring-guide.md
related-skills: laravel-architecture, fusecore
---

# SOLID PHP - Laravel 12 + PHP 8.5

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing architecture
2. **fuse-ai-pilot:research-expert** - Verify Laravel/PHP docs via Context7
3. **mcp__context7__query-docs** - Check SOLID patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Auto-Detection

| Files Detected | Architecture | Interfaces Location |
|----------------|--------------|---------------------|
| `composer.json` + `artisan` | Laravel Standard | `app/Contracts/` |
| `app/Modules/` directory | FuseCore Modular | `app/Modules/[Feature]/Contracts/` |
| `routes/modules.php` | FuseCore Modular | `app/Modules/[Feature]/Contracts/` |

**Verification**: `php artisan --version` → Laravel 12.x

---

## Decision Tree: Where to Put Code?

```
New code needed?
├── HTTP validation → app/Http/Requests/
├── Single action → app/Actions/
├── Business logic → app/Services/ (or Modules/[X]/Services/)
├── Data access → app/Repositories/
├── Data transfer → app/DTOs/
├── Interface → app/Contracts/
├── Event → app/Events/
└── Authorization → app/Policies/
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

### 2. Interfaces Separated
```
app/Contracts/           # Interfaces ONLY
├── UserRepositoryInterface.php
└── PaymentGatewayInterface.php
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
| **SOLID** | [solid-principles.md](references/solid-principles.md) | S, O, L, I, D implementation |
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
| Interfaces in impl files | Location | Move to Contracts/ |
| Business logic in Models | Code in model | Extract to Service |
| Concrete dependencies | `new Class()` | Inject interface |
| Missing PHPDoc | No doc block | Add documentation |
| Missing strict_types | No declare | Add to all files |
| Fat classes | > 5 public methods | Split responsibilities |

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
