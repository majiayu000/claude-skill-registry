---
name: entity-event-handler
description: Use when creating entity event handlers for side effects (notifications, external APIs, cross-service sync) triggered by entity CRUD operations.
---

# Entity Event Handler Development Workflow

## When to Use This Skill
- Sending notifications (email, Teams, Slack) after entity changes
- Calling external APIs after entity changes
- Cross-service communication via message bus
- Audit logging or analytics tracking
- ANY side effect triggered by entity CRUD

## CRITICAL RULE
**NEVER call side effects directly in command handlers!**

Platform automatically raises `PlatformCqrsEntityEvent` on repository CRUD.
Handle side effects in Entity Event Handlers instead.

## Pre-Flight Checklist
- [ ] Identify which entity triggers the event
- [ ] Identify CRUD action: Created, Updated, or Deleted
- [ ] Search existing handlers: `grep "{Entity}.*EventHandler" --include="*.cs"`
- [ ] Check if similar handler exists in `UseCaseEvents/` folder

## File Location & Naming Convention

```
{Service}.Application/
└── UseCaseEvents/
    └── {Feature}/
        └── {Action}On{Event}{Entity}EntityEventHandler.cs
```

**Naming Examples:**
- `SendNotificationOnCreateLeaveRequestEntityEventHandler.cs`
- `UpdateCategoryStatsOnSnippetChangeEventHandler.cs`
- `SyncEmployeeOnEmployeeUpdatedEntityEventHandler.cs`
- `SendEmailOnPublishGoalEntityEventHandler.cs`

## Implementation Pattern

```csharp
internal sealed class Send{Action}On{Event}{Entity}EntityEventHandler
    : PlatformCqrsEntityEventApplicationHandler<{Entity}>  // Single generic parameter!
{
    private readonly INotificationService notificationService;
    private readonly I{Service}RootRepository<{Entity}> repository;

    public Send{Action}On{Event}{Entity}EntityEventHandler(
        ILoggerFactory loggerFactory,
        IPlatformUnitOfWorkManager unitOfWorkManager,
        IServiceProvider serviceProvider,
        IPlatformRootServiceProvider rootServiceProvider,
        INotificationService notificationService,
        I{Service}RootRepository<{Entity}> repository)
        : base(loggerFactory, unitOfWorkManager, serviceProvider, rootServiceProvider)
    {
        this.notificationService = notificationService;
        this.repository = repository;
    }

    // Filter: Which events to handle
    // NOTE: Must be public override async Task<bool> - NOT protected, NOT bool!
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<{Entity}> @event)
    {
        // Skip during test data seeding
        if (@event.RequestContext.IsSeedingTestingData()) return false;

        // Only handle specific CRUD actions
        return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
    }

    protected override async Task HandleAsync(
        PlatformCqrsEntityEvent<{Entity}> @event,
        CancellationToken ct)
    {
        var entity = @event.EntityData;

        // Load additional data if needed
        var relatedData = await repository.GetByIdAsync(entity.Id, ct, e => e.Related);

        // Execute side effect
        await notificationService.SendAsync(new NotificationRequest
        {
            EntityId = entity.Id,
            EntityName = entity.Name,
            Action = "Created",
            UserId = @event.RequestContext.UserId()
        });
    }
}
```

## CRUD Action Filtering Patterns

### Single Action
```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<{Entity}> @event)
{
    return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
}
```

### Multiple Actions
```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<{Entity}> @event)
{
    return @event.CrudAction is PlatformCqrsEntityEventCrudAction.Created
        or PlatformCqrsEntityEventCrudAction.Updated;
}
```

### Updated with Specific Condition
```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<{Entity}> @event)
{
    return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Updated
        && @event.EntityData.Status == Status.Published;
}
```

### Skip Test Data Seeding
```csharp
public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<{Entity}> @event)
{
    if (@event.RequestContext.IsSeedingTestingData()) return false;
    return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
}
```

## Accessing Event Data

| Property | Description |
|----------|-------------|
| `@event.EntityData` | The entity that triggered the event |
| `@event.CrudAction` | Created, Updated, or Deleted |
| `@event.RequestContext` | Request context with user/company info |
| `@event.RequestContext.UserId()` | User who triggered the change |
| `@event.RequestContext.CurrentCompanyId()` | Company context |

## Anti-Patterns to AVOID

:x: **Wrong signature for HandleWhen:**
```csharp
// WRONG - must be public override async Task<bool>
protected override bool HandleWhen(...) { }
```

:x: **Two generic parameters:**
```csharp
// WRONG - only use single generic parameter
: PlatformCqrsEntityEventApplicationHandler<{Entity}, string>
```

:x: **Wrong folder location:**
```csharp
// WRONG - don't use DomainEventHandlers/
{Service}.Application/DomainEventHandlers/...

// CORRECT - use UseCaseEvents/
{Service}.Application/UseCaseEvents/{Feature}/...
```

:x: **Side effects in command handler:**
```csharp
// WRONG - never do this!
protected override async Task<Result> HandleAsync(Command req, CancellationToken ct)
{
    await repository.CreateAsync(entity, ct);
    await notificationService.SendAsync(entity);  // BAD!
}
```

## Verification Checklist
- [ ] Handler is in `UseCaseEvents/` folder (not `DomainEventHandlers/`)
- [ ] Uses `PlatformCqrsEntityEventApplicationHandler<{Entity}>` (single generic param)
- [ ] `HandleWhen` is `public override async Task<bool>`
- [ ] Filters by `@event.CrudAction` appropriately
- [ ] Accesses entity via `@event.EntityData`
- [ ] Skips test data seeding if appropriate
- [ ] No side effects in command handlers
