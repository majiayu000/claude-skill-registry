---
name: entity-event-handler
description: Use when creating entity event handlers for side effects triggered by entity CRUD operations.
---

# Entity Event Handler Development

## Required Reading

**For comprehensive C# backend patterns, you MUST read:**

**`docs/claude/backend-csharp-complete-guide.md`** - Complete patterns for entity events, side effects, message bus

---

## CRITICAL: Side Effects Rule

**NEVER call side effects directly in command handlers!**

Side effects include:

- Sending notifications (email, Teams)
- Calling external APIs
- Cross-service communication
- File operations

## File Organization

```
{Service}.Application/
└── UseCaseEvents/{Feature}/
    └── Send{Action}On{Event}{Entity}EntityEventHandler.cs
```

## Event Handler Pattern

```csharp
internal sealed class SendNotificationOnCreate{Entity}EntityEventHandler
    : PlatformCqrsEntityEventApplicationHandler<{Entity}>
{
    private readonly INotificationService notificationService;

    public SendNotificationOnCreate{Entity}EntityEventHandler(
        ILoggerFactory loggerFactory,
        IPlatformUnitOfWorkManager unitOfWorkManager,
        IServiceProvider serviceProvider,
        IPlatformRootServiceProvider rootServiceProvider,
        INotificationService notificationService)
        : base(loggerFactory, unitOfWorkManager, serviceProvider, rootServiceProvider)
    {
        this.notificationService = notificationService;
    }

    // Filter: Only handle Created events
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<{Entity}> @event)
    {
        if (@event.RequestContext.IsSeedingTestingData()) return false;
        return @event.CrudAction == PlatformCqrsEntityEventCrudAction.Created;
    }

    protected override async Task HandleAsync(
        PlatformCqrsEntityEvent<{Entity}> @event,
        CancellationToken ct)
    {
        var entity = @event.EntityData;
        await notificationService.SendAsync(entity);
    }
}
```

## Event Types

| CrudAction | Trigger           |
| ---------- | ----------------- |
| `Created`  | After CreateAsync |
| `Updated`  | After UpdateAsync |
| `Deleted`  | After DeleteAsync |

## Key Points

1. **Base class**: `PlatformCqrsEntityEventApplicationHandler<TEntity>` (single generic param)
2. **HandleWhen**: `public override async Task<bool>` - NOT `protected override bool`
3. **Auto-raised**: Platform automatically raises events on repository CRUD
4. **No manual AddDomainEvent()**: Platform handles this automatically

## Anti-Patterns

- Calling side effects in command handlers
- Using protected instead of public for HandleWhen
- Forgetting to filter test data with IsSeedingTestingData()
