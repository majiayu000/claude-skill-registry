---
name: dapper-query-builder
description: "Generates optimized read queries using Dapper. Includes multi-mapping for joins, pagination, dynamic filtering, CTEs, and best practices for high-performance data access."
version: 1.0.0
language: C#
framework: .NET 8+
dependencies: Dapper
---

# Dapper Query Builder

## Overview

Dapper provides lightweight, high-performance data access:

- **Raw SQL** - Full control over queries
- **Multi-mapping** - Handle complex joins
- **Parameterized queries** - SQL injection protection
- **Minimal overhead** - Near ADO.NET performance

## Quick Reference

| Method | Purpose | Use Case |
|--------|---------|----------|
| `QueryAsync<T>` | Multiple rows | Lists, reports |
| `QueryFirstOrDefaultAsync<T>` | Single row | Get by ID |
| `QueryMultipleAsync` | Multiple result sets | Complex data |
| `ExecuteAsync` | No results | Insert/Update/Delete |
| `ExecuteScalarAsync<T>` | Single value | Count, exists |

---

## Template: Basic Query Handler

```csharp
// src/{name}.application/{Feature}/Get{Entity}ById/Get{Entity}ByIdQueryHandler.cs
using System.Data;
using Dapper;
using {name}.application.abstractions.data;
using {name}.application.abstractions.messaging;
using {name}.domain.abstractions;

namespace {name}.application.{feature}.Get{Entity}ById;

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
                e.is_active AS IsActive,
                e.created_at AS CreatedAt,
                o.id AS OrganizationId,
                o.name AS OrganizationName
            FROM entity e
            INNER JOIN organization o ON e.organization_id = o.id
            WHERE e.id = @Id
            """;

        var entity = await connection.QueryFirstOrDefaultAsync<{Entity}Response>(
            sql,
            new { request.Id });

        return entity is null
            ? Result.Failure<{Entity}Response>({Entity}Errors.NotFound)
            : entity;
    }
}
```

---

## Template: Multi-Mapping (One-to-Many)

```csharp
internal sealed class Get{Entity}WithDetailsQueryHandler 
    : IQueryHandler<Get{Entity}WithDetailsQuery, {Entity}DetailResponse>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public async Task<Result<{Entity}DetailResponse>> Handle(
        Get{Entity}WithDetailsQuery request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        const string sql = """
            SELECT 
                e.id AS Id,
                e.name AS Name,
                c.id AS ChildId,
                c.name AS ChildName,
                c.sort_order AS SortOrder
            FROM entity e
            LEFT JOIN child c ON c.entity_id = e.id
            WHERE e.id = @Id
            ORDER BY c.sort_order
            """;

        var entityDict = new Dictionary<Guid, {Entity}DetailResponse>();

        await connection.QueryAsync<{Entity}DetailResponse, ChildResponse, {Entity}DetailResponse>(
            sql,
            (entity, child) =>
            {
                if (!entityDict.TryGetValue(entity.Id, out var existingEntity))
                {
                    existingEntity = entity;
                    existingEntity.Children = new List<ChildResponse>();
                    entityDict.Add(entity.Id, existingEntity);
                }

                if (child is not null)
                {
                    existingEntity.Children.Add(child);
                }

                return existingEntity;
            },
            new { request.Id },
            splitOn: "ChildId");

        var result = entityDict.Values.FirstOrDefault();

        return result is null
            ? Result.Failure<{Entity}DetailResponse>({Entity}Errors.NotFound)
            : result;
    }
}
```

---

## Template: Paginated Query with Filtering

```csharp
internal sealed class Search{Entities}QueryHandler 
    : IQueryHandler<Search{Entities}Query, PagedList<{Entity}Response>>
{
    private readonly ISqlConnectionFactory _sqlConnectionFactory;

    public async Task<Result<PagedList<{Entity}Response>>> Handle(
        Search{Entities}Query request,
        CancellationToken cancellationToken)
    {
        using IDbConnection connection = _sqlConnectionFactory.CreateConnection();

        var offset = (request.PageNumber - 1) * request.PageSize;
        var searchPattern = request.SearchTerm is not null 
            ? $"%{request.SearchTerm}%" 
            : null;

        // Build dynamic WHERE clause
        var whereConditions = new List<string> { "1 = 1" };
        
        if (searchPattern is not null)
            whereConditions.Add("(e.name ILIKE @SearchPattern OR e.description ILIKE @SearchPattern)");
        
        if (request.OrganizationId.HasValue)
            whereConditions.Add("e.organization_id = @OrganizationId");
        
        if (request.IsActive.HasValue)
            whereConditions.Add("e.is_active = @IsActive");

        var whereClause = string.Join(" AND ", whereConditions);

        var countSql = $"""
            SELECT COUNT(*)
            FROM entity e
            WHERE {whereClause}
            """;

        var dataSql = $"""
            SELECT 
                e.id AS Id,
                e.name AS Name,
                e.description AS Description,
                e.is_active AS IsActive,
                e.created_at AS CreatedAt
            FROM entity e
            WHERE {whereClause}
            ORDER BY e.created_at DESC
            OFFSET @Offset ROWS
            FETCH NEXT @PageSize ROWS ONLY
            """;

        var parameters = new
        {
            SearchPattern = searchPattern,
            request.OrganizationId,
            request.IsActive,
            Offset = offset,
            request.PageSize
        };

        var totalCount = await connection.ExecuteScalarAsync<int>(countSql, parameters);
        var items = await connection.QueryAsync<{Entity}Response>(dataSql, parameters);

        return new PagedList<{Entity}Response>(
            items.ToList(),
            request.PageNumber,
            request.PageSize,
            totalCount);
    }
}
```

---

## Template: CTE (Common Table Expression)

```csharp
const string sql = """
    WITH RankedItems AS (
        SELECT 
            e.*,
            ROW_NUMBER() OVER (PARTITION BY e.category_id ORDER BY e.score DESC) as rank
        FROM entity e
        WHERE e.organization_id = @OrganizationId
    ),
    TopItems AS (
        SELECT * FROM RankedItems WHERE rank <= 3
    )
    SELECT 
        ti.id AS Id,
        ti.name AS Name,
        ti.score AS Score,
        ti.rank AS Rank,
        c.name AS CategoryName
    FROM TopItems ti
    INNER JOIN category c ON ti.category_id = c.id
    ORDER BY c.name, ti.rank
    """;
```

---

## Template: SQL Connection Factory

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

## Column Mapping (Snake Case → PascalCase)

```sql
SELECT 
    e.id AS Id,                          -- Maps to Id
    e.first_name AS FirstName,           -- Maps to FirstName
    e.created_at AS CreatedAt,           -- Maps to CreatedAt
    e.organization_id AS OrganizationId  -- Maps to OrganizationId
FROM entity e
```

---

## Critical Rules

1. **Always use parameters** - Never concatenate user input
2. **Use `using` for connections** - Proper disposal
3. **Alias columns to match DTOs** - `AS PropertyName`
4. **Multi-mapping for joins** - Avoid N+1 queries
5. **CTEs for complex logic** - More readable than nested queries
6. **OFFSET/FETCH for pagination** - Standard SQL pagination
7. **ILIKE for case-insensitive** - PostgreSQL specific
8. **Return DTOs not entities** - Query projections only

---

## Related Skills

- `cqrs-query-generator` - Query handler structure
- `repository-pattern` - EF Core for writes
- `dotnet-clean-architecture` - Application layer
