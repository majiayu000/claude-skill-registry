---
name: create-resource-service
description: Create a resource service for CRUD operations on domain entities. Use when creating services for entities like notes, users, courses that need data operations, authorization, and event emission. Triggers on "resource service", "entity service", "crud service", "note service", "create service for".
---

# Create Resource Service

Creates a service for CRUD operations on a domain entity. Resource services extend `BaseService` for event emission, inject repositories for data access, and use `AuthorizationService` for permission checks.

## Quick Reference

**Location**: `src/services/{entity-name}.service.ts`
**Naming**: Singular, kebab-case (e.g., `note.service.ts`, `course.service.ts`)

## Prerequisites

Before creating a resource service, ensure you have:

1. Schema created (`src/schemas/{entity-name}.schema.ts`)
2. Repository interface created (`src/repositories/{entity-name}.repository.ts`)
3. At least one repository implementation (MockDB or MongoDB)

## Instructions

### Step 1: Create the Service File

Create `src/services/{entity-name}.service.ts`

### Step 2: Import Dependencies

```typescript
import type { I{Entity}Repository } from "@/repositories/{entity-name}.repository";
import type { PaginatedResultType } from "@/schemas/shared.schema";
import type {
  Create{Entity}Type,
  {Entity}QueryParamsType,
  {Entity}Type,
  Update{Entity}Type,
} from "@/schemas/{entity-name}.schema";
import type { AuthenticatedUserContextType } from "@/schemas/user.schemas";
import { AuthorizationService } from "@/services/authorization.service";
import { UnauthorizedError } from "@/errors";
import { MockDb{Entity}Repository } from "@/repositories/mockdb/{entity-name}.mockdb.repository";
import { BaseService } from "@/events/base.service";
```

### Step 3: Create the Service Class

```typescript
export class {Entity}Service extends BaseService {
  private readonly {entity}Repository: I{Entity}Repository;
  private readonly authorizationService: AuthorizationService;

  constructor(
    {entity}Repository?: I{Entity}Repository,
    authorizationService?: AuthorizationService,
  ) {
    super("{entities}"); // Service name for events (plural)

    this.{entity}Repository = {entity}Repository ?? new MockDb{Entity}Repository();
    this.authorizationService = authorizationService ?? new AuthorizationService();
  }

  // CRUD methods...
}
```

### Step 4: Implement CRUD Methods

#### getAll

```typescript
async getAll(
  params: {Entity}QueryParamsType,
  user: AuthenticatedUserContextType,
): Promise<PaginatedResultType<{Entity}Type>> {
  // Admins see all, users see only their own
  if (this.authorizationService.isAdmin(user)) {
    return this.{entity}Repository.findAll(params);
  }
  return this.{entity}Repository.findAll({ ...params, createdBy: user.userId });
}
```

#### getById

```typescript
async getById(
  id: string,
  user: AuthenticatedUserContextType,
): Promise<{Entity}Type | null> {
  const {entity} = await this.{entity}Repository.findById(id);
  if (!{entity}) {
    return null;
  }

  const canView = await this.authorizationService.canView{Entity}(user, {entity});
  if (!canView) throw new UnauthorizedError();

  return {entity};
}
```

#### create

```typescript
async create(
  data: Create{Entity}Type,
  user: AuthenticatedUserContextType,
): Promise<{Entity}Type> {
  const canCreate = await this.authorizationService.canCreate{Entity}(user);
  if (!canCreate) throw new UnauthorizedError();

  const {entity} = await this.{entity}Repository.create(data, user.userId);

  this.emitEvent("created", {entity}, {
    id: {entity}.id,
    user,
  });

  return {entity};
}
```

#### update

```typescript
async update(
  id: string,
  data: Update{Entity}Type,
  user: AuthenticatedUserContextType,
): Promise<{Entity}Type | null> {
  const {entity} = await this.{entity}Repository.findById(id);
  if (!{entity}) {
    return null;
  }

  const canUpdate = await this.authorizationService.canUpdate{Entity}(user, {entity});
  if (!canUpdate) throw new UnauthorizedError();

  const updated{Entity} = await this.{entity}Repository.update(id, data);
  if (!updated{Entity}) {
    return null;
  }

  this.emitEvent("updated", updated{Entity}, {
    id: updated{Entity}.id,
    user,
  });

  return updated{Entity};
}
```

#### delete

```typescript
async delete(
  id: string,
  user: AuthenticatedUserContextType,
): Promise<boolean> {
  const {entity} = await this.{entity}Repository.findById(id);
  if (!{entity}) {
    return false;
  }

  const canDelete = await this.authorizationService.canDelete{Entity}(user, {entity});
  if (!canDelete) throw new UnauthorizedError();

  const deleted = await this.{entity}Repository.remove(id);
  if (deleted) {
    this.emitEvent("deleted", {entity}, {
      id: {entity}.id,
      user,
    });
  }

  return deleted;
}
```

## Patterns & Rules

### Extending BaseService

```typescript
export class {Entity}Service extends BaseService {
  constructor(...) {
    super("{entities}"); // Plural name for event namespace
  }
}
```

The `serviceName` is used for event routing (e.g., `notes:created`, `notes:updated`).

### Dependency Injection

```typescript
constructor(
  {entity}Repository?: I{Entity}Repository,
  authorizationService?: AuthorizationService,
) {
  // Provide defaults for convenience, but allow injection for testing
  this.{entity}Repository = {entity}Repository ?? new MockDb{Entity}Repository();
  this.authorizationService = authorizationService ?? new AuthorizationService();
}
```

- Accept **interfaces** for repositories (not concrete classes)
- Provide **defaults** for easier instantiation
- Allow **injection** for testing with mocks

### Authorization Pattern

Every operation should check permissions:

```typescript
const canDoX = await this.authorizationService.canX{Entity}(user, {entity});
if (!canDoX) throw new UnauthorizedError();
```

You must add corresponding methods to `AuthorizationService`:

- `canView{Entity}(user, entity)`
- `canCreate{Entity}(user)`
- `canUpdate{Entity}(user, entity)`
- `canDelete{Entity}(user, entity)`

### Event Emission Pattern

Emit events after successful operations:

```typescript
this.emitEvent("created", {entity}, { id: {entity}.id, user });
this.emitEvent("updated", updated{Entity}, { id: updated{Entity}.id, user });
this.emitEvent("deleted", {entity}, { id: {entity}.id, user });
```

Events are only emitted for `create`, `update`, `delete` - not for reads.

### Error Handling

- **Not found**: Return `null` (let controller decide HTTP status)
- **Unauthorized**: Throw `UnauthorizedError` from `@/errors`
- **Other errors**: Let them propagate (global error handler catches)

### Return Types

- `getAll`: `Promise<PaginatedResultType<{Entity}Type>>`
- `getById`: `Promise<{Entity}Type | null>`
- `create`: `Promise<{Entity}Type>`
- `update`: `Promise<{Entity}Type | null>`
- `delete`: `Promise<boolean>`

## Complete Example

See [REFERENCE.md](REFERENCE.md) for a complete `NoteService` implementation.

## After Creating the Service

1. **Add authorization methods** to `AuthorizationService` for this entity
2. **Add event schema** (optional) - see `add-resource-events` skill
3. **Create controller** - see `create-controller` skill
4. **Write tests** - see `test-service` skill

## What NOT to Do

- Do NOT put HTTP-specific logic in services (that's for controllers)
- Do NOT return HTTP status codes or responses
- Do NOT skip authorization checks
- Do NOT emit events before confirming the operation succeeded
- Do NOT inject concrete repository classes - use interfaces
