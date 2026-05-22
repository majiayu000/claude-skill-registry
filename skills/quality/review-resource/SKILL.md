---
name: review-resource
description: Review and validate a resource implementation follows all patterns. Use after creating a resource or when refactoring existing code. Triggers on "review resource", "validate resource", "check implementation", "refactor resource".
---

# Review Resource

Validates that a resource implementation follows all architectural patterns and best practices. Also provides guidance for refactoring existing code to match template patterns.

## Quick Reference

Use this skill to:

- **After creating** a resource: verify completeness and correctness
- **When refactoring**: identify deviations and plan migration
- **During code review**: check pattern compliance

## Review Checklist

### 1. File Structure

```markdown
## File Existence Check

### Schema Layer

- [ ] `src/schemas/{entity}.schema.ts` exists
- [ ] `tests/schemas/{entity}.schema.test.ts` exists

### Repository Layer

- [ ] `src/repositories/{entity}.repository.ts` (interface) exists
- [ ] `src/repositories/mockdb/{entity}.mockdb.repository.ts` exists
- [ ] `src/repositories/mongodb/{entity}.mongodb.repository.ts` exists
- [ ] `tests/repositories/{entity}.mockdb.repository.test.ts` exists
- [ ] `tests/repositories/{entity}.mongodb.repository.test.ts` exists

### Service Layer

- [ ] `src/services/{entity}.service.ts` exists
- [ ] `tests/services/{entity}.service.test.ts` exists

### Controller Layer

- [ ] `src/controllers/{entity}.controller.ts` exists
- [ ] `tests/controllers/{entity}.controller.test.ts` exists

### Routes Layer

- [ ] `src/routes/{entity}.router.ts` exists
- [ ] `tests/routes/{entity}.router.test.ts` exists
- [ ] Routes mounted in `src/app.ts`
```

### 2. Schema Patterns

```markdown
## Schema Review

- [ ] Uses `z.object()` for all schemas
- [ ] Exports both schema and inferred type
- [ ] Has `{entity}Schema` (base entity)
- [ ] Has `create{Entity}Schema` (omits id, createdAt, updatedAt, createdBy)
- [ ] Has `update{Entity}Schema` (partial of create)
- [ ] Has `{entity}QueryParamsSchema` (extends paginationQuerySchema)
- [ ] Uses `z.coerce` for numeric query params
- [ ] Test file covers: valid data, missing fields, invalid types, coercion
```

### 3. Repository Patterns

```markdown
## Repository Interface Review

- [ ] Interface named `I{Entity}Repository`
- [ ] Standard methods: `findAll`, `findById`, `create`, `update`, `remove`
- [ ] `findAll` returns `Promise<PaginatedResultType<{Entity}Type>>`
- [ ] `findById` returns `Promise<{Entity}Type | null>`
- [ ] `create` returns `Promise<{Entity}Type>`
- [ ] `update` returns `Promise<{Entity}Type | null>`
- [ ] `remove` returns `Promise<boolean>`

## MockDB Implementation Review

- [ ] Implements interface correctly
- [ ] Uses in-memory array storage
- [ ] Has `clear()` helper for testing
- [ ] Implements pagination, filtering, sorting

## MongoDB Implementation Review

- [ ] Implements interface correctly
- [ ] Uses native MongoDB driver (not Mongoose)
- [ ] Has document interface with `_id: ObjectId`
- [ ] Validates with Zod on read
- [ ] Creates proper indexes
- [ ] Has `clear()` and `getStats()` helpers
```

### 4. Service Patterns

```markdown
## Service Review

- [ ] Extends `BaseService`
- [ ] Constructor calls `super("{entities}")` (plural)
- [ ] Injects repository interface (not concrete class)
- [ ] Injects `AuthorizationService`
- [ ] Provides default implementations in constructor

## Authorization Review

- [ ] Checks permissions before each operation
- [ ] Uses `UnauthorizedError` for permission denied
- [ ] `getAll` filters by user for non-admins
- [ ] `getById`, `update`, `delete` check ownership

## Event Emission Review

- [ ] Emits "created" after successful create
- [ ] Emits "updated" after successful update
- [ ] Emits "deleted" after successful delete
- [ ] Does NOT emit for failed/unauthorized operations
```

### 5. Controller Patterns

```markdown
## Controller Review

- [ ] Uses arrow function handlers (not methods)
- [ ] Accepts `Context<AppEnv>` parameter
- [ ] Extracts user from `c.var.user`
- [ ] Extracts validated data from `c.var.validatedQuery/Body/Params`
- [ ] Throws `NotFoundError` when service returns null
- [ ] Returns response via `c.json()`
- [ ] Does NOT do validation (middleware handles)
- [ ] Does NOT catch errors (global handler catches)
```

### 6. Routes Patterns

```markdown
## Routes Review

- [ ] Uses factory function pattern
- [ ] Accepts controller via dependency injection
- [ ] Accepts middleware via dependency injection with defaults
- [ ] Uses `new Hono<AppEnv>()`
- [ ] Applies auth middleware globally with `.use("*", ...)`
- [ ] Chains validation middleware per route
- [ ] Returns the router

## Route Coverage

- [ ] GET `/` - list all
- [ ] GET `/:id` - get by id
- [ ] POST `/` - create
- [ ] PUT `/:id` or PATCH `/:id` - update
- [ ] DELETE `/:id` - delete
```

### 7. Test Coverage

```markdown
## Test Review

### Schema Tests

- [ ] Tests valid data acceptance
- [ ] Tests required field rejection
- [ ] Tests invalid type rejection
- [ ] Tests coercion behavior
- [ ] Tests optional fields

### Repository Tests

- [ ] Tests all CRUD operations
- [ ] Tests pagination
- [ ] Tests filtering
- [ ] Tests sorting
- [ ] Tests not-found returns null/false

### Service Tests

- [ ] Tests with admin user
- [ ] Tests with owner user
- [ ] Tests with other user (denied)
- [ ] Tests not-found cases
- [ ] Tests event emission
- [ ] Tests no events for failures

### Controller Tests

- [ ] Mocks service
- [ ] Tests successful responses
- [ ] Tests NotFoundError thrown
- [ ] Verifies c.json called correctly

### Routes Tests

- [ ] Integration-style with app.request()
- [ ] Tests success cases (200)
- [ ] Tests 404 for not found
- [ ] Tests 401 for unauthenticated
- [ ] Tests 403 for unauthorized
- [ ] Tests 400 for validation errors
```

### 8. Common Mistakes

```markdown
## Common Mistakes to Check

### Schema

- [ ] Not exporting types alongside schemas
- [ ] Not using `z.coerce` for query params
- [ ] Missing optional() on update fields

### Repository

- [ ] Using concrete class instead of interface
- [ ] Missing null return for not-found
- [ ] Not validating MongoDB documents with Zod

### Service

- [ ] Not extending BaseService
- [ ] Emitting events before confirming success
- [ ] Not checking authorization
- [ ] Returning HTTP status codes instead of errors

### Controller

- [ ] Using regular methods instead of arrow functions
- [ ] Accessing c.req.json() directly instead of c.var.validatedBody
- [ ] Catching and handling errors instead of letting them propagate

### Routes

- [ ] Not using factory function pattern
- [ ] Hardcoding middleware instead of injecting
- [ ] Forgetting to mount in app.ts

### Tests

- [ ] Not clearing state between tests
- [ ] Not testing authorization for all user types
- [ ] Not testing event emission
```

## Running Validation

```bash
# Run all tests for the resource
pnpm test tests/**/{entity}*

# Type check
pnpm type-check

# Lint
pnpm lint

# Full validation
pnpm validate
```

---

## Refactoring Guide

Use this section when migrating existing code to follow template patterns.

### Step 1: Assess Current State

Run through the review checklists above and document deviations:

```markdown
## {Entity} Refactoring Assessment

### File Structure

- [ ] Missing: {list missing files}
- [ ] Extra: {list files that don't fit pattern}
- [ ] Rename needed: {list files with wrong names}

### Pattern Deviations

- [ ] Schema: {describe deviations}
- [ ] Repository: {describe deviations}
- [ ] Service: {describe deviations}
- [ ] Controller: {describe deviations}
- [ ] Routes: {describe deviations}

### Breaking Changes

- [ ] {list API changes that will break clients}
- [ ] {list database schema changes}
```

### Step 2: Plan Migration Order

Refactor in this order to minimize breakage:

1. **Schema** (foundation) - Add missing types, fix validation
2. **Repository Interface** - Define contract
3. **Repository Implementation** - Migrate data access
4. **Service** - Migrate business logic, add BaseService
5. **Controller** - Convert to arrow functions, fix context usage
6. **Routes** - Convert to factory pattern
7. **Integration** - Update app.ts mounting
8. **Tests** - Add missing tests, fix existing ones

### Step 3: Common Refactoring Patterns

#### Refactoring: Add Missing Zod Schema

**Before** (TypeScript interface only):

```typescript
interface Note {
  id: string;
  content: string;
  createdBy: string;
}
```

**After** (Zod schema with inferred type):

```typescript
export const noteSchema = z.object({
  id: z.string(),
  content: z.string().min(1),
  createdBy: z.string(),
  createdAt: z.date().optional(),
  updatedAt: z.date().optional(),
});
export type NoteType = z.infer<typeof noteSchema>;
```

#### Refactoring: Convert Class Methods to Arrow Functions

**Before** (loses `this` binding):

```typescript
class NoteController {
  async getAll(c: Context): Promise<Response> {
    // ...
  }
}
```

**After** (preserves `this` binding):

```typescript
class NoteController {
  getAll = async (c: Context<AppEnv>): Promise<Response> => {
    // ...
  };
}
```

#### Refactoring: Add Repository Interface

**Before** (concrete class only):

```typescript
class NoteRepository {
  findAll() { ... }
}
```

**After** (interface + implementation):

```typescript
// note.repository.ts
export interface INoteRepository {
  findAll(query: NoteQueryParamsType): Promise<PaginatedResultType<NoteType>>;
  // ...
}

// mockdb/note.mockdb.repository.ts
export class MockDbNoteRepository implements INoteRepository {
  // ...
}
```

#### Refactoring: Convert Service to Extend BaseService

**Before**:

```typescript
class NoteService {
  constructor(private repo: NoteRepository) {}

  async create(data: CreateNote, userId: string) {
    return this.repo.create(data, userId);
  }
}
```

**After**:

```typescript
class NoteService extends BaseService {
  constructor(
    private repository: INoteRepository = new MockDbNoteRepository(),
    private authService: AuthorizationService = new AuthorizationService(),
  ) {
    super("notes");
  }

  async create(data: CreateNoteType, user: AuthenticatedUserContextType) {
    if (!(await this.authService.canCreateNote(user))) {
      throw new UnauthorizedError();
    }
    const note = await this.repository.create(data, user.userId);
    this.emitEvent("created", note, { id: note.id, user });
    return note;
  }
}
```

#### Refactoring: Convert Routes to Factory Pattern

**Before**:

```typescript
const router = new Hono();
const controller = new NoteController();

router.get("/", controller.getAll);
router.post("/", controller.create);

export { router as noteRoutes };
```

**After**:

```typescript
export interface CreateNoteRoutesDeps {
  noteController: NoteController;
  validate?: typeof defaultValidate;
  authMiddleware?: typeof defaultAuthMiddleware;
}

export const createNoteRoutes = (deps: CreateNoteRoutesDeps) => {
  const {
    noteController,
    validate = defaultValidate,
    authMiddleware = defaultAuthMiddleware,
  } = deps;

  const noteRoutes = new Hono<AppEnv>();
  noteRoutes.use("*", authMiddleware);

  noteRoutes.get(
    "/",
    validate({
      schema: noteQueryParamsSchema,
      source: "query",
      varKey: "validatedQuery",
    }),
    noteController.getAll,
  );
  // ...

  return noteRoutes;
};
```

### Step 4: Handle Breaking Changes

#### API Breaking Changes

If refactoring changes API contracts:

1. **Version the API**: Add `/v2/` prefix for new endpoints
2. **Deprecation period**: Keep old endpoints working with warnings
3. **Document changes**: Update API documentation
4. **Notify consumers**: If external clients exist

#### Database Breaking Changes

If refactoring changes data structure:

1. **Create migration script**: Transform existing data
2. **Backup first**: Always backup before migrations
3. **Test migration**: Run against copy of production data
4. **Rollback plan**: Prepare reverse migration

### Step 5: Incremental Migration Strategy

For large codebases, migrate incrementally:

```markdown
## Week 1: Foundation

- [ ] Create schema (keep old types as aliases)
- [ ] Create repository interface
- [ ] Create MockDB implementation

## Week 2: Service Layer

- [ ] Migrate service to extend BaseService
- [ ] Add authorization checks
- [ ] Add event emission

## Week 3: HTTP Layer

- [ ] Migrate controller to arrow functions
- [ ] Convert routes to factory pattern
- [ ] Update app.ts

## Week 4: Testing & Cleanup

- [ ] Add missing tests
- [ ] Remove old code
- [ ] Update documentation
```

### Step 6: Validation After Refactoring

After refactoring, run full validation:

```bash
# Type check (catches interface mismatches)
pnpm type-check

# Run all tests
pnpm test

# Lint (catches style issues)
pnpm lint

# Full validation suite
pnpm validate
```

### Refactoring Checklist

```markdown
## {Entity} Refactoring Checklist

### Pre-Refactoring

- [ ] Document current implementation
- [ ] Identify all consumers of the API
- [ ] Create backup/snapshot of current state
- [ ] Write characterization tests for current behavior

### During Refactoring

- [ ] Schema migrated and types exported
- [ ] Repository interface created
- [ ] Repository implementation(s) created
- [ ] Service extends BaseService
- [ ] Service has authorization checks
- [ ] Service emits events
- [ ] Controller uses arrow functions
- [ ] Controller uses c.var for validated data
- [ ] Routes use factory pattern
- [ ] Routes mounted in app.ts
- [ ] Authorization methods added to AuthorizationService

### Post-Refactoring

- [ ] All tests pass
- [ ] Type check passes
- [ ] Lint passes
- [ ] Manual API testing completed
- [ ] Old code removed
- [ ] Documentation updated
```

---

## See Also

- `create-resource` - Complete workflow for creating a resource
- `integrate-routes` - Mounting routes in app.ts
- `add-authorization-methods` - Adding authorization for entities
- Individual skill files for pattern details
