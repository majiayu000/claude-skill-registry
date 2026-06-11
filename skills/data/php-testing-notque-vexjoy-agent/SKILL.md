---
name: php-testing
description: "PHP testing patterns: PHPUnit, test doubles, database testing."
user-invocable: false
context: fork
agent: php-general-engineer
routing:
  triggers:
    - "php testing"
    - "phpunit"
    - "pest php"
    - "php mock"
  category: php
  pairs_with:
    - php-quality
    - test-driven-development
---

# PHP Testing Skill

## Overview

Apply PHPUnit testing patterns for PHP projects: unit tests with data providers, test doubles (stubs, mocks, Prophecy), database testing (Laravel/Symfony), HTTP testing, and coverage configuration.

> See `references/patterns.md` for full code examples, the failure modes table, and the commands reference.

## Reference Loading Table

| Signal | Load These Files | Why |
|---|---|---|
| writing PHPUnit tests: data providers, mocks/stubs, database or HTTP tests, coverage config | `patterns.md` | Loads detailed guidance from `patterns.md`. |

## Instructions

### Phase 1: IDENTIFY

Determine what needs testing:
- Unit logic: use PHPUnit `TestCase` with `test` prefix or `@test` annotation
- Table-driven cases: use `@dataProvider` static methods
- Collaborator behavior: use stubs (return values only) or mocks (assert interactions)
- Database state: use `DatabaseTransactions` (Laravel) or `KernelTestCase` (Symfony)
- HTTP endpoints: use Laravel HTTP helpers or Symfony `WebTestCase`

### Phase 2: WRITE

Write tests following these rules:
- Call `parent::setUp()` first in every `setUp()` method
- Use `assertSame()` instead of `assertTrue($a === $b)` for meaningful failure messages
- Mock only collaborators and dependencies, never the class under test
- Keep tests independent -- do not use `@depends` chains
- Extract repetitive cases to `@dataProvider` rather than duplicating test methods

For test doubles: use `createStub()` when you only need return values, `createMock()` when asserting method calls, and Prophecy (`phpspec/prophecy-phpunit`) for more expressive interaction assertions.

For database tests: use `DatabaseTransactions` (Laravel) or DoctrineTestBundle (Symfony) to roll back state after each test.

### Phase 3: VERIFY

Run the test suite and confirm all tests pass:

```bash
./vendor/bin/phpunit
```

For coverage enforcement:

```bash
XDEBUG_MODE=coverage ./vendor/bin/phpunit --coverage-text --coverage-min=80
```

**GATE**: All tests pass. Coverage threshold met if configured. No failure modes from `references/patterns.md` introduced.
