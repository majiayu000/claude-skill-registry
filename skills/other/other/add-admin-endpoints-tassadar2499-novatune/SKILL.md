---
description: Add admin API endpoints with proper authorization, audit logging, and rate limiting (project)
---
# Add Admin Endpoints Skill

Implement admin API endpoints for NovaTune with proper authorization, audit logging, and rate limiting.

## Overview

Admin endpoints provide:
- **User management**: List, view, and update user status
- **Track moderation**: List, view, moderate, and delete tracks
- **Analytics**: Dashboard overview and reports
- **Audit logs**: View and verify audit trail

## Steps

### 1. Create Authorization Policies

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Configuration/AuthorizationConfig.cs`

```csharp
namespace NovaTuneApp.ApiService.Configuration;

public static class AuthorizationConfig
{
    public static IServiceCollection AddAdminAuthorization(
        this IServiceCollection services)
    {
        services.AddAuthorization(options =>
        {
            // Basic admin access
            options.AddPolicy(PolicyNames.AdminOnly, policy =>
                policy.RequireClaim(ClaimTypes.Role, "Admin"));

            // Admin with audit access permission
            options.AddPolicy(PolicyNames.AdminWithAuditAccess, policy =>
                policy.RequireAssertion(context =>
                    context.User.HasClaim(ClaimTypes.Role, "Admin") &&
                    context.User.HasClaim("permissions", "audit.read")));
        });

        return services;
    }
}

public static class PolicyNames
{
    public const string ActiveUser = "ActiveUser";
    public const string AdminOnly = "AdminOnly";
    public const string AdminWithAuditAccess = "AdminWithAuditAccess";
}
```

### 2. Create Admin Endpoints

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Endpoints/AdminEndpoints.cs`

```csharp
namespace NovaTuneApp.ApiService.Endpoints;

public static class AdminEndpoints
{
    public static void MapAdminEndpoints(this IEndpointRouteBuilder app)
    {
        var group = app.MapGroup("/admin")
            .RequireAuthorization(PolicyNames.AdminOnly)
            .WithTags("Admin")
            .WithOpenApi();

        // User Management
        MapUserEndpoints(group);

        // Track Moderation
        MapTrackEndpoints(group);

        // Analytics Dashboard
        MapAnalyticsEndpoints(group);

        // Audit Logs
        MapAuditEndpoints(group);
    }

    private static void MapUserEndpoints(RouteGroupBuilder group)
    {
        var users = group.MapGroup("/users");

        users.MapGet("/", HandleListUsers)
            .WithName("AdminListUsers")
            .WithSummary("List and search users")
            .Produces<PagedResult<AdminUserListItem>>()
            .ProducesProblem(StatusCodes.Status401Unauthorized)
            .ProducesProblem(StatusCodes.Status403Forbidden)
            .RequireRateLimiting("admin-user-list");

        users.MapGet("/{userId}", HandleGetUser)
            .WithName("AdminGetUser")
            .WithSummary("Get user details")
            .Produces<AdminUserDetails>()
            .ProducesProblem(StatusCodes.Status404NotFound);

        users.MapPatch("/{userId}", HandleUpdateUserStatus)
            .WithName("AdminUpdateUserStatus")
            .WithSummary("Update user status")
            .Produces<AdminUserDetails>()
            .ProducesProblem(StatusCodes.Status400BadRequest)
            .ProducesProblem(StatusCodes.Status403Forbidden)
            .ProducesProblem(StatusCodes.Status404NotFound)
            .RequireRateLimiting("admin-user-modify");
    }

    private static void MapTrackEndpoints(RouteGroupBuilder group)
    {
        var tracks = group.MapGroup("/tracks");

        tracks.MapGet("/", HandleListTracks)
            .WithName("AdminListTracks")
            .WithSummary("List and search all tracks")
            .Produces<PagedResult<AdminTrackListItem>>()
            .RequireRateLimiting("admin-track-list");

        tracks.MapGet("/{trackId}", HandleGetTrack)
            .WithName("AdminGetTrack")
            .WithSummary("Get track details (admin view)")
            .Produces<AdminTrackDetails>()
            .ProducesProblem(StatusCodes.Status404NotFound);

        tracks.MapPost("/{trackId}/moderate", HandleModerateTrack)
            .WithName("AdminModerateTrack")
            .WithSummary("Moderate a track")
            .Produces<AdminTrackDetails>()
            .ProducesProblem(StatusCodes.Status400BadRequest)
            .ProducesProblem(StatusCodes.Status404NotFound)
            .RequireRateLimiting("admin-track-modify");

        tracks.MapDelete("/{trackId}", HandleDeleteTrack)
            .WithName("AdminDeleteTrack")
            .WithSummary("Delete a track (admin)")
            .Produces(StatusCodes.Status204NoContent)
            .ProducesProblem(StatusCodes.Status404NotFound)
            .RequireRateLimiting("admin-track-modify");
    }

    private static void MapAnalyticsEndpoints(RouteGroupBuilder group)
    {
        var analytics = group.MapGroup("/analytics");

        analytics.MapGet("/overview", HandleGetOverview)
            .WithName("AdminAnalyticsOverview")
            .WithSummary("Get dashboard overview metrics")
            .Produces<AnalyticsOverview>()
            .RequireRateLimiting("admin-analytics");

        analytics.MapGet("/tracks/top", HandleGetTopTracks)
            .WithName("AdminTopTracks")
            .WithSummary("Get top tracks by play count")
            .Produces<TopTracksResponse>()
            .RequireRateLimiting("admin-analytics");

        analytics.MapGet("/users/active", HandleGetActiveUsers)
            .WithName("AdminActiveUsers")
            .WithSummary("Get most active users")
            .Produces<ActiveUsersResponse>()
            .RequireRateLimiting("admin-analytics");
    }

    private static void MapAuditEndpoints(RouteGroupBuilder group)
    {
        var audit = group.MapGroup("/audit-logs")
            .RequireAuthorization(PolicyNames.AdminWithAuditAccess);

        audit.MapGet("/", HandleListAuditLogs)
            .WithName("AdminListAuditLogs")
            .WithSummary("List audit log entries")
            .Produces<PagedResult<AuditLogListItem>>()
            .RequireRateLimiting("admin-audit");

        audit.MapGet("/{auditId}", HandleGetAuditLog)
            .WithName("AdminGetAuditLog")
            .WithSummary("Get audit log entry details")
            .Produces<AuditLogDetails>()
            .ProducesProblem(StatusCodes.Status404NotFound);

        audit.MapGet("/verify", HandleVerifyIntegrity)
            .WithName("AdminVerifyAuditIntegrity")
            .WithSummary("Verify audit log integrity")
            .Produces<AuditIntegrityResult>();
    }

    // Handler implementations below
}
```

### 3. Implement User Management Handlers

```csharp
private static async Task<IResult> HandleListUsers(
    [AsParameters] AdminUserListQueryParams queryParams,
    [FromServices] IAdminUserService userService,
    CancellationToken ct)
{
    var query = new AdminUserListQuery(
        Search: queryParams.Search,
        Status: queryParams.Status,
        SortBy: queryParams.SortBy ?? "createdAt",
        SortOrder: queryParams.SortOrder ?? "desc",
        Cursor: queryParams.Cursor,
        Limit: queryParams.Limit ?? 50);

    var result = await userService.ListUsersAsync(query, ct);
    return Results.Ok(result);
}

private static async Task<IResult> HandleUpdateUserStatus(
    [FromRoute] string userId,
    [FromBody] UpdateUserStatusRequest request,
    [FromServices] IAdminUserService userService,
    [FromServices] IAuditLogService auditService,
    ClaimsPrincipal user,
    HttpContext httpContext,
    CancellationToken ct)
{
    // Validate ULID
    if (!Ulid.TryParse(userId, out _))
    {
        return Results.Problem(
            title: "Invalid user ID",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-user-id");
    }

    // Validate reason code
    if (!ModerationReasonCodes.Valid.Contains(request.ReasonCode))
    {
        return Results.Problem(
            title: "Invalid reason code",
            detail: $"Reason code must be one of: {string.Join(", ", ModerationReasonCodes.Valid)}",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-reason-code");
    }

    var adminUserId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    // Prevent self-modification
    if (userId == adminUserId)
    {
        return Results.Problem(
            title: "Self-modification denied",
            detail: "Administrators cannot modify their own status.",
            statusCode: StatusCodes.Status403Forbidden,
            type: "https://novatune.dev/errors/self-modification-denied");
    }

    try
    {
        var result = await userService.UpdateUserStatusAsync(
            userId, request, adminUserId, ct);

        // Create audit log entry
        await auditService.LogAsync(
            httpContext.CreateAuditRequest(
                action: AuditActions.UserStatusChanged,
                targetType: AuditTargetTypes.User,
                targetId: userId,
                reasonCode: request.ReasonCode,
                reasonText: request.ReasonText,
                newState: new { Status = request.Status }),
            ct);

        return Results.Ok(result);
    }
    catch (UserNotFoundException)
    {
        return Results.Problem(
            title: "User not found",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/user-not-found");
    }
}
```

### 4. Implement Track Moderation Handlers

```csharp
private static async Task<IResult> HandleModerateTrack(
    [FromRoute] string trackId,
    [FromBody] ModerateTrackRequest request,
    [FromServices] IAdminTrackService trackService,
    [FromServices] IAuditLogService auditService,
    ClaimsPrincipal user,
    HttpContext httpContext,
    CancellationToken ct)
{
    if (!Ulid.TryParse(trackId, out _))
    {
        return Results.Problem(
            title: "Invalid track ID",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-track-id");
    }

    if (!ModerationReasonCodes.Valid.Contains(request.ReasonCode))
    {
        return Results.Problem(
            title: "Invalid reason code",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-reason-code");
    }

    var adminUserId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    try
    {
        var result = await trackService.ModerateTrackAsync(
            trackId, request, adminUserId, ct);

        // Determine audit action based on moderation status
        var action = request.ModerationStatus switch
        {
            ModerationStatus.Disabled => AuditActions.TrackDisabled,
            ModerationStatus.Removed => AuditActions.TrackDeleted,
            _ => AuditActions.TrackModerated
        };

        await auditService.LogAsync(
            httpContext.CreateAuditRequest(
                action: action,
                targetType: AuditTargetTypes.Track,
                targetId: trackId,
                reasonCode: request.ReasonCode,
                reasonText: request.ReasonText,
                newState: new { ModerationStatus = request.ModerationStatus }),
            ct);

        return Results.Ok(result);
    }
    catch (TrackNotFoundException)
    {
        return Results.Problem(
            title: "Track not found",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/track-not-found");
    }
}

private static async Task<IResult> HandleDeleteTrack(
    [FromRoute] string trackId,
    [FromBody] AdminDeleteTrackRequest request,
    [FromServices] IAdminTrackService trackService,
    [FromServices] IAuditLogService auditService,
    ClaimsPrincipal user,
    HttpContext httpContext,
    CancellationToken ct)
{
    if (!Ulid.TryParse(trackId, out _))
    {
        return Results.Problem(
            title: "Invalid track ID",
            statusCode: StatusCodes.Status400BadRequest,
            type: "https://novatune.dev/errors/invalid-track-id");
    }

    var adminUserId = user.FindFirstValue(ClaimTypes.NameIdentifier)!;

    try
    {
        await trackService.DeleteTrackAsync(trackId, request, adminUserId, ct);

        await auditService.LogAsync(
            httpContext.CreateAuditRequest(
                action: AuditActions.TrackDeleted,
                targetType: AuditTargetTypes.Track,
                targetId: trackId,
                reasonCode: request.ReasonCode,
                reasonText: request.ReasonText),
            ct);

        return Results.NoContent();
    }
    catch (TrackNotFoundException)
    {
        return Results.Problem(
            title: "Track not found",
            statusCode: StatusCodes.Status404NotFound,
            type: "https://novatune.dev/errors/track-not-found");
    }
}
```

### 5. Implement Audit Log Handlers

```csharp
private static async Task<IResult> HandleListAuditLogs(
    [AsParameters] AuditLogQueryParams queryParams,
    [FromServices] IAuditLogService auditService,
    ClaimsPrincipal user,
    HttpContext httpContext,
    CancellationToken ct)
{
    var query = new AuditLogQuery(
        ActorUserId: queryParams.ActorUserId,
        Action: queryParams.Action,
        TargetType: queryParams.TargetType,
        TargetId: queryParams.TargetId,
        StartDate: queryParams.StartDate,
        EndDate: queryParams.EndDate,
        Cursor: queryParams.Cursor,
        Limit: queryParams.Limit ?? 50);

    var result = await auditService.ListAsync(query, ct);

    // Log that audit logs were viewed (audit the auditor)
    await auditService.LogAsync(
        httpContext.CreateAuditRequest(
            action: AuditActions.AuditLogViewed,
            targetType: AuditTargetTypes.AuditLog,
            targetId: "list",
            newState: new { Filters = queryParams }),
        ct);

    return Results.Ok(result);
}

private static async Task<IResult> HandleVerifyIntegrity(
    [FromQuery] DateOnly? startDate,
    [FromQuery] DateOnly? endDate,
    [FromServices] IAuditLogService auditService,
    [FromServices] IOptions<AdminOptions> options,
    ClaimsPrincipal user,
    HttpContext httpContext,
    CancellationToken ct)
{
    if (!options.Value.EnableIntegrityVerification)
    {
        return Results.Problem(
            title: "Integrity verification disabled",
            statusCode: StatusCodes.Status503ServiceUnavailable,
            type: "https://novatune.dev/errors/feature-disabled");
    }

    var start = startDate ?? DateOnly.FromDateTime(DateTime.UtcNow.AddDays(-30));
    var end = endDate ?? DateOnly.FromDateTime(DateTime.UtcNow);

    var result = await auditService.VerifyIntegrityAsync(start, end, ct);

    // Log integrity check
    await auditService.LogAsync(
        httpContext.CreateAuditRequest(
            action: AuditActions.AuditIntegrityChecked,
            targetType: AuditTargetTypes.AuditLog,
            targetId: "verify",
            newState: new { StartDate = start, EndDate = end, Result = result.IsValid }),
        ct);

    return Results.Ok(result);
}
```

### 6. Add Rate Limiting Policies

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Program.cs`

```csharp
builder.Services.AddRateLimiter(options =>
{
    // Admin user management
    options.AddSlidingWindowLimiter("admin-user-list", limiter =>
    {
        limiter.PermitLimit = 60;
        limiter.Window = TimeSpan.FromMinutes(1);
        limiter.SegmentsPerWindow = 6;
    });

    options.AddSlidingWindowLimiter("admin-user-modify", limiter =>
    {
        limiter.PermitLimit = 30;
        limiter.Window = TimeSpan.FromMinutes(1);
        limiter.SegmentsPerWindow = 6;
    });

    // Admin track management
    options.AddSlidingWindowLimiter("admin-track-list", limiter =>
    {
        limiter.PermitLimit = 60;
        limiter.Window = TimeSpan.FromMinutes(1);
        limiter.SegmentsPerWindow = 6;
    });

    options.AddSlidingWindowLimiter("admin-track-modify", limiter =>
    {
        limiter.PermitLimit = 30;
        limiter.Window = TimeSpan.FromMinutes(1);
        limiter.SegmentsPerWindow = 6;
    });

    // Admin analytics
    options.AddSlidingWindowLimiter("admin-analytics", limiter =>
    {
        limiter.PermitLimit = 30;
        limiter.Window = TimeSpan.FromMinutes(1);
        limiter.SegmentsPerWindow = 6;
    });

    // Admin audit logs
    options.AddSlidingWindowLimiter("admin-audit", limiter =>
    {
        limiter.PermitLimit = 30;
        limiter.Window = TimeSpan.FromMinutes(1);
        limiter.SegmentsPerWindow = 6;
    });
});
```

### 7. Register Endpoints in Program.cs

```csharp
// In Program.cs
app.MapAdminEndpoints();
```

### 8. Add Query Parameter Records

```csharp
public record AdminUserListQueryParams(
    [FromQuery] string? Search,
    [FromQuery] UserStatus? Status,
    [FromQuery] string? SortBy,
    [FromQuery] string? SortOrder,
    [FromQuery] string? Cursor,
    [FromQuery] int? Limit);

public record AdminTrackListQueryParams(
    [FromQuery] string? Search,
    [FromQuery] TrackStatus? Status,
    [FromQuery] ModerationStatus? ModerationStatus,
    [FromQuery] string? UserId,
    [FromQuery] string? SortBy,
    [FromQuery] string? SortOrder,
    [FromQuery] string? Cursor,
    [FromQuery] int? Limit);

public record AuditLogQueryParams(
    [FromQuery] string? ActorUserId,
    [FromQuery] string? Action,
    [FromQuery] string? TargetType,
    [FromQuery] string? TargetId,
    [FromQuery] DateOnly? StartDate,
    [FromQuery] DateOnly? EndDate,
    [FromQuery] string? Cursor,
    [FromQuery] int? Limit);

public record TopTracksQueryParams(
    [FromQuery] int? Count,
    [FromQuery] string? Period);

public record ActiveUsersQueryParams(
    [FromQuery] int? Count,
    [FromQuery] string? Period);
```

## Error Response Format

All admin endpoints use RFC 7807 Problem Details:

```json
{
  "type": "https://novatune.dev/errors/user-not-found",
  "title": "User not found",
  "status": 404,
  "detail": "The user with the specified ID does not exist.",
  "instance": "/admin/users/01HXK..."
}
```

## Security Checklist

- [ ] All endpoints require Admin role
- [ ] Audit log endpoints require additional permission
- [ ] Self-modification prevented
- [ ] All mutations create audit entries
- [ ] Rate limiting on all endpoints
- [ ] ULID validation on all IDs
- [ ] Reason codes validated against whitelist

## Testing

```csharp
[Fact]
public async Task UpdateUserStatus_Should_RequireAdminRole()
{
    // Arrange - user without Admin role
    var client = _factory.CreateAuthenticatedClient(role: "Listener");

    // Act
    var response = await client.PatchAsJsonAsync(
        "/admin/users/01HXK123",
        new UpdateUserStatusRequest(UserStatus.Disabled, "spam", null));

    // Assert
    response.StatusCode.ShouldBe(HttpStatusCode.Forbidden);
}

[Fact]
public async Task UpdateUserStatus_Should_PreventSelfModification()
{
    // Arrange - admin trying to modify self
    var adminUserId = "01HXK123";
    var client = _factory.CreateAuthenticatedClient(userId: adminUserId, role: "Admin");

    // Act
    var response = await client.PatchAsJsonAsync(
        $"/admin/users/{adminUserId}",
        new UpdateUserStatusRequest(UserStatus.Disabled, "spam", null));

    // Assert
    response.StatusCode.ShouldBe(HttpStatusCode.Forbidden);
    var problem = await response.Content.ReadFromJsonAsync<ProblemDetails>();
    problem!.Type.ShouldBe("https://novatune.dev/errors/self-modification-denied");
}

[Fact]
public async Task ModerateTrack_Should_CreateAuditEntry()
{
    // Arrange
    var client = _factory.CreateAuthenticatedClient(role: "Admin");
    var trackId = await CreateTestTrack();

    // Act
    await client.PostAsJsonAsync(
        $"/admin/tracks/{trackId}/moderate",
        new ModerateTrackRequest(ModerationStatus.Disabled, "copyright_violation", "DMCA"));

    // Assert
    var auditEntry = await GetLatestAuditEntry();
    auditEntry.Action.ShouldBe(AuditActions.TrackDisabled);
    auditEntry.TargetId.ShouldBe(trackId);
    auditEntry.ReasonCode.ShouldBe("copyright_violation");
}
```
