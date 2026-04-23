---
name: repository-pattern
description: "Generates Repository interfaces and implementations following the Repository pattern. Provides data access abstraction for aggregate roots with EF Core implementations."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Entity Framework Core
---

# Repository Pattern Generator

## Overview

This skill generates Repositories that provide an abstraction over data access:

- **Interface in Domain layer** - Defines data access contract
- **Implementation in Infrastructure** - Uses EF Core
- **Per Aggregate Root** - Not per entity
- **Unit of Work integration** - SaveChanges via IUnitOfWork

## Quick Reference

| Repository Method | Purpose | Returns |
|-------------------|---------|---------|
| `GetByIdAsync` | Retrieve by primary key | `Entity?` |
| `GetByXxxAsync` | Retrieve by business key | `Entity?` |
| `GetAllAsync` | Retrieve all (use sparingly) | `IReadOnlyList<Entity>` |
| `Add` | Track new entity | `void` |
| `Update` | Track modified entity | `void` |
| `Remove` | Track deleted entity | `void` |
| `ExistsAsync` | Check existence | `bool` |

---

## Repository Structure

```
/Domain/{Aggregate}/
└── I{Entity}Repository.cs          # Interface (Domain layer)

/Infrastructure/Repositories/
└── {Entity}Repository.cs           # Implementation (Infrastructure layer)
```

---

## Template: Repository Interface (Domain Layer)

```csharp
// src/{name}.domain/{Aggregate}/I{Entity}Repository.cs
namespace {name}.domain.{aggregate};

public interface I{Entity}Repository
{
    // ═══════════════════════════════════════════════════════════════
    // QUERY METHODS
    // ═══════════════════════════════════════════════════════════════
    
    /// <summary>
    /// Gets an entity by its unique identifier
    /// </summary>
    Task<{Entity}?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Gets an entity by its unique identifier with related entities
    /// </summary>
    Task<{Entity}?> GetByIdWithDetailsAsync(
        Guid id,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Gets an entity by a unique business key
    /// </summary>
    Task<{Entity}?> GetByNameAsync(
        string name,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Gets all entities for a parent organization
    /// </summary>
    Task<IReadOnlyList<{Entity}>> GetByOrganizationIdAsync(
        Guid organizationId,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Gets all active entities
    /// </summary>
    Task<IReadOnlyList<{Entity}>> GetAllActiveAsync(
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Checks if an entity exists
    /// </summary>
    Task<bool> ExistsAsync(
        Guid id,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Checks if an entity with the given name exists
    /// </summary>
    Task<bool> ExistsByNameAsync(
        string name,
        CancellationToken cancellationToken = default);

    // ═══════════════════════════════════════════════════════════════
    // COMMAND METHODS (tracking only, no SaveChanges)
    // ═══════════════════════════════════════════════════════════════
    
    /// <summary>
    /// Adds a new entity to the context
    /// </summary>
    void Add({Entity} {entity});

    /// <summary>
    /// Adds multiple entities to the context
    /// </summary>
    void AddRange(IEnumerable<{Entity}> {entities});

    /// <summary>
    /// Updates an existing entity in the context
    /// </summary>
    void Update({Entity} {entity});

    /// <summary>
    /// Removes an entity from the context
    /// </summary>
    void Remove({Entity} {entity});

    /// <summary>
    /// Removes multiple entities from the context
    /// </summary>
    void RemoveRange(IEnumerable<{Entity}> {entities});
}
```

---

## Template: Repository Implementation (Infrastructure Layer)

```csharp
// src/{name}.infrastructure/Repositories/{Entity}Repository.cs
using Microsoft.EntityFrameworkCore;
using {name}.domain.{aggregate};

namespace {name}.infrastructure.repositories;

internal sealed class {Entity}Repository : I{Entity}Repository
{
    private readonly ApplicationDbContext _dbContext;

    public {Entity}Repository(ApplicationDbContext dbContext)
    {
        _dbContext = dbContext;
    }

    // ═══════════════════════════════════════════════════════════════
    // QUERY METHODS
    // ═══════════════════════════════════════════════════════════════

    public async Task<{Entity}?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        return await _dbContext
            .Set<{Entity}>()
            .FirstOrDefaultAsync(e => e.Id == id, cancellationToken);
    }

    public async Task<{Entity}?> GetByIdWithDetailsAsync(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        return await _dbContext
            .Set<{Entity}>()
            .Include(e => e.{ChildEntities})
            .Include(e => e.{OtherRelation})
            .FirstOrDefaultAsync(e => e.Id == id, cancellationToken);
    }

    public async Task<{Entity}?> GetByNameAsync(
        string name,
        CancellationToken cancellationToken = default)
    {
        return await _dbContext
            .Set<{Entity}>()
            .FirstOrDefaultAsync(
                e => e.Name.ToLower() == name.ToLower(),
                cancellationToken);
    }

    public async Task<IReadOnlyList<{Entity}>> GetByOrganizationIdAsync(
        Guid organizationId,
        CancellationToken cancellationToken = default)
    {
        return await _dbContext
            .Set<{Entity}>()
            .Where(e => e.OrganizationId == organizationId)
            .OrderBy(e => e.Name)
            .ToListAsync(cancellationToken);
    }

    public async Task<IReadOnlyList<{Entity}>> GetAllActiveAsync(
        CancellationToken cancellationToken = default)
    {
        return await _dbContext
            .Set<{Entity}>()
            .Where(e => e.IsActive)
            .OrderBy(e => e.Name)
            .ToListAsync(cancellationToken);
    }

    public async Task<bool> ExistsAsync(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        return await _dbContext
            .Set<{Entity}>()
            .AnyAsync(e => e.Id == id, cancellationToken);
    }

    public async Task<bool> ExistsByNameAsync(
        string name,
        CancellationToken cancellationToken = default)
    {
        return await _dbContext
            .Set<{Entity}>()
            .AnyAsync(
                e => e.Name.ToLower() == name.ToLower(),
                cancellationToken);
    }

    // ═══════════════════════════════════════════════════════════════
    // COMMAND METHODS
    // ═══════════════════════════════════════════════════════════════

    public void Add({Entity} {entity})
    {
        _dbContext.Set<{Entity}>().Add({entity});
    }

    public void AddRange(IEnumerable<{Entity}> {entities})
    {
        _dbContext.Set<{Entity}>().AddRange({entities});
    }

    public void Update({Entity} {entity})
    {
        _dbContext.Set<{Entity}>().Update({entity});
    }

    public void Remove({Entity} {entity})
    {
        _dbContext.Set<{Entity}>().Remove({entity});
    }

    public void RemoveRange(IEnumerable<{Entity}> {entities})
    {
        _dbContext.Set<{Entity}>().RemoveRange({entities});
    }
}
```

---

## Template: Repository with Child Entity Access

```csharp
// src/{name}.domain/{Aggregate}/I{Entity}Repository.cs
namespace {name}.domain.{aggregate};

public interface I{Entity}Repository
{
    // Standard methods...

    // ═══════════════════════════════════════════════════════════════
    // CHILD ENTITY QUERIES (accessed through aggregate root)
    // ═══════════════════════════════════════════════════════════════

    /// <summary>
    /// Gets a child entity through its aggregate root
    /// </summary>
    Task<{ChildEntity}?> Get{ChildEntity}ByIdAsync(
        Guid {entity}Id,
        Guid {childEntity}Id,
        CancellationToken cancellationToken = default);

    /// <summary>
    /// Gets all child entities for a parent
    /// </summary>
    Task<IReadOnlyList<{ChildEntity}>> Get{ChildEntities}By{Entity}IdAsync(
        Guid {entity}Id,
        CancellationToken cancellationToken = default);
}
```

```csharp
// src/{name}.infrastructure/Repositories/{Entity}Repository.cs
internal sealed class {Entity}Repository : I{Entity}Repository
{
    // ... other methods

    public async Task<{ChildEntity}?> Get{ChildEntity}ByIdAsync(
        Guid {entity}Id,
        Guid {childEntity}Id,
        CancellationToken cancellationToken = default)
    {
        var {entity} = await _dbContext
            .Set<{Entity}>()
            .Include(e => e.{ChildEntities})
            .FirstOrDefaultAsync(e => e.Id == {entity}Id, cancellationToken);

        return {entity}?.{ChildEntities}
            .FirstOrDefault(c => c.Id == {childEntity}Id);
    }

    public async Task<IReadOnlyList<{ChildEntity}>> Get{ChildEntities}By{Entity}IdAsync(
        Guid {entity}Id,
        CancellationToken cancellationToken = default)
    {
        var {entity} = await _dbContext
            .Set<{Entity}>()
            .Include(e => e.{ChildEntities})
            .FirstOrDefaultAsync(e => e.Id == {entity}Id, cancellationToken);

        return {entity}?.{ChildEntities}.ToList() 
            ?? new List<{ChildEntity}>();
    }
}
```

---

## Template: Repository with Specification Pattern

```csharp
// src/{name}.domain/Abstractions/ISpecification.cs
using System.Linq.Expressions;

namespace {name}.domain.abstractions;

public interface ISpecification<T>
{
    Expression<Func<T, bool>> Criteria { get; }
    List<Expression<Func<T, object>>> Includes { get; }
    List<string> IncludeStrings { get; }
    Expression<Func<T, object>>? OrderBy { get; }
    Expression<Func<T, object>>? OrderByDescending { get; }
    int? Take { get; }
    int? Skip { get; }
    bool IsPagingEnabled { get; }
}
```

```csharp
// src/{name}.domain/Abstractions/BaseSpecification.cs
using System.Linq.Expressions;

namespace {name}.domain.abstractions;

public abstract class BaseSpecification<T> : ISpecification<T>
{
    public Expression<Func<T, bool>> Criteria { get; private set; } = _ => true;
    public List<Expression<Func<T, object>>> Includes { get; } = new();
    public List<string> IncludeStrings { get; } = new();
    public Expression<Func<T, object>>? OrderBy { get; private set; }
    public Expression<Func<T, object>>? OrderByDescending { get; private set; }
    public int? Take { get; private set; }
    public int? Skip { get; private set; }
    public bool IsPagingEnabled { get; private set; }

    protected void AddCriteria(Expression<Func<T, bool>> criteria)
    {
        Criteria = criteria;
    }

    protected void AddInclude(Expression<Func<T, object>> includeExpression)
    {
        Includes.Add(includeExpression);
    }

    protected void AddInclude(string includeString)
    {
        IncludeStrings.Add(includeString);
    }

    protected void ApplyOrderBy(Expression<Func<T, object>> orderByExpression)
    {
        OrderBy = orderByExpression;
    }

    protected void ApplyOrderByDescending(Expression<Func<T, object>> orderByDescExpression)
    {
        OrderByDescending = orderByDescExpression;
    }

    protected void ApplyPaging(int skip, int take)
    {
        Skip = skip;
        Take = take;
        IsPagingEnabled = true;
    }
}
```

```csharp
// src/{name}.domain/{Aggregate}/Specifications/Active{Entities}Specification.cs
using {name}.domain.abstractions;

namespace {name}.domain.{aggregate}.specifications;

public sealed class Active{Entities}Specification : BaseSpecification<{Entity}>
{
    public Active{Entities}Specification()
    {
        AddCriteria(e => e.IsActive);
        ApplyOrderBy(e => e.Name);
    }
}

public sealed class {Entities}ByOrganizationSpecification : BaseSpecification<{Entity}>
{
    public {Entities}ByOrganizationSpecification(Guid organizationId)
    {
        AddCriteria(e => e.OrganizationId == organizationId && e.IsActive);
        AddInclude(e => e.{ChildEntities});
        ApplyOrderBy(e => e.Name);
    }
}
```

```csharp
// Repository with specification support
public interface I{Entity}Repository
{
    Task<IReadOnlyList<{Entity}>> GetAsync(
        ISpecification<{Entity}> specification,
        CancellationToken cancellationToken = default);

    Task<{Entity}?> GetFirstOrDefaultAsync(
        ISpecification<{Entity}> specification,
        CancellationToken cancellationToken = default);

    Task<int> CountAsync(
        ISpecification<{Entity}> specification,
        CancellationToken cancellationToken = default);
}
```

---

## Template: Generic Repository Base (Optional)

```csharp
// src/{name}.infrastructure/Repositories/Repository.cs
using Microsoft.EntityFrameworkCore;
using {name}.domain.abstractions;

namespace {name}.infrastructure.repositories;

internal abstract class Repository<T> where T : Entity
{
    protected readonly ApplicationDbContext DbContext;

    protected Repository(ApplicationDbContext dbContext)
    {
        DbContext = dbContext;
    }

    public async Task<T?> GetByIdAsync(
        Guid id,
        CancellationToken cancellationToken = default)
    {
        return await DbContext
            .Set<T>()
            .FirstOrDefaultAsync(e => e.Id == id, cancellationToken);
    }

    public void Add(T entity)
    {
        DbContext.Set<T>().Add(entity);
    }

    public void Update(T entity)
    {
        DbContext.Set<T>().Update(entity);
    }

    public void Remove(T entity)
    {
        DbContext.Set<T>().Remove(entity);
    }
}
```

```csharp
// Using the base repository
internal sealed class {Entity}Repository : Repository<{Entity}>, I{Entity}Repository
{
    public {Entity}Repository(ApplicationDbContext dbContext) : base(dbContext)
    {
    }

    // Add entity-specific methods
    public async Task<{Entity}?> GetByNameAsync(
        string name,
        CancellationToken cancellationToken = default)
    {
        return await DbContext
            .Set<{Entity}>()
            .FirstOrDefaultAsync(
                e => e.Name.ToLower() == name.ToLower(),
                cancellationToken);
    }
}
```

---

## Registering Repositories

```csharp
// src/{name}.infrastructure/DependencyInjection.cs
private static void AddPersistence(IServiceCollection services, IConfiguration configuration)
{
    var connectionString = configuration.GetConnectionString("Database")
        ?? throw new ArgumentNullException(nameof(configuration));

    services.AddDbContext<ApplicationDbContext>(options =>
    {
        options.UseNpgsql(connectionString)
               .UseSnakeCaseNamingConvention();
    });

    // Register Unit of Work
    services.AddScoped<IUnitOfWork>(sp => 
        sp.GetRequiredService<ApplicationDbContext>());

    // Register Repositories
    services.AddScoped<IUserRepository, UserRepository>();
    services.AddScoped<IOrganizationRepository, OrganizationRepository>();
    services.AddScoped<IDepartmentRepository, DepartmentRepository>();
    services.AddScoped<ISurveyRepository, SurveyRepository>();
    // Add more repositories here...

    // Register SQL Connection Factory for Dapper queries
    services.AddSingleton<ISqlConnectionFactory>(_ => 
        new SqlConnectionFactory(connectionString));
}
```

---

## Query Optimization Patterns

### AsNoTracking for Read-Only Queries

```csharp
public async Task<IReadOnlyList<{Entity}>> GetAllForDisplayAsync(
    CancellationToken cancellationToken = default)
{
    return await _dbContext
        .Set<{Entity}>()
        .AsNoTracking()  // Performance: no change tracking
        .Where(e => e.IsActive)
        .OrderBy(e => e.Name)
        .ToListAsync(cancellationToken);
}
```

### Selective Includes (Avoid Over-fetching)

```csharp
// ❌ WRONG: Loading everything
public async Task<{Entity}?> GetByIdAsync(Guid id, CancellationToken ct)
{
    return await _dbContext
        .Set<{Entity}>()
        .Include(e => e.Children)
        .Include(e => e.Parent)
        .Include(e => e.Logs)  // Potentially thousands of records!
        .FirstOrDefaultAsync(e => e.Id == id, ct);
}

// ✅ CORRECT: Separate methods for different needs
public async Task<{Entity}?> GetByIdAsync(Guid id, CancellationToken ct)
{
    return await _dbContext
        .Set<{Entity}>()
        .FirstOrDefaultAsync(e => e.Id == id, ct);
}

public async Task<{Entity}?> GetByIdWithChildrenAsync(Guid id, CancellationToken ct)
{
    return await _dbContext
        .Set<{Entity}>()
        .Include(e => e.Children)
        .FirstOrDefaultAsync(e => e.Id == id, ct);
}
```

### Split Queries for Large Collections

```csharp
public async Task<{Entity}?> GetByIdWithAllRelationsAsync(
    Guid id,
    CancellationToken cancellationToken = default)
{
    return await _dbContext
        .Set<{Entity}>()
        .Include(e => e.Children)
        .Include(e => e.OtherRelation)
        .AsSplitQuery()  // Splits into multiple SQL queries
        .FirstOrDefaultAsync(e => e.Id == id, cancellationToken);
}
```

---

## Critical Rules

1. **Repository per aggregate root** - Not per entity
2. **No SaveChanges in repository** - That's IUnitOfWork's job
3. **Interface in Domain** - Implementation in Infrastructure
4. **Use CancellationToken** - All async methods
5. **Return null for not found** - Let handler decide what to do
6. **AsNoTracking for reads** - When not modifying
7. **Selective Includes** - Don't over-fetch
8. **Avoid GetAll without filters** - Can be dangerous at scale
9. **Child entities through aggregate** - Don't expose child repositories
10. **Internal class for implementation** - Hide implementation details

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: SaveChanges in repository
public void Add({Entity} {entity})
{
    _dbContext.Set<{Entity}>().Add({entity});
    _dbContext.SaveChanges();  // Don't do this!
}

// ✅ CORRECT: Only track, save via UnitOfWork
public void Add({Entity} {entity})
{
    _dbContext.Set<{Entity}>().Add({entity});
}
// In handler:
await _unitOfWork.SaveChangesAsync(ct);

// ❌ WRONG: Repository for child entities
public interface IOrderItemRepository { ... }

// ✅ CORRECT: Access through aggregate root
public interface IOrderRepository
{
    Task<OrderItem?> GetOrderItemAsync(Guid orderId, Guid itemId, ...);
}

// ❌ WRONG: Exposing IQueryable
public IQueryable<{Entity}> GetAll() => _dbContext.Set<{Entity}>();

// ✅ CORRECT: Return materialized lists
public async Task<IReadOnlyList<{Entity}>> GetAllAsync(CancellationToken ct)
{
    return await _dbContext.Set<{Entity}>().ToListAsync(ct);
}

// ❌ WRONG: Business logic in repository
public async Task<{Entity}?> GetActiveByIdAsync(Guid id, CancellationToken ct)
{
    var entity = await GetByIdAsync(id, ct);
    if (entity?.IsActive == false)
        throw new BusinessException("Entity is inactive");  // Wrong!
    return entity;
}

// ✅ CORRECT: Let handler handle business logic
public async Task<{Entity}?> GetByIdAsync(Guid id, CancellationToken ct)
{
    return await _dbContext.Set<{Entity}>()
        .FirstOrDefaultAsync(e => e.Id == id, ct);
}
```

---

## Related Skills

- `domain-entity-generator` - Generate entities for repositories
- `ef-core-configuration` - Configure entity mappings
- `cqrs-command-generator` - Use repositories in handlers
- `dotnet-clean-architecture` - Overall project structure
