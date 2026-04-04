---
name: koan-performance
description: Streaming, pagination, count strategies, bulk operations
---

# Koan Performance

## Core Principle

**Optimize for scale from day one.** Use streaming for large datasets, batch operations for bulk changes, fast counts for UI, and pagination for web APIs.

## Performance Patterns

### Streaming (Large Datasets)

```csharp
// ❌ WRONG: Load everything into memory
var allTodos = await Todo.All(); // 1 million records!

// ✅ CORRECT: Stream in batches
await foreach (var todo in Todo.AllStream(batchSize: 1000))
{
    await ProcessTodo(todo);
}
```

### Count Strategies

```csharp
// Fast count (metadata estimate - 1000x+ faster)
var fast = await Todo.Count.Fast(ct); // ~5ms for 10M rows

// Exact count (guaranteed accuracy)
var exact = await Todo.Count.Exact(ct); // ~25s for 10M rows

// Optimized (framework chooses)
var optimized = await Todo.Count; // Uses Fast if available
```

**Use Fast for:** Pagination UI, dashboards, estimates
**Use Exact for:** Critical business logic, reports, inventory

### Bulk Operations

```csharp
// Bulk create
var todos = Enumerable.Range(1, 1000)
    .Select(i => new Todo { Title = $"Task {i}" })
    .ToList();
await todos.Save(); // Single operation

// Bulk removal
await Todo.RemoveAll(RemoveStrategy.Fast); // TRUNCATE/DROP (225x faster)
```

### Batch Retrieval

```csharp
// ❌ WRONG: N queries
foreach (var id in ids)
{
    var todo = await Todo.Get(id);
}

// ✅ CORRECT: 1 query
var todos = await Todo.Get(ids);
```

### Pagination

```csharp
public async Task<IActionResult> GetTodos(
    int page = 1,
    int pageSize = 20,
    CancellationToken ct = default)
{
    var result = await Todo.QueryWithCount(
        t => !t.Completed,
        new DataQueryOptions { OrderBy = nameof(Todo.Created), Descending = true },
        ct);

    Response.Headers["X-Total-Count"] = result.TotalCount.ToString();
    return Ok(result.Items);
}
```

## Performance Benchmarks

| Operation | Inefficient | Efficient | Speedup |
|-----------|-------------|-----------|---------|
| **Bulk Remove (1M)** | DELETE loop ~45s | TRUNCATE ~200ms | 225x |
| **Count (10M)** | Full scan ~25s | Metadata ~5ms | 5000x |
| **Batch Get (100)** | 100 queries | 1 query | 100x |
| **Stream (1M)** | Load all (OOM) | Stream batches | Memory safe |

## When This Skill Applies

- ✅ Performance tuning
- ✅ Large datasets
- ✅ Optimization
- ✅ Production readiness
- ✅ Memory issues
- ✅ Query optimization

## Reference Documentation

- **Example Code:** `.claude/skills/entity-first/examples/batch-operations.cs`
- **Guide:** `docs/guides/performance.md`
- **Sample:** `samples/S14.AdapterBench/` (Performance benchmarks)
