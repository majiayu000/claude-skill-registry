---
name: laravel-billing
description: Integrate Stripe and Paddle payments with Laravel Cashier. Use when implementing subscriptions, invoices, payment methods, or billing portals.
user-invocable: false
---

# Laravel Billing (Cashier)

## Documentation

### Billing
- [billing.md](docs/billing.md) - Stripe Cashier
- [cashier-paddle.md](docs/cashier-paddle.md) - Paddle Cashier

## Stripe Setup

```php
// Install
composer require laravel/cashier

// User model
use Laravel\Cashier\Billable;

class User extends Authenticatable
{
    use Billable;
}
```

## Subscription Controller

```php
<?php

declare(strict_types=1);

namespace App\Http\Controllers;

final class SubscriptionController extends Controller
{
    public function store(Request $request)
    {
        $request->user()
            ->newSubscription('default', 'price_monthly')
            ->create($request->paymentMethodId);

        return redirect()->route('dashboard');
    }

    public function cancel(Request $request)
    {
        $request->user()->subscription('default')->cancel();
        return back();
    }

    public function resume(Request $request)
    {
        $request->user()->subscription('default')->resume();
        return back();
    }
}
```

## Check Subscription Status

```php
if ($user->subscribed('default')) {
    // Has active subscription
}

if ($user->subscribedToPrice('price_monthly', 'default')) {
    // On monthly plan
}

if ($user->onTrial('default')) {
    // Currently on trial
}

if ($user->subscription('default')->cancelled()) {
    // Subscription cancelled
}

if ($user->subscription('default')->onGracePeriod()) {
    // Still has access after cancellation
}
```

## Single Charges

```php
$user->charge(1000, $paymentMethodId);
$user->invoiceFor('Product Name', 1500);
$user->refund($paymentIntentId);
```

## Billing Portal

```php
Route::get('/billing', function (Request $request) {
    return $request->user()->redirectToBillingPortal(route('dashboard'));
})->middleware('auth');
```

## Webhooks

```php
Route::post('/stripe/webhook', [WebhookController::class, 'handleWebhook']);

class WebhookController extends CashierController
{
    public function handleInvoicePaymentSucceeded($payload)
    {
        // Handle successful payment
    }
}
```
