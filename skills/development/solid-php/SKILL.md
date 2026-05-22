---
name: solid-php
description: SOLID principles for Laravel 12 and PHP 8.5. Files < 100 lines, interfaces separated, PHPDoc mandatory.
user-invocable: true
---

# SOLID PHP - Laravel 12 + PHP 8.5

## Current Date (CRITICAL)

**Today: January 2026** - ALWAYS use the current year for your searches.
Search with "2025" or "2026", NEVER with past years.

## MANDATORY: Research Before Coding

**CRITICAL: Check today's date first, then search documentation and web BEFORE writing any code.**

1. **Use Context7** to query Laravel/PHP official documentation
2. **Use Exa web search** with current year for latest trends
3. **Check Laravel News** of current year for new features
4. **Verify package versions** for Laravel 12 compatibility

```text
WORKFLOW:
1. Check date → 2. Research docs + web (current year) → 3. Apply latest patterns → 4. Code
```

**Search queries (replace YYYY with current year):**
- `Laravel [feature] YYYY best practices`
- `PHP 8.5 [feature] YYYY`
- `Livewire 3 [component] YYYY`
- `Pest PHP testing YYYY`

Never assume - always verify current APIs and patterns exist for the current year.

---

## Codebase Analysis (MANDATORY)

**Before ANY implementation:**
1. Explore project structure to understand architecture
2. Read existing related files to follow established patterns
3. Identify naming conventions, coding style, and patterns used
4. Understand data flow and dependencies

**Continue implementation by:**
- Following existing patterns and conventions
- Matching the coding style already in place
- Respecting the established architecture
- Integrating with existing services/components

## DRY - Reuse Before Creating (MANDATORY)

**Before writing ANY new code:**
1. Search existing codebase for similar functionality
2. Check shared locations: `app/Services/`, `app/Actions/`, `app/Traits/`
3. If similar code exists → extend/reuse instead of duplicate

**When creating new code:**
- Extract repeated logic (3+ occurrences) into shared helpers
- Place shared utilities in `app/Services/` or `app/Actions/`
- Use Traits for cross-cutting concerns
- Document reusable functions with PHPDoc

---

## Absolute Rules (MANDATORY)

### 1. Files < 100 lines
- **Split at 90 lines** - Never exceed 100
- Controllers < 50 lines
- Models < 80 lines (excluding relations)
- Services < 100 lines

### 2. Interfaces Separated
```
app/
├── Contracts/           # Interfaces ONLY
│   ├── UserRepositoryInterface.php
│   └── PaymentGatewayInterface.php
├── Repositories/        # Implementations
│   └── EloquentUserRepository.php
└── Services/            # Business logic
    └── UserService.php
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

### 4. Split Strategy
```
UserService.php (main)
├── UserValidator.php (validation)
├── UserDTO.php (types)
└── UserHelper.php (utils)
```

---

## References

### SOLID Principles
See: [`references/solid-principles.md`](./references/solid-principles.md)

Detailed implementation of S, O, L, I, D principles with PHP examples.

### PHP 8.5 Features
See: [`references/php85-features.md`](./references/php85-features.md)

Pipe operator, clone with, and no-discard attribute patterns.

### Laravel 12 Structure
See: [`references/laravel12-structure.md`](./references/laravel12-structure.md)

Recommended directory structure and guidelines by layer.

### Code Templates
See: [`references/code-templates.md`](./references/code-templates.md)

Service, DTO, Interface, and Repository templates.

---

## Response Guidelines

1. **Research first** - MANDATORY: Search Context7 + Exa before ANY code
2. **Show complete code** - Working examples, not snippets
3. **Explain decisions** - Why this pattern over alternatives
4. **Include tests** - Always suggest Pest test cases
5. **Handle errors** - Never ignore exceptions
6. **Type everything** - Full type hints, return types
7. **Document code** - PHPDoc for complex methods

---

## Forbidden

- ❌ Coding without researching docs first (ALWAYS research)
- ❌ Using outdated APIs without checking current year docs
- ❌ Files > 100 lines
- ❌ Controllers > 50 lines
- ❌ Interfaces in implementation files
- ❌ Business logic in Models/Controllers
- ❌ Concrete dependencies (always use interfaces)
- ❌ Code without PHPDoc
- ❌ Missing `declare(strict_types=1)`
- ❌ Fat classes (> 5 public methods)
- ❌ N+1 queries (use eager loading)
- ❌ Raw queries without bindings
- ❌ Using `array` instead of DTOs for complex data
