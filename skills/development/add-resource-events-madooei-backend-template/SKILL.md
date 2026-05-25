---
name: add-resource-events
description: Add real-time event emission to a resource service. Use when adding SSE/real-time capabilities to a resource. Triggers on "add events", "real-time events", "SSE events".
---

# Add Resource Events

Enables real-time event emission for a resource service via Server-Sent Events (SSE).

## Quick Reference

**Event Infrastructure**:

- `src/events/event-emitter.ts` - Singleton `AppEventEmitter`
- `src/events/base.service.ts` - `BaseService` with `emitEvent()`
- `src/schemas/event.schema.ts` - Event type definitions
- `src/routes/events.router.ts` - SSE endpoint

**Event Pattern**: `{serviceName}:{action}` (e.g., `notes:created`, `notes:updated`)

## Prerequisites

To add events to a resource:

1. Service must extend `BaseService` (see `create-resource-service`)
2. Authorization methods for events in `AuthorizationService`

## How It Works

### 1. BaseService Provides emitEvent()

```typescript
// src/events/base.service.ts
export abstract class BaseService {
  constructor(protected serviceName: string) {}

  protected emitEvent<T>(
    action: ServiceEventType["action"],
    data: T,
    options?: {
      id?: string;
      user?: { userId: string; [key: string]: unknown };
    },
  ) {
    appEvents.emitServiceEvent(this.serviceName, {
      id: options?.id || uuidv4(),
      action,
      data,
      user: eventUser,
      timestamp: new Date(),
      resourceType: this.serviceName,
    });
  }
}
```

### 2. Resource Service Emits Events

```typescript
export class NoteService extends BaseService {
  constructor(...) {
    super("notes"); // Service name for event routing
  }

  async create(data, user) {
    // ... create logic ...

    this.emitEvent("created", note, { id: note.id, user });

    return note;
  }

  async update(id, data, user) {
    // ... update logic ...

    this.emitEvent("updated", updatedNote, { id: updatedNote.id, user });

    return updatedNote;
  }

  async delete(id, user) {
    // ... delete logic ...

    this.emitEvent("deleted", note, { id: note.id, user });

    return true;
  }
}
```

### 3. Events Router Streams to Clients

```typescript
// src/routes/events.router.ts
appEvents.on("notes:created", eventHandler);
appEvents.on("notes:updated", eventHandler);
appEvents.on("notes:deleted", eventHandler);
```

## Adding Events to a New Resource

### Step 1: Extend BaseService

Your service must extend `BaseService`:

```typescript
import { BaseService } from "@/events/base.service";

export class {Entity}Service extends BaseService {
  constructor(...) {
    super("{entities}"); // Plural for event namespace
  }
}
```

### Step 2: Emit Events in CRUD Methods

Add `emitEvent()` calls after successful operations:

```typescript
async create(data, user) {
  const {entity} = await this.repository.create(data, user.userId);

  this.emitEvent("created", {entity}, { id: {entity}.id, user });

  return {entity};
}

async update(id, data, user) {
  const updated = await this.repository.update(id, data);
  if (!updated) return null;

  this.emitEvent("updated", updated, { id: updated.id, user });

  return updated;
}

async delete(id, user) {
  const {entity} = await this.repository.findById(id);
  const deleted = await this.repository.remove(id);

  if (deleted) {
    this.emitEvent("deleted", {entity}, { id: {entity}.id, user });
  }

  return deleted;
}
```

### Step 3: Add Event Authorization

In `src/services/authorization.service.ts`:

```typescript
async canReceive{Entity}Event(
  user: AuthenticatedUserContextType,
  {entity}Data: { createdBy: string; [key: string]: unknown },
): Promise<boolean> {
  if (this.isAdmin(user)) return true;
  if ({entity}Data.createdBy === user.userId) return true;
  return false;
}
```

### Step 4: Update Events Router

In `src/routes/events.router.ts`, add listeners:

```typescript
// Listen to {entity} events
appEvents.on("{entities}:created", eventHandler);
appEvents.on("{entities}:updated", eventHandler);
appEvents.on("{entities}:deleted", eventHandler);
```

Update the `shouldUserReceiveEvent` function:

```typescript
async function shouldUserReceiveEvent(
  event: ServiceEventType,
  user: AuthenticatedUserContextType,
  authorizationService: AuthorizationService,
): Promise<boolean> {
  switch (event.resourceType) {
    case "notes":
      // ... existing ...
    case "{entities}":
      if (
        typeof event.data === "object" &&
        event.data !== null &&
        "createdBy" in event.data
      ) {
        return await authorizationService.canReceive{Entity}Event(
          user,
          event.data as { createdBy: string; [key: string]: unknown },
        );
      }
      return false;
    default:
      return false;
  }
}
```

### Step 5: Add Event Schema (Optional)

In `src/schemas/event.schema.ts`:

```typescript
export const {entity}EventSchema = serviceEventSchema.extend({
  data: z.object({
    id: z.string(),
    // ... entity-specific fields
    createdAt: z.date().optional(),
    updatedAt: z.date().optional(),
  }),
});

export type {Entity}EventType = z.infer<typeof {entity}EventSchema>;
```

## Event Flow

```
1. Client: POST /notes (create a note)
2. Controller: calls NoteService.create()
3. Service: creates note, calls this.emitEvent("created", note, ...)
4. BaseService: appEvents.emitServiceEvent("notes", { action: "created", ... })
5. EventEmitter: emits "notes:created" event
6. Events Router: catches event, checks authorization
7. SSE Stream: sends to authorized clients
8. Client: receives { event: "notes:created", data: {...} }
```

## Client-Side Usage

```javascript
const eventSource = new EventSource("/events", {
  headers: { Authorization: `Bearer ${token}` },
});

eventSource.addEventListener("notes:created", (event) => {
  const data = JSON.parse(event.data);
  console.log("New note:", data);
});

eventSource.addEventListener("notes:updated", (event) => {
  const data = JSON.parse(event.data);
  console.log("Updated note:", data);
});

eventSource.addEventListener("notes:deleted", (event) => {
  const data = JSON.parse(event.data);
  console.log("Deleted note:", data);
});
```

## What NOT to Do

- Do NOT emit events before confirming operation succeeded
- Do NOT emit events for failed/unauthorized operations
- Do NOT skip authorization checks in events router
- Do NOT forget to clean up event listeners on disconnect

## See Also

- `create-resource-service` - Creating services with event emission
- `create-routes` - Events router example
- `test-resource-service` - Testing event emission
