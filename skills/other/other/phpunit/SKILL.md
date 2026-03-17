---
name: phpunit
description: PHPUnit test structure, naming, assertions, and factory conventions for Laravel feature and unit tests.
---

**Name:** PHPUnit
**Description:** PHPUnit test structure, naming, assertions, and factory conventions for Laravel feature and unit tests.
**Compatible Agents:** general-purpose, testing
**Tags:** tests/**/*.php, laravel, php, testing, phpunit, unit-test, feature-test

## Rules

- **Feature tests** go in `tests/Feature/` and extend `Tests\TestCase`
- **Unit tests** go in `tests/Unit/` and extend `PHPUnit\Framework\TestCase`
- Always use `Illuminate\Foundation\Testing\RefreshDatabase` in feature tests that touch the database
- Unit tests have no Laravel bootstrap — pure PHP tests only
- Use `test_` method prefix with snake_case names: `test_user_can_create_resource`
- All test methods must have `: void` return type
- One assertion concern per test method — keep tests focused
- Prefer `assertSame` over `assertEquals` for strict type + value comparison
- Assert specific values, not just truthiness
- Every new model **must** have a corresponding factory in `database/factories/`
- Use factories in tests instead of manual `create()` / `insert()` calls
- Define meaningful default factory values; use states for variations

## Examples

```php
// Feature test
use Illuminate\Foundation\Testing\RefreshDatabase;
use Tests\TestCase;

class InvoiceControllerTest extends TestCase
{
    use RefreshDatabase;

    public function test_user_can_create_invoice(): void
    {
        $user  = User::factory()->create();
        $order = Order::factory()->create(['user_id' => $user->id]);

        $response = $this->actingAs($user)
            ->postJson('/api/invoices', ['order_id' => $order->id]);

        $response->assertStatus(201);
        $this->assertDatabaseHas('invoices', ['order_id' => $order->id]);
    }
}
```

```php
// Unit test — no Laravel bootstrap
use PHPUnit\Framework\TestCase;

class MoneyHelperTest extends TestCase
{
    public function test_formats_amount_in_cents_as_currency_string(): void
    {
        $result = MoneyHelper::format(1000, 'CHF');

        $this->assertSame('10.00 CHF', $result);
    }
}
```

```php
// Factory with states
// database/factories/UserFactory.php
public function unverified(): static
{
    return $this->state(fn (array $attributes) => [
        'email_verified_at' => null,
    ]);
}

// Usage in tests
User::factory()->create();
User::factory()->unverified()->create();
```

## Anti-Patterns

- Not using `RefreshDatabase` in feature tests that write to the database
- Using raw `insert()` or `create()` calls in tests instead of factories
- Mixing multiple assertion concerns in a single test method
- Using `assertEquals` when `assertSame` is needed for strict comparison
- Asserting truthiness (`assertTrue($result !== null)`) instead of a specific value
- Unit tests that bootstrap the full Laravel application (use `Tests\TestCase` only for feature tests)

## References

- [PHPUnit Documentation](https://phpunit.de/)
- [Laravel Testing](https://laravel.com/docs/testing)
- Related: `PestTesting/SKILL.md` — the preferred test framework (Pest over raw PHPUnit)
