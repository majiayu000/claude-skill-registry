---
name: test-utility-service
description: Test utility services that handle external APIs or authorization logic. Use when testing services like AuthenticationService or AuthorizationService. Triggers on "test auth service", "test utility service", "test authentication".
---

# Test Utility Service

Tests utility services that call external APIs or provide authorization logic.

## Quick Reference

**Location**: `tests/services/{service-name}.service.test.ts`
**Key technique**: Mock `fetch` with `vi.stubGlobal`

## Service Categories

### 1. External API Services (e.g., AuthenticationService)

Mock network calls and test error handling:

```typescript
import { describe, it, expect, beforeEach, afterEach, vi } from "vitest";
import { AuthenticationService } from "@/services/authentication.service";
import { env } from "@/env";
import { ServiceUnavailableError, UnauthenticatedError } from "@/errors";

describe("AuthenticationService", () => {
  let service: AuthenticationService;
  const token = "test-token";
  const authServiceUrl = "http://auth-service";

  beforeEach(() => {
    service = new AuthenticationService();
    env.AUTH_SERVICE_URL = authServiceUrl;
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it("authenticates and returns user on success", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ userId: "user-1", globalRole: "user" }),
      }),
    );

    const result = await service.authenticateUserByToken(token);
    expect(result.userId).toBe("user-1");
  });

  it("throws UnauthenticatedError on 401/403", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 401,
      }),
    );

    await expect(service.authenticateUserByToken(token)).rejects.toThrow(
      UnauthenticatedError,
    );
  });

  it("throws ServiceUnavailableError on 5xx", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
      }),
    );

    await expect(service.authenticateUserByToken(token)).rejects.toThrow(
      ServiceUnavailableError,
    );
  });

  it("throws ServiceUnavailableError if fetch throws", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockRejectedValue(new Error("network error")),
    );

    await expect(service.authenticateUserByToken(token)).rejects.toThrow(
      ServiceUnavailableError,
    );
  });

  it("throws ServiceUnavailableError if config missing", async () => {
    env.AUTH_SERVICE_URL = undefined;

    await expect(service.authenticateUserByToken(token)).rejects.toThrow(
      ServiceUnavailableError,
    );
  });

  it("throws UnauthenticatedError if response data invalid", async () => {
    vi.stubGlobal(
      "fetch",
      vi.fn().mockResolvedValue({
        ok: true,
        json: async () => ({ invalid: "data" }),
      }),
    );

    await expect(service.authenticateUserByToken(token)).rejects.toThrow(
      UnauthenticatedError,
    );
  });
});
```

### 2. Authorization Services (e.g., AuthorizationService)

Test permission logic with various user/resource combinations:

```typescript
import { describe, it, expect, beforeEach } from "vitest";
import { AuthorizationService } from "@/services/authorization.service";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import type { NoteType } from "@/schemas/note.schema";

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

const noteOwnedByRegularUser: NoteType = {
  id: "note-1",
  content: "Test content",
  createdBy: regularUser.userId,
  createdAt: new Date(),
  updatedAt: new Date(),
};

const noteOwnedByOtherUser: NoteType = {
  id: "note-2",
  content: "Other content",
  createdBy: otherUser.userId,
  createdAt: new Date(),
  updatedAt: new Date(),
};

describe("AuthorizationService", () => {
  let service: AuthorizationService;

  beforeEach(() => {
    service = new AuthorizationService();
  });

  describe("isAdmin", () => {
    it("returns true for admin", () => {
      expect(service.isAdmin(adminUser)).toBe(true);
    });

    it("returns false for regular user", () => {
      expect(service.isAdmin(regularUser)).toBe(false);
    });
  });

  describe("canViewNote", () => {
    it("allows admin", async () => {
      await expect(
        service.canViewNote(adminUser, noteOwnedByRegularUser),
      ).resolves.toBe(true);
    });

    it("allows owner", async () => {
      await expect(
        service.canViewNote(regularUser, noteOwnedByRegularUser),
      ).resolves.toBe(true);
    });

    it("denies non-owner", async () => {
      await expect(
        service.canViewNote(regularUser, noteOwnedByOtherUser),
      ).resolves.toBe(false);
    });
  });

  describe("canCreateNote", () => {
    it("allows admin", async () => {
      await expect(service.canCreateNote(adminUser)).resolves.toBe(true);
    });

    it("allows regular user", async () => {
      await expect(service.canCreateNote(regularUser)).resolves.toBe(true);
    });
  });

  describe("canUpdateNote", () => {
    it("allows admin", async () => {
      await expect(
        service.canUpdateNote(adminUser, noteOwnedByRegularUser),
      ).resolves.toBe(true);
    });

    it("allows owner", async () => {
      await expect(
        service.canUpdateNote(regularUser, noteOwnedByRegularUser),
      ).resolves.toBe(true);
    });

    it("denies non-owner", async () => {
      await expect(
        service.canUpdateNote(regularUser, noteOwnedByOtherUser),
      ).resolves.toBe(false);
    });
  });

  describe("canDeleteNote", () => {
    it("allows admin", async () => {
      await expect(
        service.canDeleteNote(adminUser, noteOwnedByRegularUser),
      ).resolves.toBe(true);
    });

    it("allows owner", async () => {
      await expect(
        service.canDeleteNote(regularUser, noteOwnedByRegularUser),
      ).resolves.toBe(true);
    });

    it("denies non-owner", async () => {
      await expect(
        service.canDeleteNote(regularUser, noteOwnedByOtherUser),
      ).resolves.toBe(false);
    });
  });
});
```

## Key Patterns

### Mocking Fetch

```typescript
// Success response
vi.stubGlobal(
  "fetch",
  vi.fn().mockResolvedValue({
    ok: true,
    json: async () => ({ data: "value" }),
  }),
);

// Error response
vi.stubGlobal(
  "fetch",
  vi.fn().mockResolvedValue({
    ok: false,
    status: 401,
  }),
);

// Network failure
vi.stubGlobal("fetch", vi.fn().mockRejectedValue(new Error("network error")));
```

### Manipulating Environment

```typescript
beforeEach(() => {
  env.AUTH_SERVICE_URL = "http://test-service";
});

it("handles missing config", async () => {
  env.AUTH_SERVICE_URL = undefined;
  // Test behavior
});
```

### Restoring Mocks

```typescript
afterEach(() => {
  vi.restoreAllMocks(); // Important!
});
```

## Test Categories for External API Services

| Category            | Test Cases                                |
| ------------------- | ----------------------------------------- |
| Success             | Valid response, correct data returned     |
| Auth Errors (4xx)   | 401, 403 → `UnauthenticatedError`         |
| Server Errors (5xx) | 500, 502, 503 → `ServiceUnavailableError` |
| Network Errors      | Fetch throws → `ServiceUnavailableError`  |
| Config Errors       | Missing URL → `ServiceUnavailableError`   |
| Validation Errors   | Invalid response data → appropriate error |

## Test Categories for Authorization Services

| Category       | Test Cases                            |
| -------------- | ------------------------------------- |
| Admin Access   | Admin can do everything               |
| Owner Access   | Owner can access their own resources  |
| Non-Owner Deny | Regular user denied access to others' |
| Create Access  | Who can create new resources          |
| Event Access   | Who can receive real-time events      |

## Complete Examples

See [REFERENCE.md](REFERENCE.md) for complete test implementations.

## What NOT to Do

- Do NOT forget to restore mocks in `afterEach`
- Do NOT test actual network calls (always mock)
- Do NOT skip testing error scenarios
- Do NOT skip testing missing configuration
- Do NOT hardcode URLs (use env variables)

## See Also

- `test-service` - Guide for choosing test type
- `test-resource-service` - Testing resource services
- `create-utility-service` - Creating the service to test
