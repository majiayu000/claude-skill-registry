---
name: Laravel Testing
description: Automated testing standards with Pest and PHPUnit.
metadata:
  labels: [laravel, testing, pest, phpunit, tdd]
  triggers:
    files: ['tests/**/*.php', 'phpunit.xml']
    keywords: [feature, unit, mock, factory, sqlite]
---

# Laravel Testing

## **Priority: P1 (HIGH)**

## Structure

```text
tests/
├── Feature/            # Integration/HTTP tests
├── Unit/               # Isolated logic tests
└── TestCase.php
```

## Implementation Guidelines

- **Framework**: Use **Pest** for modern DX or PHPUnit for legacy parity.
- **Fresh Context**: Use `RefreshDatabase` trait for data isolation.
- **Factories**: Create test data via **Eloquent Factories**.
- **Mockery**: Use `$this->mock()` for external service substitution.
- **In-Memory**: Use SQLite `:memory:` for high-speed unit tests.
- **HTTP Assertions**: Use `$response->assertStatus()` and `assertJson()`.

## Anti-Patterns

- **Real APIs**: **No real network calls**: Always mock or stub.
- **Global State**: **No state leakage**: Refresh DB between tests.
- **Manual Insert**: **No DB::table()->insert()**: Use Factories.
- **Slow Logic**: **No heavy unit tests**: Move to Feature tests.

## References

- [Testing & Mocking Guide](references/implementation.md)
