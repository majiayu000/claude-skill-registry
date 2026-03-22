---
description: Plan and implement Stage 8 Admin/Moderation with user management, track moderation, analytics dashboards, and audit logging (plan)
---
# Implement Admin / Moderation Skill

Plan and implement Stage 8 Admin/Moderation for NovaTune: user management, track moderation, analytics dashboards, and tamper-evident audit logging.

## Overview

Stage 8 implements administrative capabilities with:
- **GET /admin/users** - List/search users with pagination
- **GET /admin/users/{userId}** - Get user details
- **PATCH /admin/users/{userId}** - Update user status with reason codes
- **GET /admin/tracks** - List/search all tracks across users
- **GET /admin/tracks/{trackId}** - Get track details (admin view)
- **POST /admin/tracks/{trackId}/moderate** - Moderate track with reason codes
- **DELETE /admin/tracks/{trackId}** - Admin delete with audit trail
- **GET /admin/analytics/overview** - Dashboard overview metrics
- **GET /admin/analytics/tracks/top** - Top tracks by play count
- **GET /admin/analytics/users/active** - Most active users
- **GET /admin/audit-logs** - View audit logs with filtering
- **GET /admin/audit-logs/{auditId}** - Get audit entry details
- **GET /admin/audit-logs/verify** - Verify audit chain integrity

## Implementation Plan

### Phase 1: Data Models and Configuration

1. **Audit Log Entry Model** (`ApiService/Models/Admin/AuditLogEntry.cs`)
   - Actor identity, timestamp, action, target, reason codes
   - Hash chain fields: `PreviousEntryHash`, `ContentHash`
   - 1-year retention via RavenDB document expiration

2. **Moderation Status Enum** (`ApiService/Models/ModerationStatus.cs`)
   - `None`, `UnderReview`, `Disabled`, `Removed`

3. **Admin DTOs** (`ApiService/Models/Admin/`)
   - `AdminUserListItem`, `AdminUserDetails`, `UpdateUserStatusRequest`
   - `AdminTrackListItem`, `AdminTrackDetails`, `ModerateTrackRequest`
   - `AnalyticsOverview`, `TopTrackItem`, `UserActivityItem`
   - `AuditLogListItem`, `AuditLogDetails`

4. **Configuration** (`ApiService/Configuration/AdminOptions.cs`)
   - Page size limits, audit retention days, integrity verification settings

5. **Reason Codes** (`ApiService/Models/Admin/ModerationReasonCodes.cs`)
   - `copyright_violation`, `community_guidelines`, `illegal_content`, etc.

### Phase 2: RavenDB Indexes

1. **AuditLogs_ByFilters** (`ApiService/Infrastructure/Indexes/`)
   ```csharp
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
   ```

2. **Users_ForAdminSearch** (`ApiService/Infrastructure/Indexes/`)
   - Full-text search on email and display name
   - Filter by status, roles

3. **Tracks_ForAdminSearch** (`ApiService/Infrastructure/Indexes/`)
   - Full-text search on title and artist
   - Filter by status, moderation status, user ID

### Phase 3: Service Layer

1. **IAuditLogService** (`ApiService/Services/Admin/`)
   - `LogAsync(request, ct)` - Create audit entry with hash chain
   - `ListAsync(query, ct)` - List with filtering and pagination
   - `GetAsync(auditId, ct)` - Get single entry
   - `VerifyIntegrityAsync(startDate, endDate, ct)` - Verify hash chain

2. **IAdminUserService** (`ApiService/Services/Admin/`)
   - `ListUsersAsync(query, ct)`
   - `GetUserAsync(userId, ct)`
   - `UpdateUserStatusAsync(userId, request, adminUserId, ct)`
   - `RevokeUserSessionsAsync(userId, ct)`

3. **IAdminTrackService** (`ApiService/Services/Admin/`)
   - `ListTracksAsync(query, ct)`
   - `GetTrackAsync(trackId, ct)`
   - `ModerateTrackAsync(trackId, request, adminUserId, ct)`
   - `DeleteTrackAsync(trackId, request, adminUserId, ct)`

4. **IAdminAnalyticsService** (`ApiService/Services/Admin/`)
   - `GetOverviewAsync(ct)`
   - `GetTopTracksAsync(count, period, ct)`
   - `GetActiveUsersAsync(count, period, ct)`

### Phase 4: Authorization Policies

1. **Admin Policy** (`ApiService/Configuration/`)
   ```csharp
   options.AddPolicy("AdminOnly", policy =>
       policy.RequireClaim(ClaimTypes.Role, "Admin"));

   options.AddPolicy("AdminWithAuditAccess", policy =>
       policy.RequireAssertion(context =>
           context.User.HasClaim(ClaimTypes.Role, "Admin") &&
           context.User.HasClaim("permissions", "audit.read")));
   ```

### Phase 5: API Endpoints

1. **AdminEndpoints.cs** (`ApiService/Endpoints/`)
   ```csharp
   var group = app.MapGroup("/admin")
       .RequireAuthorization(PolicyNames.AdminOnly)
       .WithTags("Admin");

   // User management
   users.MapGet("/", HandleListUsers).RequireRateLimiting("admin-user-list");
   users.MapPatch("/{userId}", HandleUpdateUserStatus).RequireRateLimiting("admin-user-modify");

   // Track moderation
   tracks.MapPost("/{trackId}/moderate", HandleModerateTrack).RequireRateLimiting("admin-track-modify");
   tracks.MapDelete("/{trackId}", HandleDeleteTrack).RequireRateLimiting("admin-track-modify");

   // Analytics
   analytics.MapGet("/overview", HandleGetOverview).RequireRateLimiting("admin-analytics");

   // Audit logs
   audit.MapGet("/", HandleListAuditLogs).RequireRateLimiting("admin-audit");
   audit.MapGet("/verify", HandleVerifyIntegrity);
   ```

2. **Rate Limiting Policies**
   - `admin-user-list`: 60 req/min
   - `admin-user-modify`: 30 req/min
   - `admin-track-list`: 60 req/min
   - `admin-track-modify`: 30 req/min
   - `admin-analytics`: 30 req/min
   - `admin-audit`: 30 req/min

### Phase 6: Audit Log Hash Chain

1. **Hash Computation**
   ```csharp
   private static string ComputeHash(AuditLogEntry entry)
   {
       var content = $"{entry.AuditId}|{entry.ActorUserId}|{entry.Action}|" +
                     $"{entry.TargetType}|{entry.TargetId}|{entry.Timestamp:O}|" +
                     $"{entry.PreviousState}|{entry.NewState}|{entry.PreviousEntryHash}";

       using var sha256 = SHA256.Create();
       var hashBytes = sha256.ComputeHash(Encoding.UTF8.GetBytes(content));
       return Convert.ToHexString(hashBytes).ToLowerInvariant();
   }
   ```

2. **Chain Verification**
   - Load entries in timestamp order
   - Verify each entry's `PreviousEntryHash` matches previous entry's `ContentHash`
   - Verify each entry's `ContentHash` matches recomputed hash

### Phase 7: Integration Points

1. **Stage 1 (Authentication)** - Session revocation when user disabled
2. **Stage 5 (Track Management)** - Reuse soft-delete flow for admin deletions
3. **Stage 7 (Telemetry)** - Query analytics aggregates for dashboards

### Phase 8: Observability

1. **Metrics** (`ApiService/Infrastructure/Observability/`)
   - `admin_user_status_changes_total`
   - `admin_track_moderations_total`
   - `admin_track_deletions_total`
   - `admin_audit_queries_total`
   - `admin_audit_integrity_checks_total`

2. **Logging**
   - Admin operations logged at Warning level
   - Never log reason text content (NF-4.5)

### Phase 9: Testing

1. **Unit Tests**
   - `AuditLogServiceTests` - Hash chain, integrity verification
   - `AdminUserServiceTests` - Status changes, session revocation
   - `AdminTrackServiceTests` - Moderation, deletion

2. **Integration Tests**
   - End-to-end admin workflows
   - Authorization enforcement
   - Audit trail verification

## Files to Create/Modify

### New Files

| File | Purpose |
|------|---------|
| `ApiService/Models/Admin/AuditLogEntry.cs` | Audit log document |
| `ApiService/Models/Admin/AdminDtos.cs` | Admin request/response DTOs |
| `ApiService/Models/ModerationStatus.cs` | Moderation status enum |
| `ApiService/Services/Admin/IAuditLogService.cs` | Audit service interface |
| `ApiService/Services/Admin/AuditLogService.cs` | Audit service implementation |
| `ApiService/Services/Admin/IAdminUserService.cs` | User service interface |
| `ApiService/Services/Admin/AdminUserService.cs` | User service implementation |
| `ApiService/Services/Admin/IAdminTrackService.cs` | Track service interface |
| `ApiService/Services/Admin/AdminTrackService.cs` | Track service implementation |
| `ApiService/Services/Admin/IAdminAnalyticsService.cs` | Analytics service interface |
| `ApiService/Services/Admin/AdminAnalyticsService.cs` | Analytics service implementation |
| `ApiService/Endpoints/AdminEndpoints.cs` | All admin API routes |
| `ApiService/Configuration/AdminOptions.cs` | Configuration class |
| `ApiService/Infrastructure/Indexes/AuditLogs_ByFilters.cs` | Audit log index |
| `ApiService/Infrastructure/Indexes/Users_ForAdminSearch.cs` | User search index |
| `ApiService/Infrastructure/Indexes/Tracks_ForAdminSearch.cs` | Track search index |

### Modified Files

| File | Changes |
|------|---------|
| `ApiService/Models/Track.cs` | Add ModerationStatus, ModeratedAt, ModeratedByUserId |
| `ApiService/Program.cs` | Register admin services, rate limiting, authorization |

## Related Skills

- **add-audit-logging** - For implementing tamper-evident audit logs
- **add-admin-endpoints** - For creating admin API endpoints
- **add-cursor-pagination** - For paginated list endpoints
- **add-ravendb-index** - For creating search indexes
- **add-rate-limiting** - For rate limiting policies
- **add-observability** - For metrics and tracing

## Validation Checklist

- [ ] All admin endpoints require Admin role
- [ ] Audit log access requires additional permission
- [ ] Every state-changing operation creates audit entry
- [ ] Audit entries include hash chain for tamper evidence
- [ ] Admin cannot modify own status (self-lockout prevention)
- [ ] Rate limiting enforced on all admin endpoints
- [ ] Analytics queries use Stage 7 aggregates
- [ ] Session revocation works when user disabled
- [ ] Track moderation integrates with Stage 5 deletion flow
- [ ] All operations logged with correlation ID
