---
description: "Symfony validation — 3-layer validation strategy, constraints, DTO validation, domain invariants, validation groups, custom validators. Triggers on: validation, validator, constraint, DTO validation, input validation, invariant, assert, validation group"
---

# Symfony Validation

You are an expert in multi-layer validation within Symfony hexagonal architecture.

## When to Activate

- User needs input validation
- User asks about validation strategies
- User needs custom constraints
- User mentions DTO validation or domain invariants

## 3-Layer Validation Strategy

### Layer 1: Presentation (Input Validation)
**Where**: Controllers, request listeners
**What**: Format validation — is the input well-formed?
**How**: Symfony Validator on request DTOs

```php
// Request DTO with constraints
final readonly class CreateUserRequest
{
    public function __construct(
        #[Assert\NotBlank]
        #[Assert\Email]
        public string $email,

        #[Assert\NotBlank]
        #[Assert\Length(min: 2, max: 100)]
        public string $name,

        #[Assert\NotBlank]
        #[Assert\Length(min: 8)]
        #[Assert\Regex(pattern: '/[A-Z]/', message: 'Must contain uppercase')]
        #[Assert\Regex(pattern: '/[0-9]/', message: 'Must contain a number')]
        public string $password,
    ) {
    }
}
```

### Layer 2: Application (DTO/Command Validation)
**Where**: Command/Query classes, validated by Messenger middleware
**What**: Business rule pre-checks — are the values acceptable?
**How**: Symfony Validator constraints on command properties

```php
final readonly class RegisterUser
{
    public function __construct(
        #[Assert\NotBlank]
        #[Assert\Email]
        public string $email,

        #[Assert\NotBlank]
        public string $name,

        #[Assert\NotBlank]
        public string $password,
    ) {
    }
}
```

The `validation` middleware on the bus auto-validates before handler execution.

### Layer 3: Domain (Invariants)
**Where**: Entity constructors, value objects, business methods
**What**: Business invariants — is the operation valid in domain context?
**How**: Pure PHP validation, throw domain exceptions

```php
// Value object self-validates
final readonly class Email
{
    public function __construct(public string $value)
    {
        if (!filter_var($value, FILTER_VALIDATE_EMAIL)) {
            throw InvalidEmailException::forValue($value);
        }
    }
}

// Entity protects invariants
final class Order
{
    public function cancel(string $reason): void
    {
        if ($this->status === OrderStatus::DELIVERED) {
            throw CannotCancelDeliveredException::forOrder($this->id);
        }
        // ...
    }
}
```

## References

See `references/` for detailed guides:
- `validation-layers.md` — Full examples for each layer, custom constraints, groups
