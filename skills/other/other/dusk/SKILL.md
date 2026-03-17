---
name: dusk
description: End-to-end browser testing with Laravel Dusk. Used exclusively for full user flows requiring a real Chrome browser — JavaScript interactions, multi-step forms, and visual assertions.
---

**Name:** Dusk (Browser Testing)
**Description:** End-to-end browser testing with Laravel Dusk. Used exclusively for full user flows requiring a real Chrome browser — JavaScript interactions, multi-step forms, and visual assertions.
**Compatible Agents:** general-purpose, testing
**Tags:** tests/Browser/**/*.php, laravel, php, testing, dusk, browser, e2e, end-to-end

## Rules

- Browser tests live in `tests/Browser/`
- Use Dusk only where a real browser interaction is required (JavaScript, multi-step flows)
- Never use `RefreshDatabase` in Dusk tests — use `DatabaseTruncation` (preferred) or `DatabaseMigrations`
- Always call `assertNoJavaScriptErrors()` after every `visit()`
- Always use `dusk=""` HTML attributes as selectors — never CSS classes or IDs
- Never use `pause()` — use `waitFor()`, `waitForText()`, or `waitUntilMissing()` instead
- Use `loginAs()` to authenticate without going through the login form
- Extract repeated navigation into **Page Objects**
- Extract repeated interactive UI elements into **Dusk Components**
- Create a dedicated `.env.dusk.local` file to use a separate test database

## Examples

```php
uses(DatabaseTruncation::class);

it('user can submit an invoice', function () {
    // Arrange
    $user = User::factory()->create();

    // Act + Assert
    $this->browse(function (Browser $browser) use ($user) {
        $browser->loginAs($user)
                ->visit('/invoices/create')
                ->assertNoJavaScriptErrors()
                ->type('@amount-input', '100')
                ->press('@submit-button')
                ->waitForText('Invoice created')
                ->assertSee('Invoice created');
    });
});
```

```html
<!-- Blade/HTML — use dusk attributes, not CSS classes -->
<button dusk="submit-invoice">Submit</button>
<input dusk="amount-input" type="number" name="amount">
```

```php
// Page Object
class InvoicePage extends Page
{
    public function __construct(private readonly int $invoiceId) {}

    public function url(): string { return "/invoices/{$this->invoiceId}"; }

    public function assert(Browser $browser): void
    {
        $browser->assertPathIs($this->url());
    }

    public function elements(): array
    {
        return [
            '@mark-paid-button' => '[dusk="mark-paid-button"]',
        ];
    }

    public function markAsPaid(Browser $browser): void
    {
        $browser->click('@mark-paid-button')
                ->waitForText('Invoice marked as paid');
    }
}
```

```php
// Waiting — never use pause()
$browser->waitFor('@invoice-table');          // ❌ pause(3000)
$browser->waitForText('Invoice created');     // ❌ pause(2000)
$browser->waitUntilMissing('@loading-spinner'); // ❌ pause(5000)
```

## Anti-Patterns

- Using `RefreshDatabase` in Dusk tests (transactions invisible across HTTP processes)
- Using `pause(3000)` — arbitrary sleeps make tests slow and brittle
- Using CSS classes or IDs as selectors instead of `dusk=""` attributes
- Testing pure business logic or JSON API responses with Dusk (use feature tests instead)
- Not calling `assertNoJavaScriptErrors()` after `visit()`
- Repeating navigation and selector logic across test files instead of using Page Objects

## References

- [Laravel Dusk](https://laravel.com/docs/dusk)
- Related: `PestTesting/SKILL.md` — Pest syntax used for Dusk tests
- Related: `PHPUnit/SKILL.md` — feature tests for non-browser scenarios
