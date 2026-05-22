---
name: test-agent-skill
description: Complete TDD workflow for creating comprehensive failing test suites across all architectural layers (entities, use cases, services, APIs, E2E) using Vitest, Playwright, and Testing Library. Mandatory Context7 consultation for latest testing patterns.
---

# Test Agent Technical Skill

**Purpose**: Guide Test Agent through creating comprehensive failing test suites that serve as the living specification for features before any implementation begins.

**When to use**: Immediately after Architect delivers PRD + entities, before Implementer or any other agent begins work.

---

## 🎯 Core Mission

You create the **RED phase of TDD**: comprehensive test suites that FAIL appropriately, defining exactly what must be implemented. Your tests are the immutable specification—once created, they cannot be modified.

**Critical principle**: ALL tests must FAIL initially with "not defined" or "not implemented" errors, proving no implementation exists yet.

---

## 📋 6-PHASE WORKFLOW

### PHASE 0: Pre-Testing Research (CRITICAL - MANDATORY)

**⚠️ DO NOT SKIP THIS PHASE**

Before creating ANY test files, complete this research to understand requirements and verify latest patterns.

#### Step 0.1: Read and Understand Requirements

```bash
# 1. Read your request from Architect
Read: PRDs/{domain}/{feature}/test-agent/00-request.md

# 2. Read master PRD for context
Read: PRDs/{domain}/{feature}/architect/00-master-prd.md

# 3. Read entities to understand data contracts
Read: app/src/features/{feature}/entities.ts
```

**Extract from PRD**:
- ✅ All user stories and acceptance criteria
- ✅ Data contracts and validation rules
- ✅ API specifications (endpoints, request/response formats)
- ✅ Business rules and edge cases
- ✅ Security requirements (RLS policies, authorization)
- ✅ Performance requirements

#### Step 0.2: Consult Context7 for Latest Patterns (MANDATORY)

**⚠️ CRITICAL**: Always verify latest testing patterns before creating tests.

```typescript
// Query 1: Vitest mocking patterns
await context7.get_library_docs({
  context7CompatibleLibraryID: "/vitest-dev/vitest",
  topic: "mocking vi.mock vi.spyOn best practices",
  tokens: 2000
})

// Query 2: Playwright E2E patterns
await context7.get_library_docs({
  context7CompatibleLibraryID: "/microsoft/playwright",
  topic: "user flow testing accessibility keyboard navigation",
  tokens: 2500
})

// Query 3: Zod validation testing
await context7.get_library_docs({
  context7CompatibleLibraryID: "/colinhacks/zod",
  topic: "safeParse testing error validation",
  tokens: 2000
})
```

**Reference files** (if Context7 unavailable):
- `references/vitest-patterns.md` - Mocking strategies
- `references/playwright-e2e-patterns.md` - E2E best practices
- `references/zod-testing-patterns.md` - Schema validation

#### Step 0.3: Plan Test Coverage

Create mental map of ALL tests needed:

```markdown
**Entities Layer**:
- [ ] Schema validation for all fields
- [ ] Edge cases (empty, null, undefined, wrong types)
- [ ] Refinement validations (custom rules)
- [ ] Create/Update/Query schema tests

**Use Cases Layer** (for EACH use case):
- [ ] Happy path
- [ ] Business rule validations
- [ ] Authorization checks
- [ ] Error handling
- [ ] Edge cases and boundaries

**Services Layer**:
- [ ] CRUD operations
- [ ] Query filters and pagination
- [ ] Data transformations (snake_case ↔ camelCase)
- [ ] Database error handling

**API Layer** (for EACH endpoint):
- [ ] Authentication
- [ ] Authorization
- [ ] Request validation
- [ ] Response formatting
- [ ] HTTP status codes
- [ ] Error responses

**E2E Layer**:
- [ ] Complete CRUD workflows
- [ ] Accessibility (WCAG 2.1 AA)
- [ ] Keyboard navigation
- [ ] Loading/error states
```

**Checkpoint**: Do NOT proceed to Phase 1 until you have:
- ✅ Read all requirement documents
- ✅ Consulted Context7 for latest patterns
- ✅ Mapped complete test coverage

---

### PHASE 1: Create Entity Tests

**File**: `app/src/features/{feature}/entities.test.ts`

**Purpose**: Validate Zod schemas correctly enforce data contracts.

#### Step 1.1: Use Template

Start with `assets/entity-test-template.ts` as boilerplate.

#### Step 1.2: Test Main Schema

```typescript
import { describe, it, expect } from 'vitest'
import { EntitySchema } from './entities'

describe('EntitySchema', () => {
  describe('valid data', () => {
    it('accepts valid complete entity', () => {
      const validEntity = {
        id: '550e8400-e29b-41d4-a716-446655440000',
        field1: 'Valid Value',
        userId: '550e8400-e29b-41d4-a716-446655440001',
        organizationId: '550e8400-e29b-41d4-a716-446655440002',
        createdAt: new Date('2024-01-01T00:00:00Z'),
        updatedAt: new Date('2024-01-02T00:00:00Z'),
      }

      const result = EntitySchema.safeParse(validEntity)

      expect(result.success).toBe(true)
      if (result.success) {
        expect(result.data).toEqual(validEntity)
      }
    })
  })

  describe('invalid data', () => {
    it('rejects entity with invalid uuid', () => {
      const invalidEntity = {
        id: 'not-a-uuid',
        // ... other fields
      }

      const result = EntitySchema.safeParse(invalidEntity)

      expect(result.success).toBe(false)
      if (!result.success) {
        expect(result.error.issues[0].validation).toBe('uuid')
      }
    })

    // Add tests for EACH validation rule from PRD
  })
})
```

**CRITICAL**: Use `.safeParse()` NEVER `.parse()` in tests.

#### Step 1.3: Test Derived Schemas

```typescript
describe('EntityCreateSchema', () => {
  it('accepts data without auto-generated fields', () => {
    const createData = {
      field1: 'Valid Value',
      userId: 'user-id',
      organizationId: 'org-id',
      // id, createdAt, updatedAt omitted
    }

    const result = EntityCreateSchema.safeParse(createData)
    expect(result.success).toBe(true)
  })

  it('rejects data with id field', () => {
    const createData = {
      id: 'should-not-be-here',
      field1: 'Valid Value',
      // ...
    }

    const result = EntityCreateSchema.safeParse(createData)
    expect(result.success).toBe(false)
  })
})

describe('EntityUpdateSchema', () => {
  it('accepts partial data', () => {
    const updateData = { field1: 'Updated' }
    const result = EntityUpdateSchema.safeParse(updateData)
    expect(result.success).toBe(true)
  })
})
```

#### Step 1.4: Entity Test Checklist

- [ ] ✅ All schemas tested (main, Create, Update, Query)
- [ ] ✅ Valid data tests
- [ ] ✅ Invalid data tests (for EACH validation rule)
- [ ] ✅ Missing required field tests
- [ ] ✅ Min/max length tests
- [ ] ✅ Enum value tests
- [ ] ✅ UUID validation tests
- [ ] ✅ Refinement tests (custom validations)
- [ ] ✅ Uses .safeParse() everywhere
- [ ] ✅ Tests both success and error branches

**Reference**: See `references/zod-testing-patterns.md` for complete patterns.

---

### PHASE 2: Create Use Case Tests

**Files**: `app/src/features/{feature}/use-cases/{action}.test.ts`

**Purpose**: Define expected business logic behavior (will FAIL: functions not defined).

#### Step 2.1: Use Template

Start with `assets/use-case-test-template.ts`.

#### Step 2.2: Configure Mocks

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { createEntity } from './createEntity'
import type { EntityService } from '../services/entity.service'

// Mock the service module
vi.mock('../services/entity.service')

describe('createEntity', () => {
  let mockService: jest.Mocked<EntityService>

  beforeEach(() => {
    mockService = {
      create: vi.fn(),
      getById: vi.fn(),
      list: vi.fn(),
      update: vi.fn(),
      delete: vi.fn(),
    }
  })

  // Tests go here
})
```

**Reference**: See `references/vitest-patterns.md` for mocking strategies.

#### Step 2.3: Test Structure (for EACH use case)

```typescript
describe('createEntity', () => {
  describe('happy path', () => {
    it('creates entity with valid data', async () => {
      // Arrange
      const createData = { field1: 'Test' }
      const expectedEntity = { id: 'uuid', ...createData }
      mockService.create.mockResolvedValue(expectedEntity)

      // Act
      const result = await createEntity(createData, mockService)

      // Assert
      expect(result).toEqual(expectedEntity)
      expect(mockService.create).toHaveBeenCalledWith(createData)
      expect(mockService.create).toHaveBeenCalledTimes(1)
    })
  })

  describe('validation', () => {
    it('rejects invalid data', async () => {
      const invalidData = { field1: '' } // Empty (invalid)

      await expect(
        createEntity(invalidData, mockService)
      ).rejects.toThrow('Validation failed')

      expect(mockService.create).not.toHaveBeenCalled()
    })
  })

  describe('authorization', () => {
    it('allows creation in own organization', async () => {
      // Test authorization logic
    })

    it('rejects creation in unauthorized organization', async () => {
      // Test authorization rejection
    })
  })

  describe('business rules', () => {
    it('enforces unique constraint', async () => {
      // Test business rule validation
    })
  })

  describe('error handling', () => {
    it('handles database errors', async () => {
      mockService.create.mockRejectedValue(new Error('DB error'))

      await expect(
        createEntity(createData, mockService)
      ).rejects.toThrow('Failed to create')
    })
  })

  describe('edge cases', () => {
    it('handles unicode characters', async () => {
      // Test unicode support
    })
  })
})
```

#### Step 2.4: Use Case Test Checklist (for EACH use case)

- [ ] ✅ Happy path with valid data
- [ ] ✅ Input validation (all validation rules from PRD)
- [ ] ✅ Authorization checks (user/org permissions)
- [ ] ✅ Business rules (from PRD)
- [ ] ✅ Error handling (database, network, unexpected)
- [ ] ✅ Edge cases (unicode, max lengths, boundaries)
- [ ] ✅ Service mock configured
- [ ] ✅ Service calls verified
- [ ] ✅ Service NOT called when validation fails

**Reference**: See `references/test-structure-guide.md` for Arrange-Act-Assert pattern.

---

### PHASE 2.5: Create CASL Ability Tests (IF Authorization Required)

**File**: `app/src/features/{feature}/abilities/defineAbility.test.ts`

**Purpose**: Define authorization behavior for permission-based features (will FAIL: defineAbilitiesFor not defined).

**When to include**: If PRD specifies permission checks, role-based access, or Owner/Super Admin rules.

#### Step 2.5.1: Test Structure Template

```typescript
import { describe, it, expect } from 'vitest';
import { defineAbilitiesFor } from './defineAbility';
import type { User, Workspace, Permission } from '../entities';

describe('defineAbilitiesFor', () => {
  // RED phase: This should fail initially
  it('should not be defined yet (RED phase)', () => {
    expect(defineAbilitiesFor).toBeUndefined();
  });

  // These tests will fail until Implementer creates the function
  describe('Owner bypass', () => {
    it('Owner can manage all resources', () => {
      const owner: User = {
        id: 'owner-id',
        email: 'owner@test.com',
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'owner-id',
      };

      const ability = defineAbilitiesFor({
        user: owner,
        workspace,
        permissions: [],
      });

      expect(ability.can('manage', 'all')).toBe(true);
      expect(ability.can('delete', 'Board')).toBe(true);
      expect(ability.can('create', 'Card')).toBe(true);
    });
  });

  describe('Super Admin', () => {
    it('Super Admin can manage most resources', () => {
      const superAdmin: User = {
        id: 'admin-id',
        email: 'admin@test.com',
        superAdminOrgs: ['org-id'],
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'different-owner-id',
        parent_id: 'org-id', // Part of org where user is Super Admin
      };

      const ability = defineAbilitiesFor({
        user: superAdmin,
        workspace,
        permissions: [],
      });

      expect(ability.can('manage', 'all')).toBe(true);
      expect(ability.can('read', 'Board')).toBe(true);
      expect(ability.can('update', 'Card')).toBe(true);
    });

    it('Super Admin cannot delete Organization', () => {
      const superAdmin: User = {
        id: 'admin-id',
        email: 'admin@test.com',
        superAdminOrgs: ['org-id'],
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'different-owner-id',
        parent_id: 'org-id',
      };

      const ability = defineAbilitiesFor({
        user: superAdmin,
        workspace,
        permissions: [],
      });

      expect(ability.can('delete', 'Organization')).toBe(false);
    });

    it('Super Admin cannot remove Owner permissions', () => {
      const superAdmin: User = {
        id: 'admin-id',
        email: 'admin@test.com',
        superAdminOrgs: ['org-id'],
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'different-owner-id',
        parent_id: 'org-id',
      };

      const ability = defineAbilitiesFor({
        user: superAdmin,
        workspace,
        permissions: [],
      });

      expect(ability.can('remove', 'Permission', { role: 'owner' })).toBe(false);
    });
  });

  describe('Permission-based access', () => {
    it('User with boards.create permission can create boards', () => {
      const user: User = {
        id: 'user-id',
        email: 'user@test.com',
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'different-owner-id',
      };
      const permissions: Permission[] = [
        { id: '1', full_name: 'boards.create', user_id: 'user-id' },
      ];

      const ability = defineAbilitiesFor({ user, workspace, permissions });

      expect(ability.can('create', 'Board')).toBe(true);
    });

    it('User with boards.update permission can update boards', () => {
      const user: User = {
        id: 'user-id',
        email: 'user@test.com',
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'different-owner-id',
      };
      const permissions: Permission[] = [
        { id: '1', full_name: 'boards.update', user_id: 'user-id' },
      ];

      const ability = defineAbilitiesFor({ user, workspace, permissions });

      expect(ability.can('update', 'Board')).toBe(true);
      expect(ability.can('delete', 'Board')).toBe(false); // No delete permission
    });

    it('User without permission cannot access resource', () => {
      const user: User = {
        id: 'user-id',
        email: 'user@test.com',
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'different-owner-id',
      };
      const permissions: Permission[] = []; // No permissions

      const ability = defineAbilitiesFor({ user, workspace, permissions });

      expect(ability.can('create', 'Board')).toBe(false);
      expect(ability.can('read', 'Board')).toBe(false);
      expect(ability.can('update', 'Board')).toBe(false);
      expect(ability.can('delete', 'Board')).toBe(false);
    });
  });

  describe('Conditional permissions', () => {
    it('User can only update own cards', () => {
      const user: User = {
        id: 'user-id',
        email: 'user@test.com',
      };
      const workspace: Workspace = {
        id: 'workspace-id',
        owner_id: 'different-owner-id',
      };
      const permissions: Permission[] = [
        { id: '1', full_name: 'cards.update', user_id: 'user-id', conditions: { user_id: 'user-id' } },
      ];

      const ability = defineAbilitiesFor({ user, workspace, permissions });

      expect(ability.can('update', 'Card', { user_id: 'user-id' })).toBe(true);
      expect(ability.can('update', 'Card', { user_id: 'other-user-id' })).toBe(false);
    });
  });
});
```

#### Step 2.5.2: E2E Tests for CASL Visibility

**File**: `e2e/{feature}/authorization.spec.ts`

**Purpose**: Verify `<Can>` component correctly hides/shows UI based on abilities.

```typescript
import { test, expect } from '@playwright/test';

test.describe('Board authorization', () => {
  test('user without delete permission cannot see delete button', async ({ page }) => {
    // Login as user WITHOUT boards.delete permission
    await page.goto('/login');
    await page.fill('[name="email"]', 'viewer@test.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Navigate to boards page
    await page.goto('/boards/123');

    // Delete button should NOT exist in DOM
    const deleteButton = page.getByRole('button', { name: /delete/i });
    await expect(deleteButton).not.toBeVisible();
  });

  test('user with delete permission sees delete button', async ({ page }) => {
    // Login as user WITH boards.delete permission
    await page.goto('/login');
    await page.fill('[name="email"]', 'editor@test.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Navigate to boards page
    await page.goto('/boards/123');

    // Delete button SHOULD be visible
    const deleteButton = page.getByRole('button', { name: /delete/i });
    await expect(deleteButton).toBeVisible();
  });

  test('Owner sees all action buttons', async ({ page }) => {
    // Login as workspace Owner
    await page.goto('/login');
    await page.fill('[name="email"]', 'owner@test.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Navigate to boards page
    await page.goto('/boards/123');

    // All buttons should be visible
    await expect(page.getByRole('button', { name: /create/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /edit/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /delete/i })).toBeVisible();
    await expect(page.getByRole('button', { name: /settings/i })).toBeVisible();
  });

  test('user without access is redirected or sees empty state', async ({ page }) => {
    // Login as user from different organization
    await page.goto('/login');
    await page.fill('[name="email"]', 'outsider@test.com');
    await page.fill('[name="password"]', 'password');
    await page.click('button[type="submit"]');

    // Try to navigate to boards page
    await page.goto('/boards/123');

    // Should redirect to 403 or show "No access" message
    await expect(page).toHaveURL(/\/(403|forbidden|no-access)/);
    // OR
    await expect(page.getByText(/you don't have access/i)).toBeVisible();
  });
});
```

#### Step 2.5.3: CASL Test Checklist

- [ ] ✅ defineAbilitiesFor() initially undefined (RED phase)
- [ ] ✅ Owner can manage 'all' resources
- [ ] ✅ Super Admin can manage 'all' with restrictions
- [ ] ✅ Super Admin cannot delete Organization
- [ ] ✅ Super Admin cannot remove Owner permissions
- [ ] ✅ User with permission can perform action
- [ ] ✅ User without permission cannot perform action
- [ ] ✅ Conditional permissions tested (if applicable)
- [ ] ✅ Field-level permissions tested (if applicable)
- [ ] ✅ E2E tests verify <Can> component visibility
- [ ] ✅ E2E tests cover all user roles (Owner, Super Admin, Editor, Viewer)
- [ ] ✅ E2E tests verify unauthorized access handling

**Critical Rules**:
- ❌ DON'T test CASL library itself (trust it works)
- ✅ DO test your defineAbilitiesFor() logic
- ✅ DO test that abilities match PRD requirements
- ✅ DO test Owner/Super Admin special cases
- ✅ DO verify E2E visibility matches abilities

---

### PHASE 3: Create Service Tests

**Files**: `app/src/features/{feature}/services/{entity}.service.test.ts`

**Purpose**: Define data access behavior (will FAIL: service not defined).

#### Step 3.1: Use Template

Start with `assets/service-test-template.ts`.

#### Step 3.2: Mock Supabase Client

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { EntityService } from './entity.service'
import type { SupabaseClient } from '@supabase/supabase-js'

const createSupabaseMock = () => {
  const selectMock = vi.fn()
  const eqMock = vi.fn()
  const singleMock = vi.fn()
  const insertMock = vi.fn()
  const updateMock = vi.fn()
  const deleteMock = vi.fn()

  const queryBuilder = {
    select: selectMock.mockReturnThis(),
    eq: eqMock.mockReturnThis(),
    single: singleMock.mockReturnThis(),
    insert: insertMock.mockReturnThis(),
    update: updateMock.mockReturnThis(),
    delete: deleteMock.mockReturnThis(),
  }

  const supabase = {
    from: vi.fn(() => queryBuilder),
    auth: { getUser: vi.fn() },
  } as unknown as SupabaseClient

  return { supabase, mocks: { selectMock, eqMock, singleMock, insertMock, updateMock, deleteMock } }
}
```

**Reference**: See `references/vitest-patterns.md` for Supabase mocking patterns.

#### Step 3.3: Test CRUD Operations

```typescript
describe('EntityService', () => {
  let service: EntityService
  let supabase: SupabaseClient
  let mocks: ReturnType<typeof createSupabaseMock>['mocks']

  beforeEach(() => {
    const mockSetup = createSupabaseMock()
    supabase = mockSetup.supabase
    mocks = mockSetup.mocks
    service = new EntityService(supabase)
  })

  describe('create', () => {
    it('inserts new entity into database', async () => {
      const createData = { field1: 'Test', userId: 'user-123' }
      const createdEntity = {
        id: 'uuid',
        ...createData,
        created_at: '2024-01-01T00:00:00Z',
      }

      mocks.singleMock.mockResolvedValue({
        data: createdEntity,
        error: null,
      })

      const result = await service.create(createData)

      expect(supabase.from).toHaveBeenCalledWith('table_name')
      expect(mocks.insertMock).toHaveBeenCalledWith([{
        field1: createData.field1,
        user_id: createData.userId, // camelCase → snake_case
      }])
      expect(result).toEqual(expect.objectContaining({
        id: 'uuid',
        userId: 'user-123', // snake_case → camelCase
      }))
    })

    it('transforms snake_case from DB to camelCase', async () => {
      // Test case transformation
    })

    it('throws error when insert fails', async () => {
      mocks.singleMock.mockResolvedValue({
        data: null,
        error: { message: 'DB error', code: '23505' },
      })

      await expect(service.create(createData)).rejects.toThrow('DB error')
    })
  })

  // Similar structure for getById, list, update, delete
})
```

#### Step 3.4: Service Test Checklist

- [ ] ✅ CRUD operations tested
- [ ] ✅ snake_case ↔ camelCase transformation
- [ ] ✅ Pagination and sorting
- [ ] ✅ Filters (organizationId, userId)
- [ ] ✅ Error handling (not found, connection)
- [ ] ✅ Null return for not found (don't throw)
- [ ] ✅ Supabase client properly mocked
- [ ] ✅ Query builder chain tested
- [ ] ✅ NO business logic in tests

---

### PHASE 4: Create API Route Tests

**Files**: `app/src/app/api/{feature}/route.test.ts`

**Purpose**: Define API behavior (will FAIL: handlers not defined).

#### Step 4.1: Use Template

Start with `assets/api-route-test-template.ts`.

#### Step 4.2: Mock Dependencies

```typescript
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { GET, POST, PATCH, DELETE } from './route'
import { NextRequest } from 'next/server'

vi.mock('@/features/{feature}/use-cases/createEntity')
vi.mock('@/lib/supabase-server')

import { createEntity } from '@/features/{feature}/use-cases/createEntity'
import { createClient } from '@/lib/supabase-server'
```

#### Step 4.3: Test API Endpoints

```typescript
describe('POST /api/{feature}', () => {
  beforeEach(() => {
    vi.clearAllMocks()

    // Mock authenticated user
    vi.mocked(createClient).mockReturnValue({
      auth: {
        getUser: vi.fn().mockResolvedValue({
          data: { user: { id: 'user-123' } },
          error: null,
        }),
      },
    } as any)
  })

  describe('authentication', () => {
    it('requires authentication', async () => {
      vi.mocked(createClient).mockReturnValue({
        auth: {
          getUser: vi.fn().mockResolvedValue({
            data: { user: null },
            error: { message: 'Not authenticated' },
          }),
        },
      } as any)

      const request = new NextRequest('http://localhost:3000/api/feature', {
        method: 'POST',
        body: JSON.stringify({ field1: 'Test' }),
      })

      const response = await POST(request)

      expect(response.status).toBe(401)
      const data = await response.json()
      expect(data.error.code).toBe('UNAUTHORIZED')
    })
  })

  describe('validation', () => {
    it('validates request body with Zod', async () => {
      const invalidData = { field1: '' } // Invalid

      const request = new NextRequest('http://localhost:3000/api/feature', {
        method: 'POST',
        body: JSON.stringify(invalidData),
      })

      const response = await POST(request)

      expect(response.status).toBe(400)
      const data = await response.json()
      expect(data.error.code).toBe('VALIDATION_ERROR')
    })
  })

  describe('authorization', () => {
    it('allows creation in own organization', async () => {
      // Test authorization
    })

    it('rejects unauthorized access', async () => {
      // Test rejection
    })
  })
})
```

#### Step 4.4: API Test Checklist (for EACH endpoint)

- [ ] ✅ Authentication required (401)
- [ ] ✅ Valid request succeeds
- [ ] ✅ Invalid JSON rejected (400)
- [ ] ✅ Schema validation (400)
- [ ] ✅ Authorization checks (403)
- [ ] ✅ Not found handling (404)
- [ ] ✅ Error responses (500)
- [ ] ✅ Proper response format

---

### PHASE 5: Create E2E Tests

**Files**: `app/e2e/{feature-name}.spec.ts`

**Purpose**: Define complete user workflows (will FAIL: no UI exists).

#### Step 5.1: Use Template

Start with `assets/e2e-test-template.spec.ts`.

#### Step 5.2: Test User Flows

```typescript
import { test, expect } from '@playwright/test'

test.describe('{Feature} - User Flows', () => {
  test.beforeEach(async ({ page }) => {
    // Login and navigate
    await page.goto('/login')
    await page.fill('[data-testid="email"]', 'test@example.com')
    await page.fill('[data-testid="password"]', 'password123')
    await page.click('[data-testid="submit"]')
    await page.waitForURL('/dashboard')

    await page.goto('/{feature-path}')
  })

  test.describe('Create {Entity} Flow', () => {
    test('should create entity with valid data', async ({ page }) => {
      // Arrange: Open create form
      await page.click('[data-testid="create-button"]')
      await expect(page.locator('[data-testid="create-modal"]')).toBeVisible()

      // Act: Fill and submit
      await page.fill('[data-testid="field1-input"]', 'Valid Value')
      await page.click('[data-testid="submit-button"]')

      // Assert: Success feedback
      await expect(page.locator('[data-testid="success-message"]')).toBeVisible()

      // Assert: Entity in list
      await expect(page.locator('[data-testid="entity-list"]')).toContainText('Valid Value')
    })

    test('should show validation error for invalid data', async ({ page }) => {
      await page.click('[data-testid="create-button"]')
      await page.fill('[data-testid="field1-input"]', 'x') // Too short
      await page.click('[data-testid="submit-button"]')

      await expect(page.locator('[data-testid="field1-error"]')).toBeVisible()
      await expect(page.locator('[data-testid="field1-error"]')).toContainText('at least')
    })

    test('should show loading state during submission', async ({ page }) => {
      await page.click('[data-testid="create-button"]')
      await page.fill('[data-testid="field1-input"]', 'Valid')

      const submitButton = page.locator('[data-testid="submit-button"]')
      await submitButton.click()

      await expect(submitButton).toBeDisabled()
      await expect(page.locator('[data-testid="loading-spinner"]')).toBeVisible()
    })
  })

  test.describe('Accessibility', () => {
    test('should support keyboard navigation', async ({ page }) => {
      await page.locator('[data-testid="create-button"]').focus()
      await page.keyboard.press('Enter')
      await expect(page.locator('[data-testid="create-modal"]')).toBeVisible()

      await page.keyboard.press('Tab')
      await page.keyboard.type('Value 1')

      await page.keyboard.press('Escape')
      await expect(page.locator('[data-testid="create-modal"]')).not.toBeVisible()
    })

    test('should have proper ARIA labels', async ({ page }) => {
      await page.click('[data-testid="create-button"]')

      const form = page.locator('form')
      await expect(form).toHaveAttribute('aria-label', /create/i)
      await expect(page.locator('[data-testid="field1-input"]')).toHaveAttribute('aria-label')
    })
  })
})
```

**Reference**: See `references/playwright-e2e-patterns.md` for complete patterns.

#### Step 5.3: E2E Test Checklist

- [ ] ✅ All CRUD flows tested
- [ ] ✅ Validation errors shown
- [ ] ✅ Loading states tested
- [ ] ✅ Success/error messages tested
- [ ] ✅ Keyboard navigation (Tab, Enter, Esc)
- [ ] ✅ ARIA labels tested
- [ ] ✅ Focus indicators tested
- [ ] ✅ All selectors use data-testid
- [ ] ✅ Tests isolated (don't depend on each other)
- [ ] ✅ ALL tests FAIL (no UI exists)

---

### PHASE 6: Validate and Document

**Purpose**: Verify test suite completeness and RED phase compliance.

#### Step 6.1: Verify All Tests FAIL

```bash
# Run unit/integration tests
npm run test

# Expected: ALL FAIL with "not defined" or "not implemented"
# ✗ use-cases/*.test.ts - FAIL (functions not defined)
# ✗ services/*.test.ts - FAIL (class not defined)
# ✗ route.test.ts - FAIL (handlers not defined)

# Run E2E tests
npm run test:e2e

# Expected: ALL FAIL (page not found / locators not found)
# ✗ e2e/{feature}.spec.ts - FAIL (no UI exists)
```

**⚠️ CRITICAL**: If ANY test passes, you've accidentally implemented code. Delete it and fix the test.

#### Step 6.2: Check Coverage Configuration

```bash
# Verify coverage config exists
cat vitest.config.ts

# Should have:
# coverage: {
#   provider: 'v8',
#   reporter: ['text', 'json', 'html'],
#   thresholds: {
#     lines: 90,
#     branches: 90,
#     functions: 90,
#     statements: 90
#   }
# }

npm run test:coverage
# Expected: 0% coverage (no implementation exists)
```

**Reference**: See `references/coverage-validation.md` for threshold configuration.

#### Step 6.3: Document Iteration

Create `test-agent/01-iteration.md` using template:

```markdown
# Test Agent - Iteration 01

**Agent**: Test Agent
**Date**: YYYY-MM-DD HH:MM
**Status**: Ready for Review
**Based on**: 00-request.md

---

## Context and Scope

[What you're testing and why]

## Work Completed

### Summary

Created comprehensive failing test suite for {feature} covering:
- Entity validation (25 tests)
- Use cases (40 tests)
- Services (30 tests)
- API routes (35 tests)
- E2E flows (20 tests)

**Total**: 150 tests, all FAIL appropriately

### Detailed Breakdown

#### Entity Tests
- File: `features/{feature}/entities.test.ts`
- Tests created: 25
- Scenarios: Valid data, invalid data, refinements, Create/Update schemas

#### Use Case Tests
- Files: `features/{feature}/use-cases/*.test.ts`
- Tests created: 40
- Scenarios: Happy path, validation, authorization, business rules, errors

[Continue for all layers...]

## Technical Decisions

**Decision 1**: Mock strategy
- **Rationale**: Use vi.mock for modules, vi.spyOn for methods
- **Alternative considered**: Manual mocks
- **Why rejected**: Less type-safe, more boilerplate

[More decisions...]

## Artifacts and Deliverables

### Files Created
- `features/{feature}/entities.test.ts` (25 tests)
- `features/{feature}/use-cases/create{Entity}.test.ts` (8 tests)
- `features/{feature}/use-cases/get{Entity}.test.ts` (6 tests)
[Complete list...]

## Evidence and Validation

### Test Results

\`\`\`bash
npm run test
# Output showing ALL tests FAIL
\`\`\`

### Coverage

\`\`\`bash
npm run test:coverage
# Coverage: 0% (expected - no implementation)
\`\`\`

## Coverage Against Requirements

| Requirement from 00-request.md | Status | Evidence |
|-------------------------------|--------|----------|
| Entity validation tests | ✅ Done | entities.test.ts:1-100 |
| Use case tests | ✅ Done | use-cases/*.test.ts |
| Service tests | ✅ Done | services/*.test.ts |
| API tests | ✅ Done | api/route.test.ts |
| E2E tests | ✅ Done | e2e/{feature}.spec.ts |

## Quality Checklist

- [x] All objectives from 00-request.md met
- [x] Tests fail appropriately (not syntax errors)
- [x] Mocks configured correctly
- [x] E2E tests with accessibility requirements
- [x] >90% coverage target planned
- [x] No functional logic implemented
- [x] All tests use approved tech stack

---

## Review Status

**Submitted for Review**: YYYY-MM-DD HH:MM

### Architect Review
**Status**: Pending
**Feedback**: (Architect fills)

### User Review
**Status**: Pending
**Feedback**: (User fills)
```

#### Step 6.4: Final Validation Checklist

- [ ] ✅ ALL tests FAIL appropriately
- [ ] ✅ Coverage config set to >90%
- [ ] ✅ NO implementation code exists
- [ ] ✅ Mocks configured for all external dependencies
- [ ] ✅ E2E tests cover all user flows
- [ ] ✅ Iteration document complete
- [ ] ✅ Ready for Architect + User review

**Notify completion**: "Test suite iteration ready for review"

---

## 🚫 ANTI-PATTERNS TO AVOID

### ❌ DON'T: Write Tests That Pass

```typescript
// ❌ WRONG: Meaningless test that passes
it('creates entity', () => {
  expect(true).toBe(true)
})
```

```typescript
// ✅ CORRECT: Test defines behavior (will fail)
it('creates entity', async () => {
  const result = await createEntity(validData, mockService)
  expect(result).toEqual(expectedEntity)
  // FAILS: createEntity is not defined yet
})
```

### ❌ DON'T: Use .parse() in Tests

```typescript
// ❌ WRONG: Throws, harder to test
it('validates', () => {
  expect(() => schema.parse(invalidData)).toThrow()
})
```

```typescript
// ✅ CORRECT: Returns result object
it('validates', () => {
  const result = schema.safeParse(invalidData)
  expect(result.success).toBe(false)
  if (!result.success) {
    expect(result.error.issues).toHaveLength(1)
  }
})
```

### ❌ DON'T: Implement Logic in Mocks

```typescript
// ❌ WRONG: Business logic in mock
vi.mock('./createEntity', () => ({
  createEntity: vi.fn(async (data) => {
    if (!data.field1) throw new Error('Required')
    return { id: 'uuid', ...data }
  })
}))
```

```typescript
// ✅ CORRECT: Simple mock, test defines behavior
vi.mock('./createEntity')
const mockCreate = vi.mocked(createEntity)

it('validates required field', async () => {
  await expect(
    createEntity({ /* missing field1 */ }, mockService)
  ).rejects.toThrow('field1 is required')
})
```

---

## 📚 REFERENCES (Load on Demand)

### When to Load References

- **Creating entity tests** → Load `references/zod-testing-patterns.md`
- **Mocking dependencies** → Load `references/vitest-patterns.md`
- **Creating E2E tests** → Load `references/playwright-e2e-patterns.md`
- **Organizing tests** → Load `references/test-structure-guide.md`
- **Validating coverage** → Load `references/coverage-validation.md`

**Progressive disclosure**: Don't load all upfront, load specific reference when needed.

---

## ✅ SUCCESS CRITERIA

Test suite is complete when:

- ✅ ALL tests FAIL appropriately (not syntax errors)
- ✅ >90% coverage target configured
- ✅ Entity tests cover all schemas and validation rules
- ✅ Use case tests cover all business logic scenarios
- ✅ Service tests cover all CRUD operations
- ✅ API tests cover all endpoints with auth/validation
- ✅ E2E tests cover all user workflows with accessibility
- ✅ Mocks configured for Supabase, use cases, auth
- ✅ Iteration documented following template
- ✅ NO implementation code exists (pure specification)

**Your success is measured by**: Can Implementer, Supabase Agent, and UI/UX Expert understand exactly what to build from your tests?

---

**YOU ARE THE SPECIFICATION. YOUR TESTS ARE THE TRUTH.**
