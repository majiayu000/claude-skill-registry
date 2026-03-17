---
name: handling-async-operations
description: "Implements asynchronous programming patterns using Task, ValueTask, and ConfigureAwait in .NET. Use when building non-blocking I/O operations or improving application responsiveness."
---

# .NET Asynchronous Programming

A guide for APIs and patterns for efficient asynchronous programming.

**Quick Reference:** See [QUICKREF.md](QUICKREF.md) for essential patterns at a glance.

## 1. Core APIs

| API | Purpose |
|-----|---------|
| `Task` | Async operation (no return value) |
| `Task<T>` | Async operation (with return value) |
| `ValueTask<T>` | Optimization for high-frequency calls |
| `IAsyncEnumerable<T>` | Async streams |

---

## 2. Task vs ValueTask

### 2.1 When to Use Task<T>

- Most async operations
- When actual async work always occurs

### 2.2 When to Use ValueTask<T>

- When synchronous completion is frequent (cache hits)
- High-frequency call methods

```csharp
// Use ValueTask when cache hits are frequent
public ValueTask<Data> GetDataAsync(string key)
{
    if (_cache.TryGetValue(key, out var cached))
    {
        // Synchronous return (no Heap allocation)
        return new ValueTask<Data>(cached);
    }

    // When async work is needed
    return new ValueTask<Data>(LoadFromDbAsync(key));
}
```

### 2.3 ValueTask Cautions

```csharp
// ❌ Bad example: Awaiting ValueTask multiple times
var task = GetDataAsync("key");
var result1 = await task;
var result2 = await task; // May cause error!

// ✅ Good example: Await only once
var result = await GetDataAsync("key");
```

---

## 3. ConfigureAwait

```csharp
// Use ConfigureAwait(false) in libraries
public async Task<string> FetchDataAsync()
{
    var response = await _httpClient.GetAsync(url)
        .ConfigureAwait(false);
    return await response.Content.ReadAsStringAsync()
        .ConfigureAwait(false);
}
```

---

## 4. Async Streams (IAsyncEnumerable)

```csharp
public async IAsyncEnumerable<Data> GetDataStreamAsync(
    [EnumeratorCancellation] CancellationToken ct = default)
{
    await foreach (var item in _source.ReadAllAsync(ct))
    {
        yield return await ProcessAsync(item);
    }
}

// Consuming
await foreach (var data in GetDataStreamAsync(ct))
{
    Console.WriteLine(data);
}
```

---

## 5. Cancellation Token

```csharp
public async Task<Data> LoadDataAsync(CancellationToken ct = default)
{
    ct.ThrowIfCancellationRequested();
    return await _httpClient.GetFromJsonAsync<Data>(url, ct);
}

// Setting timeout
using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(30));
await LongRunningOperationAsync(cts.Token);
```

---

## 6. Concurrency Control

```csharp
private readonly SemaphoreSlim _semaphore = new(maxCount: 10);

public async Task ProcessWithThrottlingAsync(Data data)
{
    await _semaphore.WaitAsync();
    try
    {
        await ProcessAsync(data);
    }
    finally
    {
        _semaphore.Release();
    }
}
```

---

## 7. Anti-patterns

```csharp
// ❌ No async void (cannot handle exceptions)
public async void BadMethod() { }

// ✅ async Task
public async Task GoodMethod() { }

// ❌ No .Result, .Wait() (deadlock risk)
var result = GetDataAsync().Result;

// ✅ Use await
var result = await GetDataAsync();

// ❌ Unnecessary async/await
public async Task<Data> GetDataAsync()
{
    return await _repository.GetAsync();
}

// ✅ Direct return
public Task<Data> GetDataAsync()
{
    return _repository.GetAsync();
}
```

---

## 8. References

- [Task-based Asynchronous Pattern](https://learn.microsoft.com/en-us/dotnet/standard/asynchronous-programming-patterns/task-based-asynchronous-pattern-tap)
- [ValueTask](https://learn.microsoft.com/en-us/dotnet/api/system.threading.tasks.valuetask-1)

