---
name: test-mockdb-repository
description: Write tests for MockDB (in-memory) repository implementations. Use when testing MockDB repositories, in-memory data access, or mock repository behavior. Triggers on "test mockdb", "mockdb tests", "test mock repository".
---

# Test MockDB Repository

Write Vitest tests for MockDB (in-memory) repository implementations. No external dependencies required.

## Quick Reference

**Location**: `tests/repositories/{entity-name}.mockdb.repository.test.ts`
**Run tests**: `pnpm test -- tests/repositories/{entity-name}.mockdb.repository.test.ts`

## Test Structure

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { MockDb{Entity}Repository } from "@/repositories/mockdb/{entity-name}.mockdb.repository";
import type { Create{Entity}Type } from "@/schemas/{entity-name}.schema";

const userId = "user-1";
const otherUserId = "user-2";

describe("MockDb{Entity}Repository", () => {
  let repo: MockDb{Entity}Repository;

  beforeEach(() => {
    repo = new MockDb{Entity}Repository();
    repo.clear(); // Clean slate for each test
  });

  // Test cases...
});
```

## Test Cases

### Create

```typescript
describe("create", () => {
  it("creates an entity and returns it", async () => {
    const data: Create{Entity}Type = { content: "Test content" };
    const entity = await repo.create(data, userId);

    expect(entity.id).toBeDefined();
    expect(entity.content).toBe("Test content");
    expect(entity.createdBy).toBe(userId);
    expect(entity.createdAt).toBeInstanceOf(Date);
    expect(entity.updatedAt).toBeInstanceOf(Date);
  });
});
```

### FindById

```typescript
describe("findById", () => {
  it("returns entity by id", async () => {
    const created = await repo.create({ content: "Find me" }, userId);
    const found = await repo.findById(created.id);

    expect(found).not.toBeNull();
    expect(found!.id).toBe(created.id);
  });

  it("returns null if not found", async () => {
    const found = await repo.findById("not-exist");
    expect(found).toBeNull();
  });
});
```

### FindAll

```typescript
describe("findAll", () => {
  beforeEach(async () => {
    await repo.create({ content: "A" }, userId);
    await repo.create({ content: "B" }, userId);
    await repo.create({ content: "C" }, otherUserId);
  });

  it("returns all entities", async () => {
    const result = await repo.findAll({});
    expect(result.data.length).toBe(3);
  });

  it("filters by createdBy", async () => {
    const result = await repo.findAll({ createdBy: userId });
    expect(result.data.length).toBe(2);
    expect(result.data.every((e) => e.createdBy === userId)).toBe(true);
  });

  it("searches by content", async () => {
    const result = await repo.findAll({ search: "B" });
    expect(result.data.length).toBe(1);
    expect(result.data[0].content).toBe("B");
  });

  it("paginates results", async () => {
    const result = await repo.findAll({ page: 2, limit: 2 });
    expect(result.data.length).toBe(1);
    expect(result.page).toBe(2);
    expect(result.limit).toBe(2);
  });

  it("sorts results", async () => {
    const result = await repo.findAll({ sortBy: "content", sortOrder: "desc" });
    expect(result.data[0].content >= result.data[1].content).toBe(true);
  });
});
```

### Update

```typescript
describe("update", () => {
  it("updates entity fields", async () => {
    const entity = await repo.create({ content: "Old" }, userId);
    await new Promise((r) => setTimeout(r, 10)); // Ensure updatedAt changes

    const updated = await repo.update(entity.id, { content: "New" });

    expect(updated).not.toBeNull();
    expect(updated!.content).toBe("New");
    expect(updated!.updatedAt).not.toEqual(entity.updatedAt);
  });

  it("returns null if entity does not exist", async () => {
    const updated = await repo.update("not-exist", { content: "X" });
    expect(updated).toBeNull();
  });
});
```

### Remove

```typescript
describe("remove", () => {
  it("deletes entity and returns true", async () => {
    const entity = await repo.create({ content: "Del" }, userId);
    const result = await repo.remove(entity.id);

    expect(result).toBe(true);
    expect(await repo.findById(entity.id)).toBeNull();
  });

  it("returns false if entity does not exist", async () => {
    const result = await repo.remove("not-exist");
    expect(result).toBe(false);
  });
});
```

## What to Test

| Category     | Test Cases                                                    |
| ------------ | ------------------------------------------------------------- |
| **Create**   | Returns entity with ID, sets timestamps, sets createdBy       |
| **FindById** | Returns entity, returns null for not found                    |
| **FindAll**  | Returns all, filters, searches, paginates, sorts              |
| **Update**   | Updates fields, updates timestamp, returns null for not found |
| **Remove**   | Deletes and returns true, returns false for not found         |

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a complete test file example.

## What NOT to Do

- Do NOT forget to call `repo.clear()` in `beforeEach`
- Do NOT test the interface - test the implementation
- Do NOT skip pagination/filter/sort tests
- Do NOT mock the repository - test the actual implementation
