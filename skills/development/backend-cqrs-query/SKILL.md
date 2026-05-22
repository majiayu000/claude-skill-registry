---
name: cqrs-query
description: Use when creating or modifying a CQRS Query (Get, List, Search) or query handler with filtering, paging, or full-text search.
---

# CQRS Query Development Workflow

## Pre-Flight Checklist
- [ ] Search for similar queries: `grep "Query.*{EntityName}" --include="*.cs"`
- [ ] Check if entity has search columns: `grep "DefaultFullTextSearchColumns" {Entity}.cs`
- [ ] Identify if paged or single result needed
- [ ] Check for existing entity expressions: `grep "static.*Expression.*{Entity}" --include="*.cs"`

## File Organization
**Query + Handler + Result = ONE FILE**

```
{Service}.Application/
└── UseCaseQueries/
    └── {Feature}/
        └── Get{Entity}ListQuery.cs  ← Contains all 3 classes
```

## Query Types

### Type 1: Paged List Query
```csharp
public sealed class Get{Entity}ListQuery : PlatformCqrsPagedQuery<Get{Entity}ListQueryResult, {Entity}Dto>
{
    public List<Status> Statuses { get; set; } = [];
    public string? SearchText { get; set; }
    public List<string>? FilterIds { get; set; }
    public DateTime? FromDate { get; set; }
    public DateTime? ToDate { get; set; }
}
```

### Type 2: Single Entity Query
```csharp
public sealed class Get{Entity}ByIdQuery : PlatformCqrsQuery<Get{Entity}ByIdQueryResult>
{
    public string Id { get; set; } = string.Empty;

    public override PlatformValidationResult<IPlatformCqrsRequest> Validate()
    {
        return base.Validate()
            .And(_ => Id.IsNotNullOrEmpty(), "Id is required");
    }
}
```

## Handler Implementation

### Paged Query Handler with GetQueryBuilder
```csharp
internal sealed class Get{Entity}ListQueryHandler :
    PlatformCqrsQueryApplicationHandler<Get{Entity}ListQuery, Get{Entity}ListQueryResult>
{
    private readonly I{Service}RootRepository<{Entity}> repository;
    private readonly IPlatformFullTextSearchPersistenceService searchService;

    protected override async Task<Get{Entity}ListQueryResult> HandleAsync(
        Get{Entity}ListQuery req, CancellationToken ct)
    {
        // Build reusable query with GetQueryBuilder
        var queryBuilder = repository.GetQueryBuilder((uow, q) => q
            .Where(e => e.CompanyId == RequestContext.CurrentCompanyId())
            .WhereIf(req.Statuses.Any(), e => req.Statuses.Contains(e.Status))
            .WhereIf(req.FilterIds.IsNotNullOrEmpty(), e => req.FilterIds!.Contains(e.Id))
            .WhereIf(req.FromDate.HasValue, e => e.CreatedDate >= req.FromDate)
            .WhereIf(req.ToDate.HasValue, e => e.CreatedDate <= req.ToDate)
            .PipeIf(req.SearchText.IsNotNullOrEmpty(), q =>
                searchService.Search(q, req.SearchText, {Entity}.DefaultFullTextSearchColumns())));

        // Parallel tuple queries (count + data)
        var (total, items) = await (
            repository.CountAsync((uow, q) => queryBuilder(uow, q), ct),
            repository.GetAllAsync((uow, q) => queryBuilder(uow, q)
                .OrderByDescending(e => e.CreatedDate)
                .PageBy(req.SkipCount, req.MaxResultCount), ct,
                e => e.RelatedEntity,     // Eager load related
                e => e.AnotherRelated)
        );

        // Map to DTOs
        return new Get{Entity}ListQueryResult(
            items.SelectList(e => new {Entity}Dto(e).WithRelated(e.RelatedEntity)),
            total,
            req);
    }
}
```

### Single Entity Handler
```csharp
protected override async Task<Get{Entity}ByIdQueryResult> HandleAsync(
    Get{Entity}ByIdQuery req, CancellationToken ct)
{
    var entity = await repository.GetByIdAsync(req.Id, ct,
        e => e.RelatedEntity,
        e => e.Children)
        .EnsureFound($"Entity not found: {req.Id}");

    return new Get{Entity}ByIdQueryResult
    {
        Entity = new {Entity}Dto(entity)
            .WithRelated(entity.RelatedEntity)
            .WithChildren(entity.Children)
    };
}
```

## Key Query Patterns

| Pattern | Usage | Example |
|---------|-------|---------|
| `GetQueryBuilder` | Reusable query | `repository.GetQueryBuilder((uow, q) => ...)` |
| `WhereIf` | Conditional filter | `.WhereIf(ids.Any(), e => ids.Contains(e.Id))` |
| `PipeIf` | Conditional transform | `.PipeIf(text != null, q => searchService.Search(...))` |
| `PageBy` | Pagination | `.PageBy(skip, take)` |
| Tuple await | Parallel queries | `var (count, items) = await (q1, q2)` |
| Eager load | Load relations | `GetByIdAsync(id, ct, e => e.Related)` |

## Full-Text Search Pattern
```csharp
// In entity - define searchable columns
public static Expression<Func<{Entity}, object?>>[] DefaultFullTextSearchColumns()
    => [e => e.Name, e => e.Code, e => e.Description, e => e.Email];

// In query handler
.PipeIf(req.SearchText.IsNotNullOrEmpty(), q =>
    searchService.Search(
        q,
        req.SearchText,
        {Entity}.DefaultFullTextSearchColumns(),
        fullTextAccurateMatch: true,      // true=exact phrase, false=fuzzy
        includeStartWithProps: {Entity}.DefaultFullTextSearchColumns()  // For autocomplete
    ))
```

## Advanced: Aggregation Query
```csharp
// Get data + aggregated counts in parallel
var (total, items, statusCounts) = await (
    repository.CountAsync((uow, q) => queryBuilder(uow, q), ct),
    repository.GetAllAsync((uow, q) => queryBuilder(uow, q).PageBy(skip, take), ct),
    repository.GetAllAsync((uow, q) => queryBuilder(uow, q)
        .GroupBy(e => e.Status)
        .Select(g => new { Status = g.Key, Count = g.Count() }), ct)
);
```

## Anti-Patterns to AVOID
- :x: Using raw `query.Where()` instead of `GetQueryBuilder`
- :x: Sequential await for independent queries (use tuple await)
- :x: Forgetting eager loading (causes N+1 queries)
- :x: Hardcoding company/user filters (use `RequestContext`)

## Verification Checklist
- [ ] Uses `GetQueryBuilder` for reusable queries
- [ ] Uses `WhereIf` for optional filters
- [ ] Uses tuple await for parallel count + data
- [ ] Full-text search uses entity's `DefaultFullTextSearchColumns()`
- [ ] Proper eager loading with params
- [ ] Uses `RequestContext` for tenant/user context
