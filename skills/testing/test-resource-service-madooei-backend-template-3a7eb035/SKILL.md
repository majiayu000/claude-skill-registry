---
name: test-resource-service
description: Test resource services that handle CRUD operations. Use when testing services that extend BaseService with authorization and event emission. Triggers on "test note service", "test resource service", "test crud service".
---

# Test Resource Service

Tests resource services that extend `BaseService` and perform CRUD operations with authorization and event emission.

## Quick Reference

**Location**: `tests/services/{entity-name}.service.test.ts`
**Dependencies**: MockDB repository, vitest, user fixtures

## Test Structure

```typescript
import { describe, it, expect, beforeEach, vi } from "vitest";
import { {Entity}Service } from "@/services/{entity-name}.service";
import { MockDb{Entity}Repository } from "@/repositories/mockdb/{entity-name}.mockdb.repository";
import type { Create{Entity}Type, {Entity}Type } from "@/schemas/{entity-name}.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import { UnauthorizedError } from "@/errors";
import { appEvents } from "@/events/event-emitter";

// User fixtures
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

describe("{Entity}Service", () => {
  let repository: MockDb{Entity}Repository;
  let service: {Entity}Service;

  beforeEach(() => {
    repository = new MockDb{Entity}Repository();
    service = new {Entity}Service(repository);
    repository.clear();
    appEvents.removeAllListeners();
  });

  // Test groups...
});
```

## Test Categories

### 1. Create Tests

```typescript
describe("create", () => {
  it("allows admin to create", async () => {
    const data: Create{Entity}Type = { /* valid data */ };
    const result = await service.create(data, adminUser);
    expect(result.createdBy).toBe(adminUser.userId);
  });

  it("allows regular user to create", async () => {
    const data: Create{Entity}Type = { /* valid data */ };
    const result = await service.create(data, regularUser);
    expect(result.createdBy).toBe(regularUser.userId);
  });
});
```

### 2. GetAll Tests (Authorization Filtering)

```typescript
describe("getAll", () => {
  beforeEach(async () => {
    await service.create(
      {
        /* data */
      },
      regularUser,
    );
    await service.create(
      {
        /* data */
      },
      adminUser,
    );
    await service.create(
      {
        /* data */
      },
      otherUser,
    );
  });

  it("returns all items for admin", async () => {
    const result = await service.getAll({}, adminUser);
    expect(result.data.length).toBe(3);
  });

  it("returns only user's items for regular user", async () => {
    const result = await service.getAll({}, regularUser);
    expect(result.data.length).toBe(1);
    expect(
      result.data.every((item) => item.createdBy === regularUser.userId),
    ).toBe(true);
  });

  it("supports search and pagination", async () => {
    const result = await service.getAll(
      { search: "term", page: 1, limit: 10 },
      adminUser,
    );
    // Assert filtered results
  });
});
```

### 3. GetById Tests (Authorization)

```typescript
describe("getById", () => {
  let item: {Entity}Type;

  beforeEach(async () => {
    item = await service.create({ /* data */ }, regularUser);
  });

  it("allows owner to get their item", async () => {
    const found = await service.getById(item.id, regularUser);
    expect(found).not.toBeNull();
    expect(found!.id).toBe(item.id);
  });

  it("allows admin to get any item", async () => {
    const found = await service.getById(item.id, adminUser);
    expect(found).not.toBeNull();
  });

  it("denies other users", async () => {
    await expect(service.getById(item.id, otherUser)).rejects.toThrow(UnauthorizedError);
  });

  it("returns null for non-existent item", async () => {
    await expect(service.getById("not-exist", adminUser)).resolves.toBeNull();
  });
});
```

### 4. Update Tests (Authorization)

```typescript
describe("update", () => {
  let item: {Entity}Type;

  beforeEach(async () => {
    item = await service.create({ /* data */ }, regularUser);
  });

  it("allows owner to update", async () => {
    const updated = await service.update(item.id, { /* new data */ }, regularUser);
    expect(updated).not.toBeNull();
  });

  it("allows admin to update", async () => {
    const updated = await service.update(item.id, { /* new data */ }, adminUser);
    expect(updated).not.toBeNull();
  });

  it("denies other users", async () => {
    await expect(service.update(item.id, { /* data */ }, otherUser)).rejects.toThrow(UnauthorizedError);
  });

  it("returns null for non-existent item", async () => {
    await expect(service.update("not-exist", { /* data */ }, adminUser)).resolves.toBeNull();
  });
});
```

### 5. Delete Tests (Authorization)

```typescript
describe("delete", () => {
  let item: {Entity}Type;

  beforeEach(async () => {
    item = await service.create({ /* data */ }, regularUser);
  });

  it("allows owner to delete", async () => {
    const result = await service.delete(item.id, regularUser);
    expect(result).toBe(true);
  });

  it("allows admin to delete", async () => {
    const result = await service.delete(item.id, adminUser);
    expect(result).toBe(true);
  });

  it("denies other users", async () => {
    await expect(service.delete(item.id, otherUser)).rejects.toThrow(UnauthorizedError);
  });

  it("returns false for non-existent item", async () => {
    await expect(service.delete("not-exist", adminUser)).resolves.toBe(false);
  });
});
```

### 6. Event Emission Tests

```typescript
describe("Event Emission", () => {
  it("emits created event after successful creation", async () => {
    const eventSpy = vi.fn();
    appEvents.on("{entities}:created", eventSpy);

    const item = await service.create(
      {
        /* data */
      },
      regularUser,
    );

    expect(eventSpy).toHaveBeenCalledWith({
      id: expect.any(String),
      action: "created",
      data: item,
      user: expect.objectContaining({
        userId: regularUser.userId,
        globalRole: regularUser.globalRole,
      }),
      timestamp: expect.any(Date),
      resourceType: "{entities}",
    });
  });

  it("emits updated event after successful update", async () => {
    const item = await service.create(
      {
        /* data */
      },
      regularUser,
    );

    const eventSpy = vi.fn();
    appEvents.on("{entities}:updated", eventSpy);

    await service.update(
      item.id,
      {
        /* new data */
      },
      regularUser,
    );

    expect(eventSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        action: "updated",
        resourceType: "{entities}",
      }),
    );
  });

  it("emits deleted event after successful deletion", async () => {
    const item = await service.create(
      {
        /* data */
      },
      regularUser,
    );

    const eventSpy = vi.fn();
    appEvents.on("{entities}:deleted", eventSpy);

    await service.delete(item.id, regularUser);

    expect(eventSpy).toHaveBeenCalledWith(
      expect.objectContaining({
        action: "deleted",
        resourceType: "{entities}",
      }),
    );
  });

  it("does not emit events for failed operations", async () => {
    const eventSpy = vi.fn();
    appEvents.on("{entities}:updated", eventSpy);
    appEvents.on("{entities}:deleted", eventSpy);

    await service.update(
      "non-existent",
      {
        /* data */
      },
      adminUser,
    );
    await service.delete("non-existent", adminUser);

    expect(eventSpy).not.toHaveBeenCalled();
  });

  it("does not emit events for unauthorized operations", async () => {
    const item = await service.create(
      {
        /* data */
      },
      regularUser,
    );

    const eventSpy = vi.fn();
    appEvents.on("{entities}:updated", eventSpy);

    try {
      await service.update(
        item.id,
        {
          /* data */
        },
        otherUser,
      );
    } catch {
      // Expected
    }

    expect(eventSpy).not.toHaveBeenCalled();
  });
});
```

## Key Patterns

### Use Real MockDB Repository

Inject the actual MockDB repository for integration-like tests:

```typescript
beforeEach(() => {
  repository = new MockDbNoteRepository();
  service = new NoteService(repository);
  repository.clear(); // Reset state
});
```

### Clear Event Listeners

Prevent test pollution by removing listeners:

```typescript
beforeEach(() => {
  appEvents.removeAllListeners();
});
```

### Test Authorization Matrix

| User Type | Own Resource | Other's Resource | Non-existent |
| --------- | ------------ | ---------------- | ------------ |
| Admin     | Allow        | Allow            | null/false   |
| Owner     | Allow        | Deny (throw)     | null/false   |
| Other     | Deny (throw) | Deny (throw)     | null/false   |

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a complete `note.service.test.ts` implementation.

## What NOT to Do

- Do NOT mock the repository methods (use real MockDB)
- Do NOT forget to clear repository between tests
- Do NOT forget to remove event listeners between tests
- Do NOT skip testing authorization for all user types
- Do NOT skip testing event emission for all operations

## See Also

- `test-service` - Guide for choosing test type
- `test-utility-service` - Testing utility services
- `create-resource-service` - Creating the service to test
