---
name: add-authorization-methods
description: Add authorization methods for a new entity to AuthorizationService. Use after creating a resource service. Triggers on "add permissions", "authorization methods", "entity permissions", "add auth methods".
---

# Add Authorization Methods

Adds entity-specific authorization methods to `AuthorizationService` for permission checks.

## Quick Reference

**File to modify**: `src/services/authorization.service.ts`
**When to use**: After creating a resource service with `create-resource-service` skill

## Prerequisites

Before adding authorization methods:

1. Entity schema created with `createdBy` field
2. Resource service created that uses `AuthorizationService`

## Instructions

### Step 1: Import Entity Type

Add the entity type import at the top of `authorization.service.ts`:

```typescript
import type { {Entity}Type } from "@/schemas/{entity-name}.schema";
```

### Step 2: Add CRUD Permission Methods

Add these methods to the `AuthorizationService` class:

```typescript
// =============================================================================
// {Entity} Permissions
// =============================================================================

async canView{Entity}(
  user: AuthenticatedUserContextType,
  {entity}: {Entity}Type,
): Promise<boolean> {
  // Admins can view any entity
  if (this.isAdmin(user)) return true;
  // Users can view their own entities
  if ({entity}.createdBy === user.userId) return true;
  return false;
}

async canCreate{Entity}(
  user: AuthenticatedUserContextType,
): Promise<boolean> {
  // Admins can always create
  if (this.isAdmin(user)) return true;
  // Regular users can create
  if (user.globalRole === "user") return true;
  return false;
}

async canUpdate{Entity}(
  user: AuthenticatedUserContextType,
  {entity}: {Entity}Type,
): Promise<boolean> {
  // Admins can update any entity
  if (this.isAdmin(user)) return true;
  // Users can update their own entities
  if ({entity}.createdBy === user.userId) return true;
  return false;
}

async canDelete{Entity}(
  user: AuthenticatedUserContextType,
  {entity}: {Entity}Type,
): Promise<boolean> {
  // Admins can delete any entity
  if (this.isAdmin(user)) return true;
  // Users can delete their own entities
  if ({entity}.createdBy === user.userId) return true;
  return false;
}
```

### Step 3: Add Event Permission Method

If using SSE events, add the event permission method:

```typescript
async canReceive{Entity}Event(
  user: AuthenticatedUserContextType,
  {entity}Data: { createdBy: string; [key: string]: unknown },
): Promise<boolean> {
  // Apply same rules as viewing
  if (this.isAdmin(user)) return true;
  if ({entity}Data.createdBy === user.userId) return true;
  return false;
}
```

### Step 4: Update Events Router (if using SSE)

In `src/routes/events.router.ts`, add the event listener and authorization check:

```typescript
// Add event listeners
appEvents.on("{entities}:created", eventHandler);
appEvents.on("{entities}:updated", eventHandler);
appEvents.on("{entities}:deleted", eventHandler);

// Update shouldUserReceiveEvent function
async function shouldUserReceiveEvent(...): Promise<boolean> {
  switch (event.resourceType) {
    // ... existing cases ...
    case "{entities}":
      if (
        typeof event.data === "object" &&
        event.data !== null &&
        "createdBy" in event.data
      ) {
        return await authorizationService.canReceive{Entity}Event(
          user,
          event.data as { createdBy: string; [key: string]: unknown },
        );
      }
      return false;
    default:
      return false;
  }
}
```

## Authorization Patterns

### Standard Owner-Based Pattern

The most common pattern - admin can do everything, users can only access their own:

```typescript
async canView{Entity}(user, {entity}): Promise<boolean> {
  if (this.isAdmin(user)) return true;
  if ({entity}.createdBy === user.userId) return true;
  return false;
}
```

### Public Read Pattern

For entities that anyone can view but only owners can modify:

```typescript
async canView{Entity}(user, {entity}): Promise<boolean> {
  // Anyone authenticated can view
  return true;
}

async canUpdate{Entity}(user, {entity}): Promise<boolean> {
  if (this.isAdmin(user)) return true;
  if ({entity}.createdBy === user.userId) return true;
  return false;
}
```

### Role-Based Pattern

For entities with role-specific access:

```typescript
async canView{Entity}(user, {entity}): Promise<boolean> {
  if (this.isAdmin(user)) return true;
  if (user.globalRole === "moderator") return true;
  if ({entity}.createdBy === user.userId) return true;
  return false;
}
```

### Team/Group Pattern

For entities shared within a team:

```typescript
async canView{Entity}(user, {entity}): Promise<boolean> {
  if (this.isAdmin(user)) return true;
  if ({entity}.createdBy === user.userId) return true;
  // Check if user is in the same team
  if ({entity}.teamId && user.teamIds?.includes({entity}.teamId)) return true;
  return false;
}
```

### Create Restrictions

Sometimes creation should be restricted:

```typescript
// Only admins can create
async canCreate{Entity}(user): Promise<boolean> {
  return this.isAdmin(user);
}

// Users with specific role can create
async canCreate{Entity}(user): Promise<boolean> {
  if (this.isAdmin(user)) return true;
  if (user.globalRole === "instructor") return true;
  return false;
}
```

## Method Signatures Reference

| Method                    | Parameters             | Returns            | Purpose            |
| ------------------------- | ---------------------- | ------------------ | ------------------ |
| `canView{Entity}`         | `user`, `{entity}`     | `Promise<boolean>` | Read single entity |
| `canCreate{Entity}`       | `user`                 | `Promise<boolean>` | Create new entity  |
| `canUpdate{Entity}`       | `user`, `{entity}`     | `Promise<boolean>` | Modify entity      |
| `canDelete{Entity}`       | `user`, `{entity}`     | `Promise<boolean>` | Remove entity      |
| `canReceive{Entity}Event` | `user`, `{entity}Data` | `Promise<boolean>` | SSE event access   |

## Complete Example

```typescript
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import type { NoteType } from "@/schemas/note.schema";
import type { ProjectType } from "@/schemas/project.schema";

export class AuthorizationService {
  isAdmin(user: AuthenticatedUserContextType): boolean {
    return user.globalRole === "admin";
  }

  // =============================================================================
  // Note Permissions
  // =============================================================================

  async canViewNote(
    user: AuthenticatedUserContextType,
    note: NoteType,
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if (note.createdBy === user.userId) return true;
    return false;
  }

  async canCreateNote(user: AuthenticatedUserContextType): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if (user.globalRole === "user") return true;
    return false;
  }

  async canUpdateNote(
    user: AuthenticatedUserContextType,
    note: NoteType,
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if (note.createdBy === user.userId) return true;
    return false;
  }

  async canDeleteNote(
    user: AuthenticatedUserContextType,
    note: NoteType,
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if (note.createdBy === user.userId) return true;
    return false;
  }

  async canReceiveNoteEvent(
    user: AuthenticatedUserContextType,
    noteData: { createdBy: string; [key: string]: unknown },
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if (noteData.createdBy === user.userId) return true;
    return false;
  }

  // =============================================================================
  // Project Permissions
  // =============================================================================

  async canViewProject(
    user: AuthenticatedUserContextType,
    project: ProjectType,
  ): Promise<boolean> {
    if (this.isAdmin(user)) return true;
    if (project.createdBy === user.userId) return true;
    return false;
  }

  // ... other project methods following same pattern ...
}
```

## Testing Authorization Methods

Add tests to `tests/services/authorization.service.test.ts`:

```typescript
describe("{Entity} Permissions", () => {
  const {entity}OwnedByUser: {Entity}Type = {
    id: "{entity}-1",
    // ... entity fields
    createdBy: regularUser.userId,
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  const {entity}OwnedByOther: {Entity}Type = {
    id: "{entity}-2",
    // ... entity fields
    createdBy: otherUser.userId,
    createdAt: new Date(),
    updatedAt: new Date(),
  };

  describe("canView{Entity}", () => {
    it("allows admin", async () => {
      await expect(
        service.canView{Entity}(adminUser, {entity}OwnedByUser)
      ).resolves.toBe(true);
    });

    it("allows owner", async () => {
      await expect(
        service.canView{Entity}(regularUser, {entity}OwnedByUser)
      ).resolves.toBe(true);
    });

    it("denies non-owner", async () => {
      await expect(
        service.canView{Entity}(regularUser, {entity}OwnedByOther)
      ).resolves.toBe(false);
    });
  });

  // Similar tests for canCreate, canUpdate, canDelete...
});
```

## What NOT to Do

- Do NOT return void - always return boolean
- Do NOT throw errors - return false for denied access
- Do NOT forget async - methods should be async for consistency
- Do NOT skip the event permission method if using SSE
- Do NOT forget to update events router for new entity

## See Also

- `create-resource-service` - Creating the service that uses these methods
- `add-resource-events` - Setting up SSE events
- `test-utility-service` - Testing authorization service
