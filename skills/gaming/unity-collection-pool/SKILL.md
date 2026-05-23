---
name: unity-collection-pool
description: Unity Collection Pool expert for GC-free collection management using ListPool, DictionaryPool, HashSetPool, and ObjectPool. Masters memory optimization, pool sizing, and allocation-free patterns. Use PROACTIVELY for collection allocations, GC pressure reduction, temporary list/dictionary usage, or performance-critical code paths.
requires:
  - csharp-plugin:csharp-code-style
---

# Unity Collection Pool - GC-Free Collection Management

## Overview

Unity's `UnityEngine.Pool` namespace (2021.1+) provides built-in collection pooling to eliminate GC allocations from temporary collection usage.

**Foundation Required**: `unity-csharp-fundamentals` (TryGetComponent, FindAnyObjectByType), C# generics, IDisposable pattern

**Core Topics**:
- ListPool, HashSetPool, DictionaryPool usage
- CollectionPool for custom collections
- ObjectPool for arbitrary objects
- Pool lifecycle and disposal patterns
- Memory optimization strategies

## Quick Start

### ListPool Basic Usage

```csharp
using UnityEngine.Pool;
using System.Collections.Generic;

public class PoolExample : MonoBehaviour
{
    void ProcessItems()
    {
        // Get pooled list (zero allocation after warmup)
        List<int> tempList = ListPool<int>.Get();

        try
        {
            // Use the list
            tempList.Add(1);
            tempList.Add(2);
            tempList.Add(3);
            ProcessList(tempList);
        }
        finally
        {
            // Always return to pool
            ListPool<int>.Release(tempList);
        }
    }
}
```

### Using Statement Pattern (Recommended)

```csharp
using UnityEngine.Pool;

void ProcessWithUsing()
{
    // Auto-release via PooledObject<T>
    List<int> tempList;
    using (ListPool<int>.Get(out tempList))
    {
        tempList.Add(1);
        tempList.Add(2);
        DoSomething(tempList);
    } // Automatically returned to pool
}

// HashSet example
void CheckDuplicates(IEnumerable<string> items)
{
    HashSet<string> seen;
    using (HashSetPool<string>.Get(out seen))
    {
        foreach (string item in items)
        {
            if (!seen.Add(item))
                Debug.Log($"Duplicate: {item}");
        }
    }
}

// Dictionary example
void BuildLookup(Item[] items)
{
    Dictionary<int, Item> lookup;
    using (DictionaryPool<int, Item>.Get(out lookup))
    {
        foreach (Item item in items)
            lookup[item.Id] = item;

        ProcessLookup(lookup);
    }
}
```

## Available Pools

| Pool Type | Usage | Get/Release |
|-----------|-------|-------------|
| `ListPool<T>` | Temporary lists | `Get()` / `Release(list)` |
| `HashSetPool<T>` | Duplicate checking, set operations | `Get()` / `Release(set)` |
| `DictionaryPool<K,V>` | Temporary lookups | `Get()` / `Release(dict)` |
| `CollectionPool<C,T>` | Custom ICollection types | `Get()` / `Release(coll)` |
| `ObjectPool<T>` | Arbitrary object pooling | `Get()` / `Release(obj)` |
| `LinkedPool<T>` | Linked list-based pool | `Get()` / `Release(obj)` |
| `GenericPool<T>` | Static shared pool | `Get()` / `Release(obj)` |

## Common Patterns

### Raycast Results Pooling

```csharp
void DetectCollisions(Vector3 origin, Vector3 direction)
{
    List<RaycastHit> hits;
    using (ListPool<RaycastHit>.Get(out hits))
    {
        int count = Physics.RaycastNonAlloc(origin, direction, hitsArray);
        for (int i = 0; i < count; i++)
            hits.Add(hitsArray[i]);

        ProcessHits(hits);
    }
}
```

### Component Query Pooling

```csharp
void FindAllEnemies()
{
    List<Enemy> enemies;
    using (ListPool<Enemy>.Get(out enemies))
    {
        GetComponentsInChildren(enemies); // Overload that takes list
        foreach (Enemy enemy in enemies)
            enemy.Alert();
    }
}
```

### LINQ Alternative (GC-Free)

```csharp
// AVOID: LINQ allocates
List<Item> filtered = items.Where(x => x.IsActive).ToList();

// PREFER: Pooled collection
List<Item> pooledFiltered;
using (ListPool<Item>.Get(out pooledFiltered))
{
    foreach (Item item in items)
    {
        if (item.IsActive)
            pooledFiltered.Add(item);
    }
    Process(pooledFiltered);
}
```

## Performance Guidelines

### When to Use Pools

```yaml
Use Pools:
  - Temporary collections in Update/FixedUpdate
  - Collections created and discarded within single method
  - High-frequency operations (per-frame, per-physics-step)
  - Known short-lived collection usage

Avoid Pools:
  - Long-lived collections (store as fields instead)
  - Collections passed across async boundaries
  - Collections with unclear ownership
  - Very small operations (< 3 items, consider stackalloc)
```

### Pool vs Stackalloc

```csharp
// For very small, fixed-size arrays, prefer stackalloc
Span<int> small = stackalloc int[4];

// For variable size or larger collections, use pool
List<int> larger;
using (ListPool<int>.Get(out larger))
{
    // Variable size operations
}
```

## Key Principles

1. **Always Release**: Use `using` pattern or try/finally to guarantee release
2. **Clear on Get**: Pools automatically clear collections on Get
3. **Don't Store References**: Never cache pooled collection references
4. **Match Types**: Release to same pool type that provided the collection
5. **Prefer `using` Pattern**: Auto-disposal prevents leaks

## Anti-Patterns

```csharp
// WRONG: Storing pooled reference
private List<int> mCachedList;
void Bad()
{
    mCachedList = ListPool<int>.Get(); // Memory leak!
}

// WRONG: Missing release
void AlsoBAD()
{
    List<int> list = ListPool<int>.Get();
    Process(list);
    // Forgot to release - leak!
}

// WRONG: Releasing wrong pool
void VeryBad()
{
    List<int> list = ListPool<int>.Get();
    ListPool<float>.Release(list); // Type mismatch!
}

// WRONG: Using after release
void TerriblyBad()
{
    List<int> list;
    using (ListPool<int>.Get(out list)) { }
    list.Add(1); // Using disposed collection!
}
```

## Reference Documentation

### [Pool Fundamentals](references/pool-fundamentals.md)
Core pool concepts:
- Pool lifecycle and memory management
- Built-in pool types detailed API
- Collection clearing behavior
- Capacity management
- Thread safety considerations

### [Advanced Patterns](references/advanced-patterns.md)
Advanced usage patterns:
- Custom ObjectPool implementation
- Pool configuration and sizing
- Nested pool usage
- Integration with ECS/DOTS
- Profiling pool efficiency

## Integration with Other Skills

- **unity-performance**: Collection pooling is key optimization technique
- **unity-async**: Careful pool usage across async boundaries
- **unity-unitask**: Combine with UniTask for async pooling patterns
