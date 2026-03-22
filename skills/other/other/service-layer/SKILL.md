---
name: service-layer
description: |
  Service layer patterns for this Next.js application.
  Covers static class pattern, RLS integration, standard method signatures, and BaseEntityService.
  Use this skill when implementing business logic or data access services.
allowed-tools: Read, Glob, Grep
version: 1.0.0
---

# Service Layer Skill

Patterns for implementing business logic and data access services with RLS integration.

## Architecture Overview

```
core/lib/services/
├── base-entity.service.ts    # Generic CRUD service base class
├── user.service.ts           # User management
├── team.service.ts           # Team CRUD and membership
├── team-member.service.ts    # Team membership management
├── permission.service.ts     # Permission checks (O(1))
├── membership.service.ts     # Complete membership context
├── subscription.service.ts   # Subscription lifecycle
├── plan.service.ts           # Plan queries
├── usage.service.ts          # Usage tracking and quotas
├── meta.service.ts           # Flexible entity metadata
├── invoice.service.ts        # Invoice management
├── theme.service.ts          # Theme registry queries
├── entity-type.service.ts    # Entity registry queries
└── ...

core/lib/db.ts                # RLS query functions
```

> **📍 Context-Aware Paths:** Paths shown assume monorepo development. In consumer projects,
> create in `contents/themes/{theme}/services/` instead. Core is read-only.
> See `core-theme-responsibilities` skill for complete rules.

## When to Use This Skill

- Implementing business logic services
- Creating data access layer for entities
- Working with RLS (Row Level Security)
- Implementing transactions
- Querying registries

## Static Class Pattern

**All services use static methods exclusively:**

```typescript
// core/lib/services/customer.service.ts

export class CustomerService {
  // No constructor - all methods are static
  // No instance state

  static async getById(id: string, userId: string): Promise<Customer | null> {
    // Implementation
  }

  static async list(userId: string, options?: ListOptions): Promise<ListResult<Customer>> {
    // Implementation
  }

  static async create(userId: string, teamId: string, data: CreateCustomer): Promise<Customer> {
    // Implementation
  }

  static async update(id: string, userId: string, data: UpdateCustomer): Promise<Customer> {
    // Implementation
  }

  static async delete(id: string, userId: string): Promise<boolean> {
    // Implementation
  }
}
```

**Usage (no instantiation):**
```typescript
import { CustomerService } from '@/core/lib/services/customer.service'

// Direct static method calls
const customer = await CustomerService.getById('cust-123', userId)
const customers = await CustomerService.list(userId, { limit: 10 })
const created = await CustomerService.create(userId, teamId, { name: 'Acme' })
```

## Standard Method Signatures

### Query Methods (Read Operations)

```typescript
// Get single entity by ID
static async getById(
  id: string,
  userId: string
): Promise<Entity | null>

// List with pagination, filtering, ordering
static async list(
  userId: string,
  options?: ListOptions
): Promise<ListResult<Entity>>

// Simple query (wrapper over list)
static async query(
  userId: string,
  options?: QueryOptions
): Promise<Entity[]>

// Check existence
static async exists(
  id: string,
  userId: string
): Promise<boolean>

// Count with optional filtering
static async count(
  userId: string,
  where?: Record<string, unknown>
): Promise<number>
```

### Mutation Methods (Write Operations)

```typescript
// Create new entity
static async create(
  userId: string,
  teamId: string,
  data: CreateEntity
): Promise<Entity>

// Update existing entity
static async update(
  id: string,
  userId: string,
  data: UpdateEntity
): Promise<Entity>

// Delete entity
static async delete(
  id: string,
  userId: string
): Promise<boolean>
```

### ListOptions Interface

```typescript
interface ListOptions {
  limit?: number                     // Pagination limit (default: 20)
  offset?: number                    // Pagination offset
  orderBy?: string                   // Sort field (default: 'createdAt')
  orderDir?: 'asc' | 'desc'         // Sort direction (default: 'desc')
  where?: Record<string, unknown>   // Filters
  search?: string                    // Text search
}

interface ListResult<T> {
  data: T[]
  total: number
  limit: number
  offset: number
}
```

## RLS Integration

### Core RLS Functions

```typescript
// core/lib/db.ts

// Query with RLS context (SELECT)
export async function queryWithRLS<T>(
  query: string,
  params: unknown[] = [],
  userId?: string | null
): Promise<T[]>

// Query single result with RLS
export async function queryOneWithRLS<T>(
  query: string,
  params: unknown[] = [],
  userId?: string | null
): Promise<T | null>

// Mutation with RLS (INSERT, UPDATE, DELETE)
export async function mutateWithRLS<T>(
  query: string,
  params: unknown[] = [],
  userId?: string | null
): Promise<{ rows: T[], rowCount: number }>
```

**RLS Context:**
- Functions set PostgreSQL `app.user_id` session variable
- RLS policies use this to filter/restrict data access
- Always pass `userId` parameter for proper isolation

### Service Implementation with RLS

```typescript
import { queryOneWithRLS, queryWithRLS, mutateWithRLS } from '@/core/lib/db'

export class CustomerService {
  static async getById(id: string, userId: string): Promise<Customer | null> {
    // Input validation
    if (!id?.trim()) throw new Error('Customer ID is required')
    if (!userId?.trim()) throw new Error('User ID is required')

    return queryOneWithRLS<Customer>(
      'SELECT * FROM "customers" WHERE id = $1',
      [id],
      userId  // Sets app.user_id for RLS
    )
  }

  static async list(userId: string, options: ListOptions = {}): Promise<ListResult<Customer>> {
    const { limit = 20, offset = 0, orderBy = 'createdAt', orderDir = 'desc' } = options

    const data = await queryWithRLS<Customer>(
      `SELECT * FROM "customers"
       ORDER BY "${orderBy}" ${orderDir.toUpperCase()}
       LIMIT $1 OFFSET $2`,
      [limit, offset],
      userId
    )

    const countResult = await queryOneWithRLS<{ count: number }>(
      'SELECT COUNT(*) as count FROM "customers"',
      [],
      userId
    )

    return {
      data,
      total: countResult?.count ?? 0,
      limit,
      offset
    }
  }

  static async create(userId: string, teamId: string, data: CreateCustomer): Promise<Customer> {
    const id = generateId()
    const now = new Date().toISOString()

    const result = await mutateWithRLS<Customer>(
      `INSERT INTO "customers" (id, "userId", "teamId", name, email, "createdAt", "updatedAt")
       VALUES ($1, $2, $3, $4, $5, $6, $7)
       RETURNING *`,
      [id, userId, teamId, data.name, data.email, now, now],
      userId
    )

    return result.rows[0]
  }

  static async update(id: string, userId: string, data: UpdateCustomer): Promise<Customer> {
    const setClauses: string[] = []
    const params: unknown[] = []
    let paramIndex = 1

    if (data.name !== undefined) {
      setClauses.push(`name = $${paramIndex++}`)
      params.push(data.name)
    }
    if (data.email !== undefined) {
      setClauses.push(`email = $${paramIndex++}`)
      params.push(data.email)
    }

    setClauses.push(`"updatedAt" = $${paramIndex++}`)
    params.push(new Date().toISOString())

    params.push(id)  // WHERE id = $N

    const result = await mutateWithRLS<Customer>(
      `UPDATE "customers"
       SET ${setClauses.join(', ')}
       WHERE id = $${paramIndex}
       RETURNING *`,
      params,
      userId
    )

    if (result.rowCount === 0) {
      throw new Error('Customer not found')
    }

    return result.rows[0]
  }

  static async delete(id: string, userId: string): Promise<boolean> {
    const result = await mutateWithRLS(
      'DELETE FROM "customers" WHERE id = $1',
      [id],
      userId
    )
    return result.rowCount > 0
  }
}
```

## Transaction Pattern

```typescript
import { getTransactionClient } from '@/core/lib/db'

export class TeamService {
  static async createWithOwner(
    userId: string,
    teamData: CreateTeam
  ): Promise<{ team: Team; membership: TeamMember }> {
    const tx = await getTransactionClient(userId)

    try {
      // Create team
      const team = await tx.queryOne<Team>(
        `INSERT INTO "teams" (id, name, slug, "createdAt")
         VALUES ($1, $2, $3, $4)
         RETURNING *`,
        [generateId(), teamData.name, teamData.slug, new Date().toISOString()]
      )

      // Add owner membership
      const membership = await tx.queryOne<TeamMember>(
        `INSERT INTO "teamMembers" (id, "userId", "teamId", role, "createdAt")
         VALUES ($1, $2, $3, $4, $5)
         RETURNING *`,
        [generateId(), userId, team.id, 'owner', new Date().toISOString()]
      )

      // Commit transaction
      await tx.commit()

      return { team, membership }
    } catch (error) {
      // Rollback on error
      await tx.rollback()
      throw error
    }
  }
}
```

## BaseEntityService

Generic base class for entity CRUD operations:

```typescript
// core/lib/services/base-entity.service.ts

export interface EntityServiceConfig {
  tableName: string                   // e.g., 'customers'
  fields: string[]                    // Custom fields (excluding system fields)
  searchableFields?: string[]         // Fields for text search
  defaultOrderBy?: string             // Default: 'createdAt'
  defaultOrderDir?: 'asc' | 'desc'   // Default: 'desc'
  defaultLimit?: number               // Default: 20
}

export class BaseEntityService<TEntity, TCreate, TUpdate> {
  protected config: EntityServiceConfig

  constructor(config: EntityServiceConfig) {
    this.config = {
      defaultOrderBy: 'createdAt',
      defaultOrderDir: 'desc',
      defaultLimit: 20,
      ...config
    }
  }

  async getById(id: string, userId: string): Promise<TEntity | null> { ... }
  async list(userId: string, options?: ListOptions): Promise<ListResult<TEntity>> { ... }
  async create(userId: string, teamId: string, data: TCreate): Promise<TEntity> { ... }
  async update(id: string, userId: string, data: TUpdate): Promise<TEntity> { ... }
  async delete(id: string, userId: string): Promise<boolean> { ... }
}
```

**Extending BaseEntityService:**
```typescript
class ProductsService extends BaseEntityService<Product, CreateProduct, UpdateProduct> {
  constructor() {
    super({
      tableName: 'products',
      fields: ['title', 'description', 'status', 'price'],
      searchableFields: ['title', 'description'],
    })
  }

  // Custom methods
  async getByStatus(userId: string, status: string): Promise<Product[]> {
    return this.query(userId, {
      where: { status },
      orderBy: 'createdAt'
    })
  }
}

// Usage
const service = new ProductsService()
const products = await service.list(userId, { search: 'laptop' })
```

## Service Categories

### Data Access Services
Use `queryWithRLS` and `mutateWithRLS` for database operations:
- UserService, TeamService, CustomerService
- SubscriptionService, InvoiceService
- Always accept `userId` parameter

### Registry Services
Query pre-generated registries (O(1) lookups):
- ThemeService, EntityTypeService
- NamespaceService, ScopeService
- Synchronous operations, no RLS needed

```typescript
// Registry service example
export class ThemeService {
  static getAll(): ThemeConfig[] {
    return Object.values(THEME_REGISTRY)
  }

  static getByName(name: string): ThemeConfig | undefined {
    return THEME_REGISTRY[name]
  }
}
```

### Composite Services
Combine multiple services for complex operations:
- MembershipService (TeamMember + Subscription + Permissions)
- Returns rich objects with helper methods

## Existing Services (24)

| Service | Category | Purpose |
|---------|----------|---------|
| `UserService` | Data | User management, profile |
| `TeamService` | Data | Team CRUD, slug management |
| `TeamMemberService` | Data | Membership, role management |
| `MetaService` | Data | Flexible entity metadata |
| `PermissionService` | Registry | O(1) permission checks |
| `MembershipService` | Composite | Complete membership context |
| `SubscriptionService` | Data | Subscription lifecycle |
| `PlanService` | Registry | Plan queries |
| `UsageService` | Data | Usage tracking, quotas |
| `InvoiceService` | Data | Invoice management |
| `ThemeService` | Registry | Theme configuration |
| `EntityTypeService` | Registry | Entity registry queries |
| `NamespaceService` | Registry | Route namespaces |
| `ScopeService` | Registry | API scopes |
| `MiddlewareService` | Registry | Middleware execution |
| `RouteHandlerService` | Registry | Route handlers |
| `PluginService` | Registry | Plugin configuration |
| `ApiRoutesService` | Registry | API route discovery |
| `BlockService` | Registry | Page builder blocks |
| `TemplateService` | Registry | Template management |
| `TranslationService` | Registry | I18n translations |
| `UserFlagsService` | Data | Feature flags |

## Error Handling

```typescript
static async getById(id: string, userId: string): Promise<Entity | null> {
  // Input validation
  if (!id || id.trim() === '') {
    throw new Error('Entity ID is required')
  }
  if (!userId || userId.trim() === '') {
    throw new Error('User ID is required for authentication')
  }

  try {
    return await queryOneWithRLS<Entity>(
      'SELECT * FROM "entities" WHERE id = $1',
      [id],
      userId
    )
  } catch (error) {
    console.error('EntityService.getById error:', error)
    throw new Error(
      error instanceof Error ? error.message : 'Failed to fetch entity'
    )
  }
}
```

## JSDoc Documentation

```typescript
/**
 * Get entity by ID
 *
 * @param id - Entity UUID
 * @param userId - Current user ID for RLS context
 * @returns Entity object or null if not found
 * @throws Error if ID or userId is missing
 *
 * @example
 * const customer = await CustomerService.getById('cust-123', userId)
 * if (customer) {
 *   console.log(customer.name)
 * }
 */
static async getById(id: string, userId: string): Promise<Customer | null> {
  // Implementation
}
```

## Anti-Patterns

```typescript
// NEVER: Instance methods
class BadService {
  async getById(id: string, userId: string) {}  // Not static!
}
const service = new BadService()  // Requires instantiation

// CORRECT: Static methods
class GoodService {
  static async getById(id: string, userId: string) {}
}
GoodService.getById('id', userId)  // No instantiation

// NEVER: Skip RLS
const customers = await query('SELECT * FROM customers')  // No RLS!

// CORRECT: Use RLS functions
const customers = await queryWithRLS('SELECT * FROM customers', [], userId)

// NEVER: Build SQL with string interpolation
const query = `SELECT * FROM customers WHERE name = '${name}'`  // SQL injection!

// CORRECT: Use parameterized queries
const query = 'SELECT * FROM customers WHERE name = $1'
await queryWithRLS(query, [name], userId)

// NEVER: Skip input validation
static async delete(id: string, userId: string) {
  await mutateWithRLS('DELETE FROM customers WHERE id = $1', [id], userId)
}

// CORRECT: Validate inputs
static async delete(id: string, userId: string) {
  if (!id?.trim()) throw new Error('ID is required')
  if (!userId?.trim()) throw new Error('User ID is required')
  await mutateWithRLS('DELETE FROM customers WHERE id = $1', [id], userId)
}

// NEVER: Forget to pass userId for RLS
await queryWithRLS(query, params)  // Missing userId!

// CORRECT: Always pass userId
await queryWithRLS(query, params, userId)
```

## Checklist

Before finalizing service implementation:

- [ ] All methods are static
- [ ] Uses RLS functions (queryWithRLS, mutateWithRLS)
- [ ] userId parameter on all database operations
- [ ] Input validation at method start
- [ ] Parameterized queries (no string interpolation)
- [ ] Proper error handling with descriptive messages
- [ ] JSDoc documentation with @param, @returns, @example
- [ ] Transactions for multi-step operations
- [ ] Consistent method signatures

## Related Skills

- `entity-system` - Entity definition patterns
- `entity-api` - API endpoint patterns
- `permissions-system` - Permission checking
- `database-migrations` - Migration patterns
