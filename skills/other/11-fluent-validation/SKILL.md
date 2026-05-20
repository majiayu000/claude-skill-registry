---
name: fluent-validation
description: "Generates FluentValidation validators for commands and queries. Includes common validation rules, custom validators, async validation, and integration with MediatR pipeline behaviors."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: FluentValidation, FluentValidation.DependencyInjectionExtensions
---

# FluentValidation Rules Generator

## Overview

FluentValidation provides a fluent interface for building strongly-typed validation rules:

- **Declarative rules** - Readable, maintainable validation logic
- **Separation of concerns** - Validation separate from domain
- **Integration with MediatR** - Automatic validation via pipeline behavior
- **Custom validators** - Reusable validation components

## Quick Reference

| Validator Type | Purpose | Example |
|----------------|---------|---------|
| Built-in | Common validations | `NotEmpty()`, `MaximumLength()` |
| Custom | Reusable rules | `Must(BeValidEmail)` |
| Async | Database checks | `MustAsync(BeUniqueEmail)` |
| Child | Nested objects | `SetValidator(new AddressValidator())` |
| Collection | List items | `RuleForEach(x => x.Items)` |

---

## Validator Structure

```
/Application/{Feature}/
├── Create{Entity}/
│   ├── Create{Entity}Command.cs
│   └── Create{Entity}CommandValidator.cs    # Or inline in Command.cs
├── Update{Entity}/
│   └── Update{Entity}Command.cs             # Validator inline
└── Validators/
    ├── EmailValidator.cs                     # Reusable validators
    └── PhoneNumberValidator.cs
```

---

## Template: Basic Command Validator

```csharp
// src/{name}.application/{Feature}/Create{Entity}/Create{Entity}CommandValidator.cs
using FluentValidation;

namespace {name}.application.{feature}.Create{Entity};

public sealed class Create{Entity}CommandValidator : AbstractValidator<Create{Entity}Command>
{
    public Create{Entity}CommandValidator()
    {
        // ═══════════════════════════════════════════════════════════════
        // STRING VALIDATIONS
        // ═══════════════════════════════════════════════════════════════
        
        RuleFor(x => x.Name)
            .NotEmpty()
                .WithMessage("{Entity} name is required")
            .MaximumLength(100)
                .WithMessage("{Entity} name must not exceed 100 characters")
            .MinimumLength(2)
                .WithMessage("{Entity} name must be at least 2 characters");

        RuleFor(x => x.Description)
            .MaximumLength(500)
                .WithMessage("Description must not exceed 500 characters")
            .When(x => !string.IsNullOrEmpty(x.Description));

        // ═══════════════════════════════════════════════════════════════
        // GUID VALIDATIONS
        // ═══════════════════════════════════════════════════════════════
        
        RuleFor(x => x.OrganizationId)
            .NotEmpty()
                .WithMessage("Organization ID is required")
            .NotEqual(Guid.Empty)
                .WithMessage("Organization ID cannot be empty GUID");

        // ═══════════════════════════════════════════════════════════════
        // OPTIONAL FOREIGN KEY
        // ═══════════════════════════════════════════════════════════════
        
        RuleFor(x => x.ParentId)
            .NotEqual(Guid.Empty)
                .WithMessage("Parent ID cannot be empty GUID")
            .When(x => x.ParentId.HasValue);
    }
}
```

---

## Template: Inline Validator (Preferred Pattern)

```csharp
// src/{name}.application/{Feature}/Create{Entity}/Create{Entity}Command.cs
using FluentValidation;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.{feature}.Create{Entity};

// ═══════════════════════════════════════════════════════════════
// COMMAND
// ═══════════════════════════════════════════════════════════════
public sealed record Create{Entity}Command(
    string Name,
    string? Description,
    Guid OrganizationId,
    string Email,
    decimal Amount,
    List<CreateItemRequest> Items) : ICommand<Guid>;

public sealed class CreateItemRequest
{
    public required string Name { get; init; }
    public int Quantity { get; init; }
}

// ═══════════════════════════════════════════════════════════════
// VALIDATOR (internal, same file)
// ═══════════════════════════════════════════════════════════════
internal sealed class Create{Entity}CommandValidator : AbstractValidator<Create{Entity}Command>
{
    public Create{Entity}CommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Email)
            .NotEmpty()
            .EmailAddress()
                .WithMessage("A valid email address is required");

        RuleFor(x => x.Amount)
            .GreaterThan(0)
                .WithMessage("Amount must be positive")
            .LessThanOrEqualTo(1_000_000)
                .WithMessage("Amount cannot exceed 1,000,000");

        RuleFor(x => x.Items)
            .NotEmpty()
                .WithMessage("At least one item is required")
            .Must(items => items.Count <= 100)
                .WithMessage("Cannot have more than 100 items");

        RuleForEach(x => x.Items)
            .ChildRules(item =>
            {
                item.RuleFor(i => i.Name)
                    .NotEmpty()
                    .MaximumLength(200);

                item.RuleFor(i => i.Quantity)
                    .GreaterThan(0)
                    .LessThanOrEqualTo(10000);
            });
    }
}

// ═══════════════════════════════════════════════════════════════
// HANDLER
// ═══════════════════════════════════════════════════════════════
internal sealed class Create{Entity}CommandHandler 
    : ICommandHandler<Create{Entity}Command, Guid>
{
    // ... implementation
}
```

---

## Template: Async Validator with Database Check

```csharp
// src/{name}.application/{Feature}/Create{Entity}/Create{Entity}CommandValidator.cs
using FluentValidation;
using {name}.domain.{aggregate};

namespace {name}.application.{feature}.Create{Entity};

internal sealed class Create{Entity}CommandValidator : AbstractValidator<Create{Entity}Command>
{
    private readonly I{Entity}Repository _{entity}Repository;
    private readonly IOrganizationRepository _organizationRepository;

    public Create{Entity}CommandValidator(
        I{Entity}Repository {entity}Repository,
        IOrganizationRepository organizationRepository)
    {
        _{entity}Repository = {entity}Repository;
        _organizationRepository = organizationRepository;

        // Sync validations first (fast)
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.OrganizationId)
            .NotEmpty();

        // Async validations (database calls)
        RuleFor(x => x.Name)
            .MustAsync(BeUniqueName)
                .WithMessage("A {entity} with this name already exists");

        RuleFor(x => x.OrganizationId)
            .MustAsync(OrganizationExists)
                .WithMessage("Organization does not exist");
    }

    private async Task<bool> BeUniqueName(string name, CancellationToken ct)
    {
        var existing = await _{entity}Repository.GetByNameAsync(name, ct);
        return existing is null;
    }

    private async Task<bool> OrganizationExists(Guid organizationId, CancellationToken ct)
    {
        return await _organizationRepository.ExistsAsync(organizationId, ct);
    }
}
```

**Note**: Prefer doing existence checks in the Handler rather than Validator for better separation of concerns and testability. Use async validation sparingly.

---

## Template: Reusable Custom Validator

```csharp
// src/{name}.application/Validators/EmailValidator.cs
using FluentValidation;
using FluentValidation.Validators;

namespace {name}.application.validators;

/// <summary>
/// Validates email format with stricter rules than built-in EmailAddress
/// </summary>
public sealed class StrictEmailValidator<T> : PropertyValidator<T, string>
{
    public override string Name => "StrictEmailValidator";

    public override bool IsValid(ValidationContext<T> context, string value)
    {
        if (string.IsNullOrWhiteSpace(value))
        {
            return true; // Let NotEmpty handle null/empty
        }

        // Stricter email validation
        value = value.Trim().ToLowerInvariant();

        if (value.Length > 254)
            return false;

        var atIndex = value.IndexOf('@');
        if (atIndex <= 0)
            return false;

        var dotIndex = value.LastIndexOf('.');
        if (dotIndex <= atIndex + 1)
            return false;

        if (dotIndex >= value.Length - 1)
            return false;

        // Check for common invalid patterns
        if (value.Contains("..") || value.Contains(".@") || value.Contains("@."))
            return false;

        return true;
    }

    protected override string GetDefaultMessageTemplate(string errorCode)
        => "{PropertyName} must be a valid email address";
}

// Extension method for fluent usage
public static class ValidatorExtensions
{
    public static IRuleBuilderOptions<T, string> StrictEmail<T>(
        this IRuleBuilder<T, string> ruleBuilder)
    {
        return ruleBuilder.SetValidator(new StrictEmailValidator<T>());
    }
}
```

### Using Custom Validator

```csharp
public sealed class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator()
    {
        RuleFor(x => x.Email)
            .NotEmpty()
            .StrictEmail();  // Custom validator
    }
}
```

---

## Template: Nested Object Validator

```csharp
// src/{name}.application/Validators/AddressValidator.cs
using FluentValidation;

namespace {name}.application.validators;

public sealed class AddressValidator : AbstractValidator<AddressRequest>
{
    public AddressValidator()
    {
        RuleFor(x => x.Street)
            .NotEmpty()
            .MaximumLength(200);

        RuleFor(x => x.City)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.State)
            .NotEmpty()
            .MaximumLength(50);

        RuleFor(x => x.ZipCode)
            .NotEmpty()
            .Matches(@"^\d{5}(-\d{4})?$")
                .WithMessage("Invalid ZIP code format");

        RuleFor(x => x.Country)
            .NotEmpty()
            .MaximumLength(100);
    }
}

// Using nested validator
public sealed class CreateCustomerCommandValidator : AbstractValidator<CreateCustomerCommand>
{
    public CreateCustomerCommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);

        // Nested object validation
        RuleFor(x => x.BillingAddress)
            .NotNull()
                .WithMessage("Billing address is required")
            .SetValidator(new AddressValidator());

        // Optional nested object
        RuleFor(x => x.ShippingAddress)
            .SetValidator(new AddressValidator()!)
            .When(x => x.ShippingAddress is not null);
    }
}
```

---

## Template: Collection Validator

```csharp
// src/{name}.application/{Feature}/CreateOrder/CreateOrderCommandValidator.cs
using FluentValidation;

namespace {name}.application.orders.createorder;

public sealed class CreateOrderCommandValidator : AbstractValidator<CreateOrderCommand>
{
    public CreateOrderCommandValidator()
    {
        // Collection must have items
        RuleFor(x => x.Items)
            .NotEmpty()
                .WithMessage("Order must contain at least one item")
            .Must(items => items.Count <= 50)
                .WithMessage("Order cannot contain more than 50 items");

        // Validate each item in collection
        RuleForEach(x => x.Items)
            .ChildRules(item =>
            {
                item.RuleFor(i => i.ProductId)
                    .NotEmpty();

                item.RuleFor(i => i.Quantity)
                    .GreaterThan(0)
                    .LessThanOrEqualTo(1000);

                item.RuleFor(i => i.UnitPrice)
                    .GreaterThan(0);
            });

        // Cross-item validation
        RuleFor(x => x.Items)
            .Must(HaveUniqueProducts)
                .WithMessage("Order cannot contain duplicate products");

        RuleFor(x => x.Items)
            .Must(items => items.Sum(i => i.Quantity * i.UnitPrice) <= 100_000)
                .WithMessage("Order total cannot exceed $100,000");
    }

    private bool HaveUniqueProducts(List<OrderItemRequest> items)
    {
        return items.Select(i => i.ProductId).Distinct().Count() == items.Count;
    }
}
```

---

## Template: Conditional Validation

```csharp
// src/{name}.application/{Feature}/UpdatePayment/UpdatePaymentCommandValidator.cs
using FluentValidation;

namespace {name}.application.payments.updatepayment;

public sealed class UpdatePaymentCommandValidator : AbstractValidator<UpdatePaymentCommand>
{
    public UpdatePaymentCommandValidator()
    {
        RuleFor(x => x.PaymentMethod)
            .NotEmpty()
            .IsInEnum();

        // ═══════════════════════════════════════════════════════════════
        // CONDITIONAL: Credit Card rules
        // ═══════════════════════════════════════════════════════════════
        When(x => x.PaymentMethod == PaymentMethod.CreditCard, () =>
        {
            RuleFor(x => x.CardNumber)
                .NotEmpty()
                    .WithMessage("Card number is required for credit card payments")
                .CreditCard()
                    .WithMessage("Invalid credit card number");

            RuleFor(x => x.ExpiryMonth)
                .InclusiveBetween(1, 12);

            RuleFor(x => x.ExpiryYear)
                .GreaterThanOrEqualTo(DateTime.UtcNow.Year)
                    .WithMessage("Card has expired");

            RuleFor(x => x.Cvv)
                .NotEmpty()
                .Matches(@"^\d{3,4}$")
                    .WithMessage("CVV must be 3 or 4 digits");
        });

        // ═══════════════════════════════════════════════════════════════
        // CONDITIONAL: Bank Transfer rules
        // ═══════════════════════════════════════════════════════════════
        When(x => x.PaymentMethod == PaymentMethod.BankTransfer, () =>
        {
            RuleFor(x => x.AccountNumber)
                .NotEmpty()
                    .WithMessage("Account number is required for bank transfers")
                .Matches(@"^\d{8,17}$")
                    .WithMessage("Invalid account number format");

            RuleFor(x => x.RoutingNumber)
                .NotEmpty()
                .Matches(@"^\d{9}$")
                    .WithMessage("Routing number must be 9 digits");
        });

        // ═══════════════════════════════════════════════════════════════
        // UNLESS: Skip validation when condition is true
        // ═══════════════════════════════════════════════════════════════
        RuleFor(x => x.BillingAddress)
            .NotNull()
            .Unless(x => x.UseSavedAddress);
    }
}
```

---

## Built-in Validators Reference

### String Validators

```csharp
RuleFor(x => x.Name)
    .NotEmpty()                          // Not null, not empty, not whitespace
    .NotNull()                           // Not null only
    .Length(min, max)                    // Exact range
    .MinimumLength(5)                    // At least 5 chars
    .MaximumLength(100)                  // At most 100 chars
    .Matches(@"^[a-zA-Z]+$")            // Regex pattern
    .EmailAddress()                      // Valid email format
    .CreditCard()                        // Valid credit card (Luhn)
    .Equal("expected")                   // Exact match
    .NotEqual("forbidden");              // Not equal
```

### Numeric Validators

```csharp
RuleFor(x => x.Amount)
    .GreaterThan(0)                      // > 0
    .GreaterThanOrEqualTo(1)            // >= 1
    .LessThan(100)                       // < 100
    .LessThanOrEqualTo(99)              // <= 99
    .InclusiveBetween(1, 100)           // 1 <= x <= 100
    .ExclusiveBetween(0, 100)           // 0 < x < 100
    .PrecisionScale(10, 2, true);       // Decimal precision
```

### Collection Validators

```csharp
RuleFor(x => x.Items)
    .NotEmpty()                          // Has at least one item
    .NotNull()                           // Not null
    .Must(x => x.Count <= 10)           // Custom condition
    .ForEach(item => item.NotNull());   // Each item not null
```

### Comparison Validators

```csharp
RuleFor(x => x.EndDate)
    .GreaterThan(x => x.StartDate)      // Compare to another property
    .NotEqual(x => x.StartDate);

RuleFor(x => x.ConfirmPassword)
    .Equal(x => x.Password)
        .WithMessage("Passwords must match");
```

### Enum Validators

```csharp
RuleFor(x => x.Status)
    .NotEmpty()
    .IsInEnum()                          // Valid enum value
    .NotEqual(Status.Unknown);           // Exclude specific value
```

---

## Registering Validators

```csharp
// src/{name}.application/DependencyInjection.cs
using FluentValidation;
using Microsoft.Extensions.DependencyInjection;

namespace {name}.application;

public static class DependencyInjection
{
    public static IServiceCollection AddApplication(this IServiceCollection services)
    {
        // Register all validators from assembly
        services.AddValidatorsFromAssembly(
            typeof(DependencyInjection).Assembly,
            includeInternalTypes: true);  // Include internal validators

        services.AddMediatR(configuration =>
        {
            configuration.RegisterServicesFromAssembly(typeof(DependencyInjection).Assembly);
            configuration.AddOpenBehavior(typeof(ValidationBehavior<,>));
        });

        return services;
    }
}
```

---

## Error Messages Best Practices

```csharp
public sealed class CreateUserCommandValidator : AbstractValidator<CreateUserCommand>
{
    public CreateUserCommandValidator()
    {
        // ═══════════════════════════════════════════════════════════════
        // USE PLACEHOLDERS
        // ═══════════════════════════════════════════════════════════════
        RuleFor(x => x.Name)
            .NotEmpty()
                .WithMessage("{PropertyName} is required")      // "Name is required"
            .MaximumLength(100)
                .WithMessage("{PropertyName} must not exceed {MaxLength} characters");

        // ═══════════════════════════════════════════════════════════════
        // CUSTOM ERROR CODES (for API responses)
        // ═══════════════════════════════════════════════════════════════
        RuleFor(x => x.Email)
            .NotEmpty()
                .WithMessage("Email is required")
                .WithErrorCode("USER_EMAIL_REQUIRED")
            .EmailAddress()
                .WithMessage("Invalid email format")
                .WithErrorCode("USER_EMAIL_INVALID");

        // ═══════════════════════════════════════════════════════════════
        // CUSTOM STATE (additional context)
        // ═══════════════════════════════════════════════════════════════
        RuleFor(x => x.Age)
            .GreaterThanOrEqualTo(18)
                .WithState(x => new { MinAge = 18, ProvidedAge = x.Age });
    }
}
```

---

## Critical Rules

1. **Validators are internal** - Not exposed outside Application layer
2. **Sync rules first** - Fast validations before database calls
3. **Use async sparingly** - Prefer checking in handler
4. **One validator per command** - Keep validation focused
5. **Reuse with SetValidator** - Extract common validators
6. **Clear error messages** - User-friendly, actionable
7. **Error codes for APIs** - Machine-readable codes
8. **Conditional validation** - Use When/Unless appropriately
9. **Collection bounds** - Always limit collection sizes
10. **Don't duplicate domain rules** - Domain validates invariants

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Business logic in validator
RuleFor(x => x.Amount)
    .MustAsync(async (amount, ct) =>
    {
        var balance = await _accountService.GetBalance();
        return balance >= amount;  // Business rule belongs in handler!
    });

// ✅ CORRECT: Only input validation in validator
RuleFor(x => x.Amount)
    .GreaterThan(0)
    .LessThanOrEqualTo(1_000_000);

// ❌ WRONG: Modifying data in validator
RuleFor(x => x.Email)
    .Must(email =>
    {
        x.Email = email.ToLower();  // Don't modify!
        return true;
    });

// ✅ CORRECT: Validation only, transformation elsewhere
RuleFor(x => x.Email)
    .EmailAddress();

// ❌ WRONG: Catching exceptions in validator
RuleFor(x => x.Id)
    .Must(id =>
    {
        try { return Guid.Parse(id) != Guid.Empty; }
        catch { return false; }  // Use proper Guid type instead
    });

// ✅ CORRECT: Use proper types
public record Command(Guid Id);  // Guid, not string
RuleFor(x => x.Id).NotEmpty();
```

---

## Related Skills

- `cqrs-command-generator` - Commands with validators
- `pipeline-behaviors` - ValidationBehavior integration
- `result-pattern` - ValidationResult type
- `api-controller-generator` - Error responses
