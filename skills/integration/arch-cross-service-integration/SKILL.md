---
name: arch-cross-service-integration
description: Use when designing or implementing cross-service communication, data synchronization, or service boundary patterns.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

# Cross-Service Integration Workflow

## When to Use This Skill
- Designing service-to-service communication
- Implementing data synchronization
- Analyzing service boundaries
- Troubleshooting cross-service issues

## Pre-Flight Checklist
- [ ] Identify source and target services
- [ ] Determine data ownership
- [ ] Choose communication pattern (sync vs async)
- [ ] Map data transformation requirements

## Service Boundaries

### EasyPlatform Services
```
┌─────────────────────────────────────────────────────────────────────┐
│                        EasyPlatform Platform                          │
├───────────────┬───────────────┬───────────────┬────────────────────┤
│ TextSnippet  │ TextSnippet   │ TextSnippet  │ TextSnippet      │
│ (Example) │ (Example) │ (Example)     │ (Example)        │
├───────────────┴───────────────┴───────────────┴────────────────────┤
│                         Accounts Service                            │
│                    (Authentication & Users)                         │
├─────────────────────────────────────────────────────────────────────┤
│                      Shared Infrastructure                          │
│              RabbitMQ │ Redis │ MongoDB │ PostgreSQL                │
└─────────────────────────────────────────────────────────────────────┘
```

## Communication Patterns

### Pattern 1: Entity Event Bus (Recommended)

**Use when**: Source service owns data, target services need copies.

```
Source Service                    Target Service
┌────────────┐                   ┌────────────┐
│  Employee  │──── Create ────▶ │ Repository │
│ Repository │                   └────────────┘
└────────────┘                          │
      │                                 │
      │ Auto-raise                      │
      ▼                                 ▼
┌────────────┐                   ┌────────────┐
│  Producer  │── RabbitMQ ────▶ │  Consumer  │
└────────────┘                   └────────────┘
```

**Implementation**:
```csharp
// Producer (Source: Accounts)
internal sealed class EmployeeEntityEventBusMessageProducer
    : PlatformCqrsEntityEventBusMessageProducer<EmployeeEntityEventBusMessage, Employee, string>
{
    public override async Task<bool> HandleWhen(PlatformCqrsEntityEvent<Employee> @event)
        => @event.EntityData.IsActive || @event.CrudAction == PlatformCqrsEntityEventCrudAction.Deleted;
}

// Consumer (Target: TextSnippet)
internal sealed class UpsertEmployeeConsumer
    : PlatformApplicationMessageBusConsumer<EmployeeEntityEventBusMessage>
{
    public override async Task HandleLogicAsync(EmployeeEntityEventBusMessage message, string routingKey)
    {
        // Wait for dependencies
        // Handle Create/Update/Delete
    }
}
```

### Pattern 2: Direct API Call

**Use when**: Real-time data needed, no local copy required.

```csharp
// In TextSnippet, calling Accounts API
public class AccountsApiClient
{
    private readonly HttpClient _client;

    public async Task<UserDto?> GetUserAsync(string userId)
    {
        var response = await _client.GetAsync($"/api/User/{userId}");
        if (!response.IsSuccessStatusCode) return null;
        return await response.Content.ReadFromJsonAsync<UserDto>();
    }
}
```

**Considerations**:
- Add circuit breaker for resilience
- Cache responses when possible
- Handle service unavailability

### Pattern 3: Shared Database View (Anti-Pattern!)

**:x: DO NOT USE**: Violates service boundaries

```csharp
// WRONG - Direct cross-service database access
var accountsData = await accountsDbContext.Users.ToListAsync();
```

## Data Ownership Matrix

| Entity | Owner Service | Consumers |
|--------|---------------|-----------|
| User | Accounts | All services |
| Employee | TextSnippet | TextSnippet, TextSnippet |
| Candidate | TextSnippet | TextSnippet (on hire) |
| Company | Accounts | All services |
| Survey | TextSnippet | TextSnippet |

## Synchronization Patterns

### Full Sync (Initial/Recovery)
```csharp
// For initial data population or recovery
public class FullSyncJob : PlatformApplicationBackgroundJobExecutor
{
    public override async Task ProcessAsync(object? param)
    {
        // Fetch all from source
        var allEmployees = await sourceApi.GetAllAsync();

        // Upsert to local
        foreach (var batch in allEmployees.Batch(100))
        {
            await localRepo.CreateOrUpdateManyAsync(
                batch.Select(MapToLocal),
                dismissSendEvent: true);
        }
    }
}
```

### Incremental Sync (Event-Driven)
```csharp
// Normal operation via message bus
internal sealed class EmployeeSyncConsumer : PlatformApplicationMessageBusConsumer<EmployeeEventBusMessage>
{
    public override async Task HandleLogicAsync(EmployeeEventBusMessage message, string routingKey)
    {
        // Check if newer than current (race condition prevention)
        if (existing?.LastMessageSyncDate > message.CreatedUtcDate)
            return;

        // Apply change
        await ApplyChange(message);
    }
}
```

### Conflict Resolution
```csharp
// Use LastMessageSyncDate for ordering
entity.With(e => e.LastMessageSyncDate = message.CreatedUtcDate);

// Only update if message is newer
if (existing.LastMessageSyncDate <= message.CreatedUtcDate)
{
    await repository.UpdateAsync(updatedEntity);
}
```

## Integration Checklist

### Before Integration
- [ ] Define data ownership clearly
- [ ] Document which fields sync
- [ ] Plan for missing dependencies
- [ ] Define conflict resolution strategy

### Implementation
- [ ] Message defined in PlatformExampleApp.Shared
- [ ] Producer filters appropriate events
- [ ] Consumer waits for dependencies
- [ ] Race condition handling implemented
- [ ] Soft delete handled

### Testing
- [ ] Create event flows correctly
- [ ] Update event flows correctly
- [ ] Delete event flows correctly
- [ ] Out-of-order messages handled
- [ ] Missing dependency handled
- [ ] Force sync works

## Troubleshooting

### Message Not Arriving
```bash
# Check RabbitMQ queues
rabbitmqctl list_queues

# Check producer is publishing
grep -r "HandleWhen" --include="*Producer.cs" -A 5

# Check consumer is registered
grep -r "AddConsumer" --include="*.cs"
```

### Data Mismatch
```bash
# Compare source and target counts
# In source service DB
SELECT COUNT(*) FROM Employees WHERE IsActive = 1;

# In target service DB
SELECT COUNT(*) FROM SyncedEmployees;
```

### Stuck Messages
```csharp
// Check for waiting dependencies
Logger.LogWarning("Waiting for Company {CompanyId}", companyId);

// Force reprocess
await messageBus.PublishAsync(message.With(m => m.IsForceSync = true));
```

## Anti-Patterns to AVOID

:x: **Direct database access**
```csharp
// WRONG
await otherServiceDbContext.Table.ToListAsync();
```

:x: **Synchronous cross-service calls in transaction**
```csharp
// WRONG
using var transaction = await db.BeginTransactionAsync();
await externalService.NotifyAsync();  // If fails, transaction stuck
await transaction.CommitAsync();
```

:x: **No dependency waiting**
```csharp
// WRONG - FK violation if company not synced
await repo.CreateAsync(employee);  // Employee.CompanyId references Company

// CORRECT
await Util.TaskRunner.TryWaitUntilAsync(() => companyRepo.AnyAsync(...));
```

:x: **Ignoring message order**
```csharp
// WRONG - older message overwrites newer
await repo.UpdateAsync(entity);

// CORRECT - check timestamp
if (existing.LastMessageSyncDate <= message.CreatedUtcDate)
```

## Verification Checklist
- [ ] Data ownership clearly defined
- [ ] Message bus pattern used (not direct DB)
- [ ] Dependencies waited for in consumers
- [ ] Race conditions handled with timestamps
- [ ] Soft delete synchronized properly
- [ ] Force sync mechanism available
- [ ] Monitoring/alerting in place

## Task Planning Notes

- Always plan and break many small todo tasks
- Always add a final review todo task to review the works done at the end to find any fix or enhancement needed
