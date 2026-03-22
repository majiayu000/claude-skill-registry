---
version: 1.0.0
name: dev-dotnet-efcore
description: >
  EF Core query optimization and best practices. Covers N+1 detection, query
  splitting, compiled queries, change tracking optimization, and migration strategies.
  Conditionally installed when project uses EF Core.
disable-model-invocation: true
user-invocable: false
context: fork
---

# EF Core Optimization

Query optimization, change tracking, and migration best practices for Entity Framework Core.

> **Stack:** C#/.NET (EF Core 8+)

## When to Use

- Slow database queries or API responses
- EF Core code review (new repositories, query changes)
- Planning EF Core migrations
- Investigating N+1 query patterns in Aspire traces

## Core Principle

**Measure before optimizing.** Use SQL logging or Aspire distributed traces to identify actual bottlenecks. Don't optimize queries that aren't slow.

## Query Optimization Checklist

Run through these checks for any EF Core data access code:

### 1. Enable SQL Logging (development only)

```csharp
optionsBuilder
    .LogTo(Console.WriteLine, LogLevel.Information)
    .EnableSensitiveDataLogging()  // Shows parameter values
    .EnableDetailedErrors();       // Better error messages
```

### 2. Check for N+1 Queries

**Bad — loads related data in a loop:**
```csharp
var orders = await db.Orders.ToListAsync();
foreach (var order in orders)
{
    var items = order.Items; // Lazy load = 1 query per order!
}
```

**Fix — eager load with Include:**
```csharp
var orders = await db.Orders
    .Include(o => o.Items)
    .ToListAsync();
```

### 3. Check for Over-Fetching

**Bad — loads entire entity when only 2 fields needed:**
```csharp
var users = await db.Users.ToListAsync();
return users.Select(u => new { u.Name, u.Email });
```

**Fix — project at the database level:**
```csharp
var users = await db.Users
    .Select(u => new { u.Name, u.Email })
    .ToListAsync();
```

### 4. Check for Client-Side Evaluation

If a LINQ expression can't be translated to SQL, EF Core evaluates it in memory. Watch for warnings:
```
The LINQ expression could not be translated and will be evaluated locally.
```

**Fix:** Restructure the query to use translatable expressions, or explicitly call `.AsEnumerable()` at the point where you intend client evaluation.

### 5. Use AsNoTracking for Read-Only Queries

```csharp
var products = await db.Products
    .AsNoTracking()  // No change tracking overhead
    .Where(p => p.IsActive)
    .ToListAsync();
```

### 6. Use Split Queries for Complex Includes

```csharp
var orders = await db.Orders
    .Include(o => o.Items)
    .Include(o => o.Customer)
    .Include(o => o.ShippingAddress)
    .AsSplitQuery()  // Prevents cartesian explosion
    .ToListAsync();
```

### 7. Use Compiled Queries for Hot Paths

```csharp
private static readonly Func<AppDbContext, int, Task<Order?>> GetOrderById =
    EF.CompileAsyncQuery((AppDbContext db, int id) =>
        db.Orders
            .Include(o => o.Items)
            .FirstOrDefault(o => o.Id == id));

// Usage:
var order = await GetOrderById(db, orderId);
```

## Change Tracking

### Default: Track Everything

EF Core tracks all queried entities by default. This is expensive for read-heavy workloads.

### Opt-Out Per Query

```csharp
var data = await db.Products.AsNoTracking().ToListAsync();
```

### Opt-Out Globally

For read-heavy services, disable tracking by default:

```csharp
services.AddDbContext<AppDbContext>(options =>
{
    options.UseNpgsql(connectionString);
    options.UseQueryTrackingBehavior(QueryTrackingBehavior.NoTracking);
});
```

Then opt-in for mutations:
```csharp
db.ChangeTracker.QueryTrackingBehavior = QueryTrackingBehavior.TrackAll;
var entity = await db.Products.FindAsync(id);
entity.Name = "Updated";
await db.SaveChangesAsync();
```

## Migration Best Practices

### Always Review Generated SQL

```bash
# Generate migration
dotnet ef migrations add AddUserEmail

# Review the SQL it will execute
dotnet ef migrations script --idempotent

# Or for a specific migration
dotnet ef migrations script PreviousMigration AddUserEmail
```

### Idempotent Migrations

Always generate idempotent scripts for production:
```bash
dotnet ef migrations script --idempotent -o migration.sql
```

### Data Migrations vs Schema Migrations

Keep them separate:
- **Schema migration:** Add column, create index, rename table
- **Data migration:** Backfill values, transform data, seed lookup tables

Never mix data manipulation with schema changes in the same migration.

### HasData Sparingly

```csharp
// OK for lookup tables (enum-like data)
modelBuilder.Entity<OrderStatus>().HasData(
    new OrderStatus { Id = 1, Name = "Pending" },
    new OrderStatus { Id = 2, Name = "Shipped" }
);

// BAD for user data or dynamic content
// Use a separate seeding mechanism instead
```

## Performance Patterns

### Batch Operations (EF Core 7+)

```csharp
// Bulk update — single SQL statement, no entity loading
await db.Products
    .Where(p => p.CategoryId == oldCategoryId)
    .ExecuteUpdateAsync(s => s.SetProperty(p => p.CategoryId, newCategoryId));

// Bulk delete — single SQL statement
await db.Orders
    .Where(o => o.CreatedAt < cutoffDate)
    .ExecuteDeleteAsync();
```

### Raw SQL for Complex Reports

```csharp
var report = await db.Database
    .SqlQuery<SalesReport>($"""
        SELECT CategoryName, SUM(Total) as Revenue, COUNT(*) as OrderCount
        FROM Orders o
        JOIN Categories c ON o.CategoryId = c.Id
        WHERE o.CreatedAt >= {startDate}
        GROUP BY CategoryName
        ORDER BY Revenue DESC
    """)
    .ToListAsync();
```

### Connection Resiliency

```csharp
services.AddDbContext<AppDbContext>(options =>
{
    options.UseNpgsql(connectionString, npgsql =>
    {
        npgsql.EnableRetryOnFailure(
            maxRetryCount: 3,
            maxRetryDelay: TimeSpan.FromSeconds(5),
            errorCodesToAdd: null);
    });
});
```

## Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| Lazy loading in APIs | N+1 queries per request | Eager load with `.Include()` |
| `ToList()` then `Where()` | Loads entire table into memory | Filter in query (`.Where()` before `.ToList()`) |
| `Find()` in a loop | N queries for N entities | Use `.Where(e => ids.Contains(e.Id))` |
| Missing indexes | Full table scans | Add `HasIndex()` in `OnModelCreating` |
| SaveChanges in a loop | N transactions | Batch changes, single `SaveChangesAsync()` |
| DbContext as singleton | Thread-safety issues, memory leaks | Use scoped lifetime (default) |
| No query timeout | Runaway queries block connections | Set `CommandTimeout` in options |

## Reference Docs

- [query-optimization.md](references/query-optimization.md) — Deep dive into query patterns, pagination, indexes, and benchmarking
