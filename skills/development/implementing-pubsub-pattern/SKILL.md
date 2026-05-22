---
name: implementing-pubsub-pattern
description: "Implements Pub-Sub patterns using System.Reactive and Channels for event-based communication in .NET. Use when building reactive applications or decoupled event-driven architectures."
---

# .NET Pub-Sub Pattern

A guide for Pub-Sub patterns for event-based asynchronous communication.

**Quick Reference:** See [QUICKREF.md](QUICKREF.md) for essential patterns at a glance.

## 1. Core APIs

| API | Purpose | NuGet |
|-----|---------|-------|
| `System.Reactive` (Rx.NET) | Reactive event streams | System.Reactive |
| `System.Threading.Channels` | Async Producer-Consumer | BCL |
| `IObservable<T>` | Observable sequence | BCL |

---

## 2. System.Threading.Channels

### 2.1 Basic Usage

```csharp
using System.Threading.Channels;

public sealed class MessageProcessor
{
    private readonly Channel<Message> _channel =
        Channel.CreateUnbounded<Message>();

    // Producer - Send message
    public async Task SendAsync(Message message)
    {
        await _channel.Writer.WriteAsync(message);
    }

    // Consumer - Process message
    public async Task ProcessAsync(CancellationToken ct)
    {
        await foreach (var message in _channel.Reader.ReadAllAsync(ct))
        {
            await HandleMessage(message);
        }
    }

    // Channel completion signal
    public void Complete() => _channel.Writer.Complete();
}
```

### 2.2 Bounded Channel (Backpressure Control)

```csharp
// Backpressure control with buffer size limit
var options = new BoundedChannelOptions(capacity: 100)
{
    FullMode = BoundedChannelFullMode.Wait, // Wait when full
    SingleReader = true,
    SingleWriter = false
};

var channel = Channel.CreateBounded<Message>(options);

// Writer waits until space is available
await channel.Writer.WriteAsync(message);
```

### 2.3 Multiple Consumer Pattern

```csharp
public sealed class WorkerPool
{
    private readonly Channel<WorkItem> _channel;
    private readonly int _workerCount;

    public WorkerPool(int workerCount = 4)
    {
        _workerCount = workerCount;
        _channel = Channel.CreateUnbounded<WorkItem>();
    }

    public async Task StartAsync(CancellationToken ct)
    {
        var workers = Enumerable.Range(0, _workerCount)
            .Select(_ => ProcessAsync(ct));

        await Task.WhenAll(workers);
    }

    private async Task ProcessAsync(CancellationToken ct)
    {
        await foreach (var item in _channel.Reader.ReadAllAsync(ct))
        {
            await ProcessItem(item);
        }
    }

    public ValueTask EnqueueAsync(WorkItem item) =>
        _channel.Writer.WriteAsync(item);
}
```

---

## 3. System.Reactive (Rx.NET)

### 3.1 EventAggregator Pattern

```csharp
using System.Reactive.Linq;
using System.Reactive.Subjects;

public sealed class EventAggregator : IDisposable
{
    private readonly Subject<object> _subject = new();

    // Subscribe to specific event type
    public IObservable<T> GetEvent<T>() =>
        _subject.OfType<T>().AsObservable();

    // Publish event
    public void Publish<T>(T @event) =>
        _subject.OnNext(@event!);

    public void Dispose() => _subject.Dispose();
}
```

### 3.2 Usage Example

```csharp
// Event definitions
public record UserLoggedIn(string UserId);
public record OrderPlaced(int OrderId);

// Subscription
var aggregator = new EventAggregator();

aggregator.GetEvent<UserLoggedIn>()
    .Subscribe(e => Console.WriteLine($"User logged in: {e.UserId}"));

aggregator.GetEvent<OrderPlaced>()
    .Where(e => e.OrderId > 100)
    .Subscribe(e => Console.WriteLine($"Large order: {e.OrderId}"));

// Publish
aggregator.Publish(new UserLoggedIn("user123"));
aggregator.Publish(new OrderPlaced(150));
```

### 3.3 Rx Operators

```csharp
// Debounce - Process only the last event in a sequence
searchInput
    .Throttle(TimeSpan.FromMilliseconds(300))
    .DistinctUntilChanged()
    .Subscribe(query => Search(query));

// Buffer - Collect events for a period and process as batch
events
    .Buffer(TimeSpan.FromSeconds(5))
    .Subscribe(batch => ProcessBatch(batch));

// Retry - Retry on failure
observable
    .Retry(3)
    .Subscribe(
        onNext: data => Process(data),
        onError: ex => LogError(ex)
    );
```

---

## 4. Comparison: Channels vs Rx

| Feature | Channels | Rx.NET |
|---------|----------|--------|
| Purpose | Producer-Consumer | Event streams |
| Backpressure | Built-in (Bounded) | Separate implementation |
| Operators | Basic | Rich |
| Learning curve | Low | High |
| Dependency | BCL | NuGet |

---

## 5. DI Integration

```csharp
// Program.cs
services.AddSingleton(Channel.CreateUnbounded<Message>());
services.AddSingleton(sp => sp.GetRequiredService<Channel<Message>>().Reader);
services.AddSingleton(sp => sp.GetRequiredService<Channel<Message>>().Writer);

// Producer
public sealed class Producer(ChannelWriter<Message> writer)
{
    public ValueTask SendAsync(Message msg) => writer.WriteAsync(msg);
}

// Consumer
public sealed class Consumer(ChannelReader<Message> reader)
{
    public async Task ProcessAsync(CancellationToken ct)
    {
        await foreach (var msg in reader.ReadAllAsync(ct))
        {
            await Handle(msg);
        }
    }
}
```

---

## 6. Required NuGet Package

```xml
<ItemGroup>
  <PackageReference Include="System.Reactive" Version="6.0.*" />
</ItemGroup>
```

---

## 7. Important Notes

### Memory Leaks

```csharp
// Subscription disposal is required
var subscription = observable.Subscribe(handler);

// After use
subscription.Dispose();
```

### Thread Safety

- Channels are thread-safe by default
- Subject is not thread-safe (use Synchronize() if needed)

### Backpressure Handling

```csharp
// Prevent memory explosion with Bounded Channel
var channel = Channel.CreateBounded<Message>(new BoundedChannelOptions(1000)
{
    FullMode = BoundedChannelFullMode.DropOldest // Drop old messages
});
```

---

## 8. References

- [Channels](https://learn.microsoft.com/en-us/dotnet/core/extensions/channels)
- [System.Reactive](https://github.com/dotnet/reactive)

