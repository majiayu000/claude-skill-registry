---
name: php-quality
description: "PHP code quality: PSR standards, strict types, framework idioms."
user-invocable: false
context: fork
agent: php-general-engineer
routing:
  triggers:
    - "php quality"
    - "php code review"
    - "PSR standards"
    - "phpstan"
    - "php-cs-fixer"
  category: php
  pairs_with:
    - php-testing
    - code-linting
---

# PHP Quality Skill

PHP code quality enforcement: strict types, PSR-12 compliance, modern language features, framework idioms, and static analysis tooling.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| union types, intersection types, DNF, enums, readonly, named arguments, match expression, null-safe operator, PHP 8.0, PHP 8.1, PHP 8.2 | `references/modern-php-features.md` | ~160 lines |
| Laravel, Eloquent, Collections, Service Container, Symfony, DI attributes, Event Dispatcher, framework | `references/framework-idioms.md` | ~70 lines |
| PHP-CS-Fixer, PHPStan, Psalm, Rector, static analysis, CI, linting, code style, taint analysis | `references/quality-tools.md` | ~60 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.

---

## Core Rules (Always Apply)

### Strict Types Declaration

Every PHP file must begin with `declare(strict_types=1)`. This enforces scalar type coercion rules, catching type errors at call time instead of silently converting values.

```php
<?php

declare(strict_types=1);

// Without strict_types: strlen(123) silently returns 3
// With strict_types: strlen(123) throws TypeError
```

This is non-negotiable. Omitting it is a code quality defect.

### PSR-12 Coding Standard

PSR-12 extends PSR-1 and PSR-2 as the accepted PHP coding style. Key rules:

- 4-space indentation, no trailing whitespace
- One class per file
- `use` statements after namespace with a blank line before and after
- Visibility required on all properties, methods, and constants
- Opening braces on same line for control structures
- Opening braces on next line for classes and methods

---

## Phase 1: ASSESS

Determine what kind of PHP quality review is needed:

| Request type | Load references | Action |
|-------------|----------------|--------|
| Code review | All three | Full quality pass |
| Type system question | `modern-php-features.md` | Feature-specific guidance |
| Framework patterns | `framework-idioms.md` | Idiomatic pattern review |
| Tooling setup | `quality-tools.md` | Config and CI guidance |

**Gate**: Request classified and relevant references loaded.

---

## Phase 2: REVIEW

Apply loaded reference knowledge to the user's code or question. Every review checks:
1. `declare(strict_types=1)` present
2. PSR-12 compliance
3. Modern PHP features used where appropriate (from references)
4. Framework idioms followed (if applicable)
5. Quality tooling configured (if applicable)

**Gate**: Specific, reference-backed feedback provided.
