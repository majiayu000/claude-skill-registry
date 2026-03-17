---
name: general
description: Project-wide Laravel conventions that always apply: configuration access, database patterns, logging, activity logging, and code formatting.
---

**Name:** Laravel General Conventions
**Description:** Project-wide Laravel conventions that always apply: configuration access, database patterns, logging, activity logging, and code formatting.
**Compatible Agents:** general-purpose, backend
**Tags:** app/**/*.php, laravel, php, backend, config, logging, formatting, conventions

## Rules

- Use `config()` helper to read configuration values — **never** use `env()` directly outside of config files
- Add new config keys to the appropriate file in `config/`
- Use Eloquent or Query Builder — no raw DB queries
- Wrap multi-step writes in `DB::transaction()`
- Use `Illuminate\Support\Facades\Log` with structured context arrays for logging
- Add the `Spatie\Activitylog\Traits\LogsActivity` trait on all models that track business data
- Configure `getActivitylogOptions()` with `logAll()`, `logOnlyDirty()`, `dontSubmitEmptyLogs()`
- Use `activity()->performedOn($model)->log(...)` for manual log entries in jobs and controllers
- Run **Laravel Pint** on all PHP code before committing

## Examples

```php
// Configuration — always use config()
$secret = config('services.stripe.secret');
// ❌ env('STRIPE_SECRET')
```

```php
// Structured logging
Log::info('Invoice created.', [
    'invoice_id' => $invoice->id,
    'order_id'   => $order->id,
    'amount'     => $invoice->amount,
]);

Log::error('Payment failed.', [
    'invoice_id' => $invoice->id,
    'error'      => $exception->getMessage(),
]);
```

```php
// Database transactions for multi-step writes
$payment = DB::transaction(function () use ($order) {
    $invoice = $this->createInvoice->execute($order);
    $payment = $this->chargePaymentMethod->execute($order, $invoice);

    return $payment;
});
```

```php
// Manual activity log entry
activity()
    ->performedOn($invoice)
    ->withProperties(['amount' => $invoice->amount])
    ->log('Invoice paid manually via admin panel.');
```

## Anti-Patterns

- Using `env('KEY')` directly in application code outside of config files
- Writing raw SQL queries with `DB::statement()` or `DB::select()` when Eloquent/Query Builder can be used
- Using `Log::info('Message')` without a context array — always include structured data
- Not wrapping related database operations in a transaction

## References

- [Laravel Configuration](https://laravel.com/docs/configuration)
- [Laravel Logging](https://laravel.com/docs/logging)
- [Spatie Activity Log](https://spatie.be/docs/laravel-activitylog/)
- [Laravel Pint](https://laravel.com/docs/pint)
