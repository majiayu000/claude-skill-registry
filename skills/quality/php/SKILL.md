---
name: php
description: "PHP development: code quality, PSR standards, testing with PHPUnit."
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
    - "php testing"
    - "phpunit"
    - "pest php"
    - "php mock"
  category: php
  pairs_with:
    - code-linting
    - test-driven-development
---

# PHP Skill

PHP code quality and testing: strict types, PSR-12 compliance, modern language features, framework idioms, static analysis tooling, and PHPUnit testing patterns.

## Reference Loading Table

| Signal | Reference | Size |
|--------|-----------|------|
| union types, intersection types, DNF, enums, readonly, named arguments, match expression, null-safe operator, PHP 8.0, PHP 8.1, PHP 8.2 | `references/modern-php-features.md` | ~160 lines |
| Laravel, Eloquent, Collections, Service Container, Symfony, DI attributes, Event Dispatcher, framework | `references/framework-idioms.md` | ~70 lines |
| PHP-CS-Fixer, PHPStan, Psalm, Rector, static analysis, CI, linting, code style, taint analysis | `references/quality-tools.md` | ~60 lines |
| PHPUnit tests, data providers, mocks, stubs, database testing, HTTP testing, coverage | `references/testing-patterns.md` | ~120 lines |
| quality review process, phases, PSR-12 enforcement | `references/php-quality.md` | ~60 lines |
| test writing process, test doubles, Prophecy, database fixtures | `references/php-testing.md` | ~50 lines |

**Load greedily.** If the user's question touches any signal keyword, load the matching reference before responding. Multiple signals matching = load all matching references.

---

## Core Rules (Always Apply)

### Strict Types Declaration

Every PHP file must begin with `declare(strict_types=1)`. This enforces scalar type coercion rules, catching type errors at call time instead of silently converting values. Omitting it is a code quality defect.

### PSR-12 Coding Standard

PSR-12 extends PSR-1 and PSR-2 as the accepted PHP coding style:

- 4-space indentation, no trailing whitespace
- One class per file
- `use` statements after namespace with a blank line before and after
- Visibility required on all properties, methods, and constants
- Opening braces on same line for control structures
- Opening braces on next line for classes and methods

---

## Phase 1: ASSESS

Determine what kind of PHP work is needed:

| Request type | Load references | Action |
|-------------|----------------|--------|
| Code review | quality refs + quality-tools | Full quality pass |
| Type system question | modern-php-features | Feature-specific guidance |
| Framework patterns | framework-idioms | Idiomatic pattern review |
| Tooling setup | quality-tools | Config and CI guidance |
| Write tests | testing-patterns + php-testing | PHPUnit test authoring |
| Test review | testing-patterns | Test quality review |

**Gate**: Request classified and relevant references loaded.

---

## Phase 2: EXECUTE

Apply loaded reference knowledge to the user's code or question.

For quality reviews, check:
1. `declare(strict_types=1)` present
2. PSR-12 compliance
3. Modern PHP features used where appropriate
4. Framework idioms followed (if applicable)
5. Quality tooling configured (if applicable)

For testing work:
1. Use PHPUnit `TestCase` with `test` prefix or `@test` annotation
2. Use `@dataProvider` for table-driven cases
3. Use `createStub()` for return values, `createMock()` for interaction assertions
4. Use `DatabaseTransactions` (Laravel) or `KernelTestCase` (Symfony) for database tests
5. Call `parent::setUp()` first in every `setUp()` method

**Gate**: Specific, reference-backed feedback or code provided.

---

## Phase 3: VERIFY

Run the test suite and confirm:

```bash
./vendor/bin/phpunit
# For coverage enforcement:
XDEBUG_MODE=coverage ./vendor/bin/phpunit --coverage-text --coverage-min=80
```

**Gate**: All tests pass. Coverage threshold met if configured.
