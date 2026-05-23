---
name: setup-events
description: Configure event-driven architecture with event emitter and base service. Use when adding real-time updates or event system. Triggers on "setup events", "add events", "event system", "SSE", "real-time".
---

# Setup Events

Configures event-driven architecture infrastructure including an event emitter, base service class for event emission, and event schema.

## Quick Reference

**Files created**:

- `src/events/event-emitter.ts` - Central event hub
- `src/events/base.service.ts` - Abstract service with event emission
- `src/schemas/event.schema.ts` - Event type definitions

**When to use**: When you need real-time updates via SSE or event-driven architecture

## Prerequisites

- Project bootstrapped with `bootstrap-project`
- `uuid` package installed

## Instructions

### Phase 1: Install Dependencies

#### Step 1: Install UUID Package

```bash
pnpm add uuid
pnpm add -D @types/uuid
```

### Phase 2: Create Event Infrastructure

#### Step 2: Create Events Directory

```bash
mkdir -p src/events
```

#### Step 3: Create Event Emitter

Create `src/events/event-emitter.ts`:

```typescript
import { EventEmitter } from "events";
import type { ServiceEventType } from "@/schemas/event.schema";

class AppEventEmitter extends EventEmitter {
  emitServiceEvent(serviceName: string, event: ServiceEventType) {
    this.emit(`${serviceName}:${event.action}`, event);
  }
}

export const appEvents = new AppEventEmitter();
```

#### Step 4: Create Base Service

Create `src/events/base.service.ts`:

```typescript
import { appEvents } from "./event-emitter";
import type { ServiceEventType } from "@/schemas/event.schema";
import { v4 as uuidv4 } from "uuid";

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
    const eventUser = options?.user
      ? {
          id: options.user.userId,
          ...options.user,
        }
      : undefined;

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

### Phase 3: Create Event Schema

#### Step 5: Create Event Schema

Create `src/schemas/event.schema.ts`:

```typescript
import { z } from "zod";

export const serviceEventSchema = z.object({
  id: z.string(), // Event's own ID for storage/audit
  action: z.enum(["created", "updated", "deleted"]),
  data: z.unknown(), // Will be typed based on specific entity
  user: z
    .object({
      id: z.string(),
    })
    .passthrough()
    .optional(), // Optional for system events
  timestamp: z.date(), // When event occurred
  resourceType: z.string(), // 'notes', 'users', 'projects', etc.
});

export type ServiceEventType = z.infer<typeof serviceEventSchema>;
```

## Usage Patterns

### Extending BaseService

Services that need event emission should extend `BaseService`:

```typescript
import { BaseService } from "@/events/base.service";
import type { INoteRepository } from "@/repositories/note.repository";
import type { CreateNoteType, NoteType } from "@/schemas/note.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";

export class NoteService extends BaseService {
  constructor(private noteRepository: INoteRepository) {
    super("notes"); // Service name for event routing
  }

  async create(
    data: CreateNoteType,
    user: AuthenticatedUserContextType,
  ): Promise<NoteType> {
    const note = await this.noteRepository.create(data, user.userId);

    // Emit event after successful operation
    this.emitEvent("created", note, {
      id: note.id,
      user,
    });

    return note;
  }

  async update(
    id: string,
    data: UpdateNoteType,
    user: AuthenticatedUserContextType,
  ): Promise<NoteType> {
    const note = await this.noteRepository.update(id, data);

    this.emitEvent("updated", note, {
      id: note.id,
      user,
    });

    return note;
  }

  async delete(id: string, user: AuthenticatedUserContextType): Promise<void> {
    await this.noteRepository.remove(id);

    this.emitEvent(
      "deleted",
      { id },
      {
        id,
        user,
      },
    );
  }
}
```

### Listening to Events

```typescript
import { appEvents } from "@/events/event-emitter";
import type { ServiceEventType } from "@/schemas/event.schema";

// Listen to specific event types
appEvents.on("notes:created", (event: ServiceEventType) => {
  console.log("Note created:", event.data);
});

appEvents.on("notes:updated", (event: ServiceEventType) => {
  console.log("Note updated:", event.data);
});

appEvents.on("notes:deleted", (event: ServiceEventType) => {
  console.log("Note deleted:", event.data);
});
```

### SSE Endpoint Pattern

For real-time updates via Server-Sent Events, see the `add-resource-events` skill. Basic pattern:

```typescript
import { Hono } from "hono";
import { appEvents } from "@/events/event-emitter";
import type { AppEnv } from "@/schemas/app-env.schema";
import type { ServiceEventType } from "@/schemas/event.schema";

export function createEventsRoutes() {
  const router = new Hono<AppEnv>();

  router.get("/", async (c) => {
    const readable = new ReadableStream({
      start(controller) {
        // Send initial connection message
        controller.enqueue(
          new TextEncoder().encode(`data: {"type":"connected"}\n\n`),
        );

        const eventHandler = (event: ServiceEventType) => {
          const eventData = `event: ${event.resourceType}:${event.action}\ndata: ${JSON.stringify(event)}\n\n`;
          controller.enqueue(new TextEncoder().encode(eventData));
        };

        // Listen to events
        appEvents.on("notes:created", eventHandler);
        appEvents.on("notes:updated", eventHandler);
        appEvents.on("notes:deleted", eventHandler);

        // Store cleanup function
        (controller as any).cleanup = () => {
          appEvents.off("notes:created", eventHandler);
          appEvents.off("notes:updated", eventHandler);
          appEvents.off("notes:deleted", eventHandler);
        };
      },
      cancel(controller) {
        if ((controller as any).cleanup) {
          (controller as any).cleanup();
        }
      },
    });

    return new Response(readable, {
      headers: {
        "Content-Type": "text/event-stream",
        "Cache-Control": "no-cache",
        Connection: "keep-alive",
      },
    });
  });

  return router;
}
```

## Event Structure

Events follow this structure:

```typescript
{
  id: "uuid-v4-event-id",           // Unique event ID
  action: "created" | "updated" | "deleted",
  data: { /* entity data */ },       // The affected entity
  user: {                            // User who triggered the event
    id: "user-id",
    userId: "user-id",
    globalRole: "user"
  },
  timestamp: Date,                   // When event occurred
  resourceType: "notes"              // Service/resource name
}
```

## Files Created Summary

```plaintext
src/
├── events/
│   ├── event-emitter.ts   # Central event hub
│   └── base.service.ts    # Abstract service with event emission
└── schemas/
    └── event.schema.ts    # Event type definitions
```

## Testing Events

```typescript
import { describe, it, expect, vi } from "vitest";
import { appEvents } from "@/events/event-emitter";
import { NoteService } from "@/services/note.service";

describe("NoteService Event Emission", () => {
  it("should emit created event after successful note creation", async () => {
    const eventSpy = vi.spyOn(appEvents, "emitServiceEvent");

    const noteService = new NoteService(mockRepository);
    const note = await noteService.create(validNoteData, mockUser);

    expect(eventSpy).toHaveBeenCalledWith("notes", {
      id: expect.any(String),
      action: "created",
      data: note,
      user: {
        id: mockUser.userId,
        ...mockUser,
      },
      timestamp: expect.any(Date),
      resourceType: "notes",
    });
  });
});
```

## What NOT to Do

- Do NOT emit events before the operation succeeds (emit after success)
- Do NOT include sensitive data in events (passwords, tokens, etc.)
- Do NOT forget to clean up event listeners when SSE connections close
- Do NOT create circular event dependencies
- Do NOT emit events in the constructor

## See Also

- `add-resource-events` - Add SSE endpoint with authorization
- `create-resource-service` - Services that extend BaseService
- `test-resource-service` - Testing event emission
