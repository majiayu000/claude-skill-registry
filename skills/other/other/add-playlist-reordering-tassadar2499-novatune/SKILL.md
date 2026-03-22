---
description: Implement playlist track reordering with move operations and position management (project)
---
# Add Playlist Reordering Skill

Implement track reordering within playlists using move operations with stable position management.

## Overview

Playlist reordering allows users to change the order of tracks via move operations. Each move specifies a source position and target position.

## Steps

### 1. Create Move Operation Model

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Playlists/`

```csharp
namespace NovaTuneApp.ApiService.Models.Playlists;

/// <summary>
/// Represents a single move operation in a reorder request.
/// </summary>
/// <param name="From">Current position of the track (0-based)</param>
/// <param name="To">Target position for the track (0-based)</param>
public record MoveOperation(int From, int To);

/// <summary>
/// Request to reorder tracks within a playlist.
/// </summary>
/// <param name="Moves">List of move operations (applied sequentially)</param>
public record ReorderRequest(IReadOnlyList<MoveOperation> Moves);
```

### 2. Add Validation

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Validators/`

```csharp
using FluentValidation;

namespace NovaTuneApp.ApiService.Validators;

public class ReorderRequestValidator : AbstractValidator<ReorderRequest>
{
    public ReorderRequestValidator(IOptions<PlaylistOptions> options)
    {
        RuleFor(x => x.Moves)
            .NotEmpty()
            .WithMessage("At least one move operation is required")
            .Must(m => m.Count <= options.Value.MaxMovesPerReorderRequest)
            .WithMessage($"Maximum {options.Value.MaxMovesPerReorderRequest} moves per request");

        RuleForEach(x => x.Moves)
            .ChildRules(move =>
            {
                move.RuleFor(m => m.From)
                    .GreaterThanOrEqualTo(0)
                    .WithMessage("From position must be non-negative");

                move.RuleFor(m => m.To)
                    .GreaterThanOrEqualTo(0)
                    .WithMessage("To position must be non-negative");
            });
    }
}
```

### 3. Implement Reorder Logic in Service

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/PlaylistService.cs`

```csharp
public async Task<PlaylistDetails> ReorderTracksAsync(
    string playlistId,
    string userId,
    ReorderRequest request,
    CancellationToken ct = default)
{
    var playlist = await _session.LoadAsync<Playlist>($"Playlists/{playlistId}", ct);

    if (playlist is null)
        throw new PlaylistNotFoundException(playlistId);

    if (playlist.UserId != userId)
        throw new PlaylistAccessDeniedException(playlistId);

    if (playlist.Tracks.Count == 0)
        throw new InvalidOperationException("Cannot reorder empty playlist");

    // Validate all positions before applying any moves
    foreach (var move in request.Moves)
    {
        if (move.From < 0 || move.From >= playlist.Tracks.Count)
            throw new InvalidPositionException(move.From, playlist.Tracks.Count);

        if (move.To < 0 || move.To >= playlist.Tracks.Count)
            throw new InvalidPositionException(move.To, playlist.Tracks.Count);
    }

    // Sort tracks by position to work with a proper list
    var tracks = playlist.Tracks.OrderBy(t => t.Position).ToList();

    // Apply moves sequentially
    foreach (var move in request.Moves)
    {
        if (move.From == move.To)
            continue; // No-op move

        var track = tracks[move.From];
        tracks.RemoveAt(move.From);
        tracks.Insert(move.To, track);
    }

    // Reassign positions to maintain contiguous 0-based indices
    for (var i = 0; i < tracks.Count; i++)
    {
        tracks[i].Position = i;
    }

    playlist.Tracks = tracks;
    playlist.UpdatedAt = DateTimeOffset.UtcNow;

    await _session.SaveChangesAsync(ct);

    _logger.LogInformation(
        "Reordered {MoveCount} tracks in playlist {PlaylistId} for user {UserId}",
        request.Moves.Count, playlistId, userId);

    return await MapToDetailsAsync(playlist, ct);
}
```

### 4. Create Custom Exception

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Exceptions/`

```csharp
namespace NovaTuneApp.ApiService.Infrastructure.Exceptions;

/// <summary>
/// Thrown when a position is out of valid range.
/// </summary>
public class InvalidPositionException : Exception
{
    public int Position { get; }
    public int MaxPosition { get; }

    public InvalidPositionException(int position, int trackCount)
        : base($"Position {position} is out of range. Valid range: 0 to {trackCount - 1}")
    {
        Position = position;
        MaxPosition = trackCount - 1;
    }
}
```

### 5. Add Endpoint

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/PlaylistEndpoints.cs`

```csharp
group.MapPost("/{playlistId}/reorder", HandleReorderTracks)
    .WithName("ReorderPlaylistTracks")
    .WithSummary("Reorder tracks within a playlist")
    .Produces<PlaylistDetails>(StatusCodes.Status200OK)
    .ProducesProblem(StatusCodes.Status400BadRequest)
    .ProducesProblem(StatusCodes.Status404NotFound)
    .ProducesProblem(StatusCodes.Status409Conflict)
    .RequireRateLimiting("playlist-reorder");

private static async Task<IResult> HandleReorderTracks(
    [FromRoute] string playlistId,
    [FromBody] ReorderRequest request,
    [FromServices] IPlaylistService playlistService,
    [FromServices] IValidator<ReorderRequest> validator,
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
        var playlist = await playlistService.ReorderTracksAsync(
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
    catch (InvalidPositionException ex)
    {
        return Results.Problem(
            title: "Invalid position",
            detail: ex.Message,
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-position",
            extensions: new Dictionary<string, object?>
            {
                ["position"] = ex.Position,
                ["maxPosition"] = ex.MaxPosition
            });
    }
    catch (ConcurrencyException)
    {
        return Results.Problem(
            title: "Concurrent modification",
            detail: "The playlist was modified by another request. Please retry.",
            statusCode: StatusCodes.Status409Conflict,
            type: "https://novatune.dev/errors/concurrency-conflict");
    }
}
```

## Request/Response Examples

### Request

```json
POST /playlists/01HXK.../reorder
{
  "moves": [
    { "from": 5, "to": 0 },
    { "from": 10, "to": 3 }
  ]
}
```

### Response (200 OK)

```json
{
  "playlistId": "01HXK...",
  "name": "My Playlist",
  "trackCount": 20,
  "tracks": {
    "items": [
      { "position": 0, "trackId": "01HXL...", "title": "Moved Track" },
      { "position": 1, "trackId": "01HXM...", "title": "Second Track" }
    ],
    "hasMore": true
  }
}
```

### Error Response (400 Bad Request)

```json
{
  "type": "https://novatune.dev/errors/invalid-position",
  "title": "Invalid position",
  "status": 400,
  "detail": "Position 25 is out of range. Valid range: 0 to 19",
  "position": 25,
  "maxPosition": 19
}
```

## Move Semantics

Moves are applied **sequentially**, which means:

1. **Move A from 5 to 0**: Track at position 5 becomes position 0, others shift
2. **Move B from 10 to 3**: Applied to the **new** state after Move A

This allows complex reorderings with predictable results.

### Example: Moving track from end to beginning

Before: `[A, B, C, D, E]` (positions 0-4)
Move: `{ "from": 4, "to": 0 }`
After: `[E, A, B, C, D]` (positions 0-4)

### Example: Swapping two tracks

Before: `[A, B, C, D, E]`
Moves: `[{ "from": 0, "to": 4 }, { "from": 4, "to": 0 }]`
After Move 1: `[B, C, D, E, A]`
After Move 2: `[A, B, C, D, E]` (back to original - this is NOT a swap)

For a true swap, use: `[{ "from": 0, "to": 4 }, { "from": 3, "to": 0 }]`

## Alternative: Single Move Endpoint

For simpler UX, consider also exposing a single-move endpoint:

```csharp
group.MapPost("/{playlistId}/tracks/{position:int}/move", HandleMoveTrack)
    .WithName("MovePlaylistTrack")
    .WithSummary("Move a single track to a new position");
```

Request: `POST /playlists/01HXK.../tracks/5/move?to=0`

## Validation Rules

| Rule | Error |
|------|-------|
| Moves array not empty | 400 Bad Request |
| Max 50 moves per request | 400 Bad Request |
| From position in valid range | 400 Bad Request |
| To position in valid range | 400 Bad Request |
| Playlist exists | 404 Not Found |
| User owns playlist | 403 Forbidden |

## Performance Considerations

- **Embedded list**: Track entries are embedded in the playlist document, so reordering is atomic
- **Position reindexing**: O(n) operation where n = track count
- **Optimistic concurrency**: Use RavenDB etag to detect concurrent modifications
- **Max moves limit**: Prevents abuse and excessive computation

## Stage 6 Documentation

- **Reorder API**: `doc/implementation/stage-6/09-api-reorder-tracks.md`
- **Service Interface**: `doc/implementation/stage-6/10-service-interface.md`
- **Test Strategy**: `doc/implementation/stage-6/18-test-strategy.md`

## Related Skills

- **implement-playlists** - Full playlist implementation plan
- **add-playlist-tracks** - Track add/remove operations
- **add-api-endpoint** - Minimal API endpoint structure
