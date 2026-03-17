---
name: test-routes
description: Test route configurations with integration-style tests. Use when testing complete request/response cycles through routes. Triggers on "test routes", "test note routes", "integration test".
---

# Test Routes

Integration-style tests that exercise the full request/response cycle through routes.

## Quick Reference

**Location**: `tests/routes/{entity-name}.router.test.ts`
**Key technique**: Use `app.request()`, mock middleware, use real MockDB

## Test Structure

```typescript
import { describe, it, expect, beforeEach, vi, afterEach } from "vitest";
import type { Mock } from "vitest";
import { Hono, type Next } from "hono";
import { createNoteRoutes } from "@/routes/note.router";
import { NoteController } from "@/controllers/note.controller";
import { NoteService } from "@/services/note.service";
import { MockDbNoteRepository } from "@/repositories/mockdb/note.mockdb.repository";
import type { AppEnv } from "@/schemas/app-env.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import {
  globalErrorHandler,
  UnauthenticatedError,
  BadRequestError,
} from "@/errors";

describe("Note Routes", () => {
  let app: Hono<AppEnv>;
  let mockDbRepo: MockDbNoteRepository;
  let noteService: NoteService;
  let noteController: NoteController;
  let mockAuthMiddleware: Mock;
  let mockValidateFactory: Mock;

  const testUser: AuthenticatedUserContextType = {
    userId: "user-test-123",
    globalRole: "user",
  };

  beforeEach(async () => {
    // Mock auth middleware - sets user by default
    mockAuthMiddleware = vi.fn(async (c: any, next: Next) => {
      c.set("user", testUser);
      await next();
    });

    // Mock validation factory
    mockValidateFactory = vi.fn((config: any) => {
      return vi.fn(async (c: any, next: Next) => {
        if (config.source === "params") {
          c.set(config.varKey, { id: c.req.param("id") });
        } else if (config.source === "query") {
          c.set(config.varKey, c.req.query());
        } else if (config.source === "body") {
          c.set(config.varKey, await c.req.json());
        }
        await next();
      });
    });

    // Set up real repository and services
    mockDbRepo = new MockDbNoteRepository();
    mockDbRepo.clear();
    noteService = new NoteService(mockDbRepo);
    noteController = new NoteController(noteService);

    // Create app with error handler
    app = new Hono<AppEnv>();
    app.onError(globalErrorHandler);
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  const setupRoutes = () => {
    app.route(
      "/notes",
      createNoteRoutes({
        noteController,
        authMiddleware: mockAuthMiddleware,
        validate: mockValidateFactory,
      }),
    );
  };

  // Tests...
});
```

## Test Categories

### 1. Success Cases

```typescript
it("GET /notes - returns all notes for user", async () => {
  setupRoutes();
  await mockDbRepo.create({ content: "Note 1" }, testUser.userId);
  await mockDbRepo.create({ content: "Note 2" }, testUser.userId);

  const response = await app.request("/notes", { method: "GET" });

  expect(response.status).toBe(200);
  const body = await response.json();
  expect(body.data).toHaveLength(2);
});

it("GET /notes/:id - returns specific note", async () => {
  setupRoutes();
  const note = await mockDbRepo.create({ content: "Test" }, testUser.userId);

  const response = await app.request(`/notes/${note.id}`, { method: "GET" });

  expect(response.status).toBe(200);
  const body = await response.json();
  expect(body.id).toBe(note.id);
});

it("POST /notes - creates new note", async () => {
  setupRoutes();

  const response = await app.request("/notes", {
    method: "POST",
    body: JSON.stringify({ content: "New note" }),
    headers: { "Content-Type": "application/json" },
  });

  expect(response.status).toBe(200);
  const body = await response.json();
  expect(body.content).toBe("New note");
  expect(body.createdBy).toBe(testUser.userId);
});

it("PUT /notes/:id - updates note", async () => {
  setupRoutes();
  const note = await mockDbRepo.create(
    { content: "Original" },
    testUser.userId,
  );

  const response = await app.request(`/notes/${note.id}`, {
    method: "PUT",
    body: JSON.stringify({ content: "Updated" }),
    headers: { "Content-Type": "application/json" },
  });

  expect(response.status).toBe(200);
  const body = await response.json();
  expect(body.content).toBe("Updated");
});

it("DELETE /notes/:id - deletes note", async () => {
  setupRoutes();
  const note = await mockDbRepo.create(
    { content: "To delete" },
    testUser.userId,
  );

  const response = await app.request(`/notes/${note.id}`, { method: "DELETE" });

  expect(response.status).toBe(200);
  const dbNote = await mockDbRepo.findById(note.id);
  expect(dbNote).toBeNull();
});
```

### 2. Error Cases

```typescript
it("returns 404 for non-existent resource", async () => {
  setupRoutes();

  const response = await app.request("/notes/non-existent", { method: "GET" });

  expect(response.status).toBe(404);
});

it("returns 401 when not authenticated", async () => {
  mockAuthMiddleware.mockImplementationOnce(async () => {
    throw new UnauthenticatedError("Not authenticated");
  });
  setupRoutes();

  const response = await app.request("/notes", { method: "GET" });

  expect(response.status).toBe(401);
});

it("returns 400 for invalid request body", async () => {
  mockValidateFactory.mockImplementation((config: any) => {
    if (config.source === "body") {
      return vi.fn(async () => {
        throw new BadRequestError("Invalid");
      });
    }
    return vi.fn(async (c: any, next: Next) => await next());
  });
  setupRoutes();

  const response = await app.request("/notes", {
    method: "POST",
    body: JSON.stringify({}),
    headers: { "Content-Type": "application/json" },
  });

  expect(response.status).toBe(400);
});

it("returns 403 when accessing other user's resource", async () => {
  setupRoutes();
  const otherUsersNote = await mockDbRepo.create(
    { content: "Other" },
    "other-user",
  );

  const response = await app.request(`/notes/${otherUsersNote.id}`, {
    method: "PUT",
    body: JSON.stringify({ content: "Hack" }),
    headers: { "Content-Type": "application/json" },
  });

  expect(response.status).toBe(403);
});
```

## Key Patterns

### Use app.request()

```typescript
// GET request
const response = await app.request("/notes", { method: "GET" });

// POST with body
const response = await app.request("/notes", {
  method: "POST",
  body: JSON.stringify({ content: "test" }),
  headers: { "Content-Type": "application/json" },
});
```

### Assert Status and Body

```typescript
expect(response.status).toBe(200);
const body = await response.json();
expect(body.data).toHaveLength(2);
```

### Override Middleware for Error Tests

```typescript
mockAuthMiddleware.mockImplementationOnce(async () => {
  throw new UnauthenticatedError();
});
setupRoutes(); // Set up AFTER mock override
```

### Use Real MockDB for State

```typescript
// Create test data
const note = await mockDbRepo.create({ content: "Test" }, testUser.userId);

// Verify database state after operation
const dbNote = await mockDbRepo.findById(note.id);
expect(dbNote).toBeNull();
```

## What NOT to Do

- Do NOT make actual HTTP requests to a running server
- Do NOT use production database
- Do NOT skip error case testing
- Do NOT forget to set up routes AFTER mock overrides

## See Also

- `create-routes` - Creating routes
- `test-controller` - Unit testing controllers
- `test-middleware` - Unit testing middleware
