---
name: acc-create-anti-corruption-layer
description: Generates DDD Anti-Corruption Layer for PHP 8.5. Creates translation layer between bounded contexts or external systems. Includes adapters, translators, facades, and unit tests.
---

# Anti-Corruption Layer Generator

Generate DDD-compliant Anti-Corruption Layer (ACL) components for isolating bounded contexts and integrating with external/legacy systems.

## When to Use

| Scenario | Example |
|----------|---------|
| Legacy system integration | ERP, CRM, mainframe |
| Third-party API integration | Payment gateway, shipping API |
| Bounded context communication | Order ↔ Inventory contexts |
| Database migration | Old schema → new domain model |
| Microservice integration | External service with different model |

## Anti-Corruption Layer Characteristics

- **Isolation**: Protects domain model from external/foreign concepts
- **Translation**: Converts between domain and external models
- **Facade**: Provides simplified interface to external systems
- **Adapter**: Implements domain ports using external services
- **No Domain Leakage**: External concepts never enter domain layer
- **Bidirectional**: Can translate both inbound and outbound

---

## ACL Architecture

```
YOUR BOUNDED CONTEXT
├── DOMAIN LAYER
│   └── Port (Interface) ←────────────┐
│                                      │
├── ANTI-CORRUPTION LAYER             │
│   ├── Adapter (implements Port) ────┘
│   ├── Translator (Domain ↔ External)
│   ├── Facade (External system wrapper)
│   └── External DTOs
│
└── EXTERNAL SYSTEM (Legacy, API, other bounded context)
```

---

## Generation Process

### Step 1: Generate Domain Port

**Path:** `src/Domain/{BoundedContext}/Port/`

1. `{ExternalSystem}PortInterface.php` — Domain interface for external system

### Step 2: Generate External DTOs

**Path:** `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/DTO/`

1. `{ExternalSystem}{Concept}DTO.php` — DTOs matching external format

### Step 3: Generate Translator

**Path:** `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/`

1. `{ExternalSystem}Translator.php` — Domain ↔ External conversion

### Step 4: Generate Facade

**Path:** `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/`

1. `{ExternalSystem}Facade.php` — Simplified external system interface

### Step 5: Generate Adapter

**Path:** `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/`

1. `{ExternalSystem}Adapter.php` — Implements domain port

### Step 6: Generate Exceptions

**Path:** `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/Exception/`

1. `{ExternalSystem}Exception.php` — Domain exception
2. `{ExternalSystem}ConnectionException.php` — Infrastructure exception

### Step 7: Generate Tests

1. `{ExternalSystem}TranslatorTest.php` — Translation tests
2. `{ExternalSystem}AdapterTest.php` — Adapter integration tests

---

## File Placement

| Component | Path |
|-----------|------|
| Domain Port | `src/Domain/{BoundedContext}/Port/{ExternalSystem}PortInterface.php` |
| External DTO | `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/DTO/` |
| Translator | `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/{ExternalSystem}Translator.php` |
| Facade | `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/{ExternalSystem}Facade.php` |
| Adapter | `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/{ExternalSystem}Adapter.php` |
| Exceptions | `src/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/Exception/` |
| Tests | `tests/Unit/Infrastructure/{BoundedContext}/ACL/{ExternalSystem}/` |

---

## Naming Conventions

| Component | Pattern | Example |
|-----------|---------|---------|
| Port | `{ExternalSystem}PortInterface` | `PaymentGatewayPortInterface` |
| DTO | `{ExternalSystem}{Concept}DTO` | `StripeChargeDTO` |
| Translator | `{ExternalSystem}Translator` | `StripeTranslator` |
| Facade | `{ExternalSystem}Facade` | `StripeFacade` |
| Adapter | `{ExternalSystem}Adapter` | `StripeAdapter` |
| Exception | `{ExternalSystem}Exception` | `StripeException` |

---

## Quick Template Reference

### Domain Port

```php
interface {ExternalSystem}PortInterface
{
    public function {operation}({DomainParameters}): {DomainReturnType};
}
```

### Translator

```php
final readonly class {ExternalSystem}Translator
{
    public function toDomain({ExternalSystem}DTO $dto): {Entity};
    public function toExternal({Entity} $entity): {ExternalSystem}DTO;
}
```

### Adapter

```php
final readonly class {ExternalSystem}Adapter implements {ExternalSystem}PortInterface
{
    public function __construct(
        private {ExternalSystem}Facade $facade,
        private {ExternalSystem}Translator $translator,
    ) {}

    public function {operation}({DomainParameters}): {DomainReturnType}
    {
        $dto = $this->translator->toExternal($entity);
        $result = $this->facade->{externalOperation}($dto);
        return $this->translator->toDomain($result);
    }
}
```

---

## Usage Example

```php
// Domain port interface
interface PaymentGatewayPortInterface
{
    public function charge(Payment $payment): PaymentId;
    public function refund(PaymentId $paymentId, Money $amount): void;
}

// Adapter implementation
final readonly class StripeAdapter implements PaymentGatewayPortInterface
{
    public function charge(Payment $payment): PaymentId
    {
        $stripeCharge = $this->translator->toStripeCharge($payment);
        $result = $this->facade->createCharge($stripeCharge);
        return $this->translator->toPaymentId($result);
    }
}
```

---

## Anti-patterns to Avoid

| Anti-pattern | Problem | Solution |
|--------------|---------|----------|
| Domain using external DTOs | External concepts leak into domain | Always translate at ACL boundary |
| Translator in domain layer | Infrastructure concern in domain | Keep translator in infrastructure |
| Exposing external exceptions | Coupling to external system | Wrap in domain exceptions |
| Direct API calls from domain | No isolation | Use port/adapter pattern |
| Shared DTOs across ACLs | Coupling between integrations | Each ACL has own DTOs |
| Business logic in translator | Wrong responsibility | Translator only maps data |

---

## DI Configuration

```yaml
# services.yaml
Domain\Payment\Port\PaymentGatewayPortInterface:
    alias: Infrastructure\Payment\ACL\Stripe\StripeAdapter

Infrastructure\Payment\ACL\Stripe\StripeFacade:
    arguments:
        $client: '@stripe.client'
```

---

## References

For complete PHP templates and examples, see:
- `references/templates.md` — Domain Port, External DTO, Translator, Facade, Adapter, Exception templates
- `references/examples.md` — Stripe Payment Gateway ACL complete example and tests
