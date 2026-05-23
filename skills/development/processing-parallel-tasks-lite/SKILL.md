---
name: processing-parallel-tasks-lite
description: "Provides essential parallel processing patterns with Parallel.ForEach and PLINQ. Use when quickly referencing core parallel processing techniques without detailed explanations."
---

# Parallel Processing Essentials

## 1. Parallel.ForEach

```csharp
var options = new ParallelOptions
{
    MaxDegreeOfParallelism = Environment.ProcessorCount
};

Parallel.ForEach(items, options, item =>
{
    ProcessItem(item);
});
```

## 2. PLINQ

```csharp
var results = data
    .AsParallel()
    .Where(d => d.IsValid)
    .Select(d => Transform(d))
    .ToList();
```

## 3. Thread-Safe Collections

```csharp
// Collecting results during parallel processing
var results = new ConcurrentBag<Result>();

Parallel.ForEach(data, item =>
{
    results.Add(Process(item));
});
```

## 4. Important Notes

- CPU-bound: Use Parallel
- I/O-bound: Use async-await

```csharp
// ❌ Using Parallel for I/O
Parallel.ForEach(urls, url => httpClient.GetAsync(url).Result);

// ✅ Using async-await for I/O
await Task.WhenAll(urls.Select(url => httpClient.GetAsync(url)));
```

> For details: See `/dotnet-parallel` skill
