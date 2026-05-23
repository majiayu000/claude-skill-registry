---
name: content-workflow
description: Use when implementing editorial workflows, approval chains, scheduled publishing, or role-based content permissions. Covers workflow states, transitions, notifications, and workflow APIs for headless CMS.
allowed-tools: Read, Glob, Grep, Task, Skill
---

# Content Workflow

Guidance for implementing editorial workflows, approval processes, and scheduled publishing in headless CMS systems.

## When to Use This Skill

- Implementing multi-stage approval workflows
- Adding scheduled/embargo publishing
- Building content moderation systems
- Defining role-based publishing permissions
- Automating workflow notifications

## Workflow States

### Basic Workflow States

```csharp
public enum WorkflowState
{
    Draft,          // Initial creation, author editing
    InReview,       // Submitted for review
    Approved,       // Approved, ready to publish
    Published,      // Live content
    Unpublished,    // Removed from live
    Archived,       // Long-term storage
    Rejected        // Review rejected, needs revision
}
```

### Extended Workflow States

```csharp
public enum ExtendedWorkflowState
{
    // Creation
    Draft,

    // Review stages
    PendingEditorialReview,
    EditorialApproved,
    PendingLegalReview,
    LegalApproved,
    PendingFinalApproval,

    // Publication
    Scheduled,
    Published,

    // Post-publication
    Unpublished,
    Expired,
    Archived
}
```

## State Machine Implementation

### Workflow Definition

```csharp
public class WorkflowDefinition
{
    public string Name { get; set; } = string.Empty;
    public List<WorkflowStateDefinition> States { get; set; } = new();
    public List<WorkflowTransition> Transitions { get; set; } = new();
}

public class WorkflowStateDefinition
{
    public string Name { get; set; } = string.Empty;
    public bool IsInitial { get; set; }
    public bool IsFinal { get; set; }
    public List<string> AllowedRoles { get; set; } = new();
    public List<string> RequiredFields { get; set; } = new();
}

public class WorkflowTransition
{
    public string Name { get; set; } = string.Empty;
    public string FromState { get; set; } = string.Empty;
    public string ToState { get; set; } = string.Empty;
    public List<string> AllowedRoles { get; set; } = new();
    public bool RequiresComment { get; set; }
    public List<string> Notifications { get; set; } = new();
}
```

### State Machine Service

```csharp
public class WorkflowService
{
    public async Task<bool> CanTransitionAsync(
        ContentItem content,
        string transition,
        ClaimsPrincipal user)
    {
        var workflow = await GetWorkflowAsync(content.ContentType);
        var transitionDef = workflow.Transitions
            .FirstOrDefault(t => t.Name == transition
                && t.FromState == content.WorkflowState);

        if (transitionDef == null)
            return false;

        // Check role permissions
        var userRoles = user.Claims
            .Where(c => c.Type == ClaimTypes.Role)
            .Select(c => c.Value);

        return transitionDef.AllowedRoles
            .Any(r => userRoles.Contains(r));
    }

    public async Task TransitionAsync(
        Guid contentId,
        string transition,
        string? comment,
        ClaimsPrincipal user)
    {
        var content = await _repository.GetAsync(contentId);
        if (!await CanTransitionAsync(content!, transition, user))
            throw new WorkflowException("Transition not allowed");

        var workflow = await GetWorkflowAsync(content!.ContentType);
        var transitionDef = workflow.Transitions
            .First(t => t.Name == transition);

        // Validate required fields for target state
        var targetState = workflow.States
            .First(s => s.Name == transitionDef.ToState);
        await ValidateRequiredFieldsAsync(content, targetState);

        // Record transition
        var history = new WorkflowHistory
        {
            Id = Guid.NewGuid(),
            ContentItemId = contentId,
            FromState = content.WorkflowState,
            ToState = transitionDef.ToState,
            Transition = transition,
            Comment = comment,
            UserId = user.GetUserId(),
            OccurredUtc = DateTime.UtcNow
        };

        content.WorkflowState = transitionDef.ToState;
        content.ModifiedUtc = DateTime.UtcNow;

        await _repository.UpdateAsync(content);
        await _historyRepository.AddAsync(history);

        // Send notifications
        await SendNotificationsAsync(content, transitionDef);
    }
}
```

## Scheduled Publishing

### Schedule Model

```csharp
public class PublishSchedule
{
    public Guid ContentItemId { get; set; }

    // Publishing window
    public DateTime? PublishAtUtc { get; set; }
    public DateTime? UnpublishAtUtc { get; set; }

    // Recurrence (optional)
    public bool IsRecurring { get; set; }
    public string? CronExpression { get; set; }

    // Status
    public ScheduleStatus Status { get; set; }
    public DateTime? LastExecutedUtc { get; set; }
}

public enum ScheduleStatus
{
    Pending,
    Published,
    Completed,
    Failed,
    Cancelled
}
```

### Scheduled Publishing Service

```csharp
public class ScheduledPublishingService
{
    public async Task SchedulePublishAsync(
        Guid contentId,
        DateTime publishAtUtc,
        DateTime? unpublishAtUtc = null)
    {
        var content = await _repository.GetAsync(contentId);
        if (content == null)
            throw new NotFoundException();

        // Validate content is ready to publish
        await ValidateForPublishAsync(content);

        var schedule = new PublishSchedule
        {
            ContentItemId = contentId,
            PublishAtUtc = publishAtUtc,
            UnpublishAtUtc = unpublishAtUtc,
            Status = ScheduleStatus.Pending
        };

        await _scheduleRepository.AddAsync(schedule);

        // Update content state
        content.WorkflowState = "Scheduled";
        content.ScheduledPublishUtc = publishAtUtc;
        await _repository.UpdateAsync(content);
    }

    // Called by background job
    public async Task ProcessScheduledItemsAsync()
    {
        var now = DateTime.UtcNow;

        // Items to publish
        var toPublish = await _scheduleRepository
            .GetPendingPublishAsync(now);

        foreach (var schedule in toPublish)
        {
            try
            {
                await PublishContentAsync(schedule.ContentItemId);
                schedule.Status = ScheduleStatus.Published;
                schedule.LastExecutedUtc = now;
            }
            catch (Exception ex)
            {
                schedule.Status = ScheduleStatus.Failed;
                _logger.LogError(ex, "Failed to publish {ContentId}",
                    schedule.ContentItemId);
            }

            await _scheduleRepository.UpdateAsync(schedule);
        }

        // Items to unpublish
        var toUnpublish = await _scheduleRepository
            .GetPendingUnpublishAsync(now);

        foreach (var schedule in toUnpublish)
        {
            await UnpublishContentAsync(schedule.ContentItemId);
            schedule.Status = ScheduleStatus.Completed;
            await _scheduleRepository.UpdateAsync(schedule);
        }
    }
}
```

### Background Job Configuration

```csharp
// Using Hangfire or similar
public class ScheduledPublishingJob
{
    private readonly ScheduledPublishingService _service;

    [AutomaticRetry(Attempts = 3)]
    public async Task Execute()
    {
        await _service.ProcessScheduledItemsAsync();
    }
}

// Registration
RecurringJob.AddOrUpdate<ScheduledPublishingJob>(
    "scheduled-publishing",
    job => job.Execute(),
    "*/5 * * * *"); // Every 5 minutes
```

## Approval Chains

### Multi-Stage Approval

```csharp
public class ApprovalChain
{
    public Guid Id { get; set; }
    public string Name { get; set; } = string.Empty;
    public List<ApprovalStage> Stages { get; set; } = new();
}

public class ApprovalStage
{
    public int Order { get; set; }
    public string Name { get; set; } = string.Empty;
    public ApprovalType Type { get; set; }
    public List<string> ApproverRoles { get; set; } = new();
    public List<Guid>? SpecificApproverIds { get; set; }
    public int RequiredApprovals { get; set; } = 1;
    public TimeSpan? Timeout { get; set; }
}

public enum ApprovalType
{
    AnyApprover,      // Any one from the list
    AllApprovers,     // Everyone must approve
    MajorityApprovers // Majority rule
}
```

### Approval Tracking

```csharp
public class ApprovalRequest
{
    public Guid Id { get; set; }
    public Guid ContentItemId { get; set; }
    public Guid ApprovalChainId { get; set; }
    public int CurrentStage { get; set; }
    public ApprovalStatus Status { get; set; }
    public DateTime RequestedUtc { get; set; }
    public DateTime? CompletedUtc { get; set; }

    public List<ApprovalDecision> Decisions { get; set; } = new();
}

public class ApprovalDecision
{
    public Guid Id { get; set; }
    public Guid ApprovalRequestId { get; set; }
    public int Stage { get; set; }
    public string ApproverId { get; set; } = string.Empty;
    public ApprovalDecisionType Decision { get; set; }
    public string? Comment { get; set; }
    public DateTime DecidedUtc { get; set; }
}

public enum ApprovalDecisionType
{
    Pending,
    Approved,
    Rejected,
    Delegated
}
```

## Notifications

### Notification Types

```csharp
public enum WorkflowNotificationType
{
    // Review requests
    ReviewRequested,
    ApprovalRequired,

    // Decisions
    ContentApproved,
    ContentRejected,

    // Publishing
    ContentPublished,
    ContentScheduled,
    ContentExpiring,

    // Reminders
    ReviewOverdue,
    ApprovalOverdue
}
```

### Notification Service

```csharp
public class WorkflowNotificationService
{
    public async Task SendNotificationAsync(
        WorkflowNotificationType type,
        ContentItem content,
        IEnumerable<string> recipientIds,
        Dictionary<string, string>? extraData = null)
    {
        var template = await _templateService.GetAsync(type.ToString());

        foreach (var recipientId in recipientIds)
        {
            var recipient = await _userService.GetAsync(recipientId);

            var notification = new Notification
            {
                Id = Guid.NewGuid(),
                Type = type.ToString(),
                RecipientId = recipientId,
                Subject = template.RenderSubject(content, extraData),
                Body = template.RenderBody(content, extraData),
                ContentItemId = content.Id,
                CreatedUtc = DateTime.UtcNow
            };

            await _notificationRepository.AddAsync(notification);

            // Send via configured channels
            if (recipient.EmailNotifications)
                await _emailService.SendAsync(recipient.Email, notification);

            if (recipient.SlackNotifications)
                await _slackService.SendAsync(recipient.SlackId, notification);
        }
    }
}
```

## Role-Based Permissions

### Content Permissions

```csharp
public class ContentPermission
{
    public string ContentType { get; set; } = string.Empty;
    public string Role { get; set; } = string.Empty;
    public ContentPermissionLevel Level { get; set; }
}

[Flags]
public enum ContentPermissionLevel
{
    None = 0,
    Read = 1,
    Create = 2,
    Edit = 4,
    Delete = 8,
    Publish = 16,
    Unpublish = 32,
    Archive = 64,
    ManageWorkflow = 128,
    Full = Read | Create | Edit | Delete | Publish | Unpublish | Archive | ManageWorkflow
}
```

### Permission Checking

```csharp
public class ContentAuthorizationService
{
    public async Task<bool> CanPerformActionAsync(
        ClaimsPrincipal user,
        ContentItem content,
        ContentPermissionLevel action)
    {
        var userRoles = user.Claims
            .Where(c => c.Type == ClaimTypes.Role)
            .Select(c => c.Value);

        var permissions = await _permissionRepository
            .GetByContentTypeAsync(content.ContentType);

        foreach (var role in userRoles)
        {
            var permission = permissions.FirstOrDefault(p => p.Role == role);
            if (permission != null && permission.Level.HasFlag(action))
                return true;
        }

        return false;
    }
}
```

## API Design

### Workflow Endpoints

```text
GET    /api/content/{id}/workflow              # Get workflow state
POST   /api/content/{id}/workflow/transition   # Execute transition
GET    /api/content/{id}/workflow/history      # Transition history
GET    /api/content/{id}/workflow/available    # Available transitions

# Scheduling
POST   /api/content/{id}/schedule              # Schedule publish
DELETE /api/content/{id}/schedule              # Cancel schedule
GET    /api/scheduled                          # List scheduled items

# Approvals
POST   /api/content/{id}/submit-for-review     # Start approval
POST   /api/approvals/{id}/approve             # Approve
POST   /api/approvals/{id}/reject              # Reject
GET    /api/approvals/pending                  # My pending approvals
```

## Related Skills

- `content-versioning` - Version control with workflows
- `content-type-modeling` - Workflow-enabled content types
- `headless-api-design` - Workflow API endpoints
