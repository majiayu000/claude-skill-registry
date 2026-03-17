---
name: test-service
description: Guide for testing service layer. Use when asked to test services. Directs to implementation-specific testing skills.
---

# Test Service

## Service Types Have Different Testing Strategies

Services fall into two categories with different testing approaches:

| Type             | Testing Strategy                                | Skill                   |
| ---------------- | ----------------------------------------------- | ----------------------- |
| Resource Service | Mock repository, test authorization + events    | `test-resource-service` |
| Utility Service  | Mock external APIs (fetch), test error handling | `test-utility-service`  |

## When to Test

Test services **after** you have:

1. Created the service (`create-resource-service` or `create-utility-service`)
2. Created any dependencies (repositories, schemas)

## Which Skill to Use

### Use `test-resource-service` when:

- Testing services that extend `BaseService`
- Testing CRUD operations on domain entities
- Testing authorization logic (admin vs owner vs other)
- Testing event emission

**Examples**: `NoteService`, `UserService`, `CourseService`

### Use `test-utility-service` when:

- Testing services that call external APIs
- Testing authentication/authorization logic services
- Testing error handling for external failures
- Mocking `fetch` or other network calls

**Examples**: `AuthenticationService`, `AuthorizationService`, `EmailService`

## Common Testing Patterns

Both service types share these patterns:

### User Context Fixtures

```typescript
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
```

### Error Assertions

```typescript
// Expect specific error type
await expect(service.someMethod()).rejects.toThrow(UnauthorizedError);

// Expect any error
await expect(service.someMethod()).rejects.toThrow();
```

### Cleanup in beforeEach/afterEach

```typescript
beforeEach(() => {
  // Reset state
});

afterEach(() => {
  vi.restoreAllMocks();
});
```

## See Also

- `test-resource-service` - Testing resource services (CRUD + events)
- `test-utility-service` - Testing utility services (external APIs)
