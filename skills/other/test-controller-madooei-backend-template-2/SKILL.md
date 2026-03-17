---
name: test-controller
description: Test controllers that handle HTTP requests. Use when testing controller methods that call services and return responses. Triggers on "test controller", "test note controller".
---

# Test Controller

Tests controllers by mocking services and Hono context.

## Quick Reference

**Location**: `tests/controllers/{entity-name}.controller.test.ts`
**Key technique**: Mock service methods, create mock Hono context

## Test Structure

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { {Entity}Controller } from "@/controllers/{entity-name}.controller";
import type { {Entity}Service } from "@/services/{entity-name}.service";
import type {
  Create{Entity}Type,
  Update{Entity}Type,
  {Entity}QueryParamsType,
  {Entity}Type,
} from "@/schemas/{entity-name}.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import type { PaginatedResultType, EntityIdParamType } from "@/schemas/shared.schema";
import { NotFoundError } from "@/errors";

// Mock context helper
interface MockContextConfig {
  user?: AuthenticatedUserContextType;
  validatedQuery?: {Entity}QueryParamsType;
  validatedParams?: EntityIdParamType;
  validatedBody?: Create{Entity}Type | Update{Entity}Type;
}

const createMockContext = (config: MockContextConfig = {}) => {
  const mockJson = vi.fn((data) => data);
  return {
    var: {
      user: config.user || ({} as AuthenticatedUserContextType),
      validatedQuery: config.validatedQuery || ({} as {Entity}QueryParamsType),
      validatedParams: config.validatedParams || ({} as EntityIdParamType),
      validatedBody: config.validatedBody || ({} as Create{Entity}Type | Update{Entity}Type),
    },
    json: mockJson,
  } as any;
};

// Mock service
const mockService = {
  getAll: vi.fn(),
  getById: vi.fn(),
  create: vi.fn(),
  update: vi.fn(),
  delete: vi.fn(),
};

describe("{Entity}Controller", () => {
  let controller: {Entity}Controller;
  let user: AuthenticatedUserContextType;
  let sample{Entity}: {Entity}Type;

  beforeEach(() => {
    controller = new {Entity}Controller(mockService as unknown as {Entity}Service);
    user = { userId: "user-1", globalRole: "user" };
    sample{Entity} = {
      id: "{entity}-1",
      // ... entity fields
      createdBy: user.userId,
      createdAt: new Date(),
      updatedAt: new Date(),
    };
  });

  afterEach(() => {
    vi.clearAllMocks();
  });

  // Test groups...
});
```

## Test Categories

### 1. getAll Tests

```typescript
describe("getAll", () => {
  it("returns items from service and calls c.json", async () => {
    const query: {Entity}QueryParamsType = { page: 1, limit: 10 };
    const result: PaginatedResultType<{Entity}Type> = {
      data: [sample{Entity}],
      total: 1,
      page: 1,
      limit: 10,
      totalPages: 1,
    };
    mockService.getAll.mockResolvedValue(result);

    const mockCtx = createMockContext({ user, validatedQuery: query });
    const response = await controller.getAll(mockCtx);

    expect(mockService.getAll).toHaveBeenCalledWith(query, user);
    expect(mockCtx.json).toHaveBeenCalledWith(result);
    expect(response).toEqual(result);
  });
});
```

### 2. getById Tests

```typescript
describe("getById", () => {
  it("returns item when found", async () => {
    const params: EntityIdParamType = { id: sample{Entity}.id };
    mockService.getById.mockResolvedValue(sample{Entity});

    const mockCtx = createMockContext({ user, validatedParams: params });
    const response = await controller.getById(mockCtx);

    expect(mockService.getById).toHaveBeenCalledWith(params.id, user);
    expect(mockCtx.json).toHaveBeenCalledWith(sample{Entity});
  });

  it("throws NotFoundError when not found", async () => {
    const params: EntityIdParamType = { id: "non-existent" };
    mockService.getById.mockResolvedValue(null);

    const mockCtx = createMockContext({ user, validatedParams: params });

    await expect(controller.getById(mockCtx)).rejects.toThrow(NotFoundError);
    expect(mockCtx.json).not.toHaveBeenCalled();
  });
});
```

### 3. create Tests

```typescript
describe("create", () => {
  it("creates item and returns it", async () => {
    const createDto: Create{Entity}Type = { /* data */ };
    const created{Entity} = { ...sample{Entity}, ...createDto };
    mockService.create.mockResolvedValue(created{Entity});

    const mockCtx = createMockContext({ user, validatedBody: createDto });
    const response = await controller.create(mockCtx);

    expect(mockService.create).toHaveBeenCalledWith(createDto, user);
    expect(mockCtx.json).toHaveBeenCalledWith(created{Entity});
  });
});
```

### 4. update Tests

```typescript
describe("update", () => {
  it("updates item and returns it", async () => {
    const params: EntityIdParamType = { id: sample{Entity}.id };
    const updateDto: Update{Entity}Type = { /* data */ };
    const updated{Entity} = { ...sample{Entity}, ...updateDto };
    mockService.update.mockResolvedValue(updated{Entity});

    const mockCtx = createMockContext({
      user,
      validatedParams: params,
      validatedBody: updateDto,
    });
    const response = await controller.update(mockCtx);

    expect(mockService.update).toHaveBeenCalledWith(params.id, updateDto, user);
    expect(mockCtx.json).toHaveBeenCalledWith(updated{Entity});
  });

  it("throws NotFoundError when not found", async () => {
    const params: EntityIdParamType = { id: "non-existent" };
    mockService.update.mockResolvedValue(null);

    const mockCtx = createMockContext({
      user,
      validatedParams: params,
      validatedBody: { /* data */ },
    });

    await expect(controller.update(mockCtx)).rejects.toThrow(NotFoundError);
  });
});
```

### 5. delete Tests

```typescript
describe("delete", () => {
  it("deletes item and returns success message", async () => {
    const params: EntityIdParamType = { id: sample{Entity}.id };
    mockService.delete.mockResolvedValue(true);

    const mockCtx = createMockContext({ user, validatedParams: params });
    await controller.delete(mockCtx);

    expect(mockService.delete).toHaveBeenCalledWith(params.id, user);
    expect(mockCtx.json).toHaveBeenCalledWith({
      message: "{Entity} deleted successfully",
    });
  });

  it("throws NotFoundError when not found", async () => {
    const params: EntityIdParamType = { id: "non-existent" };
    mockService.delete.mockResolvedValue(false);

    const mockCtx = createMockContext({ user, validatedParams: params });

    await expect(controller.delete(mockCtx)).rejects.toThrow(NotFoundError);
  });
});
```

## Key Patterns

### Mock Context Factory

```typescript
const createMockContext = (config: MockContextConfig = {}) => {
  const mockJson = vi.fn((data) => data);
  return {
    var: {
      user: config.user,
      validatedQuery: config.validatedQuery,
      validatedParams: config.validatedParams,
      validatedBody: config.validatedBody,
    },
    json: mockJson,
  } as any;
};
```

### Mock Service Object

```typescript
const mockService = {
  getAll: vi.fn(),
  getById: vi.fn(),
  create: vi.fn(),
  update: vi.fn(),
  delete: vi.fn(),
};

// Inject into controller
controller = new Controller(mockService as unknown as Service);
```

### Assertions

```typescript
// Verify service called correctly
expect(mockService.getById).toHaveBeenCalledWith(id, user);

// Verify response
expect(mockCtx.json).toHaveBeenCalledWith(expectedData);

// Verify error thrown
await expect(controller.method(ctx)).rejects.toThrow(NotFoundError);

// Verify json NOT called on error
expect(mockCtx.json).not.toHaveBeenCalled();
```

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a complete controller test.

## What NOT to Do

- Do NOT test actual HTTP requests (that's integration testing)
- Do NOT use real services (mock them)
- Do NOT forget to clear mocks between tests
- Do NOT test validation (that's middleware's job)
- Do NOT test authorization (that's service's job)

## See Also

- `create-controller` - Creating controllers
- `test-routes` - Integration testing with routes
- `test-middleware` - Testing middleware
