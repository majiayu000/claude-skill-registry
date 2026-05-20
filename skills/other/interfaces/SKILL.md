---
name: interfaces
description: Contracts defining the shape a class must conform to. Used for decoupling dependent classes from concrete implementations, enabling multiple implementations and easier testing.
---

**Name:** Interfaces & Contracts
**Description:** Contracts defining the shape a class must conform to. Used for decoupling dependent classes from concrete implementations, enabling multiple implementations and easier testing.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Contracts/**/*.php, laravel, php, backend, interface, contract, dependency-inversion

## Rules

- Interface classes live in `app/Contracts/`
- Interfaces define a **contract** — the shape a class must conform to, without dictating the implementation
- Use a clear noun or adjective that describes the capability: `PaymentGateway`, `Notifiable`, `ReportGenerator`
- Avoid an `Interface` suffix — the namespace and context make it clear
- Only create an interface when there are (or you anticipate) **multiple implementations**
- Always type-hint the interface, never the concrete class, in consuming classes
- Bind the interface to a concrete implementation in a service provider
- Define only public method signatures — no implementation, no properties

## Examples

```php
// Interface definition
namespace App\Contracts;

use App\Models\Order;
use App\Data\PaymentResult;

interface PaymentGateway
{
    public function charge(Order $order, int $amountInCents): PaymentResult;

    public function refund(string $transactionId, int $amountInCents): PaymentResult;
}
```

```php
// Implementation
namespace App\Services\Payment;

use App\Contracts\PaymentGateway;

class StripeGateway implements PaymentGateway
{
    public function charge(Order $order, int $amountInCents): PaymentResult
    {
        // Stripe-specific implementation
    }

    public function refund(string $transactionId, int $amountInCents): PaymentResult
    {
        // Stripe-specific implementation
    }
}
```

```php
// Service container binding — AppServiceProvider
public function register(): void
{
    $this->app->bind(PaymentGateway::class, StripeGateway::class);
}
```

```php
// Consuming — type-hint the interface
class ChargePaymentMethod
{
    public function __construct(
        private readonly PaymentGateway $gateway,
    ) {}
}
```

```php
// Testing — swap the binding
$this->app->bind(PaymentGateway::class, FakePaymentGateway::class);
```

## Anti-Patterns

- Creating an interface for every class by default — only add interfaces where they provide real decoupling
- Creating an interface when there is only one implementation and no realistic chance of another
- Adding default implementations to an interface (use an abstract class instead)
- Adding constants specific to one implementation (keep in the concrete class)
- Type-hinting the concrete class instead of the interface in consumers

## References

- [Laravel Service Container](https://laravel.com/docs/container)
- [PHP Interfaces](https://www.php.net/manual/en/language.oop5.interfaces.php)
- Related: `Services/SKILL.md` — services often implement interfaces
