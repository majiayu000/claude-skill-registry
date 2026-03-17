---
name: koan-entity-first
description: Entity<T> patterns, GUID v7 auto-generation, static methods vs manual repositories
---

# Koan Entity-First Development

## Core Principle

**Entity<T> replaces manual repositories.** Every entity is self-aware and self-persisting. This pattern eliminates repository boilerplate while maintaining provider transparency.

## Revolutionary Approach

- **GUID v7 Auto-Generation**: IDs generated automatically with chronological ordering
- **Instance Methods**: `await entity.Save()`, `await entity.Remove()`
- **Static Queries**: `await Entity.All()`, `await Entity.Get(id)`, `await Entity.Query()`
- **Provider Agnostic**: Same code works across SQL, NoSQL, Vector, JSON stores

## Quick Reference Card

### Basic Operations

```csharp
// Create entity
public class Todo : Entity<Todo>
{
    public string Title { get; set; } = "";
    public bool Completed { get; set; }
    // Id automatically generated as GUID v7 on first access
}

// Save (create or update)
var todo = new Todo { Title = "Buy milk" };
await todo.Save();

// Retrieve by ID
var loaded = await Todo.Get(id);

// Query all
var allTodos = await Todo.All();

// Filter with LINQ
var completed = await Todo.Query(t => t.Completed);

// Remove
await todo.Remove();
```

### Custom Keys (When Needed)

```csharp
// For non-GUID keys: Entity<T, TKey>
public class NumericEntity : Entity<NumericEntity, int>
{
    public override int Id { get; set; }
    public string Title { get; set; } = "";
}

// Manual key management
var entity = new NumericEntity { Id = 42, Title = "Meaningful" };
await entity.Save();
```

## Batch Operations

### Batch Retrieval (Prevents N+1 Queries)

```csharp
// ✅ EFFICIENT: Single bulk query with IN clause
var ids = new[] { id1, id2, id3, id4 };
var todos = await Todo.Get(ids, ct);
// Result: [Todo?, Todo?, null, Todo?] - preserves order, null for missing

// ❌ INEFFICIENT: N database round-trips
var todos = new List<Todo?>();
foreach (var id in ids)
{
    todos.Add(await Todo.Get(id, ct));  // N queries!
}
```

**Use Cases:**
- Collection/playlist pagination - fetch page of items by stored IDs
- Relationship navigation - fetch all related entities at once
- Bulk validation - check which IDs exist in single query

**Performance:** Single query vs N queries = 10-100x faster for typical datasets

### Batch Persistence

```csharp
// Bulk save - efficient provider-specific batching
var todos = Enumerable.Range(0, 1000)
    .Select(i => new Todo { Title = $"Task {i}" })
    .ToList();
await todos.Save();

// Batch operations - add/update/delete in one transaction
await Todo.Batch()
    .Add(new Todo { Title = "New task" })
    .Update(existingId, todo => todo.Completed = true)
    .Delete(oldId)
    .SaveAsync();
```

## Pagination & Streaming

### Pagination (Web APIs)

```csharp
// Basic pagination
var page = await Todo.Page(pageNumber: 1, pageSize: 20);

// With total count for UI
var result = await Todo.QueryWithCount(
    t => t.ProjectId == projectId,
    new DataQueryOptions(
        orderBy: nameof(Todo.Created),
        descending: true
    ),
    ct);
Console.WriteLine($"Showing {result.Items.Count} of {result.TotalCount}");
```

### Streaming (Large Datasets)

```csharp
// Stream to avoid loading everything into memory
await foreach (var todo in Todo.AllStream(batchSize: 1000, ct))
{
    // Process in batches - memory-efficient
    await ProcessTodo(todo);
}

// Stream with filter
await foreach (var reading in Reading.QueryStream(
    "plot == 'A1'",
    batchSize: 200,
    ct))
{
    await ProcessReading(reading);
}
```

**When to Stream:** Large datasets (>10k records), background jobs, ETL pipelines

## Anti-Patterns to Avoid

### ❌ WRONG: Manual Repository Pattern

```csharp
// DON'T create repository interfaces
public interface ITodoRepository
{
    Task<Todo> GetAsync(string id);
    Task SaveAsync(Todo todo);
    Task<List<Todo>> GetAllAsync();
}

// DON'T inject repositories
public class TodoService
{
    private readonly ITodoRepository _repo; // Unnecessary!
    public TodoService(ITodoRepository repo) => _repo = repo;
}
```

**Why wrong?** Entity<T> already provides all repository functionality. Manual repositories:
- Duplicate framework features
- Break provider transparency
- Add unnecessary abstraction layers
- Increase maintenance burden

### ✅ CORRECT: Entity Service Pattern

```csharp
// Business logic services use Entity<T> directly
public class TodoService
{
    public async Task<Todo> CompleteAsync(string id)
    {
        var todo = await Todo.Get(id); // Direct entity usage
        if (todo is null)
            throw new InvalidOperationException("Todo not found");

        todo.Completed = true;
        return await todo.Save(); // Instance save method
    }

    public async Task<List<Todo>> GetCompletedAsync()
    {
        return await Todo.Query(t => t.Completed); // Static query
    }
}
```

## When This Skill Applies

Invoke this skill when:
- ✅ Creating new entities
- ✅ Adding data access code
- ✅ Refactoring repositories to Entity<T>
- ✅ Building CRUD operations
- ✅ Reviewing data access patterns
- ✅ Troubleshooting entity persistence
- ✅ Optimizing queries (batch operations, streaming)

## Advanced: Count Operations

```csharp
// Default: framework chooses best strategy (usually optimized)
var total = await Todo.Count;

// Explicit exact count (guaranteed accuracy, may be slower)
var exact = await Todo.Count.Exact(ct);

// Explicit fast count (metadata estimate, extremely fast)
var fast = await Todo.Count.Fast(ct);

// Filtered count
var completed = await Todo.Count.Where(t => t.Completed);
```

**Performance:** Fast counts use database metadata (1000-20000x faster on large tables)
- Postgres: `pg_stat_user_tables` (~5ms vs 25s for 10M rows)
- SQL Server: `sys.dm_db_partition_stats` (~1ms vs 20s)
- MongoDB: `estimatedDocumentCount()` (~10ms vs 15s)

**When to Use:**
- **Fast**: Pagination UI, dashboard summaries, estimates acceptable
- **Exact**: Critical business logic, inventory counts, reports requiring accuracy

## Bundled Resources

- `examples/entity-crud.cs` - Complete CRUD patterns
- `examples/entity-relationships.cs` - Navigation helpers
- `examples/batch-operations.cs` - Bulk loading and saving
- `anti-patterns/manual-repositories.md` - What NOT to do with detailed explanations

## Reference Documentation

- **Full Guide:** `docs/guides/entity-capabilities-howto.md`
- **Data Modeling:** `docs/guides/data-modeling.md`
- **ADR:** DATA-0059 (Entity-first facade decision)
- **Sample:** `samples/S1.Web/` (Relationship patterns)
- **Sample:** `samples/S0.ConsoleJsonRepo/` (Minimal 20-line example)

## Framework Compliance

Entity<T> patterns are **mandatory** in Koan Framework. Manual repositories break:
- Provider transparency
- Framework auto-registration
- Capability detection
- Multi-tenant context routing

Always prefer Entity<T> patterns over custom data access abstractions.
