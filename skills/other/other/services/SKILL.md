---
name: services
description: Orchestration classes that coordinate multiple Actions, external APIs, or domain operations into a cohesive workflow. Services own transaction boundaries and third-party API integrations.
---

**Name:** Services
**Description:** Orchestration classes that coordinate multiple Actions, external APIs, or domain operations into a cohesive workflow. Services own transaction boundaries and third-party API integrations.
**Compatible Agents:** general-purpose, backend
**Tags:** app/Services/**/*.php, laravel, php, backend, service, orchestration, api-integration

## Rules

- Service classes live in `app/Services/`
- Name after the domain or integration they serve: `PaymentService`, `SubscriptionService`, `StripeService`
- Avoid generic suffixes like `Manager` or `Handler`
- Services may expose multiple related methods, all scoped to their domain
- Inject dependencies via the constructor
- Use `DB::transaction()` for multi-step operations that must all succeed or fail together
- Wrap third-party SDKs behind a service class with a clean internal interface
- Register external service wrappers as singletons in a service provider
- Use Actions for individual discrete operations — a Service orchestrates multiple Actions

## Examples

```php
namespace App\Services;

use App\Actions\CreateInvoice;
use App\Actions\ChargePaymentMethod;
use App\Actions\SendPaymentConfirmation;
use App\Models\Order;
use App\Models\Payment;
use Illuminate\Support\Facades\DB;

class PaymentService
{
    public function __construct(
        private readonly CreateInvoice           $createInvoice,
        private readonly ChargePaymentMethod     $chargePaymentMethod,
        private readonly SendPaymentConfirmation $sendConfirmation,
    ) {}

    public function processOrderPayment(Order $order): Payment
    {
        return DB::transaction(function () use ($order) {
            $invoice = $this->createInvoice->execute($order);
            $payment = $this->chargePaymentMethod->execute($order, $invoice);
            $this->sendConfirmation->execute($payment);

            return $payment;
        });
    }

    public function refund(Payment $payment): void
    {
        // refund orchestration logic
    }
}
```

```php
// Registering an external service wrapper — AppServiceProvider
$this->app->singleton(StripeService::class, function () {
    return new StripeService(config('services.stripe.secret'));
});
```

```php
// Controller
class PaymentController extends Controller
{
    public function store(StorePaymentRequest $request, PaymentService $service): JsonResponse
    {
        $order = Order::findOrFail($request->validated('order_id'));
        $payment = $service->processOrderPayment($order);

        return new JsonResponse(new PaymentResource($payment), 201);
    }
}
```

## Anti-Patterns

- Using a Service for a single discrete operation (use an Action instead)
- Putting HTTP concerns (request, response) inside a Service
- Naming a service `DataManager` or `UserHandler` instead of a domain-specific name
- Putting model attribute logic in a Service (belongs in the Model)
- Putting authorization in a Service (belongs in Policies)
- Making raw HTTP calls instead of using Saloon for external API integrations

## References

- [Laravel Service Container](https://laravel.com/docs/container)
- Related: `Actions/SKILL.md` — individual operations that Services orchestrate
- Related: `Saloon/SKILL.md` — the pattern for external API integrations
