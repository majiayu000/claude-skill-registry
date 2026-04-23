---
name: specification-pattern
description: "Implements the Specification pattern for encapsulating query logic. Enables composable, reusable, and testable query criteria with support for includes, ordering, and pagination."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Entity Framework Core
pattern: Specification Pattern, Query Object
---

# Specification Pattern Generator

## Overview

The Specification pattern encapsulates query logic:

- **Reusable criteria** - Define once, use everywhere
- **Composable** - Combine with And/Or
- **Testable** - Test query logic in isolation
- **Type-safe** - Compile-time checking

## Quick Reference

| Component | Purpose |
|-----------|---------|
| `ISpecification<T>` | Base specification interface |
| `BaseSpecification<T>` | Abstract implementation |
| `SpecificationEvaluator` | Applies spec to IQueryable |

---

## Template: Specification Interface

```csharp
// src/{name}.domain/Abstractions/ISpecification.cs
using System.Linq.Expressions;

namespace {name}.domain.abstractions;

public interface ISpecification<T>
{
    Expression<Func<T, bool>>? Criteria { get; }
    List<Expression<Func<T, object>>> Includes { get; }
    List<string> IncludeStrings { get; }
    Expression<Func<T, object>>? OrderBy { get; }
    Expression<Func<T, object>>? OrderByDescending { get; }
    int? Take { get; }
    int? Skip { get; }
    bool IsPagingEnabled { get; }
}
```

---

## Template: Base Specification

```csharp
// src/{name}.domain/Abstractions/BaseSpecification.cs
using System.Linq.Expressions;

namespace {name}.domain.abstractions;

public abstract class BaseSpecification<T> : ISpecification<T>
{
    public Expression<Func<T, bool>>? Criteria { get; private set; }
    public List<Expression<Func<T, object>>> Includes { get; } = new();
    public List<string> IncludeStrings { get; } = new();
    public Expression<Func<T, object>>? OrderBy { get; private set; }
    public Expression<Func<T, object>>? OrderByDescending { get; private set; }
    public int? Take { get; private set; }
    public int? Skip { get; private set; }
    public bool IsPagingEnabled { get; private set; }

    protected void AddCriteria(Expression<Func<T, bool>> criteria) => Criteria = criteria;

    protected void AddInclude(Expression<Func<T, object>> include) => Includes.Add(include);

    protected void AddInclude(string include) => IncludeStrings.Add(include);

    protected void ApplyOrderBy(Expression<Func<T, object>> orderBy) => OrderBy = orderBy;

    protected void ApplyOrderByDescending(Expression<Func<T, object>> orderBy) => OrderByDescending = orderBy;

    protected void ApplyPaging(int skip, int take)
    {
        Skip = skip;
        Take = take;
        IsPagingEnabled = true;
    }
}
```

---

## Template: Concrete Specifications

```csharp
// src/{name}.domain/{Aggregate}/Specifications/Active{Entities}Specification.cs
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
    public {Entities}ByOrganizationSpecification(Guid organizationId, bool includeChildren = false)
    {
        AddCriteria(e => e.OrganizationId == organizationId && e.IsActive);
        
        if (includeChildren)
        {
            AddInclude(e => e.Children);
        }
        
        ApplyOrderBy(e => e.Name);
    }
}

public sealed class {Entity}ByIdSpecification : BaseSpecification<{Entity}>
{
    public {Entity}ByIdSpecification(Guid id, bool includeAll = false)
    {
        AddCriteria(e => e.Id == id);
        
        if (includeAll)
        {
            AddInclude(e => e.Children);
            AddInclude(e => e.Organization);
            AddInclude("Children.SubItems");  // String-based deep include
        }
    }
}

public sealed class Paged{Entities}Specification : BaseSpecification<{Entity}>
{
    public Paged{Entities}Specification(int pageNumber, int pageSize, string? searchTerm = null)
    {
        if (!string.IsNullOrEmpty(searchTerm))
        {
            AddCriteria(e => e.Name.ToLower().Contains(searchTerm.ToLower()));
        }
        else
        {
            AddCriteria(e => e.IsActive);
        }

        ApplyOrderByDescending(e => e.CreatedAt);
        ApplyPaging((pageNumber - 1) * pageSize, pageSize);
    }
}
```

---

## Template: Specification Evaluator

```csharp
// src/{name}.infrastructure/Specifications/SpecificationEvaluator.cs
using Microsoft.EntityFrameworkCore;
using {name}.domain.abstractions;

namespace {name}.infrastructure.specifications;

public static class SpecificationEvaluator
{
    public static IQueryable<T> GetQuery<T>(
        IQueryable<T> inputQuery,
        ISpecification<T> specification) where T : class
    {
        var query = inputQuery;

        if (specification.Criteria is not null)
        {
            query = query.Where(specification.Criteria);
        }

        foreach (var include in specification.Includes)
        {
            query = query.Include(include);
        }

        foreach (var includeString in specification.IncludeStrings)
        {
            query = query.Include(includeString);
        }

        if (specification.OrderBy is not null)
        {
            query = query.OrderBy(specification.OrderBy);
        }
        else if (specification.OrderByDescending is not null)
        {
            query = query.OrderByDescending(specification.OrderByDescending);
        }

        if (specification.IsPagingEnabled)
        {
            query = query.Skip(specification.Skip!.Value).Take(specification.Take!.Value);
        }

        return query;
    }
}
```

---

## Template: Repository Integration

```csharp
// src/{name}.infrastructure/Repositories/{Entity}Repository.cs
public async Task<IReadOnlyList<{Entity}>> GetAsync(
    ISpecification<{Entity}> specification,
    CancellationToken cancellationToken = default)
{
    return await SpecificationEvaluator
        .GetQuery(_dbContext.Set<{Entity}>(), specification)
        .ToListAsync(cancellationToken);
}

public async Task<{Entity}?> GetFirstOrDefaultAsync(
    ISpecification<{Entity}> specification,
    CancellationToken cancellationToken = default)
{
    return await SpecificationEvaluator
        .GetQuery(_dbContext.Set<{Entity}>(), specification)
        .FirstOrDefaultAsync(cancellationToken);
}

public async Task<int> CountAsync(
    ISpecification<{Entity}> specification,
    CancellationToken cancellationToken = default)
{
    return await SpecificationEvaluator
        .GetQuery(_dbContext.Set<{Entity}>(), specification)
        .CountAsync(cancellationToken);
}
```

---

## Usage in Handler

```csharp
public async Task<Result<IReadOnlyList<{Entity}Response>>> Handle(
    Get{Entities}Query request,
    CancellationToken cancellationToken)
{
    var specification = new {Entities}ByOrganizationSpecification(
        request.OrganizationId,
        includeChildren: true);

    var entities = await _{entity}Repository.GetAsync(specification, cancellationToken);

    return entities.Select(e => new {Entity}Response(e)).ToList();
}
```

---

## Related Skills

- `repository-pattern` - Repository with specification support
- `cqrs-query-generator` - Query handlers using specifications
- `domain-entity-generator` - Entities queried by specifications
