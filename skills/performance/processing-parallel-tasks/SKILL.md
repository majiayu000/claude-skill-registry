---
name: processing-parallel-tasks
description: "Implements parallel processing using Parallel, PLINQ, and ConcurrentCollections in .NET. Use when processing CPU-bound tasks in parallel or improving multi-core utilization."
---

# .NET Parallel Processing

A guide for APIs and patterns for parallel processing of CPU-bound tasks.

**Quick Reference:** See [QUICKREF.md](QUICKREF.md) for essential patterns at a glance.

## 1. Core APIs

| API | Purpose |
|-----|---------|
| `Parallel.For`, `Parallel.ForEach` | CPU-bound parallel processing |
| `PLINQ (.AsParallel())` | LINQ query parallelization |
| `Partitioner<T>` | Large data partitioning |
| `ConcurrentDictionary<K,V>` | Thread-safe dictionary |

---

## 2. Parallel Class

### 2.1 Parallel.ForEach

```csharp
public sealed class ImageProcessor
{
    public void ProcessImages(IEnumerable<string> imagePaths)
    {
        var options = new ParallelOptions
        {
            MaxDegreeOfParallelism = Environment.ProcessorCount
        };

        Parallel.ForEach(imagePaths, options, path =>
        {
            ProcessImage(path);
        });
    }
}
```

### 2.2 Early Termination

```csharp
Parallel.For(0, data.Length, (i, state) =>
{
    if (data[i] == target)
    {
        state.Break();
    }
});
```

---

## 3. PLINQ

```csharp
var results = data
    .AsParallel()
    .WithDegreeOfParallelism(Environment.ProcessorCount)
    .Where(d => d.IsValid)
    .Select(d => Transform(d))
    .ToList();

// When order preservation is needed
var results = data
    .AsParallel()
    .AsOrdered()
    .Select(d => Process(d))
    .ToList();
```

---

## 4. Thread-Safe Collections

| Collection | Purpose |
|------------|---------|
| `ConcurrentDictionary<K,V>` | Thread-safe dictionary |
| `ConcurrentQueue<T>` | Thread-safe FIFO queue |
| `ConcurrentBag<T>` | Thread-safe unordered collection |

```csharp
// Collecting results during parallel processing
var results = new ConcurrentBag<Result>();

Parallel.ForEach(data, item =>
{
    var result = Process(item);
    results.Add(result);
});
```

---

## 5. ThreadLocal<T>

Prevents contention with thread-local variables

```csharp
private readonly ThreadLocal<StringBuilder> _localBuilder =
    new(() => new StringBuilder());

public void ProcessInParallel()
{
    Parallel.For(0, 1000, i =>
    {
        var sb = _localBuilder.Value!;
        sb.Clear();
        sb.Append(i);
    });
}
```

---

## 6. Important Notes

### Parallel Processing vs Async

- **CPU-bound**: Use Parallel
- **I/O-bound**: Use async-await

```csharp
// ❌ Using Parallel for I/O operations
Parallel.ForEach(urls, url => httpClient.GetAsync(url).Result);

// ✅ Using async-await for I/O operations
await Task.WhenAll(urls.Select(url => httpClient.GetAsync(url)));
```

### Shared State Synchronization

```csharp
// ❌ Parallel writes to regular collection
var list = new List<int>();
Parallel.For(0, 1000, i => list.Add(i)); // Race condition!

// ✅ Using thread-safe collection
var bag = new ConcurrentBag<int>();
Parallel.For(0, 1000, i => bag.Add(i));
```

---

## 7. References

- [Parallel Class](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.parallel)
- [PLINQ](https://learn.microsoft.com/en-us/dotnet/standard/parallel-programming/introduction-to-plinq)
