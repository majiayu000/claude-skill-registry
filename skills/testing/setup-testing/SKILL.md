---
name: setup-testing
description: Configure test infrastructure with fixtures, helpers, and enhanced coverage. Use when setting up comprehensive testing. Triggers on "setup testing", "test infrastructure", "test helpers", "test fixtures".
---

# Setup Testing

Configures enhanced test infrastructure including shared fixtures, test helpers for mocking Hono context, and coverage configuration.

## Quick Reference

**Files created**:

- `tests/config/` - Test configuration directory
- `tests/fixtures/` - Shared test data
- `tests/helpers/` - Test utility functions

**When to use**: After bootstrapping, before writing tests for services/controllers

## Prerequisites

- Project bootstrapped with `bootstrap-project`
- Vitest installed as a dev dependency

## Instructions

### Phase 1: Create Test Directory Structure

#### Step 1: Create Test Directories

```bash
mkdir -p tests/config
mkdir -p tests/fixtures
mkdir -p tests/helpers
```

### Phase 2: Enhanced Vitest Configuration

#### Step 2: Update Vitest Config

Update `vitest.config.ts` with enhanced coverage settings:

```typescript
import path from "path";
import { defineConfig } from "vitest/config";

export default defineConfig({
  test: {
    include: ["tests/**/*.test.ts"],
    // Per-test setup (optional, create if needed)
    // setupFiles: ["./tests/config/setup.ts"],
    coverage: {
      provider: "v8",
      reporter: ["text", "json", "html"],
      all: true,
      include: ["src/**/*.ts"],
      exclude: [
        "**/*.test.ts",
        "**/coverage/**",
        "**/node_modules/**",
        "**/dist/**",
        "**/scripts/**",
        "**/src/server.ts",
        "**/src/config/**",
      ],
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
});
```

### Phase 3: Create Test Helpers

#### Step 3: Create Hono Context Mock Helper

Create `tests/helpers/hono-context.helper.ts`:

```typescript
import type { Context } from "hono";
import type { AppEnv } from "@/schemas/app-env.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";

interface MockContextOptions {
  user?: AuthenticatedUserContextType;
  validatedBody?: unknown;
  validatedQuery?: unknown;
  validatedParams?: unknown;
  params?: Record<string, string>;
}

export function createMockContext(
  options: MockContextOptions = {},
): Context<AppEnv> {
  const mockJson = vi.fn().mockImplementation((data, status = 200) => {
    return new Response(JSON.stringify(data), {
      status,
      headers: { "Content-Type": "application/json" },
    });
  });

  const mockText = vi.fn().mockImplementation((text, status = 200) => {
    return new Response(text, { status });
  });

  return {
    var: {
      user: options.user,
      validatedBody: options.validatedBody,
      validatedQuery: options.validatedQuery,
      validatedParams: options.validatedParams,
    },
    req: {
      param: (key?: string) => (key ? options.params?.[key] : options.params),
      query: () => options.validatedQuery || {},
      json: async () => options.validatedBody,
    },
    json: mockJson,
    text: mockText,
  } as unknown as Context<AppEnv>;
}

// Import vi from vitest at the top of your test file
import { vi } from "vitest";
```

#### Step 4: Create Response Helper

Create `tests/helpers/response.helper.ts`:

```typescript
export async function parseJsonResponse<T>(response: Response): Promise<T> {
  return response.json() as Promise<T>;
}

export function expectStatus(response: Response, expectedStatus: number): void {
  expect(response.status).toBe(expectedStatus);
}

export async function expectJsonResponse<T>(
  response: Response,
  expectedStatus: number,
): Promise<T> {
  expectStatus(response, expectedStatus);
  return parseJsonResponse<T>(response);
}
```

### Phase 4: Create Shared Fixtures

#### Step 5: Create User Fixtures

Create `tests/fixtures/user.fixtures.ts`:

```typescript
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";

export const mockAdminUser: AuthenticatedUserContextType = {
  userId: "admin-user-id",
  globalRole: "admin",
};

export const mockRegularUser: AuthenticatedUserContextType = {
  userId: "regular-user-id",
  globalRole: "user",
};

export const mockAnotherUser: AuthenticatedUserContextType = {
  userId: "another-user-id",
  globalRole: "user",
};

export function createMockUser(
  overrides: Partial<AuthenticatedUserContextType> = {},
): AuthenticatedUserContextType {
  return {
    userId: `user-${Date.now()}`,
    globalRole: "user",
    ...overrides,
  };
}
```

#### Step 6: Create Common Test Utilities

Create `tests/fixtures/index.ts`:

```typescript
export * from "./user.fixtures";

// Factory for creating unique IDs
export function createTestId(prefix: string = "test"): string {
  return `${prefix}-${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
}

// Factory for creating dates
export function createTestDate(daysAgo: number = 0): Date {
  const date = new Date();
  date.setDate(date.getDate() - daysAgo);
  return date;
}
```

### Phase 5: Create Test Setup File (Optional)

#### Step 7: Create Global Test Setup

Create `tests/config/setup.ts`:

```typescript
import { beforeAll, afterAll, beforeEach, afterEach } from "vitest";

// Global setup before all tests
beforeAll(() => {
  // Set test environment variables if needed
  process.env.NODE_ENV = "test";
});

// Global teardown after all tests
afterAll(() => {
  // Cleanup resources
});

// Reset mocks before each test
beforeEach(() => {
  // vi.clearAllMocks(); // Uncomment if using global mocks
});

// Cleanup after each test
afterEach(() => {
  // Cleanup test data
});
```

To use this setup file, uncomment the `setupFiles` line in `vitest.config.ts`.

## Usage Patterns

### Using Mock Context in Controller Tests

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { createMockContext } from "../helpers/hono-context.helper";
import { mockRegularUser } from "../fixtures/user.fixtures";
import { NoteController } from "@/controllers/note.controller";

describe("NoteController", () => {
  let controller: NoteController;
  let mockService: any;

  beforeEach(() => {
    mockService = {
      findAll: vi.fn(),
      findById: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    };
    controller = new NoteController(mockService);
  });

  describe("create", () => {
    it("should create a note and return 201", async () => {
      const mockNote = { id: "1", content: "Test note" };
      mockService.create.mockResolvedValue(mockNote);

      const context = createMockContext({
        user: mockRegularUser,
        validatedBody: { content: "Test note" },
      });

      const response = await controller.create(context);

      expect(response.status).toBe(201);
      expect(mockService.create).toHaveBeenCalledWith(
        { content: "Test note" },
        mockRegularUser,
      );
    });
  });
});
```

### Using Fixtures in Service Tests

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";
import { mockAdminUser, mockRegularUser, createTestId } from "../fixtures";
import { NoteService } from "@/services/note.service";

describe("NoteService", () => {
  let service: NoteService;
  let mockRepository: any;

  beforeEach(() => {
    mockRepository = {
      findAll: vi.fn(),
      findById: vi.fn(),
      create: vi.fn(),
      update: vi.fn(),
      remove: vi.fn(),
    };
    service = new NoteService(mockRepository);
  });

  it("should allow admin to access any note", async () => {
    const noteId = createTestId("note");
    const mockNote = {
      id: noteId,
      content: "Test",
      createdBy: mockRegularUser.userId,
    };
    mockRepository.findById.mockResolvedValue(mockNote);

    const result = await service.findById(noteId, mockAdminUser);

    expect(result).toEqual(mockNote);
  });
});
```

## Files Created Summary

```plaintext
tests/
├── config/
│   └── setup.ts           # Global test setup (optional)
├── fixtures/
│   ├── index.ts           # Re-exports and common utilities
│   └── user.fixtures.ts   # User mock data
└── helpers/
    ├── hono-context.helper.ts  # Mock Hono context creator
    └── response.helper.ts      # Response parsing utilities
```

## Test Organization Best Practices

### Directory Structure

```plaintext
tests/
├── config/           # Test configuration
├── fixtures/         # Shared test data
├── helpers/          # Test utilities
├── controllers/      # Controller tests
├── middlewares/      # Middleware tests
├── repositories/     # Repository tests
├── routes/           # Route integration tests
├── schemas/          # Schema validation tests
└── services/         # Service tests
```

### Naming Conventions

- Test files: `{source-file-name}.test.ts`
- Describe blocks: Match class/function name
- It blocks: Start with "should" describing expected behavior

### Example Test Structure

```typescript
import { describe, it, expect, vi, beforeEach } from "vitest";

describe("ComponentName", () => {
  // Setup
  let component: ComponentType;

  beforeEach(() => {
    // Reset state before each test
  });

  describe("methodName", () => {
    it("should do expected behavior", async () => {
      // Arrange
      // Act
      // Assert
    });

    it("should handle error case", async () => {
      // Arrange
      // Act
      // Assert
    });
  });
});
```

## What NOT to Do

- Do NOT put test logic in fixture files (only data)
- Do NOT create fixtures that depend on external state
- Do NOT skip cleanup in afterEach/afterAll hooks
- Do NOT use hardcoded IDs that might collide
- Do NOT import from `src/` in fixture files if avoidable

## See Also

- `setup-mongodb` - MongoDB test infrastructure with memory server
- `test-schema` - Testing Zod schemas
- `test-resource-service` - Testing services with mocked repositories
- `test-controller` - Testing controllers with mocked services
- `test-routes` - Integration testing routes
