---
description: Add metrics, logging, and distributed tracing to NovaTune services (project)
---
# Add Observability Skill

Add metrics, structured logging, and distributed tracing to NovaTune services.

## Project Context

- Metrics: Custom metrics via `System.Diagnostics.Metrics`
- Logging: Serilog with structured JSON output
- Tracing: OpenTelemetry via Aspire ServiceDefaults
- Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Observability/`

## Steps

### 1. Create Metrics Class

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Observability/NovaTuneMetrics.cs`

```csharp
using System.Diagnostics.Metrics;

namespace NovaTuneApp.ApiService.Infrastructure.Observability;

/// <summary>
/// Custom metrics for NovaTune track management.
/// </summary>
public sealed class NovaTuneMetrics
{
    public const string MeterName = "NovaTune.ApiService";

    private readonly Counter<long> _trackListRequestsTotal;
    private readonly Histogram<double> _trackListDurationMs;
    private readonly Counter<long> _trackGetRequestsTotal;
    private readonly Counter<long> _trackUpdateRequestsTotal;
    private readonly Counter<long> _trackDeleteRequestsTotal;
    private readonly Counter<long> _trackRestoreRequestsTotal;
    private readonly Counter<long> _trackSoftDeletionsTotal;
    private readonly Counter<long> _trackPhysicalDeletionsTotal;
    private readonly Histogram<double> _trackPhysicalDeletionDurationMs;
    private readonly Counter<long> _storageFreedBytesTotal;

    public NovaTuneMetrics(IMeterFactory meterFactory)
    {
        var meter = meterFactory.Create(MeterName);

        _trackListRequestsTotal = meter.CreateCounter<long>(
            "track_list_requests_total",
            unit: "{requests}",
            description: "Total track list requests");

        _trackListDurationMs = meter.CreateHistogram<double>(
            "track_list_request_duration_ms",
            unit: "ms",
            description: "Track list request duration in milliseconds");

        _trackGetRequestsTotal = meter.CreateCounter<long>(
            "track_get_requests_total",
            unit: "{requests}",
            description: "Total track get requests");

        _trackUpdateRequestsTotal = meter.CreateCounter<long>(
            "track_update_requests_total",
            unit: "{requests}",
            description: "Total track update requests");

        _trackDeleteRequestsTotal = meter.CreateCounter<long>(
            "track_delete_requests_total",
            unit: "{requests}",
            description: "Total track delete requests");

        _trackRestoreRequestsTotal = meter.CreateCounter<long>(
            "track_restore_requests_total",
            unit: "{requests}",
            description: "Total track restore requests");

        _trackSoftDeletionsTotal = meter.CreateCounter<long>(
            "track_soft_deletions_total",
            unit: "{tracks}",
            description: "Total tracks soft-deleted");

        _trackPhysicalDeletionsTotal = meter.CreateCounter<long>(
            "track_physical_deletions_total",
            unit: "{tracks}",
            description: "Total tracks physically deleted");

        _trackPhysicalDeletionDurationMs = meter.CreateHistogram<double>(
            "track_physical_deletion_duration_ms",
            unit: "ms",
            description: "Physical deletion duration in milliseconds");

        _storageFreedBytesTotal = meter.CreateCounter<long>(
            "storage_freed_bytes_total",
            unit: "By",
            description: "Total storage bytes freed by physical deletions");
    }

    public void RecordTrackListRequest(string status)
        => _trackListRequestsTotal.Add(1, new KeyValuePair<string, object?>("status", status));

    public void RecordTrackListDuration(double durationMs)
        => _trackListDurationMs.Record(durationMs);

    public void RecordTrackGetRequest(string status)
        => _trackGetRequestsTotal.Add(1, new KeyValuePair<string, object?>("status", status));

    public void RecordTrackUpdateRequest(string status)
        => _trackUpdateRequestsTotal.Add(1, new KeyValuePair<string, object?>("status", status));

    public void RecordTrackDeleteRequest(string status)
        => _trackDeleteRequestsTotal.Add(1, new KeyValuePair<string, object?>("status", status));

    public void RecordTrackRestoreRequest(string status)
        => _trackRestoreRequestsTotal.Add(1, new KeyValuePair<string, object?>("status", status));

    public void RecordSoftDeletion()
        => _trackSoftDeletionsTotal.Add(1);

    public void RecordPhysicalDeletion(string status)
        => _trackPhysicalDeletionsTotal.Add(1, new KeyValuePair<string, object?>("status", status));

    public void RecordPhysicalDeletionDuration(double durationMs)
        => _trackPhysicalDeletionDurationMs.Record(durationMs);

    public void RecordStorageFreed(long bytes)
        => _storageFreedBytesTotal.Add(bytes);
}
```

### 2. Register Metrics in Program.cs

```csharp
// Register metrics
builder.Services.AddSingleton<NovaTuneMetrics>();

// Configure OpenTelemetry to export custom metrics
builder.Services.AddOpenTelemetry()
    .WithMetrics(metrics =>
    {
        metrics.AddMeter(NovaTuneMetrics.MeterName);
    });
```

### 3. Use Metrics in Services

```csharp
public class TrackManagementService : ITrackManagementService
{
    private readonly NovaTuneMetrics _metrics;
    private readonly ILogger<TrackManagementService> _logger;

    public TrackManagementService(
        NovaTuneMetrics metrics,
        ILogger<TrackManagementService> logger)
    {
        _metrics = metrics;
        _logger = logger;
    }

    public async Task<PagedResult<TrackListItem>> ListTracksAsync(
        string userId,
        TrackListQuery query,
        CancellationToken ct)
    {
        var stopwatch = Stopwatch.StartNew();
        try
        {
            var result = await DoListTracksAsync(userId, query, ct);
            _metrics.RecordTrackListRequest("success");
            return result;
        }
        catch (Exception)
        {
            _metrics.RecordTrackListRequest("error");
            throw;
        }
        finally
        {
            _metrics.RecordTrackListDuration(stopwatch.Elapsed.TotalMilliseconds);
        }
    }
}
```

### 4. Configure Structured Logging

Location: `Program.cs` or service setup

```csharp
using Serilog;
using Serilog.Events;
using Serilog.Formatting.Compact;

// Bootstrap logger (before builder)
Log.Logger = new LoggerConfiguration()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .WriteTo.Console(new RenderedCompactJsonFormatter())
    .CreateBootstrapLogger();

// Full configuration (in builder)
builder.Services.AddSerilog((services, configuration) => configuration
    .ReadFrom.Configuration(builder.Configuration)
    .ReadFrom.Services(services)
    .MinimumLevel.Information()
    .MinimumLevel.Override("Microsoft", LogEventLevel.Warning)
    .MinimumLevel.Override("Microsoft.AspNetCore.Hosting", LogEventLevel.Warning)
    .MinimumLevel.Override("Microsoft.AspNetCore.Routing", LogEventLevel.Warning)
    .Enrich.FromLogContext()
    .Enrich.WithEnvironmentName()
    .Enrich.WithMachineName()
    .Enrich.WithProperty("Service", "NovaTune.ApiService")
    .WriteTo.Console(new RenderedCompactJsonFormatter()));
```

### 5. Implement Structured Logging

```csharp
// Good: Structured with semantic properties
_logger.LogInformation(
    "Track {TrackId} soft-deleted for user {UserId}, scheduled deletion at {ScheduledAt}",
    trackId,
    userId,
    scheduledDeletionAt);

// Good: Using scopes for correlation
using (_logger.BeginScope(new Dictionary<string, object>
{
    ["CorrelationId"] = correlationId,
    ["TrackId"] = trackId
}))
{
    _logger.LogInformation("Starting track deletion process");
    // ... operations
    _logger.LogInformation("Track deletion completed successfully");
}

// Good: Different levels for different scenarios
_logger.LogDebug("Track list requested: {Search}, {Status}, {Limit}", search, status, limit);
_logger.LogInformation("Track {TrackId} updated by user {UserId}", trackId, userId);
_logger.LogWarning("Access denied: User {UserId} attempted to access track {TrackId} owned by {OwnerId}",
    userId, trackId, ownerId);
_logger.LogError(ex, "Failed to physically delete track {TrackId}", trackId);
```

### 6. Add Distributed Tracing

```csharp
using System.Diagnostics;

public class TrackManagementService : ITrackManagementService
{
    private static readonly ActivitySource ActivitySource = new("NovaTune.TrackManagement");

    public async Task DeleteTrackAsync(string trackId, string userId, CancellationToken ct)
    {
        using var activity = ActivitySource.StartActivity("track.delete");
        activity?.SetTag("track.id", trackId);
        activity?.SetTag("user.id", userId);

        try
        {
            // Step 1: Update status
            using (var dbActivity = ActivitySource.StartActivity("db.update_status"))
            {
                await UpdateStatusAsync(trackId, ct);
            }

            // Step 2: Write outbox
            using (var outboxActivity = ActivitySource.StartActivity("outbox.write"))
            {
                await WriteOutboxAsync(trackId, ct);
            }

            // Step 3: Invalidate cache
            using (var cacheActivity = ActivitySource.StartActivity("cache.invalidate"))
            {
                await InvalidateCacheAsync(trackId, ct);
            }

            activity?.SetStatus(ActivityStatusCode.Ok);
        }
        catch (Exception ex)
        {
            activity?.SetStatus(ActivityStatusCode.Error, ex.Message);
            activity?.RecordException(ex);
            throw;
        }
    }
}
```

### 7. Register Tracing in ServiceDefaults

The ServiceDefaults project configures OpenTelemetry tracing:

```csharp
// In AddServiceDefaults extension
builder.Services.AddOpenTelemetry()
    .WithTracing(tracing =>
    {
        tracing
            .AddSource("NovaTune.TrackManagement")
            .AddSource("NovaTune.Streaming")
            .AddAspNetCoreInstrumentation()
            .AddHttpClientInstrumentation()
            .AddRavenDBInstrumentation();
    });
```

## Logging Guidelines

| Event | Level | Required Fields |
|-------|-------|-----------------|
| Track list requested | Debug | `UserId`, `Search`, `Status`, `Limit` |
| Track retrieved | Debug | `TrackId`, `UserId` |
| Track updated | Info | `TrackId`, `UserId`, `ChangedFields` |
| Track soft-deleted | Info | `TrackId`, `UserId`, `ScheduledDeletionAt` |
| Track restored | Info | `TrackId`, `UserId` |
| Physical deletion started | Info | `TrackId`, `UserId` |
| Physical deletion completed | Info | `TrackId`, `UserId`, `FreedBytes` |
| Physical deletion failed | Error | `TrackId`, `Error` |
| Access denied | Warning | `TrackId`, `UserId`, `OwnerId` |

## Redaction (NF-4.5)

Never log sensitive data:

```csharp
// BAD - Don't log object keys
_logger.LogInformation("Deleting object {ObjectKey}", objectKey);

// GOOD - Log identifiers only
_logger.LogInformation("Deleting storage objects for track {TrackId}", trackId);
```

## Metrics Summary

| Metric | Type | Labels |
|--------|------|--------|
| `track_list_requests_total` | Counter | `status` |
| `track_list_request_duration_ms` | Histogram | — |
| `track_get_requests_total` | Counter | `status` |
| `track_update_requests_total` | Counter | `status` |
| `track_delete_requests_total` | Counter | `status` |
| `track_restore_requests_total` | Counter | `status` |
| `track_soft_deletions_total` | Counter | — |
| `track_physical_deletions_total` | Counter | `status` |
| `track_physical_deletion_duration_ms` | Histogram | — |
| `storage_freed_bytes_total` | Counter | — |

## Testing Observability

```csharp
[Fact]
public void Metrics_Should_RecordTrackListRequest()
{
    // Arrange
    var meterFactory = new TestMeterFactory();
    var metrics = new NovaTuneMetrics(meterFactory);

    // Act
    metrics.RecordTrackListRequest("success");

    // Assert
    var measurements = meterFactory.GetMeasurements("track_list_requests_total");
    measurements.Should().ContainSingle()
        .Which.Value.Should().Be(1);
}
```
