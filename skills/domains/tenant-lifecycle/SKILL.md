---
name: tenant-lifecycle
description: Tenant state management patterns for SaaS applications. Covers Trial, Active, Suspended, Deleted states with transitions, grace periods, and data retention.
allowed-tools: Read, Glob, Grep, Task, mcp__perplexity__search, mcp__perplexity__reason, mcp__microsoft-learn__microsoft_docs_search, mcp__microsoft-learn__microsoft_docs_fetch
---

# Tenant Lifecycle Skill

Patterns for managing tenant states throughout their lifecycle in multi-tenant SaaS applications.

## When to Use This Skill

Use this skill when:

- **Tenant Lifecycle tasks** - Working on tenant state management patterns for saas applications. covers trial, active, suspended, deleted states with transitions, grace periods, and data retention
- **Planning or design** - Need guidance on Tenant Lifecycle approaches
- **Best practices** - Want to follow established patterns and standards

## Overview

Tenant lifecycle management handles the progression of tenants through states from trial to active to potential suspension and deletion. Proper lifecycle management protects revenue, ensures compliance, and maintains data integrity.

## Lifecycle State Machine

```text
+------------------------------------------------------------------+
|                    Tenant Lifecycle States                        |
+------------------------------------------------------------------+
|                                                                   |
|  +---------+    +--------+    +----------+    +---------+        |
|  | Trial   |--->| Active |--->| Suspended|--->| Deleted |        |
|  +---------+    +--------+    +----------+    +---------+        |
|       |              |             |               ^              |
|       |              |             |               |              |
|       v              v             v               |              |
|  +---------+    +--------+    +----------+        |              |
|  | Expired |    | Past   |    | Grace    |--------+              |
|  | (churn) |    | Due    |    | Period   |                       |
|  +---------+    +--------+    +----------+                       |
|                                                                   |
+------------------------------------------------------------------+
```

## State Definitions

```csharp
public enum TenantStatus
{
    /// <summary>Trial period - limited features, time-bound</summary>
    Trial,

    /// <summary>Active subscription - full access</summary>
    Active,

    /// <summary>Payment past due - still active, dunning in progress</summary>
    PastDue,

    /// <summary>Suspended - read-only or no access, awaiting payment/action</summary>
    Suspended,

    /// <summary>Grace period before deletion - can be recovered</summary>
    GracePeriod,

    /// <summary>Scheduled for deletion - cleanup in progress</summary>
    PendingDeletion,

    /// <summary>Deleted - data removed (or anonymized)</summary>
    Deleted,

    /// <summary>Trial expired without conversion</summary>
    Expired
}
```

## State Transitions

### Transition Rules

```text
State Transition Matrix:
+------------------------------------------------------------------+
| From State      | To State        | Trigger              | Auto? |
+-----------------+-----------------+----------------------+-------+
| Trial           | Active          | Payment received     | Yes   |
| Trial           | Expired         | Trial period ends    | Yes   |
| Active          | PastDue         | Payment fails        | Yes   |
| Active          | Suspended       | Admin action         | No    |
| Active          | GracePeriod     | Cancellation request | Yes   |
| PastDue         | Active          | Payment received     | Yes   |
| PastDue         | Suspended       | Dunning exhausted    | Yes   |
| Suspended       | Active          | Payment received     | Yes   |
| Suspended       | GracePeriod     | Max suspend time     | Yes   |
| GracePeriod     | Active          | Reactivation         | No    |
| GracePeriod     | PendingDeletion | Grace period ends    | Yes   |
| PendingDeletion | Deleted         | Cleanup complete     | Yes   |
| Expired         | Active          | Late conversion      | No    |
+-----------------+-----------------+----------------------+-------+
```

### Transition Service

```csharp
public sealed class TenantLifecycleService(
    IDbContext db,
    IEventPublisher events,
    ITenantNotificationService notifications,
    ILogger<TenantLifecycleService> logger)
{
    public async Task<TransitionResult> TransitionAsync(
        Guid tenantId,
        TenantStatus newStatus,
        string reason,
        CancellationToken ct = default)
    {
        var tenant = await db.Tenants.FindAsync([tenantId], ct);
        if (tenant is null)
            return TransitionResult.NotFound();

        var oldStatus = tenant.Status;

        // Validate transition
        if (!IsValidTransition(oldStatus, newStatus))
            return TransitionResult.InvalidTransition(oldStatus, newStatus);

        // Apply transition
        tenant.Status = newStatus;
        tenant.StatusChangedAt = DateTimeOffset.UtcNow;
        tenant.StatusReason = reason;

        // Set expiration dates based on new state
        ApplyStateTimers(tenant, newStatus);

        await db.SaveChangesAsync(ct);

        // Publish event
        await events.PublishAsync(new TenantStatusChangedEvent
        {
            TenantId = tenantId,
            OldStatus = oldStatus,
            NewStatus = newStatus,
            Reason = reason,
            Timestamp = DateTimeOffset.UtcNow
        }, ct);

        // Send notifications
        await notifications.NotifyStatusChangeAsync(tenantId, oldStatus, newStatus, ct);

        logger.LogInformation(
            "Tenant {TenantId} transitioned from {OldStatus} to {NewStatus}: {Reason}",
            tenantId, oldStatus, newStatus, reason);

        return TransitionResult.Success(oldStatus, newStatus);
    }

    private static bool IsValidTransition(TenantStatus from, TenantStatus to)
    {
        return (from, to) switch
        {
            (TenantStatus.Trial, TenantStatus.Active) => true,
            (TenantStatus.Trial, TenantStatus.Expired) => true,
            (TenantStatus.Active, TenantStatus.PastDue) => true,
            (TenantStatus.Active, TenantStatus.Suspended) => true,
            (TenantStatus.Active, TenantStatus.GracePeriod) => true,
            (TenantStatus.PastDue, TenantStatus.Active) => true,
            (TenantStatus.PastDue, TenantStatus.Suspended) => true,
            (TenantStatus.Suspended, TenantStatus.Active) => true,
            (TenantStatus.Suspended, TenantStatus.GracePeriod) => true,
            (TenantStatus.GracePeriod, TenantStatus.Active) => true,
            (TenantStatus.GracePeriod, TenantStatus.PendingDeletion) => true,
            (TenantStatus.PendingDeletion, TenantStatus.Deleted) => true,
            (TenantStatus.Expired, TenantStatus.Active) => true,
            _ => false
        };
    }

    private static void ApplyStateTimers(Tenant tenant, TenantStatus newStatus)
    {
        tenant.GracePeriodEndsAt = newStatus switch
        {
            TenantStatus.GracePeriod => DateTimeOffset.UtcNow.AddDays(30),
            _ => null
        };

        tenant.DeletionScheduledAt = newStatus switch
        {
            TenantStatus.PendingDeletion => DateTimeOffset.UtcNow.AddDays(7),
            _ => null
        };
    }
}
```

## Trial Management

### Trial Configuration

```csharp
public sealed record TrialConfiguration
{
    public required int TrialDays { get; init; } = 14;
    public required bool RequireCreditCard { get; init; } = false;
    public required List<string> TrialFeatures { get; init; }
    public required int TrialUserLimit { get; init; } = 5;
    public required bool AllowTrialExtension { get; init; } = true;
    public required int MaxExtensionDays { get; init; } = 7;
}
```

### Trial Expiration Job

```csharp
public sealed class TrialExpirationJob(
    IDbContext db,
    ITenantLifecycleService lifecycle,
    ILogger<TrialExpirationJob> logger) : IScheduledJob
{
    public async Task ExecuteAsync(CancellationToken ct)
    {
        var expiredTrials = await db.Tenants
            .Where(t => t.Status == TenantStatus.Trial)
            .Where(t => t.TrialEndsAt <= DateTimeOffset.UtcNow)
            .ToListAsync(ct);

        foreach (var tenant in expiredTrials)
        {
            await lifecycle.TransitionAsync(
                tenant.Id,
                TenantStatus.Expired,
                "Trial period ended",
                ct);
        }

        logger.LogInformation("Expired {Count} trial tenants", expiredTrials.Count);
    }
}
```

### Trial Extension

```csharp
public async Task<ExtensionResult> ExtendTrialAsync(
    Guid tenantId,
    int days,
    string reason,
    CancellationToken ct)
{
    var tenant = await db.Tenants.FindAsync([tenantId], ct);
    if (tenant is null)
        return ExtensionResult.NotFound();

    if (tenant.Status != TenantStatus.Trial)
        return ExtensionResult.NotInTrial();

    var config = await GetTrialConfigAsync(ct);
    if (!config.AllowTrialExtension)
        return ExtensionResult.ExtensionsDisabled();

    var totalExtension = tenant.TrialExtensionDays + days;
    if (totalExtension > config.MaxExtensionDays)
        return ExtensionResult.MaxExtensionExceeded(config.MaxExtensionDays);

    tenant.TrialEndsAt = tenant.TrialEndsAt!.Value.AddDays(days);
    tenant.TrialExtensionDays = totalExtension;
    tenant.TrialExtensionReason = reason;

    await db.SaveChangesAsync(ct);

    return ExtensionResult.Success(tenant.TrialEndsAt.Value);
}
```

## Suspension Handling

### Suspension Modes

```text
Suspension Modes:
+------------------------------------------------------------------+
| Mode              | Access Level       | Use Case                |
+-------------------+--------------------+-------------------------+
| Read-Only         | View data only     | Payment issues          |
| Admin-Only        | Only admins access | Policy violation review |
| Full Block        | No access          | Serious violation       |
| Degraded          | Core features only | Temporary capacity      |
+-------------------+--------------------+-------------------------+
```

### Access Control by Status

```csharp
public sealed class TenantAccessMiddleware(
    RequestDelegate next,
    ITenantContext tenantContext)
{
    public async Task InvokeAsync(HttpContext context)
    {
        var tenant = await tenantContext.GetCurrentTenantAsync();

        var accessResult = tenant?.Status switch
        {
            TenantStatus.Trial => AccessResult.FullAccess(),
            TenantStatus.Active => AccessResult.FullAccess(),
            TenantStatus.PastDue => AccessResult.FullAccess(), // Grace during dunning
            TenantStatus.Suspended => CheckSuspensionAccess(context, tenant),
            TenantStatus.GracePeriod => AccessResult.ReadOnly(),
            TenantStatus.PendingDeletion => AccessResult.Blocked("Account scheduled for deletion"),
            TenantStatus.Deleted => AccessResult.Blocked("Account has been deleted"),
            TenantStatus.Expired => AccessResult.Blocked("Trial has expired"),
            null => AccessResult.Blocked("Tenant not found"),
            _ => AccessResult.Blocked("Unknown status")
        };

        if (!accessResult.IsAllowed)
        {
            context.Response.StatusCode = 403;
            await context.Response.WriteAsJsonAsync(new
            {
                error = "access_denied",
                message = accessResult.Message,
                tenantStatus = tenant?.Status.ToString()
            });
            return;
        }

        if (accessResult.IsReadOnly)
        {
            context.Items["ReadOnlyMode"] = true;
        }

        await next(context);
    }
}
```

## Grace Period and Deletion

### Grace Period Configuration

```csharp
public sealed record DeletionConfiguration
{
    public required int GracePeriodDays { get; init; } = 30;
    public required int DeletionDelayDays { get; init; } = 7;
    public required bool AnonymizeInsteadOfDelete { get; init; } = true;
    public required List<int> ReminderDays { get; init; } = [7, 3, 1];
}
```

### Deletion Pipeline

```csharp
public sealed class TenantDeletionService(
    IDbContext db,
    IStorageService storage,
    IAuditLog audit,
    ILogger<TenantDeletionService> logger)
{
    public async Task<DeletionResult> DeleteTenantAsync(
        Guid tenantId,
        DeletionConfiguration config,
        CancellationToken ct)
    {
        var tenant = await db.Tenants.FindAsync([tenantId], ct);
        if (tenant is null)
            return DeletionResult.NotFound();

        if (tenant.Status != TenantStatus.PendingDeletion)
            return DeletionResult.InvalidState(tenant.Status);

        logger.LogInformation("Starting deletion for tenant {TenantId}", tenantId);

        try
        {
            // Step 1: Export data (if required for compliance)
            await ExportTenantDataAsync(tenantId, ct);

            // Step 2: Delete or anonymize user data
            if (config.AnonymizeInsteadOfDelete)
            {
                await AnonymizeTenantDataAsync(tenantId, ct);
            }
            else
            {
                await DeleteTenantDataAsync(tenantId, ct);
            }

            // Step 3: Delete storage
            await storage.DeleteTenantStorageAsync(tenantId, ct);

            // Step 4: Mark as deleted
            tenant.Status = TenantStatus.Deleted;
            tenant.DeletedAt = DateTimeOffset.UtcNow;
            await db.SaveChangesAsync(ct);

            // Step 5: Audit log (immutable record)
            await audit.LogAsync(new AuditEntry
            {
                TenantId = tenantId,
                Action = "tenant_deleted",
                Details = new { AnonymizedOnly = config.AnonymizeInsteadOfDelete },
                Timestamp = DateTimeOffset.UtcNow
            }, ct);

            return DeletionResult.Success();
        }
        catch (Exception ex)
        {
            logger.LogError(ex, "Deletion failed for tenant {TenantId}", tenantId);
            return DeletionResult.Failed(ex.Message);
        }
    }

    private async Task AnonymizeTenantDataAsync(Guid tenantId, CancellationToken ct)
    {
        // Anonymize PII while retaining aggregate data
        await db.Database.ExecuteSqlInterpolatedAsync($@"
            UPDATE Users
            SET Email = CONCAT('deleted_', Id, '@anonymized.local'),
                FirstName = 'Deleted',
                LastName = 'User',
                Phone = NULL
            WHERE TenantId = {tenantId}", ct);

        // Similar anonymization for other PII-containing tables
    }
}
```

## Notifications

### Lifecycle Notification Templates

```text
Notification Triggers:
+------------------------------------------------------------------+
| Event                  | Channel    | Timing                     |
+------------------------+------------+----------------------------+
| Trial starting         | Email      | Immediate                  |
| Trial ending soon      | Email      | 3 days, 1 day before       |
| Trial expired          | Email      | Immediate                  |
| Payment failed         | Email+App  | Immediate                  |
| Account suspended      | Email      | Immediate                  |
| Grace period starting  | Email      | Immediate                  |
| Grace period ending    | Email      | 7, 3, 1 days before        |
| Deletion scheduled     | Email      | Immediate                  |
| Account reactivated    | Email      | Immediate                  |
+------------------------+------------+----------------------------+
```

### Notification Service

```csharp
public sealed class TenantNotificationService(
    IEmailService email,
    IInAppNotifications inApp) : ITenantNotificationService
{
    public async Task NotifyStatusChangeAsync(
        Guid tenantId,
        TenantStatus oldStatus,
        TenantStatus newStatus,
        CancellationToken ct)
    {
        var template = (oldStatus, newStatus) switch
        {
            (TenantStatus.Trial, TenantStatus.Active) => "trial_converted",
            (TenantStatus.Trial, TenantStatus.Expired) => "trial_expired",
            (TenantStatus.Active, TenantStatus.PastDue) => "payment_failed",
            (TenantStatus.PastDue, TenantStatus.Suspended) => "account_suspended",
            (TenantStatus.Active, TenantStatus.GracePeriod) => "cancellation_started",
            (TenantStatus.GracePeriod, TenantStatus.PendingDeletion) => "deletion_scheduled",
            (_, TenantStatus.Active) => "account_reactivated",
            _ => null
        };

        if (template is not null)
        {
            await email.SendTemplateAsync(tenantId, template, ct);
        }
    }
}
```

## Scheduled Jobs

### Lifecycle Background Jobs

```csharp
public sealed class LifecycleScheduler(IServiceProvider services)
{
    public void ConfigureJobs(IRecurringJobManager jobs)
    {
        // Check trial expirations every hour
        jobs.AddOrUpdate<TrialExpirationJob>(
            "trial-expiration",
            job => job.ExecuteAsync(default),
            Cron.Hourly);

        // Check grace period expirations daily
        jobs.AddOrUpdate<GracePeriodExpirationJob>(
            "grace-period-expiration",
            job => job.ExecuteAsync(default),
            Cron.Daily);

        // Process pending deletions daily
        jobs.AddOrUpdate<TenantDeletionJob>(
            "tenant-deletion",
            job => job.ExecuteAsync(default),
            Cron.Daily);

        // Send reminder emails daily
        jobs.AddOrUpdate<LifecycleReminderJob>(
            "lifecycle-reminders",
            job => job.ExecuteAsync(default),
            "0 9 * * *"); // 9 AM daily
    }
}
```

## Best Practices

```text
Lifecycle Management Best Practices:
+------------------------------------------------------------------+
| Practice                    | Benefit                            |
+-----------------------------+------------------------------------+
| Clear state machine         | Predictable transitions            |
| Grace periods               | Revenue recovery, compliance       |
| Notification cadence        | User awareness, reduce churn       |
| Soft delete first           | Recovery possible, audit trail     |
| Anonymize vs delete         | GDPR compliance, analytics         |
| Status in JWT claims        | Fast access checks                 |
| Event-driven transitions    | Decoupled, auditable               |
+-----------------------------+------------------------------------+
```

## Anti-Patterns

| Anti-Pattern | Problem | Solution |
| ------------ | ------- | -------- |
| Hard delete immediately | No recovery, compliance issues | Grace period + soft delete |
| Status in UI only | Inconsistent enforcement | Middleware check on every request |
| No audit trail | Compliance/legal risk | Event sourcing for transitions |
| Silent suspension | User confusion | Clear notifications |
| One-size grace period | Revenue loss | Tier-based grace periods |

## References

Load for detailed implementation:

- `references/lifecycle-states.md` - State machine details
- `references/deletion-compliance.md` - GDPR/CCPA deletion requirements

## Related Skills

- `tenant-provisioning` - Initial tenant creation
- `subscription-models` - Payment status integration
- `audit-logging` - Lifecycle event logging
- `saas-compliance-frameworks` - Deletion compliance

## MCP Research

For current lifecycle patterns:

```text
perplexity: "SaaS tenant lifecycle 2024" "tenant soft delete GDPR"
microsoft-learn: "Azure AD B2C tenant management" "subscription state machine"
```
