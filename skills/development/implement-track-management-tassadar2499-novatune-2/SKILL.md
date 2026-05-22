---
description: Plan and implement Stage 5 Track Management with CRUD endpoints, soft-delete, and lifecycle worker (plan)
---
# Implement Track Management Skill

Plan and implement Stage 5 Track Management for NovaTune: CRUD endpoints, soft-delete semantics, lifecycle worker, and observability.

## Overview

Stage 5 implements user library management with:
- **GET /tracks** - List tracks with search, filter, sort, cursor-based pagination
- **GET /tracks/{trackId}** - Get track details
- **PATCH /tracks/{trackId}** - Update track metadata (merge policy)
- **DELETE /tracks/{trackId}** - Soft-delete with grace period
- **POST /tracks/{trackId}/restore** - Restore within grace period
- **Lifecycle Worker** - Physical deletion after grace period

## Implementation Plan

### Phase 1: Models and Configuration

1. **Extend Track Model** (`ApiService/Models/Track.cs`)
   - Add soft-delete fields: `DeletedAt`, `ScheduledDeletionAt`, `StatusBeforeDeletion`

2. **Add Configuration** (`ApiService/Configuration/TrackManagementOptions.cs`)
   - `DeletionGracePeriod` (default: 30 days)
   - `MaxPageSize` (default: 100)
   - `DefaultPageSize` (default: 20)

3. **Add DTOs** (`ApiService/Models/`)
   - `TrackListQuery`, `TrackListQueryParams`
   - `TrackListItem`, `TrackDetails`
   - `UpdateTrackRequest`
   - `PagedResult<T>`, `TrackListCursor`

### Phase 2: RavenDB Indexes

1. **Tracks_ByUserForSearch** (`ApiService/Infrastructure/Indexes/`)
   ```csharp
   Map = tracks => from track in tracks
                   where track.Status != TrackStatus.Unknown
                   select new
                   {
                       track.UserId,
                       track.Status,
                       track.Title,
                       track.Artist,
                       track.CreatedAt,
                       track.UpdatedAt,
                       track.Duration,
                       SearchText = new[] { track.Title, track.Artist }
                   };
   Index("SearchText", FieldIndexing.Search);
   ```

2. **Tracks_ByScheduledDeletion** (`ApiService/Infrastructure/Indexes/`)
   ```csharp
   Map = tracks => from track in tracks
                   where track.Status == TrackStatus.Deleted
                      && track.ScheduledDeletionAt != null
                   select new { track.Status, track.ScheduledDeletionAt };
   ```

### Phase 3: Service Layer

1. **ITrackManagementService** (`ApiService/Services/`)
   - `ListTracksAsync(userId, query, ct)`
   - `GetTrackAsync(trackId, userId, ct)`
   - `UpdateTrackAsync(trackId, userId, request, ct)`
   - `DeleteTrackAsync(trackId, userId, ct)`
   - `RestoreTrackAsync(trackId, userId, ct)`

2. **Custom Exceptions** (`ApiService/Infrastructure/Exceptions/`)
   - `TrackNotFoundException`
   - `TrackAccessDeniedException`
   - `TrackDeletedException`
   - `RestorationExpiredException`

### Phase 4: API Endpoints

1. **TrackEndpoints.cs** (`ApiService/Endpoints/`)
   ```csharp
   group.MapGet("/", HandleListTracks).RequireRateLimiting("track-list");
   group.MapGet("/{trackId}", HandleGetTrack);
   group.MapPatch("/{trackId}", HandleUpdateTrack).RequireRateLimiting("track-update");
   group.MapDelete("/{trackId}", HandleDeleteTrack).RequireRateLimiting("track-delete");
   group.MapPost("/{trackId}/restore", HandleRestoreTrack);
   ```

2. **Rate Limiting Policies**
   - `track-list`: 60 req/min
   - `track-update`: 30 req/min
   - `track-delete`: 10 req/min

### Phase 5: Event Publishing

1. **TrackDeletedEvent** (`ApiService/Infrastructure/Messaging/Messages/`)
   - Migrate from Guid to ULID strings
   - Include `ObjectKey`, `WaveformObjectKey`, `FileSizeBytes`

2. **Outbox Pattern**
   - Write event to `OutboxMessages` collection in same transaction
   - Outbox processor publishes to `{prefix}-track-deletions` topic

### Phase 6: Lifecycle Worker

1. **Create Worker Project** (`Workers.Lifecycle/`)
   - Use `add-aspire-worker-project` skill

2. **TrackDeletedHandler** - Kafka consumer for immediate cache invalidation

3. **PhysicalDeletionService** - Background service polling for expired tracks
   - Delete MinIO objects (audio + waveform)
   - Delete RavenDB document
   - Update user quota

### Phase 7: Observability

1. **Metrics** (`ApiService/Infrastructure/Observability/`)
   - `track_list_requests_total`
   - `track_get_requests_total`
   - `track_update_requests_total`
   - `track_delete_requests_total`
   - `track_physical_deletions_total`

2. **Logging**
   - Track operations with `TrackId`, `UserId`, `CorrelationId`
   - Never log object keys in production

### Phase 8: Testing

1. **Unit Tests**
   - `TrackManagementServiceTests`
   - Pagination cursor encoding/decoding
   - Soft-delete state transitions

2. **Integration Tests**
   - End-to-end CRUD flow
   - Soft-delete → restore → delete cycle
   - Physical deletion via lifecycle worker

## Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `ApiService/Configuration/TrackManagementOptions.cs` | Configuration |
| `ApiService/Services/ITrackManagementService.cs` | Service interface |
| `ApiService/Services/TrackManagementService.cs` | Service implementation |
| `ApiService/Endpoints/TrackEndpoints.cs` | API endpoints |
| `ApiService/Models/TrackListQuery.cs` | Query model |
| `ApiService/Models/PagedResult.cs` | Pagination result |
| `ApiService/Infrastructure/Indexes/Tracks_ByUserForSearch.cs` | Search index |
| `ApiService/Infrastructure/Indexes/Tracks_ByScheduledDeletion.cs` | Deletion index |
| `ApiService/Infrastructure/Exceptions/TrackExceptions.cs` | Custom exceptions |
| `Workers.Lifecycle/` | New worker project |

### Modified Files

| File | Changes |
|------|---------|
| `ApiService/Models/Track.cs` | Add soft-delete fields |
| `ApiService/Program.cs` | Register services, rate limiting |
| `AppHost/AppHost.cs` | Add lifecycle worker |

## Related Skills

- **add-ravendb-index** - For creating RavenDB indexes
- **add-rate-limiting** - For rate limiting policies
- **add-background-service** - For physical deletion service
- **add-kafka-consumer** - For TrackDeletedHandler
- **add-aspire-worker-project** - For lifecycle worker project
- **add-observability** - For metrics and tracing

## Validation Checklist

- [ ] All CRUD endpoints return RFC 7807 problem details on error
- [ ] Rate limiting enforced on mutation endpoints
- [ ] Soft-delete preserves `StatusBeforeDeletion` for restore
- [ ] Physical deletion only after grace period
- [ ] Cache invalidated immediately on soft-delete
- [ ] Quota updated only after physical deletion
- [ ] All operations logged with correlation ID
- [ ] Optimistic concurrency on updates
