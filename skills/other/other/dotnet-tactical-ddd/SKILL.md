---
name: dotnet-tactical-ddd
description: Use when building .NET backend APIs with business logic, domain rules, invariants to enforce, or projects expanding beyond simple CRUD. Symptoms - anemic models with public setters, domain logic in controllers, AutoMapper bypassing validation, primitives instead of value objects
---

# .NET Tactical Domain-Driven Design

## Overview

**Rich domain models with behavior, not anemic data containers.** Apply tactical DDD patterns to all .NET backend development for maintainable, testable, domain-centric code.

**Core principle:** Domain models encapsulate business rules and invariants. DTOs are immutable data contracts at API boundaries. Manual mapping via extension methods. Never expose domain models in APIs.

**Base classes:** See [base-classes.cs](base-classes.cs) for `Result<T>`, `ValueObject`, `AggregateRoot<T>`, `IDomainEvent` implementations. Copy into your `Domain/` project.

## 0. The Dependency Rule (Foundation)

**Dependencies point inward only.** Outer layers depend on inner layers, never the reverse.

```
Infrastructure → Application → Domain
   (adapters)     (use cases)    (core)
```

**Violations to catch:**
- Domain/ importing `Microsoft.EntityFrameworkCore`, `System.Net.Http`, `Serilog`
- Controllers calling repositories directly (bypassing Application/ use cases)
- Entities depending on application services
- Application/ directly instantiating Infrastructure/ classes (should use DI)

**Verification test:** "Can I run domain logic from unit tests with no database/HTTP/file system?" If yes, boundaries are correct.

## Layer Decision Tree

**Where does this code go?**

| Code Type | Layer | Example |
|-----------|-------|---------|
| Pure business logic, no I/O | `Domain/Entities/` or `Domain/ValueObjects/` | `OrderLine.CalculateTotal()` |
| Business rule across entities | `Domain/Services/` | `IPricingService.CalculateDiscount()` |
| Orchestrates domain + calls infra | `Application/{UseCase}/Handler` | `CreateOrderHandler` |
| Interface for external dependency | `Domain/Interfaces/` (if domain needs it)<br>`Application/Common/Interfaces/` (if only app uses) | `IEmailService` interface |
| Database implementation | `Infrastructure/Persistence/` | `OrderRepository` |
| HTTP/external API call | `Infrastructure/Services/` | `SmtpEmailService` |
| Request/Response DTO | `WebApi/DTOs/` | `CreateOrderRequest` |
| Extension methods for mapping | `WebApi/Extensions/` or `Application/Common/Mapping/` | `ProductMapper.ToDto()` |

## When to Use

**Apply tactical DDD when:**
- Building business logic beyond CRUD operations
- Domain rules and invariants need enforcement
- Business concepts need clear boundaries
- Project may expand beyond simple CRUD (most do)

**Skip tactical DDD ONLY when:**
- Absolutely certain code remains simple CRUD forever
- Overhead clearly outweighs complexity
- **When uncertain, ASK user first** - only they know if project will expand

## Quick Reference

| Pattern | Purpose | Example |
|---------|---------|---------|
| **Value Objects** | Immutable, value equality | `Money`, `EmailAddress`, `Quantity` |
| **Entities** | Identity, private setters | `Customer`, `OrderLine` |
| **Aggregates** | Transaction boundaries | `Order`, `Product`, `ShoppingCart` |
| **Factories** | Create valid objects | `Product.Create()`, `IOrderFactory` |
| **Repositories** | Persist/retrieve aggregates | `IOrderRepository` |
| **Domain Events** | Decouple aggregates | `OrderShippedEvent` |
| **Domain Services** | Multi-aggregate logic | `IPricingService` |
| **DTOs** | API boundaries | `CreateProductRequest`, `ProductDto` |
| **Result<T>** | Railway-oriented errors | `Result<Product>` |

## 1. Value Objects

```csharp
// ✅ Good: Immutable, private ctor, factory with Result<T>
public class Money : ValueObject
{
    public decimal Amount { get; }
    public string Currency { get; }

    private Money(decimal amount, string currency) {
        Amount = amount;
        Currency = currency;
    }

    public static Result<Money> Create(decimal amount, string currency) {
        if (amount < 0) return Result.Failure<Money>("Amount cannot be negative");
        if (string.IsNullOrWhiteSpace(currency))
            return Result.Failure<Money>("Currency required");
        return Result.Success(new Money(amount, currency.ToUpperInvariant()));
    }

    protected override IEnumerable<object> GetEqualityComponents() {
        yield return Amount;
        yield return Currency;
    }
}

// ❌ Bad: Mutable, no validation
public class Money {
    public decimal Amount { get; set; }
    public string Currency { get; set; }
}
```

## 2. Entities & Aggregates

Aggregate rules: reference other aggregates by ID only, enforce invariants, single entry point for modifications.

```csharp
// ✅ Good: Aggregate with behavior and invariants
public class Order : AggregateRoot<Guid>
{
    public Guid CustomerId { get; private set; }
    public OrderStatus Status { get; private set; }
    private readonly List<OrderLine> _lines = new();
    public IReadOnlyList<OrderLine> Lines => _lines.AsReadOnly();

    private Order() { } // EF Core
    private Order(Guid id, Guid customerId) : base(id) {
        CustomerId = customerId;
        Status = OrderStatus.Pending;
    }

    public static Result<Order> Create(Guid customerId) {
        if (customerId == Guid.Empty)
            return Result.Failure<Order>("Customer ID required");

        var order = new Order(Guid.NewGuid(), customerId);
        order.AddDomainEvent(new OrderCreatedEvent(order.Id, customerId, DateTime.UtcNow));
        return Result.Success(order);
    }

    public Result AddLine(Product product, int quantity) {
        if (Status == OrderStatus.Completed)
            return Result.Failure("Cannot modify completed order");
        if (quantity <= 0)
            return Result.Failure("Quantity must be positive");

        _lines.Add(OrderLine.Create(product.Id, product.Price, quantity));
        return Result.Success();
    }
}

// ❌ Bad: Anemic entity with public setters
public class Order {
    public Guid Id { get; set; }
    public Guid CustomerId { get; set; }
    public List<OrderLine> Lines { get; set; }
}
```

## 3. Factories

Static factory methods returning `Result<T>`. Private constructors prevent invalid state.

```csharp
// ✅ Good: Factory with validation
public class Product : AggregateRoot<Guid>
{
    public string Name { get; private set; }
    public Money Price { get; private set; }

    private Product(Guid id, string name, Money price) : base(id) {
        Name = name;
        Price = price;
    }

    public static Result<Product> Create(string name, Money price) {
        if (string.IsNullOrWhiteSpace(name))
            return Result.Failure<Product>("Name required");
        if (name.Length > 200)
            return Result.Failure<Product>("Name too long");
        if (price.Amount <= 0)
            return Result.Failure<Product>("Price must be positive");

        return Result.Success(new Product(Guid.NewGuid(), name, price));
    }
}

// ❌ Bad: Public constructor allows invalid state
public class Product {
    public string Name { get; set; }
    public Product() { }
}
```

## 4. Repositories

One interface per aggregate. Eager load to avoid N+1.

```csharp
// ✅ Good: Specific interface per aggregate
public interface IOrderRepository {
    Task<Order?> GetByIdAsync(Guid id, CancellationToken ct = default);
    Task AddAsync(Order order, CancellationToken ct = default);
    Task SaveChangesAsync(CancellationToken ct = default);
}

public class OrderRepository : IOrderRepository {
    private readonly ApplicationDbContext _context;

    public async Task<Order?> GetByIdAsync(Guid id, CancellationToken ct) {
        return await _context.Orders
            .Include(o => o.Lines) // Eager loading
            .FirstOrDefaultAsync(o => o.Id == id, ct);
    }

    public async Task SaveChangesAsync(CancellationToken ct) {
        await _context.SaveChangesAsync(ct);
    }
}

// ❌ Bad: Generic repository
public interface IRepository<T> {
    Task<IEnumerable<T>> GetAllAsync();
}
```

## 5. EF Core Configuration

Private setters and private collections require explicit EF Core configuration. Without this, runtime errors occur.

```csharp
// Infrastructure/Persistence/Configurations/OrderConfiguration.cs
public class OrderConfiguration : IEntityTypeConfiguration<Order>
{
    public void Configure(EntityTypeBuilder<Order> builder)
    {
        builder.HasKey(o => o.Id);

        // Private collection: tell EF about the backing field
        builder.HasMany(o => o.Lines)
            .WithOne()
            .HasForeignKey("OrderId");
        builder.Navigation(o => o.Lines)
            .UsePropertyAccessMode(PropertyAccessMode.Field);
        // SetField only needed if backing field doesn't follow _camelCase convention:
        // builder.Metadata.FindNavigation(nameof(Order.Lines))!.SetField("_myCustomField");

        // Value object as owned type (if Order had a TotalPrice property)
        // builder.OwnsOne(o => o.TotalPrice, p => {
        //     p.Property(m => m.Amount).HasColumnName("TotalAmount");
        //     p.Property(m => m.Currency).HasColumnName("TotalCurrency");
        // });

        // Enum stored as string
        builder.Property(o => o.Status)
            .HasConversion<string>();
    }
}

// Value object owned type pattern (Money on OrderLine):
public class OrderLineConfiguration : IEntityTypeConfiguration<OrderLine>
{
    public void Configure(EntityTypeBuilder<OrderLine> builder)
    {
        builder.OwnsOne(l => l.Price, p => {
            p.Property(m => m.Amount).HasColumnName("Price");
            p.Property(m => m.Currency).HasColumnName("PriceCurrency");
        });
    }
}
```

**EF Core rules:**
- Private collections need `UsePropertyAccessMode(PropertyAccessMode.Field)` (+ `SetField()` only for non-convention field names)
- Value objects use `OwnsOne()` - maps to columns in parent table
- All entities need parameterless `protected` constructor for EF (see base-classes.cs)
- Register configs: `modelBuilder.ApplyConfigurationsFromAssembly(typeof(ApplicationDbContext).Assembly);`

## 6. Domain Events

Immutable records (past tense) decoupling aggregates. Use handlers for cross-aggregate logic.

```csharp
// ✅ Good: Immutable record, past tense
public record OrderShippedEvent(
    Guid OrderId,
    Guid CustomerId,
    DateTime OccurredAt
) : IDomainEvent;

public class Order : AggregateRoot<Guid> {
    public void Ship() {
        Status = OrderStatus.Shipped;
        AddDomainEvent(new OrderShippedEvent(Id, CustomerId, DateTime.UtcNow));
    }
}

public class AwardLoyaltyPointsHandler : IDomainEventHandler<OrderShippedEvent> {
    public async Task Handle(OrderShippedEvent @event, CancellationToken ct) {
        var customer = await _customerRepo.GetByIdAsync(@event.CustomerId, ct);
        customer?.AwardPoints(100);
        await _customerRepo.SaveChangesAsync(ct);
    }
}

// ❌ Bad: Mutable, present tense
public class ShipOrder {
    public Guid OrderId { get; set; }
}
```

## 7. DTOs at API Boundaries

Never expose domain models in controllers. Immutable records + extension methods for mapping.

```csharp
// DTOs
public record CreateProductRequest(string Name, decimal Price, string Currency);
public record ProductDto(Guid Id, string Name, decimal Price, string Currency);

// Extension methods for mapping
public static class ProductMapper
{
    public static ProductDto ToDto(this Product product) => new(
        product.Id, product.Name, product.Price.Amount, product.Price.Currency);

    public static Result<Product> ToDomain(this CreateProductRequest request)
    {
        var priceResult = Money.Create(request.Price, request.Currency);
        if (priceResult.IsFailure) return Result.Failure<Product>(priceResult.Error);
        return Product.Create(request.Name, priceResult.Value);
    }
}

// Controller
[HttpPost]
public async Task<ActionResult<ProductDto>> Create(CreateProductRequest request)
{
    var result = request.ToDomain();
    if (result.IsFailure) return BadRequest(result.Error);

    await _repository.AddAsync(result.Value);
    await _repository.SaveChangesAsync();
    return CreatedAtAction(nameof(Get), new { id = result.Value.Id }, result.Value.ToDto());
}

// ❌ Bad: Domain in API
[HttpPost]
public async Task<ActionResult<Product>> Create(Product product) {
    return Ok(product);
}
```

**Security:** DTOs prevent over-posting attacks. Domain controls privileged fields.

```csharp
// ✅ Good: Safe DTO
public record CreateUserRequest(string Name);

// Domain controls IsAdmin, not client
var result = User.Create(request.Name);
```

**Pagination:**
```csharp
public record ProductQuery(string? SearchTerm, int PageNumber = 1, int PageSize = 20);
public record PagedResult<T>(List<T> Items, int Total, int Page, int PageSize);
```

## 8. Update/Mutation Pattern

Entity behavior methods + `UpdateFromRequest` extension method. Never direct property assignment.

```csharp
// DTO
public record UpdateProductRequest(string Name, decimal Price, string Currency);

// Entity behavior method
public class Product : AggregateRoot<Guid>
{
    // ... existing fields and Create factory ...

    public Result UpdateName(string name) {
        if (string.IsNullOrWhiteSpace(name))
            return Result.Failure("Name required");
        if (name.Length > 200)
            return Result.Failure("Name too long");
        Name = name;
        AddDomainEvent(new ProductUpdatedEvent(Id, DateTime.UtcNow));
        return Result.Success();
    }

    public Result UpdatePrice(Money price) {
        if (price.Amount <= 0)
            return Result.Failure("Price must be positive");
        Price = price;
        return Result.Success();
    }
}

// Extension method orchestrates the update (same ProductMapper class from Section 7)
public static class ProductMapper
{
    // ... existing ToDto, ToDomain ...

    public static Result UpdateFromRequest(this Product product, UpdateProductRequest request)
    {
        var nameResult = product.UpdateName(request.Name);
        if (nameResult.IsFailure) return nameResult;

        var priceResult = Money.Create(request.Price, request.Currency);
        if (priceResult.IsFailure) return Result.Failure(priceResult.Error);

        return product.UpdatePrice(priceResult.Value);
    }
}

// Controller
[HttpPut("{id:guid}")]
public async Task<ActionResult<ProductDto>> Update(Guid id, UpdateProductRequest request)
{
    var product = await _repository.GetByIdAsync(id);
    if (product is null) return NotFound();

    var result = product.UpdateFromRequest(request);
    if (result.IsFailure) return BadRequest(result.Error);

    await _repository.SaveChangesAsync();
    return Ok(product.ToDto());
}
```

**Key rules:** Entity owns validation. Extension method orchestrates. Controller handles HTTP concerns only.

## Red Flags - STOP and Fix

| Violation | Fix |
|-----------|-----|
| Public setters on domain entities | Private setters + behavior methods |
| `decimal` instead of `Money` | Value objects for domain concepts |
| `new Product { Name = ... }` initializer | `Product.Create()` factory method |
| `throw new Exception()` for business rules | Return `Result<T>` |
| Domain models in controller params/returns | DTOs with manual mapping |
| Inline DTO mapping in controllers | Extension methods (`ToDto()`, `ToDomain()`) |
| Generic `IRepository<T>` | Specific interfaces per aggregate |
| DbContext injected into controllers | Repository pattern |
| Full entity references across aggregates | Reference by ID only |
| No EF Core config for private fields | `UsePropertyAccessMode` + `SetField` |

**When you see these: Refactor immediately. These are architectural violations.**

## Common Rationalizations (Resist These!)

| Excuse | Reality |
|--------|---------|
| "Too simple for DDD" / "Just CRUD" | DDD scales down. If uncertain, ask the user — most domains grow complex. |
| "Time pressure - skip patterns" | Patterns prevent future bugs. Shortcuts create more debt than they save. |
| "Public setters are standard C#" | In DTOs yes, in domain models no. Encapsulation is non-negotiable. |
| "AutoMapper is industry standard" | Manual mapping gives control. AutoMapper bypasses factories and validation. |

**All of these mean: Apply tactical DDD correctly.**

## Project Structure

```
Solution.sln
├── Domain/                     # Pure business logic
│   ├── Entities/
│   ├── ValueObjects/
│   ├── Exceptions/
│   └── Interfaces/
├── Application/                # Use cases, orchestration
│   ├── Products/
│   │   ├── Commands/
│   │   └── Queries/
│   └── Common/
│       └── Interfaces/
├── Infrastructure/             # External concerns
│   ├── Persistence/
│   │   ├── Configurations/
│   │   └── Repositories/
│   └── Services/
└── WebApi/                     # API layer
    ├── Controllers/
    ├── DTOs/
    └── Extensions/
```

## Naming Conventions

- Requests: `CreateXRequest`, `UpdateXRequest`, `XQuery`
- Responses: `XDto`, `XDetailDto`, `XSummaryDto`
- Domain: `X` (entity), no suffixes
- Events: `XCreatedEvent`, `XUpdatedEvent` (past tense)
- Mappers: `XMapper.ToDto()`, `XMapper.ToDomain()`, `XMapper.UpdateFromRequest()`

## Common Flows

```
Create: CreateProductRequest → ToDomain() → Product.Create() → Result<Product> → AddAsync → SaveChanges
Read:   GetByIdAsync → product.ToDto() → ProductDto
Update: GetByIdAsync → product.UpdateFromRequest(request) → Result → SaveChanges
```
