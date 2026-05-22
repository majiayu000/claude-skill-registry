---
name: acc-clean-arch-knowledge
description: Clean Architecture knowledge base. Provides patterns, antipatterns, and PHP-specific guidelines for Clean Architecture and Hexagonal Architecture audits.
---

# Clean Architecture Knowledge Base

Quick reference for Clean Architecture / Hexagonal Architecture patterns and PHP implementation guidelines.

## Core Principles

### The Dependency Rule

```
┌────────────────────────────────────────────────────────────────┐
│                    FRAMEWORKS & DRIVERS                        │
│  (Web, UI, DB, External Services, Devices)                     │
├────────────────────────────────────────────────────────────────┤
│                    INTERFACE ADAPTERS                          │
│  (Controllers, Gateways, Presenters, Repositories)             │
├────────────────────────────────────────────────────────────────┤
│                    APPLICATION BUSINESS RULES                  │
│  (Use Cases, Application Services)                             │
├────────────────────────────────────────────────────────────────┤
│                    ENTERPRISE BUSINESS RULES                   │
│  (Entities, Value Objects, Domain Services)                    │
└────────────────────────────────────────────────────────────────┘
                              ▲
                              │
              Dependencies point INWARD only
```

**Rule:** Source code dependencies must point INWARD. Inner layers know nothing about outer layers.

### Hexagonal Architecture (Ports & Adapters)

```
                    ┌─────────────────┐
                    │   Primary       │
                    │   Adapters      │
                    │  (Controllers)  │
                    └────────┬────────┘
                             │
                             ▼
                    ┌─────────────────┐
        ┌──────────►│     PORTS       │◄──────────┐
        │           │  (Interfaces)   │           │
        │           └────────┬────────┘           │
        │                    │                    │
        │                    ▼                    │
        │           ┌─────────────────┐           │
        │           │   APPLICATION   │           │
        │           │    (Use Cases)  │           │
        │           └────────┬────────┘           │
        │                    │                    │
        │                    ▼                    │
        │           ┌─────────────────┐           │
        │           │     DOMAIN      │           │
        │           │   (Entities)    │           │
        │           └─────────────────┘           │
        │                                         │
        │           ┌─────────────────┐           │
        └───────────│   Secondary     │───────────┘
                    │   Adapters      │
                    │ (Repositories,  │
                    │  External APIs) │
                    └─────────────────┘
```

**Rule:** Application core defines Ports (interfaces). Adapters implement them.

## Quick Checklists

### Domain Layer Checklist

- [ ] No imports from outer layers
- [ ] No framework dependencies
- [ ] Pure business logic
- [ ] Value Objects for concepts
- [ ] Entities with behavior
- [ ] Repository interfaces only

### Application Layer Checklist

- [ ] Use Cases orchestrate domain
- [ ] Defines Ports (interfaces) for external services
- [ ] DTOs for input/output
- [ ] No infrastructure details
- [ ] No framework dependencies

### Interface Adapters Checklist

- [ ] Implements domain/application interfaces
- [ ] Controllers call Use Cases
- [ ] Presenters format output
- [ ] No business logic

### Frameworks & Drivers Checklist

- [ ] Configuration only
- [ ] Wiring/DI setup
- [ ] Framework-specific code isolated

## Common Violations Quick Reference

| Violation | Where to Look | Severity |
|-----------|---------------|----------|
| Inner layer imports outer | Domain/Application importing Infrastructure | Critical |
| Framework in core | Doctrine/Symfony in Domain | Critical |
| Use Case with HTTP details | Request/Response in Application | Critical |
| Business logic in Controller | if/switch on domain state | Warning |
| Missing Port | Direct external service call | Warning |
| Adapter with logic | Repository doing validation | Warning |

## PHP 8.5 Clean Architecture Patterns

### Port (Driven Port)

```php
// Application layer - defines the contract
namespace Application\Order\Port;

interface PaymentGatewayInterface
{
    public function charge(PaymentRequest $request): PaymentResponse;
    public function refund(string $transactionId, Money $amount): RefundResponse;
}
```

### Adapter (Driven Adapter)

```php
// Infrastructure layer - implements the contract
namespace Infrastructure\Payment;

final readonly class StripePaymentGateway implements PaymentGatewayInterface
{
    public function __construct(
        private StripeClient $stripe
    ) {}

    public function charge(PaymentRequest $request): PaymentResponse
    {
        $charge = $this->stripe->charges->create([
            'amount' => $request->amount->cents(),
            'currency' => $request->currency->value,
            'source' => $request->token,
        ]);

        return new PaymentResponse(
            transactionId: $charge->id,
            status: PaymentStatus::from($charge->status)
        );
    }
}
```

### Use Case (Application Service)

```php
namespace Application\Order\UseCase;

final readonly class ProcessPaymentUseCase
{
    public function __construct(
        private OrderRepositoryInterface $orders,
        private PaymentGatewayInterface $paymentGateway,  // Port
        private EventDispatcherInterface $events
    ) {}

    public function execute(ProcessPaymentCommand $command): PaymentResult
    {
        $order = $this->orders->findById($command->orderId);

        $payment = $this->paymentGateway->charge(
            new PaymentRequest($order->total(), $command->paymentToken)
        );

        if ($payment->isSuccessful()) {
            $order->markAsPaid($payment->transactionId());
            $this->orders->save($order);
        }

        return new PaymentResult($payment->transactionId(), $payment->status());
    }
}
```

### Controller (Driving Adapter)

```php
namespace Presentation\Api\Order;

final readonly class PaymentController
{
    public function __construct(
        private ProcessPaymentUseCase $processPayment
    ) {}

    public function process(Request $request): JsonResponse
    {
        $command = new ProcessPaymentCommand(
            orderId: new OrderId($request->get('order_id')),
            paymentToken: $request->get('payment_token')
        );

        $result = $this->processPayment->execute($command);

        return new JsonResponse([
            'transaction_id' => $result->transactionId,
            'status' => $result->status->value,
        ]);
    }
}
```

## References

For detailed information, load these reference files:

- `references/dependency-rule.md` — The Dependency Rule explained
- `references/layer-boundaries.md` — Layer responsibilities and boundaries
- `references/port-adapter-patterns.md` — Hexagonal Architecture patterns
- `references/antipatterns.md` — Common violations with detection patterns
