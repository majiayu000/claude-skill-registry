---
name: add-integration-tests
description: Scaffold and write Aspire integration tests for NovaTune API endpoints
user_invocable: true
arguments:
  - name: feature
    description: Feature area to test (e.g., playlists, telemetry, upload, tracks, streaming)
    required: true
---

# Add Integration Tests Skill

Scaffold and write Aspire integration tests for a NovaTune API feature area.

## Steps

1. **Read the task plan** at `tasks/add_integration_tests/main.md` to understand the test specifications for the target feature.

2. **Read the target endpoint file** at `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/{Feature}Endpoints.cs` to understand:
   - All routes, HTTP methods, and auth policies
   - Request/response types
   - Validation rules and error responses
   - Exception handling

3. **Read the test factory** at `src/integration_tests/NovaTuneApp.IntegrationTests/IntegrationTestsApiFactory.cs` to understand available helpers. If the feature needs new helpers (e.g., `SeedPlaylistAsync`), add them first.

4. **Read existing test files** for patterns:
   - `src/integration_tests/NovaTuneApp.IntegrationTests/AuthIntegrationTests.cs` — auth pattern
   - `src/integration_tests/NovaTuneApp.IntegrationTests/TrackEndpointTests.cs` — CRUD pattern
   - `src/integration_tests/NovaTuneApp.IntegrationTests/AdminEndpointTests.cs` — admin pattern

5. **Create the test file** at `src/integration_tests/NovaTuneApp.IntegrationTests/{Feature}EndpointTests.cs` following the template:

```csharp
using System.Net;
using System.Net.Http.Json;
using System.Text.Json;
using Microsoft.AspNetCore.Mvc;
using NovaTuneApp.ApiService.Models;
// Add feature-specific model imports
using Shouldly;

namespace NovaTuneApp.Tests;

[Collection("Integration Tests")]
[Trait("Category", "Aspire")]
public class {Feature}EndpointTests(IntegrationTestsApiFactory factory) : IAsyncLifetime
{
    private readonly IntegrationTestsApiFactory _factory = factory;

    private static readonly JsonSerializerOptions JsonOptions = new()
    {
        PropertyNameCaseInsensitive = true
    };

    public async Task InitializeAsync() => await _factory.ClearDataAsync();
    public Task DisposeAsync() => Task.CompletedTask;

    // Tests follow...
}
```

6. **Write tests** covering these categories (in order):
   - **Authentication**: 401 for unauthenticated requests
   - **Happy paths**: Successful operations with correct status codes
   - **Validation**: 400 for invalid inputs (IDs, required fields, constraints)
   - **Authorization**: 403 for wrong user/role
   - **Not found**: 404 for nonexistent resources
   - **Conflicts**: 409 for invalid state transitions
   - **Lifecycle**: End-to-end flows combining multiple operations

7. **Verify tests compile and run**:
```bash
dotnet build src/integration_tests/NovaTuneApp.IntegrationTests/NovaTuneApp.IntegrationTests.csproj
dotnet test src/integration_tests/NovaTuneApp.IntegrationTests/NovaTuneApp.IntegrationTests.csproj --filter "FullyQualifiedName~{Feature}EndpointTests"
```

## Test Conventions

- **Naming**: `{Action}_Should_{expected_behavior}` or `{Action}_Should_{behavior}_when_{condition}`
- **Assertions**: Shouldly (`ShouldBe`, `ShouldNotBeNull`, `ShouldContain`)
- **Emails**: Unique per test — `$"user-{Guid.NewGuid():N}@test.com"`
- **Error format**: RFC 7807 ProblemDetails — check `Type`, `Status`, `Detail`
- **Isolation**: `ClearDataAsync()` in `InitializeAsync()`
- **No parallelization**: Tests run sequentially in the "Integration Tests" collection

## Feature-Specific Notes

### Playlists (`feature=playlists`)
- Test CRUD + track add/remove/reorder
- Need `SeedPlaylistAsync` and `SeedPlaylistWithTracksAsync` helpers in factory
- Tracks added to playlists must be seeded first with `SeedTrackAsync`
- Test deleted track rejection (409) when adding to playlist

### Telemetry (`feature=telemetry`)
- All responses are 202 Accepted (fire-and-forget)
- Valid event types: play_start, play_stop, play_progress, play_complete, seek
- Test batch validation (empty batch, invalid events in batch)
- Track ownership checked (403 for other user's track)

### Upload (`feature=upload`)
- MinIO is disabled in testing environment
- Only auth and validation tests are feasible
- Skip tests requiring presigned URL generation with `[Fact(Skip = "Requires MinIO")]`

### Streaming (`feature=streaming`)
- MinIO disabled — can only test auth, validation, and status-based errors
- Seed tracks with specific `TrackStatus` values to test 409 responses
