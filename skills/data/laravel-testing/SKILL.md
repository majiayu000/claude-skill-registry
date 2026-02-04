---
name: laravel-testing
description: Write tests with Pest 3/PHPUnit, feature tests, unit tests, mocking, fakes, and factories. Use when testing controllers, services, models, or implementing TDD.
versions:
  laravel: "12.46"
  pest: "3.0"
  php: "8.5"
user-invocable: false
references: references/pest-basics.md, references/pest-datasets.md, references/pest-arch.md, references/http-requests.md, references/http-json.md, references/http-auth.md, references/http-assertions.md, references/database-basics.md, references/database-factories.md, references/database-assertions.md, references/mocking-services.md, references/mocking-fakes.md, references/mocking-http.md, references/console-tests.md, references/troubleshooting.md, references/templates/FeatureTest.php.md, references/templates/UnitTest.php.md, references/templates/ArchTest.php.md, references/templates/ApiTest.php.md, references/templates/PestConfig.php.md
related-skills: laravel-architecture, laravel-eloquent
---

# Laravel Testing

## Agent Workflow (MANDATORY)

Before ANY implementation, launch in parallel:

1. **fuse-ai-pilot:explore-codebase** - Analyze existing test patterns
2. **fuse-ai-pilot:research-expert** - Verify Pest/PHPUnit docs via Context7
3. **mcp__context7__query-docs** - Check assertion and mocking patterns

After implementation, run **fuse-ai-pilot:sniper** for validation.

---

## Overview

| Type | Purpose | Location |
|------|---------|----------|
| **Feature** | HTTP, full stack | `tests/Feature/` |
| **Unit** | Isolated classes | `tests/Unit/` |
| **Arch** | Code architecture | `tests/Arch.php` |

---

## Decision Guide: Test Type

```
What to test?
├── HTTP endpoint → Feature test
├── Service/Policy logic → Unit test
├── Code structure → Arch test
├── External API → Mock with Http::fake()
├── Mail/Queue/Event → Use Fakes
└── Database state → assertDatabaseHas()
```

---

## Decision Guide: Test Strategy

```
Coverage strategy?
├── Feature tests (70%) → Critical flows
├── Unit tests (25%) → Business logic
├── E2E tests (5%) → User journeys
└── Arch tests → Structural rules
```

---

## Critical Rules

1. **Use RefreshDatabase** for database isolation
2. **Use factories** for test data (never raw inserts)
3. **Mock external services** - Never call real APIs
4. **Test edge cases** - Empty, null, boundaries
5. **Run parallel** - `pest --parallel` for speed

---

## Reference Guide

### Pest Basics

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Pest Syntax** | [pest-basics.md](references/pest-basics.md) | it(), test(), describe() |
| **Datasets** | [pest-datasets.md](references/pest-datasets.md) | Data providers, hooks |
| **Architecture** | [pest-arch.md](references/pest-arch.md) | arch() tests |

### HTTP Testing

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Requests** | [http-requests.md](references/http-requests.md) | GET, POST, headers |
| **JSON API** | [http-json.md](references/http-json.md) | API assertions |
| **Authentication** | [http-auth.md](references/http-auth.md) | actingAs, guards |
| **Assertions** | [http-assertions.md](references/http-assertions.md) | Status, redirects |

### Database Testing

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Basics** | [database-basics.md](references/database-basics.md) | RefreshDatabase |
| **Factories** | [database-factories.md](references/database-factories.md) | Factory patterns |
| **Assertions** | [database-assertions.md](references/database-assertions.md) | DB assertions |

### Mocking

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Services** | [mocking-services.md](references/mocking-services.md) | Mock, spy |
| **Fakes** | [mocking-fakes.md](references/mocking-fakes.md) | Mail, Queue, Event |
| **HTTP & Time** | [mocking-http.md](references/mocking-http.md) | Http::fake, travel |

### Other

| Topic | Reference | When to Consult |
|-------|-----------|-----------------|
| **Console** | [console-tests.md](references/console-tests.md) | Artisan tests |
| **Troubleshooting** | [troubleshooting.md](references/troubleshooting.md) | Common errors |

### Templates

| Template | When to Use |
|----------|-------------|
| [FeatureTest.php.md](references/templates/FeatureTest.php.md) | HTTP feature test |
| [UnitTest.php.md](references/templates/UnitTest.php.md) | Service unit test |
| [ArchTest.php.md](references/templates/ArchTest.php.md) | Architecture test |
| [ApiTest.php.md](references/templates/ApiTest.php.md) | REST API test |
| [PestConfig.php.md](references/templates/PestConfig.php.md) | Pest configuration |

---

## Quick Reference

```php
// Feature test
it('creates a post', function () {
    $user = User::factory()->create();

    $this->actingAs($user)
        ->postJson('/api/posts', ['title' => 'Test'])
        ->assertCreated()
        ->assertJsonPath('data.title', 'Test');

    $this->assertDatabaseHas('posts', ['title' => 'Test']);
});

// With dataset
it('validates emails', function (string $email, bool $valid) {
    // test logic
})->with([
    ['valid@test.com', true],
    ['invalid', false],
]);

// Mock facade
Mail::fake();
// ... action ...
Mail::assertSent(OrderShipped::class);
```

---

## Commands

```bash
# Run all tests
php artisan test

# Pest directly
./vendor/bin/pest

# Parallel execution
./vendor/bin/pest --parallel

# Filter by name
./vendor/bin/pest --filter "user can"

# Coverage
./vendor/bin/pest --coverage --min=80

# Profile slow tests
./vendor/bin/pest --profile
```

---

## Best Practices

### DO
- Use `RefreshDatabase` trait
- Follow AAA pattern (Arrange-Act-Assert)
- Name tests descriptively
- Test one thing per test
- Use factories for data

### DON'T
- Create test dependencies
- Call real external APIs
- Use production database
- Skip edge cases
