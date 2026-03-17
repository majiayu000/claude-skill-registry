---
name: database-optimization
description: Use when optimizing database queries, indexes, N+1 problems, slow queries, or analyzing query performance. Triggers on keywords like "slow query", "N+1", "index", "query optimization", "database performance", "eager loading".
allowed-tools: Read, Write, Edit, Bash, Grep, Glob, Task, TodoWrite
infer: true
---

# Database Optimization

Expert database performance agent for EasyPlatform. Optimizes queries, indexes, and data access patterns for MongoDB, SQL Server, and PostgreSQL.

## Common Performance Issues

### N+1 Query Problem

```csharp
// BAD: N+1 queries - one query per employee's department
var employees = await repo.GetAllAsync(e => e.CompanyId == companyId, ct);
foreach (var emp in employees)
{
    var dept = await deptRepo.GetByIdAsync(emp.DepartmentId, ct);  // N queries!
}

// GOOD: Eager loading with loadRelatedEntities
var employees = await repo.GetAllAsync(
    e => e.CompanyId == companyId,
    ct,
    loadRelatedEntities: e => e.Department);  // Single query with join

// GOOD: Batch load related entities
var employees = await repo.GetAllAsync(e => e.CompanyId == companyId, ct);
var deptIds = employees.Select(e => e.DepartmentId).Distinct().ToList();
var departments = await deptRepo.GetByIdsAsync(deptIds, ct);
var deptMap = departments.ToDictionary(d => d.Id);
employees.ForEach(e => e.Department = deptMap.GetValueOrDefault(e.DepartmentId));
```

### Select Only Needed Columns

```csharp
// BAD: Fetching entire entity when only ID needed
var employee = await repo.GetByIdAsync(id, ct);
return employee.Id;

// GOOD: Projection to fetch only needed data
var employeeId = await repo.FirstOrDefaultAsync(
    query => query
        .Where(Employee.UniqueExpr(userId, companyId))
        .Select(e => e.Id),  // Only fetch ID column
    ct);
```

### Parallel Independent Queries

```csharp
// BAD: Sequential queries that could run in parallel
var count = await repo.CountAsync(filter, ct);
var items = await repo.GetAllAsync(filter, ct);
var stats = await statsRepo.GetAsync(companyId, ct);

// GOOD: Parallel tuple queries
var (count, items, stats) = await (
    repo.CountAsync((uow, q) => queryBuilder(uow, q), ct),
    repo.GetAllAsync((uow, q) => queryBuilder(uow, q).PageBy(skip, take), ct),
    statsRepo.GetAsync(companyId, ct)
);
```

## Query Optimization Patterns

### GetQueryBuilder for Reusable Queries

```csharp
protected override async Task<Result> HandleAsync(Query req, CancellationToken ct)
{
    // Define query once, reuse for count and data
    var queryBuilder = repo.GetQueryBuilder((uow, q) => q
        .Where(Employee.OfCompanyExpr(RequestContext.CurrentCompanyId()))
        .WhereIf(req.Statuses.Any(), e => req.Statuses.Contains(e.Status))
        .WhereIf(req.DepartmentId.IsNotNullOrEmpty(), e => e.DepartmentId == req.DepartmentId)
        .PipeIf(req.SearchText.IsNotNullOrEmpty(), q =>
            fullTextSearch.Search(q, req.SearchText, Employee.SearchColumns())));

    // Parallel execution
    var (total, items) = await (
        repo.CountAsync((uow, q) => queryBuilder(uow, q), ct),
        repo.GetAllAsync((uow, q) => queryBuilder(uow, q)
            .OrderByDescending(e => e.CreatedDate)
            .PageBy(req.SkipCount, req.MaxResultCount), ct)
    );

    return new Result(items, total);
}
```

### Conditional Filtering with WhereIf

```csharp
// Builds efficient query with only needed conditions
var query = repo.GetQueryBuilder((uow, q) => q
    .Where(e => e.CompanyId == companyId)  // Always applied
    .WhereIf(status.HasValue, e => e.Status == status)  // Only if provided
    .WhereIf(deptIds.Any(), e => deptIds.Contains(e.DepartmentId))
    .WhereIf(dateFrom.HasValue, e => e.CreatedDate >= dateFrom)
    .WhereIf(dateTo.HasValue, e => e.CreatedDate <= dateTo));
```

### Full-Text Search Optimization

```csharp
// Define searchable columns in entity
public static Expression<Func<Employee, object?>>[] DefaultFullTextSearchColumns()
    => [e => e.FullName, e => e.Email, e => e.EmployeeCode, e => e.FullTextSearch];

// Use full-text search service
.PipeIf(searchText.IsNotNullOrEmpty(), q => fullTextSearch.Search(
    q,
    searchText,
    Employee.DefaultFullTextSearchColumns(),
    fullTextAccurateMatch: true,  // Exact phrase match
    includeStartWithProps: [e => e.FullName, e => e.EmployeeCode]  // Prefix matching
));
```

## Index Recommendations

### MongoDB Indexes

```csharp
// Single field index - for equality queries
{ "CompanyId": 1 }

// Compound index - for filtered queries
{ "CompanyId": 1, "Status": 1, "CreatedDate": -1 }

// Text index - for full-text search
{ "FullName": "text", "Email": "text", "EmployeeCode": "text" }

// Sparse index - for optional fields
{ "ExternalId": 1, sparse: true }
```

### SQL Server / PostgreSQL Indexes

```sql
-- Covering index for common query
CREATE INDEX IX_Employee_Company_Status
ON Employees (CompanyId, Status)
INCLUDE (FullName, Email, CreatedDate);

-- Filtered index for active records
CREATE INDEX IX_Employee_Active
ON Employees (CompanyId, CreatedDate)
WHERE Status = 'Active' AND IsDeleted = 0;

-- Full-text index
CREATE FULLTEXT INDEX ON Employees (FullName, Email)
KEY INDEX PK_Employees;
```

## Pagination Best Practices

```csharp
// GOOD: Keyset pagination for large datasets (cursor-based)
var items = await repo.GetAllAsync(q => q
    .Where(e => e.CompanyId == companyId)
    .Where(e => e.Id > lastId)  // Cursor
    .OrderBy(e => e.Id)
    .Take(pageSize), ct);

// GOOD: Offset pagination for moderate datasets
var items = await repo.GetAllAsync(q => q
    .Where(filter)
    .OrderByDescending(e => e.CreatedDate)
    .PageBy(skip, take), ct);  // Platform helper

// BAD: Skip without limit (fetches all then skips)
var items = await repo.GetAllAsync(q => q.Skip(1000), ct);
```

## Bulk Operations

```csharp
// Bulk insert
await repo.CreateManyAsync(entities, ct);

// Bulk update (with optimization flags)
await repo.UpdateManyAsync(
    entities,
    dismissSendEvent: true,  // Skip entity events for performance
    checkDiff: false,        // Skip change detection
    ct);

// Bulk delete by expression
await repo.DeleteManyAsync(e => e.Status == Status.Deleted && e.DeletedDate < cutoffDate, ct);
```

## Performance Analysis Workflow

### Phase 1: Identify Slow Queries

1. Check application logs for slow query warnings
2. Review query patterns in handlers
3. Look for N+1 patterns (loops with DB calls)

### Phase 2: Analyze Query Plan

```csharp
// MongoDB - Check indexes used
db.employees.find({ companyId: "x", status: "Active" }).explain("executionStats")

// SQL Server - Check execution plan
SET STATISTICS IO ON
SELECT * FROM Employees WHERE CompanyId = 'x' AND Status = 'Active'
```

### Phase 3: Optimize

1. Add missing indexes
2. Use eager loading for related entities
3. Add projections for partial data needs
4. Parallelize independent queries
5. Implement caching for frequently accessed data

## Optimization Checklist

- [ ] N+1 queries identified and fixed?
- [ ] Eager loading for related entities?
- [ ] Projections for partial data needs?
- [ ] Parallel queries for independent operations?
- [ ] Proper indexes for filter/sort columns?
- [ ] Pagination implemented correctly?
- [ ] Full-text search for text queries?
- [ ] Bulk operations for batch processing?

## Anti-Patterns

- **Loading entire collections**: Always filter and paginate
- **Fetching unused data**: Use projections
- **Sequential independent queries**: Use parallel tuple queries
- **Index on every column**: Only index frequently queried fields
- **Skip without ordering**: Always order before pagination
