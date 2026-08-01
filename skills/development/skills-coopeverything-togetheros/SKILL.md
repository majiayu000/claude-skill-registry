---
name: skills-coopeverything-togetheros
description: This skill helps maintainers and contributors build the TogetherOS Reward
  System module efficiently. It provides templates, patterns, and guidance for creating
  well-structured, contributor-friendly issues and implementing features that follow
  TogetherOS principles.
---

# Reward Builder Skill

## Purpose

This skill helps maintainers and contributors build the TogetherOS Reward System module efficiently. It provides templates, patterns, and guidance for creating well-structured, contributor-friendly issues and implementing features that follow TogetherOS principles.

---

## Target Users

- **Maintainers:** Breaking down module into issues, reviewing PRs
- **Contributors:** First-time and experienced developers building features
- **Project Leads:** Planning sprints and prioritizing work

---

## Skill Capabilities

### 1. Issue Creation Templates
### 2. Code Implementation Patterns
### 3. Testing Strategies
### 4. PR Review Checklists
### 5. Documentation Standards

---

## 1. Issue Creation Templates

### Template: Entity Definition

```markdown
## Title
Define [EntityName] Entity

## Description
Create the core domain model for [entity purpose].

## Acceptance Criteria
- [ ] TypeScript interface defined in `packages/types/src/rewards.ts`
- [ ] All required fields documented with JSDoc comments
- [ ] Validation logic for field constraints
- [ ] Unit tests cover edge cases
- [ ] Type exports added to index.ts

## Technical Details

**File:** `packages/types/src/rewards.ts`

**Interface Structure:**
\`\`\`typescript
interface [EntityName] {
  id: string                    // UUID
  [field]: [type]              // [description]
  // ... more fields
}
\`\`\`

**Validation Rules:**
- [Rule 1]
- [Rule 2]

## Related Files
- `packages/validators/src/rewards.ts` (Zod schemas)
- `docs/modules/rewards.md` (specification reference)

## Size
`size:XS` (1-2 hours)

## Labels
`good-first-issue`, `module:rewards`, `type:entity`

## Help Available
Ask questions in Discussions #88 or tag @[maintainer]
```

---

### Template: Repository Implementation

```markdown
## Title
Implement [RepositoryName] with In-Memory Storage

## Description
Create repository interface and in-memory implementation for [entity].

## Acceptance Criteria
- [ ] Interface defined in `packages/rewards-domain/repos/[Name]Repo.ts`
- [ ] In-memory implementation in `InMemory[Name]Repo.ts`
- [ ] CRUD operations implemented (create, find, update, delete)
- [ ] Fixture seed data for testing
- [ ] Unit tests achieve 90%+ coverage
- [ ] Repository exports added to index.ts

## Technical Details

**Interface Methods:**
\`\`\`typescript
export interface [Name]Repo {
  create(input: Create[Name]Input): Promise<[Name]>
  findById(id: string): Promise<[Name] | null>
  list(filters: [Name]Filters): Promise<[Name][]>
  update(id: string, updates: Partial<[Name]>): Promise<[Name]>
  delete(id: string): Promise<void>
}
\`\`\`

**In-Memory Implementation:**
- Use `Map<string, [Name]>` for storage
- Implement filtering logic
- Handle not-found cases gracefully

## Files to Create
- `packages/rewards-domain/repos/[Name]Repo.ts` (interface)
- `packages/rewards-domain/repos/InMemory[Name]Repo.ts` (implementation)
- `packages/rewards-domain/repos/__tests__/[Name]Repo.test.ts` (tests)

## Dependencies
- Requires: [EntityName] entity defined
- Blocks: API handlers for [entity]

## Size
`size:S` (2-4 hours)

## Labels
`module:rewards`, `type:repository`

## Testing Guidance
See "Repository Testing Pattern" in this skill document.
```

---

### Template: API Endpoint

```markdown
## Title
Create [METHOD] /api/rewards/[route] Endpoint

## Description
Implement API endpoint for [action description].

## Acceptance Criteria
- [ ] Handler created in `apps/api/src/modules/rewards/handlers/[name].ts`
- [ ] Zod schema validates input
- [ ] Repository integration works
- [ ] Error handling covers all cases (401, 403, 422, 500)
- [ ] Contract tests pass
- [ ] API documented in rewards.md spec

## Technical Details

**Endpoint:** `[METHOD] /api/rewards/[route]`

**Request Schema:**
\`\`\`typescript
const [name]Schema = z.object({
  // fields
})
\`\`\`

**Response (Success):**
\`\`\`typescript
[status] [Status Text]
{
  // response body
}
\`\`\`

**Error Responses:**
- `401 Unauthorized` — Missing/invalid auth
- `403 Forbidden` — Insufficient permissions
- `422 Unprocessable Entity` — Validation failed
- `500 Internal Server Error` — Unexpected failure

## Files to Create/Modify
- `apps/api/src/modules/rewards/handlers/[name].ts`
- `packages/validators/src/rewards.ts` (add schema)
- `apps/api/src/modules/rewards/handlers/__tests__/[name].test.ts`

## Dependencies
- Requires: [Repository] implementation
- Requires: [Entity] definition

## Size
`size:S` (2-4 hours)

## Labels
`module:rewards`, `type:api-endpoint`

## Testing Guidance
See "API Contract Testing Pattern" in this skill document.
```

---

### Template: GitHub Integration

```markdown
## Title
Implement GitHub [EventType] Webhook Handler

## Description
Handle [event type] webhooks from GitHub and create reward events.

## Acceptance Criteria
- [ ] Webhook handler receives and validates GitHub payload
- [ ] Event data extracted correctly
- [ ] GitHub user mapped to TogetherOS member
- [ ] RewardEvent created with correct weight
- [ ] Signature verification implemented
- [ ] Deduplication prevents double-counting
- [ ] Integration tests pass with sample payloads

## Technical Details

**Webhook Event:** `[github_event_name]`

**Payload Structure:**
\`\`\`typescript
interface [EventName]Payload {
  // GitHub webhook payload fields
}
\`\`\`

**Event Mapping:**
\`\`\`typescript
{
  event_type: '[reward_event_type]',
  context: {
    // extracted context
  },
  weight: [calculated_weight]
}
\`\`\`

**Weight Calculation:**
[Describe logic]

## Files to Create/Modify
- `apps/api/src/modules/rewards/handlers/githubWebhook.ts`
- `apps/api/src/modules/rewards/lib/calculateWeight.ts`
- `apps/api/src/modules/rewards/__tests__/githubWebhook.test.ts`

## Sample Payloads
Create test fixtures in `packages/rewards-fixtures/github/`

## Size
`size:M` (4-6 hours)

## Labels
`module:rewards`, `type:integration`, `priority:high`

## Security Considerations
- Verify webhook signature using GitHub secret
- Validate payload structure before processing
- Rate limit webhook endpoint
```

---

### Template: UI Component

```markdown
## Title
Create [ComponentName] UI Component

## Description
Build [component purpose] for member profiles/dashboard.

## Acceptance Criteria
- [ ] Component created in `packages/ui/src/rewards/[ComponentName].tsx`
- [ ] Props interface defined and documented
- [ ] All states handled (loading, empty, error, success)
- [ ] Accessible (keyboard nav, ARIA labels, screen readers)
- [ ] Storybook stories for all states
- [ ] Tailwind styling follows design system
- [ ] Responsive design (mobile, tablet, desktop)

## Technical Details

**Component API:**
\`\`\`typescript
interface [ComponentName]Props {
  [prop]: [type]
  // ... more props
}
\`\`\`

**States to Handle:**
\`\`\`typescript
type ComponentState =
  | { status: 'loading' }
  | { status: 'empty' }
  | { status: 'error'; error: Error }
  | { status: 'success'; data: [Type] }
\`\`\`

**Storybook Stories:**
- Default
- Loading
- Empty
- Error
- With Data (multiple scenarios)

## Files to Create
- `packages/ui/src/rewards/[ComponentName].tsx`
- `packages/ui/src/rewards/[ComponentName].stories.tsx`
- `packages/ui/src/rewards/__tests__/[ComponentName].test.tsx`

## Design Reference
[Link to design mockup if available]

## Size
`size:M` (4-6 hours)

## Labels
`module:rewards`, `type:ui-component`

## Accessibility Checklist
See "UI Component Accessibility" section in this skill.
```

---

## 2. Code Implementation Patterns

### Pattern: Entity Definition

```typescript
// packages/types/src/rewards.ts

/**
 * Represents a contribution event that earns rewards.
 *
 * Events are immutable records of actions taken by members
 * that contribute value to the cooperative.
 */
export interface RewardEvent {
  /** Unique identifier (UUID v4) */
  id: string

  /** Member who performed the action */
  actor_id: string

  /** Type of contribution event */
  event_type: RewardEventType

  /** When the event occurred (ISO 8601) */
  timestamp: Date

  /** Domain-specific metadata */
  context: EventContext

  /** Origin system (github, forum, bridge) */
  source: string

  /** Support Points value */
  weight: number

  /** Processing status */
  status: 'pending' | 'processed' | 'rejected'

  /** When event was processed */
  processed_at?: Date
}

/**
 * Contribution event types across all cooperation domains.
 */
export type RewardEventType =
  // Code & Infrastructure
  | 'pr_merged'
  | 'pr_reviewed'
  | 'issue_created'
  | 'issue_triaged'
  | 'bug_fixed'
  | 'docs_contribution'
  // Add more as needed

/**
 * Domain-specific context for events.
 * Structure varies by event_type.
 */
export interface EventContext {
  // GitHub-specific
  pr_number?: number
  pr_size?: 'small' | 'medium' | 'large'
  files_changed?: number
  lines_changed?: number
  repository?: string

  // Extensible for other domains
  [key: string]: any
}
```

**Best Practices:**
- ✅ Use JSDoc comments for all interfaces and fields
- ✅ Define union types explicitly (no `string` for enums)
- ✅ Make optional fields explicit with `?`
- ✅ Use Date objects, not strings (convert on boundaries)
- ✅ Keep entities pure (no framework dependencies)

---

### Pattern: Repository Interface

```typescript
// packages/rewards-domain/repos/RewardEventRepo.ts

import { RewardEvent, RewardEventType, EventContext } from '@togetheros/types'

/**
 * Repository interface for managing reward events.
 *
 * Implementations can use in-memory storage, databases,
 * or external services while maintaining the same contract.
 */
export interface RewardEventRepo {
  /**
   * Create a new reward event.
   *
   * @throws {ValidationError} If input invalid
   * @throws {DuplicateError} If event already exists
   */
  create(input: CreateRewardEventInput): Promise<RewardEvent>

  /**
   * Find event by unique ID.
   *
   * @returns Event if found, null otherwise
   */
  findById(id: string): Promise<RewardEvent | null>

  /**
   * List events for a specific member.
   *
   * @param memberId - Member UUID
   * @param filters - Optional filtering criteria
   * @returns Array of matching events
   */
  findByMember(memberId: string, filters?: EventFilters): Promise<RewardEvent[]>

  /**
   * Find all pending (unprocessed) events.
   *
   * Used by reward processing job to calculate balances.
   */
  findPending(): Promise<RewardEvent[]>

  /**
   * Mark event as processed.
   *
   * Called after Support Points calculated and awarded.
   */
  markProcessed(id: string): Promise<void>

  /**
   * Check if event already exists.
   *
   * Prevents duplicate rewards for same action.
   */
  checkDuplicate(source: string, context: EventContext): Promise<boolean>
}

/**
 * Input for creating a new reward event.
 */
export interface CreateRewardEventInput {
  actor_id: string
  event_type: RewardEventType
  source: string
  context: EventContext
}

/**
 * Filters for querying events.
 */
export interface EventFilters {
  event_types?: RewardEventType[]
  date_range?: { start: Date; end: Date }
  status?: 'pending' | 'processed' | 'rejected'
  limit?: number
}
```

**Best Practices:**
- ✅ Define clear interface boundaries
- ✅ Use async/await (Promises) for all methods
- ✅ Document error conditions with @throws
- ✅ Keep methods focused (single responsibility)
- ✅ Use descriptive parameter names

---

### Pattern: In-Memory Repository

```typescript
// packages/rewards-domain/repos/InMemoryRewardEventRepo.ts

import { RewardEvent, RewardEventType } from '@togetheros/types'
import { RewardEventRepo, CreateRewardEventInput, EventFilters } from './RewardEventRepo'
import { generateId } from '../lib/uuid'
import { calculateWeight } from '../lib/calculateWeight'

/**
 * In-memory implementation of RewardEventRepo.
 *
 * Used for testing and MVP phase before database integration.
 * NOT suitable for production (data lost on restart).
 */
export class InMemoryRewardEventRepo implements RewardEventRepo {
  private events: Map<string, RewardEvent> = new Map()

  async create(input: CreateRewardEventInput): Promise<RewardEvent> {
    // Check for duplicates
    const isDupe = await this.checkDuplicate(input.source, input.context)
    if (isDupe) {
      throw new Error('Event already exists')
    }

    // Create event
    const event: RewardEvent = {
      id: generateId(),
      actor_id: input.actor_id,
      event_type: input.event_type,
      timestamp: new Date(),
      context: input.context,
      source: input.source,
      weight: calculateWeight(input.event_type, input.context),
      status: 'pending',
    }

    this.events.set(event.id, event)
    return event
  }

  async findById(id: string): Promise<RewardEvent | null> {
    return this.events.get(id) || null
  }

  async findByMember(memberId: string, filters?: EventFilters): Promise<RewardEvent[]> {
    let results = Array.from(this.events.values())
      .filter(e => e.actor_id === memberId)

    // Apply filters
    if (filters?.event_types) {
      results = results.filter(e => filters.event_types!.includes(e.event_type))
    }

    if (filters?.date_range) {
      results = results.filter(e =>
        e.timestamp >= filters.date_range!.start &&
        e.timestamp <= filters.date_range!.end
      )
    }

    if (filters?.status) {
      results = results.filter(e => e.status === filters.status)
    }

    // Apply limit
    const limit = filters?.limit || 100
    return results.slice(0, limit)
  }

  async findPending(): Promise<RewardEvent[]> {
    return Array.from(this.events.values())
      .filter(e => e.status === 'pending')
  }

  async markProcessed(id: string): Promise<void> {
    const event = this.events.get(id)
    if (event) {
      event.status = 'processed'
      event.processed_at = new Date()
    }
  }

  async checkDuplicate(source: string, context: EventContext): Promise<boolean> {
    // Simple duplicate check based on source + key context fields
    const key = this.generateDuplicateKey(source, context)

    return Array.from(this.events.values()).some(e =>
      this.generateDuplicateKey(e.source, e.context) === key
    )
  }

  private generateDuplicateKey(source: string, context: EventContext): string {
    // Create unique key from source + relevant context
    // Adjust based on event type
    if (context.pr_number) {
      return `${source}:pr:${context.pr_number}`
    }
    if (context.issue_number) {
      return `${source}:issue:${context.issue_number}`
    }
    // Fallback: stringify entire context
    return `${source}:${JSON.stringify(context)}`
  }
}
```

**Best Practices:**
- ✅ Implement full interface (no partial implementations)
- ✅ Handle edge cases (nulls, empty arrays, not found)
- ✅ Add private helper methods for clarity
- ✅ Document limitations (e.g., "not for production")
- ✅ Use Map/Set for efficient lookups

---

### Pattern: Zod Validation Schema

```typescript
// packages/validators/src/rewards.ts

import { z } from 'zod'

/**
 * Schema for creating a reward event via API.
 */
export const createRewardEventSchema = z.object({
  actor_id: z.string().uuid('Invalid member UUID'),
  event_type: z.enum([
    'pr_merged',
    'pr_reviewed',
    'issue_created',
    'issue_triaged',
    'bug_fixed',
    'docs_contribution',
  ]),
  source: z.string().min(1),
  context: z.record(z.any()), // Flexible for different event types
})

export type CreateRewardEventInput = z.infer<typeof createRewardEventSchema>

/**
 * Schema for PR merge context.
 */
export const prMergeContextSchema = z.object({
  pr_number: z.number().int().positive(),
  pr_size: z.enum(['small', 'medium', 'large']),
  files_changed: z.number().int().nonnegative(),
  lines_changed: z.number().int().nonnegative(),
  repository: z.string(),
})

/**
 * Schema for filtering events.
 */
export const eventFiltersSchema = z.object({
  event_types: z.array(z.string()).optional(),
  date_range: z.object({
    start: z.coerce.date(),
    end: z.coerce.date(),
  }).optional(),
  status: z.enum(['pending', 'processed', 'rejected']).optional(),
  limit: z.number().int().positive().max(100).optional(),
})

export type EventFilters = z.infer<typeof eventFiltersSchema>
```

**Best Practices:**
- ✅ Use descriptive error messages
- ✅ Validate all inputs at API boundaries
- ✅ Use z.infer to generate TypeScript types
- ✅ Separate schemas for different contexts
- ✅ Set reasonable limits (max array size, string length)

---

### Pattern: API Handler

```typescript
// apps/api/src/modules/rewards/handlers/createEvent.ts

import { createRewardEventSchema } from '@togetheros/validators'
import { RewardEventRepo } from '@togetheros/rewards-domain/repos'

/**
 * Handle POST /api/rewards/events
 *
 * Creates a new reward event from external systems.
 */
export async function createEvent(
  request: Request,
  repo: RewardEventRepo
): Promise<Response> {
  try {
    // Parse and validate input
    const body = await request.json()
    const data = createRewardEventSchema.parse(body)

    // Create event
    const event = await repo.create(data)

    // Return success
    return Response.json(
      {
        id: event.id,
        weight: event.weight,
        processed: event.status === 'processed',
      },
      { status: 201 }
    )
  } catch (error) {
    // Handle validation errors
    if (error instanceof z.ZodError) {
      return Response.json(
        {
          error: {
            code: 'VALIDATION_ERROR',
            message: 'Invalid input',
            details: error.errors,
          }
        },
        { status: 422 }
      )
    }

    // Handle duplicate errors
    if (error.message === 'Event already exists') {
      return Response.json(
        {
          error: {
            code: 'EVENT_ALREADY_PROCESSED',
            message: 'Event with this source and context already exists',
          }
        },
        { status: 409 }
      )
    }

    // Handle unexpected errors
    console.error('Error creating reward event:', error)
    return Response.json(
      {
        error: {
          code: 'INTERNAL_ERROR',
          message: 'An unexpected error occurred',
        }
      },
      { status: 500 }
    )
  }
}
```

**Best Practices:**
- ✅ Validate input with Zod schemas
- ✅ Handle all error types explicitly
- ✅ Return appropriate HTTP status codes
- ✅ Use consistent error response format
- ✅ Log errors for debugging (never expose internals to client)

---

## 3. Testing Strategies

### Unit Test Pattern: Entity

```typescript
// packages/rewards-domain/__tests__/RewardEvent.test.ts

import { describe, it, expect } from 'vitest'
import { createRewardEvent } from '../lib/createRewardEvent'

describe('RewardEvent', () => {
  it('creates event with valid input', () => {
    const event = createRewardEvent({
      actor_id: 'member-123',
      event_type: 'pr_merged',
      source: 'github',
      context: { pr_number: 42 }
    })

    expect(event.id).toBeDefined()
    expect(event.actor_id).toBe('member-123')
    expect(event.status).toBe('pending')
  })

  it('calculates weight for small PR', () => {
    const event = createRewardEvent({
      event_type: 'pr_merged',
      context: { pr_size: 'small' }
    })

    expect(event.weight).toBe(5)
  })

  it('calculates weight for medium PR', () => {
    const event = createRewardEvent({
      event_type: 'pr_merged',
      context: { pr_size: 'medium' }
    })

    expect(event.weight).toBe(10)
  })

  it('throws on invalid actor_id', () => {
    expect(() => createRewardEvent({
      actor_id: 'not-a-uuid',
      event_type: 'pr_merged'
    })).toThrow('Invalid member UUID')
  })
})
```

---

### Unit Test Pattern: Repository

```typescript
// packages/rewards-domain/repos/__tests__/RewardEventRepo.test.ts

import { describe, it, expect, beforeEach } from 'vitest'
import { InMemoryRewardEventRepo } from '../InMemoryRewardEventRepo'

describe('RewardEventRepo', () => {
  let repo: InMemoryRewardEventRepo

  beforeEach(() => {
    repo = new InMemoryRewardEventRepo()
  })

  describe('create', () => {
    it('creates event successfully', async () => {
      const event = await repo.create({
        actor_id: 'member-123',
        event_type: 'pr_merged',
        source: 'github',
        context: { pr_number: 42 }
      })

      expect(event.id).toBeDefined()
      expect(event.actor_id).toBe('member-123')
    })

    it('prevents duplicate events', async () => {
      await repo.create({
        source: 'github',
        context: { pr_number: 42 }
      })

      await expect(repo.create({
        source: 'github',
        context: { pr_number: 42 }
      })).rejects.toThrow('Event already exists')
    })
  })

  describe('findByMember', () => {
    it('returns all events for member', async () => {
      await repo.create({ actor_id: 'member-123', ... })
      await repo.create({ actor_id: 'member-123', ... })
      await repo.create({ actor_id: 'member-456', ... })

      const events = await repo.findByMember('member-123')
      expect(events).toHaveLength(2)
    })

    it('filters by event type', async () => {
      await repo.create({ event_type: 'pr_merged', ... })
      await repo.create({ event_type: 'pr_reviewed', ... })

      const events = await repo.findByMember('member-123', {
        event_types: ['pr_merged']
      })
      expect(events).toHaveLength(1)
      expect(events[0].event_type).toBe('pr_merged')
    })

    it('respects limit', async () => {
      for (let i = 0; i < 10; i++) {
        await repo.create({ actor_id: 'member-123', ... })
      }

      const events = await repo.findByMember('member-123', { limit: 5 })
      expect(events).toHaveLength(5)
    })
  })
})
```

---

### Contract Test Pattern: API

```typescript
// apps/api/src/modules/rewards/__tests__/createEvent.test.ts

import { describe, it, expect } from 'vitest'
import { createRewardEventSchema } from '@togetheros/validators'

describe('POST /api/rewards/events', () => {
  describe('input validation', () => {
    it('accepts valid input', () => {
      const result = createRewardEventSchema.safeParse({
        actor_id: '550e8400-e29b-41d4-a716-446655440000',
        event_type: 'pr_merged',
        source: 'github',
        context: { pr_number: 42 }
      })

      expect(result.success).toBe(true)
    })

    it('rejects invalid actor_id', () => {
      const result = createRewardEventSchema.safeParse({
        actor_id: 'not-a-uuid',
        event_type: 'pr_merged',
        source: 'github',
        context: {}
      })

      expect(result.success).toBe(false)
    })

    it('rejects unknown event_type', () => {
      const result = createRewardEventSchema.safeParse({
        actor_id: '550e8400-e29b-41d4-a716-446655440000',
        event_type: 'unknown_type',
        source: 'github',
        context: {}
      })

      expect(result.success).toBe(false)
    })
  })
})
```

---

## 4. PR Review Checklist

### For Reviewers

**Code Quality:**
- [ ] Follows TogetherOS code style and patterns
- [ ] No unnecessary complexity or premature optimization
- [ ] Functions are small and focused (single responsibility)
- [ ] Variable names are descriptive and clear
- [ ] Comments explain "why", not "what"

**Testing:**
- [ ] Unit tests cover all code paths
- [ ] Contract tests validate API schemas
- [ ] Edge cases are tested (nulls, empty arrays, errors)
- [ ] Test coverage is >80% (aim for 90%+)

**Documentation:**
- [ ] JSDoc comments on all exported functions/interfaces
- [ ] README updated if public API changed
- [ ] Module spec updated if behavior changed

**TogetherOS Principles:**
- [ ] One tiny change per PR (smallest shippable increment)
- [ ] Docs-first: spec matches implementation
- [ ] Privacy-first: no PII exposure, IP hashing if needed
- [ ] Validation: Zod schemas validate all inputs

**CI/CD:**
- [ ] PR includes proof lines in description
- [ ] All CI checks pass (ci/lint, ci/docs, ci/smoke)
- [ ] No linting errors or warnings
- [ ] Branch targets `Claude-1st-build` (not main)

**Path Labels:**
- [ ] PR tagged with correct Cooperation Path
- [ ] Keywords listed in PR description

**Git Hygiene:**
- [ ] Commit messages follow convention (type(scope): message)
- [ ] No merge commits (rebase preferred)
- [ ] Single focused change (not multiple unrelated changes)

---

## 5. Documentation Standards

### Module Spec Format

Every module needs a comprehensive spec in `docs/modules/[module].md`:

**Required Sections:**
1. **Overview** — Purpose, status, priority
2. **Why This Exists** — Problem/solution, outcomes
3. **Core Principles** — Non-negotiables
4. **Implementation Sequence** — Phases A/B/C/D
5. **Data Models** — Complete entity specifications
6. **API Contracts** — Request/response schemas
7. **UI Components** — Component specs (if applicable)
8. **Repository Pattern** — Interface + implementation guide
9. **Testing Strategy** — Unit/contract/integration patterns
10. **Definition of Done** — Acceptance checklist
11. **Contributing** — How developers can help
12. **Related KB Files** — Links to dependencies

---

### JSDoc Standards

```typescript
/**
 * Brief one-line description of what this does.
 *
 * More detailed explanation if needed. Explain why this exists,
 * what problem it solves, and any important constraints.
 *
 * @param paramName - Description of parameter
 * @param optionalParam - Optional parameter description
 * @returns Description of return value
 * @throws {ErrorType} When this error occurs
 *
 * @example
 * ```typescript
 * const result = functionName('input')
 * console.log(result) // Expected output
 * ```
 */
export function functionName(
  paramName: string,
  optionalParam?: number
): ReturnType {
  // Implementation
}
```

---

### Inline Comment Guidelines

**DO comment:**
- Why a specific approach was chosen
- Business logic or domain rules
- Complex algorithms or calculations
- Workarounds for known issues
- TODOs with context

**DON'T comment:**
- What the code does (code should be self-documenting)
- Obvious operations
- Auto-generated comments

**Examples:**

✅ Good:
```typescript
// Use SHA-256 for deduplication to balance privacy and uniqueness
const key = createHash('sha256').update(data).digest('hex')

// Cooldown prevents spam: max 5 PRs/day counted toward rewards
if (prCountToday >= 5) return
```

❌ Bad:
```typescript
// Create a hash
const key = createHash('sha256').update(data).digest('hex')

// Check if greater than 5
if (prCountToday >= 5) return
```

---

## Skill Usage Examples

### Example 1: Creating Entity Definition Issue

**Maintainer Task:** Break down "Event Model" into actionable issue

**Use Skill:**
1. Open "1. Issue Creation Templates" → "Template: Entity Definition"
2. Fill in placeholders:
   - `[EntityName]` → `RewardEvent`
   - `[entity purpose]` → `contribution events that earn rewards`
3. Copy template to GitHub Issues
4. Add labels: `good-first-issue`, `module:rewards`, `type:entity`, `size:XS`
5. Assign to project board

**Result:** Clear, actionable issue ready for contributor pickup

---

### Example 2: Implementing Repository

**Contributor Task:** Implement InMemoryRewardEventRepo

**Use Skill:**
1. Read "2. Code Implementation Patterns" → "Pattern: Repository Interface"
2. Copy interface boilerplate
3. Read "Pattern: In-Memory Repository"
4. Implement methods following pattern
5. Read "3. Testing Strategies" → "Unit Test Pattern: Repository"
6. Write tests matching pattern
7. Submit PR with proof lines

**Result:** High-quality implementation matching TogetherOS standards

---

### Example 3: Reviewing PR

**Maintainer Task:** Review PR for reward event creation

**Use Skill:**
1. Open "4. PR Review Checklist"
2. Go through each section systematically
3. Leave specific feedback referencing patterns
4. If issues found, link to relevant skill sections
5. Approve when all boxes checked

**Result:** Thorough, constructive review ensuring quality

---

## Maintenance & Updates

### When to Update This Skill

- New issue type identified (add template)
- Code pattern evolves (update example)
- Test strategy improves (add new pattern)
- PR review catches common issue (add to checklist)
- Documentation standard changes (update guidelines)

### Update Process

1. Identify improvement needed
2. Update relevant section
3. Add example if helpful
4. Test with real issue/PR
5. Commit with clear message

---

## Success Metrics

**For Maintainers:**
- Time to create issue reduced from 20min → 5min
- Issue quality consistent across all created
- Fewer "what should I do?" questions

**For Contributors:**
- First-time contributors ship PRs faster
- Code reviews have fewer rounds
- Tests follow standard patterns
- Documentation complete on first submission

**For Project:**
- More contributors able to participate
- Higher quality contributions
- Faster feature delivery
- Better maintainability

---

## Related Documentation

- [Rewards Module Spec](../docs/modules/rewards.md) — Complete technical specification
- [Main KB](../docs/togetheros-kb.md) — Core principles and workflow
- [CI/CD Discipline](../docs/ci-cd-discipline.md) — Validation and proof lines
- [Architecture](../docs/architecture.md) — Domain-driven design patterns
- [Cooperation Paths](../docs/cooperation-paths.md) — All 8 contribution domains
