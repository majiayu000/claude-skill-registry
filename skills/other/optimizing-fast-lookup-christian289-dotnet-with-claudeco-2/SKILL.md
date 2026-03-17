---
name: optimizing-fast-lookup
description: "Implements fast O(1) lookup patterns using HashSet, FrozenSet, and optimized Dictionary in .NET. Use when building high-performance search or membership testing operations."
---

# .NET Fast Lookup

A guide for fast lookup APIs leveraging O(1) time complexity.

**Quick Reference:** See [QUICKREF.md](QUICKREF.md) for essential patterns at a glance.

## 1. Core APIs

| API | Time Complexity | Features |
|-----|-----------------|----------|
| `HashSet<T>` | O(1) | Mutable, no duplicates |
| `FrozenSet<T>` | O(1) | Immutable, .NET 8+ |
| `Dictionary<K,V>` | O(1) | Mutable, Key-Value |
| `FrozenDictionary<K,V>` | O(1) | Immutable, .NET 8+ |

---

## 2. HashSet<T>

```csharp
// O(1) time complexity for existence check
var allowedIds = new HashSet<int> { 1, 2, 3, 4, 5 };

if (allowedIds.Contains(userId))
{
    // Allowed user
}

// Set operations
setA.IntersectWith(setB); // Intersection
setA.UnionWith(setB);     // Union
setA.ExceptWith(setB);    // Difference
```

---

## 3. FrozenSet<T> (.NET 8+)

```csharp
using System.Collections.Frozen;

// Immutable fast lookup (read-only scenarios)
var allowedExtensions = new[] { ".jpg", ".png", ".gif" }
    .ToFrozenSet(StringComparer.OrdinalIgnoreCase);

if (allowedExtensions.Contains(fileExtension))
{
    // Allowed extension
}
```

---

## 4. Dictionary<K,V> Optimization

```csharp
// ❌ Two lookups
if (dict.ContainsKey(key))
{
    var value = dict[key];
}

// ✅ Single lookup
if (dict.TryGetValue(key, out var value))
{
    // Use value
}

// Lookup with default value
var value = dict.GetValueOrDefault(key, defaultValue);
```

---

## 5. Comparer Optimization

```csharp
// Case-insensitive string comparison
var set = new HashSet<string>(StringComparer.OrdinalIgnoreCase);
set.Add("Hello");
set.Contains("HELLO"); // true
```

---

## 6. When to Use

| Scenario | Recommended Collection |
|----------|------------------------|
| Frequently modified set | `HashSet<T>` |
| Read-only configuration data | `FrozenSet<T>` |
| Frequent existence checks | `HashSet<T>` / `FrozenSet<T>` |
| Key-Value cache | `Dictionary<K,V>` |
| Static mapping table | `FrozenDictionary<K,V>` |

---

## 7. References

- [HashSet<T>](https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.hashset-1)
- [FrozenSet<T>](https://learn.microsoft.com/en-us/dotnet/api/system.collections.frozen.frozenset-1)
