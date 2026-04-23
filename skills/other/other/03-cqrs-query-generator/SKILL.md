---
name: cqrs-query-generator
description: "Generates CQRS Queries with Handlers and Response DTOs for read operations. Uses Dapper for optimized read queries, bypassing the domain model for better performance."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: MediatR, Dapper, FluentValidation
---

# CQRS Query Generator

## Overview

This skill generates Queries following the CQRS pattern. Queries are read-only operations that return data without modifying state. Key principles:

- **Queries never modify state** - Read-only operations
- **Use Dapper for reads** - Bypass EF Core for performance
- **Return DTOs, not entities** - Projection to response models
- **Direct SQL queries** - Optimized for the specific use case

## Quick Reference

| Query Type | Use Case | Returns |
|------------|----------|---------|
| GetById | Single entity by ID | `Result<EntityResponse>` |
| GetAll | All entities (with optional filtering) | `Result<IReadOnlyList<EntityResponse>>` |
| GetPaged | Paginated list | `Result<PagedList<EntityResponse>>` |
| Search | Filtered/searched results | `Result<IReadOnlyList<EntityResponse>>` |
| Exists | Check if entity exists | `Result<bool>` |

---

## Query Structure

```
/Application/{Feature}/
├── Get{Entity}ById/
│   ├── Get{Entity}ByIdQuery.cs       # Query + Validator + Handler
│   └── {Entity}Response.cs            # Response DTO
├── GetAll{Entities}/
│   ├── GetAll{Entities}Query.cs
│   └── {Entity}ListResponse.cs
└── Get{Entities}ByOrganization/
    ├── Get{Entities}ByOrganizationQuery.cs
    └── {Entity}ByOrganizationResponse.cs
```

---

## Template: Get By ID Query

```csharp
// src/{name}.application/{Feature}/Get{Entity}ById/Get{Entity}ByIdQuery.cs
using System.Data;
using Dapper;
using FluentValidation;
using {name}.application.abstractions.data;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;
using {name}.domain.{entities};

namespace {name}.application.{feature}.Get{Entity}ById;

// ═══════════════════════════════════════════════════════════════
// QUERY RECORD
// ═══════════════════════════════════════════════════════════════
public sealed record Get{Entity}ByIdQuery(Guid Id) : IQuery<{Entity}Response>;

// ═══════════════════════════════════════════════════════════════
// VALIDATOR
// ═══════════════════════════════════════════════════════════════
internal sealed class Get{Entity}ByIdQueryValidator : AbstractValidator<Get{Entity}ByIdQuery>
{
    public Get{Entity}ByIdQueryValidator()
    {
        RuleFor(x => x.Id)
            .NotEmpty()
            .WithMessage("{Entity} ID is required");
    }
}

// ═══════════════════════════════════════════════════════════════
// HANDLER
// ═══════════════════════════════════════════════════════════════
internal sealed class Get{Entity}ByIdQueryHandler 
    : IQueryHandler<Get{Entity}ByIdQuery, {Entity}Response>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public Get{Entity}ByIdQueryHandler(ISqlConnectionFactory sqlConnectionFactory)
    {
        _sqlConnectionFactory = sqlConnectionFactory;
    }

    public async Task<Result<{Entity}Response>> Handle(
        Get{Entity}ByIdQuery request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        const string sql = """
            SELECT 
                e.id AS Id,
                e.name AS Name,
                e.description AS Description,
                e.created_at AS CreatedAt,
                e.updated_at AS UpdatedAt
            FROM {table_name} e
            WHERE e.id = @Id
            """;

        var {entity} = await connection.QueryFirstOrDefaultAsync<{Entity}Response>(
            sql,
            new { request.Id });

        if ({entity} is null)
        {
            return Result.Failure<{Entity}Response>({Entity}Errors.NotFound);
        }

        return {entity};
    }
}
```

### Response DTO

```csharp
// src/{name}.application/{Feature}/Get{Entity}ById/{Entity}Response.cs
namespace {name}.application.{feature}.Get{Entity}ById;

public sealed class {Entity}Response
{
    public Guid Id { get; init; }
    public required string Name { get; init; }
    public string? Description { get; init; }
    public DateTime CreatedAt { get; init; }
    public DateTime UpdatedAt { get; init; }
}
```

---

## Template: Get All Query

```csharp
// src/{name}.application/{Feature}/GetAll{Entities}/GetAll{Entities}Query.cs
using System.Data;
using Dapper;
using {name}.application.abstractions.data;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.{feature}.GetAll{Entities};

public sealed record GetAll{Entities}Query : IQuery<IReadOnlyList<{Entity}ListResponse>>;

internal sealed class GetAll{Entities}QueryHandler 
    : IQueryHandler<GetAll{Entities}Query, IReadOnlyList<{Entity}ListResponse>>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public GetAll{Entities}QueryHandler(ISqlConnectionFactory sqlConnectionFactory)
    {
        _sqlConnectionFactory = sqlConnectionFactory;
    }

    public async Task<Result<IReadOnlyList<{Entity}ListResponse>>> Handle(
        GetAll{Entities}Query request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        const string sql = """
            SELECT 
                e.id AS Id,
                e.name AS Name,
                e.description AS Description
            FROM {table_name} e
            ORDER BY e.name ASC
            """;

        var {entities} = await connection.QueryAsync<{Entity}ListResponse>(sql);

        return {entities}.ToList();
    }
}
```

---

## Template: Get By Parent ID Query

```csharp
// src/{name}.application/{Feature}/Get{Entities}ByOrganizationId/Get{Entities}ByOrganizationIdQuery.cs
using System.Data;
using Dapper;
using FluentValidation;
using {name}.application.abstractions.data;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.{feature}.Get{Entities}ByOrganizationId;

public sealed record Get{Entities}ByOrganizationIdQuery(
    Guid OrganizationId) : IQuery<IReadOnlyList<{Entity}Response>>;

internal sealed class Get{Entities}ByOrganizationIdQueryValidator 
    : AbstractValidator<Get{Entities}ByOrganizationIdQuery>
{
    public Get{Entities}ByOrganizationIdQueryValidator()
    {
        RuleFor(x => x.OrganizationId).NotEmpty();
    }
}

internal sealed class Get{Entities}ByOrganizationIdQueryHandler 
    : IQueryHandler<Get{Entities}ByOrganizationIdQuery, IReadOnlyList<{Entity}Response>>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public Get{Entities}ByOrganizationIdQueryHandler(ISqlConnectionFactory sqlConnectionFactory)
    {
        _sqlConnectionFactory = sqlConnectionFactory;
    }

    public async Task<Result<IReadOnlyList<{Entity}Response>>> Handle(
        Get{Entities}ByOrganizationIdQuery request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        const string sql = """
            SELECT 
                e.id AS Id,
                e.name AS Name,
                e.description AS Description,
                e.organization_id AS OrganizationId,
                o.name AS OrganizationName
            FROM {table_name} e
            INNER JOIN organization o ON e.organization_id = o.id
            WHERE e.organization_id = @OrganizationId
            ORDER BY e.name ASC
            """;

        var {entities} = await connection.QueryAsync<{Entity}Response>(
            sql,
            new { request.OrganizationId });

        return {entities}.ToList();
    }
}
```

---

## Template: Paginated Query

```csharp
// src/{name}.application/{Feature}/Get{Entities}Paged/Get{Entities}PagedQuery.cs
using System.Data;
using Dapper;
using FluentValidation;
using {name}.application.abstractions.data;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.{feature}.Get{Entities}Paged;

public sealed record Get{Entities}PagedQuery(
    int PageNumber,
    int PageSize,
    string? SearchTerm = null) : IQuery<PagedList<{Entity}Response>>;

internal sealed class Get{Entities}PagedQueryValidator 
    : AbstractValidator<Get{Entities}PagedQuery>
{
    public Get{Entities}PagedQueryValidator()
    {
        RuleFor(x => x.PageNumber).GreaterThan(0);
        RuleFor(x => x.PageSize).InclusiveBetween(1, 100);
    }
}

internal sealed class Get{Entities}PagedQueryHandler 
    : IQueryHandler<Get{Entities}PagedQuery, PagedList<{Entity}Response>>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public Get{Entities}PagedQueryHandler(ISqlConnectionFactory sqlConnectionFactory)
    {
        _sqlConnectionFactory = sqlConnectionFactory;
    }

    public async Task<Result<PagedList<{Entity}Response>>> Handle(
        Get{Entities}PagedQuery request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        var offset = (request.PageNumber - 1) * request.PageSize;
        var searchPattern = request.SearchTerm is not null 
            ? $"%{request.SearchTerm}%" 
            : null;

        const string countSql = """
            SELECT COUNT(*)
            FROM {table_name} e
            WHERE (@SearchTerm IS NULL OR e.name ILIKE @SearchTerm)
            """;

        const string dataSql = """
            SELECT 
                e.id AS Id,
                e.name AS Name,
                e.description AS Description,
                e.created_at AS CreatedAt
            FROM {table_name} e
            WHERE (@SearchTerm IS NULL OR e.name ILIKE @SearchTerm)
            ORDER BY e.created_at DESC
            OFFSET @Offset ROWS
            FETCH NEXT @PageSize ROWS ONLY
            """;

        var totalCount = await connection.ExecuteScalarAsync<int>(
            countSql,
            new { SearchTerm = searchPattern });

        var items = await connection.QueryAsync<{Entity}Response>(
            dataSql,
            new 
            { 
                SearchTerm = searchPattern,
                Offset = offset,
                request.PageSize 
            });

        return new PagedList<{Entity}Response>(
            items.ToList(),
            request.PageNumber,
            request.PageSize,
            totalCount);
    }
}

// Shared paged list model
public sealed class PagedList<T>
{
    public IReadOnlyList<T> Items { get; }
    public int PageNumber { get; }
    public int PageSize { get; }
    public int TotalCount { get; }
    public int TotalPages => (int)Math.Ceiling(TotalCount / (double)PageSize);
    public bool HasPreviousPage => PageNumber > 1;
    public bool HasNextPage => PageNumber < TotalPages;

    public PagedList(IReadOnlyList<T> items, int pageNumber, int pageSize, int totalCount)
    {
        Items = items;
        PageNumber = pageNumber;
        PageSize = pageSize;
        TotalCount = totalCount;
    }
}
```

---

## Template: Query with Multi-Mapping (Joins)

```csharp
// src/{name}.application/{Feature}/Get{Entity}WithDetails/Get{Entity}WithDetailsQuery.cs
using System.Data;
using Dapper;
using FluentValidation;
using {name}.application.abstractions.data;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.{feature}.Get{Entity}WithDetails;

public sealed record Get{Entity}WithDetailsQuery(
    Guid Id) : IQuery<{Entity}DetailResponse>;

internal sealed class Get{Entity}WithDetailsQueryHandler 
    : IQueryHandler<Get{Entity}WithDetailsQuery, {Entity}DetailResponse>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public Get{Entity}WithDetailsQueryHandler(ISqlConnectionFactory sqlConnectionFactory)
    {
        _sqlConnectionFactory = sqlConnectionFactory;
    }

    public async Task<Result<{Entity}DetailResponse>> Handle(
        Get{Entity}WithDetailsQuery request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        const string sql = """
            SELECT 
                e.id AS Id,
                e.name AS Name,
                e.description AS Description,
                c.id AS ChildId,
                c.name AS ChildName,
                c.sort_order AS ChildSortOrder
            FROM {table_name} e
            LEFT JOIN {child_table} c ON c.{entity}_id = e.id
            WHERE e.id = @Id
            ORDER BY c.sort_order ASC
            """;

        // Dictionary to track parent entity for multi-mapping
        Dictionary<Guid, {Entity}DetailResponse> entityDictionary = new();

        var result = await connection.QueryAsync<{Entity}DetailResponse, {Child}Response, {Entity}DetailResponse>(
            sql,
            (entity, child) =>
            {
                if (!entityDictionary.TryGetValue(entity.Id, out var existingEntity))
                {
                    existingEntity = entity;
                    entityDictionary.Add(entity.Id, existingEntity);
                }

                if (child is not null)
                {
                    existingEntity.Children.Add(child);
                }

                return existingEntity;
            },
            new { request.Id },
            splitOn: "ChildId");

        var {entity} = entityDictionary.Values.FirstOrDefault();

        if ({entity} is null)
        {
            return Result.Failure<{Entity}DetailResponse>({Entity}Errors.NotFound);
        }

        return {entity};
    }
}

// Response with nested children
public sealed class {Entity}DetailResponse
{
    public Guid Id { get; init; }
    public required string Name { get; init; }
    public string? Description { get; init; }
    public List<{Child}Response> Children { get; init; } = new();
}

public sealed class {Child}Response
{
    public Guid ChildId { get; init; }
    public required string ChildName { get; init; }
    public int ChildSortOrder { get; init; }
}
```

---

## Template: Aggregate Report Query

```csharp
// src/{name}.application/Reports/{ReportName}/{ReportName}Query.cs
using System.Data;
using Dapper;
using FluentValidation;
using {name}.application.abstractions.data;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.reports.{ReportName};

public sealed record {ReportName}Query(
    Guid OrganizationId,
    DateTime? StartDate = null,
    DateTime? EndDate = null) : IQuery<IReadOnlyList<{ReportName}Response>>;

internal sealed class {ReportName}QueryValidator : AbstractValidator<{ReportName}Query>
{
    public {ReportName}QueryValidator()
    {
        RuleFor(x => x.OrganizationId).NotEmpty();
        
        RuleFor(x => x.EndDate)
            .GreaterThan(x => x.StartDate)
            .When(x => x.StartDate.HasValue && x.EndDate.HasValue)
            .WithMessage("End date must be after start date");
    }
}

internal sealed class {ReportName}QueryHandler 
    : IQueryHandler<{ReportName}Query, IReadOnlyList<{ReportName}Response>>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public {ReportName}QueryHandler(ISqlConnectionFactory sqlConnectionFactory)
    {
        _sqlConnectionFactory = sqlConnectionFactory;
    }

    public async Task<Result<IReadOnlyList<{ReportName}Response>>> Handle(
        {ReportName}Query request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        const string sql = """
            WITH AggregatedData AS (
                SELECT 
                    d.id AS DepartmentId,
                    d.name AS DepartmentName,
                    COUNT(DISTINCT u.id) AS TotalUsers,
                    ROUND(AVG(a.score), 2) AS AverageScore
                FROM department d
                INNER JOIN user_department ud ON d.id = ud.department_id
                INNER JOIN app_user u ON ud.user_id = u.id
                LEFT JOIN assessment a ON a.user_id = u.id
                WHERE 
                    d.organization_id = @OrganizationId
                    AND (@StartDate IS NULL OR a.created_at >= @StartDate)
                    AND (@EndDate IS NULL OR a.created_at <= @EndDate)
                GROUP BY d.id, d.name
            )
            SELECT 
                DepartmentId,
                DepartmentName,
                TotalUsers,
                AverageScore
            FROM AggregatedData
            ORDER BY AverageScore DESC NULLS LAST
            """;

        var results = await connection.QueryAsync<{ReportName}Response>(
            sql,
            new 
            { 
                request.OrganizationId,
                request.StartDate,
                request.EndDate
            });

        return results.ToList();
    }
}

public sealed class {ReportName}Response
{
    public Guid DepartmentId { get; init; }
    public required string DepartmentName { get; init; }
    public int TotalUsers { get; init; }
    public decimal? AverageScore { get; init; }
}
```

---

## SQL Connection Factory

```csharp
// src/{name}.application/Abstractions/Data/ISqlConnectionFactory.cs
using System.Data;

namespace {name}.application.abstractions.data;

public interface ISqlConnectionFactory
{
    IDbConnection CreateConnection();
}

// src/{name}.infrastructure/Data/SqlConnectionFactory.cs
using System.Data;
using Npgsql;
using {name}.application.abstractions.data;

namespace {name}.infrastructure.data;

internal sealed class SqlConnectionFactory : ISqlConnectionFactory
{
    private readonly string _connectionString;

    public SqlConnectionFactory(string connectionString)
    {
        _connectionString = connectionString;
    }

    public IDbConnection CreateConnection()
    {
        var connection = new NpgsqlConnection(_connectionString);
        connection.Open();
        return connection;
    }
}
```

---

## SQL Best Practices

### Column Naming (Snake Case to PascalCase)

```sql
-- PostgreSQL with snake_case columns
SELECT 
    e.id AS Id,                          -- Maps to Id property
    e.first_name AS FirstName,           -- Maps to FirstName property
    e.created_at AS CreatedAt,           -- Maps to CreatedAt property
    e.organization_id AS OrganizationId  -- Maps to OrganizationId property
FROM entity e
```

### Avoiding N+1 Queries

```sql
-- ❌ BAD: Separate queries for children
SELECT * FROM parent WHERE id = @Id;
-- Then for each parent:
SELECT * FROM child WHERE parent_id = @ParentId;

-- ✅ GOOD: Single query with JOIN
SELECT 
    p.id AS Id, p.name AS Name,
    c.id AS ChildId, c.name AS ChildName
FROM parent p
LEFT JOIN child c ON c.parent_id = p.id
WHERE p.id = @Id
```

### Using CTEs for Complex Queries

```sql
WITH RankedItems AS (
    SELECT 
        *,
        ROW_NUMBER() OVER (PARTITION BY category_id ORDER BY score DESC) as rank
    FROM items
),
TopItems AS (
    SELECT * FROM RankedItems WHERE rank <= 3
)
SELECT * FROM TopItems ORDER BY category_id, rank;
```

---

## Critical Rules

1. **Queries never modify state** - Read-only operations
2. **Use Dapper for queries** - Better performance than EF Core for reads
3. **Return DTOs, not entities** - Don't expose domain models
4. **Use parameterized queries** - Prevent SQL injection
5. **Alias columns to match DTOs** - Use `AS PropertyName`
6. **Always close connections** - Use `using` statement
7. **Use multi-mapping for joins** - Avoid N+1 queries
8. **Validate query parameters** - Especially for pagination
9. **Use CTEs for complex logic** - More readable than nested queries
10. **Handle null results** - Return `Result.Failure` for not found

---

## Anti-Patterns to Avoid

```csharp
// ❌ WRONG: Using EF Core for read queries
public async Task<Result<EntityResponse>> Handle(...)
{
    var entity = await _dbContext.Entities
        .Include(e => e.Children)
        .FirstOrDefaultAsync(e => e.Id == request.Id);
    // Heavy, tracks changes unnecessarily
}

// ✅ CORRECT: Use Dapper
public async Task<Result<EntityResponse>> Handle(...)
{
    using var connection = _sqlConnectionFactory.CreateConnection();
    // Direct SQL, no tracking overhead
}

// ❌ WRONG: Returning domain entities
public sealed record GetEntityQuery(Guid Id) : IQuery<Entity>; // Exposes domain

// ✅ CORRECT: Return DTOs
public sealed record GetEntityQuery(Guid Id) : IQuery<EntityResponse>;

// ❌ WRONG: String concatenation in SQL
var sql = $"SELECT * FROM entity WHERE name = '{request.Name}'"; // SQL injection!

// ✅ CORRECT: Parameterized queries
var sql = "SELECT * FROM entity WHERE name = @Name";
await connection.QueryAsync(sql, new { request.Name });
```

---

## Related Skills

- `cqrs-command-generator` - Generate write-side commands
- `domain-entity-generator` - Generate domain entities
- `ef-core-configuration` - EF Core for write operations
- `result-pattern` - Error handling pattern
