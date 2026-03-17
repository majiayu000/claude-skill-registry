---
description: Implement tamper-evident audit logging with hash chain verification for admin actions (project)
---
# Add Audit Logging Skill

Implement tamper-evident audit logging with SHA-256 hash chain verification for NovaTune admin operations.

## Overview

Audit logging provides:
- **Accountability**: Track who did what, when, and why
- **Compliance**: Meet regulatory requirements (NF-3.5)
- **Forensics**: Investigate security incidents
- **Tamper evidence**: Hash chain detects modifications

## Steps

### 1. Create Audit Log Entry Model

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Admin/AuditLogEntry.cs`

```csharp
namespace NovaTuneApp.ApiService.Models.Admin;

/// <summary>
/// Audit log entry for admin actions (NF-3.5).
/// </summary>
public sealed class AuditLogEntry
{
    /// <summary>
    /// RavenDB document ID: "AuditLogs/{ulid}".
    /// </summary>
    public string Id { get; init; } = string.Empty;

    /// <summary>
    /// Unique audit entry ID (ULID).
    /// </summary>
    [Required]
    [MaxLength(26)]
    public string AuditId { get; init; } = string.Empty;

    /// <summary>
    /// Admin user who performed the action.
    /// </summary>
    [Required]
    public string ActorUserId { get; init; } = string.Empty;

    /// <summary>
    /// Actor's email at time of action (denormalized).
    /// </summary>
    [Required]
    public string ActorEmail { get; init; } = string.Empty;

    /// <summary>
    /// Action performed (from AuditActions constants).
    /// </summary>
    [Required]
    [MaxLength(64)]
    public string Action { get; init; } = string.Empty;

    /// <summary>
    /// Resource type affected.
    /// </summary>
    [Required]
    [MaxLength(32)]
    public string TargetType { get; init; } = string.Empty;

    /// <summary>
    /// Target resource ID.
    /// </summary>
    [Required]
    [MaxLength(64)]
    public string TargetId { get; init; } = string.Empty;

    /// <summary>
    /// Reason code for the action.
    /// </summary>
    [MaxLength(64)]
    public string? ReasonCode { get; init; }

    /// <summary>
    /// Free-text reason/notes from admin.
    /// </summary>
    [MaxLength(1000)]
    public string? ReasonText { get; init; }

    /// <summary>
    /// Previous state (JSON serialized).
    /// </summary>
    public string? PreviousState { get; init; }

    /// <summary>
    /// New state (JSON serialized).
    /// </summary>
    public string? NewState { get; init; }

    /// <summary>
    /// Server timestamp when action occurred.
    /// </summary>
    public DateTimeOffset Timestamp { get; init; }

    /// <summary>
    /// Request correlation ID for tracing.
    /// </summary>
    [MaxLength(128)]
    public string? CorrelationId { get; init; }

    /// <summary>
    /// IP address of the admin.
    /// </summary>
    [MaxLength(45)]
    public string? IpAddress { get; init; }

    /// <summary>
    /// User agent of the admin client.
    /// </summary>
    [MaxLength(500)]
    public string? UserAgent { get; init; }

    /// <summary>
    /// Hash of previous audit entry (tamper-evidence chain).
    /// </summary>
    [MaxLength(64)]
    public string? PreviousEntryHash { get; init; }

    /// <summary>
    /// SHA-256 hash of this entry's content.
    /// </summary>
    [MaxLength(64)]
    public string? ContentHash { get; init; }

    /// <summary>
    /// Expiration for document retention (1 year per NF-3.5).
    /// </summary>
    [JsonPropertyName("@expires")]
    public DateTimeOffset? Expires { get; init; }
}
```

### 2. Create Action and Target Constants

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Models/Admin/AuditConstants.cs`

```csharp
namespace NovaTuneApp.ApiService.Models.Admin;

/// <summary>
/// Standard audit action types.
/// </summary>
public static class AuditActions
{
    // User management
    public const string UserStatusChanged = "user.status_changed";
    public const string UserRoleChanged = "user.role_changed";
    public const string UserDeleted = "user.deleted";
    public const string UserSessionsRevoked = "user.sessions_revoked";

    // Track moderation
    public const string TrackDeleted = "track.deleted";
    public const string TrackModerated = "track.moderated";
    public const string TrackDisabled = "track.disabled";
    public const string TrackRestored = "track.restored";

    // Audit log access
    public const string AuditLogViewed = "audit.viewed";
    public const string AuditLogExported = "audit.exported";
    public const string AuditIntegrityChecked = "audit.integrity_checked";
}

/// <summary>
/// Target resource types for audit entries.
/// </summary>
public static class AuditTargetTypes
{
    public const string User = "User";
    public const string Track = "Track";
    public const string AuditLog = "AuditLog";
}
```

### 3. Create Audit Log Service Interface

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/Admin/IAuditLogService.cs`

```csharp
namespace NovaTuneApp.ApiService.Services.Admin;

public interface IAuditLogService
{
    /// <summary>
    /// Records an audit log entry with hash chain.
    /// </summary>
    Task<AuditLogEntry> LogAsync(
        AuditLogRequest request,
        CancellationToken ct = default);

    /// <summary>
    /// Lists audit log entries with filtering.
    /// </summary>
    Task<PagedResult<AuditLogListItem>> ListAsync(
        AuditLogQuery query,
        CancellationToken ct = default);

    /// <summary>
    /// Gets a specific audit log entry.
    /// </summary>
    Task<AuditLogDetails> GetAsync(
        string auditId,
        CancellationToken ct = default);

    /// <summary>
    /// Verifies integrity of audit log chain.
    /// </summary>
    Task<AuditIntegrityResult> VerifyIntegrityAsync(
        DateOnly startDate,
        DateOnly endDate,
        CancellationToken ct = default);
}

public record AuditLogRequest(
    string ActorUserId,
    string ActorEmail,
    string Action,
    string TargetType,
    string TargetId,
    string? ReasonCode = null,
    string? ReasonText = null,
    object? PreviousState = null,
    object? NewState = null,
    string? CorrelationId = null,
    string? IpAddress = null,
    string? UserAgent = null);

public record AuditLogQuery(
    string? ActorUserId = null,
    string? Action = null,
    string? TargetType = null,
    string? TargetId = null,
    DateOnly? StartDate = null,
    DateOnly? EndDate = null,
    string? Cursor = null,
    int Limit = 50);

public record AuditIntegrityResult(
    bool IsValid,
    int EntriesChecked,
    int InvalidEntries,
    IReadOnlyList<string> InvalidAuditIds);
```

### 4. Implement Audit Log Service with Hash Chain

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Services/Admin/AuditLogService.cs`

```csharp
using System.Security.Cryptography;
using System.Text;
using System.Text.Json;

namespace NovaTuneApp.ApiService.Services.Admin;

public class AuditLogService : IAuditLogService
{
    private readonly IAsyncDocumentSession _session;
    private readonly IOptions<AdminOptions> _options;
    private readonly ILogger<AuditLogService> _logger;

    public AuditLogService(
        IAsyncDocumentSession session,
        IOptions<AdminOptions> options,
        ILogger<AuditLogService> logger)
    {
        _session = session;
        _options = options;
        _logger = logger;
    }

    public async Task<AuditLogEntry> LogAsync(
        AuditLogRequest request,
        CancellationToken ct = default)
    {
        var now = DateTimeOffset.UtcNow;
        var auditId = Ulid.NewUlid().ToString();

        // Get hash of previous entry for chain
        var previousEntry = await _session
            .Query<AuditLogEntry>()
            .OrderByDescending(e => e.Timestamp)
            .FirstOrDefaultAsync(ct);

        var previousHash = previousEntry?.ContentHash;

        var entry = new AuditLogEntry
        {
            Id = $"AuditLogs/{auditId}",
            AuditId = auditId,
            ActorUserId = request.ActorUserId,
            ActorEmail = request.ActorEmail,
            Action = request.Action,
            TargetType = request.TargetType,
            TargetId = request.TargetId,
            ReasonCode = request.ReasonCode,
            ReasonText = request.ReasonText,
            PreviousState = request.PreviousState is not null
                ? JsonSerializer.Serialize(request.PreviousState)
                : null,
            NewState = request.NewState is not null
                ? JsonSerializer.Serialize(request.NewState)
                : null,
            Timestamp = now,
            CorrelationId = request.CorrelationId,
            IpAddress = request.IpAddress,
            UserAgent = request.UserAgent,
            PreviousEntryHash = previousHash,
            Expires = now.AddDays(_options.Value.AuditRetentionDays)
        };

        // Compute content hash
        entry = entry with { ContentHash = ComputeHash(entry) };

        await _session.StoreAsync(entry, ct);
        await _session.SaveChangesAsync(ct);

        _logger.LogInformation(
            "Audit log created: {Action} on {TargetType}/{TargetId} by {ActorUserId}",
            entry.Action, entry.TargetType, entry.TargetId, entry.ActorUserId);

        return entry;
    }

    public async Task<AuditIntegrityResult> VerifyIntegrityAsync(
        DateOnly startDate,
        DateOnly endDate,
        CancellationToken ct = default)
    {
        var entries = await _session
            .Query<AuditLogEntry>()
            .Where(e => e.Timestamp >= startDate.ToDateTime(TimeOnly.MinValue, DateTimeKind.Utc)
                     && e.Timestamp <= endDate.ToDateTime(TimeOnly.MaxValue, DateTimeKind.Utc))
            .OrderBy(e => e.Timestamp)
            .ToListAsync(ct);

        var invalidIds = new List<string>();
        string? expectedPreviousHash = null;

        // For first entry in range, get the actual previous entry's hash
        if (entries.Count > 0)
        {
            var firstEntry = entries[0];
            expectedPreviousHash = firstEntry.PreviousEntryHash;

            // Verify we can trust the starting point
            if (firstEntry.PreviousEntryHash is not null)
            {
                var actualPrevious = await _session
                    .Query<AuditLogEntry>()
                    .Where(e => e.Timestamp < firstEntry.Timestamp)
                    .OrderByDescending(e => e.Timestamp)
                    .FirstOrDefaultAsync(ct);

                if (actualPrevious?.ContentHash != firstEntry.PreviousEntryHash)
                {
                    invalidIds.Add(firstEntry.AuditId);
                }
            }
            expectedPreviousHash = firstEntry.ContentHash;
        }

        // Verify chain within range
        for (int i = 1; i < entries.Count; i++)
        {
            var entry = entries[i];

            // Verify previous hash chain
            if (entry.PreviousEntryHash != expectedPreviousHash)
            {
                invalidIds.Add(entry.AuditId);
                _logger.LogWarning(
                    "Audit chain broken at {AuditId}: expected previous hash {Expected}, got {Actual}",
                    entry.AuditId, expectedPreviousHash, entry.PreviousEntryHash);
            }

            // Verify content hash
            var computedHash = ComputeHash(entry);
            if (entry.ContentHash != computedHash)
            {
                if (!invalidIds.Contains(entry.AuditId))
                {
                    invalidIds.Add(entry.AuditId);
                    _logger.LogWarning(
                        "Audit content hash mismatch at {AuditId}: expected {Expected}, got {Actual}",
                        entry.AuditId, computedHash, entry.ContentHash);
                }
            }

            expectedPreviousHash = entry.ContentHash;
        }

        var result = new AuditIntegrityResult(
            invalidIds.Count == 0,
            entries.Count,
            invalidIds.Count,
            invalidIds);

        if (!result.IsValid)
        {
            _logger.LogError(
                "Audit log integrity check FAILED: {InvalidCount} of {TotalCount} entries invalid",
                result.InvalidEntries, result.EntriesChecked);
        }

        return result;
    }

    private static string ComputeHash(AuditLogEntry entry)
    {
        // Include all immutable fields in hash
        var content = string.Join("|",
            entry.AuditId,
            entry.ActorUserId,
            entry.ActorEmail,
            entry.Action,
            entry.TargetType,
            entry.TargetId,
            entry.ReasonCode ?? "",
            entry.Timestamp.ToString("O"),
            entry.PreviousState ?? "",
            entry.NewState ?? "",
            entry.PreviousEntryHash ?? "");

        using var sha256 = SHA256.Create();
        var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(content));
        return Convert.ToHexString(hashBytes).ToLowerInvariant();
    }

    // ListAsync and GetAsync implementations...
}
```

### 5. Create RavenDB Index

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Infrastructure/Indexes/AuditLogs_ByFilters.cs`

```csharp
using Raven.Client.Documents.Indexes;
using NovaTuneApp.ApiService.Models.Admin;

namespace NovaTuneApp.ApiService.Infrastructure.Indexes;

public class AuditLogs_ByFilters : AbstractIndexCreationTask<AuditLogEntry>
{
    public AuditLogs_ByFilters()
    {
        Map = entries => from entry in entries
                         select new
                         {
                             entry.ActorUserId,
                             entry.Action,
                             entry.TargetType,
                             entry.TargetId,
                             entry.Timestamp,
                             entry.ReasonCode
                         };
    }
}
```

### 6. Add Configuration

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Configuration/AdminOptions.cs`

```csharp
namespace NovaTuneApp.ApiService.Configuration;

public class AdminOptions
{
    public const string SectionName = "Admin";

    /// <summary>
    /// Audit log retention period in days.
    /// Default: 365 (1 year per NF-3.5).
    /// </summary>
    public int AuditRetentionDays { get; set; } = 365;

    /// <summary>
    /// Enable audit log integrity verification.
    /// </summary>
    public bool EnableIntegrityVerification { get; set; } = true;

    /// <summary>
    /// Maximum audit log entries per page.
    /// </summary>
    public int MaxAuditPageSize { get; set; } = 100;
}
```

### 7. Create Extension Method for Easy Logging

Location: `src/NovaTuneApp/NovaTuneApp.ApiService/Extensions/AuditLogExtensions.cs`

```csharp
namespace NovaTuneApp.ApiService.Extensions;

public static class AuditLogExtensions
{
    /// <summary>
    /// Creates an audit log request from HTTP context.
    /// </summary>
    public static AuditLogRequest CreateAuditRequest(
        this HttpContext context,
        string action,
        string targetType,
        string targetId,
        string? reasonCode = null,
        string? reasonText = null,
        object? previousState = null,
        object? newState = null)
    {
        var user = context.User;
        var userId = user.FindFirstValue(ClaimTypes.NameIdentifier) ?? "unknown";
        var email = user.FindFirstValue(ClaimTypes.Email) ?? "unknown";
        var correlationId = Activity.Current?.Id;
        var ipAddress = context.Connection.RemoteIpAddress?.ToString();
        var userAgent = context.Request.Headers.UserAgent.ToString();

        return new AuditLogRequest(
            ActorUserId: userId,
            ActorEmail: email,
            Action: action,
            TargetType: targetType,
            TargetId: targetId,
            ReasonCode: reasonCode,
            ReasonText: reasonText,
            PreviousState: previousState,
            NewState: newState,
            CorrelationId: correlationId,
            IpAddress: ipAddress,
            UserAgent: userAgent);
    }
}
```

### 8. Usage in Admin Services

```csharp
public class AdminUserService : IAdminUserService
{
    private readonly IAuditLogService _auditLog;

    public async Task<AdminUserDetails> UpdateUserStatusAsync(
        string userId,
        UpdateUserStatusRequest request,
        string adminUserId,
        HttpContext httpContext,
        CancellationToken ct = default)
    {
        var user = await _session.LoadAsync<ApplicationUser>($"Users/{userId}", ct);

        if (user is null)
            throw new UserNotFoundException(userId);

        var previousStatus = user.Status;
        user.Status = request.Status;

        // Create audit log entry
        await _auditLog.LogAsync(
            httpContext.CreateAuditRequest(
                action: AuditActions.UserStatusChanged,
                targetType: AuditTargetTypes.User,
                targetId: userId,
                reasonCode: request.ReasonCode,
                reasonText: request.ReasonText,
                previousState: new { Status = previousStatus },
                newState: new { Status = request.Status }),
            ct);

        await _session.SaveChangesAsync(ct);

        return MapToDetails(user);
    }
}
```

## Hash Chain Verification

```
┌────────────────┐     ┌────────────────┐     ┌────────────────┐
│   Entry #1     │     │   Entry #2     │     │   Entry #3     │
│                │     │                │     │                │
│ ContentHash: A │────►│ PrevHash: A    │────►│ PrevHash: B    │
│                │     │ ContentHash: B │     │ ContentHash: C │
└────────────────┘     └────────────────┘     └────────────────┘

If any entry is modified, its ContentHash changes,
breaking the chain verification for all subsequent entries.
```

## Security Considerations

1. **Immutability**: Audit entries should never be modified after creation
2. **Hash algorithm**: Use SHA-256 for industry-standard security
3. **Include all fields**: Hash must include all meaningful content
4. **Timestamp precision**: Use ISO 8601 with timezone for consistency
5. **Retention**: 1 year retention per NF-3.5, then auto-expire

## Testing

```csharp
[Fact]
public async Task LogAsync_Should_CreateEntry_WithHashChain()
{
    // Arrange
    var request = new AuditLogRequest(
        ActorUserId: "admin1",
        ActorEmail: "admin@example.com",
        Action: AuditActions.UserStatusChanged,
        TargetType: AuditTargetTypes.User,
        TargetId: "user1");

    // Act
    var entry1 = await _service.LogAsync(request);
    var entry2 = await _service.LogAsync(request with { TargetId = "user2" });

    // Assert
    entry1.ContentHash.ShouldNotBeNullOrEmpty();
    entry2.PreviousEntryHash.ShouldBe(entry1.ContentHash);
}

[Fact]
public async Task VerifyIntegrityAsync_Should_DetectTampering()
{
    // Arrange - create entries
    await _service.LogAsync(CreateRequest("user1"));
    await _service.LogAsync(CreateRequest("user2"));

    // Tamper with middle entry
    var entry = await _session.Query<AuditLogEntry>().Skip(1).FirstAsync();
    entry = entry with { ReasonCode = "tampered" };
    await _session.SaveChangesAsync();

    // Act
    var result = await _service.VerifyIntegrityAsync(
        DateOnly.FromDateTime(DateTime.UtcNow.AddDays(-1)),
        DateOnly.FromDateTime(DateTime.UtcNow.AddDays(1)));

    // Assert
    result.IsValid.ShouldBeFalse();
    result.InvalidEntries.ShouldBe(1);
}
```

## Best Practices

1. **Log before commit**: Create audit entry in same transaction as business operation
2. **Denormalize actor info**: Store email at time of action (user might change later)
3. **Capture IP and User-Agent**: Essential for security forensics
4. **Use correlation IDs**: Link audit entries to distributed traces
5. **Never log PII in reason text**: Redact sensitive information
6. **Alert on integrity failures**: Notify security team immediately
7. **Periodic verification**: Run integrity checks on schedule
