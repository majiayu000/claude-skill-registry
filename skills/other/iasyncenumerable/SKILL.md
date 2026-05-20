---
name: iasyncenumerable
description: >
  USE FOR: Streaming data asynchronously using IAsyncEnumerable<T> with yield return, including
  database result streaming, API pagination, file processing, and gRPC server streaming.
  DO NOT USE FOR: Event-based reactive streams (use IObservable<T>/Rx), producer/consumer queues
  (use System.Threading.Channels), or fire-and-forget background work.
license: MIT
metadata:
  displayName: IAsyncEnumerable
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "IAsyncEnumerable API Reference"
    url: "https://learn.microsoft.com/en-us/dotnet/api/system.collections.generic.iasyncenumerable-1"
  - title: "Async Streams Tutorial"
    url: "https://learn.microsoft.com/en-us/dotnet/csharp/asynchronous-programming/generate-consume-asynchronous-stream"
---

# IAsyncEnumerable<T>

## Overview

`IAsyncEnumerable<T>` is the async counterpart of `IEnumerable<T>`, enabling pull-based streaming of data where each element is produced asynchronously. It uses `yield return` inside `async` iterator methods and is consumed with `await foreach`. Unlike `Task<List<T>>` which waits for all items before returning, `IAsyncEnumerable<T>` yields items one at a time as they become available, reducing memory pressure and time-to-first-result for large datasets.

`IAsyncEnumerable<T>` is supported natively in ASP.NET Core (controller actions, minimal APIs), Entity Framework Core (streaming query results), gRPC (server streaming), and System.Text.Json (streaming serialization). It was introduced in C# 8 / .NET Core 3.0 and requires no additional packages.

## Basic Producer and Consumer

```csharp
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

namespace MyApp.Services;

public class SensorDataService
{
    // Producer: yields sensor readings one at a time
    public async IAsyncEnumerable<SensorReading> StreamReadingsAsync(
        string sensorId,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        while (!cancellationToken.IsCancellationRequested)
        {
            var reading = await ReadSensorAsync(sensorId, cancellationToken);
            yield return reading;
            await Task.Delay(TimeSpan.FromSeconds(1), cancellationToken);
        }
    }

    private async Task<SensorReading> ReadSensorAsync(
        string sensorId, CancellationToken ct)
    {
        // Simulate async I/O
        await Task.Delay(10, ct);
        return new SensorReading(
            SensorId: sensorId,
            Value: Random.Shared.NextDouble() * 100,
            Timestamp: DateTime.UtcNow);
    }
}

public record SensorReading(string SensorId, double Value, DateTime Timestamp);
```

```csharp
using System;
using System.Threading;
using System.Threading.Tasks;
using MyApp.Services;

// Consumer: processes items as they arrive
public class SensorMonitor
{
    private readonly SensorDataService _service;

    public SensorMonitor(SensorDataService service)
    {
        _service = service;
    }

    public async Task MonitorAsync(string sensorId, CancellationToken ct)
    {
        await foreach (var reading in _service.StreamReadingsAsync(sensorId, ct))
        {
            if (reading.Value > 90.0)
            {
                Console.WriteLine(
                    $"ALERT: Sensor {reading.SensorId} reading {reading.Value:F1} " +
                    $"at {reading.Timestamp:HH:mm:ss}");
            }
        }
    }
}
```

## Entity Framework Core Streaming

EF Core's `AsAsyncEnumerable()` streams query results without loading all rows into memory.

```csharp
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using Microsoft.EntityFrameworkCore;

namespace MyApp.Data;

public class OrderRepository
{
    private readonly AppDbContext _context;

    public OrderRepository(AppDbContext context)
    {
        _context = context;
    }

    // Streams orders from the database without loading all into memory
    public async IAsyncEnumerable<Order> GetLargeOrdersAsync(
        decimal minTotal,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        await foreach (var order in _context.Orders
            .Where(o => o.Total >= minTotal)
            .OrderByDescending(o => o.CreatedAt)
            .AsAsyncEnumerable()
            .WithCancellation(cancellationToken))
        {
            yield return order;
        }
    }

    // Batch processing with streaming
    public async IAsyncEnumerable<Order[]> GetOrderBatchesAsync(
        int batchSize,
        [EnumeratorCancellation] CancellationToken cancellationToken = default)
    {
        var batch = new List<Order>(batchSize);

        await foreach (var order in _context.Orders
            .AsAsyncEnumerable()
            .WithCancellation(cancellationToken))
        {
            batch.Add(order);
            if (batch.Count >= batchSize)
            {
                yield return batch.ToArray();
                batch.Clear();
            }
        }

        if (batch.Count > 0)
        {
            yield return batch.ToArray();
        }
    }
}

public class Order
{
    public int Id { get; set; }
    public decimal Total { get; set; }
    public DateTime CreatedAt { get; set; }
}

public class AppDbContext : DbContext
{
    public DbSet<Order> Orders => Set<Order>();

    public AppDbContext(DbContextOptions<AppDbContext> options) : base(options) { }
}
```

## ASP.NET Core Integration

ASP.NET Core natively supports `IAsyncEnumerable<T>` in controller actions and minimal APIs, streaming JSON array elements as they are produced.

```csharp
using System.Collections.Generic;
using System.Runtime.CompilerServices;
using System.Threading;
using Microsoft.AspNetCore.Mvc;
using MyApp.Data;

namespace MyApp.Controllers;

[ApiController]
[Route("api/[controller]")]
public class OrdersController : ControllerBase
{
    private readonly OrderRepository _repository;

    public OrdersController(OrderRepository repository)
    {
        _repository = repository;
    }

    // ASP.NET Core streams the JSON array elements one at a time
    [HttpGet("large")]
    public IAsyncEnumerable<Order> GetLargeOrders(
        [FromQuery] decimal minTotal = 1000,
        CancellationToken cancellationToken = default)
    {
        return _repository.GetLargeOrdersAsync(minTotal, cancellationToken);
    }
}
```

```csharp
// Minimal API equivalent
app.MapGet("/api/orders/stream", (
    OrderRepository repo,
    CancellationToken ct) =>
{
    return repo.GetLargeOrdersAsync(1000, ct);
});
```

## LINQ Operators for IAsyncEnumerable

`System.Linq.Async` (NuGet package) provides LINQ operators for `IAsyncEnumerable<T>`.

```csharp
using System.Collections.Generic;
using System.Linq;
using System.Runtime.CompilerServices;
using System.Threading;
using System.Threading.Tasks;

namespace MyApp.Services;

public class AnalyticsService
{
    private readonly SensorDataService _sensors;

    public AnalyticsService(SensorDataService sensors)
    {
        _sensors = sensors;
    }

    // Filter, transform, and take from an async stream
    public async IAsyncEnumerable<Alert> GetAlertsAsync(
        string sensorId,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        await foreach (var alert in _sensors.StreamReadingsAsync(sensorId, ct)
            .Where(r => r.Value > 85.0)
            .Select(r => new Alert(
                r.SensorId,
                $"High reading: {r.Value:F1}",
                r.Timestamp))
            .Take(50)
            .WithCancellation(ct))
        {
            yield return alert;
        }
    }

    // Aggregate over a stream
    public async Task<double> GetAverageAsync(
        string sensorId, int sampleCount, CancellationToken ct)
    {
        return await _sensors.StreamReadingsAsync(sensorId, ct)
            .Take(sampleCount)
            .AverageAsync(r => r.Value, ct);
    }

    // Buffer into chunks
    public async IAsyncEnumerable<SensorReading[]> GetBufferedAsync(
        string sensorId,
        int bufferSize,
        [EnumeratorCancellation] CancellationToken ct = default)
    {
        await foreach (var chunk in _sensors.StreamReadingsAsync(sensorId, ct)
            .Buffer(bufferSize)
            .WithCancellation(ct))
        {
            yield return chunk.ToArray();
        }
    }
}

public record Alert(string SensorId, string Message, DateTime Timestamp);
```

## IAsyncEnumerable vs. Alternatives

| Feature                | IAsyncEnumerable<T>        | Task<List<T>>           | IObservable<T>            | Channel<T>               |
|------------------------|----------------------------|-------------------------|---------------------------|--------------------------|
| Pull/Push model        | Pull (consumer controls)   | Pull (all at once)      | Push (producer controls)  | Push with backpressure   |
| Memory usage           | O(1) per item              | O(n) all items          | O(1) per item             | O(capacity)              |
| Cancellation           | CancellationToken          | CancellationToken       | Dispose subscription      | CancellationToken        |
| Backpressure           | Natural (consumer speed)   | N/A                     | Must implement manually   | Bounded channel          |
| Multiple consumers     | Not supported natively     | Share the list          | Multiple subscriptions    | Multiple readers         |
| LINQ support           | System.Linq.Async          | System.Linq             | System.Reactive.Linq      | None built-in            |
| Best for               | Streaming query results    | Small result sets       | Event streams, UI events  | Producer/consumer queues |

## Best Practices

1. **Always accept `[EnumeratorCancellation] CancellationToken` as the last parameter of async iterator methods** so that consumers can cancel enumeration; the attribute wires the token from `WithCancellation()` to the parameter automatically.

2. **Use `await foreach` with `ConfigureAwait(false)` in library code** by writing `await foreach (var item in stream.ConfigureAwait(false))` to avoid capturing the synchronization context on each iteration.

3. **Return `IAsyncEnumerable<T>` from ASP.NET Core endpoints for large result sets** instead of `Task<List<T>>` so that ASP.NET streams JSON array elements incrementally, reducing memory allocation and time-to-first-byte.

4. **Use `AsAsyncEnumerable()` in EF Core queries instead of `ToListAsync()` for large datasets** to stream rows from the database one at a time; note that the `DbContext` must remain alive for the duration of the enumeration.

5. **Install the `System.Linq.Async` NuGet package for LINQ operators** (`Where`, `Select`, `Take`, `Skip`, `AverageAsync`, `Buffer`) because the BCL does not include LINQ extension methods for `IAsyncEnumerable<T>`.

6. **Do not enumerate the same `IAsyncEnumerable<T>` instance multiple times** because each enumeration restarts the producer; if multiple consumers need the data, materialize it into a list first or use a different abstraction like channels.

7. **Use `yield return` with `try/finally` for resource cleanup** instead of manual iterator state machines, because the compiler generates the correct disposal logic when `await using` or `await foreach` exits (including on cancellation or exception).

8. **Prefer `IAsyncEnumerable<T>` over `IObservable<T>` when the consumer controls the pace** (pull-based) -- database queries, file reading, paginated APIs -- and prefer `IObservable<T>` when the producer controls the pace (push-based) -- UI events, message bus subscriptions.

9. **Batch items using `Buffer(count)` from System.Linq.Async when processing items individually is too slow** -- for example, inserting 100 rows at a time into a database instead of one at a time, reducing round-trip overhead.

10. **Test async iterators by collecting results into a list with `await stream.ToListAsync()`** or by asserting on individual items with `await foreach` and a counter, ensuring the stream terminates correctly and cancellation is honored.
