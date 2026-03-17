---
name: reactive-extensions
description: >
  USE FOR: Composing event streams, UI events, timers, and asynchronous data sources using
  IObservable<T> with LINQ operators for filtering, throttling, combining, and error handling.
  DO NOT USE FOR: Simple async/await workflows, pull-based data streaming (use IAsyncEnumerable),
  or producer/consumer queues (use System.Threading.Channels).
license: MIT
metadata:
  displayName: Reactive Extensions (Rx.NET)
  author: "Tyler-R-Kendrick"
  version: "1.0.0"
compatibility:
  - claude
  - copilot
  - cursor
references:
  - title: "Rx.NET GitHub Repository"
    url: "https://github.com/dotnet/reactive"
  - title: "System.Reactive NuGet Package"
    url: "https://www.nuget.org/packages/System.Reactive"
---

# Reactive Extensions (Rx.NET)

## Overview

Reactive Extensions (Rx) is a library for composing asynchronous and event-based programs using observable sequences (`IObservable<T>`) and LINQ-style query operators. Rx turns events, callbacks, timers, and async operations into first-class data streams that can be filtered, combined, throttled, buffered, and error-handled declaratively. The programming model is push-based: producers push values to subscribers through the `IObserver<T>` interface.

Rx.NET provides operators for creating observables (`Observable.Create`, `Observable.Timer`, `Observable.FromEventPattern`), transforming them (`Select`, `SelectMany`, `Buffer`, `Window`), filtering them (`Where`, `Throttle`, `DistinctUntilChanged`, `Take`), combining them (`Merge`, `CombineLatest`, `Zip`, `Switch`), and handling errors (`Retry`, `Catch`, `OnErrorResumeNext`).

## Installation

```bash
dotnet add package System.Reactive
```

## Creating Observables

```csharp
using System;
using System.Reactive.Linq;
using System.Threading.Tasks;

namespace MyApp.Streams;

public static class ObservableFactory
{
    // From a timer
    public static IObservable<long> CreateTimer(TimeSpan interval) =>
        Observable.Interval(interval);

    // From an async factory (cold observable - new subscription = new execution)
    public static IObservable<StockQuote> CreateStockStream(string symbol) =>
        Observable.Create<StockQuote>(async (observer, ct) =>
        {
            while (!ct.IsCancellationRequested)
            {
                try
                {
                    var quote = await FetchQuoteAsync(symbol, ct);
                    observer.OnNext(quote);
                    await Task.Delay(TimeSpan.FromSeconds(1), ct);
                }
                catch (OperationCanceledException)
                {
                    break;
                }
                catch (Exception ex)
                {
                    observer.OnError(ex);
                    return;
                }
            }
            observer.OnCompleted();
        });

    // From an event pattern (e.g., FileSystemWatcher)
    public static IObservable<FileSystemEventArgs> WatchDirectory(string path)
    {
        var watcher = new FileSystemWatcher(path) { EnableRaisingEvents = true };
        return Observable.FromEventPattern<FileSystemEventHandler, FileSystemEventArgs>(
                h => watcher.Changed += h,
                h => watcher.Changed -= h)
            .Select(e => e.EventArgs)
            .Finally(() => watcher.Dispose());
    }

    private static async Task<StockQuote> FetchQuoteAsync(
        string symbol, System.Threading.CancellationToken ct)
    {
        await Task.Delay(10, ct);
        return new StockQuote(symbol, 150.0m + (decimal)(Random.Shared.NextDouble() * 10), DateTime.UtcNow);
    }
}

public record StockQuote(string Symbol, decimal Price, DateTime Timestamp);
```

## Filtering and Transformation

```csharp
using System;
using System.Reactive.Linq;

namespace MyApp.Streams;

public class TradeMonitor : IDisposable
{
    private readonly IDisposable _subscription;

    public TradeMonitor()
    {
        var stockStream = ObservableFactory.CreateStockStream("AAPL");

        _subscription = stockStream
            // Only significant price changes
            .DistinctUntilChanged(q => Math.Round(q.Price, 0))
            // Ignore rapid fluctuations
            .Throttle(TimeSpan.FromMilliseconds(500))
            // Transform to alert
            .Where(q => q.Price > 155.0m)
            .Select(q => new TradeAlert(
                q.Symbol,
                $"Price above threshold: {q.Price:C}",
                q.Timestamp))
            // Take first 10 alerts then complete
            .Take(10)
            .Subscribe(
                onNext: alert => Console.WriteLine(
                    $"[{alert.Timestamp:HH:mm:ss}] {alert.Symbol}: {alert.Message}"),
                onError: ex => Console.WriteLine($"Error: {ex.Message}"),
                onCompleted: () => Console.WriteLine("Monitoring complete"));
    }

    public void Dispose() => _subscription.Dispose();
}

public record TradeAlert(string Symbol, string Message, DateTime Timestamp);
```

## Combining Streams

```csharp
using System;
using System.Reactive.Linq;

namespace MyApp.Streams;

public class DashboardService
{
    // CombineLatest: emit when ANY source emits, using latest from each
    public IObservable<DashboardData> CreateDashboardStream()
    {
        var prices = ObservableFactory.CreateStockStream("AAPL");
        var volume = Observable.Interval(TimeSpan.FromSeconds(5))
            .Select(_ => Random.Shared.Next(1000, 50000));
        var sentiment = Observable.Interval(TimeSpan.FromSeconds(10))
            .Select(_ => Random.Shared.NextDouble() * 2 - 1); // -1 to 1

        return Observable.CombineLatest(
            prices,
            volume,
            sentiment,
            (price, vol, sent) => new DashboardData(
                price.Price,
                vol,
                sent,
                DateTime.UtcNow));
    }

    // Merge: interleave multiple streams into one
    public IObservable<StockQuote> CreateMultiStockStream(params string[] symbols)
    {
        var streams = symbols.Select(ObservableFactory.CreateStockStream);
        return streams.Merge();
    }

    // Switch: cancel previous inner observable when outer emits
    public IObservable<StockQuote> CreateSearchableStream(
        IObservable<string> searchTerms)
    {
        return searchTerms
            .Throttle(TimeSpan.FromMilliseconds(300))
            .DistinctUntilChanged()
            .Select(term => ObservableFactory.CreateStockStream(term))
            .Switch(); // Unsubscribe from previous, subscribe to new
    }
}

public record DashboardData(
    decimal Price, int Volume, double Sentiment, DateTime Timestamp);
```

## Buffering and Windowing

```csharp
using System;
using System.Collections.Generic;
using System.Reactive.Linq;

namespace MyApp.Streams;

public class BatchProcessor
{
    // Buffer: collect items into batches
    public IObservable<IList<StockQuote>> BatchByCount(
        IObservable<StockQuote> source, int batchSize)
    {
        return source.Buffer(batchSize);
    }

    // Buffer by time: emit batch every N seconds
    public IObservable<IList<StockQuote>> BatchByTime(
        IObservable<StockQuote> source, TimeSpan interval)
    {
        return source.Buffer(interval);
    }

    // Buffer by count OR time (whichever comes first)
    public IObservable<IList<StockQuote>> BatchByCountOrTime(
        IObservable<StockQuote> source, int count, TimeSpan interval)
    {
        return source.Buffer(interval, count);
    }

    // Window: like Buffer but emits IObservable<T> instead of IList<T>
    public IObservable<IObservable<StockQuote>> WindowByCount(
        IObservable<StockQuote> source, int windowSize)
    {
        return source.Window(windowSize);
    }

    // Sliding window with overlap
    public IObservable<IList<StockQuote>> SlidingWindow(
        IObservable<StockQuote> source, int windowSize, int skip)
    {
        return source.Buffer(windowSize, skip);
    }
}
```

## Error Handling

```csharp
using System;
using System.Reactive.Linq;

namespace MyApp.Streams;

public class ResilientStream
{
    public IObservable<StockQuote> CreateWithRetry(string symbol)
    {
        return ObservableFactory.CreateStockStream(symbol)
            // Retry up to 3 times on error with delay
            .RetryWhen(errors => errors
                .Select((error, index) => (error, index))
                .SelectMany(pair =>
                {
                    if (pair.index >= 3)
                        return Observable.Throw<long>(pair.error);

                    var delay = TimeSpan.FromSeconds(Math.Pow(2, pair.index));
                    Console.WriteLine(
                        $"Retry {pair.index + 1}/3 after {delay.TotalSeconds}s: {pair.error.Message}");
                    return Observable.Timer(delay);
                }));
    }

    public IObservable<StockQuote> CreateWithFallback(
        string primarySymbol, string fallbackSymbol)
    {
        return ObservableFactory.CreateStockStream(primarySymbol)
            .Catch<StockQuote, Exception>(ex =>
            {
                Console.WriteLine($"Primary failed: {ex.Message}, switching to fallback");
                return ObservableFactory.CreateStockStream(fallbackSymbol);
            });
    }
}
```

## Hot vs. Cold Observables

```csharp
using System;
using System.Reactive.Linq;
using System.Reactive.Subjects;

namespace MyApp.Streams;

public class HotColdDemo
{
    // Cold: each subscriber gets its own sequence
    public IObservable<int> ColdObservable()
    {
        return Observable.Create<int>(observer =>
        {
            for (int i = 0; i < 5; i++)
                observer.OnNext(i);
            observer.OnCompleted();
            return System.Reactive.Disposables.Disposable.Empty;
        });
    }

    // Hot: shared sequence via Subject
    public (IObservable<StockQuote> Stream, IDisposable Connection) HotObservable(
        string symbol)
    {
        var source = ObservableFactory.CreateStockStream(symbol)
            .Publish();  // Convert to IConnectableObservable
        var connection = source.Connect(); // Start producing
        return (source, connection);
    }

    // RefCount: auto-connect when first subscriber, disconnect when last unsubscribes
    public IObservable<StockQuote> SharedStream(string symbol)
    {
        return ObservableFactory.CreateStockStream(symbol)
            .Publish()
            .RefCount();
    }
}
```

## Key Operators Reference

| Category    | Operator                | Purpose                                       |
|-------------|-------------------------|-----------------------------------------------|
| Creation    | `Observable.Create`     | Custom observable with observer callbacks      |
| Creation    | `Observable.Interval`   | Emit sequential numbers at fixed intervals     |
| Creation    | `FromEventPattern`      | Convert .NET events to observables             |
| Filtering   | `Where`                 | Filter elements by predicate                   |
| Filtering   | `Throttle`              | Emit only after a quiet period                 |
| Filtering   | `DistinctUntilChanged`  | Suppress consecutive duplicates                |
| Filtering   | `Take` / `Skip`         | Limit number of elements                       |
| Transform   | `Select`                | Map each element                               |
| Transform   | `SelectMany`            | Flatten nested observables                     |
| Combining   | `Merge`                 | Interleave multiple streams                    |
| Combining   | `CombineLatest`         | Emit when any stream emits (latest of each)    |
| Combining   | `Zip`                   | Pair elements by position                      |
| Combining   | `Switch`                | Subscribe to latest inner observable only       |
| Buffering   | `Buffer`                | Collect elements into batches                  |
| Error       | `Retry`                 | Resubscribe on error                           |
| Error       | `Catch`                 | Switch to fallback on error                    |
| Sharing     | `Publish().RefCount()`  | Share a single subscription among observers    |

## Best Practices

1. **Always dispose subscriptions by storing the `IDisposable` returned by `Subscribe` and calling `Dispose` when done** to prevent memory leaks; use `CompositeDisposable` to manage multiple subscriptions in a single `Dispose` call.

2. **Use `Publish().RefCount()` to share a single upstream subscription among multiple downstream subscribers** instead of letting each subscriber create its own connection to the data source, which duplicates network calls or event handlers.

3. **Apply `Throttle` (debounce) for user input streams and `Sample` for periodic snapshots** -- `Throttle` waits for a quiet period before emitting, while `Sample` emits the latest value at fixed intervals regardless of activity.

4. **Prefer `DistinctUntilChanged` over `Distinct`** because `DistinctUntilChanged` only compares consecutive elements (O(1) memory), while `Distinct` tracks all previously seen values (O(n) memory and unbounded for infinite streams).

5. **Use `ObserveOn(scheduler)` to marshal notifications to the UI thread** and `SubscribeOn(scheduler)` to control which thread the subscription (source) runs on; place `ObserveOn` as late as possible in the pipeline for best performance.

6. **Use `Switch` instead of `SelectMany` when only the latest inner observable matters** (e.g., autocomplete search) because `Switch` automatically unsubscribes from the previous inner observable, preventing stale results from arriving after newer ones.

7. **Handle errors at the subscription level with `onError` or in the pipeline with `Catch` and `Retry`** because an unhandled `OnError` terminates the observable sequence permanently; after `OnError`, no more `OnNext` values are delivered.

8. **Use `Observable.Create` with a `CancellationToken` for async producers** rather than wrapping `Task`-returning methods in `Observable.FromAsync`, because `Create` gives full control over the observable lifecycle and cancellation.

9. **Keep observable pipelines in named methods or well-commented chains** because deeply nested LINQ operators become unreadable; extract complex sub-pipelines into descriptive methods that return `IObservable<T>`.

10. **Test observables using `TestScheduler` from `Microsoft.Reactive.Testing`** to control virtual time and verify time-dependent operators (`Throttle`, `Buffer`, `Delay`) deterministically without waiting for real time to pass.
