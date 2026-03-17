---
name: test-events-router
description: Test the SSE events router and real-time event streaming. Use when testing Server-Sent Events endpoint or event authorization. Triggers on "test events", "test sse", "test events router", "test real-time".
---

# Test Events Router

Tests the Server-Sent Events (SSE) endpoint that streams real-time events to authenticated clients.

## Quick Reference

**Location**: `tests/routes/events.router.test.ts`
**Key challenges**: SSE streaming, async event emission, authorization filtering

## Prerequisites

Before testing events router:

1. Events infrastructure exists (`src/events/`, `src/routes/events.router.ts`)
2. At least one resource service emits events
3. Authorization methods for events exist in `AuthorizationService`

## Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import type { Mock } from "vitest";
import { Hono, type Next } from "hono";
import { createEventsRoutes } from "@/routes/events.router";
import { appEvents } from "@/events/event-emitter";
import { AuthorizationService } from "@/services/authorization.service";
import type { AppEnv } from "@/schemas/app-env.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import type { ServiceEventType } from "@/schemas/event.schema";
import { globalErrorHandler, UnauthenticatedError } from "@/errors";

// Mock the AuthorizationService module
vi.mock("@/services/authorization.service");

describe("Events Router", () => {
  let app: Hono<AppEnv>;
  let mockAuthMiddleware: Mock;
  let mockAuthorizationService: AuthorizationService;

  const adminUser: AuthenticatedUserContextType = {
    userId: "admin-1",
    globalRole: "admin",
  };
  const regularUser: AuthenticatedUserContextType = {
    userId: "user-1",
    globalRole: "user",
  };
  const otherUser: AuthenticatedUserContextType = {
    userId: "user-2",
    globalRole: "user",
  };

  beforeEach(() => {
    // Mock auth middleware
    mockAuthMiddleware = vi.fn(async (c: any, next: Next) => {
      c.set("user", regularUser);
      await next();
    });

    // Mock AuthorizationService methods
    // IMPORTANT: Use a function expression, NOT an arrow function!
    // Arrow functions cannot be used with `new`, and the router calls
    // `new AuthorizationService()` internally.
    mockAuthorizationService = {
      canReceiveNoteEvent: vi.fn().mockResolvedValue(true),
      isAdmin: vi.fn().mockReturnValue(false),
    } as any;

    vi.mocked(AuthorizationService).mockImplementation(function () {
      return mockAuthorizationService;
    } as any);

    // Create app
    app = new Hono<AppEnv>();
    app.onError(globalErrorHandler);

    // Clear event listeners
    appEvents.removeAllListeners();
  });

  afterEach(() => {
    vi.clearAllMocks();
    appEvents.removeAllListeners();
  });

  const setupRoutes = (user?: AuthenticatedUserContextType) => {
    if (user) {
      mockAuthMiddleware = vi.fn(async (c: any, next: Next) => {
        c.set("user", user);
        await next();
      });
    }
    app.route(
      "/events",
      createEventsRoutes({ authMiddleware: mockAuthMiddleware }),
    );
  };

  // Tests...
});
```

## Test Categories

### 1. Authentication Tests

```typescript
describe("Authentication", () => {
  it("returns 401 when not authenticated", async () => {
    mockAuthMiddleware = vi.fn(async () => {
      throw new UnauthenticatedError("Not authenticated");
    });
    setupRoutes();

    const response = await app.request("/events", { method: "GET" });

    expect(response.status).toBe(401);
  });

  it("allows authenticated users to connect", async () => {
    setupRoutes(regularUser);

    const response = await app.request("/events", { method: "GET" });

    // SSE endpoint returns streaming response
    expect(response.status).toBe(200);
    expect(response.headers.get("content-type")).toContain("text/event-stream");
  });
});
```

### 2. SSE Response Format Tests

```typescript
describe("SSE Response Format", () => {
  it("returns correct SSE headers", async () => {
    setupRoutes(regularUser);

    const response = await app.request("/events", { method: "GET" });

    expect(response.headers.get("content-type")).toBe(
      "text/event-stream; charset=utf-8",
    );
    expect(response.headers.get("cache-control")).toBe("no-cache");
    expect(response.headers.get("connection")).toBe("keep-alive");
  });

  it("sends initial connection event", async () => {
    setupRoutes(regularUser);

    const response = await app.request("/events", { method: "GET" });
    const text = await response.text();

    // Should include connection confirmation
    expect(text).toContain("event: connected");
    expect(text).toContain(`data: {"userId":"${regularUser.userId}"}`);
  });
});
```

### 3. Event Emission Tests

```typescript
describe("Event Emission", () => {
  it("streams events to connected clients", async () => {
    setupRoutes(regularUser);

    // Start SSE connection
    const responsePromise = app.request("/events", { method: "GET" });

    // Give time for connection to establish
    await new Promise((r) => setTimeout(r, 50));

    // Emit an event
    const testEvent: ServiceEventType = {
      id: "event-1",
      action: "created",
      data: { id: "note-1", content: "Test", createdBy: regularUser.userId },
      user: { id: regularUser.userId },
      timestamp: new Date(),
      resourceType: "notes",
    };
    appEvents.emit("notes:created", testEvent);

    // Get response
    const response = await responsePromise;
    const text = await response.text();

    expect(text).toContain("event: notes:created");
    expect(text).toContain('"id":"note-1"');
  });
});
```

### 4. Event Authorization Tests

```typescript
describe("Event Authorization", () => {
  it("sends events for user's own resources", async () => {
    setupRoutes(regularUser);

    const responsePromise = app.request("/events", { method: "GET" });
    await new Promise((r) => setTimeout(r, 50));

    // Event for user's own note
    const ownEvent: ServiceEventType = {
      id: "event-1",
      action: "created",
      data: { id: "note-1", createdBy: regularUser.userId },
      user: { id: regularUser.userId },
      timestamp: new Date(),
      resourceType: "notes",
    };
    appEvents.emit("notes:created", ownEvent);

    const response = await responsePromise;
    const text = await response.text();

    expect(text).toContain("notes:created");
  });

  it("does not send events for other users' resources", async () => {
    setupRoutes(regularUser);

    const responsePromise = app.request("/events", { method: "GET" });
    await new Promise((r) => setTimeout(r, 50));

    // Event for another user's note
    const otherEvent: ServiceEventType = {
      id: "event-2",
      action: "created",
      data: { id: "note-2", createdBy: otherUser.userId },
      user: { id: otherUser.userId },
      timestamp: new Date(),
      resourceType: "notes",
    };
    appEvents.emit("notes:created", otherEvent);

    const response = await responsePromise;
    const text = await response.text();

    // Should not contain the other user's event data
    expect(text).not.toContain('"id":"note-2"');
  });

  it("admin receives all events", async () => {
    setupRoutes(adminUser);

    const responsePromise = app.request("/events", { method: "GET" });
    await new Promise((r) => setTimeout(r, 50));

    // Event from another user
    const otherEvent: ServiceEventType = {
      id: "event-1",
      action: "updated",
      data: { id: "note-1", createdBy: otherUser.userId },
      user: { id: otherUser.userId },
      timestamp: new Date(),
      resourceType: "notes",
    };
    appEvents.emit("notes:updated", otherEvent);

    const response = await responsePromise;
    const text = await response.text();

    // Admin should receive the event
    expect(text).toContain("notes:updated");
    expect(text).toContain('"id":"note-1"');
  });
});
```

### 5. Multiple Event Types Tests

```typescript
describe("Multiple Event Types", () => {
  it("handles created, updated, and deleted events", async () => {
    setupRoutes(adminUser);

    const responsePromise = app.request("/events", { method: "GET" });
    await new Promise((r) => setTimeout(r, 50));

    // Emit different event types
    const baseEvent = {
      id: "event-1",
      data: { id: "note-1", createdBy: regularUser.userId },
      user: { id: regularUser.userId },
      timestamp: new Date(),
      resourceType: "notes",
    };

    appEvents.emit("notes:created", { ...baseEvent, action: "created" });
    appEvents.emit("notes:updated", {
      ...baseEvent,
      id: "event-2",
      action: "updated",
    });
    appEvents.emit("notes:deleted", {
      ...baseEvent,
      id: "event-3",
      action: "deleted",
    });

    const response = await responsePromise;
    const text = await response.text();

    expect(text).toContain("event: notes:created");
    expect(text).toContain("event: notes:updated");
    expect(text).toContain("event: notes:deleted");
  });

  it("handles events from multiple resource types", async () => {
    setupRoutes(adminUser);

    const responsePromise = app.request("/events", { method: "GET" });
    await new Promise((r) => setTimeout(r, 50));

    // Note event
    appEvents.emit("notes:created", {
      id: "event-1",
      action: "created",
      data: { id: "note-1", createdBy: adminUser.userId },
      user: { id: adminUser.userId },
      timestamp: new Date(),
      resourceType: "notes",
    });

    // Project event (if exists)
    appEvents.emit("projects:created", {
      id: "event-2",
      action: "created",
      data: { id: "project-1", createdBy: adminUser.userId },
      user: { id: adminUser.userId },
      timestamp: new Date(),
      resourceType: "projects",
    });

    const response = await responsePromise;
    const text = await response.text();

    expect(text).toContain("notes:created");
    // Only check for projects if that resource exists
    // expect(text).toContain("projects:created");
  });
});
```

### 6. Connection Lifecycle Tests

```typescript
describe("Connection Lifecycle", () => {
  it("handles client disconnect gracefully", async () => {
    setupRoutes(regularUser);

    // This is difficult to test without actual streaming
    // The key behavior is that event listeners are cleaned up on disconnect

    const response = await app.request("/events", { method: "GET" });
    expect(response.status).toBe(200);

    // In a real scenario, you'd abort the request and verify cleanup
    // This is primarily tested through integration tests
  });

  it("sends heartbeat/keepalive", async () => {
    setupRoutes(regularUser);

    const response = await app.request("/events", { method: "GET" });
    const text = await response.text();

    // Check for keepalive comment or ping event
    // Implementation depends on your events router
    // expect(text).toContain(": keepalive");
  });
});
```

## Testing SSE with Hono's Testing Utilities

Hono's `app.request()` waits for the entire response, which complicates streaming tests. For more realistic tests:

### Option 1: Use Short-Lived Streams

```typescript
// Configure events router to close after sending events
const response = await app.request("/events?timeout=100", { method: "GET" });
```

### Option 2: Use Manual Event Emission Timing

```typescript
// Set up a delayed event emission before starting request
setTimeout(() => {
  appEvents.emit("notes:created", testEvent);
}, 50);

const response = await app.request("/events", { method: "GET" });
```

### Option 3: Integration Tests with Real Server

For comprehensive SSE testing, consider integration tests with a running server:

```typescript
import { EventSource } from "eventsource";

it("streams events in real-time", async () => {
  const events: ServiceEventType[] = [];

  const es = new EventSource("http://localhost:3000/events", {
    headers: { Authorization: "Bearer test-token" },
  });

  es.addEventListener("notes:created", (e) => {
    events.push(JSON.parse(e.data));
  });

  // Trigger event via API call
  await fetch("http://localhost:3000/notes", {
    method: "POST",
    headers: {
      Authorization: "Bearer test-token",
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ content: "Test note" }),
  });

  // Wait for event
  await new Promise((r) => setTimeout(r, 100));

  expect(events).toHaveLength(1);
  es.close();
});
```

## What to Test

| Category          | Test Cases                                       |
| ----------------- | ------------------------------------------------ |
| **Auth**          | Unauthenticated rejected, authenticated accepted |
| **Headers**       | Content-Type, Cache-Control, Connection          |
| **Format**        | Event name, data JSON, newlines                  |
| **Authorization** | Own resources, others' resources, admin access   |
| **Events**        | created, updated, deleted for each resource      |
| **Lifecycle**     | Connection, disconnect, cleanup                  |

## What NOT to Do

- Do NOT forget to clear event listeners in afterEach
- Do NOT make tests depend on timing (use proper async patterns)
- Do NOT skip authorization tests
- Do NOT test only happy paths
- Do NOT use arrow functions when mocking classes that are instantiated with `new`

## Common Pitfalls

### Mocking Classes with `new`

When mocking a class like `AuthorizationService` that is instantiated with `new` inside the code under test, you **must** use a function expression, not an arrow function:

```typescript
// ❌ WRONG - Arrow functions cannot be used with `new`
vi.mocked(AuthorizationService).mockImplementation(
  () => mockAuthorizationService,
);
// Error: () => mockAuthorizationService is not a constructor

// ✅ CORRECT - Use a function expression
vi.mocked(AuthorizationService).mockImplementation(function () {
  return mockAuthorizationService;
} as any);
```

This is because JavaScript arrow functions don't have their own `this` binding and cannot be used as constructors.

## See Also

- `add-resource-events` - Adding events to a resource
- `create-routes` - Creating the events router
- `test-resource-service` - Testing event emission from services
