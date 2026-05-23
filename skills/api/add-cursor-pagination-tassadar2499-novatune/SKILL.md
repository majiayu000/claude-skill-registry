---
description: Add cursor-based pagination for list endpoints with stable ordering (project)
---
# Add Cursor-Based Pagination Skill

Implement cursor-based pagination for list endpoints in NovaTune, providing stable results during data changes.

## Overview

Cursor-based pagination advantages:
- **Stable results**: Works correctly when items are added/deleted during navigation
- **Efficient queries**: Uses indexed seek instead of offset skip
- **Scalable**: Performance doesn't degrade with large offsets

## Steps

### 1. Create Cursor Model

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Pagination/`

```csharp
using System.Text;
using System.Text.Json;

namespace NovaTuneApp.ApiService.Models.Pagination;

/// <summary>
/// Cursor for stable pagination through sorted results.
/// </summary>
/// <param name="SortValue">Value of the sort field at cursor position</param>
/// <param name="Id">ULID for tie-breaking (provides chronological ordering)</param>
/// <param name="Timestamp">When cursor was created (for expiry)</param>
public record PaginationCursor(
    string SortValue,
    string Id,
    DateTimeOffset Timestamp)
{
    /// <summary>
    /// Encodes cursor as base64 URL-safe string.
    /// </summary>
    public string Encode()
    {
        var json = JsonSerializer.Serialize(this);
        var bytes = Encoding.UTF8.GetBytes(json);
        return Convert.ToBase64String(bytes)
            .Replace('+', '-')
            .Replace('/', '_')
            .TrimEnd('=');
    }

    /// <summary>
    /// Decodes cursor from base64 URL-safe string.
    /// </summary>
    public static PaginationCursor? Decode(string? encoded)
    {
        if (string.IsNullOrEmpty(encoded))
            return null;

        try
        {
            // Restore base64 padding
            var padded = encoded
                .Replace('-', '+')
                .Replace('_', '/');

            switch (padded.Length % 4)
            {
                case 2: padded += "=="; break;
                case 3: padded += "="; break;
            }

            var bytes = Convert.FromBase64String(padded);
            var json = Encoding.UTF8.GetString(bytes);
            return JsonSerializer.Deserialize<PaginationCursor>(json);
        }
        catch
        {
            return null;
        }
    }

    /// <summary>
    /// Checks if cursor has expired.
    /// </summary>
    public bool IsExpired(TimeSpan maxAge) =>
        DateTimeOffset.UtcNow - Timestamp > maxAge;
}
```

### 2. Create Paged Result Model

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Pagination/PagedResult.cs`

```csharp
namespace NovaTuneApp.ApiService.Models.Pagination;

/// <summary>
/// Paginated result with cursor-based navigation.
/// </summary>
/// <typeparam name="T">Item type</typeparam>
/// <param name="Items">Items in current page</param>
/// <param name="NextCursor">Cursor for next page (null if no more pages)</param>
/// <param name="TotalCount">Approximate total count</param>
/// <param name="HasMore">Whether more items exist</param>
public record PagedResult<T>(
    IReadOnlyList<T> Items,
    string? NextCursor,
    int TotalCount,
    bool HasMore);
```

### 3. Create Query Parameters Model

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Pagination/PaginatedQueryParams.cs`

```csharp
using Microsoft.AspNetCore.Mvc;

namespace NovaTuneApp.ApiService.Models.Pagination;

/// <summary>
/// Base query parameters for paginated list endpoints.
/// </summary>
public record PaginatedQueryParams(
    [FromQuery] string? SortBy,
    [FromQuery] string? SortOrder,
    [FromQuery] string? Cursor,
    [FromQuery] int? Limit);

/// <summary>
/// Query parameters for track list endpoint.
/// </summary>
public record TrackListQueryParams(
    [FromQuery] string? Search,
    [FromQuery] TrackStatus? Status,
    [FromQuery] string? SortBy,
    [FromQuery] string? SortOrder,
    [FromQuery] string? Cursor,
    [FromQuery] int? Limit,
    [FromQuery] bool? IncludeDeleted) : PaginatedQueryParams(SortBy, SortOrder, Cursor, Limit);
```

### 4. Create Pagination Extension Methods

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Extensions/PaginationExtensions.cs`

```csharp
using System.Linq.Expressions;
using Raven.Client.Documents;
using Raven.Client.Documents.Linq;
using NovaTuneApp.ApiService.Models.Pagination;

namespace NovaTuneApp.ApiService.Extensions;

public static class PaginationExtensions
{
    /// <summary>
    /// Applies cursor-based pagination to a RavenDB query.
    /// </summary>
    /// <typeparam name="T">Entity type</typeparam>
    /// <param name="query">RavenDB query</param>
    /// <param name="cursor">Decoded cursor (null for first page)</param>
    /// <param name="sortField">Field to sort by</param>
    /// <param name="sortDescending">Sort direction</param>
    /// <param name="limit">Page size</param>
    /// <param name="getSortValue">Function to extract sort value from entity</param>
    /// <param name="getId">Function to extract ID from entity</param>
    public static async Task<PagedResult<TResult>> ToCursorPagedAsync<T, TResult>(
        this IRavenQueryable<T> query,
        PaginationCursor? cursor,
        Expression<Func<T, object>> sortField,
        bool sortDescending,
        int limit,
        Func<T, string> getSortValue,
        Func<T, string> getId,
        Func<T, TResult> mapper,
        CancellationToken ct = default)
    {
        // Apply cursor filter if present
        if (cursor is not null)
        {
            query = ApplyCursorFilter(query, cursor, sortField, sortDescending);
        }

        // Apply sorting
        query = sortDescending
            ? query.OrderByDescending(sortField).ThenByDescending(x => x)
            : query.OrderBy(sortField).ThenBy(x => x);

        // Fetch one extra to determine HasMore
        var items = await query
            .Take(limit + 1)
            .ToListAsync(ct);

        var hasMore = items.Count > limit;
        if (hasMore)
            items = items.Take(limit).ToList();

        // Build next cursor from last item
        string? nextCursor = null;
        if (hasMore && items.Count > 0)
        {
            var lastItem = items[^1];
            var newCursor = new PaginationCursor(
                getSortValue(lastItem),
                getId(lastItem),
                DateTimeOffset.UtcNow);
            nextCursor = newCursor.Encode();
        }

        // Get approximate total count (cached, not per-request)
        var totalCount = await query.CountAsync(ct);

        var results = items.Select(mapper).ToList();

        return new PagedResult<TResult>(
            results,
            nextCursor,
            totalCount,
            hasMore);
    }

    private static IRavenQueryable<T> ApplyCursorFilter<T>(
        IRavenQueryable<T> query,
        PaginationCursor cursor,
        Expression<Func<T, object>> sortField,
        bool sortDescending)
    {
        // This is a simplified example - actual implementation would need
        // to build the expression dynamically based on the sort field
        // For production, consider using a library like LinqKit or
        // building expressions manually

        // The filter logic:
        // For descending: (sortValue < cursorValue) OR (sortValue == cursorValue AND id < cursorId)
        // For ascending:  (sortValue > cursorValue) OR (sortValue == cursorValue AND id > cursorId)

        return query; // Placeholder - implement dynamic expression building
    }
}
```

### 5. Implement in Service Layer

Example for TrackManagementService:

```csharp
public async Task<PagedResult<TrackListItem>> ListTracksAsync(
    string userId,
    TrackListQuery query,
    CancellationToken ct = default)
{
    // Validate and constrain limit
    var limit = Math.Clamp(query.Limit, 1, _options.Value.MaxPageSize);

    // Decode cursor
    var cursor = PaginationCursor.Decode(query.Cursor);
    if (cursor?.IsExpired(TimeSpan.FromHours(24)) == true)
    {
        throw new InvalidCursorException("Cursor has expired");
    }

    // Build base query
    var baseQuery = _session
        .Query<Track, Tracks_ByUserForSearch>()
        .Where(t => t.UserId == userId);

    // Apply status filter
    if (query.Status.HasValue)
    {
        baseQuery = baseQuery.Where(t => t.Status == query.Status.Value);
    }
    else if (!query.IncludeDeleted)
    {
        baseQuery = baseQuery.Where(t => t.Status != TrackStatus.Deleted);
    }

    // Apply search filter
    if (!string.IsNullOrWhiteSpace(query.Search))
    {
        baseQuery = baseQuery.Search(t => t.Title, query.Search)
                            .Search(t => t.Artist, query.Search, SearchOptions.Or);
    }

    // Determine sort direction
    var sortDescending = query.SortOrder?.ToLowerInvariant() == "desc";

    // Apply cursor-based pagination
    return await ApplyCursorPagination(
        baseQuery, cursor, query.SortBy, sortDescending, limit, ct);
}

private async Task<PagedResult<TrackListItem>> ApplyCursorPagination(
    IRavenQueryable<Track> query,
    PaginationCursor? cursor,
    string sortBy,
    bool sortDescending,
    int limit,
    CancellationToken ct)
{
    // Apply cursor filter
    if (cursor is not null)
    {
        query = ApplyCursorCondition(query, cursor, sortBy, sortDescending);
    }

    // Apply sort
    query = sortBy?.ToLowerInvariant() switch
    {
        "title" => sortDescending
            ? query.OrderByDescending(t => t.Title).ThenByDescending(t => t.TrackId)
            : query.OrderBy(t => t.Title).ThenBy(t => t.TrackId),
        "artist" => sortDescending
            ? query.OrderByDescending(t => t.Artist).ThenByDescending(t => t.TrackId)
            : query.OrderBy(t => t.Artist).ThenBy(t => t.TrackId),
        "duration" => sortDescending
            ? query.OrderByDescending(t => t.Duration).ThenByDescending(t => t.TrackId)
            : query.OrderBy(t => t.Duration).ThenBy(t => t.TrackId),
        "updatedat" => sortDescending
            ? query.OrderByDescending(t => t.UpdatedAt).ThenByDescending(t => t.TrackId)
            : query.OrderBy(t => t.UpdatedAt).ThenBy(t => t.TrackId),
        _ => sortDescending
            ? query.OrderByDescending(t => t.CreatedAt).ThenByDescending(t => t.TrackId)
            : query.OrderBy(t => t.CreatedAt).ThenBy(t => t.TrackId)
    };

    // Fetch limit + 1 to check for more
    var items = await query.Take(limit + 1).ToListAsync(ct);
    var hasMore = items.Count > limit;

    if (hasMore)
        items = items.Take(limit).ToList();

    // Build next cursor
    string? nextCursor = null;
    if (hasMore && items.Count > 0)
    {
        var last = items[^1];
        var sortValue = GetSortValue(last, sortBy);
        nextCursor = new PaginationCursor(sortValue, last.TrackId, DateTimeOffset.UtcNow).Encode();
    }

    // Map to DTOs
    var results = items.Select(t => new TrackListItem(
        t.TrackId,
        t.Title,
        t.Artist,
        t.Duration,
        t.Status,
        t.FileSizeBytes,
        t.MimeType,
        t.CreatedAt,
        t.UpdatedAt,
        t.ProcessedAt)).ToList();

    // Get approximate count
    var totalCount = await _session
        .Query<Track, Tracks_ByUserForSearch>()
        .Where(t => t.UserId == query.UserId && t.Status != TrackStatus.Deleted)
        .CountAsync(ct);

    return new PagedResult<TrackListItem>(results, nextCursor, totalCount, hasMore);
}

private static string GetSortValue(Track track, string sortBy) =>
    sortBy?.ToLowerInvariant() switch
    {
        "title" => track.Title,
        "artist" => track.Artist ?? "",
        "duration" => track.Duration.TotalSeconds.ToString("F0"),
        "updatedat" => track.UpdatedAt.ToString("O"),
        _ => track.CreatedAt.ToString("O")
    };
```

### 6. Endpoint Implementation

```csharp
group.MapGet("/", async (
    [AsParameters] TrackListQueryParams queryParams,
    [FromServices] ITrackManagementService trackService,
    ClaimsPrincipal user,
    CancellationToken ct) =>
{
    var userId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    // Validate cursor format
    if (queryParams.Cursor is not null &&
        PaginationCursor.Decode(queryParams.Cursor) is null)
    {
        return Results.Problem(
            title: "Invalid cursor",
            detail: "The pagination cursor is malformed or corrupted.",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-cursor");
    }

    var query = new TrackListQuery(
        queryParams.Search,
        queryParams.Status,
        queryParams.SortBy ?? "createdAt",
        queryParams.SortOrder ?? "desc",
        queryParams.Cursor,
        queryParams.Limit ?? 20,
        queryParams.IncludeDeleted ?? false);

    var result = await trackService.ListTracksAsync(userId, query, ct);
    return Results.Ok(result);
})
.WithName("ListTracks")
.Produces<PagedResult<TrackListItem>>(StatusCodes.Status200OK)
.ProducesProblem(StatusCodes.Status400BadRequest);
```

## Response Format

```json
{
  "items": [
    {
      "trackId": "01HXK...",
      "title": "My Track",
      "artist": "Artist Name",
      "duration": "PT3M42S",
      "status": "Ready",
      "fileSizeBytes": 15728640,
      "mimeType": "audio/mpeg",
      "createdAt": "2025-01-08T10:00:00Z",
      "updatedAt": "2025-01-08T10:05:00Z"
    }
  ],
  "nextCursor": "eyJTb3J0VmFsdWUiOiIyMDI1LTAxLTA4VDEwOjAwOjAwWiIsIklkIjoiMDFIWEsuLi4iLCJUaW1lc3RhbXAiOiIyMDI1LTAxLTA4VDEyOjAwOjAwWiJ9",
  "totalCount": 150,
  "hasMore": true
}
```

## Validation Rules

| Parameter | Rule | Error |
|-----------|------|-------|
| `limit` | 1-100 | 400 Bad Request |
| `sortBy` | Valid field name | 400 Bad Request |
| `sortOrder` | `asc` or `desc` | 400 Bad Request |
| `cursor` | Valid base64, not expired | 400 Bad Request |

## Best Practices

1. **ULID as tie-breaker**: Provides natural chronological ordering
2. **Cursor expiry**: Prevent stale cursors (24h default)
3. **Approximate total**: Cache total count, don't compute per-request
4. **URL-safe encoding**: Use base64url without padding
5. **Fetch N+1**: Get one extra item to determine `hasMore`
