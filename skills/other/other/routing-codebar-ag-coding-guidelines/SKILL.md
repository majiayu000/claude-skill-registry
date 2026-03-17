---
name: routing
description: Route file conventions for organising API and web routes. Covers file separation, naming, grouping, middleware, and route model binding.
---

**Name:** Routing
**Description:** Route file conventions for organising API and web routes. Covers file separation, naming, grouping, middleware, and route model binding.
**Compatible Agents:** general-purpose, backend
**Tags:** routes/**/*.php, laravel, php, backend, routing, routes, api, web

## Rules

- API routes in `routes/api.php`; web routes in `routes/web.php`
- Group related routes with prefixes and middleware
- Use route model binding where possible
- Use resourceful route names: `invoices.index`, `invoices.store`
- Use kebab-case for URL segments: `/invoice-lines`
- Prefix API routes with `/api` (handled by Laravel automatically via `api.php`)
- Apply authentication middleware at the group level
- Apply throttle middleware on API endpoints
- Use custom middleware for webhook signature verification

## Examples

```php
// routes/api.php
Route::middleware('auth:sanctum')->group(function () {
    Route::apiResource('invoices', InvoiceController::class);

    Route::prefix('invoices')->group(function () {
        Route::post('{invoice}/pay', PayInvoiceController::class)->name('invoices.pay');
    });
});

Route::middleware(['throttle:webhook'])->group(function () {
    Route::post('webhooks/stripe', ProcessStripeWebhookController::class)
        ->middleware(VerifyStripeSignature::class)
        ->name('webhooks.stripe');
});
```

```php
// Route model binding — automatic resolution
Route::get('invoices/{invoice}', ShowInvoiceController::class);

// Controller resolves the model automatically
public function __invoke(Invoice $invoice): JsonResponse { ... }
```

```php
// Naming with resourceful convention
Route::apiResource('invoice-lines', InvoiceLineController::class);
// Generates: invoice-lines.index, invoice-lines.store, invoice-lines.show, etc.
```

## Anti-Patterns

- Mixing API and web routes in the same file
- Not using route model binding when an ID is passed to look up a model
- Applying authentication middleware per route instead of at the group level
- Using camelCase or snake_case in URL segments instead of kebab-case
- Not naming routes (anonymous routes are harder to reference and refactor)

## References

- [Laravel Routing](https://laravel.com/docs/routing)
- Related: `Controllers/SKILL.md` — controllers that handle routes
- Related: `Middleware/SKILL.md` — middleware applied at the route group level
