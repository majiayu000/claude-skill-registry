---
description: Create RavenDB indexes for efficient document queries (project)
---
# Add RavenDB Index Skill

Create RavenDB indexes for efficient document queries in NovaTune.

## Project Context

- Index location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/RavenDb/Indexes/`
- Naming convention: `{Collection}_{By|For}{Criteria}.cs`
- Example: `Users_ByEmail.cs`, `Tracks_ByUserForSearch.cs`

## Steps

### 1. Create Index Class

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/RavenDb/Indexes/{IndexName}.cs`

```csharp
using NovaTuneApp.ApiService.Models;
using Raven.Client.Documents.Indexes;

namespace NovaTuneApp.ApiService.Infrastructure.RavenDb.Indexes;

/// <summary>
/// RavenDB index for {description}.
/// </summary>
public class Tracks_ByUserForSearch : AbstractIndexCreationTask<Track>
{
    public Tracks_ByUserForSearch()
    {
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

        // For full-text search
        Index("SearchText", FieldIndexing.Search);
        Analyze("SearchText", "StandardAnalyzer");
    }
}
```

### 2. Register Index in Program.cs

Indexes are automatically deployed when using `IndexCreation.CreateIndexes()`:

```csharp
// In Program.cs or a startup extension
var store = services.GetRequiredService<IDocumentStore>();
await IndexCreation.CreateIndexesAsync(
    typeof(Tracks_ByUserForSearch).Assembly,
    store);
```

Or register individual indexes:

```csharp
await new Tracks_ByUserForSearch().ExecuteAsync(store);
```

### 3. Query Using Index

```csharp
// Use the index explicitly
var tracks = await session
    .Query<Track, Tracks_ByUserForSearch>()
    .Where(t => t.UserId == userId)
    .Where(t => t.Status != TrackStatus.Deleted)
    .OrderByDescending(t => t.CreatedAt)
    .Take(20)
    .ToListAsync(ct);

// Full-text search
var searchResults = await session
    .Query<Track, Tracks_ByUserForSearch>()
    .Search(t => t.Title, searchTerm)
    .Search(t => t.Artist, searchTerm, options: SearchOptions.Or)
    .ToListAsync(ct);
```

## Index Types

### Simple Index (Single Field)

```csharp
public class Users_ByEmail : AbstractIndexCreationTask<ApplicationUser>
{
    public Users_ByEmail()
    {
        Map = users => from user in users
                       select new { user.NormalizedEmail };
    }
}
```

### Composite Index (Multiple Fields)

```csharp
public class UploadSessions_ByUserAndStatus : AbstractIndexCreationTask<UploadSession>
{
    public UploadSessions_ByUserAndStatus()
    {
        Map = sessions => from session in sessions
                          select new
                          {
                              session.UserId,
                              session.Status,
                              session.ExpiresAt
                          };
    }
}
```

### Full-Text Search Index

```csharp
public class Tracks_ByUserForSearch : AbstractIndexCreationTask<Track>
{
    public Tracks_ByUserForSearch()
    {
        Map = tracks => from track in tracks
                        select new
                        {
                            track.UserId,
                            SearchText = new[] { track.Title, track.Artist }
                        };

        Index("SearchText", FieldIndexing.Search);
        Analyze("SearchText", "StandardAnalyzer");
    }
}
```

### Filtering Index (With Where Clause)

```csharp
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

## Naming Conventions

| Pattern | Example | Use Case |
|---------|---------|----------|
| `{Collection}_By{Field}` | `Users_ByEmail` | Single-field lookup |
| `{Collection}_By{Field}And{Field}` | `Sessions_ByUserAndStatus` | Multi-field lookup |
| `{Collection}_For{Purpose}` | `Tracks_ForSearch` | Special-purpose index |
| `{Collection}_By{Field}For{Purpose}` | `Tracks_ByUserForSearch` | Combined |

## Best Practices

1. **Only index fields you query** - Don't index every property
2. **Use where clauses** - Filter out documents you'll never query
3. **Consider staleness** - Use `WaitForNonStaleResults()` when needed
4. **Add XML documentation** - Explain what the index is for
5. **Test index behavior** - Write unit tests for complex indexes

## Testing

```csharp
[Fact]
public async Task Index_Should_ReturnUserTracks_FilteredByStatus()
{
    // Arrange
    var track = new Track { UserId = "user1", Status = TrackStatus.Ready };
    await session.StoreAsync(track);
    await session.SaveChangesAsync();

    // Act
    var results = await session
        .Query<Track, Tracks_ByUserForSearch>()
        .Where(t => t.UserId == "user1")
        .Where(t => t.Status == TrackStatus.Ready)
        .ToListAsync();

    // Assert
    results.Should().ContainSingle();
}
```
