---
name: domain-entity-generator
description: "Generates Domain Entities following DDD principles with factory methods, private setters, domain events, and proper encapsulation. Supports aggregate roots, child entities, and value objects."
version: 1.0.0
language: C#
framework: .NET 8+
pattern: Domain-Driven Design
---

# Domain Entity Generator

## Overview

This skill generates Domain Entities following Domain-Driven Design (DDD) principles:

- **Encapsulation** - Private setters, controlled modification
- **Factory Methods** - Static `Create()` methods with validation
- **Domain Events** - State changes raise events
- **Rich Domain Model** - Behavior lives in the entity, not services
- **Invariant Protection** - Entity always in valid state

## Quick Reference

| Concept | Purpose | Example |
|---------|---------|---------|
| Aggregate Root | Entry point for aggregate | `Organization`, `User` |
| Child Entity | Part of aggregate, no own identity outside | `OrderItem`, `AssessmentDetail` |
| Value Object | Immutable, no identity | `Email`, `Money`, `Address` |
| Domain Event | Signal state change | `UserCreatedDomainEvent` |

---

## Entity Structure

```
/Domain/{Aggregate}/
├── {Entity}.cs                    # Main entity
├── {Entity}Errors.cs              # Typed errors
├── I{Entity}Repository.cs         # Repository interface
├── ValueObjects/
│   ├── {ValueObject}.cs
│   └── ...
└── Events/
    ├── {Entity}CreatedDomainEvent.cs
    ├── {Entity}UpdatedDomainEvent.cs
    └── ...
```

---

## Template: Aggregate Root Entity

```csharp
// src/{name}.domain/{Aggregate}/{Entity}.cs
using {name}.domain.abstractions;
using {name}.domain.{aggregate}.events;

namespace {name}.domain.{aggregate};

public sealed class {Entity} : Entity
{
    // ═══════════════════════════════════════════════════════════════
    // PRIVATE COLLECTIONS (encapsulated)
    // ═══════════════════════════════════════════════════════════════
    private readonly List<{ChildEntity}> _{childEntities} = new();

    // ═══════════════════════════════════════════════════════════════
    // PROPERTIES (private setters)
    // ═══════════════════════════════════════════════════════════════
    public string Name { get; private set; }
    public string? Description { get; private set; }
    public bool IsActive { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime UpdatedAt { get; private set; }
    
    // Navigation property (read-only collection)
    public IReadOnlyCollection<{ChildEntity}> {ChildEntities} => _{childEntities}.AsReadOnly();

    // ═══════════════════════════════════════════════════════════════
    // CONSTRUCTORS
    // ═══════════════════════════════════════════════════════════════
    
    // Private constructor for EF Core
    private {Entity}() { }

    // Private constructor for factory method
    private {Entity}(
        Guid id,
        string name,
        string? description,
        DateTime createdAt)
        : base(id)
    {
        Name = name;
        Description = description;
        IsActive = true;
        CreatedAt = createdAt;
        UpdatedAt = createdAt;
    }

    // ═══════════════════════════════════════════════════════════════
    // FACTORY METHODS
    // ═══════════════════════════════════════════════════════════════
    
    /// <summary>
    /// Creates a new {Entity} with validation
    /// </summary>
    public static Result<{Entity}> Create(
        string name,
        string? description,
        DateTime createdAt)
    {
        // Validate invariants
        if (string.IsNullOrWhiteSpace(name))
        {
            return Result.Failure<{Entity}>({Entity}Errors.NameIsRequired);
        }

        if (name.Length > 100)
        {
            return Result.Failure<{Entity}>({Entity}Errors.NameTooLong);
        }

        var {entity} = new {Entity}(
            Guid.NewGuid(),
            name,
            description,
            createdAt);

        // Raise domain event
        {entity}.RaiseDomainEvent(new {Entity}CreatedDomainEvent({entity}.Id));

        return {entity};
    }

    // ═══════════════════════════════════════════════════════════════
    // DOMAIN METHODS
    // ═══════════════════════════════════════════════════════════════
    
    /// <summary>
    /// Updates the {Entity} properties
    /// </summary>
    public Result Update(
        string name,
        string? description,
        DateTime updatedAt)
    {
        if (string.IsNullOrWhiteSpace(name))
        {
            return Result.Failure({Entity}Errors.NameIsRequired);
        }

        if (name.Length > 100)
        {
            return Result.Failure({Entity}Errors.NameTooLong);
        }

        Name = name;
        Description = description;
        UpdatedAt = updatedAt;

        RaiseDomainEvent(new {Entity}UpdatedDomainEvent(Id));

        return Result.Success();
    }

    /// <summary>
    /// Deactivates the {Entity}
    /// </summary>
    public Result Deactivate(DateTime updatedAt)
    {
        if (!IsActive)
        {
            return Result.Failure({Entity}Errors.AlreadyDeactivated);
        }

        IsActive = false;
        UpdatedAt = updatedAt;

        RaiseDomainEvent(new {Entity}DeactivatedDomainEvent(Id));

        return Result.Success();
    }

    /// <summary>
    /// Reactivates the {Entity}
    /// </summary>
    public Result Activate(DateTime updatedAt)
    {
        if (IsActive)
        {
            return Result.Failure({Entity}Errors.AlreadyActive);
        }

        IsActive = true;
        UpdatedAt = updatedAt;

        return Result.Success();
    }

    // ═══════════════════════════════════════════════════════════════
    // CHILD ENTITY MANAGEMENT
    // ═══════════════════════════════════════════════════════════════
    
    /// <summary>
    /// Adds a child entity to this aggregate
    /// </summary>
    public Result Add{ChildEntity}({ChildEntity} {childEntity})
    {
        if ({childEntity} is null)
        {
            return Result.Failure({Entity}Errors.Child{ChildEntity}Required);
        }

        if (_{childEntities}.Any(c => c.Name == {childEntity}.Name))
        {
            return Result.Failure({Entity}Errors.Duplicate{ChildEntity}Name);
        }

        _{childEntities}.Add({childEntity});

        RaiseDomainEvent(new {ChildEntity}AddedDomainEvent(Id, {childEntity}.Id));

        return Result.Success();
    }

    /// <summary>
    /// Removes a child entity from this aggregate
    /// </summary>
    public Result Remove{ChildEntity}(Guid {childEntity}Id)
    {
        var {childEntity} = _{childEntities}.FirstOrDefault(c => c.Id == {childEntity}Id);

        if ({childEntity} is null)
        {
            return Result.Failure({Entity}Errors.{ChildEntity}NotFound);
        }

        _{childEntities}.Remove({childEntity});

        return Result.Success();
    }

    // ═══════════════════════════════════════════════════════════════
    // QUERY METHODS
    // ═══════════════════════════════════════════════════════════════
    
    public bool HasActiveChildren() => _{childEntities}.Any(c => c.IsActive);

    public {ChildEntity}? GetChildById(Guid childId) => 
        _{childEntities}.FirstOrDefault(c => c.Id == childId);
}
```

---

## Template: Child Entity (Part of Aggregate)

```csharp
// src/{name}.domain/{Aggregate}/{ChildEntity}.cs
using {name}.domain.abstractions;

namespace {name}.domain.{aggregate};

public sealed class {ChildEntity} : Entity
{
    // ═══════════════════════════════════════════════════════════════
    // PROPERTIES
    // ═══════════════════════════════════════════════════════════════
    public Guid {Parent}Id { get; private set; }
    public string Name { get; private set; }
    public string? Description { get; private set; }
    public int SortOrder { get; private set; }
    public bool IsActive { get; private set; }
    public DateTime CreatedAt { get; private set; }
    public DateTime UpdatedAt { get; private set; }

    // Navigation property
    public {Parent} {Parent} { get; private set; } = null!;

    // ═══════════════════════════════════════════════════════════════
    // CONSTRUCTORS
    // ═══════════════════════════════════════════════════════════════
    
    private {ChildEntity}() { } // EF Core

    private {ChildEntity}(
        Guid id,
        Guid {parent}Id,
        string name,
        string? description,
        int sortOrder,
        DateTime createdAt)
        : base(id)
    {
        {Parent}Id = {parent}Id;
        Name = name;
        Description = description;
        SortOrder = sortOrder;
        IsActive = true;
        CreatedAt = createdAt;
        UpdatedAt = createdAt;
    }

    // ═══════════════════════════════════════════════════════════════
    // FACTORY METHOD
    // ═══════════════════════════════════════════════════════════════
    
    public static {ChildEntity} Create(
        Guid {parent}Id,
        string name,
        string? description,
        int sortOrder,
        DateTime createdAt)
    {
        return new {ChildEntity}(
            Guid.NewGuid(),
            {parent}Id,
            name,
            description,
            sortOrder,
            createdAt);
    }

    // ═══════════════════════════════════════════════════════════════
    // DOMAIN METHODS
    // ═══════════════════════════════════════════════════════════════
    
    public void Update(
        string name,
        string? description,
        int sortOrder,
        DateTime updatedAt)
    {
        Name = name;
        Description = description;
        SortOrder = sortOrder;
        UpdatedAt = updatedAt;
    }

    public void Deactivate(DateTime updatedAt)
    {
        IsActive = false;
        UpdatedAt = updatedAt;
    }
}
```

---

## Template: Value Object

```csharp
// src/{name}.domain/{Aggregate}/ValueObjects/Email.cs
namespace {name}.domain.{aggregate}.valueobjects;

public sealed record Email
{
    public string Value { get; }

    private Email(string value)
    {
        Value = value;
    }

    public static Result<Email> Create(string email)
    {
        if (string.IsNullOrWhiteSpace(email))
        {
            return Result.Failure<Email>(EmailErrors.Empty);
        }

        email = email.Trim().ToLowerInvariant();

        if (email.Length > 255)
        {
            return Result.Failure<Email>(EmailErrors.TooLong);
        }

        if (!IsValidFormat(email))
        {
            return Result.Failure<Email>(EmailErrors.InvalidFormat);
        }

        return new Email(email);
    }

    private static bool IsValidFormat(string email)
    {
        // Simple email validation
        var atIndex = email.IndexOf('@');
        var dotIndex = email.LastIndexOf('.');
        
        return atIndex > 0 
            && dotIndex > atIndex + 1 
            && dotIndex < email.Length - 1;
    }

    public override string ToString() => Value;

    // Implicit conversion for convenience
    public static implicit operator string(Email email) => email.Value;
}

public static class EmailErrors
{
    public static readonly Error Empty = new("Email.Empty", "Email cannot be empty");
    public static readonly Error TooLong = new("Email.TooLong", "Email cannot exceed 255 characters");
    public static readonly Error InvalidFormat = new("Email.InvalidFormat", "Email format is invalid");
}
```

### More Value Object Examples

```csharp
// Money Value Object
public sealed record Money
{
    public decimal Amount { get; }
    public string Currency { get; }

    private Money(decimal amount, string currency)
    {
        Amount = amount;
        Currency = currency;
    }

    public static Result<Money> Create(decimal amount, string currency = "USD")
    {
        if (amount < 0)
            return Result.Failure<Money>(MoneyErrors.NegativeAmount);

        if (string.IsNullOrWhiteSpace(currency) || currency.Length != 3)
            return Result.Failure<Money>(MoneyErrors.InvalidCurrency);

        return new Money(Math.Round(amount, 2), currency.ToUpperInvariant());
    }

    public Money Add(Money other)
    {
        if (Currency != other.Currency)
            throw new InvalidOperationException("Cannot add different currencies");

        return new Money(Amount + other.Amount, Currency);
    }

    public static Money Zero(string currency = "USD") => new(0, currency);
}

// DateRange Value Object
public sealed record DateRange
{
    public DateTime Start { get; }
    public DateTime End { get; }

    private DateRange(DateTime start, DateTime end)
    {
        Start = start;
        End = end;
    }

    public static Result<DateRange> Create(DateTime start, DateTime end)
    {
        if (end <= start)
            return Result.Failure<DateRange>(DateRangeErrors.EndMustBeAfterStart);

        return new DateRange(start, end);
    }

    public bool Contains(DateTime date) => date >= Start && date <= End;
    
    public bool Overlaps(DateRange other) => 
        Start < other.End && End > other.Start;

    public int DurationInDays => (End - Start).Days;
}
```

---

## Template: Domain Errors

```csharp
// src/{name}.domain/{Aggregate}/{Entity}Errors.cs
using {name}.domain.abstractions;

namespace {name}.domain.{aggregate};

public static class {Entity}Errors
{
    // Not found errors
    public static readonly Error NotFound = new(
        "{Entity}.NotFound",
        "The {entity} with the specified ID was not found");

    // Validation errors
    public static readonly Error NameIsRequired = new(
        "{Entity}.NameRequired",
        "{Entity} name is required");

    public static readonly Error NameTooLong = new(
        "{Entity}.NameTooLong",
        "{Entity} name cannot exceed 100 characters");

    // Business rule errors
    public static readonly Error AlreadyExists = new(
        "{Entity}.AlreadyExists",
        "A {entity} with this name already exists");

    public static readonly Error AlreadyDeactivated = new(
        "{Entity}.AlreadyDeactivated",
        "The {entity} is already deactivated");

    public static readonly Error AlreadyActive = new(
        "{Entity}.AlreadyActive",
        "The {entity} is already active");

    public static readonly Error CannotDeleteWithActiveRelationships = new(
        "{Entity}.CannotDeleteWithActiveRelationships",
        "Cannot delete {entity} with active relationships");

    // Child entity errors
    public static readonly Error {ChildEntity}NotFound = new(
        "{Entity}.{ChildEntity}NotFound",
        "The {childEntity} was not found in this {entity}");

    public static readonly Error Duplicate{ChildEntity}Name = new(
        "{Entity}.Duplicate{ChildEntity}Name",
        "A {childEntity} with this name already exists");

    public static readonly Error Child{ChildEntity}Required = new(
        "{Entity}.Child{ChildEntity}Required",
        "{ChildEntity} cannot be null");
}
```

---

## Template: Domain Events

```csharp
// src/{name}.domain/{Aggregate}/Events/{Entity}CreatedDomainEvent.cs
using {name}.domain.abstractions;

namespace {name}.domain.{aggregate}.events;

public sealed record {Entity}CreatedDomainEvent(Guid {Entity}Id) : IDomainEvent;

// src/{name}.domain/{Aggregate}/Events/{Entity}UpdatedDomainEvent.cs
public sealed record {Entity}UpdatedDomainEvent(Guid {Entity}Id) : IDomainEvent;

// src/{name}.domain/{Aggregate}/Events/{Entity}DeactivatedDomainEvent.cs
public sealed record {Entity}DeactivatedDomainEvent(Guid {Entity}Id) : IDomainEvent;

// src/{name}.domain/{Aggregate}/Events/{ChildEntity}AddedDomainEvent.cs
public sealed record {ChildEntity}AddedDomainEvent(
    Guid {Entity}Id,
    Guid {ChildEntity}Id) : IDomainEvent;
```

---

## Template: Repository Interface

```csharp
// src/{name}.domain/{Aggregate}/I{Entity}Repository.cs
namespace {name}.domain.{aggregate};

public interface I{Entity}Repository
{
    // ═══════════════════════════════════════════════════════════════
    // READ OPERATIONS
    // ═══════════════════════════════════════════════════════════════
    
    Task<{Entity}?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken = default);

    Task<{Entity}?> GetByNameAsync(
        string name,
        CancellationToken cancellationToken = default);

    Task<IReadOnlyList<{Entity}>> GetByOrganizationIdAsync(
        Guid organizationId,
        CancellationToken cancellationToken = default);

    Task<bool> ExistsAsync(
        Guid id,
        CancellationToken cancellationToken = default);

    // ═══════════════════════════════════════════════════════════════
    // WRITE OPERATIONS
    // ═══════════════════════════════════════════════════════════════
    
    void Add({Entity} {entity});

    void AddRange(IEnumerable<{Entity}> {entities});

    void Update({Entity} {entity});

    void Remove({Entity} {entity});
}
```

---

## Entity Base Class

```csharp
// src/{name}.domain/Abstractions/Entity.cs
namespace {name}.domain.abstractions;

public abstract class Entity
{
    private readonly List<IDomainEvent> _domainEvents = new();

    protected Entity(Guid id)
    {
        Id = id;
    }

    protected Entity() { } // EF Core

    public Guid Id { get; init; }

    public IReadOnlyList<IDomainEvent> GetDomainEvents() => _domainEvents.ToList();

    public void ClearDomainEvents() => _domainEvents.Clear();

    protected void RaiseDomainEvent(IDomainEvent domainEvent)
    {
        _domainEvents.Add(domainEvent);
    }

    public override bool Equals(object? obj)
    {
        if (obj is not Entity other)
            return false;

        if (ReferenceEquals(this, other))
            return true;

        if (GetType() != other.GetType())
            return false;

        if (Id == Guid.Empty || other.Id == Guid.Empty)
            return false;

        return Id == other.Id;
    }

    public static bool operator ==(Entity? left, Entity? right)
    {
        if (left is null && right is null)
            return true;

        if (left is null || right is null)
            return false;

        return left.Equals(right);
    }

    public static bool operator !=(Entity? left, Entity? right) => !(left == right);

    public override int GetHashCode() => Id.GetHashCode() * 41;
}
```

---

## Critical DDD Rules

1. **Private setters always** - No direct property modification from outside
2. **Factory methods for creation** - `Create()` static methods with validation
3. **Domain events for state changes** - Signal significant changes
4. **Entities are always valid** - Invariants protected in constructors and methods
5. **Aggregate root controls children** - Child entities managed through root
6. **Value objects are immutable** - Use `record` types
7. **Repository per aggregate root** - Not per entity
8. **No logic in setters** - Use named methods
9. **Use Result pattern** - Return errors, don't throw
10. **Keep entities persistence-ignorant** - No EF Core attributes on domain

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Public setters
public string Name { get; set; }

// ✅ CORRECT: Private setters
public string Name { get; private set; }

// ❌ WRONG: Constructor with all parameters
public User(Guid id, string name, string email, DateTime createdAt, ...)

// ✅ CORRECT: Factory method
public static Result<User> Create(string name, string email, DateTime createdAt)

// ❌ WRONG: Throwing exceptions
if (name == null) throw new ArgumentNullException(nameof(name));

// ✅ CORRECT: Return Result
if (string.IsNullOrWhiteSpace(name))
    return Result.Failure<Entity>(EntityErrors.NameRequired);

// ❌ WRONG: Anemic domain model
public class User
{
    public string Name { get; set; }
    public void SetName(string name) => Name = name; // Just a setter!
}

// ✅ CORRECT: Rich domain model with behavior
public class User
{
    public string Name { get; private set; }
    
    public Result ChangeName(string newName, DateTime updatedAt)
    {
        if (string.IsNullOrWhiteSpace(newName))
            return Result.Failure(UserErrors.NameRequired);
        
        Name = newName;
        UpdatedAt = updatedAt;
        RaiseDomainEvent(new UserNameChangedDomainEvent(Id, newName));
        return Result.Success();
    }
}

// ❌ WRONG: Exposing internal collections
public List<OrderItem> Items { get; set; } = new();

// ✅ CORRECT: Encapsulated collections
private readonly List<OrderItem> _items = new();
public IReadOnlyCollection<OrderItem> Items => _items.AsReadOnly();
```

---

## Related Skills

- `repository-pattern` - Implement repositories
- `ef-core-configuration` - Map entities to database
- `domain-events-generator` - Handle domain events
- `result-pattern` - Error handling
