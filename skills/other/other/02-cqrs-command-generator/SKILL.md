---
name: cqrs-command-generator
description: "Generates CQRS Commands with Handlers, Validators, and Request DTOs following Clean Architecture patterns. Commands represent actions that modify state and return Result types for proper error handling."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: MediatR, FluentValidation
---

# CQRS Command Generator

## Overview

This skill generates Commands following the CQRS (Command Query Responsibility Segregation) pattern. Commands represent intentions to change system state. Each command has:

- **Command Record** - Immutable data structure with request parameters
- **Validator** - FluentValidation rules for input validation
- **Handler** - Business logic implementation returning Result
- **Request DTO** (optional) - API layer request model

## Quick Reference

| Command Type | Returns | Use Case |
|--------------|---------|----------|
| `ICommand` | `Result` | Operations without return value (Update, Delete) |
| `ICommand<T>` | `Result<T>` | Operations returning data (Create returns Id) |

---

## Command Structure

```
/Application/{Feature}/
├── Create{Entity}/
│   ├── Create{Entity}Command.cs        # Record + Validator + Handler
│   └── Create{Entity}Request.cs        # Optional API DTO
├── Update{Entity}/
│   ├── Update{Entity}Command.cs
│   └── Update{Entity}Request.cs
└── Delete{Entity}/
    └── Delete{Entity}Command.cs
```

---

## Template: Command with Return Value (Create)

Use for operations that return data (typically entity ID after creation).

```csharp
// src/{name}.application/{Feature}/Create{Entity}/Create{Entity}Command.cs
using FluentValidation;
using {name}.application.abstractions.clock;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;
using {name}.domain.{entities};

namespace {name}.application.{feature}.Create{Entity};

// ═══════════════════════════════════════════════════════════════
// COMMAND RECORD
// ═══════════════════════════════════════════════════════════════
public sealed record Create{Entity}Command(
    string Name,
    string? Description,
    Guid? ParentId) : ICommand<Guid>;

// ═══════════════════════════════════════════════════════════════
// VALIDATOR
// ═══════════════════════════════════════════════════════════════
internal sealed class Create{Entity}CommandValidator : AbstractValidator<Create{Entity}Command>
{
    public Create{Entity}CommandValidator()
    {
        RuleFor(x => x.Name)
            .NotEmpty()
            .WithMessage("{Entity} name is required")
            .MaximumLength(100)
            .WithMessage("{Entity} name must not exceed 100 characters");

        RuleFor(x => x.Description)
            .MaximumLength(500)
            .When(x => x.Description is not null);
    }
}

// ═══════════════════════════════════════════════════════════════
// HANDLER
// ═══════════════════════════════════════════════════════════════
internal sealed class Create{Entity}CommandHandler 
    : ICommandHandler<Create{Entity}Command, Guid>
{
    private readonly I{Entity}Repository _{entity}Repository;
    private readonly IDateTimeProvider _dateTimeProvider;
    private readonly IUnitOfWork _unitOfWork;

    public Create{Entity}CommandHandler(
        I{Entity}Repository {entity}Repository,
        IDateTimeProvider dateTimeProvider,
        IUnitOfWork unitOfWork)
    {
        _{entity}Repository = {entity}Repository;
        _dateTimeProvider = dateTimeProvider;
        _unitOfWork = unitOfWork;
    }

    public async Task<Result<Guid>> Handle(
        Create{Entity}Command request,
        CancellationToken cancellationToken)
    {
        // 1. Validate business rules
        var existingEntity = await _{entity}Repository
            .GetByNameAsync(request.Name, cancellationToken);

        if (existingEntity is not null)
        {
            return Result.Failure<Guid>({Entity}Errors.AlreadyExists);
        }

        // 2. Create domain entity using factory method
        var {entity}Result = {Entity}.Create(
            request.Name,
            request.Description,
            _dateTimeProvider.UtcNow);

        if ({entity}Result.IsFailure)
        {
            return Result.Failure<Guid>({entity}Result.Error);
        }

        // 3. Persist to repository
        _{entity}Repository.Add({entity}Result.Value);

        // 4. Save changes (via Unit of Work)
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        // 5. Return created entity ID
        return {entity}Result.Value.Id;
    }
}
```

---

## Template: Command without Return Value (Update)

Use for operations that don't return data.

```csharp
// src/{name}.application/{Feature}/Update{Entity}/Update{Entity}Command.cs
using FluentValidation;
using {name}.application.abstractions.clock;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;
using {name}.domain.{entities};

namespace {name}.application.{feature}.Update{Entity};

// ═══════════════════════════════════════════════════════════════
// COMMAND RECORD
// ═══════════════════════════════════════════════════════════════
public sealed record Update{Entity}Command(
    Guid Id,
    string Name,
    string? Description) : ICommand;

// ═══════════════════════════════════════════════════════════════
// VALIDATOR
// ═══════════════════════════════════════════════════════════════
internal sealed class Update{Entity}CommandValidator : AbstractValidator<Update{Entity}Command>
{
    public Update{Entity}CommandValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty()
            .WithMessage("{Entity} ID is required");

        RuleFor(x => x.Name)
            .NotEmpty()
            .MaximumLength(100);
    }
}

// ═══════════════════════════════════════════════════════════════
// HANDLER
// ═══════════════════════════════════════════════════════════════
internal sealed class Update{Entity}CommandHandler 
    : ICommandHandler<Update{Entity}Command>
{
    private readonly I{Entity}Repository _{entity}Repository;
    private readonly IDateTimeProvider _dateTimeProvider;
    private readonly IUnitOfWork _unitOfWork;

    public Update{Entity}CommandHandler(
        I{Entity}Repository {entity}Repository,
        IDateTimeProvider dateTimeProvider,
        IUnitOfWork unitOfWork)
    {
        _{entity}Repository = {entity}Repository;
        _dateTimeProvider = dateTimeProvider;
        _unitOfWork = unitOfWork;
    }

    public async Task<r> Handle(
        Update{Entity}Command request,
        CancellationToken cancellationToken)
    {
        // 1. Retrieve existing entity
        var {entity} = await _{entity}Repository
            .GetByIdAsync(request.Id, cancellationToken);

        if ({entity} is null)
        {
            return Result.Failure({Entity}Errors.NotFound);
        }

        // 2. Call domain method to update
        var updateResult = {entity}.Update(
            request.Name,
            request.Description,
            _dateTimeProvider.UtcNow);

        if (updateResult.IsFailure)
        {
            return Result.Failure(updateResult.Error);
        }

        // 3. Save changes
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        return Result.Success();
    }
}
```

---

## Template: Delete Command

```csharp
// src/{name}.application/{Feature}/Delete{Entity}/Delete{Entity}Command.cs
using FluentValidation;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;
using {name}.domain.{entities};

namespace {name}.application.{feature}.Delete{Entity};

public sealed record Delete{Entity}Command(Guid Id) : ICommand;

internal sealed class Delete{Entity}CommandValidator : AbstractValidator<Delete{Entity}Command>
{
    public Delete{Entity}CommandValidator()
    {
        RuleFor(x => x.Id).NotEmpty();
    }
}

internal sealed class Delete{Entity}CommandHandler 
    : ICommandHandler<Delete{Entity}Command>
{
    private readonly I{Entity}Repository _{entity}Repository;
    private readonly IUnitOfWork _unitOfWork;

    public Delete{Entity}CommandHandler(
        I{Entity}Repository {entity}Repository,
        IUnitOfWork unitOfWork)
    {
        _{entity}Repository = {entity}Repository;
        _unitOfWork = unitOfWork;
    }

    public async Task<r> Handle(
        Delete{Entity}Command request,
        CancellationToken cancellationToken)
    {
        var {entity} = await _{entity}Repository
            .GetByIdAsync(request.Id, cancellationToken);

        if ({entity} is null)
        {
            return Result.Failure({Entity}Errors.NotFound);
        }

        // Check business rules before deletion
        if ({entity}.HasActiveRelationships())
        {
            return Result.Failure({Entity}Errors.CannotDeleteWithActiveRelationships);
        }

        _{entity}Repository.Remove({entity});

        await _unitOfWork.SaveChangesAsync(cancellationToken);

        return Result.Success();
    }
}
```

---

## Template: Command with Complex Request Object

For commands with many parameters, use a nested request object.

```csharp
// src/{name}.application/{Feature}/Create{Entity}/Create{Entity}Command.cs
using FluentValidation;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.{feature}.Create{Entity};

// Request object for complex data
public sealed class Create{Entity}Request
{
    public required string Name { get; init; }
    public string? Description { get; init; }
    public required Guid OrganizationId { get; init; }
    public List<Create{Child}Request> Children { get; init; } = new();
}

public sealed class Create{Child}Request
{
    public required string Name { get; init; }
    public int SortOrder { get; init; }
}

// Command wraps the request
public sealed record Create{Entity}Command(
    Create{Entity}Request Request) : ICommand<Guid>;

// Validator for nested structures
internal sealed class Create{Entity}CommandValidator 
    : AbstractValidator<Create{Entity}Command>
{
    public Create{Entity}CommandValidator()
    {
        RuleFor(x => x.Request.Name)
            .NotEmpty()
            .MaximumLength(100);

        RuleFor(x => x.Request.OrganizationId)
            .NotEmpty();

        RuleForEach(x => x.Request.Children)
            .ChildRules(child =>
            {
                child.RuleFor(c => c.Name).NotEmpty();
                child.RuleFor(c => c.SortOrder).GreaterThanOrEqualTo(0);
            });
    }
}

// Handler processes the complex request
internal sealed class Create{Entity}CommandHandler 
    : ICommandHandler<Create{Entity}Command, Guid>
{
    // ... dependencies

    public async Task<Result<Guid>> Handle(
        Create{Entity}Command command,
        CancellationToken cancellationToken)
    {
        var request = command.Request;
        
        // Process parent entity
        var {entity} = {Entity}.Create(
            request.Name,
            request.Description,
            request.OrganizationId);

        // Process children
        foreach (var childRequest in request.Children)
        {
            var child = {Child}.Create(
                childRequest.Name,
                childRequest.SortOrder);
            
            {entity}.AddChild(child);
        }

        _{entity}Repository.Add({entity});
        await _unitOfWork.SaveChangesAsync(cancellationToken);

        return {entity}.Id;
    }
}
```

---

## Validation Rules Reference

### Common Validators

```csharp
// String validations
RuleFor(x => x.Name)
    .NotEmpty().WithMessage("Name is required")
    .NotNull().WithMessage("Name cannot be null")
    .MaximumLength(100).WithMessage("Name too long")
    .MinimumLength(3).WithMessage("Name too short")
    .Matches("^[a-zA-Z]+$").WithMessage("Only letters allowed");

// Numeric validations
RuleFor(x => x.Amount)
    .GreaterThan(0).WithMessage("Must be positive")
    .LessThanOrEqualTo(1000).WithMessage("Max 1000")
    .InclusiveBetween(1, 100).WithMessage("Must be 1-100");

// GUID validations
RuleFor(x => x.Id)
    .NotEmpty().WithMessage("ID is required")
    .NotEqual(Guid.Empty).WithMessage("Invalid ID");

// Email validation
RuleFor(x => x.Email)
    .NotEmpty()
    .EmailAddress().WithMessage("Invalid email format");

// Conditional validation
RuleFor(x => x.ParentId)
    .NotEmpty()
    .When(x => x.RequiresParent);

// Collection validation
RuleFor(x => x.Items)
    .NotEmpty().WithMessage("At least one item required")
    .Must(items => items.Count <= 10).WithMessage("Max 10 items");

// Custom validation
RuleFor(x => x.DateRange)
    .Must(BeValidDateRange).WithMessage("End date must be after start date");

private bool BeValidDateRange(DateRange range) => range.End > range.Start;
```

### Async Validation (Use Sparingly)

```csharp
internal sealed class Create{Entity}CommandValidator 
    : AbstractValidator<Create{Entity}Command>
{
    private readonly I{Entity}Repository _{entity}Repository;

    public Create{Entity}CommandValidator(I{Entity}Repository {entity}Repository)
    {
        _{entity}Repository = {entity}Repository;

        RuleFor(x => x.Name)
            .MustAsync(BeUniqueName)
            .WithMessage("Name already exists");
    }

    private async Task<bool> BeUniqueName(string name, CancellationToken ct)
    {
        var existing = await _{entity}Repository.GetByNameAsync(name, ct);
        return existing is null;
    }
}
```

**Note**: Prefer doing existence checks in the Handler rather than Validator for better separation of concerns.

---

## Handler Patterns

### Pattern 1: Single Entity Operation

```csharp
public async Task<Result<Guid>> Handle(CreateCommand request, CancellationToken ct)
{
    // Create
    var entity = Entity.Create(request.Data);
    _repository.Add(entity);
    await _unitOfWork.SaveChangesAsync(ct);
    return entity.Id;
}
```

### Pattern 2: With Related Entities

```csharp
public async Task<Result<Guid>> Handle(CreateCommand request, CancellationToken ct)
{
    // Load related entity
    var parent = await _parentRepository.GetByIdAsync(request.ParentId, ct);
    if (parent is null)
        return Result.Failure<Guid>(ParentErrors.NotFound);

    // Create with relationship
    var entity = Entity.Create(request.Data, parent);
    _repository.Add(entity);
    await _unitOfWork.SaveChangesAsync(ct);
    return entity.Id;
}
```

### Pattern 3: Batch Operations

```csharp
public async Task<r> Handle(CreateBatchCommand request, CancellationToken ct)
{
    var entities = new List<Entity>();

    foreach (var item in request.Items)
    {
        var entityResult = Entity.Create(item);
        if (entityResult.IsFailure)
            return Result.Failure(entityResult.Error);
        
        entities.Add(entityResult.Value);
    }

    _repository.AddRange(entities);
    await _unitOfWork.SaveChangesAsync(ct);
    return Result.Success();
}
```

### Pattern 4: With Transaction

```csharp
public async Task<r> Handle(ComplexCommand request, CancellationToken ct)
{
    using var transaction = await _unitOfWork.BeginTransactionAsync(ct);
    
    try
    {
        // Multiple operations
        var entity1 = await CreateEntity1(request);
        var entity2 = await CreateEntity2(request, entity1);
        
        await _unitOfWork.SaveChangesAsync(ct);
        await transaction.CommitAsync(ct);
        
        return Result.Success();
    }
    catch
    {
        await transaction.RollbackAsync(ct);
        throw;
    }
}
```

---

## Critical Rules

1. **Commands are records** - Immutable, value equality
2. **One handler per command** - No shared handlers
3. **Validators are internal** - Not exposed outside Application layer
4. **Use Result pattern** - Never throw exceptions for business errors
5. **Inject IUnitOfWork** - Don't call SaveChanges in repository
6. **Always use CancellationToken** - Pass through all async calls
7. **Domain logic in Domain** - Handler orchestrates, doesn't contain business rules
8. **Return IDs from Create** - Use `ICommand<Guid>` for creation
9. **Validate in order** - Check existence before creating, then validate business rules
10. **Keep handlers focused** - One responsibility per handler

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Throwing exceptions for business errors
if (entity is null)
    throw new NotFoundException("Entity not found");

// ✅ CORRECT: Return Result
if (entity is null)
    return Result.Failure<Guid>(EntityErrors.NotFound);

// ❌ WRONG: Saving in repository
public void Add(Entity entity)
{
    _dbContext.Add(entity);
    _dbContext.SaveChanges(); // Don't do this!
}

// ✅ CORRECT: Handler calls SaveChanges via UnitOfWork
_repository.Add(entity);
await _unitOfWork.SaveChangesAsync(ct);

// ❌ WRONG: Business logic in handler
if (request.Amount > 1000 && user.Level < 5)
    return Result.Failure(Error.InsufficientLevel);

// ✅ CORRECT: Business logic in domain
var result = entity.ProcessOrder(request.Amount, user);
if (result.IsFailure)
    return Result.Failure(result.Error);
```

---

## Related Skills

- `cqrs-query-generator` - Generate read-side queries
- `domain-entity-generator` - Generate domain entities with factory methods
- `result-pattern` - Complete Result pattern implementation
- `pipeline-behaviors` - Validation and logging behaviors
