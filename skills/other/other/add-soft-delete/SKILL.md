---
description: Implement soft-delete pattern with grace period and restoration for entities (project)
---
# Add Soft-Delete Pattern Skill

Implement soft-delete semantics with grace period and restoration capabilities for NovaTune entities.

## Overview

Soft-delete provides:
- **Data recovery**: Users can restore deleted items within grace period
- **Audit trail**: Deletion timestamps preserved for compliance
- **Deferred cleanup**: Physical deletion happens asynchronously
- **Quota preservation**: Storage quota released only after physical deletion

## Steps

### 1. Add Soft-Delete Fields to Entity

Location: Extend existing entity model (e.g., `Track.cs`)

```csharp
public sealed class Track
{
    // ... existing fields ...

    // Soft-delete fields
    /// <summary>
    /// Timestamp when the entity was soft-deleted.
    /// Null if not deleted.
    /// </summary>
    public DateTimeOffset? DeletedAt { get; set; }

    /// <summary>
    /// Timestamp when physical deletion will occur.
    /// Null if not deleted.
    /// </summary>
    public DateTimeOffset? ScheduledDeletionAt { get; set; }

    /// <summary>
    /// Status before deletion, used for restoration.
    /// Null if not deleted.
    /// </summary>
    public TrackStatus? StatusBeforeDeletion { get; set; }

    /// <summary>
    /// Indicates if the entity is soft-deleted.
    /// </summary>
    [JsonIgnore]
    public bool IsDeleted => Status == TrackStatus.Deleted;

    /// <summary>
    /// Indicates if the entity can be restored.
    /// </summary>
    [JsonIgnore]
    public bool CanRestore =>
        IsDeleted &&
        ScheduledDeletionAt.HasValue &&
        ScheduledDeletionAt.Value > DateTimeOffset.UtcNow;
}
```

### 2. Add Status Enum Value

```csharp
public enum TrackStatus
{
    Unknown = 0,
    Processing = 1,
    Ready = 2,
    Failed = 3,
    Deleted = 4  // Add if not present
}
```

### 3. Create Configuration Options

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Configuration/SoftDeleteOptions.cs`

```csharp
namespace NovaTuneApp.ApiService.Configuration;

public class SoftDeleteOptions
{
    public const string SectionName = "SoftDelete";

    /// <summary>
    /// Grace period before physical deletion.
    /// Default: 30 days.
    /// </summary>
    public TimeSpan GracePeriod { get; set; } = TimeSpan.FromDays(30);

    /// <summary>
    /// Whether soft-delete is enabled (vs immediate delete).
    /// Default: true.
    /// </summary>
    public bool Enabled { get; set; } = true;
}
```

### 4. Create Custom Exceptions

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Exceptions/`

```csharp
namespace NovaTuneApp.ApiService.Infrastructure.Exceptions;

/// <summary>
/// Thrown when attempting to operate on a deleted entity.
/// </summary>
public class EntityDeletedException : Exception
{
    public string EntityId { get; }
    public string EntityType { get; }
    public DateTimeOffset DeletedAt { get; }

    public EntityDeletedException(string entityType, string entityId, DateTimeOffset deletedAt)
        : base($"{entityType} '{entityId}' has been deleted.")
    {
        EntityType = entityType;
        EntityId = entityId;
        DeletedAt = deletedAt;
    }
}

/// <summary>
/// Thrown when entity is already deleted.
/// </summary>
public class AlreadyDeletedException : Exception
{
    public string EntityId { get; }

    public AlreadyDeletedException(string entityId)
        : base($"Entity '{entityId}' is already deleted.")
    {
        EntityId = entityId;
    }
}

/// <summary>
/// Thrown when restoration grace period has expired.
/// </summary>
public class RestorationExpiredException : Exception
{
    public string EntityId { get; }
    public DateTimeOffset DeletedAt { get; }
    public DateTimeOffset ScheduledDeletionAt { get; }

    public RestorationExpiredException(
        string entityId,
        DateTimeOffset deletedAt,
        DateTimeOffset scheduledDeletionAt)
        : base($"Entity '{entityId}' cannot be restored. Grace period expired at {scheduledDeletionAt}.")
    {
        EntityId = entityId;
        DeletedAt = deletedAt;
        ScheduledDeletionAt = scheduledDeletionAt;
    }
}

/// <summary>
/// Thrown when trying to restore non-deleted entity.
/// </summary>
public class NotDeletedException : Exception
{
    public string EntityId { get; }

    public NotDeletedException(string entityId)
        : base($"Entity '{entityId}' is not deleted and cannot be restored.")
    {
        EntityId = entityId;
    }
}
```

### 5. Implement Soft-Delete in Service

```csharp
public class TrackManagementService : ITrackManagementService
{
    private readonly IAsyncDocumentSession _session;
    private readonly IOutboxService _outboxService;
    private readonly IOptions<SoftDeleteOptions> _softDeleteOptions;
    private readonly IStreamingService _streamingService;
    private readonly ILogger<TrackManagementService> _logger;

    /// <summary>
    /// Soft-deletes a track.
    /// </summary>
    public async Task DeleteTrackAsync(
        string trackId,
        string userId,
        CancellationToken ct = default)
    {
        var track = await _session.LoadAsync<Track>($"Tracks/{trackId}", ct);

        if (track is null)
            throw new TrackNotFoundException(trackId);

        if (track.UserId != userId)
            throw new TrackAccessDeniedException(trackId);

        if (track.Status == TrackStatus.Deleted)
            throw new AlreadyDeletedException(trackId);

        var now = DateTimeOffset.UtcNow;
        var scheduledDeletion = now.Add(_softDeleteOptions.Value.GracePeriod);

        // Preserve current status for potential restoration
        track.StatusBeforeDeletion = track.Status;
        track.Status = TrackStatus.Deleted;
        track.DeletedAt = now;
        track.ScheduledDeletionAt = scheduledDeletion;
        track.UpdatedAt = now;

        // Queue event for physical deletion worker
        var evt = new TrackDeletedEvent
        {
            TrackId = trackId,
            UserId = userId,
            ObjectKey = track.ObjectKey,
            WaveformObjectKey = track.WaveformObjectKey,
            FileSizeBytes = track.FileSizeBytes,
            DeletedAt = now,
            ScheduledDeletionAt = scheduledDeletion,
            CorrelationId = Activity.Current?.Id ?? Ulid.NewUlid().ToString(),
            Timestamp = now
        };

        await _outboxService.WriteAsync(evt, partitionKey: trackId, ct: ct);

        // Save atomically
        await _session.SaveChangesAsync(ct);

        // Invalidate cache immediately (best effort)
        try
        {
            await _streamingService.InvalidateCacheAsync(trackId, userId, ct);
        }
        catch (Exception ex)
        {
            _logger.LogWarning(ex, "Failed to invalidate cache for track {TrackId}", trackId);
        }

        _logger.LogInformation(
            "Track {TrackId} soft-deleted for user {UserId}, scheduled for physical deletion at {ScheduledAt}",
            trackId, userId, scheduledDeletion);
    }

    /// <summary>
    /// Restores a soft-deleted track within the grace period.
    /// </summary>
    public async Task<TrackDetails> RestoreTrackAsync(
        string trackId,
        string userId,
        CancellationToken ct = default)
    {
        var track = await _session.LoadAsync<Track>($"Tracks/{trackId}", ct);

        if (track is null)
            throw new TrackNotFoundException(trackId);

        if (track.UserId != userId)
            throw new TrackAccessDeniedException(trackId);

        if (track.Status != TrackStatus.Deleted)
            throw new NotDeletedException(trackId);

        if (!track.CanRestore)
        {
            throw new RestorationExpiredException(
                trackId,
                track.DeletedAt!.Value,
                track.ScheduledDeletionAt!.Value);
        }

        // Restore to previous status
        track.Status = track.StatusBeforeDeletion ?? TrackStatus.Ready;
        track.StatusBeforeDeletion = null;
        track.DeletedAt = null;
        track.ScheduledDeletionAt = null;
        track.UpdatedAt = DateTimeOffset.UtcNow;

        await _session.SaveChangesAsync(ct);

        _logger.LogInformation(
            "Track {TrackId} restored for user {UserId}",
            trackId, userId);

        return MapToDetails(track);
    }
}
```

### 6. Add API Endpoints

```csharp
// DELETE /tracks/{trackId} - Soft delete
group.MapDelete("/{trackId}", async (
    [FromRoute] string trackId,
    [FromServices] ITrackManagementService trackService,
    ClaimsPrincipal user,
    CancellationToken ct) =>
{
    if (!Ulid.TryParse(trackId, out _))
    {
        return Results.Problem(
            title: "Invalid track ID",
            detail: "Track ID must be a valid ULID.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-track-id");
    }

    var userId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    try
    {
        await trackService.DeleteTrackAsync(trackId, userId, ct);
        return Results.NoContent();
    }
    catch (TrackNotFoundException)
    {
        return Results.Problem(
            title: "Track not found",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/track-not-found");
    }
    catch (TrackAccessDeniedException)
    {
        return Results.Problem(
            title: "Access denied",
            statusCode: StatusCodes.Status403Forbidden,
            type: "https://novatune.dev/errors/forbidden");
    }
    catch (AlreadyDeletedException ex)
    {
        return Results.Problem(
            title: "Track already deleted",
            detail: "This track has already been deleted.",
            statusCode: StatusCodes.Status409Conflict,
            type: "https://novatune.dev/errors/already-deleted",
            extensions: new Dictionary<string, object?>
            {
                ["trackId"] = ex.EntityId
            });
    }
})
.WithName("DeleteTrack")
.Produces(StatusCodes.Status204NoContent)
.ProducesProblem(StatusCodes.Status404NotFound)
.ProducesProblem(StatusCodes.Status409Conflict);

// POST /tracks/{trackId}/restore - Restore soft-deleted track
group.MapPost("/{trackId}/restore", async (
    [FromRoute] string trackId,
    [FromServices] ITrackManagementService trackService,
    ClaimsPrincipal user,
    CancellationToken ct) =>
{
    if (!Ulid.TryParse(trackId, out _))
    {
        return Results.Problem(
            title: "Invalid track ID",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-track-id");
    }

    var userId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    try
    {
        var track = await trackService.RestoreTrackAsync(trackId, userId, ct);
        return Results.Ok(track);
    }
    catch (TrackNotFoundException)
    {
        return Results.Problem(
            title: "Track not found",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/track-not-found");
    }
    catch (TrackAccessDeniedException)
    {
        return Results.Problem(
            title: "Access denied",
            statusCode: StatusCodes.Status403Forbidden,
            type: "https://novatune.dev/errors/forbidden");
    }
    catch (NotDeletedException ex)
    {
        return Results.Problem(
            title: "Track not deleted",
            detail: "This track is not deleted and cannot be restored.",
            statusCode: StatusCodes.Status409Conflict,
            type: "https://novatune.dev/errors/not-deleted",
            extensions: new Dictionary<string, object?>
            {
                ["trackId"] = ex.EntityId
            });
    }
    catch (RestorationExpiredException ex)
    {
        return Results.Problem(
            title: "Restoration period expired",
            detail: $"The track cannot be restored because the grace period has expired.",
            statusCode: StatusCodes.Status410Gone,
            type: "https://novatune.dev/errors/restoration-expired",
            extensions: new Dictionary<string, object?>
            {
                ["trackId"] = ex.EntityId,
                ["deletedAt"] = ex.DeletedAt,
                ["scheduledDeletionAt"] = ex.ScheduledDeletionAt
            });
    }
})
.WithName("RestoreTrack")
.Produces<TrackDetails>(StatusCodes.Status200OK)
.ProducesProblem(StatusCodes.Status404NotFound)
.ProducesProblem(StatusCodes.Status409Conflict)
.ProducesProblem(StatusCodes.Status410Gone);
```

### 7. Create RavenDB Index for Scheduled Deletions

```csharp
using Raven.Client.Documents.Indexes;
using NovaTuneApp.ApiService.Models;

namespace NovaTuneApp.ApiService.Infrastructure.Indexes;

public class Tracks_ByScheduledDeletion : AbstractIndexCreationTask<Track>
{
    public Tracks_ByScheduledDeletion()
    {
        Map = tracks => from track in tracks
                        where track.Status == TrackStatus.Deleted
                           && track.ScheduledDeletionAt != null
                        select new
                        {
                            track.Status,
                            track.ScheduledDeletionAt
                        };
    }
}
```

### 8. Add Configuration to appsettings.json

```json
{
  "SoftDelete": {
    "GracePeriod": "30.00:00:00",
    "Enabled": true
  }
}
```

### 9. Register Configuration

```csharp
builder.Services.Configure<SoftDeleteOptions>(
    builder.Configuration.GetSection(SoftDeleteOptions.SectionName));
```

## State Transitions

```
┌──────────────┐     DELETE      ┌─────────────┐     RESTORE     ┌──────────────┐
│  Processing  │ ───────────────►│   Deleted   │ ───────────────►│   Ready      │
│  or Ready    │                 │             │                 │ (previous)   │
└──────────────┘                 └──────┬──────┘                 └──────────────┘
                                        │
                                        │ Grace period expires
                                        ▼
                                 ┌─────────────┐
                                 │  Physically │
                                 │  Deleted    │
                                 └─────────────┘
```

## Query Patterns

### Exclude Deleted by Default

```csharp
var activeTracks = await session
    .Query<Track>()
    .Where(t => t.UserId == userId && t.Status != TrackStatus.Deleted)
    .ToListAsync(ct);
```

### Include Deleted (for restore UI)

```csharp
var allTracks = await session
    .Query<Track>()
    .Where(t => t.UserId == userId)
    .ToListAsync(ct);
```

### Find Tracks Ready for Physical Deletion

```csharp
var expiredTracks = await session
    .Query<Track, Tracks_ByScheduledDeletion>()
    .Where(t => t.Status == TrackStatus.Deleted
             && t.ScheduledDeletionAt <= DateTimeOffset.UtcNow)
    .Take(batchSize)
    .ToListAsync(ct);
```

## Best Practices

1. **Preserve previous status**: Store `StatusBeforeDeletion` for accurate restoration
2. **Use transactions**: Write entity update and outbox message atomically
3. **Validate ownership**: Always check user owns entity before delete/restore
4. **Log state transitions**: Include timestamps and correlation IDs
5. **Rate limit deletions**: Prevent abuse (10 req/min per user)
6. **Exclude deleted by default**: List endpoints should not show deleted items unless requested
7. **Cache invalidation**: Invalidate immediately on soft-delete

## Testing

```csharp
[Fact]
public async Task DeleteTrack_Should_SoftDelete_WithGracePeriod()
{
    // Arrange
    var track = await CreateTestTrack(TrackStatus.Ready);

    // Act
    await _service.DeleteTrackAsync(track.TrackId, _userId, CancellationToken.None);

    // Assert
    var deleted = await _session.LoadAsync<Track>($"Tracks/{track.TrackId}");
    deleted.Status.ShouldBe(TrackStatus.Deleted);
    deleted.DeletedAt.ShouldNotBeNull();
    deleted.ScheduledDeletionAt.ShouldNotBeNull();
    deleted.StatusBeforeDeletion.ShouldBe(TrackStatus.Ready);
}

[Fact]
public async Task RestoreTrack_Should_RestorePreviousStatus()
{
    // Arrange
    var track = await CreateTestTrack(TrackStatus.Processing);
    await _service.DeleteTrackAsync(track.TrackId, _userId, CancellationToken.None);

    // Act
    var restored = await _service.RestoreTrackAsync(track.TrackId, _userId, CancellationToken.None);

    // Assert
    restored.Status.ShouldBe(TrackStatus.Processing);
}

[Fact]
public async Task RestoreTrack_Should_Throw_WhenGracePeriodExpired()
{
    // Arrange - create track with expired scheduled deletion
    var track = await CreateTestTrack(TrackStatus.Ready);
    track.Status = TrackStatus.Deleted;
    track.DeletedAt = DateTimeOffset.UtcNow.AddDays(-31);
    track.ScheduledDeletionAt = DateTimeOffset.UtcNow.AddDays(-1);
    await _session.SaveChangesAsync();

    // Act & Assert
    await Should.ThrowAsync<RestorationExpiredException>(
        () => _service.RestoreTrackAsync(track.TrackId, _userId, CancellationToken.None));
}
```
