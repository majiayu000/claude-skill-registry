---
description: Add and remove tracks from playlists with position management and validation (project)
---
# Add Playlist Tracks Skill

Implement adding and removing tracks from playlists with ownership validation, position management, and quota enforcement.

## Overview

Playlist track management involves:
- Adding tracks at specific positions (or appending)
- Removing tracks by position
- Validating track ownership and status
- Enforcing track limits per playlist
- Maintaining position integrity

## Steps

### 1. Create Request Models

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Playlists/`

```csharp
namespace NovaTuneApp.ApiService.Models.Playlists;

/// <summary>
/// Request to add tracks to a playlist.
/// </summary>
/// <param name="TrackIds">Track IDs to add (1-100 per request)</param>
/// <param name="Position">Insert position (null = append to end)</param>
public record AddTracksRequest(
    IReadOnlyList<string> TrackIds,
    int? Position = null);
```

### 2. Add Validation

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Validators/`

```csharp
using FluentValidation;

namespace NovaTuneApp.ApiService.Validators;

public class AddTracksRequestValidator : AbstractValidator<AddTracksRequest>
{
    public AddTracksRequestValidator(IOptions<PlaylistOptions> options)
    {
        RuleFor(x => x.TrackIds)
            .NotEmpty()
            .WithMessage("At least one track ID is required")
            .Must(ids => ids.Count <= options.Value.MaxTracksPerAddRequest)
            .WithMessage($"Maximum {options.Value.MaxTracksPerAddRequest} tracks per request");

        RuleForEach(x => x.TrackIds)
            .Must(id => Ulid.TryParse(id, out _))
            .WithMessage("Track ID must be a valid ULID");

        RuleFor(x => x.Position)
            .GreaterThanOrEqualTo(0)
            .When(x => x.Position.HasValue)
            .WithMessage("Position must be non-negative");
    }
}
```

### 3. Implement Add Tracks in Service

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/PlaylistService.cs`

```csharp
public async Task<PlaylistDetails> AddTracksAsync(
    string playlistId,
    string userId,
    AddTracksRequest request,
    CancellationToken ct = default)
{
    var playlist = await _session.LoadAsync<Playlist>($"Playlists/{playlistId}", ct);

    if (playlist is null)
        throw new PlaylistNotFoundException(playlistId);

    if (playlist.UserId != userId)
        throw new PlaylistAccessDeniedException(playlistId);

    // Check track limit
    if (playlist.TrackCount + request.TrackIds.Count > _options.Value.MaxTracksPerPlaylist)
    {
        throw new PlaylistTrackLimitExceededException(
            playlistId,
            playlist.TrackCount,
            request.TrackIds.Count,
            _options.Value.MaxTracksPerPlaylist);
    }

    // Load and validate all tracks
    var trackDocIds = request.TrackIds.Select(id => $"Tracks/{id}").ToList();
    var trackDocs = await _session.LoadAsync<Track>(trackDocIds, ct);

    var validatedTracks = new List<Track>();
    foreach (var trackId in request.TrackIds)
    {
        var docId = $"Tracks/{trackId}";
        if (!trackDocs.TryGetValue(docId, out var track) || track is null)
            throw new TrackNotFoundException(trackId);

        if (track.UserId != userId)
            throw new TrackAccessDeniedException(trackId);

        if (track.Status == TrackStatus.Deleted)
            throw new TrackDeletedException(trackId);

        validatedTracks.Add(track);
    }

    var now = DateTimeOffset.UtcNow;
    var insertPosition = request.Position ?? playlist.Tracks.Count;

    // Validate insert position
    if (insertPosition < 0 || insertPosition > playlist.Tracks.Count)
    {
        throw new InvalidPositionException(insertPosition, playlist.Tracks.Count + 1);
    }

    // Shift existing tracks at and after insert position
    foreach (var entry in playlist.Tracks.Where(t => t.Position >= insertPosition))
    {
        entry.Position += request.TrackIds.Count;
    }

    // Create new track entries
    var newEntries = request.TrackIds.Select((id, i) => new PlaylistTrackEntry
    {
        Position = insertPosition + i,
        TrackId = id,
        AddedAt = now
    }).ToList();

    playlist.Tracks.AddRange(newEntries);

    // Sort by position to maintain order
    playlist.Tracks = playlist.Tracks.OrderBy(t => t.Position).ToList();

    // Update denormalized fields
    playlist.TrackCount = playlist.Tracks.Count;
    playlist.TotalDuration = CalculateTotalDuration(playlist.Tracks, trackDocs);
    playlist.UpdatedAt = now;

    await _session.SaveChangesAsync(ct);

    _logger.LogInformation(
        "Added {Count} tracks to playlist {PlaylistId} at position {Position} for user {UserId}",
        request.TrackIds.Count, playlistId, insertPosition, userId);

    return await MapToDetailsAsync(playlist, ct);
}

private TimeSpan CalculateTotalDuration(
    List<PlaylistTrackEntry> entries,
    IDictionary<string, Track?> trackDocs)
{
    var total = TimeSpan.Zero;
    foreach (var entry in entries)
    {
        if (trackDocs.TryGetValue($"Tracks/{entry.TrackId}", out var track) && track is not null)
        {
            total += track.Duration;
        }
    }
    return total;
}
```

### 4. Implement Remove Track in Service

```csharp
public async Task RemoveTrackAsync(
    string playlistId,
    string userId,
    int position,
    CancellationToken ct = default)
{
    var playlist = await _session.LoadAsync<Playlist>($"Playlists/{playlistId}", ct);

    if (playlist is null)
        throw new PlaylistNotFoundException(playlistId);

    if (playlist.UserId != userId)
        throw new PlaylistAccessDeniedException(playlistId);

    // Find track at position
    var trackToRemove = playlist.Tracks.FirstOrDefault(t => t.Position == position);
    if (trackToRemove is null)
        throw new PlaylistTrackNotFoundException(playlistId, position);

    // Remove the track
    playlist.Tracks.Remove(trackToRemove);

    // Reindex positions for tracks after the removed one
    foreach (var entry in playlist.Tracks.Where(t => t.Position > position))
    {
        entry.Position--;
    }

    // Update denormalized fields
    playlist.TrackCount = playlist.Tracks.Count;
    playlist.UpdatedAt = DateTimeOffset.UtcNow;

    // Recalculate total duration
    await RecalculateTotalDurationAsync(playlist, ct);

    await _session.SaveChangesAsync(ct);

    _logger.LogInformation(
        "Removed track at position {Position} from playlist {PlaylistId} for user {UserId}",
        position, playlistId, userId);
}

private async Task RecalculateTotalDurationAsync(Playlist playlist, CancellationToken ct)
{
    if (playlist.Tracks.Count == 0)
    {
        playlist.TotalDuration = TimeSpan.Zero;
        return;
    }

    var trackIds = playlist.Tracks.Select(t => $"Tracks/{t.TrackId}").ToList();
    var tracks = await _session.LoadAsync<Track>(trackIds, ct);

    playlist.TotalDuration = CalculateTotalDuration(playlist.Tracks, tracks);
}
```

### 5. Create Custom Exceptions

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Exceptions/`

```csharp
namespace NovaTuneApp.ApiService.Infrastructure.Exceptions;

/// <summary>
/// Thrown when adding tracks would exceed the playlist track limit.
/// </summary>
public class PlaylistTrackLimitExceededException : Exception
{
    public string PlaylistId { get; }
    public int CurrentCount { get; }
    public int AddCount { get; }
    public int MaxCount { get; }

    public PlaylistTrackLimitExceededException(
        string playlistId,
        int currentCount,
        int addCount,
        int maxCount)
        : base($"Cannot add {addCount} tracks. Playlist has {currentCount} tracks, limit is {maxCount}.")
    {
        PlaylistId = playlistId;
        CurrentCount = currentCount;
        AddCount = addCount;
        MaxCount = maxCount;
    }
}

/// <summary>
/// Thrown when a track is not found at the specified position in a playlist.
/// </summary>
public class PlaylistTrackNotFoundException : Exception
{
    public string PlaylistId { get; }
    public int Position { get; }

    public PlaylistTrackNotFoundException(string playlistId, int position)
        : base($"No track found at position {position} in playlist {playlistId}")
    {
        PlaylistId = playlistId;
        Position = position;
    }
}
```

### 6. Add Endpoints

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/PlaylistEndpoints.cs`

```csharp
group.MapPost("/{playlistId}/tracks", HandleAddTracks)
    .WithName("AddTracksToPlaylist")
    .WithSummary("Add tracks to a playlist")
    .Produces<PlaylistDetails>(StatusCodes.Status200OK)
    .ProducesProblem(StatusCodes.Status400BadRequest)
    .ProducesProblem(StatusCodes.Status403Forbidden)
    .ProducesProblem(StatusCodes.Status404NotFound)
    .RequireRateLimiting("playlist-tracks-add");

group.MapDelete("/{playlistId}/tracks/{position:int}", HandleRemoveTrack)
    .WithName("RemoveTrackFromPlaylist")
    .WithSummary("Remove a track from a playlist by position")
    .Produces(StatusCodes.Status204NoContent)
    .ProducesProblem(StatusCodes.Status404NotFound)
    .RequireRateLimiting("playlist-tracks-remove");

private static async Task<IResult> HandleAddTracks(
    [FromRoute] string playlistId,
    [FromBody] AddTracksRequest request,
    [FromServices] IPlaylistService playlistService,
    [FromServices] IValidator<AddTracksRequest> validator,
    ClaimsPrincipal user,
    CancellationToken ct)
{
    if (!Ulid.TryParse(playlistId, out _))
    {
        return Results.Problem(
            title: "Invalid playlist ID",
            detail: "Playlist ID must be a valid ULID.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-playlist-id");
    }

    var validationResult = await validator.ValidateAsync(request, ct);
    if (!validationResult.IsValid)
    {
        return Results.ValidationProblem(validationResult.ToDictionary());
    }

    var userId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    try
    {
        var playlist = await playlistService.AddTracksAsync(
            playlistId, userId, request, ct);
        return Results.Ok(playlist);
    }
    catch (PlaylistNotFoundException)
    {
        return Results.Problem(
            title: "Playlist not found",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/playlist-not-found");
    }
    catch (PlaylistAccessDeniedException)
    {
        return Results.Problem(
            title: "Access denied",
            statusCode: StatusCodes.Status403Forbidden,
            type: "https://novatune.dev/errors/forbidden");
    }
    catch (TrackNotFoundException ex)
    {
        return Results.Problem(
            title: "Track not found",
            detail: $"Track {ex.Message} was not found.",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/track-not-found");
    }
    catch (TrackAccessDeniedException ex)
    {
        return Results.Problem(
            title: "Track access denied",
            detail: $"You do not have access to track {ex.Message}.",
            statusCode: StatusCodes.Status403Forbidden,
            type: "https://novatune.dev/errors/track-forbidden");
    }
    catch (TrackDeletedException ex)
    {
        return Results.Problem(
            title: "Track is deleted",
            detail: $"Track {ex.Message} has been deleted and cannot be added to playlists.",
            statusCode: StatusCodes.Status409Conflict,
            type: "https://novatune.dev/errors/track-deleted");
    }
    catch (PlaylistTrackLimitExceededException ex)
    {
        return Results.Problem(
            title: "Track limit exceeded",
            detail: ex.Message,
            statusCode: StatusCodes.Status403Forbidden,
            type: "https://novatune.dev/errors/playlist-track-limit-exceeded",
            extensions: new Dictionary<string, object?>
            {
                ["currentCount"] = ex.CurrentCount,
                ["addCount"] = ex.AddCount,
                ["maxCount"] = ex.MaxCount
            });
    }
    catch (InvalidPositionException ex)
    {
        return Results.Problem(
            title: "Invalid position",
            detail: ex.Message,
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-position");
    }
}

private static async Task<IResult> HandleRemoveTrack(
    [FromRoute] string playlistId,
    [FromRoute] int position,
    [FromServices] IPlaylistService playlistService,
    ClaimsPrincipal user,
    CancellationToken ct)
{
    if (!Ulid.TryParse(playlistId, out _))
    {
        return Results.Problem(
            title: "Invalid playlist ID",
            detail: "Playlist ID must be a valid ULID.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-playlist-id");
    }

    if (position < 0)
    {
        return Results.Problem(
            title: "Invalid position",
            detail: "Position must be non-negative.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-position");
    }

    var userId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    try
    {
        await playlistService.RemoveTrackAsync(playlistId, userId, position, ct);
        return Results.NoContent();
    }
    catch (PlaylistNotFoundException)
    {
        return Results.Problem(
            title: "Playlist not found",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/playlist-not-found");
    }
    catch (PlaylistAccessDeniedException)
    {
        return Results.Problem(
            title: "Access denied",
            statusCode: StatusCodes.Status403Forbidden,
            type: "https://novatune.dev/errors/forbidden");
    }
    catch (PlaylistTrackNotFoundException ex)
    {
        return Results.Problem(
            title: "Track not found in playlist",
            detail: $"No track at position {ex.Position}.",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/track-not-in-playlist");
    }
}
```

## Request/Response Examples

### Add Tracks Request

```json
POST /playlists/01HXK.../tracks
{
  "trackIds": ["01HXL...", "01HXM...", "01HXN..."],
  "position": 5
}
```

### Add Tracks Response (200 OK)

```json
{
  "playlistId": "01HXK...",
  "name": "My Playlist",
  "trackCount": 25,
  "totalDuration": "PT1H30M",
  "updatedAt": "2025-01-08T12:00:00Z"
}
```

### Remove Track Request

```
DELETE /playlists/01HXK.../tracks/5
```

### Remove Track Response

```
204 No Content
```

## Validation Rules

### Adding Tracks

| Rule | Error |
|------|-------|
| TrackIds not empty | 400 Bad Request |
| Max 100 tracks per request | 400 Bad Request |
| All track IDs valid ULIDs | 400 Bad Request |
| All tracks exist | 404 Not Found |
| All tracks owned by user | 403 Forbidden |
| No tracks with Deleted status | 409 Conflict |
| Position in valid range | 400 Bad Request |
| Won't exceed 10,000 track limit | 403 Forbidden |

### Removing Tracks

| Rule | Error |
|------|-------|
| Position >= 0 | 400 Bad Request |
| Track exists at position | 404 Not Found |
| Playlist exists | 404 Not Found |
| User owns playlist | 403 Forbidden |

## Duplicates Policy

Per requirements (Req 7 clarifications), **duplicates are allowed**. The same track can appear multiple times in a playlist at different positions.

## Position Management

Positions are 0-based and contiguous:
- `[0, 1, 2, 3, 4]` - Valid
- `[0, 1, 3, 4]` - Invalid (gap at position 2)

After any add/remove operation, positions are automatically reindexed to maintain contiguity.

## Stage 6 Documentation

- **Add Tracks API**: `doc/implementation/stage-6/07-api-add-tracks.md`
- **Remove Track API**: `doc/implementation/stage-6/08-api-remove-track.md`
- **Service Interface**: `doc/implementation/stage-6/10-service-interface.md`
- **Test Strategy**: `doc/implementation/stage-6/18-test-strategy.md`

## Related Skills

- **implement-playlists** - Full playlist implementation plan
- **add-playlist-reordering** - Track reordering operations
- **add-api-endpoint** - Minimal API endpoint structure
