---
name: async-patterns
description: Async/await patterns for the .NET 8 WPF widget host app. Use when implementing async commands, background operations, cancellation, progress reporting, or UI thread marshaling.
---

# Async Patterns

## Overview

Establish consistent async patterns that keep the UI responsive while handling long-running operations safely.

## Core Principles

1. **Never block the UI thread** - Use async/await, not `.Result` or `.Wait()`
2. **Always provide cancellation** - Long operations should be cancellable
3. **Report progress** - Users should see feedback on long operations
4. **Handle exceptions** - Async exceptions need explicit handling

---

## Patterns

### 1. Async Commands (RelayCommand)

```csharp
[RelayCommand]
private async Task LoadDataAsync(CancellationToken cancellationToken)
{
    IsLoading = true;
    try
    {
        Data = await _service.GetDataAsync(cancellationToken);
    }
    finally
    {
        IsLoading = false;
    }
}
```

### 2. Cancellation Support

```csharp
private CancellationTokenSource? _cts;

[RelayCommand]
private async Task StartOperationAsync()
{
    _cts?.Cancel();
    _cts = new CancellationTokenSource();
    
    try
    {
        await LongRunningOperationAsync(_cts.Token);
    }
    catch (OperationCanceledException)
    {
        // User cancelled - this is expected
    }
}

[RelayCommand]
private void Cancel()
{
    _cts?.Cancel();
}
```

### 3. Progress Reporting

```csharp
[ObservableProperty]
private int _progress;

[RelayCommand]
private async Task ProcessItemsAsync(CancellationToken cancellationToken)
{
    var items = await GetItemsAsync(cancellationToken);
    
    for (int i = 0; i < items.Count; i++)
    {
        cancellationToken.ThrowIfCancellationRequested();
        await ProcessItemAsync(items[i], cancellationToken);
        Progress = (i + 1) * 100 / items.Count;
    }
}
```

### 4. UI Thread Marshaling

```csharp
// When updating UI from background thread
Application.Current.Dispatcher.Invoke(() =>
{
    Items.Add(newItem);
});

// Prefer async version when possible
await Application.Current.Dispatcher.InvokeAsync(() =>
{
    Items.Add(newItem);
});
```

### 5. Fire-and-Forget (Use Sparingly)

```csharp
// Only for truly fire-and-forget scenarios
_ = Task.Run(async () =>
{
    try
    {
        await BackgroundWorkAsync();
    }
    catch (Exception ex)
    {
        Log.Error(ex, "Background work failed");
    }
});
```

---

## Definition of Done (DoD)

- [ ] Long-running operations use async/await
- [ ] No `.Result` or `.Wait()` calls on UI thread
- [ ] Operations > 100ms have loading indicators
- [ ] User-initiated operations support cancellation
- [ ] Progress shown for batch operations
- [ ] Exceptions logged and user-notified appropriately
- [ ] Dispatcher used for cross-thread UI updates

---

## Anti-Patterns

| ❌ Don't | ✅ Do |
|----------|-------|
| `task.Result` | `await task` |
| `task.Wait()` | `await task` |
| `async void` methods | `async Task` methods |
| Swallowing exceptions | Log and notify user |
| Blocking UI for network | Show loading, use async |

---

## Key Components

| Component | Purpose |
|-----------|---------|
| `[RelayCommand]` | CommunityToolkit async command generation |
| `CancellationTokenSource` | Cancellation coordination |
| `IProgress<T>` | Progress reporting interface |
| `Dispatcher.InvokeAsync` | UI thread marshaling |

---

## Task Scheduling

For background work that shouldn't block commands:

```csharp
// Schedule periodic background work
private readonly PeriodicTimer _timer = new(TimeSpan.FromMinutes(5));

private async Task StartBackgroundRefreshAsync(CancellationToken stoppingToken)
{
    while (await _timer.WaitForNextTickAsync(stoppingToken))
    {
        try
        {
            await RefreshDataAsync(stoppingToken);
        }
        catch (Exception ex) when (ex is not OperationCanceledException)
        {
            Log.Warning(ex, "Background refresh failed");
        }
    }
}
```

