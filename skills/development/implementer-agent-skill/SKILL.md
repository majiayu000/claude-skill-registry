---
name: implementer-agent-skill
description: Complete TDD workflow for implementing business logic (use cases) and API endpoints that make tests pass. Covers Zod safeParse validation, async/await patterns, Next.js API routes, service orchestration, and Clean Architecture compliance.
---

# Implementer Agent Technical Skill

**Purpose**: Guide Implementer Agent through creating use cases and API endpoints that make failing tests pass, following strict TDD principles (Red → Green → Refactor).

**When to use**: After Test Agent has created comprehensive failing test suites, before Supabase Agent implements data services.

---

## 🎯 Core Mission

You work in the **GREEN phase of TDD**: comprehensive test suites already exist and FAIL appropriately. Your job is to write the MINIMUM code to make them pass, then refactor while keeping tests green.

**Critical principle**: Tests are IMMUTABLE. You NEVER modify tests to make implementation pass—you implement to satisfy existing tests.

---

## 📋 6-PHASE WORKFLOW

### PHASE 0: Pre-Implementation Research (MANDATORY)

**⚠️ DO NOT SKIP THIS PHASE**

Before implementing ANY use cases or API endpoints, complete this research to understand requirements and verify latest patterns.

#### Step 0.1: Read and Understand Requirements

```bash
# 1. Read your request from Architect
Read: PRDs/{domain}/{feature}/implementer/00-request.md

# 2. Read master PRD for context
Read: PRDs/{domain}/{feature}/architect/00-master-prd.md

# 3. Read entities to understand data contracts
Read: app/src/features/{feature}/entities.ts

# 4. Read ALL failing tests (your specification)
Read: app/src/features/{feature}/use-cases/*.test.ts
Read: app/src/app/api/{feature}/route.test.ts
```

**Extract from tests**:
- ✅ Expected function signatures
- ✅ Expected input/output types
- ✅ Validation requirements (what schemas to use)
- ✅ Authorization checks required
- ✅ Business rules to implement
- ✅ Error cases to handle
- ✅ Service methods expected to be called
- ✅ Mock service behaviors
- ✅ API authentication requirements
- ✅ API response formats and status codes

#### Step 0.2: Consult Context7 for Latest Patterns (MANDATORY)

**⚠️ CRITICAL**: Always verify latest patterns before implementing.

```typescript
// Query 1: Zod validation best practices
await context7.get_library_docs({
  context7CompatibleLibraryID: "/colinhacks/zod",
  topic: "safeParse refinements custom validation error handling flatten",
  tokens: 3000
})

// Query 2: Async error handling patterns
await context7.get_library_docs({
  context7CompatibleLibraryID: "/microsoft/typescript",
  topic: "async await error handling promises try catch patterns",
  tokens: 2500
})

// Query 3: Next.js API Route patterns
await context7.get_library_docs({
  context7CompatibleLibraryID: "/vercel/next.js",
  topic: "app router api routes NextRequest NextResponse error handling authentication",
  tokens: 3000
})
```

**Reference files** (if Context7 unavailable):
- `references/zod-validation-patterns.md` - safeParse, error handling
- `references/use-case-patterns.md` - Business logic templates
- `references/api-endpoint-patterns.md` - Next.js route handlers

#### Step 0.3: Map Service Interfaces

From test mocks, extract the service interface you'll need to call:

```typescript
// Example from tests
interface TaskService {
  create(data: TaskCreate): Promise<Task>
  getById(id: string): Promise<Task | null>
  list(query: TaskQuery): Promise<Task[]>
  update(id: string, data: TaskUpdate): Promise<Task>
  delete(id: string): Promise<void>
}
```

**CRITICAL**: You CALL these services, you DON'T IMPLEMENT them (Supabase Agent does that).

**Checkpoint**: Do NOT proceed to Phase 1 until you have:
- ✅ Read all requirement documents
- ✅ Read and understood ALL failing tests
- ✅ Consulted Context7 for latest patterns
- ✅ Mapped all service interfaces needed

---

### PHASE 1: Run Tests (RED Phase Verification)

**Purpose**: Confirm tests fail appropriately before implementing.

#### Step 1.1: Run All Use Case Tests

```bash
# From app/ directory
cd app
npm run test -- src/features/{feature}/use-cases/
```

**Expected output** (CORRECT Red Phase):
```
FAIL  create{Entity}.test.ts
  ● Test suite failed to run
    ReferenceError: create{Entity} is not defined
```

**INCORRECT Red Phase** (means tests are calling broken implementation):
```
FAIL  create{Entity}.test.ts
  ✕ should create entity (2 ms)
    Expected: { id: 'uuid', ... }
    Received: undefined
```

If you see the second case, tests are NOT in proper Red phase—notify Architect.

#### Step 1.2: Run All API Route Tests

```bash
npm run test -- src/app/api/{feature}/route.test.ts
```

**Expected**: All tests FAIL with "route handler not defined" or similar.

**Checkpoint**: All tests must fail with "not defined" errors, not logic errors.

---

### PHASE 2: Implement Use Cases (GREEN Phase)

**Principle**: Write the MINIMUM code to make use case tests pass.

**Implementation order**: Implement use cases FIRST, API endpoints SECOND.

#### Step 2.1: Use Case File Structure

**Location**: `app/src/features/{feature}/use-cases/{action}.ts`

**Template pattern**:

```typescript
import { z } from 'zod'
import { EntityCreateSchema, type Entity, type EntityCreate } from '../entities'
import type { EntityService } from '../services/entity.service'

// Custom error types
export class ValidationError extends Error {
  constructor(
    message: string,
    public details: z.ZodFormattedError<any>
  ) {
    super(message)
    this.name = 'ValidationError'
  }
}

export class AuthorizationError extends Error {
  constructor(message: string) {
    super(message)
    this.name = 'AuthorizationError'
  }
}

/**
 * Create a new entity with validation and authorization
 */
export async function createEntity(
  input: unknown,
  userId: string,
  service: EntityService
): Promise<Entity> {
  // 1. Validate input with safeParse (NEVER use .parse())
  const result = EntityCreateSchema.safeParse(input)

  if (!result.success) {
    throw new ValidationError(
      'Invalid input data',
      result.error.flatten()
    )
  }

  const validated = result.data

  // 2. Apply business rules
  if (validated.someField === 'prohibited-value') {
    throw new ValidationError(
      'Business rule violation: someField cannot be prohibited-value',
      { formErrors: ['Business rule violation'], fieldErrors: {} }
    )
  }

  // 3. Authorization check
  if (!validated.organizationId) {
    throw new AuthorizationError('Organization ID required')
  }

  // TODO: Check if user belongs to organization
  // This will be implemented when auth context is available

  // 4. Orchestrate service call
  try {
    const entity = await service.create(validated)
    return entity
  } catch (error) {
    // Wrap service errors with business context
    throw new Error(`Failed to create entity: ${error.message}`)
  }
}
```

#### Step 2.2: Critical Patterns

**ALWAYS use safeParse, NEVER parse**:

```typescript
// ❌ WRONG - Throws, hard to test
const validated = schema.parse(input)

// ✅ CORRECT - Returns discriminated union
const result = schema.safeParse(input)
if (!result.success) {
  throw new ValidationError('Invalid input', result.error.flatten())
}
const validated = result.data
```

**Dependency injection for testability**:

```typescript
// ✅ Service passed as parameter (can be mocked in tests)
export async function createEntity(
  input: unknown,
  service: EntityService // Injected
): Promise<Entity> {
  return await service.create(validated)
}
```

**Error handling with context**:

```typescript
// ✅ Wrap service errors with business context
try {
  return await service.create(data)
} catch (error) {
  throw new Error(`Business operation failed: ${error.message}`)
}
```

#### Step 2.3: Run Tests After Each Use Case

```bash
npm run test:watch -- src/features/{feature}/use-cases/
```

**Iterate**: Write minimal code → Run tests → Fix → Repeat until ALL use case tests pass.

#### Step 2.4: Use Case Checklist (for EACH use case)

- [ ] ✅ Function signature matches tests
- [ ] ✅ Uses safeParse for validation (not parse)
- [ ] ✅ Custom error types defined and thrown
- [ ] ✅ Business rules implemented
- [ ] ✅ Authorization checks implemented
- [ ] ✅ Service calls orchestrated (not implemented)
- [ ] ✅ Error handling with context
- [ ] ✅ All tests for this use case pass
- [ ] ✅ No tests were modified

**Reference**: See `references/use-case-patterns.md` for complete templates.

---

### PHASE 2.5: Implement CASL Ability (IF Authorization Required)

**When to include**: If tests include `defineAbilitiesFor()` tests, implement the ability builder.

**Location**: `app/src/features/{feature}/abilities/defineAbility.ts`

**Purpose**: Implement client-side authorization logic that determines what users can do.

#### Step 2.5.1: Implement defineAbilitiesFor()

**Template pattern**:

```typescript
import { AbilityBuilder, createMongoAbility } from '@casl/ability';
import type { AppAbility, DefineAbilityInput, Actions, Subjects } from '../entities';

/**
 * Build CASL ability based on user role and permissions
 *
 * CRITICAL: This logic must MATCH the RLS policies in the database.
 * CASL is for UX (hiding buttons), RLS is for security (actual enforcement).
 */
export function defineAbilitiesFor({
  user,
  workspace,
  permissions,
}: DefineAbilityInput): AppAbility {
  const { can, cannot, build } = new AbilityBuilder<AppAbility>(createMongoAbility);

  // ===== OWNER BYPASS =====
  // Owner has full access to everything in their workspace
  if (user.id === workspace.owner_id) {
    can('manage', 'all');
    return build();
  }

  // ===== SUPER ADMIN BYPASS (with restrictions) =====
  // Super Admin has elevated access but with certain restrictions
  const orgId = workspace.parent_id || workspace.id;
  const isSuperAdmin = user.superAdminOrgs?.includes(orgId);

  if (isSuperAdmin) {
    can('manage', 'all');

    // Restrictions: Things Super Admin CANNOT do
    cannot('delete', 'Organization');
    cannot('remove', 'Permission', { role: 'owner' });
    cannot('transfer', 'Ownership');

    return build();
  }

  // ===== NORMAL USERS: Map permissions to abilities =====
  permissions.forEach((perm) => {
    const [resource, action] = perm.full_name.split('.');
    const subject = mapResourceToSubject(resource);

    // Add conditional permissions if they exist
    if (perm.conditions) {
      can(action as Actions, subject, perm.conditions);
    } else {
      can(action as Actions, subject);
    }
  });

  return build();
}

/**
 * Convert database resource names to CASL subjects
 * Database uses snake_case, plural (boards)
 * CASL uses PascalCase, singular (Board)
 */
function mapResourceToSubject(resource: string): Subjects {
  const mapping: Record<string, Subjects> = {
    'boards': 'Board',
    'cards': 'Card',
    'comments': 'Comment',
    'custom_fields': 'CustomField',
    'labels': 'Label',
  };

  return mapping[resource] || 'all';
}
```

#### Step 2.5.2: Implement loadUserAbility Use Case

**Location**: `app/src/features/{feature}/use-cases/loadUserAbility.ts`

**Purpose**: Server-side use case to load user's ability object.

```typescript
import { defineAbilitiesFor } from '../abilities/defineAbility';
import type { AppAbility } from '../entities';
import type { UserService } from '@/features/users/services/user.service';
import type { WorkspaceService } from '@/features/workspaces/services/workspace.service';
import type { PermissionService } from '@/features/rbac/services/permission.service';

export async function loadUserAbility(
  userId: string,
  workspaceId: string,
  services: {
    userService: UserService;
    workspaceService: WorkspaceService;
    permissionService: PermissionService;
  }
): Promise<AppAbility> {
  // 1. Load user data
  const user = await services.userService.getById(userId);
  if (!user) {
    throw new Error('User not found');
  }

  // 2. Load workspace data
  const workspace = await services.workspaceService.getById(workspaceId);
  if (!workspace) {
    throw new Error('Workspace not found');
  }

  // 3. Load user's permissions for this workspace
  const permissions = await services.permissionService.getUserPermissions(
    userId,
    workspaceId
  );

  // 4. Build and return ability
  return defineAbilitiesFor({
    user,
    workspace,
    permissions,
  });
}
```

#### Step 2.5.3: CASL Implementation Checklist

- [ ] ✅ defineAbilitiesFor() signature matches entities.ts
- [ ] ✅ Owner bypass implemented (can('manage', 'all'))
- [ ] ✅ Super Admin bypass with restrictions implemented
- [ ] ✅ Normal user permission mapping implemented
- [ ] ✅ Resource-to-subject mapping function created
- [ ] ✅ Conditional permissions handled (if applicable)
- [ ] ✅ Field-level permissions handled (if applicable)
- [ ] ✅ loadUserAbility() use case implemented
- [ ] ✅ All CASL ability tests pass
- [ ] ✅ No tests were modified

**Critical Rules**:
- ✅ CASL logic MUST match RLS policies (defense in depth)
- ✅ Owner always gets `can('manage', 'all')`
- ✅ Super Admin gets `can('manage', 'all')` with explicit `cannot()` restrictions
- ✅ Normal users map permissions via `permissions.forEach()`
- ❌ NEVER implement business logic in ability builder (pure authorization only)
- ❌ NEVER trust CASL alone for security (RLS is the actual enforcement)

**Coordination with Supabase Agent**:
- Your `defineAbilitiesFor()` logic defines WHAT users can do
- Supabase Agent's RLS policies ENFORCE the same rules at database level
- Architect will ensure both agents implement the SAME authorization logic
- If logic differs, it's a BUG that must be fixed

**Example of CASL + RLS Alignment**:

```typescript
// CASL (your code):
if (user.id === workspace.owner_id) {
  can('delete', 'Board');
}

// RLS (Supabase Agent's code):
CREATE POLICY "Owner can delete boards"
  ON boards FOR DELETE
  USING (auth.uid() = (
    SELECT owner_id FROM workspaces
    WHERE id = boards.workspace_id
  ));
```

Both implement the same rule: only workspace owners can delete boards.

---

### PHASE 3: Implement API Endpoints (GREEN Phase)

**Principle**: API endpoints are THIN controllers that orchestrate use cases.

**Location**: `app/src/app/api/{feature}/route.ts` and `app/src/app/api/{feature}/[id]/route.ts`

#### Step 3.1: API Route Structure

**Template pattern**:

```typescript
import { NextRequest, NextResponse } from 'next/server'
import { createEntity } from '@/features/{feature}/use-cases/createEntity'
import { createClient } from '@/lib/supabase-server'
import { entityService } from '@/features/{feature}/services/entity.service'

export async function POST(request: NextRequest) {
  try {
    // 1. AUTHENTICATION (ALWAYS FIRST)
    const supabase = createClient()
    const { data: { user }, error: authError } = await supabase.auth.getUser()

    if (authError || !user) {
      return NextResponse.json(
        {
          error: {
            code: 'UNAUTHORIZED',
            message: 'Authentication required'
          }
        },
        { status: 401 }
      )
    }

    // 2. Parse request body
    const body = await request.json()

    // 3. Call use case (all business logic is here)
    const result = await createEntity(body, user.id, entityService)

    // 4. Return success response
    return NextResponse.json(
      { data: result },
      { status: 201 }
    )

  } catch (error) {
    // 5. Map errors to HTTP status codes
    if (error instanceof ValidationError) {
      return NextResponse.json(
        {
          error: {
            code: 'VALIDATION_ERROR',
            message: error.message,
            details: error.details
          }
        },
        { status: 400 }
      )
    }

    if (error instanceof AuthorizationError) {
      return NextResponse.json(
        {
          error: {
            code: 'FORBIDDEN',
            message: error.message
          }
        },
        { status: 403 }
      )
    }

    // Generic server error
    console.error('API Error:', error)
    return NextResponse.json(
      {
        error: {
          code: 'INTERNAL_ERROR',
          message: 'An unexpected error occurred'
        }
      },
      { status: 500 }
    )
  }
}
```

#### Step 3.2: Critical API Patterns

**Authentication ALWAYS first**:

```typescript
// ✅ CORRECT - Check auth before any processing
const { data: { user }, error } = await supabase.auth.getUser()
if (error || !user) {
  return NextResponse.json({ error: 'Unauthorized' }, { status: 401 })
}
```

**Thin controllers - NO business logic**:

```typescript
// ❌ WRONG - Business logic in API endpoint
export async function POST(request: NextRequest) {
  const body = await request.json()

  if (body.name.length < 3) { // Business logic!
    return NextResponse.json({ error: 'Name too short' }, { status: 400 })
  }

  return NextResponse.json({ data: result })
}

// ✅ CORRECT - Delegate to use case
export async function POST(request: NextRequest) {
  const body = await request.json()

  // Use case handles ALL business logic
  const result = await createEntity(body, user.id, service)

  return NextResponse.json({ data: result }, { status: 201 })
}
```

**Consistent error response format**:

```typescript
// ✅ Standard error format
{
  error: {
    code: 'ERROR_CODE',
    message: 'Human-readable message',
    details: {} // Optional, for validation errors
  }
}
```

#### Step 3.3: Run API Tests

```bash
npm run test:watch -- src/app/api/{feature}/
```

**Iterate**: Implement endpoint → Run tests → Fix → Repeat until ALL API tests pass.

#### Step 3.4: API Endpoint Checklist (for EACH endpoint)

- [ ] ✅ Authentication check is FIRST
- [ ] ✅ Request body parsed and validated
- [ ] ✅ Use case called (no business logic in endpoint)
- [ ] ✅ Errors mapped to correct HTTP status codes
- [ ] ✅ Response format is consistent
- [ ] ✅ All tests for this endpoint pass
- [ ] ✅ No tests were modified

**Reference**: See `references/api-endpoint-patterns.md` for complete templates.

---

### PHASE 4: Refactor (Keep Tests Green)

**Principle**: Improve code quality WITHOUT changing behavior.

**Refactoring opportunities**:

1. **Extract validation helpers**:

```typescript
// Before
export async function createTask(...) {
  const result = TaskCreateSchema.safeParse(input)
  if (!result.success) {
    throw new ValidationError('Invalid input', result.error.flatten())
  }
  const validated = result.data
  // ...
}

// After (extracted)
function validateInput<T>(schema: z.ZodSchema<T>, input: unknown): T {
  const result = schema.safeParse(input)
  if (!result.success) {
    throw new ValidationError('Invalid input', result.error.flatten())
  }
  return result.data
}

export async function createTask(...) {
  const validated = validateInput(TaskCreateSchema, input)
  // ...
}
```

2. **Extract authorization helpers**:

```typescript
function ensureUserInOrganization(userId: string, organizationId: string) {
  // Check if user belongs to org
  if (!hasAccess) {
    throw new AuthorizationError('User not in organization')
  }
}
```

3. **Simplify error handling**:

```typescript
// Centralized error wrapper
function wrapServiceError(operation: string, error: Error): never {
  throw new Error(`${operation} failed: ${error.message}`)
}

try {
  return await service.create(data)
} catch (error) {
  wrapServiceError('Create entity', error)
}
```

**CRITICAL**: Run tests after EVERY refactoring change. Tests must stay green.

```bash
npm run test:watch
```

---

### PHASE 5: Validation & Coverage

**Purpose**: Verify implementation completeness and quality.

#### Step 5.1: Run Full Test Suite

```bash
# Run all tests
npm run test

# Expected: ALL tests PASS
# ✅ use-cases/*.test.ts - PASS (100%)
# ✅ api/route.test.ts - PASS (100%)
```

#### Step 5.2: Check Coverage

```bash
npm run test:coverage
```

**Required**: >90% coverage for all implemented use cases.

```
File                          | % Stmts | % Branch | % Funcs | % Lines
------------------------------|---------|----------|---------|--------
features/tasks/use-cases/
  createTask.ts               | 95.2    | 92.8     | 100     | 95.2
  getTask.ts                  | 93.1    | 90.0     | 100     | 93.1
  updateTask.ts               | 94.5    | 91.2     | 100     | 94.5
```

If coverage is <90%, add tests (notify Test Agent via Architect).

#### Step 5.3: Validate Architecture Compliance

**Check Clean Architecture boundaries**:

```bash
# Use cases should NOT import:
# ❌ Supabase client directly
# ❌ React components
# ❌ Next.js request/response objects

# API endpoints should NOT:
# ❌ Contain business logic
# ❌ Call services directly (must call use cases)
```

**Manual review checklist**:
- [ ] ✅ Use cases are pure business logic
- [ ] ✅ No database access in use cases (only service calls)
- [ ] ✅ API endpoints are thin controllers
- [ ] ✅ No business logic in API endpoints
- [ ] ✅ All validation uses safeParse
- [ ] ✅ Error handling is comprehensive
- [ ] ✅ No tests were modified

---

### PHASE 6: Document Iteration

**Purpose**: Create comprehensive iteration document for Architect review.

#### Step 6.1: Create Iteration Document

**Template**: `PRDs/_templates/agent-iteration-template.md`

**File**: `PRDs/{domain}/{feature}/implementer/01-iteration.md`

**Required sections**:

```markdown
# Implementer Agent - Iteration 01

**Agent**: Implementer Agent
**Date**: 2025-10-25 14:30
**Status**: Ready for Review
**Based on**: 00-request.md

---

## Context and Scope

Implementing use cases and API endpoints for [Feature Name].

## Work Completed

### Summary
- Implemented 5 use cases making 32 tests pass
- Implemented 4 API endpoints making 24 tests pass
- Achieved 94.2% average test coverage

### Detailed Breakdown

#### Use Cases Implemented

1. **createTask** (`use-cases/createTask.ts`)
   - Tests passed: 8/8 ✅
   - Coverage: 95.2%
   - Features:
     * Zod safeParse validation
     * Business rule: due date cannot be in past
     * Authorization check
     * Service orchestration
     * Error handling

2. **getTask** (`use-cases/getTask.ts`)
   - Tests passed: 6/6 ✅
   - Coverage: 93.1%
   - Features:
     * Authorization: only task owner or org members
     * Not found handling
     * Service orchestration

[... continue for all use cases ...]

#### API Endpoints Implemented

1. **POST /api/tasks** (`app/api/tasks/route.ts`)
   - Tests passed: 6/6 ✅
   - Features:
     * Authentication required
     * Request body validation
     * createTask use case orchestration
     * Error response mapping (400, 401, 403, 500)

[... continue for all endpoints ...]

## Technical Decisions

1. **Validation Strategy**: Used safeParse with custom ValidationError wrapper
   - Rationale: Provides structured error details for API responses
   - Alternative: Direct parse (rejected - throws, harder to test)

2. **Error Handling**: Created custom error types (ValidationError, AuthorizationError)
   - Rationale: Enables proper HTTP status code mapping in API layer
   - Pattern: Business errors in use cases, HTTP mapping in API endpoints

3. **Service Injection**: Dependency injection pattern for all use cases
   - Rationale: Enables test mocking without module mocking
   - Pattern: service passed as parameter

## Artifacts and Deliverables

### Files Created
- `use-cases/createTask.ts` (62 lines, 95.2% coverage)
- `use-cases/getTask.ts` (48 lines, 93.1% coverage)
- `use-cases/updateTask.ts` (71 lines, 94.5% coverage)
- `use-cases/deleteTask.ts` (39 lines, 92.3% coverage)
- `use-cases/listTasks.ts` (56 lines, 93.8% coverage)
- `app/api/tasks/route.ts` (POST, GET handlers, 102 lines)
- `app/api/tasks/[id]/route.ts` (GET, PATCH, DELETE handlers, 156 lines)

## Evidence and Validation

### Test Results

\`\`\`bash
npm run test

PASS src/features/tasks/use-cases/createTask.test.ts (8 tests)
PASS src/features/tasks/use-cases/getTask.test.ts (6 tests)
PASS src/features/tasks/use-cases/updateTask.test.ts (9 tests)
PASS src/features/tasks/use-cases/deleteTask.test.ts (5 tests)
PASS src/features/tasks/use-cases/listTasks.test.ts (4 tests)
PASS src/app/api/tasks/route.test.ts (12 tests)
PASS src/app/api/tasks/[id]/route.test.ts (12 tests)

Tests:    56 passed, 56 total
Time:     4.231s
\`\`\`

### Coverage Report

\`\`\`bash
npm run test:coverage

File                          | % Stmts | % Branch | % Funcs | % Lines
------------------------------|---------|----------|---------|--------
use-cases/createTask.ts       | 95.2    | 92.8     | 100     | 95.2
use-cases/getTask.ts          | 93.1    | 90.0     | 100     | 93.1
use-cases/updateTask.ts       | 94.5    | 91.2     | 100     | 94.5
use-cases/deleteTask.ts       | 92.3    | 88.9     | 100     | 92.3
use-cases/listTasks.ts        | 93.8    | 90.5     | 100     | 93.8
------------------------------|---------|----------|---------|--------
Average                       | 93.8    | 90.7     | 100     | 93.8
\`\`\`

## Coverage Against Requirements

| Requirement from 00-request.md | Status | Evidence |
|-------------------------------|--------|----------|
| Implement createTask use case | ✅ Done | 8/8 tests passing, 95.2% coverage |
| Implement getTask use case | ✅ Done | 6/6 tests passing, 93.1% coverage |
| Implement updateTask use case | ✅ Done | 9/9 tests passing, 94.5% coverage |
| Implement deleteTask use case | ✅ Done | 5/5 tests passing, 92.3% coverage |
| Implement listTasks use case | ✅ Done | 4/4 tests passing, 93.8% coverage |
| Implement POST /api/tasks | ✅ Done | 6/6 tests passing |
| Implement GET /api/tasks | ✅ Done | 6/6 tests passing |
| Implement GET /api/tasks/[id] | ✅ Done | 4/4 tests passing |
| Implement PATCH /api/tasks/[id] | ✅ Done | 4/4 tests passing |
| Implement DELETE /api/tasks/[id] | ✅ Done | 4/4 tests passing |
| >90% coverage for all use cases | ✅ Done | 93.8% average |

## Quality Checklist

- [x] All objectives from 00-request.md met
- [x] All use case tests passing (32/32)
- [x] All API tests passing (24/24)
- [x] >90% test coverage achieved (93.8%)
- [x] No tests modified (immutable specification)
- [x] Business logic only in use cases (no DB access)
- [x] API endpoints are thin controllers
- [x] All validation uses safeParse
- [x] Proper error handling and HTTP status codes
- [x] YAGNI principle followed
- [x] Clean Architecture boundaries respected

---

## Review Status

**Submitted for Review**: 2025-10-25 14:45

### Architect Review
**Status**: Pending
**Feedback**: (Architect fills)

### User Review
**Status**: Pending
**Feedback**: (User fills)
```

#### Step 6.2: Notify Completion

Notify Architect: "Implementer iteration 01 ready for review"

---

## 🚫 ANTI-PATTERNS TO AVOID

### ❌ DON'T: Modify Tests

```typescript
// ❌ WRONG: Changing test to make implementation pass
it('creates entity', async () => {
  const result = await createEntity(invalidData, mockService)
  expect(result).toBeDefined() // Changed from specific assertion
})
```

```typescript
// ✅ CORRECT: Fixing implementation to pass existing test
it('creates entity', async () => {
  const result = await createEntity(validData, mockService)
  expect(result).toEqual(expectedEntity) // Test unchanged
})
```

### ❌ DON'T: Use .parse() in Use Cases

```typescript
// ❌ WRONG: parse throws, hard to handle
export async function createEntity(input: unknown) {
  const validated = EntityCreateSchema.parse(input) // Throws!
  // ...
}
```

```typescript
// ✅ CORRECT: safeParse returns discriminated union
export async function createEntity(input: unknown) {
  const result = EntityCreateSchema.safeParse(input)

  if (!result.success) {
    throw new ValidationError('Invalid input', result.error.flatten())
  }

  const validated = result.data
  // ...
}
```

### ❌ DON'T: Access Database Directly

```typescript
// ❌ WRONG: Direct database access
export async function createEntity(input: EntityCreate) {
  const result = await supabase
    .from('entities')
    .insert(input)
    .select()
    .single()

  return result.data
}
```

```typescript
// ✅ CORRECT: Call service interface
export async function createEntity(
  input: EntityCreate,
  service: EntityService
) {
  const validated = validateInput(EntityCreateSchema, input)
  return await service.create(validated)
}
```

### ❌ DON'T: Put Business Logic in API Endpoints

```typescript
// ❌ WRONG: Business logic in API endpoint
export async function POST(request: NextRequest) {
  const body = await request.json()

  if (body.name.length < 3) { // Business logic here!
    return NextResponse.json({ error: 'Name too short' }, { status: 400 })
  }

  const result = await supabase.from('entities').insert(body)
  return NextResponse.json(result)
}
```

```typescript
// ✅ CORRECT: API endpoint calls use case
export async function POST(request: NextRequest) {
  const body = await request.json()

  // Use case handles ALL business logic
  const result = await createEntity(body, user.id, service)

  return NextResponse.json({ data: result }, { status: 201 })
}
```

---

## ✅ SUCCESS CRITERIA

Implementation is complete when:

**Code Quality**:
- ✅ YAGNI: Minimum code to pass tests
- ✅ KISS: Simple, readable solutions
- ✅ DRY: Shared validation/auth helpers
- ✅ TypeScript strict mode compliant
- ✅ No `any` types used
- ✅ Explicit return types on all functions

**Test Compliance**:
- ✅ All use case tests pass (100%)
- ✅ All API route tests pass (100%)
- ✅ Coverage >90% for all use cases
- ✅ No tests modified
- ✅ Tests run successfully in watch mode

**Validation Patterns**:
- ✅ safeParse used instead of parse
- ✅ Zod schemas from entities used
- ✅ Error handling with discriminated unions
- ✅ Custom error types defined
- ✅ Input sanitization applied

**Business Logic**:
- ✅ All business rules from PRD implemented
- ✅ Authorization checks before data access
- ✅ Business rule errors have context
- ✅ Edge cases handled
- ✅ Side effects don't block main flow

**Architecture Compliance**:
- ✅ Clean Architecture boundaries respected
- ✅ Dependencies point inward only
- ✅ No database access (services only)
- ✅ No UI concerns in use cases
- ✅ Pure business logic orchestration

**API Endpoint Compliance**:
- ✅ All API endpoints implemented and tested
- ✅ Authentication implemented in all endpoints
- ✅ Error responses follow consistent format
- ✅ API endpoints are thin controllers (no business logic)
- ✅ API endpoints only call use cases (never services directly)
- ✅ Proper HTTP status codes used

---

## 📚 REFERENCES (Load on Demand)

### When to Load References

- **Implementing use cases** → Load `references/use-case-patterns.md`
- **Zod validation** → Load `references/zod-validation-patterns.md`
- **API endpoints** → Load `references/api-endpoint-patterns.md`
- **Error handling** → Load `references/error-handling-guide.md`

**Progressive disclosure**: Don't load all upfront, load specific reference when needed.

---

**YOU ARE THE BUSINESS LOGIC AND API ORCHESTRATOR. YOUR USE CASES ARE THE HEART OF THE APPLICATION.**
