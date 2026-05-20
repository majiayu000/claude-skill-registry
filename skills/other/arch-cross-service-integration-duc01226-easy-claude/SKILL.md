---
name: arch-cross-service-integration
version: 1.1.0
description: '[Architecture] Use when designing or implementing cross-service communication, data synchronization, or service boundary patterns.'
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task
---

> **[IMPORTANT]** Use `TaskCreate` to break ALL work into small tasks BEFORE starting — including tasks for each file read. This prevents context loss from long files. For simple tasks, AI MUST ask user whether to skip.

**Prerequisites:** **MUST READ** `.claude/skills/shared/evidence-based-reasoning-protocol.md` before executing.

- `docs/project-reference/domain-entities-reference.md` — Domain entity catalog, relationships, cross-service sync (read when task involves business entities/models)

## Quick Summary

**Goal:** Design and implement cross-service communication, data sync, and service boundary patterns.

**Workflow:**

1. **Pre-Flight** — Identify source/target services, data ownership, sync vs async
2. **Choose Pattern** — Entity Event Bus (recommended), Direct API, never shared DB
3. **Implement** — Producer + Consumer with dependency waiting and race condition handling
4. **Test** — Verify create/update/delete flows, out-of-order messages, force sync

**Key Rules:**

- Never access another service's database directly
- Use `LastMessageSyncDate` for conflict resolution (only update if newer)
- Consumers must wait for dependencies with `TryWaitUntilAsync`
- Messages defined in shared project (search for: shared message definitions, bus message classes)

**Be skeptical. Apply critical thinking, sequential thinking. Every claim needs traced proof, confidence percentages (Idea should be more than 80%).**

> **MANDATORY IMPORTANT MUST** Plan ToDo Task to READ the following project-specific reference doc:
>
> - `backend-patterns-reference.md` — backend CQRS, entity event bus, message bus patterns
>
> If file not found, search for: cross-service message definitions, entity event producers, message bus consumers.

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

> **Note:** Search for `project-structure-reference.md` or the project's service directories to discover the platform's service map, data ownership matrix, and shared infrastructure components.

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
│  Producer  │── MsgBus  ────▶ │  Consumer  │
└────────────┘                   └────────────┘
```

**⚠️ MUST READ:** CLAUDE.md for Entity Event Bus Producer and Message Bus Consumer implementation patterns.

### Pattern 2: Direct API Call

**Use when**: Real-time data needed, no local copy required.

```csharp
// In Service A, calling Service B API
public class ServiceBApiClient
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

> **Note:** Search for `project-structure-reference.md` or the project's documentation for the entity ownership matrix. Each entity should have exactly ONE owning service; consumers receive synced copies via message bus.

## Synchronization Patterns

### Full Sync (Initial/Recovery)

```csharp
// For initial data population or recovery
public class FullSyncJob : BackgroundJobExecutor // project background job base (see docs/project-reference/backend-patterns-reference.md)
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
internal sealed class EmployeeSyncConsumer : MessageBusConsumer<EmployeeEventBusMessage> // project message bus base (see docs/project-reference/backend-patterns-reference.md)
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

Use `LastMessageSyncDate` for ordering - only update if message is newer. See CLAUDE.md Message Bus Consumer pattern for full implementation.

## Integration Checklist

### Before Integration

- [ ] Define data ownership clearly
- [ ] Document which fields sync
- [ ] Plan for missing dependencies
- [ ] Define conflict resolution strategy

### Implementation

- [ ] Message defined in shared project
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
# Check message broker queues (search for: queue management commands)

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

## Related

- `arch-security-review`
- `api-design`

---

**IMPORTANT Task Planning Notes (MUST FOLLOW)**

- Always plan and break work into many small todo tasks
- Always add a final review todo task to verify work quality and identify fixes/enhancements
