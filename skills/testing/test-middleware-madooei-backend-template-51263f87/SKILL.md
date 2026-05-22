---
name: test-middleware
description: Test middleware functions. Use when testing authentication, validation, or other middleware. Triggers on "test middleware", "test auth middleware", "test validation middleware".
---

# Test Middleware

Tests middleware by mocking dependencies and Hono context.

## Quick Reference

**Location**: `tests/middlewares/{middleware-name}.middleware.test.ts`
**Key technique**: Mock context, mock services, test next() calls

## Test Structure

```typescript
import { describe, it, expect, beforeEach, vi, type Mock } from "vitest";
import {
  createAuthMiddleware,
  type AuthMiddlewareDeps,
} from "@/middlewares/auth.middleware";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import { UnauthenticatedError, ServiceUnavailableError } from "@/errors";
import type { MiddlewareHandler } from "hono";
import type { AppEnv } from "@/schemas/app-env.schema";

let mockAuthService: AuthMiddlewareDeps["authenticationService"];
let middleware: MiddlewareHandler<AppEnv>;

function createMockContext(headers: Record<string, string> = {}) {
  return {
    req: {
      header: (name: string) => headers[name],
    },
    set: vi.fn(),
    var: {},
  } as any;
}

describe("authMiddleware", () => {
  let user: AuthenticatedUserContextType;
  let next: Mock;

  beforeEach(() => {
    mockAuthService = {
      authenticateUserByToken: vi.fn(),
    } as AuthMiddlewareDeps["authenticationService"];

    middleware = createAuthMiddleware({
      authenticationService: mockAuthService,
    });
    user = { userId: "user-1", globalRole: "user" };
    next = vi.fn();
  });

  // Tests...
});
```

## Auth Middleware Tests

```typescript
it("throws UnauthenticatedError if Authorization header missing", async () => {
  const c = createMockContext();
  await expect(middleware(c, next)).rejects.toThrow(UnauthenticatedError);
  expect(mockAuthService.authenticateUserByToken).not.toHaveBeenCalled();
  expect(next).not.toHaveBeenCalled();
});

it("throws UnauthenticatedError if invalid format", async () => {
  const c = createMockContext({ Authorization: "InvalidToken" });
  await expect(middleware(c, next)).rejects.toThrow(UnauthenticatedError);
});

it("throws UnauthenticatedError if token missing after Bearer", async () => {
  const c = createMockContext({ Authorization: "Bearer " });
  await expect(middleware(c, next)).rejects.toThrow(UnauthenticatedError);
});

it("throws UnauthenticatedError if service throws UnauthenticatedError", async () => {
  const c = createMockContext({ Authorization: "Bearer valid-token" });
  (mockAuthService.authenticateUserByToken as Mock).mockRejectedValue(
    new UnauthenticatedError("Invalid token"),
  );
  await expect(middleware(c, next)).rejects.toThrow(UnauthenticatedError);
});

it("throws ServiceUnavailableError if service unavailable", async () => {
  const c = createMockContext({ Authorization: "Bearer valid-token" });
  (mockAuthService.authenticateUserByToken as Mock).mockRejectedValue(
    new ServiceUnavailableError("Service down"),
  );
  await expect(middleware(c, next)).rejects.toThrow(ServiceUnavailableError);
});

it("sets user and calls next() on success", async () => {
  const c = createMockContext({ Authorization: "Bearer valid-token" });
  (mockAuthService.authenticateUserByToken as Mock).mockResolvedValue(user);

  await middleware(c, next);

  expect(mockAuthService.authenticateUserByToken).toHaveBeenCalledWith(
    "valid-token",
  );
  expect(c.set).toHaveBeenCalledWith("user", user);
  expect(next).toHaveBeenCalledTimes(1);
});
```

## Validation Middleware Tests

```typescript
import { validate } from "@/middlewares/validation.middleware";
import { z } from "zod";
import { BadRequestError } from "@/errors";

function createMockContext(
  options: {
    json?: () => Promise<any>;
    query?: Record<string, string>;
    param?: Record<string, string>;
  } = {},
) {
  return {
    req: {
      json: options.json || (async () => ({})),
      query: () => options.query || {},
      param: () => options.param || {},
    },
    set: vi.fn(),
    var: {},
  } as any;
}

describe("validation middleware", () => {
  it("validates body and sets validatedBody on success", async () => {
    const schema = z.object({ content: z.string() });
    const middleware = validate({
      schema,
      source: "body",
      varKey: "validatedBody",
    });
    const next = vi.fn();

    const c = createMockContext({
      json: async () => ({ content: "test" }),
    });

    await middleware(c, next);

    expect(c.set).toHaveBeenCalledWith("validatedBody", { content: "test" });
    expect(next).toHaveBeenCalled();
  });

  it("throws BadRequestError on validation failure", async () => {
    const schema = z.object({ content: z.string().min(1) });
    const middleware = validate({
      schema,
      source: "body",
      varKey: "validatedBody",
    });
    const next = vi.fn();

    const c = createMockContext({
      json: async () => ({ content: "" }),
    });

    await expect(middleware(c, next)).rejects.toThrow(BadRequestError);
    expect(next).not.toHaveBeenCalled();
  });

  it("validates query params", async () => {
    const schema = z.object({ page: z.coerce.number().optional() });
    const middleware = validate({
      schema,
      source: "query",
      varKey: "validatedQuery",
    });
    const next = vi.fn();

    const c = createMockContext({ query: { page: "1" } });

    await middleware(c, next);

    expect(c.set).toHaveBeenCalledWith("validatedQuery", { page: 1 });
  });

  it("validates URL params", async () => {
    const schema = z.object({ id: z.string() });
    const middleware = validate({
      schema,
      source: "params",
      varKey: "validatedParams",
    });
    const next = vi.fn();

    const c = createMockContext({ param: { id: "123" } });

    await middleware(c, next);

    expect(c.set).toHaveBeenCalledWith("validatedParams", { id: "123" });
  });
});
```

## Key Patterns

### Mock Context Factory

```typescript
function createMockContext(headers: Record<string, string> = {}) {
  return {
    req: {
      header: (name: string) => headers[name],
      json: async () => ({}),
      query: () => ({}),
      param: () => ({}),
    },
    set: vi.fn(),
    var: {},
  } as any;
}
```

### Test next() Behavior

```typescript
// Verify next called on success
expect(next).toHaveBeenCalledTimes(1);

// Verify next NOT called on error
expect(next).not.toHaveBeenCalled();
```

### Test c.set() Calls

```typescript
expect(c.set).toHaveBeenCalledWith("user", expectedUser);
expect(c.set).toHaveBeenCalledWith("validatedBody", expectedData);
```

## What NOT to Do

- Do NOT test actual HTTP requests
- Do NOT forget to test error cases
- Do NOT forget to verify next() is/isn't called
- Do NOT use real services (mock them)

## See Also

- `create-middleware` - Creating middleware
- `test-routes` - Integration testing
