---
description: Add a new minimal API endpoint to NovaTune with service, models, and tests
---
# Add API Endpoint Skill

Add a new minimal API endpoint to NovaTune.

## Steps

### 1. Create/Update Request and Response Models

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/`

```csharp
// Models/Requests/CreateTrackRequest.cs
public record CreateTrackRequest(
    string Title,
    string? Description);

// Models/Responses/TrackResponse.cs
public record TrackResponse(
    Guid Id,
    string Title,
    string? Description,
    DateTimeOffset CreatedAt);
```

### 2. Create/Update Service

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/`

```csharp
public interface ITrackService
{
    Task<Track> CreateAsync(CreateTrackRequest request, CancellationToken ct);
}

public class TrackService : ITrackService
{
    private readonly IDocumentSession _session;

    public TrackService(IDocumentSession session)
    {
        _session = session;
    }

    public async Task<Track> CreateAsync(CreateTrackRequest request, CancellationToken ct)
    {
        var track = new Track
        {
            Title = request.Title,
            Description = request.Description,
            CreatedAt = DateTimeOffset.UtcNow
        };

        await _session.StoreAsync(track, ct);
        await _session.SaveChangesAsync(ct);

        return track;
    }
}
```

### 3. Create Endpoint Group

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/`

```csharp
public static class TrackEndpoints
{
    public static void MapTrackEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/api/tracks")
            .WithTags("Tracks")
            .WithOpenApi();

        group.MapPost("/", CreateTrack)
            .WithName("CreateTrack")
            .RequireAuthorization();

        group.MapGet("/{id:guid}", GetTrack)
            .WithName("GetTrack");
    }

    private static async Task<IResult> CreateTrack(
        CreateTrackRequest request,
        ITrackService trackService,
        CancellationToken ct)
    {
        var track = await trackService.CreateAsync(request, ct);
        return TypedResults.Created($"/api/tracks/{track.Id}", track.ToResponse());
    }

    private static async Task<IResult> GetTrack(
        Guid id,
        ITrackService trackService,
        CancellationToken ct)
    {
        var track = await trackService.GetByIdAsync(id, ct);
        return track is null
            ? TypedResults.NotFound()
            : TypedResults.Ok(track.ToResponse());
    }
}
```

### 4. Register in Program.cs

```csharp
// Register service
builder.Services.AddScoped<ITrackService, TrackService>();

// Map endpoints (after app.Build())
app.MapTrackEndpoints();
```

### 5. Add Tests

Unit test: `src/unit_tests/TrackServiceTests.cs`
Integration test: `src/NovaTuneApp/NovaTuneApp.Tests/TrackEndpoints.IntegrationTests.cs`

## Conventions

- Use minimal APIs with `MapGroup`
- Return `TypedResults` for proper OpenAPI schema
- Use `WithTags` and `WithOpenApi` for Scalar documentation
- Add `RequireAuthorization()` for protected endpoints
- Use `CancellationToken` in all async methods
- PascalCase for endpoint names

## Response Status Codes

| Operation | Success | Error |
|-----------|---------|-------|
| Create | 201 Created | 400 Bad Request |
| Get | 200 OK | 404 Not Found |
| Update | 200 OK / 204 No Content | 404 Not Found |
| Delete | 204 No Content | 404 Not Found |
| List | 200 OK | - |

## API Documentation

Access Scalar UI at `/scalar/v1` when running the API.
