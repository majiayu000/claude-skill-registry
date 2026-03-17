---
description: Create BackgroundService implementations for scheduled or polling tasks (project)
---
# Add Background Service Skill

Create `BackgroundService` implementations for scheduled or polling tasks in NovaTune.

## Project Context

- Service location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/` or worker projects
- Base class: `Microsoft.Extensions.Hosting.BackgroundService`
- Pattern: Polling loop with configurable interval

## Steps

### 1. Create Options Class

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Configuration/{ServiceName}Options.cs`

```csharp
namespace NovaTuneApp.ApiService.Configuration;

public class PhysicalDeletionOptions
{
    public const string SectionName = "PhysicalDeletion";

    /// <summary>
    /// Interval between polling cycles.
    /// Default: 5 minutes.
    /// </summary>
    public TimeSpan PollingInterval { get; set; } = TimeSpan.FromMinutes(5);

    /// <summary>
    /// Maximum items to process per cycle.
    /// Default: 50.
    /// </summary>
    public int BatchSize { get; set; } = 50;

    /// <summary>
    /// Whether the service is enabled.
    /// Default: true.
    /// </summary>
    public bool Enabled { get; set; } = true;
}
```

### 2. Create Background Service

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Services/{ServiceName}Service.cs`

```csharp
using Microsoft.Extensions.Options;

namespace NovaTuneApp.ApiService.Infrastructure.Services;

/// <summary>
/// Background service that processes physical deletions for soft-deleted tracks.
/// </summary>
public class PhysicalDeletionService : BackgroundService
{
    private readonly IServiceProvider _serviceProvider;
    private readonly IOptions<PhysicalDeletionOptions> _options;
    private readonly ILogger<PhysicalDeletionService> _logger;

    public PhysicalDeletionService(
        IServiceProvider serviceProvider,
        IOptions<PhysicalDeletionOptions> options,
        ILogger<PhysicalDeletionService> logger)
    {
        _serviceProvider = serviceProvider;
        _options = options;
        _logger = logger;
    }

    protected override async Task ExecuteAsync(CancellationToken stoppingToken)
    {
        if (!_options.Value.Enabled)
        {
            _logger.LogInformation("Physical deletion service is disabled");
            return;
        }

        _logger.LogInformation(
            "Physical deletion service starting with {Interval} interval",
            _options.Value.PollingInterval);

        while (!stoppingToken.IsCancellationRequested)
        {
            try
            {
                await ProcessBatchAsync(stoppingToken);
            }
            catch (OperationCanceledException) when (stoppingToken.IsCancellationRequested)
            {
                break;
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Error processing physical deletions");
            }

            await Task.Delay(_options.Value.PollingInterval, stoppingToken);
        }

        _logger.LogInformation("Physical deletion service stopped");
    }

    private async Task ProcessBatchAsync(CancellationToken ct)
    {
        using var scope = _serviceProvider.CreateScope();
        var session = scope.ServiceProvider.GetRequiredService<IAsyncDocumentSession>();
        var storageService = scope.ServiceProvider.GetRequiredService<IStorageService>();

        var itemsToProcess = await session
            .Query<Track, Tracks_ByScheduledDeletion>()
            .Where(t => t.Status == TrackStatus.Deleted
                     && t.ScheduledDeletionAt <= DateTimeOffset.UtcNow)
            .Take(_options.Value.BatchSize)
            .ToListAsync(ct);

        if (itemsToProcess.Count == 0)
        {
            _logger.LogDebug("No items to process");
            return;
        }

        _logger.LogInformation("Processing {Count} items for physical deletion", itemsToProcess.Count);

        foreach (var item in itemsToProcess)
        {
            try
            {
                await ProcessItemAsync(item, session, storageService, ct);
            }
            catch (Exception ex)
            {
                _logger.LogError(ex, "Failed to process item {ItemId}", item.Id);
                // Continue with next item; will retry on next poll
            }
        }
    }

    private async Task ProcessItemAsync(
        Track track,
        IAsyncDocumentSession session,
        IStorageService storageService,
        CancellationToken ct)
    {
        // Delete storage objects
        await storageService.DeleteObjectAsync(track.ObjectKey, ct);

        if (track.WaveformObjectKey is not null)
        {
            await storageService.DeleteObjectAsync(track.WaveformObjectKey, ct);
        }

        // Delete document
        session.Delete(track);
        await session.SaveChangesAsync(ct);

        _logger.LogInformation(
            "Physically deleted track {TrackId} for user {UserId}",
            track.TrackId, track.UserId);
    }
}
```

### 3. Register Service

In `Program.cs`:

```csharp
// Register options
builder.Services.Configure<PhysicalDeletionOptions>(
    builder.Configuration.GetSection(PhysicalDeletionOptions.SectionName));

// Register hosted service
builder.Services.AddHostedService<PhysicalDeletionService>();
```

### 4. Add Configuration

In `appsettings.json`:

```json
{
  "PhysicalDeletion": {
    "PollingInterval": "00:05:00",
    "BatchSize": 50,
    "Enabled": true
  }
}
```

## Patterns

### Simple Polling Service

```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    while (!stoppingToken.IsCancellationRequested)
    {
        await DoWorkAsync(stoppingToken);
        await Task.Delay(_interval, stoppingToken);
    }
}
```

### Service with Startup Delay

```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    // Let the app start up first
    await Task.Delay(TimeSpan.FromSeconds(10), stoppingToken);

    while (!stoppingToken.IsCancellationRequested)
    {
        await DoWorkAsync(stoppingToken);
        await Task.Delay(_interval, stoppingToken);
    }
}
```

### Service with Retry Logic

```csharp
protected override async Task ExecuteAsync(CancellationToken stoppingToken)
{
    const int maxRetries = 5;

    while (!stoppingToken.IsCancellationRequested)
    {
        var retryCount = 0;
        var success = false;

        while (!success && retryCount < maxRetries)
        {
            try
            {
                await DoWorkAsync(stoppingToken);
                success = true;
            }
            catch (Exception ex) when (retryCount < maxRetries - 1)
            {
                retryCount++;
                _logger.LogWarning(ex, "Retry {Attempt}/{Max}", retryCount, maxRetries);
                await Task.Delay(TimeSpan.FromSeconds(Math.Pow(2, retryCount)), stoppingToken);
            }
        }

        await Task.Delay(_interval, stoppingToken);
    }
}
```

## Best Practices

1. **Use scoped services** - Create scope for each batch/iteration
2. **Handle cancellation** - Always check `stoppingToken`
3. **Log appropriately** - Info for start/stop, Debug for iterations
4. **Configure intervals** - Use options pattern for configuration
5. **Process in batches** - Avoid loading too many items at once
6. **Continue on item failure** - Don't fail the entire batch

## Testing

```csharp
[Fact]
public async Task Service_Should_ProcessItemsInBatches()
{
    // Arrange
    var options = Options.Create(new PhysicalDeletionOptions
    {
        BatchSize = 10,
        PollingInterval = TimeSpan.FromMilliseconds(100)
    });

    var service = new PhysicalDeletionService(
        _serviceProvider,
        options,
        _logger);

    // Act
    using var cts = new CancellationTokenSource(TimeSpan.FromSeconds(1));
    await service.StartAsync(cts.Token);
    await Task.Delay(500);
    await service.StopAsync(CancellationToken.None);

    // Assert
    // Verify items were processed
}
```
