---
description: Plan and implement Stage 6 Playlists with CRUD endpoints, track management, and reordering (plan)
---
# Implement Playlists Skill

Plan and implement Stage 6 Playlists for NovaTune: CRUD endpoints, track management, stable ordering, and lifecycle integration.

## Overview

Stage 6 implements playlist management with:
- **GET /playlists** - List playlists with search and cursor-based pagination
- **POST /playlists** - Create playlist with quota enforcement
- **GET /playlists/{playlistId}** - Get playlist with paginated tracks
- **PATCH /playlists/{playlistId}** - Update playlist metadata
- **DELETE /playlists/{playlistId}** - Hard delete playlist
- **POST /playlists/{playlistId}/tracks** - Add tracks at position
- **DELETE /playlists/{playlistId}/tracks/{position}** - Remove track
- **POST /playlists/{playlistId}/reorder** - Reorder tracks

## Implementation Plan

### Phase 1: Models and Configuration

1. **Create Playlist Model** (`ApiService/Models/Playlist.cs`)
   - `PlaylistId` (ULID)
   - `UserId` (owner)
   - `Name`, `Description`
   - `Tracks` (embedded `List<PlaylistTrackEntry>`)
   - `TrackCount`, `TotalDuration` (denormalized)
   - `Visibility` enum (Private, Unlisted, Public)
   - `CreatedAt`, `UpdatedAt`

2. **Create PlaylistTrackEntry** (`ApiService/Models/PlaylistTrackEntry.cs`)
   - `Position` (0-based index)
   - `TrackId` (ULID reference)
   - `AddedAt`

3. **Add Configuration** (`ApiService/Configuration/PlaylistOptions.cs`)
   - `MaxPlaylistsPerUser` (default: 200)
   - `MaxTracksPerPlaylist` (default: 10,000)
   - `MaxTracksPerAddRequest` (default: 100)
   - `MaxMovesPerReorderRequest` (default: 50)
   - `MaxNameLength` (default: 100)
   - `MaxDescriptionLength` (default: 500)
   - `DefaultPageSize` (default: 20)
   - `MaxPageSize` (default: 50)

4. **Add DTOs** (`ApiService/Models/`)
   - `PlaylistListQuery`, `PlaylistDetailQuery`
   - `PlaylistListItem`, `PlaylistDetails`, `PlaylistTrackItem`
   - `CreatePlaylistRequest`, `UpdatePlaylistRequest`
   - `AddTracksRequest`, `ReorderRequest`, `MoveOperation`

### Phase 2: RavenDB Indexes

1. **Playlists_ByUserForSearch** (`ApiService/Infrastructure/Indexes/`)
   ```csharp
   Map = playlists => from playlist in playlists
                      select new
                      {
                          playlist.UserId,
                          playlist.Name,
                          playlist.TrackCount,
                          playlist.CreatedAt,
                          playlist.UpdatedAt,
                          SearchText = playlist.Name
                      };
   Index("SearchText", FieldIndexing.Search);
   ```

2. **Playlists_ByTrackReference** (`ApiService/Infrastructure/Indexes/`)
   ```csharp
   Map = playlists => from playlist in playlists
                      from track in playlist.Tracks
                      select new
                      {
                          UserId = playlist.UserId,
                          PlaylistId = playlist.PlaylistId,
                          TrackId = track.TrackId
                      };
   ```

### Phase 3: Service Layer

1. **IPlaylistService** (`ApiService/Services/`)
   - `ListPlaylistsAsync(userId, query, ct)`
   - `CreatePlaylistAsync(userId, request, ct)`
   - `GetPlaylistAsync(playlistId, userId, query, ct)`
   - `UpdatePlaylistAsync(playlistId, userId, request, ct)`
   - `DeletePlaylistAsync(playlistId, userId, ct)`
   - `AddTracksAsync(playlistId, userId, request, ct)`
   - `RemoveTrackAsync(playlistId, userId, position, ct)`
   - `ReorderTracksAsync(playlistId, userId, request, ct)`
   - `RemoveDeletedTrackReferencesAsync(trackId, userId, ct)`

2. **Custom Exceptions** (`ApiService/Infrastructure/Exceptions/`)
   - `PlaylistNotFoundException`
   - `PlaylistAccessDeniedException`
   - `PlaylistQuotaExceededException`
   - `PlaylistTrackLimitExceededException`
   - `PlaylistTrackNotFoundException`
   - `InvalidPositionException`

### Phase 4: API Endpoints

1. **PlaylistEndpoints.cs** (`ApiService/Endpoints/`)
   ```csharp
   group.MapGet("/", HandleListPlaylists).RequireRateLimiting("playlist-list");
   group.MapPost("/", HandleCreatePlaylist).RequireRateLimiting("playlist-create");
   group.MapGet("/{playlistId}", HandleGetPlaylist);
   group.MapPatch("/{playlistId}", HandleUpdatePlaylist).RequireRateLimiting("playlist-update");
   group.MapDelete("/{playlistId}", HandleDeletePlaylist).RequireRateLimiting("playlist-delete");
   group.MapPost("/{playlistId}/tracks", HandleAddTracks).RequireRateLimiting("playlist-tracks-add");
   group.MapDelete("/{playlistId}/tracks/{position:int}", HandleRemoveTrack).RequireRateLimiting("playlist-tracks-remove");
   group.MapPost("/{playlistId}/reorder", HandleReorderTracks).RequireRateLimiting("playlist-reorder");
   ```

2. **Rate Limiting Policies**
   - `playlist-list`: 60 req/min
   - `playlist-create`: 20 req/min
   - `playlist-update`: 30 req/min
   - `playlist-delete`: 20 req/min
   - `playlist-tracks-add`: 30 req/min
   - `playlist-tracks-remove`: 60 req/min
   - `playlist-reorder`: 30 req/min

### Phase 5: Track Validation

When adding tracks to playlists:
1. Verify track IDs are valid ULIDs
2. Verify tracks exist in RavenDB
3. Verify tracks are owned by the same user
4. Verify tracks are not deleted (`Status != Deleted`)
5. Verify playlist track limit not exceeded

```csharp
var trackDocs = await _session.LoadAsync<Track>(
    request.TrackIds.Select(id => $"Tracks/{id}"), ct);

foreach (var (trackId, track) in trackDocs)
{
    if (track is null)
        throw new TrackNotFoundException(trackId);
    if (track.UserId != userId)
        throw new TrackAccessDeniedException(trackId);
    if (track.Status == TrackStatus.Deleted)
        throw new TrackDeletedException(trackId);
}
```

### Phase 6: Position Management

**Adding tracks:**
```csharp
var insertPosition = request.Position ?? playlist.Tracks.Count;

// Shift existing tracks
foreach (var entry in playlist.Tracks.Where(t => t.Position >= insertPosition))
    entry.Position += request.TrackIds.Count;

// Add new tracks
var newEntries = request.TrackIds.Select((id, i) => new PlaylistTrackEntry
{
    Position = insertPosition + i,
    TrackId = id,
    AddedAt = now
});
playlist.Tracks.AddRange(newEntries);
```

**Removing tracks:**
```csharp
playlist.Tracks.Remove(trackToRemove);

// Reindex positions
foreach (var entry in playlist.Tracks.Where(t => t.Position > position))
    entry.Position--;
```

**Reordering tracks:**
```csharp
foreach (var move in request.Moves)
{
    var track = tracks[move.From];
    tracks.RemoveAt(move.From);
    tracks.Insert(move.To, track);
}

// Reassign positions
for (var i = 0; i < tracks.Count; i++)
    tracks[i].Position = i;
```

### Phase 7: Lifecycle Integration

Extend lifecycle worker to clean up playlist references when tracks are physically deleted:

1. Query `Playlists_ByTrackReference` index to find affected playlists
2. Remove all entries for the deleted track
3. Reindex positions
4. Update denormalized `TrackCount` and `TotalDuration`

### Phase 8: Observability

1. **Metrics** (`ApiService/Infrastructure/Observability/`)
   - `playlist_list_requests_total`
   - `playlist_create_requests_total`
   - `playlist_get_requests_total`
   - `playlist_update_requests_total`
   - `playlist_delete_requests_total`
   - `playlist_tracks_add_requests_total`
   - `playlist_tracks_remove_requests_total`
   - `playlist_reorder_requests_total`
   - `playlist_track_count` (histogram)

2. **Logging**
   - Playlist operations with `PlaylistId`, `UserId`, `CorrelationId`
   - Track additions/removals with count and position

### Phase 9: Testing

1. **Unit Tests**
   - `PlaylistServiceTests`
   - Position reindexing logic
   - Quota enforcement
   - Track validation

2. **Integration Tests**
   - End-to-end CRUD flow
   - Add/remove/reorder tracks
   - Track deletion cascade to playlists
   - Concurrent modification handling

## Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `ApiService/Models/Playlist.cs` | Playlist document model |
| `ApiService/Models/PlaylistTrackEntry.cs` | Embedded track entry |
| `ApiService/Models/PlaylistVisibility.cs` | Visibility enum |
| `ApiService/Configuration/PlaylistOptions.cs` | Configuration |
| `ApiService/Services/IPlaylistService.cs` | Service interface |
| `ApiService/Services/PlaylistService.cs` | Service implementation |
| `ApiService/Endpoints/PlaylistEndpoints.cs` | API endpoints |
| `ApiService/Models/PlaylistListQuery.cs` | Query models |
| `ApiService/Models/PlaylistDetails.cs` | Response DTOs |
| `ApiService/Infrastructure/Indexes/Playlists_ByUserForSearch.cs` | Search index |
| `ApiService/Infrastructure/Indexes/Playlists_ByTrackReference.cs` | Track reference index |
| `ApiService/Infrastructure/Exceptions/PlaylistExceptions.cs` | Custom exceptions |

### Modified Files

| File | Changes |
|------|---------|
| `ApiService/Program.cs` | Register services, rate limiting |
| `Workers.Lifecycle/PhysicalDeletionService.cs` | Add playlist cleanup |

## Stage 6 Documentation

Detailed specifications are available in `doc/implementation/stage-6/`:

| Document | Description |
|----------|-------------|
| `00-overview.md` | Architecture diagram and index |
| `01-data-model.md` | Playlist and PlaylistTrackEntry models |
| `02-api-list-playlists.md` | GET /playlists endpoint |
| `03-api-create-playlist.md` | POST /playlists endpoint |
| `04-api-get-playlist.md` | GET /playlists/{id} endpoint |
| `05-api-update-playlist.md` | PATCH /playlists/{id} endpoint |
| `06-api-delete-playlist.md` | DELETE /playlists/{id} endpoint |
| `07-api-add-tracks.md` | POST /playlists/{id}/tracks endpoint |
| `08-api-remove-track.md` | DELETE /playlists/{id}/tracks/{pos} endpoint |
| `09-api-reorder-tracks.md` | POST /playlists/{id}/reorder endpoint |
| `10-service-interface.md` | IPlaylistService and DTOs |
| `11-ravendb-indexes.md` | Search and track reference indexes |
| `12-track-deletion-integration.md` | Lifecycle worker integration |
| `13-configuration.md` | PlaylistOptions configuration |
| `14-endpoint-implementation.md` | PlaylistEndpoints.cs structure |
| `18-test-strategy.md` | Unit and integration test plan |
| `19-implementation-tasks.md` | Implementation checklist |

## Related Skills

- **add-api-endpoint** - For endpoint structure
- **add-cursor-pagination** - For playlist list pagination
- **add-ravendb-index** - For creating RavenDB indexes
- **add-rate-limiting** - For rate limiting policies
- **add-observability** - For metrics and tracing
- **add-playlist-reordering** - For reorder implementation
- **add-playlist-tracks** - For track add/remove

## Claude Agents

- **playlist-api-implementer** - Implement playlist service, endpoints, and models
- **playlist-tester** - Write unit and integration tests for playlists

## Validation Checklist

- [ ] All CRUD endpoints return RFC 7807 problem details on error
- [ ] Rate limiting enforced on all mutation endpoints
- [ ] Playlist quota enforced (200 per user)
- [ ] Track limit enforced (10,000 per playlist)
- [ ] Track ownership verified before adding to playlist
- [ ] Deleted tracks not allowed in playlists
- [ ] Position indices maintained correctly
- [ ] Denormalized fields updated atomically
- [ ] Optimistic concurrency on updates
- [ ] Lifecycle worker removes deleted track references
- [ ] All operations logged with correlation ID
