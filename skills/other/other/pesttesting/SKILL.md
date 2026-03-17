---
name: pesttesting
description: Laravel testing conventions using the Pest PHP framework. Covers test structure, AAA pattern, HTTP assertions, datasets, mocking, browser tests, and architecture tests.
---

**Name:** Pest Testing
**Description:** Laravel testing conventions using the Pest PHP framework. Covers test structure, AAA pattern, HTTP assertions, datasets, mocking, browser tests, and architecture tests.
**Compatible Agents:** general-purpose, testing
**Tags:** tests/**/*.php, laravel, php, testing, pest, feature-test, unit-test, browser-test

## Rules

- Always use **Pest syntax** — never raw PHPUnit classes or `$this->assert*` outside of HTTP responses
- Always follow **AAA**: Arrange → Act → Assert, with a comment label for each section
- Always use **named HTTP assertion methods** — never `assertStatus(int)` with a raw integer
- Never delete a test without explicit approval
- Test files mirror the class they test: `UserController` → `UserControllerTest.php`
- Test descriptions read as plain English: `it('creates an invoice for the given order')`
- Group related tests with `describe()` named after the class or feature under test
- Use `uses(RefreshDatabase::class)` in every test file that touches the database
- Use `beforeEach()` inside `describe()` blocks for shared setup — never repeat setup across tests
- Use datasets instead of duplicating tests for multiple inputs
- Prefer **Laravel fakes** over mocks for events, mail, notifications, and queues
- Browser tests: always use `DatabaseTruncation` — never `RefreshDatabase`
- Browser tests: always call `assertNoJavaScriptErrors()` after every `visit()`
- Browser tests: always use `dusk=""` HTML attributes as selectors — never CSS classes or IDs
- Browser tests: never use `pause()` — use `waitFor()`, `waitForText()`, or `waitUntilMissing()`
- Add architecture tests in `tests/Architecture/` to enforce conventions automatically

## Examples

```php
// Basic test — AAA pattern
uses(RefreshDatabase::class);

it('creates an invoice for the given order', function () {
    // Arrange
    $order = Order::factory()->create();

    // Act
    $response = $this->postJson('/api/invoices', ['order_id' => $order->id]);

    // Assert
    $response->assertCreated();
    expect(Invoice::count())->toBe(1);
});
```

```php
// Grouped with describe() and beforeEach()
describe('InvoiceController', function () {
    beforeEach(function () {
        $this->user = User::factory()->create();
        $this->actingAs($this->user);
    });

    it('lists all invoices', function () {
        Invoice::factory()->count(3)->create();
        $this->getJson('/api/invoices')->assertSuccessful();
    });

    it('creates an invoice', function () {
        $order = Order::factory()->create();
        $this->postJson('/api/invoices', ['order_id' => $order->id])
            ->assertCreated();
    });
});
```

```php
// Datasets for multiple inputs
it('rejects invalid email addresses', function (string $email) {
    $this->postJson('/api/users', ['email' => $email])
        ->assertUnprocessable();
})->with([
    'empty string'  => [''],
    'missing @'     => ['notanemail'],
    'missing tld'   => ['user@domain'],
]);
```

```php
// Named HTTP assertion methods
$response->assertSuccessful();    // ❌ assertStatus(200)
$response->assertCreated();       // ❌ assertStatus(201)
$response->assertNoContent();     // ❌ assertStatus(204)
$response->assertUnprocessable(); // ❌ assertStatus(422)
$response->assertForbidden();     // ❌ assertStatus(403)
$response->assertUnauthorized();  // ❌ assertStatus(401)
$response->assertNotFound();      // ❌ assertStatus(404)
```

```php
// Architecture tests
arch('no debug calls in production code')
    ->expect('App')
    ->not->toUse(['dd', 'dump', 'var_dump', 'ray']);

arch('controllers have the correct suffix')
    ->expect('App\Http\Controllers')
    ->toHaveSuffix('Controller');
```

## Anti-Patterns

- Using `assertStatus(200)` instead of named assertion methods
- Using `RefreshDatabase` in browser (Dusk) tests — use `DatabaseTruncation`
- Using `pause(3000)` in browser tests — use `waitFor()` or `waitForText()`
- Repeating the same test for multiple inputs instead of using datasets
- Using CSS class or ID selectors in Dusk — use `dusk=""` attributes
- Missing `uses(RefreshDatabase::class)` in feature/unit files that touch the database
- Deleting a test without explicit approval
- Missing `assertNoJavaScriptErrors()` after `visit()` in browser tests

## References

- [Pest PHP Documentation](https://pestphp.com/)
- [Laravel Testing](https://laravel.com/docs/testing)
- Related: `Dusk/SKILL.md` — full browser (E2E) test conventions
- Related: `PHPStan/SKILL.md` — static analysis runs alongside tests
