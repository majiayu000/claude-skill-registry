---
name: koan-multi-provider
description: Provider transparency, capability detection, context routing (partition/source/adapter)
---

# Koan Multi-Provider Transparency

## Core Principle

**Same entity code works across SQL, NoSQL, Vector, JSON stores.** Koan Framework provides complete provider transparency with automatic capability detection and graceful fallbacks.

## Revolutionary Approach

Write code once, run on any data provider:
- **PostgreSQL** - Relational with JSON support
- **MongoDB** - Document database
- **SQLite** - Embedded relational
- **Redis** - Key-value cache
- **JSON** - File-based development
- **Weaviate/Milvus** - Vector databases
- **InMemory** - Testing

No code changes needed to switch providers. Just change configuration.

## Provider Capability Detection

```csharp
// Check what current provider supports
var capabilities = Data<Todo, string>.QueryCaps;

if (capabilities.Capabilities.HasFlag(QueryCapabilities.LinqQueries))
{
    // Provider supports server-side LINQ (Postgres, Mongo, SQL Server)
    var filtered = await Todo.Query(t => t.Priority > 3 && !t.Completed);
}
else
{
    // Provider requires client-side filtering (JSON, InMemory)
    var all = await Todo.All();
    var filtered = all.Where(t => t.Priority > 3 && !t.Completed).ToList();
}

// Check fast removal support
if (Todo.SupportsFastRemove)
{
    // Provider supports TRUNCATE/DROP (Postgres, SQL Server, Mongo)
    await Todo.RemoveAll(RemoveStrategy.Fast);
}
```

## Context Routing

### Partition (Logical Suffix)

Partitions provide logical data isolation within same provider:

```csharp
// Default partition
var todo = new Todo { Title = "Active task" };
await todo.Save(); // Stored as Todo

// Archive partition
using (EntityContext.Partition("archive"))
{
    var archived = new Todo { Title = "Archived task" };
    await archived.Save(); // Stored as Todo#archive
}

// Tenant isolation
using (EntityContext.Partition($"tenant-{tenantId}"))
{
    var tenantTodos = await Todo.All(); // Only this tenant's data
}
```

**Use Cases:**
- Multi-tenant isolation
- Archival storage
- Test data separation
- Environment segmentation

### Source (Named Configuration)

Sources route to different provider configurations:

```csharp
// appsettings.json
{
  "Koan": {
    "Data": {
      "Sources": {
        "Default": {
          "Adapter": "postgres",
          "ConnectionString": "Host=localhost;Database=main"
        },
        "Analytics": {
          "Adapter": "postgres",
          "ConnectionString": "Host=readonly-replica;Database=analytics"
        },
        "Cache": {
          "Adapter": "redis",
          "ConnectionString": "localhost:6379"
        }
      }
    }
  }
}

// Route to analytics read-replica
using (EntityContext.Source("analytics"))
{
    var stats = await Todo.Count; // Reads from replica
}

// Route to cache
using (EntityContext.Source("cache"))
{
    var frequent = await FrequentQuery.Get(id); // From Redis
}
```

**Use Cases:**
- Read replicas
- Analytics databases
- Cache layers
- Regional data centers

### Adapter (Explicit Provider Override)

Adapters explicitly select provider regardless of configuration:

```csharp
// Force MongoDB
using (EntityContext.Adapter("mongodb"))
{
    var todos = await Todo.All(); // Always uses MongoDB
}

// Force JSON for testing
using (EntityContext.Adapter("json"))
{
    await todo.Save(); // Writes to JSON file
}
```

**Use Cases:**
- Provider-specific features
- Migration testing
- Development overrides
- Provider comparison

### CRITICAL RULE: Source XOR Adapter

**NEVER combine Source and Adapter** (ADR DATA-0077):

```csharp
// ❌ WRONG: Conflicting context
using (EntityContext.Source("analytics"))
using (EntityContext.Adapter("mongodb"))
{
    // Which wins? Undefined behavior!
}

// ✅ CORRECT: Use one or the other
using (EntityContext.Source("analytics"))
{
    // Routes via named source configuration
}

// OR

using (EntityContext.Adapter("mongodb"))
{
    // Explicit provider override
}
```

## Context Nesting

Contexts nest and replace previous values:

```csharp
// Outer context
using (EntityContext.Source("analytics"))
{
    var count1 = await Todo.Count; // analytics source

    // Inner context replaces outer
    using (EntityContext.Partition("archive"))
    {
        var count2 = await Todo.Count; // analytics + archive partition
    }

    var count3 = await Todo.Count; // back to analytics (no partition)
}
```

## Provider-Specific Configuration

### Forcing Specific Provider

Use `[DataAdapter]` attribute to pin entity to provider:

```csharp
// Always use MongoDB for this entity
[DataAdapter("mongodb")]
public class FlexibleDocument : Entity<FlexibleDocument>
{
    public Dictionary<string, object> Properties { get; set; } = new();
}

// Always use vector database
[DataAdapter("weaviate")]
public class MediaEmbedding : Entity<MediaEmbedding>
{
    [VectorField]
    public float[] Embedding { get; set; } = Array.Empty<float>();
}
```

## Capability Fallback Patterns

```csharp
public async Task<List<Todo>> SearchWithFallback(string searchTerm)
{
    var caps = Data<Todo, string>.QueryCaps;

    if (caps.Capabilities.HasFlag(QueryCapabilities.FullTextSearch))
    {
        // Provider supports full-text search
        return await Todo.Query($"CONTAINS(Title, '{searchTerm}')");
    }
    else
    {
        // Fallback to client-side filtering
        var all = await Todo.All();
        return all.Where(t => t.Title.Contains(searchTerm,
            StringComparison.OrdinalIgnoreCase)).ToList();
    }
}
```

## Provider Comparison Matrix

| Provider | LINQ Queries | Transactions | Fast Remove | Vector Search | JSON Fields |
|----------|--------------|--------------|-------------|---------------|-------------|
| **PostgreSQL** | ✅ | ✅ | ✅ | ✅ (pgvector) | ✅ |
| **SQL Server** | ✅ | ✅ | ✅ | ❌ | ✅ (limited) |
| **MongoDB** | ✅ | ✅ | ✅ | ❌ | ✅ (native) |
| **SQLite** | ✅ | ✅ | ✅ | ❌ | ✅ (json1) |
| **Redis** | ❌ | ❌ | ✅ | ❌ | ✅ |
| **JSON** | ❌ | ❌ | ❌ | ❌ | ✅ (native) |
| **InMemory** | ❌ | ❌ | ❌ | ❌ | ✅ |
| **Weaviate** | ❌ | ❌ | ❌ | ✅ | ✅ |
| **Milvus** | ❌ | ❌ | ❌ | ✅ | ✅ |

## When This Skill Applies

Invoke this skill when:
- ✅ Working with multiple data providers
- ✅ Switching between providers
- ✅ Implementing multi-tenant isolation
- ✅ Routing to read replicas
- ✅ Writing capability-aware code
- ✅ Debugging provider-specific issues

## Reference Documentation

- **Full Guide:** `docs/guides/entity-capabilities-howto.md` § Context Routing
- **ADR:** DATA-0077 (Source XOR Adapter rule)
- **Sample:** `samples/S10.DevPortal/` (Multi-provider showcase)
- **Sample:** `samples/S14.AdapterBench/` (Provider performance comparison)

## Framework Compliance

Multi-provider patterns are fundamental to Koan Framework:
- ✅ Write provider-agnostic code
- ✅ Use capability detection
- ✅ Implement graceful fallbacks
- ✅ Follow Source XOR Adapter rule
- ❌ Never write provider-specific code without capability checks
- ❌ Never hard-code provider assumptions
